from typing import Optional
from pricing.providers.base import PricingProvider

class SafewayPricingProvider(PricingProvider):
    """Safeway pricing using estimated prices (no public API available)."""

    STORE_NAME = "Safeway"

    def __init__(self, base_provider: Optional[PricingProvider] = None):
        self.base_provider = base_provider
        self.multiplier = 1.10
        self.estimated_prices = {
            "chicken breast": 4.49,  # per lb
            "rice": 1.29,            # per lb
            "pasta": 1.99,           # per lb
            "eggs": 3.49,            # per dozen
            "onion": 0.99,           # per lb
            "canned tomatoes": 1.49  # per can
        }

    def get_price(self, ingredient_name: str) -> float:
        """Get estimated Safeway price."""
        if self.base_provider is not None:
            return round(self.base_provider.get_price(ingredient_name) * self.multiplier, 2)

        if ingredient_name not in self.estimated_prices:
            raise ValueError(f"No estimated price for {ingredient_name} at Safeway")
        return self.estimated_prices[ingredient_name]