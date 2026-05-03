import json
from typing import Dict
from ..provider import NutritionProvider

# Rough nutrition values per 100g for core ingredients.
NUTRITION_PER_100G: Dict[str, Dict[str, float]] = {
    "pasta": {"calories": 131, "protein": 5.0, "carbs": 25.0, "fat": 1.1},
    "canned tomatoes": {"calories": 18, "protein": 0.9, "carbs": 3.9, "fat": 0.2},
    "onion": {"calories": 40, "protein": 1.1, "carbs": 9.3, "fat": 0.1},
    "rice": {"calories": 130, "protein": 2.7, "carbs": 28.0, "fat": 0.3},
    "chicken breast": {"calories": 165, "protein": 31.0, "carbs": 0.0, "fat": 3.6},
    "eggs": {"calories": 155, "protein": 13.0, "carbs": 1.1, "fat": 11.0},
    "milk": {"calories": 60, "protein": 3.2, "carbs": 5.0, "fat": 3.3},
    "banana": {"calories": 89, "protein": 1.1, "carbs": 23.0, "fat": 0.3},
    "apple": {"calories": 52, "protein": 0.3, "carbs": 14.0, "fat": 0.2},
    "bread": {"calories": 265, "protein": 9.0, "carbs": 49.0, "fat": 3.2},
    "olive oil": {"calories": 884, "protein": 0.0, "carbs": 0.0, "fat": 100.0},
    "butter": {"calories": 717, "protein": 0.9, "carbs": 0.1, "fat": 81.0},
    "cheese": {"calories": 402, "protein": 25.0, "carbs": 1.3, "fat": 33.0},
    "tomato": {"calories": 18, "protein": 0.9, "carbs": 3.9, "fat": 0.2},
    "spinach": {"calories": 23, "protein": 2.9, "carbs": 3.6, "fat": 0.4},
}

UNIT_TO_GRAMS: Dict[str, float] = {
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

INGREDIENT_UNIT_OVERRIDES: Dict[str, Dict[str, float]] = {
    "rice": {"cup": 158.0},
    "pasta": {"cup": 140.0},
    "eggs": {"each": 50.0},
    "onion": {"each": 110.0},
    "chicken breast": {"lb": 453.592},
    "canned tomatoes": {"can": 240.0},
}


def normalize_ingredient(name: str) -> str:
    return name.strip().lower()


class MockNutritionProvider(NutritionProvider):
    def get_nutrition(self, ingredient_name: str, quantity: float, unit: str) -> Dict[str, float]:
        normalized = normalize_ingredient(ingredient_name)
        if normalized not in NUTRITION_PER_100G:
            raise ValueError(f"No nutrition data available for '{ingredient_name}'")

        grams = self._convert_quantity_to_grams(normalized, quantity, unit)
        factor = grams / 100.0
        base = NUTRITION_PER_100G[normalized]
        return {
            "calories": round(base["calories"] * factor, 2),
            "protein": round(base["protein"] * factor, 2),
            "carbs": round(base["carbs"] * factor, 2),
            "fat": round(base["fat"] * factor, 2),
        }

    def _convert_quantity_to_grams(self, ingredient_name: str, quantity: float, unit: str) -> float:
        lookup_unit = unit.strip().lower()
        override = INGREDIENT_UNIT_OVERRIDES.get(ingredient_name, {})
        if lookup_unit in override:
            return quantity * override[lookup_unit]

        if lookup_unit in UNIT_TO_GRAMS:
            return quantity * UNIT_TO_GRAMS[lookup_unit]

        raise ValueError(f"Unsupported nutrition unit '{unit}' for '{ingredient_name}'")
