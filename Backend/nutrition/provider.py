from typing import Dict


class NutritionProvider:
    def set_location(self, zip_code: str) -> None:
        """Set location context for nutrition provider if needed."""
        pass

    def get_nutrition(self, ingredient_name: str, quantity: float, unit: str) -> Dict[str, float]:
        """Get nutrition facts for an ingredient quantity."""
        raise NotImplementedError
