from models.meal import Meal
from typing import List, Dict, Any
from pricing.provider import PricingProvider
from models.pricing import calculate_meal_cost

def filter_by_equipment(meals: List[Meal], available_equipment: List[str]) -> List[Meal]:
    """Filter meals that require equipment not available to the user."""
    filtered = []
    for meal in meals:
        if all(eq in available_equipment for eq in meal.equipment_required):
            filtered.append(meal)
    return filtered

def filter_by_time(meals: List[Meal], max_time_minutes: int) -> List[Meal]:
    """Filter meals that take longer than the user's max time."""
    return [meal for meal in meals if meal.cook_time_minutes <= max_time_minutes]

def filter_by_distance(meals: List[Meal], max_distance_miles: float) -> List[Meal]:
    """Placeholder: Filter meals based on distance to required stores.
    
    TODO: Implement distance calculation based on meal ingredients' stores.
    For now, returns all meals.
    """
    # Placeholder implementation
    return meals

def mark_meals_with_cost(meals: List[Meal], pricing_provider: PricingProvider) -> List[Dict[str, Any]]:
    """Mark meals with their estimated costs for pre-filtering."""
    marked = []
    for meal in meals:
        cost = calculate_meal_cost(meal, pricing_provider)
        marked.append({
            "meal": meal,
            "estimated_cost": cost
        })
    return marked