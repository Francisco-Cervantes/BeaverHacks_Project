// API communication manager for backend integration
class APIManager {
    constructor() {
        // FastAPI backend (meals, pricing)
        this.baseURL = 'http://localhost:8001';
        // Flask AI chat server
        this.chatBaseURL = 'http://localhost:5000';
        this.init();
    }

    init() {
        // Set default headers
        this.defaultHeaders = {
            'Content-Type': 'application/json',
        };
    }

    // Generic request method
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        
        const config = {
            headers: { ...this.defaultHeaders },
            ...options,
        };

        try {
            const response = await fetch(url, config);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            return data;
        } catch (error) {
            console.error(`API request failed: ${endpoint}`, error);
            
            // Return mock data in development/offline mode
            if (error.name === 'TypeError' && error.message.includes('fetch')) {
                console.log('Using mock data due to network error');
                return this.getMockData(endpoint);
            }
            
            throw error;
        }
    }

    // GET request helper
    async get(endpoint) {
        return this.request(endpoint, {
            method: 'GET',
        });
    }

    // POST request helper
    async post(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }

    // API endpoints
    async getMeals() {
        try {
            const response = await this.get('/meals');
            return response.meals || [];
        } catch (error) {
            console.error('Error fetching meals:', error);
            return this.getMockMeals();
        }
    }

    async getFilteredMeals(constraints) {
        try {
            const response = await this.post('/available-meals', constraints);
            return response.meals || [];
        } catch (error) {
            console.error('Error fetching filtered meals:', error);
            // Return filtered mock data
            return this.getMockMeals().filter(meal => {
                if (constraints.max_time_minutes && meal.cook_time_minutes > constraints.max_time_minutes) {
                    return false;
                }
                if (constraints.available_equipment && !constraints.available_equipment.some(eq => meal.equipment_required.includes(eq))) {
                    return false;
                }
                return true;
            });
        }
    }

    async getMealCosts(meals) {
        try {
            const mealsData = meals.map(meal => meal);
            const response = await this.post('/meal-costs', mealsData);
            return response.costs || {};
        } catch (error) {
            console.error('Error fetching meal costs:', error);
            return this.getMockMealCosts();
        }
    }

    async getShoppingList(meals) {
        try {
            const mealsData = meals.map(meal => meal);
            const response = await this.post('/shopping-list', mealsData);
            return response.shopping_list || {};
        } catch (error) {
            console.error('Error fetching shopping list:', error);
            return this.getMockShoppingList();
        }
    }

    async getTotalCost(meals) {
        try {
            const mealsData = meals.map(meal => meal);
            const response = await this.post('/total-cost', mealsData);
            return response.total_cost || 0;
        } catch (error) {
            console.error('Error fetching total cost:', error);
            return 15.50; // Mock total cost
        }
    }

    // Chat API - integrates with Flask AI server on port 5000
    async sendChatMessage(message, context = {}) {
        try {
            const username = window.authManager?.currentUser?.name || null;
            const logged_in = window.authManager?.getIsLoggedIn() === true;
            const zip = document.getElementById('zip-input')?.value || '00000';
            const radius = parseInt(document.getElementById('mile-range')?.value || '10');

            const payload = { message, zip, radius, logged_in };
            if (username) payload.username = username;

            const response = await fetch(`${this.chatBaseURL}/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const data = await response.json();
            return data.response || 'Sorry, I could not process that request.';
        } catch (error) {
            console.error('Error sending chat message:', error);
            return this.getMockChatResponse(message, context);
        }
    }

    // Login via Flask AI server
    async loginUser(username, password) {
        const response = await fetch(`${this.chatBaseURL}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        const data = await response.json();
        if (!data.success) throw new Error(data.error || 'Login failed');
        return data;
    }

    // Register a new user
    async registerUser(username, password, zip = '00000', radius = 10) {
        const response = await fetch(`${this.chatBaseURL}/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password, zip, radius })
        });
        const data = await response.json();
        if (!data.success) throw new Error(data.error || 'Registration failed');
        return data;
    }

    async saveUserProfile(username, profileData) {
        try {
            const response = await fetch(`${this.chatBaseURL}/save-profile`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, ...profileData })
            });
            const data = await response.json();
            if (!data.success) throw new Error(data.error || 'Save failed');
            return data;
        } catch (error) {
            console.warn('Could not save profile to server, saved locally only:', error);
            return { success: true, local: true };
        }
    }

    // Mock data for development/offline mode
    getMockData(endpoint) {
        const mockResponses = {
            '/meals': { meals: this.getMockMeals() },
            '/available-meals': { meals: this.getMockMeals() },
            '/meal-costs': { costs: this.getMockMealCosts() },
            '/shopping-list': { shopping_list: this.getMockShoppingList() },
            '/total-cost': { total_cost: 15.50 }
        };

        return mockResponses[endpoint] || {};
    }

    getMockMeals() {
        return [
            {
                name: "Pasta with Tomato Sauce",
                ingredients: [
                    { ingredient_name: "pasta", quantity: 0.5, unit: "lb" },
                    { ingredient_name: "canned tomatoes", quantity: 1, unit: "can" },
                    { ingredient_name: "onion", quantity: 0.5, unit: "each" },
                    { ingredient_name: "garlic", quantity: 2, unit: "cloves" },
                    { ingredient_name: "olive oil", quantity: 2, unit: "tbsp" }
                ],
                cook_time_minutes: 20,
                equipment_required: ["stove", "pot"]
            },
            {
                name: "Chicken Rice Bowl",
                ingredients: [
                    { ingredient_name: "rice", quantity: 1, unit: "cup" },
                    { ingredient_name: "chicken breast", quantity: 0.5, unit: "lb" },
                    { ingredient_name: "onion", quantity: 0.25, unit: "each" },
                    { ingredient_name: "soy sauce", quantity: 2, unit: "tbsp" },
                    { ingredient_name: "carrots", quantity: 1, unit: "each" }
                ],
                cook_time_minutes: 30,
                equipment_required: ["stove", "pan"]
            },
            {
                name: "Scrambled Eggs",
                ingredients: [
                    { ingredient_name: "eggs", quantity: 2, unit: "each" },
                    { ingredient_name: "butter", quantity: 1, unit: "tbsp" },
                    { ingredient_name: "milk", quantity: 2, unit: "tbsp" },
                    { ingredient_name: "salt", quantity: 0.25, unit: "tsp" }
                ],
                cook_time_minutes: 5,
                equipment_required: ["stove", "pan"]
            },
            {
                name: "Vegetable Stir Fry",
                ingredients: [
                    { ingredient_name: "mixed vegetables", quantity: 2, unit: "cups" },
                    { ingredient_name: "oil", quantity: 2, unit: "tbsp" },
                    { ingredient_name: "garlic", quantity: 2, unit: "cloves" },
                    { ingredient_name: "soy sauce", quantity: 3, unit: "tbsp" },
                    { ingredient_name: "rice", quantity: 1, unit: "cup" }
                ],
                cook_time_minutes: 15,
                equipment_required: ["stove", "wok"]
            },
            {
                name: "Peanut Butter Sandwich",
                ingredients: [
                    { ingredient_name: "bread", quantity: 2, unit: "slices" },
                    { ingredient_name: "peanut butter", quantity: 2, unit: "tbsp" },
                    { ingredient_name: "jelly", quantity: 1, unit: "tbsp" }
                ],
                cook_time_minutes: 2,
                equipment_required: ["none"]
            },
            {
                name: "Microwave Mac and Cheese",
                ingredients: [
                    { ingredient_name: "pasta", quantity: 1, unit: "cup" },
                    { ingredient_name: "cheese", quantity: 0.5, unit: "cup" },
                    { ingredient_name: "milk", quantity: 0.25, unit: "cup" },
                    { ingredient_name: "butter", quantity: 1, unit: "tbsp" }
                ],
                cook_time_minutes: 8,
                equipment_required: ["microwave"]
            }
        ];
    }

    getMockMealCosts() {
        return {
            "Pasta with Tomato Sauce": 3.25,
            "Chicken Rice Bowl": 5.50,
            "Scrambled Eggs": 1.80,
            "Vegetable Stir Fry": 4.20,
            "Peanut Butter Sandwich": 1.25,
            "Microwave Mac and Cheese": 2.75
        };
    }

    getMockShoppingList() {
        return {
            "pasta": 1.5,
            "canned tomatoes": 2,
            "onion": 1,
            "chicken breast": 1,
            "eggs": 6,
            "rice": 2
        };
    }

    getMockChatResponse(message, context) {
        const responses = {
            greeting: [
                "Hello! I'm here to help you with meal planning and grocery shopping. What would you like to know?",
                "Hi there! I can help you find budget-friendly recipes and plan your meals. How can I assist you today?",
                "Welcome! I'm your BeaverEats assistant. Ask me about recipes, meal planning, or grocery tips!"
            ],
            budget: [
                "For budget-friendly meals, I recommend our pasta dishes and rice bowls. They typically cost under $4 per serving!",
                "Check out our Scrambled Eggs ($1.80) or Peanut Butter Sandwich ($1.25) for the cheapest options.",
                "Rice and pasta-based meals are your best bet for staying within budget. Want specific recommendations?"
            ],
            recipes: [
                "I have several great recipes! Are you looking for something quick, budget-friendly, or with specific ingredients?",
                "Our recipe collection includes everything from 2-minute sandwiches to 30-minute rice bowls. What type of meal interests you?",
                "I can suggest recipes based on your cooking equipment. Do you have access to a stove, microwave, or just basic tools?"
            ],
            meal_plan: [
                "Meal planning is a great way to save money! I can help you create a weekly plan based on your preferences and budget.",
                "To create a good meal plan, I'll need to know your budget, dietary restrictions, and available cooking equipment. Shall we start?",
                "A typical student meal plan might include 2-3 simple recipes rotated throughout the week. Would you like me to suggest some combinations?"
            ],
            ingredients: [
                "Tell me what ingredients you have, and I'll suggest recipes you can make with them!",
                "Having trouble with ingredient substitutions? I can help you adapt recipes based on what's available.",
                "Fresh ingredients can be expensive. Many of our recipes use pantry staples and frozen vegetables to keep costs down."
            ],
            default: [
                "I'm here to help with meal planning, recipes, and grocery shopping. Could you be more specific about what you need?",
                "I can assist with finding budget recipes, creating shopping lists, or planning your weekly meals. What interests you most?",
                "Feel free to ask me about specific recipes, ingredient substitutions, or meal planning strategies!"
            ]
        };

        const lowerMessage = message.toLowerCase();
        let responseCategory = 'default';

        if (lowerMessage.includes('hello') || lowerMessage.includes('hi') || lowerMessage.includes('hey')) {
            responseCategory = 'greeting';
        } else if (lowerMessage.includes('budget') || lowerMessage.includes('cheap') || lowerMessage.includes('money') || lowerMessage.includes('cost')) {
            responseCategory = 'budget';
        } else if (lowerMessage.includes('recipe') || lowerMessage.includes('cook') || lowerMessage.includes('make')) {
            responseCategory = 'recipes';
        } else if (lowerMessage.includes('meal plan') || lowerMessage.includes('plan') || lowerMessage.includes('week')) {
            responseCategory = 'meal_plan';
        } else if (lowerMessage.includes('ingredient') || lowerMessage.includes('have')) {
            responseCategory = 'ingredients';
        }

        const categoryResponses = responses[responseCategory];
        return categoryResponses[Math.floor(Math.random() * categoryResponses.length)];
    }

    // Utility methods
    async testConnection() {
        try {
            const response = await this.get('/');
            return response.message === "Hello World";
        } catch (error) {
            console.warn('Backend connection failed, using mock data');
            return false;
        }
    }

    async checkHealth() {
        try {
            const response = await this.get('/test');
            return response.message === "Test endpoint working!";
        } catch (error) {
            return false;
        }
    }

    // Store and location services (for future expansion)
    async getNearbyStores(zipCode) {
        // Mock implementation - would integrate with actual store APIs
        return [
            {
                name: "Safeway",
                distance: 0.5,
                address: "123 Main St, Corvallis, OR 97331",
                priceRating: 3 // 1-5 scale
            },
            {
                name: "WinCo Foods",
                distance: 1.2,
                address: "456 Oak Ave, Corvallis, OR 97331",
                priceRating: 5 // Best prices
            },
            {
                name: "Fred Meyer",
                distance: 0.8,
                address: "789 Elm St, Corvallis, OR 97331",
                priceRating: 4
            }
        ];
    }

    async getPriceComparison(ingredient, zipCode) {
        // Mock price comparison across stores
        return {
            ingredient,
            prices: [
                { store: "WinCo Foods", price: 2.99, unit: "lb" },
                { store: "Safeway", price: 3.49, unit: "lb" },
                { store: "Fred Meyer", price: 3.29, unit: "lb" }
            ],
            savings: "Save $0.50 at WinCo Foods"
        };
    }
}

// Export for global use
window.APIManager = APIManager;