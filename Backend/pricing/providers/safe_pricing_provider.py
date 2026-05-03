from pricing.providers.base import PricingProvider
from typing import Optional

class SafePricingProvider(PricingProvider):
    """Wrapper provider that falls back to an estimated provider when primary fails."""

    def __init__(self, primary: PricingProvider, fallback: PricingProvider):
        self.primary = primary
        self.fallback = fallback
        self.primary_name = getattr(primary, "STORE_NAME", "primary")
        self.fallback_name = getattr(fallback, "STORE_NAME", "fallback")

    def set_location(self, zip_code: str) -> None:
        if hasattr(self.primary, "set_location"):
            self.primary.set_location(zip_code)

        if hasattr(self.fallback, "set_location"):
            try:
                self.fallback.set_location(zip_code)
            except NotImplementedError:
                pass

    def get_price(self, ingredient_name: str) -> float:
        try:
            return self.primary.get_price(ingredient_name)
        except Exception as exc:
            print(
                f"DEBUG: {self.primary_name} failed for '{ingredient_name}': {exc}. "
                f"Falling back to {self.fallback_name} pricing."
            )
            return self.fallback.get_price(ingredient_name)
