from typing import Optional
from pricing.providers.base import PricingProvider

class AlbertsonsPricingProvider(PricingProvider):
    """Albertsons pricing using estimated multipliers off Kroger anchor pricing."""

    STORE_NAME = "Albertsons"

    def __init__(self, base_provider: Optional[PricingProvider] = None):
        self.base_provider = base_provider
        self.multiplier = 1.11
        self.location_id: Optional[str] = None
        self.estimated_prices = {
            "chicken breast": 4.29,
            "rice": 1.29,
            "pasta": 2.19,
            "eggs": 3.29,
            "onion": 0.99,
            "canned tomatoes": 1.69,
        }

    def set_location(self, zip_code: str) -> None:
        """Set location for Albertsons pricing estimates."""
        self.location_id = zip_code

    def get_price(self, ingredient_name: str) -> float:
        """Get an estimated Albertsons price for an ingredient."""
        if self.base_provider is not None:
            return round(self.base_provider.get_price(ingredient_name) * self.multiplier, 2)

        normalized_name = ingredient_name.strip().lower()
        if normalized_name not in self.estimated_prices:
            raise ValueError(f"No estimated price for {ingredient_name} at Albertsons")
        return self.estimated_prices[normalized_name]