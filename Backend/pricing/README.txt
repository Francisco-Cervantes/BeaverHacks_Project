pricing/ Directory

This directory handles pricing logic and providers.

Files:
- provider.py: Abstract PricingProvider class with get_price method.
- mock_provider.py: Mock implementation with hardcoded prices for testing.

Purpose:
- Abstraction for different pricing sources (mock, API, database)
- Easy to swap providers for real pricing data
- Supports per-ingredient pricing with error handling for missing prices