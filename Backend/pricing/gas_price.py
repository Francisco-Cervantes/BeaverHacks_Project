import requests
import json
from typing import Optional, Dict
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# EIA API Configuration
EIA_BASE_URL = "https://api.eia.gov/v2"
EIA_API_KEY = os.getenv("EIA_API_KEY", "")  # Free API key from EIA

# State mapping for ZIP codes (first 3 digits)
ZIP_TO_STATE = {
    "97": "OR",  # Oregon
    "98": "WA",  # Washington
    "99": "AK",  # Alaska
    "80": "CO",  # Colorado
    "81": "CO",
    "82": "CO",
    "83": "CO",
    "84": "CO",
    "85": "CO",
    "86": "CO",
    "87": "CO",
    "88": "CO",
    "89": "CO",
    "90": "CA",  # California
    "91": "CA",
    "92": "CA",
    "93": "CA",
    "94": "CA",
    "95": "CA",
    "96": "CA",
    # Add more as needed
}

# State to PADD region mapping for EIA gas prices
STATE_TO_PADD = {
    # PADD 1: East Coast
    "CT": "1X", "DE": "1X", "DC": "1X", "FL": "1X", "GA": "1X", "ME": "1X", "MD": "1X", "MA": "1X", "NH": "1X", "NJ": "1X", "NY": "1X", "NC": "1X", "OH": "1X", "PA": "1X", "RI": "1X", "SC": "1X", "VT": "1X", "VA": "1X", "WV": "1X",
    # PADD 2: Midwest
    "IL": "1Y", "IN": "1Y", "IA": "1Y", "KS": "1Y", "KY": "1Y", "MI": "1Y", "MN": "1Y", "MO": "1Y", "NE": "1Y", "ND": "1Y", "SD": "1Y", "WI": "1Y",
    # PADD 3: Gulf Coast
    "AL": "1Z", "AR": "1Z", "LA": "1Z", "MS": "1Z", "NM": "1Z", "OK": "1Z", "TX": "1Z",
    # PADD 4: Rocky Mountain
    "CO": "49", "ID": "49", "MT": "49", "UT": "49", "WY": "49",
    # PADD 5: West Coast
    "AK": "CA", "AZ": "CA", "CA": "CA", "HI": "CA", "NV": "CA", "OR": "CA", "WA": "CA",
}

# Fallback gas prices by state (in $/gal)
FALLBACK_GAS_PRICES = {
    "OR": 3.92,
    "WA": 4.05,
    "CA": 4.25,
    "CO": 3.75,
    "TX": 3.50,
    "FL": 3.60,
    "NY": 3.85,
    "national": 3.78,
}

def get_state_from_zip(zip_code: str) -> Optional[str]:
    """Extract state from ZIP code."""
    if not zip_code or len(zip_code) < 3:
        return None
    prefix = zip_code[:2] if zip_code.startswith("0") else zip_code[:3]
    return ZIP_TO_STATE.get(prefix[:2])  # Use first 2 digits for simplicity

def get_gas_price_for_zip(zip_code: str) -> float:
    """Get current gas price for a ZIP code using EIA data."""
    state = get_state_from_zip(zip_code)
    if not state:
        return FALLBACK_GAS_PRICES.get("national", 3.75)

    padd = STATE_TO_PADD.get(state)
    if not padd:
        return FALLBACK_GAS_PRICES.get("national", 3.75)

    # Try to fetch from EIA
    price = fetch_eia_gas_price(padd)
    if price is not None:
        return price

    # Fallback to hardcoded
    return FALLBACK_GAS_PRICES.get(state, FALLBACK_GAS_PRICES["national"])

def fetch_eia_gas_price(padd_code: str) -> Optional[float]:
    """Fetch gas price from EIA API for a PADD region."""
    if not EIA_API_KEY:
        return None

    # EIA series ID for regular gasoline prices by PADD region
    # Format: PET.EMM_EPM0_PTE_S{padd_code}_DPG.W (weekly data)
    series_id = f"PET.EMM_EPM0_PTE_S{padd_code}_DPG.W"

    url = f"{EIA_BASE_URL}/seriesid/{series_id}"
    params = {
        "api_key": EIA_API_KEY,
        "num": 1,  # Get latest data point
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        if "response" in data and "data" in data["response"]:
            latest_data = data["response"]["data"][0]
            price_str = latest_data.get("value")
            if price_str and price_str != ".":
                return float(price_str)

    except (requests.RequestException, ValueError, KeyError, IndexError):
        pass

    return None
