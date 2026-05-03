from flask import Flask, request, jsonify
from flask_cors import CORS
from user_chat import extract_keywords, wizard_confirmation
from memory_manager import MemoryManager
from Model import ask_model
from ai_meal_planner import run_meal_planning_pipeline, format_pipeline_response
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
# Helper: detect cooking instructions requests
# ---------------------------------------------------------
def is_cooking_instructions_request(text: str) -> bool:
    """Return True when the user asks HOW to prepare/make/cook a specific dish."""
    patterns = [
        "how do i make", "how do i prepare", "how do i cook",
        "how to make", "how to prepare", "how to cook",
        "how do you make", "how do you prepare", "how do you cook",
        "steps to make", "steps to cook", "steps to prepare",
        "recipe for", "instructions for", "directions for",
        "walk me through", "teach me to make", "teach me to cook",
        "how do i go about", "how would i make", "how would i cook",
        "how would i prepare", "how do i bake", "how to bake",
        "how do i grill", "how to grill", "how do i fry", "how to fry",
        "how do i roast", "how to roast", "give me a recipe",
        "show me how to make", "show me how to cook",
        "i want to cook", "i want to make", "i want to bake",
        "i want to prepare",
    ]
    return any(p in text for p in patterns)


def get_cooking_instructions(user_message: str) -> str:
    """Ask Nemotron directly for cooking instructions and return the reply."""
    messages = [
        {
            "role": "system",
            "content": (
                "You are a friendly cooking assistant. "
                "When the user asks how to prepare or cook a dish, give them clear, "
                "numbered step-by-step instructions. Include approximate cooking times and "
                "any helpful tips. Keep the response concise but complete."
            )
        },
        {"role": "user", "content": user_message}
    ]
    try:
        reply = ask_model(messages)
        return reply.strip() if reply else "Sorry, I couldn't fetch instructions right now. Please try again."
    except Exception as e:
        return f"Sorry, I ran into an error fetching instructions: {str(e)}"


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
        "guest_mode":    False,
    }

    with open("logged_in.json", "w") as f:
        json.dump(users, f, indent=2)

    return jsonify({"success": True})


# ---------------------------------------------------------
# SAVE PROFILE
# ---------------------------------------------------------
@app.post("/save-profile")
def save_profile():
    data = request.json
    username = data.get("username", "").strip()

    try:
        with open("logged_in.json", "r") as f:
            users = json.load(f)
    except FileNotFoundError:
        return jsonify({"success": False, "error": "User database missing"}), 500

    if username not in users:
        return jsonify({"success": False, "error": "User not found"}), 404

    u = users[username]

    if "zipCode"             in data: u["zip"]           = data["zipCode"]
    if "radius"              in data: u["radius"]         = int(data["radius"])
    if "dailyCalories"       in data: u["keywords"]["calorie_target"] = data["dailyCalories"]
    if "dietaryRestrictions" in data: u["keywords"]["diet"] = data["dietaryRestrictions"]
    if "equipment"           in data: u["equipment"]      = data["equipment"]
    if "cooking_skill"       in data: u["cooking_skill"]  = data["cooking_skill"]
    if "max_cook_time"       in data: u["max_cook_time"]  = int(data["max_cook_time"])
    if "weekly_budget"       in data: u["weekly_budget"]  = float(data["weekly_budget"])
    if "meal_budget"         in data: u["meal_budget"]    = float(data["meal_budget"])
    if "allergies"           in data: u["allergies"]      = data["allergies"]
    if "name"                in data: u["display_name"]   = data["name"]

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
    # COOKING INSTRUCTIONS — "how do I make/prepare/cook X"
    # Bypass the meal planning pipeline; ask Nemotron directly
    # ---------------------------------------------------------
    if is_cooking_instructions_request(user_input):
        instructions = get_cooking_instructions(user_input_raw)
        return jsonify({"response": instructions, "structured_result": None})

    # ---------------------------------------------------------
    # MEAL PLANNING MODE — structured AI pipeline
    # Python builds facts → AI chooses names → Python computes numbers
    # ---------------------------------------------------------
    profile = mm.get_user_profile()

    # Run the structured pipeline (decision packet → Nemotron → validate → compute)
    pipeline_result = run_meal_planning_pipeline(user_input_raw, profile)
    response_text = format_pipeline_response(pipeline_result)

    # Also send structured data so the frontend can render recipe cards with real costs
    structured_result = None
    if pipeline_result.get("success") and isinstance(pipeline_result.get("result"), dict):
        r = pipeline_result["result"]
        store_name = r.get("store", "")
        meal_list = []
        for m in r.get("meals", []):
            meal_entry = {
                "name":               m.get("name", ""),
                "cook_time_minutes":  m.get("cook_time_minutes", 0),
                "equipment_required": [],   # pipeline result doesn't carry these; cards still render
                "ingredients":        [],   # recipe detail comes from the Meals page
                "cost_at_store":      m.get("cost_at_store", 0),
            }
            meal_list.append(meal_entry)
        structured_result = {
            "store":      store_name,
            "meals":      meal_list,
            "total_cost": r.get("total_cost", 0),
            "nutrition":  r.get("total_nutrition", {}),
        }

    return jsonify({"response": response_text, "structured_result": structured_result})


# ---------------------------------------------------------
# RUN SERVER
# ---------------------------------------------------------
if __name__ == "__main__":
    app.run(port=5000, debug=True)
