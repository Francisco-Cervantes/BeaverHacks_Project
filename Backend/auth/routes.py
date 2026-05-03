import json
from datetime import datetime
from typing import Optional

import jwt
from fastapi import APIRouter, Depends, Header, HTTPException, status
from pydantic import EmailStr

from auth.models import Token, UserCreate, UserLogin, UserProfileBase, UserProfileOut
from auth.security import (
    create_access_token,
    decode_access_token,
    get_password_hash,
    verify_password,
)
from database import get_connection

router = APIRouter(prefix="/auth", tags=["auth"])


def _row_to_profile(row) -> dict:
    if row is None:
        return None

    dietary_restrictions = row["dietary_restrictions"]
    return {
        "id": row["id"],
        "email": row["email"],
        "username": row["username"],
        "phone_number": row["phone_number"],
        "zip_code": row["zip_code"],
        "max_distance": row["max_distance"],
        "dietary_restrictions": json.loads(dietary_restrictions) if dietary_restrictions else [],
        "daily_calories": row["daily_calories"],
        "protein": row["protein"],
        "carbs": row["carbs"],
        "fat": row["fat"],
        "budget": row["budget"],
        "max_time_spent": row["max_time_spent"],
        "persona": row["persona"],
        "created_at": row["created_at"],
    }


def get_user_by_email(email: str):
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()
    return _row_to_profile(row)


def get_user_by_username(username: str):
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    return _row_to_profile(row)


def get_user_by_id(user_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return _row_to_profile(row)


def create_user(user: UserCreate) -> dict:
    hashed_password = get_password_hash(user.password)
    dietary_restrictions = json.dumps(user.dietary_restrictions or [])
    created_at = datetime.utcnow().isoformat() + "Z"

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO users (
                email,
                username,
                phone_number,
                password_hash,
                zip_code,
                max_distance,
                dietary_restrictions,
                daily_calories,
                protein,
                carbs,
                fat,
                budget,
                max_time_spent,
                persona,
                created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user.email,
                user.username,
                user.phone_number,
                hashed_password,
                user.zip_code,
                user.max_distance,
                dietary_restrictions,
                user.daily_calories,
                user.protein,
                user.carbs,
                user.fat,
                user.budget,
                user.max_time_spent,
                user.persona,
                created_at,
            ),
        )
        conn.commit()
        user_id = cursor.lastrowid
    finally:
        conn.close()

    return get_user_by_id(user_id)


def get_current_user(authorization: Optional[str] = Header(None)) -> dict:
    if authorization is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header required",
        )

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer token required",
        )

    try:
        payload = decode_access_token(token)
        user_id = int(payload.get("sub"))
    except (jwt.PyJWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user


@router.post("/register", response_model=Token)
def register(user_create: UserCreate):
    if get_user_by_email(user_create.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered",
        )

    if get_user_by_username(user_create.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username is already taken",
        )

    user = create_user(user_create)
    access_token = create_access_token(subject=str(user["id"]))
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
def login(credentials: UserLogin):
    user = get_user_by_email(credentials.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    conn = get_connection()
    row = conn.execute("SELECT password_hash FROM users WHERE email = ?", (credentials.email,)).fetchone()
    conn.close()

    if row is None or not verify_password(credentials.password, row["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    access_token = create_access_token(subject=str(user["id"]))
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/profile", response_model=UserProfileOut)
def read_profile(current_user: dict = Depends(get_current_user)):
    return current_user


@router.put("/profile", response_model=UserProfileOut)
def update_profile(profile_update: UserProfileBase, current_user: dict = Depends(get_current_user)):
    update_data = profile_update.dict(exclude_unset=True)
    if "dietary_restrictions" in update_data:
        update_data["dietary_restrictions"] = json.dumps(update_data["dietary_restrictions"] or [])

    if update_data:
        conn = get_connection()
        set_clause = ", ".join(f"{key} = ?" for key in update_data.keys())
        values = list(update_data.values())
        values.append(current_user["id"])
        conn.execute(f"UPDATE users SET {set_clause} WHERE id = ?", values)
        conn.commit()
        conn.close()

    return get_user_by_id(current_user["id"])
