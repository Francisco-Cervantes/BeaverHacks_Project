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
    keywords = profile.get("keywords", {})
    if not keywords:
        return "No preferences saved yet."

    lines = []
    for key, value in keywords.items():
        pretty_key = key.replace("_", " ").capitalize()
        lines.append(f"• {pretty_key}: {value}")
    return "\n".join(lines)


# ---------------------------------------------------------
# Helper: detect if user is trying to edit preferences
# ---------------------------------------------------------
def user_is_editing_preferences(text: str) -> bool:
    text = text.lower()
    edit_phrases = [
        "change my", "change the", "update my", "update the",
        "set my", "set the", "modify my", "modify the",
        "adjust my", "adjust the", "switch my", "switch the",
        "make my", "make the"
    ]
    return any(phrase in text for phrase in edit_phrases)


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
    user_input_raw = user_input_raw.replace("&", "and")  # normalize "&"
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

        # Automatic greeting for guest when frontend sends "__start__"
        if user_input == "__start__":
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

        # Automatic greeting for logged-in user when frontend sends "__start__"
        if user_input == "__start__":
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

    # ---------------------------------------------------------
    # BLOCK PREFERENCE UPDATES IN MEAL MODE
    # ---------------------------------------------------------
    if user_is_editing_preferences(user_input_raw):
        return jsonify({
            "response": (
                "Preference changes can only be made in Preference Mode.\n"
                "Say 'I am done meal planning' to switch back."
            )
        })

    # ---------------------------------------------------------
    # NATURAL MEAL ASSISTANT (MEAL PLANNING MODE)
    # ---------------------------------------------------------
    profile = mm.get_user_profile()

    system_prompt = f"""
You are a structured, reliable diet and meal assistant.

USER PROFILE:
{profile}

RULES:
- Stay on food, diet, nutrition, and meal planning.
- Understand natural requests like:
  "meals that work around my preferences",
  "show me dishes with chicken",
  "what meals fit my diet",
  "meals using tofu",
  "meals based on my zip",
  "what ingredients do I need to make X",
  "what ingredients are in X",
  "ingredients for X",
  "how do I make X".

INGREDIENT-BASED RECIPE LOOKUP:
- If the user asks for ingredients for a dish:
    1. Identify the dish name.
    2. Provide a clean ingredient list.
    3. Keep it simple and realistic.
    4. Respect the user's diet (vegan, high protein, etc.).
    5. If the dish conflicts with their diet, offer a diet‑friendly version.
- Do NOT hallucinate stores or prices.
- Do NOT output JSON.
- Keep responses clean and readable.

CALORIE-TOTAL MEAL GENERATION:
- If the user asks for meals totaling a specific calorie amount
  (e.g., "give me breakfast lunch and dinner that total 3000 calories"):
    1. Generate the requested number of meals (default: breakfast, lunch, dinner).
    2. Each meal must include:
        - Name of the dish
        - Short description
        - Estimated calories
    3. The total calories across all meals should be close to the target.
    4. Meals must respect the user's diet, preferences, and keywords.
    5. Keep the output clean and readable.

- No trivia, math explanations, or unrelated topics.
- No hallucinated stores or locations.
- Provide clear meal ideas.
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
