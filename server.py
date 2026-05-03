from flask import Flask, request, jsonify
from flask_cors import CORS
from user_chat import extract_keywords, wizard_confirmation
from memory_manager import MemoryManager
from Model import ask_model
import json

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

mm = MemoryManager()

# ---------------------------------------------------------
# Conversation State (in-memory)
# ---------------------------------------------------------
CURRENT_USERNAME = None
CURRENT_MODE = "preferences"          # "preferences" or "meal_planning"
PREFERENCE_STATE = "idle"             # "idle", "show_profile", "awaiting_yes_no", "awaiting_change"
GREETED = False                       # Has the bot greeted this session?


# ---------------------------------------------------------
# Helper: format keywords nicely
# ---------------------------------------------------------
def format_keywords(profile: dict) -> str:
    """
    Takes a user profile dict and returns a nicely formatted
    bullet list of keyword preferences.
    Expects profile to contain a "keywords" dict.
    """
    keywords = profile.get("keywords", {})
    if not keywords:
        return "No preferences saved yet."

    lines = []
    for key, value in keywords.items():
        pretty_key = key.replace("_", " ").capitalize()
        lines.append(f"• {pretty_key}: {value}")
    return "\n".join(lines)


# ---------------------------------------------------------
# REGISTER
# ---------------------------------------------------------
@app.post("/register")
def register():
    data = request.json
    username = (data.get("username") or "").strip()
    password = data.get("password", "")

    if not username or len(password) < 6:
        return jsonify({"success": False, "error": "Username required and password must be at least 6 characters"}), 400

    try:
        with open("logged_in.json", "r") as f:
            users = json.load(f)
    except FileNotFoundError:
        users = {}

    if username in users:
        return jsonify({"success": False, "error": "Username already taken"}), 400

    keywords = data.get("keywords", {})
    if not isinstance(keywords, dict):
        keywords = {}

    users[username] = {
        "password":      password,
        "email":         data.get("email", ""),
        "phone":         data.get("phone", ""),
        "zip":           data.get("zip", "00000"),
        "radius":        int(data.get("radius", 10)),
        "keywords": {
            "diet":           keywords.get("diet", "none"),
            "dieting":        bool(keywords.get("dieting", False)),
            "calorie_target": keywords.get("calorie_target", 2000),
            "protein_goal":   keywords.get("protein_goal"),
            "fat_goal":       keywords.get("fat_goal"),
            "carb_goal":      keywords.get("carb_goal"),
        },
        "allergies":     data.get("allergies", []),
        "equipment":     data.get("equipment", []),
        "cooking_skill": data.get("cooking_skill", "beginner"),
        "max_cook_time": int(data.get("max_cook_time", 30)),
        "weekly_budget": float(data.get("weekly_budget", 100)),
        "meal_budget":   float(data.get("meal_budget", 15)),
        "display_name":  data.get("display_name", username),
        "guest_mode":    False
    }

    with open("logged_in.json", "w") as f:
        json.dump(users, f, indent=2)

    return jsonify({"success": True})


# ---------------------------------------------------------
# LOGIN
# ---------------------------------------------------------
@app.post("/login")
def login():
    global CURRENT_USERNAME, CURRENT_MODE, PREFERENCE_STATE, GREETED

    data = request.json
    username = data.get("username")
    password = data.get("password")

    try:
        with open("logged_in.json", "r") as f:
            users = json.load(f)
    except FileNotFoundError:
        return jsonify({"success": False, "error": "User database missing"}), 500

    if username in users and users[username]["password"] == password:
        zip_code = users[username]["zip"]
        radius = users[username]["radius"]
        mm.login(username, zip_code, radius)

        # Reset session state
        CURRENT_USERNAME = username
        CURRENT_MODE = "preferences"
        PREFERENCE_STATE = "idle"
        GREETED = False

        return jsonify({"success": True})

    return jsonify({"success": False, "error": "Invalid credentials"}), 401


# ---------------------------------------------------------
# LOGOUT
# ---------------------------------------------------------
@app.post("/logout")
def logout():
    global CURRENT_USERNAME, CURRENT_MODE, PREFERENCE_STATE, GREETED

    mm.logout()
    CURRENT_USERNAME = None
    CURRENT_MODE = "preferences"
    PREFERENCE_STATE = "idle"
    GREETED = False

    return jsonify({"success": True})


# ---------------------------------------------------------
# CHAT
# ---------------------------------------------------------
@app.post("/chat")
def chat():
    global CURRENT_USERNAME, CURRENT_MODE, PREFERENCE_STATE, GREETED

    data = request.json
    user_input_raw = data.get("message", "")
    user_input = user_input_raw.strip().lower()

    frontend_logged_in = data.get("logged_in", False)
    username = data.get("username")
    is_guest = not (frontend_logged_in and username)

    print(f"[DEBUG] User said: {user_input_raw}")
    print("logged_in:", frontend_logged_in, "username:", username)
    print("is_guest:", is_guest, "CURRENT_MODE:", CURRENT_MODE,
          "PREFERENCE_STATE:", PREFERENCE_STATE, "GREETED:", GREETED)

    # ---------------------------------------------------------
    # GUEST MODE — skip preferences entirely
    # ---------------------------------------------------------
    if is_guest:
        zip_code = data.get("zip", "00000")
        radius = data.get("radius", 10)
        mm.save_guest_session(zip_code, radius)
        profile = mm.get_user_profile()

        # Automatic greeting for guest when frontend sends "start"
        if user_input == "start":
            GREETED = True
            CURRENT_MODE = "meal_planning"
            return jsonify({
                "response": (
                    "Hello guest! Since you're not logged in, we'll jump straight into meal planning.\n\n"
                    "What type of meals are you looking to prep?"
                )
            })

        # Allow guest to exit meal planning loop verbally
        if "done meal planning" in user_input:
            return jsonify({
                "response": (
                    "Got it. If you'd like to continue planning meals later, "
                    "just tell me what you're in the mood for."
                )
            })

        # Guest falls through to meal planning mode below

    else:
        # LOGGED-IN USER FLOW
        profile = mm.get_user_profile()

        # Automatic greeting for logged-in user when frontend sends "start"
        if user_input == "start":
            GREETED = True
            CURRENT_MODE = "preferences"
            PREFERENCE_STATE = "show_profile"

        # PREFERENCE MODE (LOGGED-IN ONLY)
        if CURRENT_MODE == "preferences":
            # Show preferences and ask yes/no
            if PREFERENCE_STATE in ["idle", "show_profile"]:
                PREFERENCE_STATE = "awaiting_yes_no"
                name = CURRENT_USERNAME or "guest"
                pretty_keywords = format_keywords(profile)

                return jsonify({
                    "response": (
                        f"Hello {name}!\n\n"
                        f"Here are your current preferences:\n{pretty_keywords}\n\n"
                        "Would you like to make any changes? (yes/no)"
                    )
                })

            # Waiting for yes/no
            if PREFERENCE_STATE == "awaiting_yes_no":
                if "yes" in user_input:
                    PREFERENCE_STATE = "awaiting_change"
                    return jsonify({"response": "What would you like to change?"})

                if "no" in user_input:
                    CURRENT_MODE = "meal_planning"
                    PREFERENCE_STATE = "idle"
                    return jsonify({
                        "response": (
                            "Great! We'll keep your current preferences.\n\n"
                            "Let's move into meal planning mode.\n"
                            "What kind of meals are you looking to prep?"
                        )
                    })

                return jsonify({
                    "response": (
                        "Please answer with 'yes' or 'no'.\n"
                        "Would you like to make any changes to your preferences?"
                    )
                })

            # Waiting for a change description
            if PREFERENCE_STATE == "awaiting_change":
                result = extract_keywords(user_input_raw)

                mm.update_keywords(
                    add_list=result.get("add", []),
                    remove_list=result.get("remove", []),
                    reset=result.get("reset", False)
                )

                profile = mm.get_user_profile()
                pretty_keywords = format_keywords(profile)

                PREFERENCE_STATE = "awaiting_yes_no"

                return jsonify({
                    "response": (
                        "Got it. I've updated your preferences.\n\n"
                        f"Here are your updated preferences:\n{pretty_keywords}\n\n"
                        "Would you like to make any more changes? (yes/no)"
                    )
                })

    # ---------------------------------------------------------
    # MEAL PLANNING MODE (GUEST + LOGGED-IN)
    # ---------------------------------------------------------
    if not is_guest and "done meal planning" in user_input:
        CURRENT_MODE = "preferences"
        PREFERENCE_STATE = "show_profile"
        profile = mm.get_user_profile()
        pretty_keywords = format_keywords(profile)

        return jsonify({
            "response": (
                "No problem. Let's go back to your preferences.\n\n"
                f"Here they are:\n{pretty_keywords}\n\n"
                "Would you like to make any changes? (yes/no)"
            )
        })

    CURRENT_MODE = "meal_planning"

    # Allow natural preference updates during meal planning (logged-in only)
    result = extract_keywords(user_input_raw)

    if not is_guest:
        mm.update_keywords(
            add_list=result.get("add", []),
            remove_list=result.get("remove", []),
            reset=result.get("reset", False)
        )

    profile = mm.get_user_profile()

    # If keywords changed, use wizard-style confirmation
    if result["add"] or result["remove"] or result["reset"]:
        return jsonify({
            "response": wizard_confirmation(
                result["add"], result["remove"], result["reset"], profile
            )
        })

    # ---------------------------------------------------------
    # NATURAL MEAL ASSISTANT (MEAL PLANNING MODE)
    # ---------------------------------------------------------
    system_prompt = f"""
You are a structured, reliable diet and meal assistant.

USER PROFILE:
{profile}

RULES:
- Stay on food, diet, nutrition, and meal planning.
- No trivia, math, or unrelated topics.
- No hallucinated stores or locations.
- Provide 1–3 clear meal ideas.
- No JSON.
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input_raw}
    ]

    response = ask_model(messages)
    return jsonify({"response": response})


# ---------------------------------------------------------
# RUN SERVER
# ---------------------------------------------------------
if __name__ == "__main__":
    app.run(port=5000, debug=True)