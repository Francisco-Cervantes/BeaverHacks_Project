pricing/providers/ Directory

Store-specific pricing provider implementations.

Files:
- base.py: Abstract PricingProvider interface
- mock_provider.py: Mock prices for testing
- kroger_provider.py: Kroger API integration (requires credentials)
- albertsons_provider.py: Placeholder for Albertsons API integration
- walmart_provider.py: Walmart estimated pricing wrapper
- costco_provider.py: Costco estimated pricing wrapper
- winco_provider.py: WinCo estimated pricing wrapper
- safeway_provider.py: Safeway estimated pricing wrapper
- grocery_outlet_provider.py: Grocery Outlet estimated pricing wrapper
- safe_pricing_provider.py: Fallback wrapper for live + estimated pricing
- registry.py: Store provider factory and supported store registry

Usage:
- All providers implement the same PricingProvider interface
- Switch providers by changing the class instantiation
- Kroger requires environment variables: KROGER_CLIENT_ID, KROGER_CLIENT_SECRET