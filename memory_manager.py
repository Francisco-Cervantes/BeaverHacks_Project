import json
import os

DEFAULT_KEYWORDS = {
    "diet": "normal",
    "dieting": "no",
    "calorie_target": 2000,
    "protein_goal": "normal"
}

class MemoryManager:
    def __init__(self, guest_file="guest.json", user_file="logged_in.json"):
        self.guest_file = guest_file
        self.user_file = user_file

        self._ensure_file(self.guest_file, {"zip": None, "radius": None, "guest_mode": True})
        self._ensure_file(self.user_file, {})

        self.guest_data = self._load_json(self.guest_file)
        self.user_data = self._load_json(self.user_file)

        self.current_user = None

    def _ensure_file(self, path, default_content):
        if not os.path.exists(path):
            with open(path, "w") as f:
                json.dump(default_content, f, indent=4)

    def _load_json(self, path):
        with open(path, "r") as f:
            return json.load(f)

    def _save_json(self, path, data):
        with open(path, "w") as f:
            json.dump(data, f, indent=4)

    def login(self, user_id, zip_code, radius):
        self.current_user = user_id

        if user_id not in self.user_data:
            self.user_data[user_id] = {
                "zip": zip_code,
                "radius": radius,
                "keywords": DEFAULT_KEYWORDS.copy(),
                "guest_mode": False
            }
            self._save_json(self.user_file, self.user_data)

    def logout(self):
        self.current_user = None

    def is_logged_in(self):
        return self.current_user is not None

    def save_guest_session(self, zip_code, radius):
        self.guest_data = {
            "zip": zip_code,
            "radius": radius,
            "guest_mode": True
        }
        self._save_json(self.guest_file, self.guest_data)

    def reset_keywords(self):
        if self.is_logged_in():
            self.user_data[self.current_user]["keywords"] = DEFAULT_KEYWORDS.copy()
            self._save_json(self.user_file, self.user_data)

    def update_keywords(self, add_list=None, remove_list=None, reset=False):
        if not self.is_logged_in():
            return

        if reset:
            self.reset_keywords()
            return

        user = self.user_data[self.current_user]
        keywords = user["keywords"]

        for kw in remove_list or []:
            if ":" in kw:
                cat = kw.split(":", 1)[0]
                if cat in keywords:
                    del keywords[cat]

        for new_kw in add_list or []:
            if ":" in new_kw:
                cat, val = new_kw.split(":", 1)
                if val.isdigit():
                    val = int(val)
                keywords[cat] = val

        self._save_json(self.user_file, self.user_data)

    def get_user_profile(self):
        if self.is_logged_in():
            return self.user_data[self.current_user]
        else:
            return self.guest_data
