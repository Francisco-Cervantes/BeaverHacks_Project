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

    # Summarize stores (Python-computed totals — AI reads but never changes these)
    store_lines = []
    for s in decision_packet["stores"]:
        store_lines.append(
            f"  • {s['name']}: total=${s['total_cost']:.2f}  "
            f"distance={s['distance_miles']}mi  "
            f"pricing={s['confidence']}"
        )
    stores_text = "\n".join(store_lines)

    # Summarize available meals (pre-filtered by Python for user's equipment/time)
    meal_lines = []
    for m in decision_packet["meals"]:
        meal_lines.append(
            f"  • {m['name']}: ~{m['nutrition'].get('calories', 0):.0f}cal  "
            f"{m['cook_time_minutes']}min  "
            f"equipment={','.join(m['equipment_required'])}"
        )
    meals_text = "\n".join(meal_lines)

    system_content = f"""You are a meal planning assistant. All prices, distances, nutrition, and \
store data below were computed by the backend system — do NOT invent or change any numbers. \
Your ONLY job is to choose names from the lists and write a short explanation.

USER PROFILE:
  Budget per meal: ${profile.get('budget', 50)}
  Max distance: {profile.get('max_distance_miles', 10)} miles
  Dietary restrictions: {profile.get('dietary_restrictions') or 'none'}
  Available equipment: {profile.get('available_equipment', ['stove', 'oven', 'microwave'])}
  Max cook time: {profile.get('max_time_minutes', 45)} min
  Daily calorie target: {profile.get('daily_calories', 2000)} kcal

AVAILABLE STORES (backend-computed totals — do NOT change these numbers):
{stores_text}

AVAILABLE MEALS (already filtered for user's equipment and time — do NOT add meals outside this list):
{meals_text}

YOUR TASK:
1. Pick the best store from AVAILABLE STORES (consider price, distance, confidence).
2. Pick 2–4 meals from AVAILABLE MEALS that match the user's request and profile.
3. Write a short reasoning sentence and a notes sentence.

RULES:
  • Respond with ONLY valid JSON — no markdown, no extra text, no code fences.
  • Use EXACT store and meal names as they appear in the lists above.
  • Do NOT invent store names or meal names not in the lists.
  • Do NOT include any numbers (prices, calories, distances) in your JSON.

Required JSON schema (copy this structure exactly):
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
    user_constraints = {
        "budget":               float(profile.get("meal_budget", keywords.get("calorie_target", 15))),
        "max_distance_miles":   float(profile.get("radius", 10)),
        "dietary_restrictions": profile.get("allergies", []),
        "available_equipment":  profile.get("equipment", ["stove", "oven", "microwave"]),
        "max_time_minutes":     int(profile.get("max_cook_time", 45)),
        "daily_calories":       int(keywords.get("calorie_target", 2000)),
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
        # AI returned free text (e.g. a recipe or ingredient answer) — pass through as-is
        return {
            "success": False,
            "error": "AI did not return structured JSON (probably a conversational answer)",
            "fallback_text": raw_response,
        }

    # STEP 5 — Validate AI choices (hallucination guard)
    is_valid, error_msg = _validate_ai_output(ai_output, decision_packet)
    if not is_valid:
        print(f"[ai_meal_planner] Validation failed: {error_msg}")
        return {
            "success": False,
            "error": error_msg,
            "fallback_text": raw_response,
        }

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
