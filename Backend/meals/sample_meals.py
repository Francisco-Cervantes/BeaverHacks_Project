from models.meal import Meal, MealIngredient

# Sample meals for testing
pasta_meal = Meal(
    name="Pasta with Tomato Sauce",
    ingredients=[
        MealIngredient(ingredient_name="pasta", quantity=0.5, unit="lb"),
        MealIngredient(ingredient_name="canned tomatoes", quantity=1, unit="can"),
        MealIngredient(ingredient_name="onion", quantity=0.5, unit="each")
    ],
    cook_time_minutes=20,
    equipment_required=["stove"]
)

rice_meal = Meal(
    name="Chicken Rice Bowl",
    ingredients=[
        MealIngredient(ingredient_name="rice", quantity=1, unit="cup"),
        MealIngredient(ingredient_name="chicken breast", quantity=0.5, unit="lb"),
        MealIngredient(ingredient_name="onion", quantity=0.25, unit="each")
    ],
    cook_time_minutes=30,
    equipment_required=["stove"]
)

egg_meal = Meal(
    name="Scrambled Eggs",
    ingredients=[
        MealIngredient(ingredient_name="eggs", quantity=2, unit="each")
    ],
    cook_time_minutes=10,
    equipment_required=["stove"]
)

sample_meals = [pasta_meal, rice_meal, egg_meal]