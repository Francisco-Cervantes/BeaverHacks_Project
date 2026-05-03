from Model import ask_model
from memory_manager import MemoryManager
import json
import re
import string


# ---------------------------------------------------------
# NORMALIZATION FUNCTION
# ---------------------------------------------------------
def normalize(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# ---------------------------------------------------------
# STRICT JSON PARSER WITH FUZZY MATCHING
# ---------------------------------------------------------
def extract_keywords(user_message):
    from keyword_patterns import (
        CHANGE_WORDS, RESET_PHRASES,
        DIET_START_PATTERNS, DIET_STOP_PATTERNS,
        DIETING_YES, DIETING_NO,
        MEAL_PREP_YES, MEAL_PREP_NO,
        CALORIE_PATTERNS, PROTEIN_PATTERNS
    )

    normalized = normalize(user_message)

    patterns_json = json.dumps({
        "change_words": CHANGE_WORDS,
        "reset_phrases": RESET_PHRASES,
        "diet_start": DIET_START_PATTERNS,
        "diet_stop": DIET_STOP_PATTERNS,
        "dieting_yes": DIETING_YES,
        "dieting_no": DIETING_NO,
        "meal_prep_yes": MEAL_PREP_YES,
        "meal_prep_no": MEAL_PREP_NO,
        "calorie_patterns": CALORIE_PATTERNS,
        "protein_patterns": PROTEIN_PATTERNS
    })

    extraction_prompt = [
        {
            "role": "system",
            "content": (
                "You are a STRICT JSON PARSER.\n"
                "You NEVER reply with natural language.\n"
                "You NEVER explain.\n"
                "You NEVER ask questions.\n"
                "You ONLY return valid JSON.\n\n"

                "Your output MUST follow this structure exactly:\n"
                "{ \"add\": [], \"remove\": [], \"reset\": false }\n\n"

                "MATCHING RULES:\n"
                "1. The user message has already been normalized.\n"
                "2. Perform fuzzy matching:\n"
                "   - substring matches\n"
                "   - partial matches\n"
                "   - semantic matches\n"
                "3. If ANY reset phrase appears → reset=true.\n"
                "4. If ANY diet_stop pattern appears → remove old diet, add diet:normal.\n"
                "5. If ANY diet_start pattern appears → add diet:<type>.\n"
                "6. If ANY dieting_yes pattern appears → add dieting:yes.\n"
                "7. If ANY dieting_no pattern appears → add dieting:no.\n"
                "8. If ANY meal_prep_yes pattern appears → add mealprep:yes.\n"
                "9. If ANY meal_prep_no pattern appears → add mealprep:no.\n"
                "10. If ANY calorie pattern appears followed by a number → add calorie_target:<number>.\n"
                "11. If ANY protein pattern appears followed by a number or word → add protein_goal:<value>.\n"
                "12. If a category already exists, include it in remove before adding the new value.\n"
                "13. NEVER output categories not found in the patterns.\n"
                "14. NEVER output anything except JSON.\n\n"

                f"PATTERNS_JSON:\n{patterns_json}"
            )
        },
        { "role": "user", "content": normalized }
    ]

    raw = ask_model(extraction_prompt)

    try:
        parsed = json.loads(raw)
        return {
            "add": parsed.get("add", []),
            "remove": parsed.get("remove", []),
            "reset": parsed.get("reset", False)
        }
    except:
        return {"add": [], "remove": [], "reset": False}



# ---------------------------------------------------------
# FRIENDLY WIZARD CONFIRMATION MESSAGES
# ---------------------------------------------------------
def wizard_confirmation(add_list, remove_list, reset, profile):
    if reset:
        return (
            "All your preferences have been reset. "
            "Want to set your diet, calorie target, or protein goal next?"
        )

    messages = []

    for item in add_list:
        cat, val = item.split(":", 1)
        if cat == "diet":
            messages.append(f"Great! I’ve updated your diet to {val}.")
        elif cat == "calorie_target":
            messages.append(f"Your calorie target is now set to {val}.")
        elif cat == "protein_goal":
            messages.append(f"Your protein goal is now {val}.")
        elif cat == "mealprep":
            messages.append(f"Meal prepping is now set to {val}.")
        elif cat == "dieting":
            messages.append(f"Your dieting status is now {val}.")

    if messages:
        messages.append("Want to adjust anything else — diet, calories, or protein?")
        return " ".join(messages)

    return None



# ---------------------------------------------------------
# MAIN CHAT LOOP
# ---------------------------------------------------------
def main():
    print("Welcome! How can I help you today.\n")

    mm = MemoryManager()

    mode = input("Are you logged in? (y/n): ").strip().lower()

    if mode == "y":
        user_id = input("Enter your username: ").strip()
        zip_code = input("Enter your zip code: ").strip()
        radius = int(input("Enter your mile radius: ").strip())

        mm.login(user_id, zip_code, radius)
        print(f"\nLogged in as {user_id}.")
    else:
        zip_code = input("Enter your zip code: ").strip()
        radius = int(input("Enter your mile radius: ").strip())

        mm.save_guest_session(zip_code, radius)
        print("\nGuest mode activated.")

    history = []

    while True:
        user_input = input("\nYou: ").strip().lower()

        if user_input in ["exit", "quit"]:
            print("Goodbye!")
            break

        # ---------------------------------------------------------
        # 1. RUN STRICT PARSER TO CHECK FOR KEYWORD UPDATES
        # ---------------------------------------------------------
        result = extract_keywords(user_input)

        if mm.is_logged_in():
            mm.update_keywords(
                add_list=result.get("add", []),
                remove_list=result.get("remove", []),
                reset=result.get("reset", False)
            )

        profile = mm.get_user_profile()

        # ---------------------------------------------------------
        # 2. IF KEYWORDS WERE UPDATED → FRIENDLY WIZARD RESPONSE
        # ---------------------------------------------------------
        if result["add"] or result["remove"] or result["reset"]:
            wizard_msg = wizard_confirmation(
                result["add"], result["remove"], result["reset"], profile
            )
            if wizard_msg:
                print(f"\nAI: {wizard_msg}")
                continue


        # ---------------------------------------------------------
        # 3. OTHERWISE → NATURAL MEAL ASSISTANT MODE
        # ---------------------------------------------------------
        system_prompt = f"""
You are a helpful diet and meal assistant.

USER PROFILE:
{profile}

BEHAVIOR RULES:
- Respond naturally and conversationally.
- NEVER ask the user to clarify preferences.
- NEVER request missing dietary information.
- ALWAYS trust the stored preferences exactly as they appear.
- NEVER contradict the stored preferences.
- NEVER modify preferences — the parser handles that.
- Provide meal ideas, guidance, and suggestions based on the profile.

DIET RULES:
- If diet is vegan: NEVER recommend meat, fish, eggs, or dairy.
- If diet is vegetarian: allow eggs/dairy, but no meat/fish.
- If diet is pescatarian: allow fish, but no meat.
- If diet is normal: no restrictions.

OUTPUT:
- Natural, friendly text.
- No JSON.
"""

        history.append({"role": "user", "content": user_input})
        messages = [{"role": "system", "content": system_prompt}] + history

        response = ask_model(messages)
        history.append({"role": "assistant", "content": response})

        print(f"\nAI: {response}")


if __name__ == "__main__":
    main()
