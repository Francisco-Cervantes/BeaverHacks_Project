from pricing.providers.base import PricingProvider
from typing import Optional
import logging

_log = logging.getLogger(__name__)

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
            _log.debug(
                "%s failed for '%s': %s. Falling back to %s pricing.",
                self.primary_name, ingredient_name, exc, self.fallback_name
            )
            return self.fallback.get_price(ingredient_name)
