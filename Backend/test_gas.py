from pricing.gas_price import get_gas_price_for_zip

print("Testing gas price API...")
try:
    price = get_gas_price_for_zip('97331')
    print(f"Gas price for 97331: ${price}")
    print("API is working correctly!")
except Exception as e:
    print(f"Error: {e}")
    print("API has issues.")