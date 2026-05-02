from fastapi import FastAPI
from services import get_all_meals, get_available_meals, get_meal_costs, get_shopping_list, get_total_cost
from pricing.mock_provider import MockPricingProvider
from typing import Dict, Any, List

app = FastAPI()
pricing_provider = MockPricingProvider()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/test")
async def test():
    return {"message": "Test endpoint working!"}

@app.get("/meals")
async def get_meals():
    meals = get_all_meals()
    return {"meals": [meal.dict() for meal in meals]}

@app.post("/available-meals")
async def available_meals(constraints: Dict[str, Any]):
    meals = get_available_meals(constraints)
    return {"meals": [meal.dict() for meal in meals]}

@app.post("/meal-costs")
async def meal_costs(meals_data: List[Dict[str, Any]]):
    # Assuming meals_data is list of meal dicts, but for simplicity, use all meals or parse
    # For now, get costs for all meals
    meals = get_all_meals()
    costs = get_meal_costs(meals, pricing_provider)
    return {"costs": costs}

@app.post("/shopping-list")
async def shopping_list(meals_data: List[Dict[str, Any]]):
    # Placeholder: parse meals_data to Meal objects
    meals = get_all_meals()  # For now
    shopping = get_shopping_list(meals)
    return {"shopping_list": shopping}

@app.post("/total-cost")
async def total_cost(meals_data: List[Dict[str, Any]]):
    meals = get_all_meals()  # For now
    cost = get_total_cost(meals, pricing_provider)
    return {"total_cost": cost}