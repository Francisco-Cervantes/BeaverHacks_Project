from typing import Optional

from pricing.distance import (
    DEFAULT_AVG_SPEED_MPH,
    DEFAULT_GAS_PRICE,
    DEFAULT_MPG,
    estimate_gas_cost,
    estimate_travel_time_minutes,
    get_zip_code_coordinates,
    haversine_distance_miles,
)
from pricing.gas_price import get_gas_price_for_zip


def get_store_distance_miles(provider: object, zip_code: str) -> Optional[float]:
    user_coords = get_zip_code_coordinates(zip_code)
    if user_coords is None:
        return None

    store_coords = getattr(provider, "store_coords", None)
    if store_coords is not None:
        return haversine_distance_miles(user_coords, store_coords)

    return getattr(provider, "default_distance_miles", None)


def build_store_comparison(
    store_name: str,
    provider: object,
    shopping_list: dict,
    zip_code: str,
    max_distance_miles: Optional[float] = None,
    gas_price: Optional[float] = None,
    vehicle_mpg: float = DEFAULT_MPG,
    avg_speed_mph: float = DEFAULT_AVG_SPEED_MPH,
) -> Optional[dict]:
    grocery_cost = 0.0
    for ingredient, quantity in shopping_list.items():
        price_per_unit = provider.get_price(ingredient)
        grocery_cost += price_per_unit * quantity

    distance_miles = get_store_distance_miles(provider, zip_code)

    if max_distance_miles is not None:
        if distance_miles is None or distance_miles > max_distance_miles:
            return None

    # Use EIA gas price if not overridden
    if gas_price is None:
        gas_price = get_gas_price_for_zip(zip_code)

    travel_time_minutes = (
        estimate_travel_time_minutes(distance_miles, avg_speed_mph)
        if distance_miles is not None
        else None
    )
    travel_cost = (
        estimate_gas_cost(distance_miles, vehicle_mpg, gas_price)
        if distance_miles is not None
        else None
    )
    effective_cost = round(grocery_cost + (travel_cost or 0.0), 2)
    confidence = "live" if store_name.lower() == "kroger" else "estimated"

    return {
        "store_name": store_name,
        "grocery_cost": round(grocery_cost, 2),
        "distance_miles": distance_miles,
        "travel_time_minutes": travel_time_minutes,
        "travel_cost": travel_cost,
        "effective_cost": effective_cost,
        "confidence": confidence,
    }
