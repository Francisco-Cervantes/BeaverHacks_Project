models/ Directory

This directory contains the data models for the meal planning application.

Files:
- ingredient.py: Defines the Ingredient model using Pydantic BaseModel. Includes name, unit, price_per_unit, and store.
- meal.py: Defines Meal and MealIngredient models. Meal includes name, ingredients list, cook_time_minutes, and equipment_required.
- pricing.py: Contains cost calculation functions - calculate_meal_cost, calculate_weekly_cost, calculate_shopping_cost.
- shopping_list.py: Function to build aggregated shopping list from multiple meals.

Purpose:
- Data validation and structure using Pydantic
- Cost calculations based on pricing providers
- Ingredient aggregation across meals