from typing import List, Optional
from pydantic import BaseModel, EmailStr


class UserProfileBase(BaseModel):
    zip_code: Optional[str] = None
    max_distance: Optional[float] = None
    dietary_restrictions: Optional[List[str]] = None
    daily_calories: Optional[int] = None
    protein: Optional[int] = None
    carbs: Optional[int] = None
    fat: Optional[int] = None
    budget: Optional[float] = None
    max_time_spent: Optional[int] = None
    persona: Optional[str] = None


class UserCreate(UserProfileBase):
    email: EmailStr
    username: str
    phone_number: str
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserProfileOut(UserProfileBase):
    id: int
    email: EmailStr
    username: str
    phone_number: str
    created_at: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
