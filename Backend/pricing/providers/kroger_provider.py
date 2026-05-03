from requests.auth import HTTPBasicAuth
import requests
import os
import logging
from typing import Optional, Dict, Any
from pathlib import Path
from dotenv import load_dotenv
from pricing.ingredient_aliases import normalize_ingredient_name
from pricing.providers.base import PricingProvider

_log = logging.getLogger(__name__)

# Load environment variables from .env file (explicit path)
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

class KrogerPricingProvider(PricingProvider):
    """
    Kroger API integration for real-time pricing.

    Requires:
    - KROGER_CLIENT_ID: Your Kroger app client ID
    - KROGER_CLIENT_SECRET: Your Kroger app client secret

    Get these from: https://developer.kroger.com/manage/apps/register
    """

    BASE_URL = "https://api-ce.kroger.com"
    KNOWN_CERTIFICATION_LOCATION = "01400943"

    def __init__(self, client_id: Optional[str] = None, client_secret: Optional[str] = None):
        self.client_id = (client_id or os.getenv("KROGER_CLIENT_ID") or "").strip()
        self.client_secret = (client_secret or os.getenv("KROGER_CLIENT_SECRET") or "").strip()
        self.access_token: Optional[str] = None
        self.location_id: Optional[str] = None
        self.store_coords: Optional[tuple] = None

        if not self.client_id or not self.client_secret:
            raise ValueError("KROGER_CLIENT_ID and KROGER_CLIENT_SECRET environment variables required")

    def _get_access_token(self) -> str:
        """Get OAuth access token using client credentials flow."""
        if self.access_token is not None:
            return self.access_token

        url = f"{self.BASE_URL}/v1/connect/oauth2/token"
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "User-Agent": "NomNomNOMatron/1.0"
        }

        data = {
            "grant_type": "client_credentials",
            "scope": "product.compact"
        }

        auth = HTTPBasicAuth(self.client_id, self.client_secret)

        try:
            response = requests.post(
                url,
                headers=headers,
                data=data,
                auth=auth,
                timeout=10
            )
            
            _log.debug("Kroger token status: %s", response.status_code)
            
            response.raise_for_status()

            token_data = response.json()
            access_token = str(token_data["access_token"])
            self.access_token = access_token
            return access_token
        except requests.exceptions.HTTPError as e:
            error_msg = f"OAuth Error: {e.response.status_code} - {e.response.text}"
            raise ValueError(f"Failed to authenticate with Kroger API. {error_msg}\n"
                           f"Check your KROGER_CLIENT_ID and KROGER_CLIENT_SECRET in .env file")

    def set_location(self, zip_code: str) -> None:
        """Find and set the nearest Kroger location for pricing."""
        if not zip_code:
            raise ValueError("zip_code is required")

        locations = self._get_nearby_locations(zip_code)
        if locations:
            location = locations[0]
            self.location_id = location["locationId"]
            self.store_coords = self._extract_location_coords(location)
            return

        self.location_id = self.KNOWN_CERTIFICATION_LOCATION
        self.store_coords = None
        _log.info("No nearby Kroger location found for %s. Using certification fallback: %s", zip_code, self.location_id)

    def _get_nearby_locations(self, zip_code: str) -> list:
        """Get nearby Kroger locations."""
        token = self._get_access_token()
        url = f"{self.BASE_URL}/v1/locations"
        headers = {"Authorization": f"Bearer {token}"}
        params = {
            "filter.zipCode.near": zip_code,
            "filter.limit": 3
        }

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        data = response.json()
        return data.get("data", [])

    def _extract_location_coords(self, location: dict) -> Optional[tuple]:
        geo = location.get("geoCode") or location.get("address", {})
        latitude = geo.get("latitude") or geo.get("lat")
        longitude = geo.get("longitude") or geo.get("lon") or geo.get("lng")
        if latitude is None or longitude is None:
            return None

        try:
            return float(latitude), float(longitude)
        except (TypeError, ValueError):
            return None

    def get_price(self, ingredient_name: str) -> float:
        """Get price for an ingredient from Kroger API."""
        if not self.location_id:
            raise ValueError("Location not set. Call set_location(zip_code) first.")

        token = self._get_access_token()
        url = f"{self.BASE_URL}/v1/products"
        headers = {"Authorization": f"Bearer {token}"}
        search_term = normalize_ingredient_name(ingredient_name)
        params = {
            "filter.term": search_term,
            "filter.locationId": self.location_id,
            "filter.limit": 1
        }

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        data = response.json()
        return self._extract_price(data)

    def _extract_price(self, data: Dict[str, Any]) -> float:
        """Extract price from Kroger API response."""
        try:
            products = data["data"]
            if not products:
                raise ValueError("No products found")

            product = products[0]
            items = product.get("items", [])
            if not items:
                raise ValueError("No items found for product")

            price_info = items[0].get("price", {})
            regular_price = price_info.get("regular")

            if regular_price is None:
                raise ValueError("No regular price found")

            return float(regular_price)

        except (KeyError, IndexError, ValueError) as e:
            raise ValueError(f"Could not extract price: {e}")