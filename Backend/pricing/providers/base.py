from typing import Dict

class PricingProvider:
    def set_location(self, zip_code: str) -> None:
        """Set the location for pricing lookups."""
        raise NotImplementedError

    def get_price(self, ingredient_name: str) -> float:
        """Get the price for an ingredient."""
        raise NotImplementedError
