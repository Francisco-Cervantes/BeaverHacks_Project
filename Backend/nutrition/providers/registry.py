import os
from pathlib import Path
from dotenv import load_dotenv

from .mock_provider import MockNutritionProvider
from .usda_provider import USDANutritionProvider
from nutrition.provider import NutritionProvider

env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

USDA_API_KEY = os.getenv("USDA_API_KEY", "")


def build_nutrition_provider() -> NutritionProvider:
    if USDA_API_KEY:
        return USDANutritionProvider()
    return MockNutritionProvider()
