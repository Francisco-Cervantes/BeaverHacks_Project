from pricing.providers.mock_provider import MockPricingProvider
from services import get_all_meals, get_meal_costs, get_shopping_list, get_total_cost, get_available_meals
from models.pricing import calculate_meal_cost, calculate_weekly_cost, calculate_shopping_cost
from filters import filter_by_equipment, filter_by_time, filter_by_distance, mark_meals_with_cost

# Initialize pricing provider
pricing_provider = MockPricingProvider()

# Get all meals
meals = get_all_meals()
print("All meals:", [meal.name for meal in meals])

# Test calculate_meal_cost
for meal in meals:
    cost = calculate_meal_cost(meal, pricing_provider)
    print(f"{meal.name}: ${cost}")

# Test calculate_weekly_cost
weekly_cost = calculate_weekly_cost(meals, pricing_provider)
print(f"Weekly cost for all meals: ${weekly_cost}")

# Test shopping list
shopping_list = get_shopping_list(meals)
print("Shopping list:", shopping_list)

# Test calculate_shopping_cost
shopping_cost = calculate_shopping_cost(shopping_list, pricing_provider)
print(f"Total shopping cost: ${shopping_cost}")

# Test filtering
constraints = {'available_equipment': ['stove'], 'max_time_minutes': 25, 'max_distance_miles': 10.0}
available_meals = get_available_meals(constraints)
print("Available meals under constraints:", [meal.name for meal in available_meals])

# Test get_meal_costs
costs = get_meal_costs(available_meals, pricing_provider)
print("Costs:", costs)

# Test get_total_cost
total_cost = get_total_cost(available_meals, pricing_provider)
print(f"Total cost for available meals: ${total_cost}")

# Test mark_meals_with_cost
marked = mark_meals_with_cost(meals, pricing_provider)
for item in marked:
    print(f"{item['meal'].name}: ${item['estimated_cost']}")