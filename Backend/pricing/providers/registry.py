from typing import List, Optional
from pricing.providers.base import PricingProvider
from pricing.providers.albertsons_provider import AlbertsonsPricingProvider
from pricing.providers.costco_provider import CostcoPricingProvider
from pricing.providers.grocery_outlet_provider import GroceryOutletPricingProvider
from pricing.providers.kroger_provider import KrogerPricingProvider
from pricing.providers.safe_pricing_provider import SafePricingProvider
from pricing.providers.safeway_provider import SafewayPricingProvider
from pricing.providers.walmart_provider import WalmartPricingProvider
from pricing.providers.winco_provider import WincoPricingProvider


SUPPORTED_STORE_NAMES = [
    "Kroger",
    "WinCo",
    "Costco",
    "Grocery Outlet",
    "Safeway",
    "Walmart",
    "Albertsons",
]


def get_supported_store_names() -> List[str]:
    return SUPPORTED_STORE_NAMES.copy()


def build_store_provider(store_name: str, base_provider: Optional[PricingProvider] = None) -> PricingProvider:
    if store_name == "Kroger":
        return build_safe_pricing_provider()

    base = base_provider if base_provider is not None else build_safe_pricing_provider()

    if store_name == "WinCo":
        return WincoPricingProvider(base)
    if store_name == "Costco":
        return CostcoPricingProvider(base)
    if store_name == "Grocery Outlet":
        return GroceryOutletPricingProvider(base)
    if store_name == "Safeway":
        return SafewayPricingProvider(base)
    if store_name == "Walmart":
        return WalmartPricingProvider(base)
    if store_name == "Albertsons":
        return AlbertsonsPricingProvider(base)

    raise ValueError(f"Unsupported store provider: {store_name}")


def build_safe_pricing_provider(
    primary: Optional[PricingProvider] = None,
    fallback: Optional[PricingProvider] = None,
) -> SafePricingProvider:
    """Build a safe wrapper around Kroger with estimated fallback pricing."""
    primary_provider = primary or KrogerPricingProvider()
    fallback_provider = fallback or CostcoPricingProvider()
    return SafePricingProvider(primary_provider, fallback_provider)
