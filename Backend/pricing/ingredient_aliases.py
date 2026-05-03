from typing import Dict

INGREDIENT_ALIASES: Dict[str, str] = {
    "onion": "yellow onion",
    "chicken breast": "boneless skinless chicken breast",
    "pasta": "spaghetti",
    "canned tomatoes": "diced tomatoes",
    "eggs": "large eggs",
    "rice": "white rice",
    "tomato": "diced tomatoes",
    "chicken": "chicken breast",
}


def normalize_ingredient_name(ingredient_name: str) -> str:
    """Normalize ingredient names before searching provider APIs."""
    normalized = ingredient_name.strip().lower()
    return INGREDIENT_ALIASES.get(normalized, normalized)
