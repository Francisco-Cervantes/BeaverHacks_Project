"""
Meal Planner Data Processor

This module contains all the data structures and computation logic for meal planning.
It processes raw ingredient data, computes nutrition and pricing, and generates
a decision packet JSON for AI reasoning.

Data Structures:
- Ingredient nutrition data (per 100g)
- Unit conversion factors
- Store configurations and pricing
- Sample meals and ingredients
- User constraint data

Computation:
- Meal-level nutrition aggregation
- Cost calculations per meal and store
- Shopping list aggregation
- Distance and travel cost calculations
"""

import json
from typing import Dict, List, Any

# Import backend modules
from models.meal import Meal, MealIngredient
from models.pricing import calculate_meal_cost, calculate_shopping_cost
from models.shopping_list import build_shopping_list
from nutrition.nutrition import calculate_meal_nutrition
from pricing.providers.mock_provider import MockPricingProvider
from pricing.providers.registry import build_store_provider, get_supported_store_names
from nutrition.providers.registry import build_nutrition_provider
from filters import filter_by_equipment, filter_by_time


# =============================================================================
# INGREDIENT NUTRITION DATA (per 100g)
# =============================================================================

INGREDIENT_NUTRITION = {
    "pasta": {
        "calories": 131.0,
        "protein": 5.0,
        "carbs": 25.0,
        "fat": 1.1
    },
    "canned tomatoes": {
        "calories": 18.0,
        "protein": 0.9,
        "carbs": 3.9,
        "fat": 0.2
    },
    "onion": {
        "calories": 40.0,
        "protein": 1.1,
        "carbs": 9.3,
        "fat": 0.1
    },
    "rice": {
        "calories": 130.0,
        "protein": 2.7,
        "carbs": 28.0,
        "fat": 0.3
    },
    "chicken breast": {
        "calories": 165.0,
        "protein": 31.0,
        "carbs": 0.0,
        "fat": 3.6
    },
    "eggs": {
        "calories": 155.0,
        "protein": 13.0,
        "carbs": 1.1,
        "fat": 11.0
    },
    "milk": {
        "calories": 60.0,
        "protein": 3.2,
        "carbs": 5.0,
        "fat": 3.3
    },
    "banana": {
        "calories": 89.0,
        "protein": 1.1,
        "carbs": 23.0,
        "fat": 0.3
    },
    "apple": {
        "calories": 52.0,
        "protein": 0.3,
        "carbs": 14.0,
        "fat": 0.2
    },
    "bread": {
        "calories": 265.0,
        "protein": 9.0,
        "carbs": 49.0,
        "fat": 3.2
    },
    "olive oil": {
        "calories": 884.0,
        "protein": 0.0,
        "carbs": 0.0,
        "fat": 100.0
    },
    "butter": {
        "calories": 717.0,
        "protein": 0.9,
        "carbs": 0.1,
        "fat": 81.0
    },
    "cheese": {
        "calories": 402.0,
        "protein": 25.0,
        "carbs": 1.3,
        "fat": 33.0
    },
    "tomato": {
        "calories": 18.0,
        "protein": 0.9,
        "carbs": 3.9,
        "fat": 0.2
    },
    "spinach": {
        "calories": 23.0,
        "protein": 2.9,
        "carbs": 3.6,
        "fat": 0.4
    },
    "ground beef": {
        "calories": 250.0,
        "protein": 26.0,
        "carbs": 0.0,
        "fat": 17.0
    },
    "potatoes": {
        "calories": 77.0,
        "protein": 2.0,
        "carbs": 17.0,
        "fat": 0.1
    },
    "carrots": {
        "calories": 41.0,
        "protein": 0.9,
        "carbs": 10.0,
        "fat": 0.2
    },
    "broccoli": {
        "calories": 34.0,
        "protein": 2.8,
        "carbs": 7.0,
        "fat": 0.4
    },
    "salmon": {
        "calories": 208.0,
        "protein": 22.0,
        "carbs": 0.0,
        "fat": 13.0
    }
}


# =============================================================================
# UNIT CONVERSION DATA
# =============================================================================

UNIT_TO_GRAMS = {
    "g": 1.0,
    "gram": 1.0,
    "grams": 1.0,
    "kg": 1000.0,
    "lb": 453.592,
    "oz": 28.35,
    "each": 60.0,
    "can": 240.0,
    "cup": 150.0,
    "tbsp": 15.0,
    "tsp": 5.0,
}

INGREDIENT_UNIT_OVERRIDES = {
    "rice": {"cup": 158.0},
    "pasta": {"cup": 140.0},
    "eggs": {"each": 50.0},
    "onion": {"each": 110.0},
    "chicken breast": {"lb": 453.592},
    "canned tomatoes": {"can": 240.0},
    "banana": {"each": 118.0},
    "apple": {"each": 182.0},
    "potatoes": {"each": 173.0},
    "carrots": {"each": 61.0},
}


# =============================================================================
# STORE CONFIGURATION DATA
# =============================================================================

STORE_CONFIGURATIONS = {
    "Kroger": {
        "multiplier": 1.0,  # Base pricing
        "default_distance_miles": 5.0,
        "confidence": "live",  # Uses real API data
        "estimated_prices": {}  # Not needed for live data
    },
    "WinCo": {
        "multiplier": 0.95,  # Generally cheaper
        "default_distance_miles": 8.0,
        "confidence": "estimated",
        "estimated_prices": {
            "chicken breast": 3.29,
            "rice": 0.99,
            "pasta": 1.69,
            "eggs": 2.89,
            "onion": 0.79,
            "canned tomatoes": 1.29,
            "milk": 2.99,
            "banana": 0.59,
            "apple": 1.29,
            "bread": 2.49,
            "ground beef": 4.99,
            "potatoes": 0.69,
            "carrots": 0.89,
            "broccoli": 1.49,
            "salmon": 8.99,
            "spinach": 1.99,
            "tomato": 1.49,
            "olive oil": 5.99,
            "butter": 2.99,
            "cheese": 3.99
        }
    },
    "Costco": {
        "multiplier": 0.9,  # Bulk pricing
        "default_distance_miles": 12.0,
        "confidence": "estimated",
        "estimated_prices": {
            "chicken breast": 2.99,
            "rice": 0.89,
            "pasta": 1.59,
            "eggs": 2.79,
            "onion": 0.69,
            "canned tomatoes": 1.19,
            "milk": 2.89,
            "banana": 0.49,
            "apple": 1.19,
            "bread": 2.39,
            "ground beef": 4.79,
            "potatoes": 0.59,
            "carrots": 0.79,
            "broccoli": 1.39,
            "salmon": 8.79,
            "spinach": 1.89,
            "tomato": 1.39,
            "olive oil": 5.79,
            "butter": 2.89,
            "cheese": 3.79
        }
    },
    "Safeway": {
        "multiplier": 1.05,
        "default_distance_miles": 6.0,
        "confidence": "estimated",
        "estimated_prices": {
            "chicken breast": 3.99,
            "rice": 1.19,
            "pasta": 1.99,
            "eggs": 3.49,
            "onion": 0.99,
            "canned tomatoes": 1.49,
            "milk": 3.29,
            "banana": 0.69,
            "apple": 1.49,
            "bread": 2.79,
            "ground beef": 5.49,
            "potatoes": 0.79,
            "carrots": 0.99,
            "broccoli": 1.69,
            "salmon": 9.49,
            "spinach": 2.19,
            "tomato": 1.69,
            "olive oil": 6.29,
            "butter": 3.19,
            "cheese": 4.19
        }
    },
    "Walmart": {
        "multiplier": 0.98,
        "default_distance_miles": 4.0,
        "confidence": "estimated",
        "estimated_prices": {
            "chicken breast": 3.49,
            "rice": 1.09,
            "pasta": 1.79,
            "eggs": 2.99,
            "onion": 0.89,
            "canned tomatoes": 1.39,
            "milk": 3.09,
            "banana": 0.59,
            "apple": 1.29,
            "bread": 2.59,
            "ground beef": 4.99,
            "potatoes": 0.69,
            "carrots": 0.89,
            "broccoli": 1.49,
            "salmon": 8.99,
            "spinach": 1.99,
            "tomato": 1.49,
            "olive oil": 5.99,
            "butter": 2.99,
            "cheese": 3.99
        }
    },
    "Albertsons": {
        "multiplier": 1.08,
        "default_distance_miles": 7.0,
        "confidence": "estimated",
        "estimated_prices": {
            "chicken breast": 4.19,
            "rice": 1.29,
            "pasta": 2.09,
            "eggs": 3.69,
            "onion": 1.09,
            "canned tomatoes": 1.59,
            "milk": 3.39,
            "banana": 0.79,
            "apple": 1.59,
            "bread": 2.89,
            "ground beef": 5.69,
            "potatoes": 0.89,
            "carrots": 1.09,
            "broccoli": 1.79,
            "salmon": 9.69,
            "spinach": 2.29,
            "tomato": 1.79,
            "olive oil": 6.39,
            "butter": 3.29,
            "cheese": 4.29
        }
    },
    "Grocery Outlet": {
        "multiplier": 0.85,  # Discount store
        "default_distance_miles": 9.0,
        "confidence": "estimated",
        "estimated_prices": {
            "chicken breast": 2.99,
            "rice": 0.79,
            "pasta": 1.39,
            "eggs": 2.49,
            "onion": 0.59,
            "canned tomatoes": 0.99,
            "milk": 2.69,
            "banana": 0.39,
            "apple": 0.99,
            "bread": 1.99,
            "ground beef": 4.29,
            "potatoes": 0.49,
            "carrots": 0.69,
            "broccoli": 1.19,
            "salmon": 7.99,
            "spinach": 1.69,
            "tomato": 1.19,
            "olive oil": 4.99,
            "butter": 2.49,
            "cheese": 3.49
        }
    }
}


# =============================================================================
# SAMPLE MEALS DATA
# =============================================================================

SAMPLE_MEALS = [
    Meal(
        name="Pasta with Tomato Sauce",
        ingredients=[
            MealIngredient(ingredient_name="pasta", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="canned tomatoes", quantity=1, unit="can"),
            MealIngredient(ingredient_name="onion", quantity=0.5, unit="each")
        ],
        cook_time_minutes=20,
        equipment_required=["stove"]
    ),
    Meal(
        name="Chicken Rice Bowl",
        ingredients=[
            MealIngredient(ingredient_name="rice", quantity=1, unit="cup"),
            MealIngredient(ingredient_name="chicken breast", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="onion", quantity=0.25, unit="each")
        ],
        cook_time_minutes=30,
        equipment_required=["stove"]
    ),
    Meal(
        name="Scrambled Eggs",
        ingredients=[
            MealIngredient(ingredient_name="eggs", quantity=2, unit="each")
        ],
        cook_time_minutes=10,
        equipment_required=["stove"]
    ),
    Meal(
        name="Grilled Chicken Salad",
        ingredients=[
            MealIngredient(ingredient_name="chicken breast", quantity=0.75, unit="lb"),
            MealIngredient(ingredient_name="spinach", quantity=2, unit="cup"),
            MealIngredient(ingredient_name="tomato", quantity=1, unit="each"),
            MealIngredient(ingredient_name="carrots", quantity=2, unit="each")
        ],
        cook_time_minutes=25,
        equipment_required=["stove"]
    ),
    Meal(
        name="Beef Stir Fry",
        ingredients=[
            MealIngredient(ingredient_name="ground beef", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="rice", quantity=1, unit="cup"),
            MealIngredient(ingredient_name="broccoli", quantity=1, unit="cup"),
            MealIngredient(ingredient_name="carrots", quantity=1, unit="each"),
            MealIngredient(ingredient_name="onion", quantity=0.5, unit="each")
        ],
        cook_time_minutes=35,
        equipment_required=["stove"]
    ),
    Meal(
        name="Baked Salmon",
        ingredients=[
            MealIngredient(ingredient_name="salmon", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="potatoes", quantity=2, unit="each"),
            MealIngredient(ingredient_name="broccoli", quantity=1, unit="cup")
        ],
        cook_time_minutes=40,
        equipment_required=["oven"]
    ),
    Meal(
        name="Vegetable Stir Fry",
        ingredients=[
            MealIngredient(ingredient_name="rice", quantity=1, unit="cup"),
            MealIngredient(ingredient_name="broccoli", quantity=1.5, unit="cup"),
            MealIngredient(ingredient_name="carrots", quantity=2, unit="each"),
            MealIngredient(ingredient_name="onion", quantity=0.5, unit="each")
        ],
        cook_time_minutes=25,
        equipment_required=["stove"]
    )
]


# =============================================================================
# CONSTRAINT/FILTER DATA
# =============================================================================

DEFAULT_CONSTRAINTS = {
    "available_equipment": ["stove", "oven", "microwave"],
    "max_time_minutes": 45,
    "max_distance_miles": 10.0
}


# =============================================================================
# COMPUTATION FUNCTIONS
# =============================================================================

def compute_meal_data(meal: Meal, nutrition_provider, pricing_providers: Dict[str, Any]) -> Dict[str, Any]:
    """Compute all data for a single meal across all stores."""
    # Calculate nutrition
    nutrition = calculate_meal_nutrition(meal, nutrition_provider)

    # Calculate costs for each store using existing functions
    costs = {}
    for store_name, provider in pricing_providers.items():
        try:
            cost = calculate_meal_cost(meal, provider)
            costs[store_name] = round(cost, 2)
        except Exception as e:
            # Use estimated pricing if provider fails
            store_config = STORE_CONFIGURATIONS.get(store_name, {})
            estimated_prices = store_config.get("estimated_prices", {})
            total_cost = 0.0
            for ingredient in meal.ingredients:
                price = estimated_prices.get(ingredient.ingredient_name, 0.0)
                total_cost += price * ingredient.quantity
            costs[store_name] = round(total_cost, 2)

    return {
        "name": meal.name,
        "nutrition": nutrition,
        "costs": costs,
        "cook_time_minutes": meal.cook_time_minutes,
        "equipment_required": meal.equipment_required,
        "ingredients": [
            {
                "name": ing.ingredient_name,
                "quantity": ing.quantity,
                "unit": ing.unit
            }
            for ing in meal.ingredients
        ]
    }


def compute_store_data(store_name: str, meals: List[Meal], pricing_provider, zip_code: str = "97201") -> Dict[str, Any]:
    """Compute store-level data including total costs and distance."""
    # Set location for distance calculations
    try:
        pricing_provider.set_location(zip_code)
    except:
        pass  # Some providers don't need location

    # Calculate total cost for all meals using existing shopping list aggregation
    shopping_list = build_shopping_list(meals)
    try:
        total_cost = calculate_shopping_cost(shopping_list, pricing_provider)
    except Exception:
        # Use estimated pricing if provider fails
        store_config = STORE_CONFIGURATIONS.get(store_name, {})
        estimated_prices = store_config.get("estimated_prices", {})
        total_cost = 0.0
        for ingredient, quantity in shopping_list.items():
            price = estimated_prices.get(ingredient, 0.0)
            total_cost += price * quantity

    store_config = STORE_CONFIGURATIONS.get(store_name, {})

    return {
        "name": store_name,
        "total_cost": round(total_cost, 2),
        "distance_miles": store_config.get("default_distance_miles", 5.0),
        "confidence": store_config.get("confidence", "estimated"),
        "shopping_list": shopping_list
    }


def filter_meals_by_constraints(meals: List[Meal], constraints: Dict[str, Any]) -> List[Meal]:
    """Filter meals based on user constraints."""
    filtered = meals

    if "available_equipment" in constraints:
        filtered = filter_by_equipment(filtered, constraints["available_equipment"])

    if "max_time_minutes" in constraints:
        filtered = filter_by_time(filtered, constraints["max_time_minutes"])

    return filtered


# =============================================================================
# MAIN DATA PROCESSOR
# =============================================================================

def generate_decision_packet(user_profile: Dict[str, Any] = None,
                           zip_code: str = "97201") -> Dict[str, Any]:
    """
    Generate the complete decision packet for AI reasoning.

    Args:
        user_profile: User constraints and preferences
        zip_code: User's location for store distance calculations

    Returns:
        JSON-serializable decision packet
    """

    # Use default constraints if none provided
    if user_profile is None:
        user_profile = DEFAULT_CONSTRAINTS.copy()

    # Initialize providers
    nutrition_provider = build_nutrition_provider()

    # Build pricing providers for all stores
    pricing_providers = {}
    for store_name in get_supported_store_names():
        try:
            pricing_providers[store_name] = build_store_provider(store_name)
            pricing_providers[store_name].set_location(zip_code)
        except Exception as e:
            print(f"Warning: Could not initialize {store_name} provider: {e}")
            # Fallback to mock provider
            pricing_providers[store_name] = MockPricingProvider()

    # Filter meals based on constraints
    available_meals = filter_meals_by_constraints(SAMPLE_MEALS, user_profile)

    # Compute meal data
    meals_data = []
    for meal in available_meals:
        meal_data = compute_meal_data(meal, nutrition_provider, pricing_providers)
        meals_data.append(meal_data)

    # Compute store data
    stores_data = []
    for store_name, provider in pricing_providers.items():
        store_data = compute_store_data(store_name, available_meals, provider, zip_code)
        stores_data.append(store_data)

    # Build the decision packet
    decision_packet = {
        "user_profile": user_profile,
        "meals": meals_data,
        "stores": stores_data,
        "metadata": {
            "total_meals_available": len(meals_data),
            "total_stores_available": len(stores_data),
            "zip_code": zip_code,
            "generated_at": "2026-05-03T00:00:00Z"  # Current date
        }
    }

    return decision_packet


# =============================================================================
# JSON EXPORT FUNCTION
# =============================================================================

def export_to_json(decision_packet: Dict[str, Any], output_path: str = "decision_packet.json"):
    """Export the decision packet to a JSON file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(decision_packet, f, indent=2, ensure_ascii=False)

    print(f"Decision packet exported to {output_path}")
    return output_path


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    # Example usage
    user_profile = {
        "persona": "college_student",
        "budget": 50.0,
        "max_distance_miles": 10.0,
        "dietary_restrictions": [],
        "available_equipment": ["stove", "microwave"],
        "max_time_minutes": 30,
        "daily_calories": 2000,
        "protein": 150,
        "carbs": 250,
        "fat": 67
    }

    # Generate decision packet
    packet = generate_decision_packet(user_profile, zip_code="97201")

    # Export to JSON
    export_to_json(packet)

    # Print summary
    print(f"Generated decision packet with {len(packet['meals'])} meals and {len(packet['stores'])} stores")
    print("Ready for AI reasoning!")