from fastapi import FastAPI
from services import (
    get_all_meals,
    get_available_meals,
    get_meal_costs,
    get_shopping_list,
    get_total_cost,
    get_store_options,
    get_prices_for_store,
    compare_store_costs,
    get_meal_nutrition,
)
from pricing.providers.mock_provider import MockPricingProvider
from nutrition.providers.registry import build_nutrition_provider
from models.meal import Meal
from auth.routes import router as auth_router
from typing import Dict, Any, List

app = FastAPI()
app.include_router(auth_router)
pricing_provider = MockPricingProvider()
nutrition_provider = build_nutrition_provider()

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

@app.post("/meal-nutrition")
async def meal_nutrition(meals_data: List[Dict[str, Any]]):
    meals = [Meal(**meal_data) for meal_data in meals_data]
    nutrition = get_meal_nutrition(meals, nutrition_provider)
    return {"nutrition": nutrition}

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


@app.get("/stores")
async def stores(zip_code: str):
    return {"stores": get_store_options(zip_code)}


@app.post("/store-prices")
async def store_prices(
    store_name: str,
    shopping_list: Dict[str, float],
    zip_code: str,
    max_distance_miles: float = None,
    gas_price: float = None,
    vehicle_mpg: float = 25.0,
    avg_speed_mph: float = 25.0,
):
    return get_prices_for_store(
        store_name,
        shopping_list,
        zip_code,
        max_distance_miles=max_distance_miles,
        gas_price=gas_price,
        vehicle_mpg=vehicle_mpg,
        avg_speed_mph=avg_speed_mph,
    )


@app.post("/compare-stores")
async def compare_stores(
    meals: List[Meal],
    zip_code: str,
    max_distance_miles: float = None,
    gas_price: float = None,
    vehicle_mpg: float = 25.0,
    avg_speed_mph: float = 25.0,
):
    return compare_store_costs(
        meals,
        zip_code,
        max_distance_miles=max_distance_miles,
        gas_price=gas_price,
        vehicle_mpg=vehicle_mpg,
        avg_speed_mph=avg_speed_mph,
    )
