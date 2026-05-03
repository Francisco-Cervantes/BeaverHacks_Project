from typing import Optional
from pricing.providers.base import PricingProvider

class WalmartPricingProvider(PricingProvider):
    """Walmart pricing using an estimated multiplier based on Kroger pricing."""

    STORE_NAME = "Walmart"

    def __init__(self, base_provider: Optional[PricingProvider] = None):
        self.base_provider = base_provider
        self.multiplier = 0.98
        self.estimated_prices = {
            "chicken breast": 3.79,
            "rice": 1.19,
            "pasta": 1.89,
            "eggs": 2.79,
            "onion": 0.95,
            "canned tomatoes": 1.39,
        }

    def get_price(self, ingredient_name: str) -> float:
        if self.base_provider is not None:
            return round(self.base_provider.get_price(ingredient_name) * self.multiplier, 2)

        if ingredient_name not in self.estimated_prices:
            raise ValueError(f"No estimated price for {ingredient_name} at Walmart")
        return self.estimated_prices[ingredient_name]