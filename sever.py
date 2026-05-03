from flask import Flask, request, jsonify
from flask_cors import CORS
from user_chat import extract_keywords, wizard_confirmation, normalize
from memory_manager import MemoryManager
from Model import ask_model
import json

app = Flask(__name__)
CORS(app)  # Allow frontend on port 8000 to call this server

# Global memory manager instance
mm = MemoryManager()


# ---------------------------------------------------------
# LOGIN ENDPOINT
# ---------------------------------------------------------
@app.post("/login")
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # Load logged_in.json
    try:
        with open("logged_in.json", "r") as f:
            users = json.load(f)
    except FileNotFoundError:
        return jsonify({"success": False, "error": "User database missing"}), 500

    # Validate user
    if username in users and users[username].get("password") == password:
        # Load user into memory manager
        zip_code = users[username]["zip"]
        radius = users[username]["radius"]
        mm.login(username, zip_code, radius)

        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "Invalid credentials"}), 401


# ---------------------------------------------------------
# REGISTER ENDPOINT
# ---------------------------------------------------------
@app.post("/register")
def register():
    data = request.json
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()
    zip_code = data.get("zip", "00000").strip()
    radius   = int(data.get("radius", 10))

    if not username or not password:
        return jsonify({"success": False, "error": "Username and password are required"}), 400

    try:
        with open("logged_in.json", "r") as f:
            users = json.load(f)
    except FileNotFoundError:
        users = {}

    if username in users:
        return jsonify({"success": False, "error": "Username already exists"}), 409

    users[username] = {
        "password": password,
        "zip": zip_code,
        "radius": radius,
        "keywords": {
            "diet": "normal",
            "dieting": "no",
            "calorie_target": 2000,
            "protein_goal": "normal"
        },
        "guest_mode": False
    }

    with open("logged_in.json", "w") as f:
        json.dump(users, f, indent=4)

    mm.login(username, zip_code, radius)
    return jsonify({"success": True})



# ---------------------------------------------------------
@app.post("/chat")
def chat():
    data = request.json
    user_input = data.get("message", "").strip().lower()
    username = data.get("username")       # optional for guest mode
    logged_in = data.get("logged_in", False)  # boolean from frontend

    # If username provided → ensure user is loaded
    if username:
        try:
            with open("logged_in.json", "r") as f:
                users = json.load(f)

            if username in users:
                mm.login(
                    username,
                    users[username]["zip"],
                    users[username]["radius"]
                )
        except:
            pass
    else:
        # Guest mode
        zip_code = data.get("zip", "00000")
        radius = data.get("radius", 10)
        mm.save_guest_session(zip_code, radius)

    # ---------------------------------------------------------
    # 1. STRICT PARSER
    # ---------------------------------------------------------
    result = extract_keywords(user_input)

    # Update memory only if frontend confirmed user is logged in
    if logged_in and mm.is_logged_in():
        mm.update_keywords(
            add_list=result.get("add", []),
            remove_list=result.get("remove", []),
            reset=result.get("reset", False)
        )

    profile = mm.get_user_profile()

    # ---------------------------------------------------------
    # 2. WIZARD CONFIRMATION (if keywords changed)
    # ---------------------------------------------------------
    if result["add"] or result["remove"] or result["reset"]:
        wizard_msg = wizard_confirmation(
            result["add"], result["remove"], result["reset"], profile
        )
        return jsonify({"response": wizard_msg})

    # ---------------------------------------------------------
    # 3. NATURAL MEAL ASSISTANT MODE
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

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]

    response = ask_model(messages)

    return jsonify({"response": response})



# ---------------------------------------------------------
# RUN SERVER
# ---------------------------------------------------------
if __name__ == "__main__":
    app.run(port=5000, debug=True)
