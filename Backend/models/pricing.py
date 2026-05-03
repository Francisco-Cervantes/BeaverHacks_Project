from pricing.providers.base import PricingProvider
from models.meal import Meal
from typing import List, Dict

def calculate_meal_cost(meal: Meal, pricing_provider: PricingProvider) -> float:
    total = 0.0
    for item in meal.ingredients:
        price = pricing_provider.get_price(item.ingredient_name)
        total += price * item.quantity
    return round(total, 2)

def calculate_weekly_cost(meals: List[Meal], pricing_provider: PricingProvider) -> float:
    total = 0.0
    for meal in meals:
        total += calculate_meal_cost(meal, pricing_provider)
    return round(total, 2)

def calculate_shopping_cost(shopping_list: Dict[str, float], pricing_provider: PricingProvider) -> float:
    total = 0.0
    for ingredient, quantity in shopping_list.items():
        try:
            price = pricing_provider.get_price(ingredient)
            total += price * quantity
        except Exception:
            # Skip ingredients that can't be priced
            continue
    return round(total, 2)
