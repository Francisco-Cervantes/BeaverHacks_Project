
from pydantic import BaseModel
from typing import List

class MealIngredient(BaseModel):
    ingredient_name: str
    quantity: float         # how much is needed
    unit: str

class Meal(BaseModel):
    name: str
    ingredients: List[MealIngredient]
    cook_time_minutes: int
    equipment_required: List[str]   # ["stove"], ["oven"], etc.
