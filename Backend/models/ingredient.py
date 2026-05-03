from pydantic import BaseModel

class Ingredient(BaseModel):
    name: str
    unit: str               # e.g. "lb", "oz", "each"
    price_per_unit: float   # price per unit
    store: str              # e.g. "Safeway"
