"""
AI Meal Planner Pipeline
========================
Implements the strict separation between AI decision logic and Python computation.

Flow (always):
  1. Python backend generates a "decision packet" (facts only — costs, nutrition, distances)
  2. Decision packet → structured prompt → Nemotron AI
  3. Nemotron returns a JSON "decision result" (store + meals + reasoning)
  4. Python validates every AI field against known stores and meals
  5. Python computes all numbers (costs, nutrition totals) using validated choices
  6. Final structured result returned to server.py

Rules enforced here:
  ✅ AI chooses: which store, which meals, reasoning text
  ❌ AI never sets: prices, distances, nutrition numbers, calories, DB writes
  ✅ Python is always the source of truth for every numeric value
"""

import os
import sys
import json
import re
from typing import Optional

# Add Backend/ to sys.path so we can import its modules
_BACKEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Backend")
if _BACKEND_DIR not in sys.path:
    sys.path.insert(0, _BACKEND_DIR)

from meal_planner_data_processor import generate_decision_packet  # noqa: E402
from Model import ask_model  # noqa: E402


# ---------------------------------------------------------------------------
# STEP 2: Strict JSON schema the AI must return
# ---------------------------------------------------------------------------
_SCHEMA_COMMENT = """\
{
  "recommended_store": "exact store name from the AVAILABLE STORES list",
  "selected_meals":    ["exact meal name 1", "exact meal name 2"],
  "reasoning":         "1-2 sentences explaining your choices",
  "notes":             "any caveats about pricing or availability (can be empty string)"
}"""


def _build_ai_prompt(user_message: str, decision_packet: dict) -> list:
    """
    STEP 2 — Build the prompt that sends the decision packet to Nemotron.
    All numeric facts come from the decision packet (Python-computed).
    The AI only chooses names and writes reasoning text.
    """
    profile = decision_packet["user_profile"]

    # Separate hard allergies from diet style so the AI doesn't refuse to suggest meals
    restrictions = profile.get('dietary_restrictions') or []
    diet_style = profile.get('diet_preference') or ''
    hard_allergies = [r for r in restrictions if r not in (
        'vegan', 'vegetarian', 'pescatarian', 'low-fat', 'low-carb',
        'low-sodium', 'keto', 'paleo', 'mediterranean', 'normal', 'none', ''
    )]
    allergies_text = ', '.join(hard_allergies) if hard_allergies else 'none'
    diet_style_text = diet_style or (restrictions[0] if restrictions else 'none')

    # Summarize stores (Python-computed totals — AI reads but never changes these)
    store_lines = []
    for s in decision_packet["stores"]:
        store_lines.append(
            f"  • {s['name']}: total=${s['total_cost']:.2f}  "
            f"distance={s['distance_miles']}mi  "
            f"pricing={s['confidence']}"
        )
    stores_text = "\n".join(store_lines)

    # Number the meals so the AI can reference them precisely
    meal_lines = []
    meal_names_list = []
    for i, m in enumerate(decision_packet["meals"], 1):
        name = m['name']
        meal_names_list.append(f'"{name}"')
        meal_lines.append(
            f"  {i}. {name}\n"
            f"     calories=~{m['nutrition'].get('calories', 0):.0f}  "
            f"time={m['cook_time_minutes']}min  "
            f"equipment={','.join(m['equipment_required'])}"
        )
    meals_text = "\n".join(meal_lines)
    valid_meal_names = ", ".join(meal_names_list)

    # Build readable macro goals for the prompt
    protein_goal = profile.get('protein_goal')
    fat_goal     = profile.get('fat_goal')
    carb_goal    = profile.get('carb_goal')
    macro_lines  = []
    if protein_goal and str(protein_goal).lower() not in ('normal', 'none', ''):
        macro_lines.append(f"protein target ≥ {protein_goal}g")
    if fat_goal:
        macro_lines.append(f"fat target ≤ {fat_goal}g")
    if carb_goal:
        macro_lines.append(f"carb target ≤ {carb_goal}g")
    macros_text = ', '.join(macro_lines) if macro_lines else 'none set'

    dieting      = profile.get('dieting', 'no')
    cooking_skill = profile.get('cooking_skill', 'beginner')
    weekly_budget = profile.get('weekly_budget', 100)

    system_content = f"""You are a meal planning assistant. All prices, distances, nutrition, and \
store data below were computed by the backend system — do NOT invent or change any numbers. \
Your ONLY job is to choose names from the numbered lists below and write a short explanation.

USER PROFILE:
  Preferred diet style: {diet_style_text}
  Actively dieting / calorie cutting: {dieting}
  Hard food allergies (avoid these ingredients): {allergies_text}
  Daily calorie target: {profile.get('daily_calories', 2000)} kcal
  Macro goals: {macros_text}
  Cooking skill: {cooking_skill}
  Available equipment: {profile.get('available_equipment', ['stove', 'oven', 'microwave'])}
  Max cook time per meal: {profile.get('max_time_minutes', 45)} min
  Budget per meal: ${profile.get('budget', 15)}
  Weekly grocery budget: ${weekly_budget}
  Max store distance: {profile.get('max_distance_miles', 10)} miles

AVAILABLE STORES (pick one — use the exact name):
{stores_text}

AVAILABLE MEALS — YOU MUST ONLY USE NAMES FROM THIS EXACT LIST, COPIED CHARACTER FOR CHARACTER:
{meals_text}

VALID MEAL NAMES (copy one or more of these strings exactly into selected_meals):
  [{valid_meal_names}]

YOUR TASK:
1. Pick the best store from AVAILABLE STORES.
2. Pick 2–4 meals from the VALID MEAL NAMES list that best fit the user's preferred diet style and request.
   IMPORTANT: You MUST always pick at least 2 meals. If no meal perfectly matches the diet style,
   pick the closest available options and explain the trade-off in your reasoning.
3. Write a 1-2 sentence reasoning and an optional notes string.

CRITICAL RULES — failure to follow these means your answer is wrong:
  • Output ONLY valid JSON — no markdown, no prose, no code fences, no <think> tags.
  • The value of "recommended_store" MUST be copied exactly from AVAILABLE STORES.
  • Every item in "selected_meals" MUST be copied exactly from VALID MEAL NAMES above.
  • "selected_meals" MUST contain at least 2 meal names — NEVER leave it empty.
  • Do NOT invent any meal name. Do NOT use any meal not in the VALID MEAL NAMES list.
  • Do NOT include numbers (prices, calories, distances) in your JSON values.

Required JSON schema:
{_SCHEMA_COMMENT}"""

    return [
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_message},
    ]


# ---------------------------------------------------------------------------
# STEP 3: Parse raw AI response → dict
# ---------------------------------------------------------------------------
def _parse_ai_json(raw: str) -> Optional[dict]:
    """
    Extract JSON from the AI response, stripping markdown fences if present.
    Returns None if no valid JSON object is found.
    """
    # Strip markdown fences (```json ... ``` or ``` ... ```)
    cleaned = re.sub(r"```(?:json)?\s*", "", raw).strip()
    cleaned = cleaned.replace("```", "").strip()

    # Attempt to find a JSON object in the response
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if not match:
        return None

    try:
        return json.loads(match.group())
    except json.JSONDecodeError:
        return None


# ---------------------------------------------------------------------------
# STEP 4: Validate AI output against known stores and meals
# ---------------------------------------------------------------------------
def _validate_ai_output(ai_output: dict, decision_packet: dict) -> tuple:
    """
    Validate every AI-chosen name against the Python-computed decision packet.
    This prevents hallucinations from reaching the backend.

    Returns (is_valid, error_message).
    """
    known_stores = {s["name"] for s in decision_packet["stores"]}
    known_meals  = {m["name"] for m in decision_packet["meals"]}

    store = ai_output.get("recommended_store", "")
    if not store:
        return False, "AI did not provide a recommended_store"
    if store not in known_stores:
        return False, f"AI recommended unknown store: '{store}' (not in {sorted(known_stores)})"

    selected_meals = ai_output.get("selected_meals", [])
    if not selected_meals or not isinstance(selected_meals, list):
        return False, "AI returned no selected_meals or wrong type"

    for meal_name in selected_meals:
        if meal_name not in known_meals:
            return False, f"AI selected unknown meal: '{meal_name}' (not in available meals)"

    return True, ""


# ---------------------------------------------------------------------------
# STEP 5 & 6: Python computes all numbers from validated AI choices
# ---------------------------------------------------------------------------
def _compute_final_results(ai_output: dict, decision_packet: dict) -> dict:
    """
    Python computes every numeric result.
    AI only chose the store name and meal names; Python does all the math.
    """
    store_name         = ai_output["recommended_store"]
    selected_meal_names = ai_output["selected_meals"]

    # Build fast lookup tables from pre-computed decision packet data
    meal_lookup  = {m["name"]: m for m in decision_packet["meals"]}
    store_lookup = {s["name"]: s for s in decision_packet["stores"]}

    selected_meals_data = [meal_lookup[name] for name in selected_meal_names]
    store_data          = store_lookup[store_name]

    # --- Python computes cost (AI never touches this) ---
    total_cost = sum(
        meal["costs"].get(store_name, 0.0)
        for meal in selected_meals_data
    )

    # --- Python aggregates nutrition (AI never touches this) ---
    total_nutrition = {"calories": 0.0, "protein": 0.0, "carbs": 0.0, "fat": 0.0}
    for meal in selected_meals_data:
        n = meal.get("nutrition", {})
        for key in total_nutrition:
            total_nutrition[key] = round(total_nutrition[key] + float(n.get(key, 0.0)), 1)

    return {
        "store":                store_name,
        "store_distance_miles": store_data["distance_miles"],
        "store_confidence":     store_data["confidence"],
        "meals": [
            {
                "name":             m["name"],
                "cost_at_store":    round(m["costs"].get(store_name, 0.0), 2),
                "nutrition":        m["nutrition"],
                "cook_time_minutes": m["cook_time_minutes"],
            }
            for m in selected_meals_data
        ],
        "total_cost":      round(total_cost, 2),
        "total_nutrition": total_nutrition,
        "reasoning":       ai_output.get("reasoning", ""),
        "notes":           ai_output.get("notes", ""),
    }


# ---------------------------------------------------------------------------
# Python fallback: select meals without the AI when validation fails
# ---------------------------------------------------------------------------
def _python_select_meals(decision_packet: dict, user_message: str) -> dict:
    """
    Pure Python meal selection used as fallback when the AI hallucinates or
    returns an empty selected_meals list.
    Picks the cheapest store, then picks up to 4 meals sorted by cost at that store.
    """
    stores = sorted(decision_packet["stores"], key=lambda s: s["total_cost"])
    best_store = stores[0]
    store_name = best_store["name"]

    meals = decision_packet["meals"]
    if not meals:
        # No meals survived filtering — return a graceful failure signal
        return {
            "recommended_store": store_name,
            "selected_meals": [],
            "reasoning": "No meals matched your current equipment and time constraints.",
            "notes": "",
        }

    # Sort meals by cost at the selected store (cheapest first)
    meals_sorted = sorted(meals, key=lambda m: m["costs"].get(store_name, 999))
    selected = meals_sorted[:4]

    reasoning = "Selected the most affordable meals available at the closest budget store based on your profile."

    return {
        "recommended_store": store_name,
        "selected_meals": [m["name"] for m in selected],
        "reasoning": reasoning,
        "notes": "",
    }


# ---------------------------------------------------------------------------
# PUBLIC API: run the full pipeline
# ---------------------------------------------------------------------------
def run_meal_planning_pipeline(user_message: str, profile: dict) -> dict:
    """
    Full 6-step pipeline:
      1. Generate decision packet (Python facts)
      2. Build AI prompt from packet
      3. Call Nemotron, receive raw response
      4. Parse JSON from raw response
      5. Validate AI choices against known data
      6. Python computes all final numbers

    Returns:
        {
            "success": bool,
            "result":  dict   (if success),
            "error":   str    (if not success),
            "fallback_text": str | None  (usable AI text if pipeline failed but AI responded)
        }
    """
    zip_code = str(profile.get("zip", "97331"))

    # --- Map user profile fields to decision packet constraints ---
    keywords = profile.get("keywords", {})

    # Build dietary_restrictions from both allergies AND the stored diet type
    # so the AI knows about vegan/vegetarian/etc. preferences
    allergies = list(profile.get("allergies") or [])
    diet_type = (keywords.get("diet") or "none").lower().strip()
    if diet_type and diet_type not in ("none", "normal", ""):
        allergies.append(diet_type)

    user_constraints = {
        "budget":               float(profile.get("meal_budget") or 15.0),
        "weekly_budget":        float(profile.get("weekly_budget") or 100.0),
        "max_distance_miles":   float(profile.get("radius") or 10),
        "dietary_restrictions": allergies,
        "diet_preference":      diet_type,
        "available_equipment":  profile.get("equipment") or ["stove", "oven", "microwave"],
        "max_time_minutes":     int(profile.get("max_cook_time") or 45),
        "cooking_skill":        profile.get("cooking_skill") or "beginner",
        "daily_calories":       int(keywords.get("calorie_target") or 2000),
        "protein_goal":         keywords.get("protein_goal") or "normal",
        "fat_goal":             keywords.get("fat_goal"),
        "carb_goal":            keywords.get("carb_goal"),
        "dieting":              keywords.get("dieting") or "no",
    }

    # STEP 1 — Python builds facts; AI never sees raw Python objects
    try:
        decision_packet = generate_decision_packet(user_constraints, zip_code)
    except Exception as exc:
        return {
            "success": False,
            "error": f"Decision packet generation failed: {exc}",
            "fallback_text": None,
        }

    # STEP 2 — Build structured prompt
    messages = _build_ai_prompt(user_message, decision_packet)

    # STEP 3 — Ask Nemotron
    try:
        raw_response = ask_model(messages)
    except Exception as exc:
        return {
            "success": False,
            "error": f"Nemotron call failed: {exc}",
            "fallback_text": None,
        }

    print(f"[ai_meal_planner] Raw AI response:\n{raw_response[:500]}")

    # STEP 4 — Parse JSON from AI response
    ai_output = _parse_ai_json(raw_response)
    if ai_output is None:
        # AI returned free text — pass through to the user as conversational response
        return {
            "success": False,
            "error": "AI did not return structured JSON",
            "fallback_text": raw_response,
        }

    # STEP 5 — Validate AI choices (hallucination guard)
    is_valid, error_msg = _validate_ai_output(ai_output, decision_packet)
    if not is_valid:
        print(f"[ai_meal_planner] Validation failed: {error_msg} — using Python fallback selection")
        # AI hallucinated a meal/store not in our data.
        # Fall back to pure Python selection so the user always gets a valid meal plan.
        ai_output = _python_select_meals(decision_packet, user_message)

    # STEP 6 — Python computes everything numeric
    result = _compute_final_results(ai_output, decision_packet)

    return {"success": True, "result": result}


# ---------------------------------------------------------------------------
# Format pipeline result → readable chat text
# ---------------------------------------------------------------------------
def format_pipeline_response(pipeline_result: dict) -> str:
    """
    Convert a pipeline result dict into a human-readable chat response.
    If pipeline failed but the AI gave usable text, pass that through.
    """
    if not pipeline_result["success"]:
        fallback = pipeline_result.get("fallback_text")
        if fallback:
            return fallback
        return (
            "I had trouble building a structured meal plan right now. "
            "Could you try asking like: 'suggest meals for this week' or "
            "'what should I cook tonight?'"
        )

    r = pipeline_result["result"]

    if not r.get("meals"):
        return (
            "I wasn't able to find meals that match your current equipment and time settings. "
            "Try updating your equipment list or increasing your max cook time in your profile."
        )

    # Build meal bullet list (all numbers from Python, not AI)
    meal_lines = []
    for m in r["meals"]:
        meal_lines.append(
            f"• {m['name']} — ${m['cost_at_store']:.2f}, "
            f"{m['cook_time_minutes']} min, "
            f"~{int(m['nutrition'].get('calories', 0))} cal"
        )
    meals_text = "\n".join(meal_lines)

    n = r["total_nutrition"]
    response = (
        f"Recommended Store: {r['store']} "
        f"({r['store_distance_miles']} mi away, {r['store_confidence']} pricing)\n\n"
        f"Selected Meals:\n{meals_text}\n\n"
        f"Total Cost: ${r['total_cost']:.2f}\n\n"
        f"Combined Nutrition:\n"
        f"  Calories: {n['calories']} kcal\n"
        f"  Protein:  {n['protein']}g\n"
        f"  Carbs:    {n['carbs']}g\n"
        f"  Fat:      {n['fat']}g\n\n"
        f"Why this plan: {r['reasoning']}"
    )

    if r.get("notes"):
        response += f"\n\nNote: {r['notes']}"

    return response
