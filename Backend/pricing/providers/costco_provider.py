from typing import Optional
from pricing.providers.base import PricingProvider

class CostcoPricingProvider(PricingProvider):
    """Costco pricing using estimated prices or Kroger-based multipliers."""

    STORE_NAME = "Costco"

    def __init__(self, base_provider: Optional[PricingProvider] = None):
        self.base_provider = base_provider
        self.multiplier = 0.95
        self.estimated_prices = {
            "chicken breast": 4.99,  # per lb
            "rice": 1.49,            # per lb
            "pasta": 2.99,           # per lb
            "eggs": 3.99,            # per dozen
            "onion": 0.89,           # per lb
            "canned tomatoes": 2.49  # per can
        }

    def get_price(self, ingredient_name: str) -> float:
        """Get estimated Costco price."""
        if self.base_provider is not None:
            return round(self.base_provider.get_price(ingredient_name) * self.multiplier, 2)

        if ingredient_name not in self.estimated_prices:
            raise ValueError(f"No estimated price for {ingredient_name} at Costco")
        return self.estimated_prices[ingredient_name]