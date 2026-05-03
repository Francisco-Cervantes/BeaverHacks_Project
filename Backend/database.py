import os
import sqlite3
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from the backend .env file
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL", str(Path(__file__).parent / "app.db"))


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DATABASE_URL, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            username TEXT UNIQUE NOT NULL,
            phone_number TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            zip_code TEXT,
            max_distance REAL,
            dietary_restrictions TEXT,
            daily_calories INTEGER,
            protein INTEGER,
            carbs INTEGER,
            fat INTEGER,
            budget REAL,
            max_time_spent INTEGER,
            persona TEXT,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


init_db()
