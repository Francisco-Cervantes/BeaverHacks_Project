def build_shopping_list(meals):
    shopping = {}
    for meal in meals:
        for item in meal.ingredients:
            shopping[item.ingredient_name] = shopping.get(item.ingredient_name, 0) + item.quantity
    return shopping
