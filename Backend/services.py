from models.meal import Meal
from models.shopping_list import build_shopping_list
from models.pricing import calculate_meal_cost, calculate_weekly_cost, calculate_shopping_cost
from filters import filter_by_equipment, filter_by_time, filter_by_distance, mark_meals_with_cost
from pricing.providers.base import PricingProvider
from pricing.providers.registry import build_store_provider, get_supported_store_names
from nutrition.nutrition import calculate_meal_nutrition, calculate_weekly_nutrition
from pricing.comparison import build_store_comparison
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


def get_store_options(zip_code: str) -> List[str]:
    """Return the list of supported store names."""
    return get_supported_store_names()


def get_prices_for_store(
    store_name: str,
    shopping_list: Dict[str, float],
    zip_code: str,
    max_distance_miles: float = None,
    gas_price: float = None,
    vehicle_mpg: float = 25.0,
    avg_speed_mph: float = 25.0,
) -> Dict[str, Any]:
    """Return per-item and total prices and travel metrics for a store."""
    provider = build_store_provider(store_name)
    if hasattr(provider, "set_location"):
        provider.set_location(zip_code)

    comparison = build_store_comparison(
        store_name,
        provider,
        shopping_list,
        zip_code,
        max_distance_miles=max_distance_miles,
        gas_price=gas_price,
        vehicle_mpg=vehicle_mpg,
        avg_speed_mph=avg_speed_mph,
    )

    if comparison is None:
        raise ValueError(f"{store_name} is unavailable within {max_distance_miles} miles of {zip_code}")

    items = []
    for ingredient, quantity in shopping_list.items():
        price = provider.get_price(ingredient)
        items.append({
            "ingredient": ingredient,
            "price_per_unit": price,
            "quantity": quantity,
            "store": store_name,
            "confidence": comparison["confidence"],
        })

    comparison["items"] = items
    comparison["shopping_list"] = shopping_list
    return comparison


def compare_store_costs(
    meals: List[Meal],
    zip_code: str,
    max_distance_miles: float = None,
    gas_price: float = None,
    vehicle_mpg: float = 25.0,
    avg_speed_mph: float = 25.0,
) -> Dict[str, Any]:
    """Compare store totals for a meal plan."""
    shopping_list = get_shopping_list(meals)
    results = {}
    excluded_stores = []

    for store_name in get_supported_store_names():
        try:
            store_data = get_prices_for_store(
                store_name,
                shopping_list,
                zip_code,
                max_distance_miles=max_distance_miles,
                gas_price=gas_price,
                vehicle_mpg=vehicle_mpg,
                avg_speed_mph=avg_speed_mph,
            )
            results[store_name] = store_data
        except ValueError:
            excluded_stores.append(store_name)

    return {
        "stores": results,
        "excluded_stores": excluded_stores,
        "shopping_list": shopping_list,
    }


def get_meal_nutrition(meals: List[Meal], nutrition_provider) -> Dict[str, Dict[str, float]]:
    return {meal.name: calculate_meal_nutrition(meal, nutrition_provider) for meal in meals}


def get_weekly_nutrition(meals: List[Meal], nutrition_provider) -> Dict[str, float]:
    return calculate_weekly_nutrition(meals, nutrition_provider)
