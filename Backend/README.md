# Meal Planning Backend

This is the backend for the Hackathon 2026 meal planning application. It provides APIs for meal suggestions, cost calculations, shopping lists, and constraint filtering.

## Project Structure

- `main.py`: FastAPI application with API endpoints
- `services.py`: Core business logic functions
- `filters.py`: Meal filtering functions (equipment, time, budget)
- `test.py`: Test script for manual verification
- `requirements.txt`: Python dependencies
- `setup_summary.txt`: Initial setup notes
- `models/`: Data models (Ingredient, Meal, etc.)
- `meals/`: Meal definitions and samples
- `pricing/`: Pricing providers and cost calculations
- `routes/`: Additional API routes (currently empty)
- `venv/`: Virtual environment (not committed)
- `__pycache__/`: Python cache files (not committed)

## Setup Instructions

### Prerequisites
- Python 3.9 or higher
- Virtual environment tool (venv)

### Installation

1. Navigate to the Backend directory:
   ```bash
   cd /path/to/Hackathon_2026/BeaverHacks_Project/Backend
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. The API will be available at:
   - http://localhost:8000
   - API documentation: http://localhost:8000/docs

### Testing

Run the test script to verify functionality:
```bash
python test.py
```

Or test endpoints manually:
```bash
curl http://localhost:8000/meals
curl -X POST http://localhost:8000/available-meals -H "Content-Type: application/json" -d '{"available_equipment": ["stove"], "max_time_minutes": 25}'
```

## API Endpoints

- `GET /`: Root endpoint
- `GET /test`: Test endpoint
- `GET /meals`: Get all available meals
- `POST /available-meals`: Get meals filtered by constraints
- `POST /meal-costs`: Get costs for meals
- `POST /shopping-list`: Get shopping list for meals
- `POST /total-cost`: Get total cost for meals

## Key Features

- Meal cost calculation with pricing providers
- Ingredient aggregation for shopping lists
- Constraint-based filtering (equipment, time)
- Mock pricing for testing
- FastAPI-based REST API

## Development Notes

- Uses Pydantic for data validation
- Mock pricing provider included for development
- Sample meals provided for testing
- All costs in USD, rounded to 2 decimals