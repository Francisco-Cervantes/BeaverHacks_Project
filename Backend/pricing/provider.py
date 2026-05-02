from typing import Dict

class PricingProvider:
    def get_price(self, ingredient_name: str) -> float:
        raise NotImplementedError
