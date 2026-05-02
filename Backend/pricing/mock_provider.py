from pricing.provider import PricingProvider

class MockPricingProvider(PricingProvider):
    def __init__(self):
        self.prices = {
            "onion": 1.29,
            "pasta": 1.99,
            "rice": 1.09,
            "eggs": 2.99,
            "chicken breast": 3.99,
            "canned tomatoes": 1.49
        }

    def get_price(self, ingredient_name: str) -> float:
        if ingredient_name not in self.prices:
            raise ValueError(f"No price found for {ingredient_name}")
        return self.prices[ingredient_name]
