from typing import Dict, Optional
from pricing.providers.base import PricingProvider

class MockPricingProvider(PricingProvider):
    """Simple mock pricing provider used for local API development and tests."""

    STORE_NAME = "Mock"

    def __init__(self):
        self.location_id: Optional[str] = None
        self.store_coords: Optional[tuple] = None
        self.default_distance_miles = 5.0
        self.mock_prices: Dict[str, float] = {
            "chicken breast": 3.49,
            "rice": 1.09,
            "pasta": 1.79,
            "eggs": 2.99,
            "onion": 0.89,
            "canned tomatoes": 1.39,
        }

    def set_location(self, zip_code: str) -> None:
        self.location_id = zip_code
        self.store_coords = None

    def get_price(self, ingredient_name: str) -> float:
        normalized = ingredient_name.strip().lower()
        if normalized not in self.mock_prices:
            raise ValueError(f"No mock price available for {ingredient_name}")
        return self.mock_prices[normalized]
