from models.meal import Meal
from models.shopping_list import build_shopping_list
from models.pricing import calculate_meal_cost, calculate_weekly_cost, calculate_shopping_cost
from filters import filter_by_equipment, filter_by_time, filter_by_distance, mark_meals_with_cost
from pricing.provider import PricingProvider
from meals.sample_meals import sample_meals
from typing import List, Dict, Any

def get_all_meals() -> List[Meal]:
    return sample_meals

def get_available_meals(constraints: Dict[str, Any]) -> List[Meal]:
    """Get meals filtered by constraints."""
    meals = get_all_meals()
    if 'available_equipment' in constraints:
        meals = filter_by_equipment(meals, constraints['available_equipment'])
    if 'max_time_minutes' in constraints:
        meals = filter_by_time(meals, constraints['max_time_minutes'])
    if 'max_distance_miles' in constraints:
        meals = filter_by_distance(meals, constraints['max_distance_miles'])
    return meals

def get_meal_costs(meals: List[Meal], pricing_provider: PricingProvider) -> Dict[str, float]:
    """Get costs for a list of meals."""
    costs = {}
    for meal in meals:
        costs[meal.name] = calculate_meal_cost(meal, pricing_provider)
    return costs

def get_shopping_list(meals: List[Meal]) -> Dict[str, float]:
    """Get aggregated shopping list for meals."""
    return build_shopping_list(meals)

def get_total_cost(meals: List[Meal], pricing_provider: PricingProvider) -> float:
    """Get total cost for meals using shopping list aggregation."""
    shopping_list = get_shopping_list(meals)
    return calculate_shopping_cost(shopping_list, pricing_provider)