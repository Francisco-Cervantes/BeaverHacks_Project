from typing import Optional
from pricing.providers.base import PricingProvider

class WincoPricingProvider(PricingProvider):
    """WinCo pricing using estimated multipliers off Kroger anchor pricing."""

    STORE_NAME = "WinCo"

    def __init__(self, base_provider: Optional[PricingProvider] = None):
        self.base_provider = base_provider
        self.multiplier = 0.88
        self.store_coords: Optional[tuple] = None
        self.default_distance_miles = 10.0
        self.estimated_prices = {
            "chicken breast": 2.99,  # per lb
            "rice": 0.99,            # per lb
            "pasta": 1.49,           # per lb
            "eggs": 2.49,            # per dozen
            "onion": 0.69,           # per lb
            "canned tomatoes": 1.29  # per can
        }

    def get_price(self, ingredient_name: str) -> float:
        """Get estimated WinCo price."""
        if self.base_provider is not None:
            return round(self.base_provider.get_price(ingredient_name) * self.multiplier, 2)

        if ingredient_name not in self.estimated_prices:
            raise ValueError(f"No estimated price for {ingredient_name} at WinCo")
        return self.estimated_prices[ingredient_name]

    def set_location(self, zip_code: str) -> None:
        self.store_coords = None