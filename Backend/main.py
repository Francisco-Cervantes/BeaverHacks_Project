from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services import (
    get_all_meals,
    get_available_meals,
    get_meal_costs,
    get_shopping_list,
    get_total_cost,
    get_store_options,
    get_prices_for_store,
    compare_store_costs,
)
from pricing.providers.mock_provider import MockPricingProvider
from models.meal import Meal
from typing import Dict, Any, List
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
pricing_provider = MockPricingProvider()

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, use specific origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/test")
async def test():
    return {"message": "Test endpoint working!"}

@app.get("/meals")
async def get_meals():
    meals = get_all_meals()
    return {"meals": [meal.dict() for meal in meals]}

@app.post("/available-meals")
async def available_meals(constraints: Dict[str, Any]):
    meals = get_available_meals(constraints)
    return {"meals": [meal.dict() for meal in meals]}

@app.post("/meal-costs")
async def meal_costs(meals_data: List[Dict[str, Any]]):
    # Assuming meals_data is list of meal dicts, but for simplicity, use all meals or parse
    # For now, get costs for all meals
    meals = get_all_meals()
    costs = get_meal_costs(meals, pricing_provider)
    return {"costs": costs}

@app.post("/shopping-list")
async def shopping_list(meals_data: List[Dict[str, Any]]):
    # Placeholder: parse meals_data to Meal objects
    meals = get_all_meals()  # For now
    shopping = get_shopping_list(meals)
    return {"shopping_list": shopping}

@app.post("/total-cost")
async def total_cost(meals_data: List[Dict[str, Any]]):
    meals = get_all_meals()  # For now
    cost = get_total_cost(meals, pricing_provider)
    return {"total_cost": cost}


@app.get("/stores")
async def stores(zip_code: str):
    return {"stores": get_store_options(zip_code)}


@app.post("/store-prices")
async def store_prices(
    store_name: str,
    shopping_list: Dict[str, float],
    zip_code: str,
    max_distance_miles: float = None,
    gas_price: float = None,
    vehicle_mpg: float = 25.0,
    avg_speed_mph: float = 25.0,
):
    return get_prices_for_store(
        store_name,
        shopping_list,
        zip_code,
        max_distance_miles=max_distance_miles,
        gas_price=gas_price,
        vehicle_mpg=vehicle_mpg,
        avg_speed_mph=avg_speed_mph,
    )


@app.post("/compare-stores")
async def compare_stores(
    meals: List[Meal],
    zip_code: str,
    max_distance_miles: float = None,
    gas_price: float = None,
    vehicle_mpg: float = 25.0,
    avg_speed_mph: float = 25.0,
):
    return compare_store_costs(
        meals,
        zip_code,
        max_distance_miles=max_distance_miles,
        gas_price=gas_price,
        vehicle_mpg=vehicle_mpg,
        avg_speed_mph=avg_speed_mph,
    )


@app.post("/chat")
async def chat_with_ai(message_data: Dict[str, Any]):
    """
    Chat endpoint that integrates with NVIDIA AI API
    """
    user_message = message_data.get("message", "")
    context = message_data.get("context", {})
    
    nvidia_api_key = os.getenv("NVIDIA_API_KEY")
    
    if not nvidia_api_key:
        # Fallback to rule-based responses if no API key
        return {"response": get_fallback_response(user_message)}
    
    try:
        # NVIDIA AI API integration
        headers = {
            "Authorization": f"Bearer {nvidia_api_key}",
            "Content-Type": "application/json",
        }
        
        # Enhanced system prompt for food/recipe assistance
        system_prompt = """You are NomNomNomotron, an AI assistant specialized in helping busy families and college students with:
- Budget-friendly meal planning and recipes
- Grocery shopping tips and price comparisons
- Quick and easy meal suggestions
- Ingredient substitutions and cooking advice

Respond in a helpful, friendly tone. Focus on practical, affordable solutions. When suggesting recipes, mention approximate cook times and cost estimates."""

        payload = {
            "model": "meta/llama-3.2-3b-instruct",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Context: {context}\n\nUser question: {user_message}"}
            ],
            "max_tokens": 512,
            "temperature": 0.7,
            "stream": False
        }
        
        response = requests.post(
            "https://integrate.api.nvidia.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            ai_response = response.json()
            if "choices" in ai_response and len(ai_response["choices"]) > 0:
                return {
                    "response": ai_response["choices"][0]["message"]["content"],
                    "source": "nvidia_ai"
                }
        
        # Fallback if API call fails
        return {"response": get_fallback_response(user_message), "source": "fallback"}
        
    except Exception as e:
        print(f"NVIDIA AI API error: {e}")
        return {"response": get_fallback_response(user_message), "source": "fallback"}


def get_fallback_response(message: str) -> str:
    """
    Rule-based fallback responses when AI API is unavailable
    """
    message_lower = message.lower()
    
    # Recipe suggestions
    if any(word in message_lower for word in ['recipe', 'cook', 'make', 'meal']):
        if 'quick' in message_lower or 'fast' in message_lower:
            return "Here are some quick meal ideas: Scrambled eggs (5 min, $2), Pasta with sauce (15 min, $3), or a PB&J sandwich (2 min, $1.50). Would you like a detailed recipe for any of these?"
        elif 'budget' in message_lower or 'cheap' in message_lower:
            return "For budget meals, try: Rice and beans ($2), Pasta with tomato sauce ($2.50), or Ramen with egg ($1.75). These are nutritious and filling!"
        else:
            return "I can help you find recipes! Try asking for 'quick meals', 'budget recipes', or tell me what ingredients you have available."
    
    # Shopping and pricing
    elif any(word in message_lower for word in ['shop', 'store', 'price', 'cost', 'grocery']):
        return "I can help you find the best grocery deals! Use our store comparison feature to find the lowest prices near you. What's your ZIP code and how far are you willing to travel?"
    
    # Meal planning
    elif any(word in message_lower for word in ['plan', 'week', 'schedule']):
        return "Meal planning saves time and money! I can help you create a weekly plan based on your budget and preferences. What's your weekly food budget and how many people are you feeding?"
    
    # Ingredients and substitutions
    elif any(word in message_lower for word in ['ingredient', 'substitute', 'replace']):
        return "I can help with ingredient substitutions! Tell me what recipe you're making and what ingredient you need to replace, and I'll suggest alternatives."
    
    # General greeting
    elif any(word in message_lower for word in ['hello', 'hi', 'hey']):
        return "Hello! I'm NomNomNomotron, your AI cooking assistant. I can help you with budget recipes, meal planning, grocery shopping, and cooking tips. What would you like help with today?"
    
    # Default response
    else:
        return "I'm here to help with cooking, recipes, meal planning, and grocery shopping! Try asking me about budget meals, quick recipes, or meal planning tips. What would you like to know?"
