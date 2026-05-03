from typing import Optional
from pricing.providers.base import PricingProvider

class GroceryOutletPricingProvider(PricingProvider):
    """Grocery Outlet pricing using estimated pricing models."""

    STORE_NAME = "Grocery Outlet"

    def __init__(self, base_provider: Optional[PricingProvider] = None):
        self.base_provider = base_provider
        self.multiplier = 0.85
        self.store_coords: Optional[tuple] = None
        self.default_distance_miles = 11.0
        self.estimated_prices = {
            "chicken breast": 2.49,
            "rice": 0.89,
            "pasta": 1.29,
            "eggs": 2.29,
            "onion": 0.79,
            "canned tomatoes": 1.19,
        }

    def set_location(self, zip_code: str) -> None:
        self.store_coords = None

    def get_price(self, ingredient_name: str) -> float:
        if self.base_provider is not None:
            return round(self.base_provider.get_price(ingredient_name) * self.multiplier, 2)

        if ingredient_name not in self.estimated_prices:
            raise ValueError(f"No estimated price for {ingredient_name} at Grocery Outlet")

        return self.estimated_prices[ingredient_name]
