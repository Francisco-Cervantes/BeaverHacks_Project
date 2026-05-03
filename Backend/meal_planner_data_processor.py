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
    },
    "bell pepper": {
        "calories": 31.0,
        "protein": 1.0,
        "carbs": 6.0,
        "fat": 0.3
    },
    "mushrooms": {
        "calories": 22.0,
        "protein": 3.1,
        "carbs": 3.3,
        "fat": 0.3
    },
    "sweet potato": {
        "calories": 86.0,
        "protein": 1.6,
        "carbs": 20.0,
        "fat": 0.1
    },
    "garlic": {
        "calories": 149.0,
        "protein": 6.4,
        "carbs": 33.0,
        "fat": 0.5
    },
    "ground turkey": {
        "calories": 189.0,
        "protein": 27.0,
        "carbs": 0.0,
        "fat": 9.0
    },
    "shrimp": {
        "calories": 99.0,
        "protein": 24.0,
        "carbs": 0.0,
        "fat": 0.3
    },
    "canned tuna": {
        "calories": 132.0,
        "protein": 29.0,
        "carbs": 0.0,
        "fat": 1.5
    },
    "black beans": {
        "calories": 132.0,
        "protein": 8.9,
        "carbs": 23.0,
        "fat": 0.5
    },
    "chickpeas": {
        "calories": 164.0,
        "protein": 8.9,
        "carbs": 27.0,
        "fat": 2.6
    },
    "lentils": {
        "calories": 116.0,
        "protein": 9.0,
        "carbs": 20.0,
        "fat": 0.4
    },
    "tofu": {
        "calories": 76.0,
        "protein": 8.1,
        "carbs": 1.9,
        "fat": 4.2
    },
    "tortillas": {
        "calories": 238.0,
        "protein": 6.0,
        "carbs": 44.0,
        "fat": 5.0
    },
    "avocado": {
        "calories": 160.0,
        "protein": 2.0,
        "carbs": 9.0,
        "fat": 15.0
    },
    "oats": {
        "calories": 389.0,
        "protein": 17.0,
        "carbs": 66.0,
        "fat": 7.0
    },
    "quinoa": {
        "calories": 120.0,
        "protein": 4.4,
        "carbs": 21.0,
        "fat": 1.9
    },
    "coconut milk": {
        "calories": 197.0,
        "protein": 2.0,
        "carbs": 6.0,
        "fat": 21.0
    },
    "greek yogurt": {
        "calories": 59.0,
        "protein": 10.0,
        "carbs": 3.6,
        "fat": 0.4
    },
    "mozzarella": {
        "calories": 280.0,
        "protein": 28.0,
        "carbs": 2.2,
        "fat": 17.0
    },
    "parmesan": {
        "calories": 431.0,
        "protein": 38.0,
        "carbs": 4.1,
        "fat": 29.0
    },
    "pork chops": {
        "calories": 231.0,
        "protein": 25.0,
        "carbs": 0.0,
        "fat": 14.0
    },
    "soy sauce": {
        "calories": 53.0,
        "protein": 8.1,
        "carbs": 5.0,
        "fat": 0.1
    },
    "cauliflower": {
        "calories": 25.0,
        "protein": 1.9,
        "carbs": 5.0,
        "fat": 0.3
    },
    "corn": {
        "calories": 86.0,
        "protein": 3.3,
        "carbs": 19.0,
        "fat": 1.4
    },
    "heavy cream": {
        "calories": 345.0,
        "protein": 2.8,
        "carbs": 2.8,
        "fat": 37.0
    },
    "chicken broth": {
        "calories": 15.0,
        "protein": 3.0,
        "carbs": 1.0,
        "fat": 0.5
    },
    "zucchini": {
        "calories": 17.0,
        "protein": 1.2,
        "carbs": 3.1,
        "fat": 0.3
    },
    "kale": {
        "calories": 49.0,
        "protein": 4.3,
        "carbs": 8.8,
        "fat": 0.9
    },
    "celery": {
        "calories": 16.0,
        "protein": 0.7,
        "carbs": 3.0,
        "fat": 0.2
    },
    "chicken thighs": {
        "calories": 209.0,
        "protein": 26.0,
        "carbs": 0.0,
        "fat": 10.9
    },
    "tilapia": {
        "calories": 128.0,
        "protein": 26.0,
        "carbs": 0.0,
        "fat": 2.7
    },
    "cod": {
        "calories": 82.0,
        "protein": 18.0,
        "carbs": 0.0,
        "fat": 0.7
    },
    "noodles": {
        "calories": 138.0,
        "protein": 4.5,
        "carbs": 25.0,
        "fat": 2.1
    },
    "kidney beans": {
        "calories": 127.0,
        "protein": 8.7,
        "carbs": 22.8,
        "fat": 0.5
    },
    "cabbage": {
        "calories": 25.0,
        "protein": 1.3,
        "carbs": 5.8,
        "fat": 0.1
    },
    "cucumber": {
        "calories": 15.0,
        "protein": 0.7,
        "carbs": 3.6,
        "fat": 0.1
    },
    "ginger": {
        "calories": 80.0,
        "protein": 1.8,
        "carbs": 18.0,
        "fat": 0.8
    },
    "peanut butter": {
        "calories": 588.0,
        "protein": 25.0,
        "carbs": 20.0,
        "fat": 50.0
    },
    "Italian sausage": {
        "calories": 301.0,
        "protein": 14.0,
        "carbs": 2.0,
        "fat": 27.0
    },
    "bacon": {
        "calories": 417.0,
        "protein": 37.0,
        "carbs": 1.3,
        "fat": 28.0
    },
    "turkey breast": {
        "calories": 189.0,
        "protein": 29.0,
        "carbs": 0.0,
        "fat": 7.0
    },
    "green beans": {
        "calories": 31.0,
        "protein": 1.8,
        "carbs": 7.0,
        "fat": 0.1
    },
    "asparagus": {
        "calories": 20.0,
        "protein": 2.2,
        "carbs": 3.9,
        "fat": 0.1
    },
    "brussels sprouts": {
        "calories": 43.0,
        "protein": 3.4,
        "carbs": 9.0,
        "fat": 0.3
    },
    "butternut squash": {
        "calories": 45.0,
        "protein": 1.0,
        "carbs": 11.7,
        "fat": 0.1
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
    "noodles": {"cup": 140.0},
    "eggs": {"each": 50.0},
    "onion": {"each": 110.0},
    "chicken breast": {"lb": 453.592},
    "chicken thighs": {"lb": 453.592},
    "ground beef": {"lb": 453.592},
    "ground turkey": {"lb": 453.592},
    "pork chops": {"lb": 453.592},
    "salmon": {"lb": 453.592},
    "shrimp": {"lb": 453.592},
    "tilapia": {"lb": 453.592},
    "cod": {"lb": 453.592},
    "Italian sausage": {"lb": 453.592},
    "bacon": {"lb": 453.592},
    "turkey breast": {"lb": 453.592},
    "tofu": {"lb": 453.592},
    "asparagus": {"lb": 453.592},
    "brussels sprouts": {"lb": 453.592},
    "green beans": {"cup": 100.0},
    "canned tomatoes": {"can": 240.0},
    "black beans": {"can": 240.0},
    "chickpeas": {"can": 240.0},
    "kidney beans": {"can": 240.0},
    "lentils": {"cup": 192.0},
    "oats": {"cup": 90.0},
    "quinoa": {"cup": 170.0},
    "coconut milk": {"can": 240.0},
    "chicken broth": {"can": 240.0},
    "banana": {"each": 118.0},
    "apple": {"each": 182.0},
    "potatoes": {"each": 173.0},
    "sweet potato": {"each": 200.0},
    "carrots": {"each": 61.0},
    "onion": {"each": 110.0},
    "cucumber": {"each": 200.0},
    "cabbage": {"each": 900.0},
    "cauliflower": {"each": 600.0},
    "butternut squash": {"each": 500.0},
    "bell pepper": {"each": 150.0},
    "tomato": {"each": 123.0},
    "mushrooms": {"cup": 70.0},
    "spinach": {"cup": 30.0},
    "broccoli": {"cup": 91.0},
    "kale": {"cup": 67.0},
    "corn": {"cup": 154.0},
    "greek yogurt": {"cup": 245.0},
    "milk": {"cup": 244.0},
    "heavy cream": {"cup": 238.0},
    "peanut butter": {"tbsp": 16.0},
    "soy sauce": {"tbsp": 18.0},
    "olive oil": {"tbsp": 14.0},
    "butter": {"tbsp": 14.0},
    "garlic": {"tbsp": 9.0},
    "ginger": {"oz": 28.35},
    "parmesan": {"tbsp": 5.0},
    "mozzarella": {"lb": 453.592},
    "bread": {"each": 30.0},
    "tortillas": {"each": 45.0},
    "avocado": {"each": 200.0},
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
            "cheese": 3.99,
            "chicken thighs": 2.49,
            "tilapia": 4.79,
            "cod": 6.79,
            "noodles": 1.59,
            "kidney beans": 0.89,
            "cabbage": 0.69,
            "cucumber": 0.79,
            "ginger": 0.69,
            "peanut butter": 3.29,
            "Italian sausage": 4.79,
            "bacon": 5.79,
            "turkey breast": 5.79,
            "green beans": 1.39,
            "asparagus": 3.79,
            "brussels sprouts": 2.79,
            "butternut squash": 2.29
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
            "cheese": 3.79,
            "chicken thighs": 2.39,
            "tilapia": 4.59,
            "cod": 6.59,
            "noodles": 1.49,
            "kidney beans": 0.79,
            "cabbage": 0.59,
            "cucumber": 0.69,
            "ginger": 0.59,
            "peanut butter": 2.99,
            "Italian sausage": 4.59,
            "bacon": 5.59,
            "turkey breast": 5.59,
            "green beans": 1.29,
            "asparagus": 3.59,
            "brussels sprouts": 2.59,
            "butternut squash": 2.09
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
            "cheese": 4.19,
            "chicken thighs": 3.19,
            "tilapia": 5.49,
            "cod": 7.49,
            "noodles": 1.89,
            "kidney beans": 1.09,
            "cabbage": 0.89,
            "cucumber": 0.99,
            "ginger": 0.89,
            "peanut butter": 3.99,
            "Italian sausage": 5.49,
            "bacon": 6.49,
            "turkey breast": 6.49,
            "green beans": 1.69,
            "asparagus": 4.49,
            "brussels sprouts": 3.49,
            "butternut squash": 2.99
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
            "cheese": 3.99,
            "chicken thighs": 2.69,
            "tilapia": 4.99,
            "cod": 6.99,
            "noodles": 1.69,
            "kidney beans": 0.99,
            "cabbage": 0.79,
            "cucumber": 0.89,
            "ginger": 0.79,
            "peanut butter": 3.49,
            "Italian sausage": 4.99,
            "bacon": 5.99,
            "turkey breast": 5.99,
            "green beans": 1.49,
            "asparagus": 3.99,
            "brussels sprouts": 2.99,
            "butternut squash": 2.49
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
            "cheese": 4.29,
            "chicken thighs": 3.29,
            "tilapia": 5.69,
            "cod": 7.69,
            "noodles": 1.99,
            "kidney beans": 1.19,
            "cabbage": 0.99,
            "cucumber": 1.09,
            "ginger": 0.99,
            "peanut butter": 4.19,
            "Italian sausage": 5.69,
            "bacon": 6.69,
            "turkey breast": 6.69,
            "green beans": 1.79,
            "asparagus": 4.69,
            "brussels sprouts": 3.69,
            "butternut squash": 3.19
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
            "cheese": 3.49,
            "chicken thighs": 2.29,
            "tilapia": 4.29,
            "cod": 5.99,
            "noodles": 1.39,
            "kidney beans": 0.79,
            "cabbage": 0.59,
            "cucumber": 0.69,
            "ginger": 0.59,
            "peanut butter": 2.99,
            "Italian sausage": 4.29,
            "bacon": 5.29,
            "turkey breast": 5.29,
            "green beans": 1.19,
            "asparagus": 3.49,
            "brussels sprouts": 2.49,
            "butternut squash": 1.99
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
    ),

    # -----------------------------------------------------------------------
    # BREAKFAST (10 meals)
    # -----------------------------------------------------------------------
    Meal(
        name="Avocado Toast with Egg",
        ingredients=[
            MealIngredient(ingredient_name="avocado", quantity=0.5, unit="each"),
            MealIngredient(ingredient_name="bread", quantity=2, unit="each"),
            MealIngredient(ingredient_name="eggs", quantity=2, unit="each"),
            MealIngredient(ingredient_name="tomato", quantity=1, unit="each"),
        ],
        cook_time_minutes=15,
        equipment_required=["stove"]
    ),
    Meal(
        name="Cheese Omelette",
        ingredients=[
            MealIngredient(ingredient_name="eggs", quantity=3, unit="each"),
            MealIngredient(ingredient_name="cheese", quantity=0.1, unit="lb"),
            MealIngredient(ingredient_name="butter", quantity=1, unit="tbsp"),
            MealIngredient(ingredient_name="bell pepper", quantity=1, unit="each"),
        ],
        cook_time_minutes=10,
        equipment_required=["stove"]
    ),
    Meal(
        name="Spinach Mushroom Omelette",
        ingredients=[
            MealIngredient(ingredient_name="eggs", quantity=3, unit="each"),
            MealIngredient(ingredient_name="spinach", quantity=1, unit="cup"),
            MealIngredient(ingredient_name="mushrooms", quantity=0.5, unit="cup"),
            MealIngredient(ingredient_name="butter", quantity=1, unit="tbsp"),
        ],
        cook_time_minutes=15,
        equipment_required=["stove"]
    ),
    Meal(
        name="Avocado Egg Toast",
        ingredients=[
            MealIngredient(ingredient_name="eggs", quantity=2, unit="each"),
            MealIngredient(ingredient_name="avocado", quantity=1, unit="each"),
            MealIngredient(ingredient_name="bread", quantity=2, unit="each"),
            MealIngredient(ingredient_name="tomato", quantity=1, unit="each"),
        ],
        cook_time_minutes=15,
        equipment_required=["stove"]
    ),
    Meal(
        name="Greek Yogurt Parfait",
        ingredients=[
            MealIngredient(ingredient_name="greek yogurt", quantity=1, unit="cup"),
            MealIngredient(ingredient_name="banana", quantity=1, unit="each"),
            MealIngredient(ingredient_name="oats", quantity=0.5, unit="cup"),
        ],
        cook_time_minutes=5,
        equipment_required=["microwave"]
    ),
    Meal(
        name="Peanut Butter Banana Oatmeal",
        ingredients=[
            MealIngredient(ingredient_name="oats", quantity=1, unit="cup"),
            MealIngredient(ingredient_name="peanut butter", quantity=2, unit="tbsp"),
            MealIngredient(ingredient_name="banana", quantity=1, unit="each"),
            MealIngredient(ingredient_name="milk", quantity=0.5, unit="cup"),
        ],
        cook_time_minutes=10,
        equipment_required=["stove"]
    ),
    Meal(
        name="Bacon and Egg Scramble",
        ingredients=[
            MealIngredient(ingredient_name="bacon", quantity=0.25, unit="lb"),
            MealIngredient(ingredient_name="eggs", quantity=3, unit="each"),
            MealIngredient(ingredient_name="onion", quantity=0.5, unit="each"),
            MealIngredient(ingredient_name="bell pepper", quantity=1, unit="each"),
        ],
        cook_time_minutes=15,
        equipment_required=["stove"]
    ),
    Meal(
        name="Veggie Frittata",
        ingredients=[
            MealIngredient(ingredient_name="eggs", quantity=4, unit="each"),
            MealIngredient(ingredient_name="bell pepper", quantity=2, unit="each"),
            MealIngredient(ingredient_name="onion", quantity=0.5, unit="each"),
            MealIngredient(ingredient_name="spinach", quantity=1, unit="cup"),
            MealIngredient(ingredient_name="mushrooms", quantity=0.5, unit="cup"),
        ],
        cook_time_minutes=25,
        equipment_required=["oven"]
    ),
    Meal(
        name="Microwave Scrambled Eggs",
        ingredients=[
            MealIngredient(ingredient_name="eggs", quantity=3, unit="each"),
            MealIngredient(ingredient_name="milk", quantity=0.25, unit="cup"),
            MealIngredient(ingredient_name="cheese", quantity=0.1, unit="lb"),
        ],
        cook_time_minutes=5,
        equipment_required=["microwave"]
    ),
    Meal(
        name="Microwave Oatmeal with Banana",
        ingredients=[
            MealIngredient(ingredient_name="oats", quantity=1, unit="cup"),
            MealIngredient(ingredient_name="milk", quantity=0.5, unit="cup"),
            MealIngredient(ingredient_name="banana", quantity=1, unit="each"),
        ],
        cook_time_minutes=5,
        equipment_required=["microwave"]
    ),

    # -----------------------------------------------------------------------
    # SANDWICHES / WRAPS / TACOS (10 meals)
    # -----------------------------------------------------------------------
    Meal(
        name="Tuna Salad Sandwich",
        ingredients=[
            MealIngredient(ingredient_name="canned tuna", quantity=1, unit="can"),
            MealIngredient(ingredient_name="bread", quantity=2, unit="each"),
            MealIngredient(ingredient_name="celery", quantity=1, unit="each"),
            MealIngredient(ingredient_name="onion", quantity=0.25, unit="each"),
        ],
        cook_time_minutes=10,
        equipment_required=["stove"]
    ),
    Meal(
        name="Black Bean Quesadilla",
        ingredients=[
            MealIngredient(ingredient_name="tortillas", quantity=2, unit="each"),
            MealIngredient(ingredient_name="black beans", quantity=0.5, unit="can"),
            MealIngredient(ingredient_name="cheese", quantity=0.125, unit="lb"),
            MealIngredient(ingredient_name="onion", quantity=0.25, unit="each"),
        ],
        cook_time_minutes=15,
        equipment_required=["stove"]
    ),
    Meal(
        name="Chicken Tacos",
        ingredients=[
            MealIngredient(ingredient_name="chicken breast", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="tortillas", quantity=3, unit="each"),
            MealIngredient(ingredient_name="onion", quantity=0.5, unit="each"),
            MealIngredient(ingredient_name="bell pepper", quantity=1, unit="each"),
            MealIngredient(ingredient_name="avocado", quantity=0.5, unit="each"),
        ],
        cook_time_minutes=25,
        equipment_required=["stove"]
    ),
    Meal(
        name="Beef Tacos",
        ingredients=[
            MealIngredient(ingredient_name="ground beef", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="tortillas", quantity=3, unit="each"),
            MealIngredient(ingredient_name="onion", quantity=0.5, unit="each"),
            MealIngredient(ingredient_name="tomato", quantity=2, unit="each"),
            MealIngredient(ingredient_name="cheese", quantity=0.125, unit="lb"),
        ],
        cook_time_minutes=25,
        equipment_required=["stove"]
    ),
    Meal(
        name="Shrimp Tacos",
        ingredients=[
            MealIngredient(ingredient_name="shrimp", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="tortillas", quantity=3, unit="each"),
            MealIngredient(ingredient_name="cabbage", quantity=0.25, unit="each"),
            MealIngredient(ingredient_name="avocado", quantity=1, unit="each"),
            MealIngredient(ingredient_name="tomato", quantity=1, unit="each"),
        ],
        cook_time_minutes=20,
        equipment_required=["stove"]
    ),
    Meal(
        name="Chicken Quesadilla",
        ingredients=[
            MealIngredient(ingredient_name="chicken breast", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="tortillas", quantity=2, unit="each"),
            MealIngredient(ingredient_name="cheese", quantity=0.25, unit="lb"),
            MealIngredient(ingredient_name="bell pepper", quantity=1, unit="each"),
        ],
        cook_time_minutes=20,
        equipment_required=["stove"]
    ),
    Meal(
        name="Ground Turkey Lettuce Wraps",
        ingredients=[
            MealIngredient(ingredient_name="ground turkey", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="cabbage", quantity=0.25, unit="each"),
            MealIngredient(ingredient_name="onion", quantity=0.5, unit="each"),
            MealIngredient(ingredient_name="soy sauce", quantity=2, unit="tbsp"),
            MealIngredient(ingredient_name="ginger", quantity=0.5, unit="oz"),
            MealIngredient(ingredient_name="garlic", quantity=1, unit="tbsp"),
        ],
        cook_time_minutes=25,
        equipment_required=["stove"]
    ),
    Meal(
        name="Chicken Burrito",
        ingredients=[
            MealIngredient(ingredient_name="chicken breast", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="tortillas", quantity=2, unit="each"),
            MealIngredient(ingredient_name="rice", quantity=0.5, unit="cup"),
            MealIngredient(ingredient_name="black beans", quantity=0.5, unit="can"),
            MealIngredient(ingredient_name="cheese", quantity=0.125, unit="lb"),
        ],
        cook_time_minutes=25,
        equipment_required=["stove"]
    ),
    Meal(
        name="Black Bean Burrito Bowl",
        ingredients=[
            MealIngredient(ingredient_name="black beans", quantity=1, unit="can"),
            MealIngredient(ingredient_name="rice", quantity=1, unit="cup"),
            MealIngredient(ingredient_name="corn", quantity=1, unit="cup"),
            MealIngredient(ingredient_name="onion", quantity=0.5, unit="each"),
            MealIngredient(ingredient_name="bell pepper", quantity=1, unit="each"),
            MealIngredient(ingredient_name="avocado", quantity=0.5, unit="each"),
        ],
        cook_time_minutes=25,
        equipment_required=["stove"]
    ),
    Meal(
        name="Turkey Avocado Wrap",
        ingredients=[
            MealIngredient(ingredient_name="turkey breast", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="tortillas", quantity=2, unit="each"),
            MealIngredient(ingredient_name="avocado", quantity=1, unit="each"),
            MealIngredient(ingredient_name="tomato", quantity=1, unit="each"),
            MealIngredient(ingredient_name="spinach", quantity=1, unit="cup"),
        ],
        cook_time_minutes=15,
        equipment_required=["stove"]
    ),

    # -----------------------------------------------------------------------
    # RICE & NOODLE BOWLS (12 meals)
    # -----------------------------------------------------------------------
    Meal(
        name="Egg Fried Rice",
        ingredients=[
            MealIngredient(ingredient_name="rice", quantity=1, unit="cup"),
            MealIngredient(ingredient_name="eggs", quantity=2, unit="each"),
            MealIngredient(ingredient_name="onion", quantity=0.5, unit="each"),
            MealIngredient(ingredient_name="soy sauce", quantity=2, unit="tbsp"),
            MealIngredient(ingredient_name="carrots", quantity=1, unit="each"),
        ],
        cook_time_minutes=20,
        equipment_required=["stove"]
    ),
    Meal(
        name="Shrimp Fried Rice",
        ingredients=[
            MealIngredient(ingredient_name="shrimp", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="rice", quantity=1, unit="cup"),
            MealIngredient(ingredient_name="eggs", quantity=1, unit="each"),
            MealIngredient(ingredient_name="carrots", quantity=1, unit="each"),
            MealIngredient(ingredient_name="onion", quantity=0.5, unit="each"),
            MealIngredient(ingredient_name="soy sauce", quantity=2, unit="tbsp"),
        ],
        cook_time_minutes=20,
        equipment_required=["stove"]
    ),
    Meal(
        name="Pork Fried Rice",
        ingredients=[
            MealIngredient(ingredient_name="pork chops", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="rice", quantity=1, unit="cup"),
            MealIngredient(ingredient_name="eggs", quantity=1, unit="each"),
            MealIngredient(ingredient_name="onion", quantity=0.5, unit="each"),
            MealIngredient(ingredient_name="soy sauce", quantity=2, unit="tbsp"),
            MealIngredient(ingredient_name="carrots", quantity=1, unit="each"),
        ],
        cook_time_minutes=30,
        equipment_required=["stove"]
    ),
    Meal(
        name="Cauliflower Fried Rice",
        ingredients=[
            MealIngredient(ingredient_name="cauliflower", quantity=1, unit="each"),
            MealIngredient(ingredient_name="eggs", quantity=2, unit="each"),
            MealIngredient(ingredient_name="carrots", quantity=2, unit="each"),
            MealIngredient(ingredient_name="onion", quantity=0.5, unit="each"),
            MealIngredient(ingredient_name="soy sauce", quantity=2, unit="tbsp"),
        ],
        cook_time_minutes=20,
        equipment_required=["stove"]
    ),
    Meal(
        name="Korean Beef Bowl",
        ingredients=[
            MealIngredient(ingredient_name="ground beef", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="rice", quantity=1, unit="cup"),
            MealIngredient(ingredient_name="soy sauce", quantity=3, unit="tbsp"),
            MealIngredient(ingredient_name="ginger", quantity=0.5, unit="oz"),
            MealIngredient(ingredient_name="garlic", quantity=2, unit="tbsp"),
            MealIngredient(ingredient_name="carrots", quantity=1, unit="each"),
        ],
        cook_time_minutes=25,
        equipment_required=["stove"]
    ),
    Meal(
        name="Tuna Rice Bowl",
        ingredients=[
            MealIngredient(ingredient_name="canned tuna", quantity=1, unit="can"),
            MealIngredient(ingredient_name="rice", quantity=1, unit="cup"),
            MealIngredient(ingredient_name="soy sauce", quantity=2, unit="tbsp"),
            MealIngredient(ingredient_name="cucumber", quantity=1, unit="each"),
            MealIngredient(ingredient_name="avocado", quantity=0.5, unit="each"),
        ],
        cook_time_minutes=20,
        equipment_required=["stove"]
    ),
    Meal(
        name="Avocado Chicken Rice Bowl",
        ingredients=[
            MealIngredient(ingredient_name="chicken breast", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="rice", quantity=1, unit="cup"),
            MealIngredient(ingredient_name="avocado", quantity=1, unit="each"),
            MealIngredient(ingredient_name="tomato", quantity=1, unit="each"),
        ],
        cook_time_minutes=30,
        equipment_required=["stove"]
    ),
    Meal(
        name="Turkey Taco Bowl",
        ingredients=[
            MealIngredient(ingredient_name="ground turkey", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="rice", quantity=1, unit="cup"),
            MealIngredient(ingredient_name="black beans", quantity=0.5, unit="can"),
            MealIngredient(ingredient_name="corn", quantity=0.5, unit="cup"),
            MealIngredient(ingredient_name="onion", quantity=0.5, unit="each"),
            MealIngredient(ingredient_name="bell pepper", quantity=1, unit="each"),
        ],
        cook_time_minutes=30,
        equipment_required=["stove"]
    ),
    Meal(
        name="Salmon Quinoa Bowl",
        ingredients=[
            MealIngredient(ingredient_name="salmon", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="quinoa", quantity=1, unit="cup"),
            MealIngredient(ingredient_name="spinach", quantity=2, unit="cup"),
            MealIngredient(ingredient_name="avocado", quantity=0.5, unit="each"),
        ],
        cook_time_minutes=30,
        equipment_required=["stove"]
    ),
    Meal(
        name="Thai Peanut Noodles",
        ingredients=[
            MealIngredient(ingredient_name="noodles", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="peanut butter", quantity=3, unit="tbsp"),
            MealIngredient(ingredient_name="soy sauce", quantity=2, unit="tbsp"),
            MealIngredient(ingredient_name="carrots", quantity=2, unit="each"),
            MealIngredient(ingredient_name="cabbage", quantity=0.25, unit="each"),
        ],
        cook_time_minutes=25,
        equipment_required=["stove"]
    ),
    Meal(
        name="Chicken Noodle Soup",
        ingredients=[
            MealIngredient(ingredient_name="chicken breast", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="noodles", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="carrots", quantity=2, unit="each"),
            MealIngredient(ingredient_name="celery", quantity=2, unit="each"),
            MealIngredient(ingredient_name="chicken broth", quantity=1, unit="can"),
            MealIngredient(ingredient_name="onion", quantity=0.5, unit="each"),
        ],
        cook_time_minutes=35,
        equipment_required=["stove"]
    ),
    Meal(
        name="Quinoa Power Bowl",
        ingredients=[
            MealIngredient(ingredient_name="quinoa", quantity=1, unit="cup"),
            MealIngredient(ingredient_name="chicken breast", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="spinach", quantity=2, unit="cup"),
            MealIngredient(ingredient_name="avocado", quantity=0.5, unit="each"),
            MealIngredient(ingredient_name="carrots", quantity=1, unit="each"),
        ],
        cook_time_minutes=30,
        equipment_required=["stove"]
    ),

    # -----------------------------------------------------------------------
    # PASTA (8 meals)
    # -----------------------------------------------------------------------
    Meal(
        name="Spaghetti Bolognese",
        ingredients=[
            MealIngredient(ingredient_name="pasta", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="ground beef", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="canned tomatoes", quantity=1, unit="can"),
            MealIngredient(ingredient_name="onion", quantity=1, unit="each"),
            MealIngredient(ingredient_name="garlic", quantity=2, unit="tbsp"),
        ],
        cook_time_minutes=35,
        equipment_required=["stove"]
    ),
    Meal(
        name="Mushroom Spinach Pasta",
        ingredients=[
            MealIngredient(ingredient_name="pasta", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="mushrooms", quantity=1.5, unit="cup"),
            MealIngredient(ingredient_name="spinach", quantity=2, unit="cup"),
            MealIngredient(ingredient_name="garlic", quantity=2, unit="tbsp"),
            MealIngredient(ingredient_name="olive oil", quantity=2, unit="tbsp"),
        ],
        cook_time_minutes=25,
        equipment_required=["stove"]
    ),
    Meal(
        name="Ground Turkey Spaghetti",
        ingredients=[
            MealIngredient(ingredient_name="pasta", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="ground turkey", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="canned tomatoes", quantity=1, unit="can"),
            MealIngredient(ingredient_name="onion", quantity=1, unit="each"),
            MealIngredient(ingredient_name="garlic", quantity=2, unit="tbsp"),
        ],
        cook_time_minutes=30,
        equipment_required=["stove"]
    ),
    Meal(
        name="Caprese Pasta",
        ingredients=[
            MealIngredient(ingredient_name="pasta", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="mozzarella", quantity=0.25, unit="lb"),
            MealIngredient(ingredient_name="tomato", quantity=3, unit="each"),
            MealIngredient(ingredient_name="olive oil", quantity=2, unit="tbsp"),
            MealIngredient(ingredient_name="garlic", quantity=2, unit="tbsp"),
        ],
        cook_time_minutes=20,
        equipment_required=["stove"]
    ),
    Meal(
        name="Pasta Primavera",
        ingredients=[
            MealIngredient(ingredient_name="pasta", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="zucchini", quantity=1, unit="each"),
            MealIngredient(ingredient_name="bell pepper", quantity=1, unit="each"),
            MealIngredient(ingredient_name="tomato", quantity=2, unit="each"),
            MealIngredient(ingredient_name="olive oil", quantity=2, unit="tbsp"),
            MealIngredient(ingredient_name="garlic", quantity=2, unit="tbsp"),
        ],
        cook_time_minutes=25,
        equipment_required=["stove"]
    ),
    Meal(
        name="Sausage Pepper Pasta",
        ingredients=[
            MealIngredient(ingredient_name="pasta", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="Italian sausage", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="bell pepper", quantity=2, unit="each"),
            MealIngredient(ingredient_name="onion", quantity=1, unit="each"),
            MealIngredient(ingredient_name="canned tomatoes", quantity=1, unit="can"),
        ],
        cook_time_minutes=35,
        equipment_required=["stove"]
    ),
    Meal(
        name="Pesto Pasta with Chicken",
        ingredients=[
            MealIngredient(ingredient_name="pasta", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="chicken breast", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="spinach", quantity=1, unit="cup"),
            MealIngredient(ingredient_name="garlic", quantity=2, unit="tbsp"),
            MealIngredient(ingredient_name="parmesan", quantity=2, unit="tbsp"),
            MealIngredient(ingredient_name="olive oil", quantity=3, unit="tbsp"),
        ],
        cook_time_minutes=30,
        equipment_required=["stove"]
    ),
    Meal(
        name="Salmon Pasta",
        ingredients=[
            MealIngredient(ingredient_name="pasta", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="salmon", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="spinach", quantity=1, unit="cup"),
            MealIngredient(ingredient_name="garlic", quantity=2, unit="tbsp"),
            MealIngredient(ingredient_name="heavy cream", quantity=0.25, unit="cup"),
        ],
        cook_time_minutes=30,
        equipment_required=["stove"]
    ),

    # -----------------------------------------------------------------------
    # SOUPS & STEWS (8 meals)
    # -----------------------------------------------------------------------
    Meal(
        name="Lentil Soup",
        ingredients=[
            MealIngredient(ingredient_name="lentils", quantity=1, unit="cup"),
            MealIngredient(ingredient_name="carrots", quantity=2, unit="each"),
            MealIngredient(ingredient_name="celery", quantity=2, unit="each"),
            MealIngredient(ingredient_name="onion", quantity=1, unit="each"),
            MealIngredient(ingredient_name="chicken broth", quantity=1, unit="can"),
            MealIngredient(ingredient_name="garlic", quantity=1, unit="tbsp"),
        ],
        cook_time_minutes=35,
        equipment_required=["stove"]
    ),
    Meal(
        name="Black Bean Soup",
        ingredients=[
            MealIngredient(ingredient_name="black beans", quantity=1, unit="can"),
            MealIngredient(ingredient_name="onion", quantity=1, unit="each"),
            MealIngredient(ingredient_name="garlic", quantity=2, unit="tbsp"),
            MealIngredient(ingredient_name="chicken broth", quantity=1, unit="can"),
            MealIngredient(ingredient_name="corn", quantity=0.5, unit="cup"),
        ],
        cook_time_minutes=30,
        equipment_required=["stove"]
    ),
    Meal(
        name="Chicken Vegetable Soup",
        ingredients=[
            MealIngredient(ingredient_name="chicken breast", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="carrots", quantity=2, unit="each"),
            MealIngredient(ingredient_name="celery", quantity=2, unit="each"),
            MealIngredient(ingredient_name="onion", quantity=1, unit="each"),
            MealIngredient(ingredient_name="chicken broth", quantity=1, unit="can"),
            MealIngredient(ingredient_name="zucchini", quantity=1, unit="each"),
        ],
        cook_time_minutes=35,
        equipment_required=["stove"]
    ),
    Meal(
        name="Coconut Lentil Soup",
        ingredients=[
            MealIngredient(ingredient_name="lentils", quantity=1, unit="cup"),
            MealIngredient(ingredient_name="coconut milk", quantity=1, unit="can"),
            MealIngredient(ingredient_name="carrots", quantity=2, unit="each"),
            MealIngredient(ingredient_name="onion", quantity=1, unit="each"),
            MealIngredient(ingredient_name="ginger", quantity=0.5, unit="oz"),
            MealIngredient(ingredient_name="garlic", quantity=1, unit="tbsp"),
        ],
        cook_time_minutes=35,
        equipment_required=["stove"]
    ),
    Meal(
        name="Beef Potato Stew",
        ingredients=[
            MealIngredient(ingredient_name="ground beef", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="potatoes", quantity=3, unit="each"),
            MealIngredient(ingredient_name="carrots", quantity=2, unit="each"),
            MealIngredient(ingredient_name="onion", quantity=1, unit="each"),
            MealIngredient(ingredient_name="celery", quantity=2, unit="each"),
            MealIngredient(ingredient_name="chicken broth", quantity=1, unit="can"),
        ],
        cook_time_minutes=40,
        equipment_required=["stove"]
    ),
    Meal(
        name="Turkey Vegetable Soup",
        ingredients=[
            MealIngredient(ingredient_name="ground turkey", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="carrots", quantity=2, unit="each"),
            MealIngredient(ingredient_name="celery", quantity=2, unit="each"),
            MealIngredient(ingredient_name="onion", quantity=1, unit="each"),
            MealIngredient(ingredient_name="chicken broth", quantity=1, unit="can"),
            MealIngredient(ingredient_name="zucchini", quantity=1, unit="each"),
        ],
        cook_time_minutes=35,
        equipment_required=["stove"]
    ),
    Meal(
        name="Mushroom Risotto",
        ingredients=[
            MealIngredient(ingredient_name="rice", quantity=1.5, unit="cup"),
            MealIngredient(ingredient_name="mushrooms", quantity=2, unit="cup"),
            MealIngredient(ingredient_name="onion", quantity=1, unit="each"),
            MealIngredient(ingredient_name="chicken broth", quantity=1, unit="can"),
            MealIngredient(ingredient_name="parmesan", quantity=2, unit="tbsp"),
            MealIngredient(ingredient_name="butter", quantity=1, unit="tbsp"),
        ],
        cook_time_minutes=35,
        equipment_required=["stove"]
    ),
    Meal(
        name="Butternut Squash Soup",
        ingredients=[
            MealIngredient(ingredient_name="butternut squash", quantity=1, unit="each"),
            MealIngredient(ingredient_name="onion", quantity=1, unit="each"),
            MealIngredient(ingredient_name="chicken broth", quantity=1, unit="can"),
            MealIngredient(ingredient_name="heavy cream", quantity=0.25, unit="cup"),
            MealIngredient(ingredient_name="garlic", quantity=2, unit="tbsp"),
        ],
        cook_time_minutes=45,
        equipment_required=["stove"]
    ),

    # -----------------------------------------------------------------------
    # CURRIES (8 meals)
    # -----------------------------------------------------------------------
    Meal(
        name="Chickpea Coconut Curry",
        ingredients=[
            MealIngredient(ingredient_name="chickpeas", quantity=1, unit="can"),
            MealIngredient(ingredient_name="coconut milk", quantity=1, unit="can"),
            MealIngredient(ingredient_name="onion", quantity=1, unit="each"),
            MealIngredient(ingredient_name="tomato", quantity=2, unit="each"),
            MealIngredient(ingredient_name="garlic", quantity=2, unit="tbsp"),
            MealIngredient(ingredient_name="spinach", quantity=1, unit="cup"),
        ],
        cook_time_minutes=30,
        equipment_required=["stove"]
    ),
    Meal(
        name="Lentil Dal",
        ingredients=[
            MealIngredient(ingredient_name="lentils", quantity=1, unit="cup"),
            MealIngredient(ingredient_name="coconut milk", quantity=0.5, unit="can"),
            MealIngredient(ingredient_name="tomato", quantity=2, unit="each"),
            MealIngredient(ingredient_name="onion", quantity=1, unit="each"),
            MealIngredient(ingredient_name="garlic", quantity=2, unit="tbsp"),
            MealIngredient(ingredient_name="ginger", quantity=0.5, unit="oz"),
        ],
        cook_time_minutes=35,
        equipment_required=["stove"]
    ),
    Meal(
        name="Tofu Tikka Masala",
        ingredients=[
            MealIngredient(ingredient_name="tofu", quantity=0.75, unit="lb"),
            MealIngredient(ingredient_name="canned tomatoes", quantity=1, unit="can"),
            MealIngredient(ingredient_name="coconut milk", quantity=0.5, unit="can"),
            MealIngredient(ingredient_name="onion", quantity=1, unit="each"),
            MealIngredient(ingredient_name="garlic", quantity=2, unit="tbsp"),
            MealIngredient(ingredient_name="ginger", quantity=0.5, unit="oz"),
        ],
        cook_time_minutes=30,
        equipment_required=["stove"]
    ),
    Meal(
        name="Chicken Tikka Masala",
        ingredients=[
            MealIngredient(ingredient_name="chicken breast", quantity=0.75, unit="lb"),
            MealIngredient(ingredient_name="canned tomatoes", quantity=1, unit="can"),
            MealIngredient(ingredient_name="heavy cream", quantity=0.5, unit="cup"),
            MealIngredient(ingredient_name="onion", quantity=1, unit="each"),
            MealIngredient(ingredient_name="garlic", quantity=2, unit="tbsp"),
            MealIngredient(ingredient_name="ginger", quantity=0.5, unit="oz"),
        ],
        cook_time_minutes=35,
        equipment_required=["stove"]
    ),
    Meal(
        name="Butter Chicken",
        ingredients=[
            MealIngredient(ingredient_name="chicken breast", quantity=0.75, unit="lb"),
            MealIngredient(ingredient_name="canned tomatoes", quantity=1, unit="can"),
            MealIngredient(ingredient_name="heavy cream", quantity=0.5, unit="cup"),
            MealIngredient(ingredient_name="butter", quantity=2, unit="tbsp"),
            MealIngredient(ingredient_name="onion", quantity=1, unit="each"),
            MealIngredient(ingredient_name="garlic", quantity=2, unit="tbsp"),
            MealIngredient(ingredient_name="ginger", quantity=0.5, unit="oz"),
        ],
        cook_time_minutes=35,
        equipment_required=["stove"]
    ),
    Meal(
        name="Chickpea Spinach Curry",
        ingredients=[
            MealIngredient(ingredient_name="chickpeas", quantity=1, unit="can"),
            MealIngredient(ingredient_name="spinach", quantity=2, unit="cup"),
            MealIngredient(ingredient_name="canned tomatoes", quantity=1, unit="can"),
            MealIngredient(ingredient_name="coconut milk", quantity=0.5, unit="can"),
            MealIngredient(ingredient_name="garlic", quantity=2, unit="tbsp"),
        ],
        cook_time_minutes=30,
        equipment_required=["stove"]
    ),
    Meal(
        name="Coconut Shrimp Curry",
        ingredients=[
            MealIngredient(ingredient_name="shrimp", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="coconut milk", quantity=1, unit="can"),
            MealIngredient(ingredient_name="bell pepper", quantity=1, unit="each"),
            MealIngredient(ingredient_name="onion", quantity=0.5, unit="each"),
            MealIngredient(ingredient_name="garlic", quantity=2, unit="tbsp"),
            MealIngredient(ingredient_name="ginger", quantity=0.5, unit="oz"),
            MealIngredient(ingredient_name="rice", quantity=1, unit="cup"),
        ],
        cook_time_minutes=30,
        equipment_required=["stove"]
    ),
    Meal(
        name="Thai Green Curry with Tofu",
        ingredients=[
            MealIngredient(ingredient_name="tofu", quantity=0.75, unit="lb"),
            MealIngredient(ingredient_name="coconut milk", quantity=1, unit="can"),
            MealIngredient(ingredient_name="zucchini", quantity=1, unit="each"),
            MealIngredient(ingredient_name="bell pepper", quantity=1, unit="each"),
            MealIngredient(ingredient_name="spinach", quantity=1, unit="cup"),
            MealIngredient(ingredient_name="garlic", quantity=2, unit="tbsp"),
            MealIngredient(ingredient_name="ginger", quantity=0.5, unit="oz"),
        ],
        cook_time_minutes=25,
        equipment_required=["stove"]
    ),

    # -----------------------------------------------------------------------
    # OVEN-BAKED (22 meals)
    # -----------------------------------------------------------------------
    Meal(
        name="Roasted Chicken Thighs and Vegetables",
        ingredients=[
            MealIngredient(ingredient_name="chicken thighs", quantity=1, unit="lb"),
            MealIngredient(ingredient_name="potatoes", quantity=3, unit="each"),
            MealIngredient(ingredient_name="carrots", quantity=3, unit="each"),
            MealIngredient(ingredient_name="onion", quantity=1, unit="each"),
            MealIngredient(ingredient_name="olive oil", quantity=2, unit="tbsp"),
        ],
        cook_time_minutes=45,
        equipment_required=["oven"]
    ),
    Meal(
        name="Baked Tilapia with Sweet Potato",
        ingredients=[
            MealIngredient(ingredient_name="tilapia", quantity=0.75, unit="lb"),
            MealIngredient(ingredient_name="sweet potato", quantity=2, unit="each"),
            MealIngredient(ingredient_name="broccoli", quantity=1, unit="cup"),
            MealIngredient(ingredient_name="olive oil", quantity=2, unit="tbsp"),
        ],
        cook_time_minutes=35,
        equipment_required=["oven"]
    ),
    Meal(
        name="Baked Chicken Breast with Broccoli",
        ingredients=[
            MealIngredient(ingredient_name="chicken breast", quantity=0.75, unit="lb"),
            MealIngredient(ingredient_name="broccoli", quantity=2, unit="cup"),
            MealIngredient(ingredient_name="garlic", quantity=2, unit="tbsp"),
            MealIngredient(ingredient_name="olive oil", quantity=2, unit="tbsp"),
        ],
        cook_time_minutes=30,
        equipment_required=["oven"]
    ),
    Meal(
        name="Stuffed Bell Peppers with Beef and Rice",
        ingredients=[
            MealIngredient(ingredient_name="bell pepper", quantity=4, unit="each"),
            MealIngredient(ingredient_name="ground beef", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="rice", quantity=0.5, unit="cup"),
            MealIngredient(ingredient_name="canned tomatoes", quantity=0.5, unit="can"),
            MealIngredient(ingredient_name="cheese", quantity=0.125, unit="lb"),
        ],
        cook_time_minutes=45,
        equipment_required=["oven"]
    ),
    Meal(
        name="Baked Cod with Green Beans",
        ingredients=[
            MealIngredient(ingredient_name="cod", quantity=0.75, unit="lb"),
            MealIngredient(ingredient_name="green beans", quantity=1, unit="cup"),
            MealIngredient(ingredient_name="potatoes", quantity=2, unit="each"),
            MealIngredient(ingredient_name="olive oil", quantity=2, unit="tbsp"),
        ],
        cook_time_minutes=30,
        equipment_required=["oven"]
    ),
    Meal(
        name="Roasted Vegetable Medley",
        ingredients=[
            MealIngredient(ingredient_name="zucchini", quantity=1, unit="each"),
            MealIngredient(ingredient_name="bell pepper", quantity=2, unit="each"),
            MealIngredient(ingredient_name="mushrooms", quantity=1, unit="cup"),
            MealIngredient(ingredient_name="onion", quantity=1, unit="each"),
            MealIngredient(ingredient_name="sweet potato", quantity=1, unit="each"),
            MealIngredient(ingredient_name="olive oil", quantity=3, unit="tbsp"),
        ],
        cook_time_minutes=35,
        equipment_required=["oven"]
    ),
    Meal(
        name="Chicken and Potato Bake",
        ingredients=[
            MealIngredient(ingredient_name="chicken thighs", quantity=1, unit="lb"),
            MealIngredient(ingredient_name="potatoes", quantity=4, unit="each"),
            MealIngredient(ingredient_name="onion", quantity=1, unit="each"),
            MealIngredient(ingredient_name="garlic", quantity=2, unit="tbsp"),
            MealIngredient(ingredient_name="olive oil", quantity=2, unit="tbsp"),
        ],
        cook_time_minutes=45,
        equipment_required=["oven"]
    ),
    Meal(
        name="Shakshuka",
        ingredients=[
            MealIngredient(ingredient_name="eggs", quantity=4, unit="each"),
            MealIngredient(ingredient_name="canned tomatoes", quantity=1, unit="can"),
            MealIngredient(ingredient_name="bell pepper", quantity=2, unit="each"),
            MealIngredient(ingredient_name="onion", quantity=1, unit="each"),
            MealIngredient(ingredient_name="garlic", quantity=2, unit="tbsp"),
        ],
        cook_time_minutes=30,
        equipment_required=["stove"]
    ),
    Meal(
        name="Roasted Sweet Potato Chickpea Bowl",
        ingredients=[
            MealIngredient(ingredient_name="sweet potato", quantity=2, unit="each"),
            MealIngredient(ingredient_name="chickpeas", quantity=1, unit="can"),
            MealIngredient(ingredient_name="spinach", quantity=2, unit="cup"),
            MealIngredient(ingredient_name="olive oil", quantity=2, unit="tbsp"),
        ],
        cook_time_minutes=40,
        equipment_required=["oven"]
    ),
    Meal(
        name="Baked Pork Chops with Sweet Potato",
        ingredients=[
            MealIngredient(ingredient_name="pork chops", quantity=0.75, unit="lb"),
            MealIngredient(ingredient_name="sweet potato", quantity=2, unit="each"),
            MealIngredient(ingredient_name="green beans", quantity=1, unit="cup"),
        ],
        cook_time_minutes=35,
        equipment_required=["oven"]
    ),
    Meal(
        name="Baked Ziti",
        ingredients=[
            MealIngredient(ingredient_name="pasta", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="canned tomatoes", quantity=1, unit="can"),
            MealIngredient(ingredient_name="mozzarella", quantity=0.25, unit="lb"),
            MealIngredient(ingredient_name="ground beef", quantity=0.5, unit="lb"),
        ],
        cook_time_minutes=45,
        equipment_required=["oven"]
    ),
    Meal(
        name="Turkey Meatloaf",
        ingredients=[
            MealIngredient(ingredient_name="ground turkey", quantity=0.75, unit="lb"),
            MealIngredient(ingredient_name="bread", quantity=2, unit="each"),
            MealIngredient(ingredient_name="eggs", quantity=1, unit="each"),
            MealIngredient(ingredient_name="onion", quantity=0.5, unit="each"),
            MealIngredient(ingredient_name="tomato", quantity=1, unit="each"),
        ],
        cook_time_minutes=55,
        equipment_required=["oven"]
    ),
    Meal(
        name="Baked Salmon with Asparagus",
        ingredients=[
            MealIngredient(ingredient_name="salmon", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="asparagus", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="olive oil", quantity=2, unit="tbsp"),
            MealIngredient(ingredient_name="garlic", quantity=1, unit="tbsp"),
        ],
        cook_time_minutes=25,
        equipment_required=["oven"]
    ),
    Meal(
        name="Beef and Vegetable Casserole",
        ingredients=[
            MealIngredient(ingredient_name="ground beef", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="potatoes", quantity=3, unit="each"),
            MealIngredient(ingredient_name="carrots", quantity=2, unit="each"),
            MealIngredient(ingredient_name="corn", quantity=1, unit="cup"),
            MealIngredient(ingredient_name="chicken broth", quantity=1, unit="can"),
        ],
        cook_time_minutes=50,
        equipment_required=["oven"]
    ),
    Meal(
        name="Roasted Brussels Sprouts Chicken Bowl",
        ingredients=[
            MealIngredient(ingredient_name="chicken thighs", quantity=0.75, unit="lb"),
            MealIngredient(ingredient_name="brussels sprouts", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="sweet potato", quantity=1, unit="each"),
            MealIngredient(ingredient_name="olive oil", quantity=2, unit="tbsp"),
        ],
        cook_time_minutes=40,
        equipment_required=["oven"]
    ),
    Meal(
        name="Chicken Enchiladas",
        ingredients=[
            MealIngredient(ingredient_name="chicken breast", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="tortillas", quantity=4, unit="each"),
            MealIngredient(ingredient_name="cheese", quantity=0.25, unit="lb"),
            MealIngredient(ingredient_name="canned tomatoes", quantity=1, unit="can"),
            MealIngredient(ingredient_name="onion", quantity=0.5, unit="each"),
        ],
        cook_time_minutes=35,
        equipment_required=["oven"]
    ),
    Meal(
        name="Sheet Pan Shrimp and Vegetables",
        ingredients=[
            MealIngredient(ingredient_name="shrimp", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="zucchini", quantity=1, unit="each"),
            MealIngredient(ingredient_name="bell pepper", quantity=2, unit="each"),
            MealIngredient(ingredient_name="onion", quantity=1, unit="each"),
            MealIngredient(ingredient_name="olive oil", quantity=2, unit="tbsp"),
        ],
        cook_time_minutes=20,
        equipment_required=["oven"]
    ),
    Meal(
        name="Quinoa Stuffed Bell Peppers",
        ingredients=[
            MealIngredient(ingredient_name="bell pepper", quantity=4, unit="each"),
            MealIngredient(ingredient_name="quinoa", quantity=1, unit="cup"),
            MealIngredient(ingredient_name="black beans", quantity=0.5, unit="can"),
            MealIngredient(ingredient_name="corn", quantity=0.5, unit="cup"),
            MealIngredient(ingredient_name="tomato", quantity=1, unit="each"),
        ],
        cook_time_minutes=40,
        equipment_required=["oven"]
    ),
    Meal(
        name="Turkey Stuffed Zucchini",
        ingredients=[
            MealIngredient(ingredient_name="ground turkey", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="zucchini", quantity=2, unit="each"),
            MealIngredient(ingredient_name="rice", quantity=0.5, unit="cup"),
            MealIngredient(ingredient_name="canned tomatoes", quantity=0.5, unit="can"),
            MealIngredient(ingredient_name="cheese", quantity=0.125, unit="lb"),
        ],
        cook_time_minutes=40,
        equipment_required=["oven"]
    ),
    Meal(
        name="BBQ Chicken Thighs with Rice",
        ingredients=[
            MealIngredient(ingredient_name="chicken thighs", quantity=0.75, unit="lb"),
            MealIngredient(ingredient_name="rice", quantity=1, unit="cup"),
            MealIngredient(ingredient_name="corn", quantity=0.5, unit="cup"),
            MealIngredient(ingredient_name="onion", quantity=0.5, unit="each"),
        ],
        cook_time_minutes=40,
        equipment_required=["oven"]
    ),
    Meal(
        name="Bacon Veggie Frittata",
        ingredients=[
            MealIngredient(ingredient_name="bacon", quantity=0.25, unit="lb"),
            MealIngredient(ingredient_name="eggs", quantity=4, unit="each"),
            MealIngredient(ingredient_name="bell pepper", quantity=1, unit="each"),
            MealIngredient(ingredient_name="onion", quantity=0.5, unit="each"),
            MealIngredient(ingredient_name="spinach", quantity=1, unit="cup"),
        ],
        cook_time_minutes=25,
        equipment_required=["oven"]
    ),
    Meal(
        name="Roasted Cauliflower Bowl",
        ingredients=[
            MealIngredient(ingredient_name="cauliflower", quantity=1, unit="each"),
            MealIngredient(ingredient_name="chickpeas", quantity=1, unit="can"),
            MealIngredient(ingredient_name="spinach", quantity=2, unit="cup"),
            MealIngredient(ingredient_name="olive oil", quantity=2, unit="tbsp"),
            MealIngredient(ingredient_name="garlic", quantity=2, unit="tbsp"),
        ],
        cook_time_minutes=35,
        equipment_required=["oven"]
    ),

    # -----------------------------------------------------------------------
    # MICROWAVE QUICK MEALS (3 meals)
    # -----------------------------------------------------------------------
    Meal(
        name="Microwave Rice and Bean Bowl",
        ingredients=[
            MealIngredient(ingredient_name="rice", quantity=1, unit="cup"),
            MealIngredient(ingredient_name="black beans", quantity=0.5, unit="can"),
            MealIngredient(ingredient_name="cheese", quantity=0.1, unit="lb"),
        ],
        cook_time_minutes=15,
        equipment_required=["microwave"]
    ),
    Meal(
        name="Microwave Baked Potato",
        ingredients=[
            MealIngredient(ingredient_name="potatoes", quantity=2, unit="each"),
            MealIngredient(ingredient_name="cheese", quantity=0.125, unit="lb"),
            MealIngredient(ingredient_name="butter", quantity=1, unit="tbsp"),
        ],
        cook_time_minutes=10,
        equipment_required=["microwave"]
    ),
    Meal(
        name="Microwave Veggie Quesadilla",
        ingredients=[
            MealIngredient(ingredient_name="tortillas", quantity=2, unit="each"),
            MealIngredient(ingredient_name="cheese", quantity=0.125, unit="lb"),
            MealIngredient(ingredient_name="bell pepper", quantity=1, unit="each"),
            MealIngredient(ingredient_name="onion", quantity=0.25, unit="each"),
        ],
        cook_time_minutes=10,
        equipment_required=["microwave"]
    ),

    # -----------------------------------------------------------------------
    # MORE STOVE MEALS (17 meals)
    # -----------------------------------------------------------------------
    Meal(
        name="Sausage and Veggie Skillet",
        ingredients=[
            MealIngredient(ingredient_name="Italian sausage", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="zucchini", quantity=1, unit="each"),
            MealIngredient(ingredient_name="bell pepper", quantity=1, unit="each"),
            MealIngredient(ingredient_name="onion", quantity=1, unit="each"),
            MealIngredient(ingredient_name="potatoes", quantity=2, unit="each"),
        ],
        cook_time_minutes=30,
        equipment_required=["stove"]
    ),
    Meal(
        name="Kale Sweet Potato Hash",
        ingredients=[
            MealIngredient(ingredient_name="sweet potato", quantity=2, unit="each"),
            MealIngredient(ingredient_name="kale", quantity=2, unit="cup"),
            MealIngredient(ingredient_name="eggs", quantity=2, unit="each"),
            MealIngredient(ingredient_name="onion", quantity=0.5, unit="each"),
            MealIngredient(ingredient_name="garlic", quantity=2, unit="tbsp"),
        ],
        cook_time_minutes=25,
        equipment_required=["stove"]
    ),
    Meal(
        name="Pork Chop with Mashed Potatoes",
        ingredients=[
            MealIngredient(ingredient_name="pork chops", quantity=0.75, unit="lb"),
            MealIngredient(ingredient_name="potatoes", quantity=4, unit="each"),
            MealIngredient(ingredient_name="butter", quantity=2, unit="tbsp"),
            MealIngredient(ingredient_name="milk", quantity=0.25, unit="cup"),
        ],
        cook_time_minutes=35,
        equipment_required=["stove"]
    ),
    Meal(
        name="Greek Chicken Quinoa Bowl",
        ingredients=[
            MealIngredient(ingredient_name="chicken breast", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="quinoa", quantity=1, unit="cup"),
            MealIngredient(ingredient_name="cucumber", quantity=1, unit="each"),
            MealIngredient(ingredient_name="tomato", quantity=2, unit="each"),
            MealIngredient(ingredient_name="spinach", quantity=1, unit="cup"),
        ],
        cook_time_minutes=30,
        equipment_required=["stove"]
    ),
    Meal(
        name="Tofu Stir Fry with Noodles",
        ingredients=[
            MealIngredient(ingredient_name="tofu", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="noodles", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="broccoli", quantity=1, unit="cup"),
            MealIngredient(ingredient_name="soy sauce", quantity=3, unit="tbsp"),
            MealIngredient(ingredient_name="ginger", quantity=0.5, unit="oz"),
            MealIngredient(ingredient_name="garlic", quantity=1, unit="tbsp"),
        ],
        cook_time_minutes=25,
        equipment_required=["stove"]
    ),
    Meal(
        name="Spaghetti with Meatballs",
        ingredients=[
            MealIngredient(ingredient_name="pasta", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="ground beef", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="eggs", quantity=1, unit="each"),
            MealIngredient(ingredient_name="canned tomatoes", quantity=1, unit="can"),
            MealIngredient(ingredient_name="onion", quantity=0.5, unit="each"),
            MealIngredient(ingredient_name="garlic", quantity=2, unit="tbsp"),
        ],
        cook_time_minutes=40,
        equipment_required=["stove"]
    ),
    Meal(
        name="Shrimp Scampi with Pasta",
        ingredients=[
            MealIngredient(ingredient_name="pasta", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="shrimp", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="garlic", quantity=3, unit="tbsp"),
            MealIngredient(ingredient_name="butter", quantity=2, unit="tbsp"),
            MealIngredient(ingredient_name="olive oil", quantity=2, unit="tbsp"),
            MealIngredient(ingredient_name="spinach", quantity=1, unit="cup"),
        ],
        cook_time_minutes=25,
        equipment_required=["stove"]
    ),
    Meal(
        name="Chicken Marsala Style",
        ingredients=[
            MealIngredient(ingredient_name="chicken breast", quantity=0.75, unit="lb"),
            MealIngredient(ingredient_name="mushrooms", quantity=1.5, unit="cup"),
            MealIngredient(ingredient_name="chicken broth", quantity=1, unit="can"),
            MealIngredient(ingredient_name="garlic", quantity=2, unit="tbsp"),
            MealIngredient(ingredient_name="butter", quantity=1, unit="tbsp"),
        ],
        cook_time_minutes=30,
        equipment_required=["stove"]
    ),
    Meal(
        name="Salmon with Quinoa and Kale",
        ingredients=[
            MealIngredient(ingredient_name="salmon", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="quinoa", quantity=1, unit="cup"),
            MealIngredient(ingredient_name="kale", quantity=2, unit="cup"),
            MealIngredient(ingredient_name="garlic", quantity=2, unit="tbsp"),
            MealIngredient(ingredient_name="olive oil", quantity=2, unit="tbsp"),
        ],
        cook_time_minutes=30,
        equipment_required=["stove"]
    ),
    Meal(
        name="Vegan Lentil Vegetable Curry",
        ingredients=[
            MealIngredient(ingredient_name="lentils", quantity=1, unit="cup"),
            MealIngredient(ingredient_name="coconut milk", quantity=1, unit="can"),
            MealIngredient(ingredient_name="sweet potato", quantity=1, unit="each"),
            MealIngredient(ingredient_name="spinach", quantity=1, unit="cup"),
            MealIngredient(ingredient_name="onion", quantity=1, unit="each"),
            MealIngredient(ingredient_name="garlic", quantity=2, unit="tbsp"),
        ],
        cook_time_minutes=35,
        equipment_required=["stove"]
    ),
    Meal(
        name="Avocado Black Bean Rice Bowl",
        ingredients=[
            MealIngredient(ingredient_name="avocado", quantity=1, unit="each"),
            MealIngredient(ingredient_name="black beans", quantity=1, unit="can"),
            MealIngredient(ingredient_name="rice", quantity=1, unit="cup"),
            MealIngredient(ingredient_name="corn", quantity=0.5, unit="cup"),
            MealIngredient(ingredient_name="tomato", quantity=1, unit="each"),
        ],
        cook_time_minutes=20,
        equipment_required=["stove"]
    ),
    Meal(
        name="Miso-Style Tofu Soup",
        ingredients=[
            MealIngredient(ingredient_name="tofu", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="chicken broth", quantity=1, unit="can"),
            MealIngredient(ingredient_name="mushrooms", quantity=1, unit="cup"),
            MealIngredient(ingredient_name="kale", quantity=1, unit="cup"),
            MealIngredient(ingredient_name="ginger", quantity=0.5, unit="oz"),
        ],
        cook_time_minutes=20,
        equipment_required=["stove"]
    ),
    Meal(
        name="Kimchi-Style Fried Rice",
        ingredients=[
            MealIngredient(ingredient_name="rice", quantity=1, unit="cup"),
            MealIngredient(ingredient_name="eggs", quantity=2, unit="each"),
            MealIngredient(ingredient_name="cabbage", quantity=0.25, unit="each"),
            MealIngredient(ingredient_name="onion", quantity=0.5, unit="each"),
            MealIngredient(ingredient_name="soy sauce", quantity=3, unit="tbsp"),
            MealIngredient(ingredient_name="ginger", quantity=0.5, unit="oz"),
        ],
        cook_time_minutes=20,
        equipment_required=["stove"]
    ),
    Meal(
        name="Pasta e Fagioli",
        ingredients=[
            MealIngredient(ingredient_name="pasta", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="kidney beans", quantity=1, unit="can"),
            MealIngredient(ingredient_name="canned tomatoes", quantity=1, unit="can"),
            MealIngredient(ingredient_name="onion", quantity=1, unit="each"),
            MealIngredient(ingredient_name="chicken broth", quantity=1, unit="can"),
            MealIngredient(ingredient_name="garlic", quantity=2, unit="tbsp"),
        ],
        cook_time_minutes=30,
        equipment_required=["stove"]
    ),
    Meal(
        name="Sweet Potato Black Bean Bowl",
        ingredients=[
            MealIngredient(ingredient_name="sweet potato", quantity=2, unit="each"),
            MealIngredient(ingredient_name="black beans", quantity=1, unit="can"),
            MealIngredient(ingredient_name="corn", quantity=0.5, unit="cup"),
            MealIngredient(ingredient_name="onion", quantity=0.5, unit="each"),
            MealIngredient(ingredient_name="avocado", quantity=0.5, unit="each"),
        ],
        cook_time_minutes=25,
        equipment_required=["stove"]
    ),
    Meal(
        name="Cucumber Tomato Tuna Salad",
        ingredients=[
            MealIngredient(ingredient_name="canned tuna", quantity=1, unit="can"),
            MealIngredient(ingredient_name="cucumber", quantity=1, unit="each"),
            MealIngredient(ingredient_name="tomato", quantity=2, unit="each"),
            MealIngredient(ingredient_name="onion", quantity=0.25, unit="each"),
            MealIngredient(ingredient_name="olive oil", quantity=1, unit="tbsp"),
        ],
        cook_time_minutes=10,
        equipment_required=["stove"]
    ),
    Meal(
        name="Chicken Fajita Skillet",
        ingredients=[
            MealIngredient(ingredient_name="chicken breast", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="bell pepper", quantity=3, unit="each"),
            MealIngredient(ingredient_name="onion", quantity=1, unit="each"),
            MealIngredient(ingredient_name="tortillas", quantity=3, unit="each"),
            MealIngredient(ingredient_name="olive oil", quantity=2, unit="tbsp"),
        ],
        cook_time_minutes=25,
        equipment_required=["stove"]
    ),
    Meal(
        name="Chicken and Spinach Stuffed Potatoes",
        ingredients=[
            MealIngredient(ingredient_name="chicken breast", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="potatoes", quantity=3, unit="each"),
            MealIngredient(ingredient_name="spinach", quantity=1, unit="cup"),
            MealIngredient(ingredient_name="cheese", quantity=0.125, unit="lb"),
        ],
        cook_time_minutes=45,
        equipment_required=["oven"]
    ),
    Meal(
        name="Sausage and Potato Skillet",
        ingredients=[
            MealIngredient(ingredient_name="Italian sausage", quantity=0.5, unit="lb"),
            MealIngredient(ingredient_name="potatoes", quantity=3, unit="each"),
            MealIngredient(ingredient_name="bell pepper", quantity=1, unit="each"),
            MealIngredient(ingredient_name="onion", quantity=1, unit="each"),
            MealIngredient(ingredient_name="garlic", quantity=1, unit="tbsp"),
        ],
        cook_time_minutes=30,
        equipment_required=["stove"]
    ),
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