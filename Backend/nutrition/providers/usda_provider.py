import os
from pathlib import Path
from typing import Dict, Optional

import requests
from dotenv import load_dotenv

from ..provider import NutritionProvider

env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

USDA_API_KEY = os.getenv("USDA_API_KEY", "")
USDA_SEARCH_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"
USDA_FOOD_URL = "https://api.nal.usda.gov/fdc/v1/food"

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


def normalize_ingredient(name: str) -> str:
    return name.strip().lower()


def _extract_nutrition(food_data: dict) -> Optional[Dict[str, float]]:
    nutrients = {
        "calories": 0.0,
        "protein": 0.0,
        "carbs": 0.0,
        "fat": 0.0,
    }

    for nutrient in food_data.get("foodNutrients", []):
        name = nutrient.get("nutrientName", "").lower()
        value = nutrient.get("value")
        if value is None:
            continue

        if "energy" in name and "kcal" in nutrient.get("unitName", "").lower():
            nutrients["calories"] = float(value)
        elif "protein" == name:
            nutrients["protein"] = float(value)
        elif "carbohydrate" in name and "total" in name:
            nutrients["carbs"] = float(value)
        elif name == "carbohydrate, by difference":
            nutrients["carbs"] = float(value)
        elif "total lipid" in name or "fat" == name:
            nutrients["fat"] = float(value)

    if any(value > 0 for value in nutrients.values()):
        return nutrients
    return None


def _get_food_item(ingredient_name: str) -> Optional[dict]:
    if not USDA_API_KEY:
        return None

    # First try searching for raw version
    queries = [f"{ingredient_name} raw", ingredient_name]
    
    for query in queries:
        params = {"api_key": USDA_API_KEY}
        body = {
            "query": query,
            "pageSize": 5,  # Get more results to find one with complete nutrition
            "dataType": ["Foundation", "SR Legacy", "Survey (FNDDS)"],
        }

        try:
            response = requests.post(USDA_SEARCH_URL, params=params, json=body, timeout=10)
            response.raise_for_status()
            data = response.json()
            foods = data.get("foods", [])
            
            if not foods:
                continue
                
            # Find the best food item (one with most complete nutrition)
            best_food = None
            best_score = 0
            
            for food in foods:
                score = 0
                nutrients = food.get("foodNutrients", [])
                
                # Score based on having our target nutrients
                nutrient_names = [n.get("nutrientName", "").lower() for n in nutrients]
                
                if any("energy" in name for name in nutrient_names):
                    score += 1
                if any("protein" in name for name in nutrient_names):
                    score += 1
                if any("carbohydrate" in name for name in nutrient_names):
                    score += 1
                if any("lipid" in name or "fat" in name for name in nutrient_names):
                    score += 1
                    
                # Prefer Foundation data type
                if food.get("dataType") == "Foundation":
                    score += 2
                    
                if score > best_score:
                    best_score = score
                    best_food = food
            
            if best_food and best_score >= 3:  # Must have at least 3 nutrients
                return best_food
                
        except Exception:
            continue
    
    return None


class USDANutritionProvider(NutritionProvider):
    def get_nutrition(self, ingredient_name: str, quantity: float, unit: str) -> Dict[str, float]:
        if not USDA_API_KEY:
            raise RuntimeError("USDA_API_KEY is not configured")

        food = _get_food_item(ingredient_name)
        if not food:
            raise ValueError(f"No USDA nutrition result for '{ingredient_name}'")

        nutrition = _extract_nutrition(food)
        if nutrition is None:
            raise ValueError(f"USDA nutrition could not be parsed for '{ingredient_name}'")

        grams = self._convert_quantity_to_grams(quantity, unit)
        factor = grams / 100.0
        return {
            "calories": round(nutrition["calories"] * factor, 2),
            "protein": round(nutrition["protein"] * factor, 2),
            "carbs": round(nutrition["carbs"] * factor, 2),
            "fat": round(nutrition["fat"] * factor, 2),
        }

    def _convert_quantity_to_grams(self, quantity: float, unit: str) -> float:
        lookup_unit = unit.strip().lower()
        if lookup_unit in UNIT_TO_GRAMS:
            return quantity * UNIT_TO_GRAMS[lookup_unit]
        raise ValueError(f"Unsupported nutrition unit '{unit}'")
