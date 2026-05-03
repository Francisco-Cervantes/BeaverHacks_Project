from math import atan2, cos, radians, sin, sqrt
from typing import Dict, Optional, Tuple

DEFAULT_AVG_SPEED_MPH = 25.0
DEFAULT_MPG = 25.0
DEFAULT_GAS_PRICE = 3.75

# Sample ZIP code centroid coordinates used for MVP distance calculation.
# Replace this with real geocoding / Google Maps later.
ZIP_COORDINATES: Dict[str, Tuple[float, float]] = {
    "97201": (45.5145, -122.6774),
    "97209": (45.5208, -122.7110),
    "97202": (45.5157, -122.6587),
    "97203": (45.5201, -122.6427),
}


def get_zip_code_coordinates(zip_code: str) -> Optional[Tuple[float, float]]:
    """Return approximate latitude/longitude for a ZIP code."""
    if not zip_code:
        return None
    normalized = str(zip_code).strip().split("-")[0]
    return ZIP_COORDINATES.get(normalized)


def haversine_distance_miles(origin: Tuple[float, float], destination: Tuple[float, float]) -> float:
    """Calculate great-circle distance between two latitude/longitude pairs."""
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 3958.8  # Earth radius in miles

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return round(radius * c, 2)


def estimate_travel_time_minutes(distance_miles: float, avg_speed_mph: float = DEFAULT_AVG_SPEED_MPH) -> float:
    """Estimate one-way travel time in minutes."""
    if distance_miles is None or avg_speed_mph <= 0:
        return 0.0
    return round((distance_miles / avg_speed_mph) * 60, 1)


def estimate_gas_cost(distance_miles: float, vehicle_mpg: float = DEFAULT_MPG, gas_price_per_gallon: float = DEFAULT_GAS_PRICE) -> float:
    """Estimate round-trip gas cost."""
    if distance_miles is None or vehicle_mpg <= 0:
        return 0.0

    round_trip = distance_miles * 2
    gallons = round_trip / vehicle_mpg
    return round(gallons * gas_price_per_gallon, 2)
