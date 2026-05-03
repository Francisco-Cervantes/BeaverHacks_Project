from typing import Dict, List

from models.meal import Meal
from nutrition.provider import NutritionProvider


def calculate_ingredient_nutrition(
    ingredient_name: str,
    quantity: float,
    unit: str,
    nutrition_provider: NutritionProvider,
) -> Dict[str, float]:
    return nutrition_provider.get_nutrition(ingredient_name, quantity, unit)


def calculate_meal_nutrition(meal: Meal, nutrition_provider: NutritionProvider) -> Dict[str, float]:
    totals = {"calories": 0.0, "protein": 0.0, "carbs": 0.0, "fat": 0.0}
    for ingredient in meal.ingredients:
        nutrition = calculate_ingredient_nutrition(
            ingredient.ingredient_name,
            ingredient.quantity,
            ingredient.unit,
            nutrition_provider,
        )
        totals["calories"] += nutrition.get("calories", 0.0)
        totals["protein"] += nutrition.get("protein", 0.0)
        totals["carbs"] += nutrition.get("carbs", 0.0)
        totals["fat"] += nutrition.get("fat", 0.0)

    return {key: round(value, 2) for key, value in totals.items()}


def calculate_weekly_nutrition(meals: List[Meal], nutrition_provider: NutritionProvider) -> Dict[str, float]:
    totals = {"calories": 0.0, "protein": 0.0, "carbs": 0.0, "fat": 0.0}
    for meal in meals:
        meal_totals = calculate_meal_nutrition(meal, nutrition_provider)
        totals["calories"] += meal_totals["calories"]
        totals["protein"] += meal_totals["protein"]
        totals["carbs"] += meal_totals["carbs"]
        totals["fat"] += meal_totals["fat"]
    return {key: round(value, 2) for key, value in totals.items()}
