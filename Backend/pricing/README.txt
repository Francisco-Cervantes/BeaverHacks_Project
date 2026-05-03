pricing/ Directory

This directory handles pricing logic and providers.

Subdirectories:
- providers/: Store-specific pricing implementations

Files in providers/:
- base.py: Abstract PricingProvider class with get_price method.
- mock_provider.py: Mock implementation with hardcoded prices for testing.
- kroger_provider.py: Kroger API integration (requires API credentials).
- walmart_provider.py: Placeholder for Walmart API.
- costco_provider.py: Estimated pricing for Costco.
- winco_provider.py: Estimated pricing for WinCo.
- safeway_provider.py: Estimated pricing for Safeway.

Purpose:
- Abstraction for different pricing sources (API, mock, estimated)
- Easy to swap providers for real pricing data
- Supports per-ingredient pricing with error handling for missing prices