// Navigation management for single-page application
class NavigationManager {
    constructor() {
        this.currentPage = 'home';
        this.pages = new Map();
        this.init();
    }

    init() {
        this.setupNavigation();
        this.setupMobileMenu();
        
        // Register page loaders
        this.registerPageLoaders();
    }

    setupNavigation() {
        // Add click listeners to nav links
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const page = link.getAttribute('data-page');
                if (page) {
                    this.navigateTo(page);
                }
            });
        });

        // Handle browser back/forward
        window.addEventListener('popstate', (e) => {
            if (e.state && e.state.page) {
                this.showPage(e.state.page, false);
            }
        });
    }

    setupMobileMenu() {
        const navToggle = document.getElementById('nav-toggle');
        const navMenu = document.getElementById('nav-menu');

        if (navToggle && navMenu) {
            navToggle.addEventListener('click', () => {
                navMenu.classList.toggle('active');
            });

            // Close mobile menu when clicking a link
            document.querySelectorAll('.nav-link').forEach(link => {
                link.addEventListener('click', () => {
                    navMenu.classList.remove('active');
                });
            });
        }
    }

    navigateTo(page) {
        // Check authentication requirements
        const authRequiredPages = ['profile', 'meal-plan'];
        if (authRequiredPages.includes(page) && !window.authManager.getIsLoggedIn()) {
            window.authManager.showAuthRequiredMessage(this.getPageTitle(page));
            return;
        }

        this.showPage(page, true);
    }

    showPage(page, updateHistory = true) {
        // Hide all pages
        document.querySelectorAll('.page').forEach(p => {
            p.classList.remove('active');
        });

        // Update nav active state
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });

        // Show target page
        const targetPage = document.getElementById(`${page}-page`);
        if (targetPage) {
            targetPage.classList.add('active');
        }

        // Update nav link
        const activeLink = document.querySelector(`[data-page="${page}"]`);
        if (activeLink) {
            activeLink.classList.add('active');
        }

        // Load page content if needed
        this.loadPageContent(page);

        // Update URL and history
        if (updateHistory) {
            const url = page === 'home' ? '/' : `/#${page}`;
            history.pushState({ page }, '', url);
        }

        this.currentPage = page;
        
        // Update page title
        document.title = `${this.getPageTitle(page)} - BeaverEats`;
    }

    getPageTitle(page) {
        const titles = {
            'home': 'Home',
            'chat': 'Chat',
            'meals': 'Meals',
            'profile': 'Profile',
            'meal-plan': 'Meal Plan',
            'recipes': 'Recipes',
            'individual-meal': 'Meal Details'
        };
        return titles[page] || 'BeaverEats';
    }

    registerPageLoaders() {
        // Register functions to load content for each page
        this.pages.set('chat', () => this.loadChatPage());
        this.pages.set('meals', () => this.loadMealsPage());
        this.pages.set('profile', () => this.loadProfilePage());
        this.pages.set('meal-plan', () => this.loadMealPlanPage());
        this.pages.set('recipes', () => this.loadRecipesPage());
        this.pages.set('individual-meal', () => this.loadIndividualMealPage());
    }

    loadPageContent(page) {
        const loader = this.pages.get(page);
        if (loader) {
            loader();
        }
    }

    // Page loaders
    loadChatPage() {
        const chatPage = document.getElementById('chat-page');
        if (chatPage && !chatPage.hasAttribute('data-loaded')) {
            chatPage.innerHTML = `
                <div class="chat-container">
                    <div style="width: 100%; display: flex; flex-direction: column; height: 100%;">
                        <div class="chat-header">
                            <h2><i class="fas fa-robot"></i> BeaverEats Assistant</h2>
                            <p>Ask me about recipes, meal planning, or grocery shopping tips!</p>
                        </div>
                        <div class="chat-messages" id="chat-messages">
                            <div class="message bot">
                                <p>Hi! I'm your BeaverEats assistant. I can help you:</p>
                                <ul style="margin: 10px 0; padding-left: 20px;">
                                    <li>Find budget-friendly recipes</li>
                                    <li>Plan your weekly meals</li>
                                    <li>Suggest grocery shopping tips</li>
                                    <li>Find stores with the best prices</li>
                                </ul>
                                <p>What would you like to know?</p>
                            </div>
                        </div>
                        <div class="chat-input-container">
                            <input 
                                type="text" 
                                id="chat-input" 
                                class="chat-input" 
                                placeholder="Type your message here..."
                            >
                            <button id="send-btn" class="send-btn">
                                <i class="fas fa-paper-plane"></i>
                            </button>
                        </div>
                    </div>
                </div>
            `;
            this.setupChatFunctionality();
            chatPage.setAttribute('data-loaded', 'true');
        }
    }

    setupChatFunctionality() {
        const chatInput = document.getElementById('chat-input');
        const sendBtn = document.getElementById('send-btn');
        const chatMessages = document.getElementById('chat-messages');

        const sendMessage = () => {
            const message = chatInput.value.trim();
            if (message) {
                this.addMessage(message, 'user');
                chatInput.value = '';
                
                // Simulate bot response
                setTimeout(() => {
                    this.getBotResponse(message);
                }, 1000);
            }
        };

        sendBtn.addEventListener('click', sendMessage);
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }

    addMessage(text, sender) {
        const chatMessages = document.getElementById('chat-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        messageDiv.textContent = text;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    async getBotResponse(userMessage) {
        const responses = {
            'budget': 'For budget-friendly meals, try our pasta dishes and rice bowls. They typically cost under $3 per serving!',
            'recipe': 'I can suggest recipes based on your preferences. What ingredients do you have available?',
            'meal plan': 'Meal planning saves time and money! Would you like me to help you create a weekly plan?',
            'grocery': 'Check our price comparison feature to find the best deals at nearby stores.',
            'cheap': 'Our cheapest meals include pasta with tomato sauce ($2.50) and scrambled eggs ($1.80).',
            'hello': 'Hello! How can I help you with your meal planning today?'
        };

        const lowerMessage = userMessage.toLowerCase();
        let response = "I'm here to help with meals, recipes, and grocery shopping. Could you be more specific about what you need?";

        for (const [keyword, reply] of Object.entries(responses)) {
            if (lowerMessage.includes(keyword)) {
                response = reply;
                break;
            }
        }

        this.addMessage(response, 'bot');
    }

    loadMealsPage() {
        const mealsPage = document.getElementById('meals-page');
        if (mealsPage && !mealsPage.hasAttribute('data-loaded')) {
            mealsPage.innerHTML = `
                <div class="container" style="padding: 40px 20px;">
                    <h1>Available Meals</h1>
                    <div class="filters-section" style="margin-bottom: 30px;">
                        <div style="display: flex; gap: 20px; flex-wrap: wrap; align-items: center;">
                            <select id="time-filter" class="form-control" style="width: auto; padding: 8px;">
                                <option value="">Any cooking time</option>
                                <option value="15">Under 15 minutes</option>
                                <option value="30">Under 30 minutes</option>
                                <option value="60">Under 1 hour</option>
                            </select>
                            <select id="equipment-filter" class="form-control" style="width: auto; padding: 8px;">
                                <option value="">Any equipment</option>
                                <option value="stove">Stove only</option>
                                <option value="oven">Oven only</option>
                                <option value="microwave">Microwave only</option>
                            </select>
                            <button id="apply-filters" class="btn btn-primary">Apply Filters</button>
                        </div>
                    </div>
                    <div id="meals-grid" class="meals-grid" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px;">
                        <div style="text-align: center; padding: 40px;">
                            <i class="fas fa-spinner fa-spin" style="font-size: 2rem; color: #007bff;"></i>
                            <p>Loading meals...</p>
                        </div>
                    </div>
                </div>
            `;
            this.loadMealsData();
            mealsPage.setAttribute('data-loaded', 'true');
        }
    }

    async loadMealsData() {
        try {
            const meals = await window.apiManager.getMeals();
            this.displayMeals(meals);
            this.setupMealsFilters();
        } catch (error) {
            console.error('Error loading meals:', error);
            const mealsGrid = document.getElementById('meals-grid');
            if (mealsGrid) {
                mealsGrid.innerHTML = '<p style="color: #666; text-align: center;">Error loading meals. Please try again later.</p>';
            }
        }
    }

    displayMeals(meals) {
        const mealsGrid = document.getElementById('meals-grid');
        if (!mealsGrid) return;

        mealsGrid.innerHTML = meals.map(meal => `
            <div class="meal-card" style="background: white; border-radius: 12px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); overflow: hidden; cursor: pointer; transition: transform 0.3s ease;" onclick="navigationManager.showMealDetail('${meal.name}')">
                <div style="height: 200px; background: linear-gradient(45deg, #f8f9fa, #e9ecef); display: flex; align-items: center; justify-content: center;">
                    <i class="fas fa-utensils" style="font-size: 3rem; color: #007bff;"></i>
                </div>
                <div style="padding: 20px;">
                    <h3 style="margin-bottom: 10px; color: #333;">${meal.name}</h3>
                    <div style="display: flex; align-items: center; gap: 15px; color: #666; font-size: 14px; margin-bottom: 15px;">
                        <span><i class="fas fa-clock"></i> ${meal.cook_time_minutes} min</span>
                        <span><i class="fas fa-tools"></i> ${meal.equipment_required.join(', ')}</span>
                    </div>
                    <div style="margin-bottom: 15px;">
                        <strong style="color: #333;">Ingredients:</strong>
                        <p style="color: #666; font-size: 14px; margin: 5px 0;">${meal.ingredients.slice(0, 3).map(i => i.ingredient_name).join(', ')}${meal.ingredients.length > 3 ? '...' : ''}</p>
                    </div>
                    <div class="btn btn-primary" style="width: 100%; text-align: center;">
                        View Recipe
                    </div>
                </div>
            </div>
        `).join('');

        // Add hover effects
        document.querySelectorAll('.meal-card').forEach(card => {
            card.addEventListener('mouseenter', () => {
                card.style.transform = 'translateY(-5px)';
            });
            card.addEventListener('mouseleave', () => {
                card.style.transform = 'translateY(0)';
            });
        });
    }

    setupMealsFilters() {
        const applyFiltersBtn = document.getElementById('apply-filters');
        if (applyFiltersBtn) {
            applyFiltersBtn.addEventListener('click', () => {
                const timeFilter = document.getElementById('time-filter').value;
                const equipmentFilter = document.getElementById('equipment-filter').value;
                
                const constraints = {};
                if (timeFilter) constraints.max_time_minutes = parseInt(timeFilter);
                if (equipmentFilter) constraints.available_equipment = [equipmentFilter];
                
                this.applyMealFilters(constraints);
            });
        }
    }

    async applyMealFilters(constraints) {
        try {
            const meals = await window.apiManager.getFilteredMeals(constraints);
            this.displayMeals(meals);
        } catch (error) {
            console.error('Error applying filters:', error);
        }
    }

    showMealDetail(mealName) {
        // Store meal name for detail page
        localStorage.setItem('currentMeal', mealName);
        this.navigateTo('individual-meal');
    }

    loadProfilePage() {
        // Call the profile page loader
        if (window.loadProfilePage) {
            window.loadProfilePage();
        }
    }

    loadMealPlanPage() {
        // Call the meal plan page loader  
        if (window.loadMealPlanPage) {
            window.loadMealPlanPage();
        }
    }

    loadRecipesPage() {
        // Recipes page - similar to meals but different layout
        const recipesPage = document.getElementById('recipes-page');
        if (recipesPage && !recipesPage.hasAttribute('data-loaded')) {
            recipesPage.innerHTML = `
                <div class="container" style="padding: 40px 20px;">
                    <h1>Recipe Collection</h1>
                    <p>Discover budget-friendly recipes perfect for students</p>
                    <div id="recipes-grid" style="margin-top: 30px;">
                        Loading recipes...
                    </div>
                </div>
            `;
            this.loadRecipesData();
            recipesPage.setAttribute('data-loaded', 'true');
        }
    }

    async loadRecipesData() {
        // Reuse meals data for recipes
        try {
            const meals = await window.apiManager.getMeals();
            const recipesGrid = document.getElementById('recipes-grid');
            if (recipesGrid) {
                recipesGrid.innerHTML = `
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px;">
                        ${meals.map(meal => `
                            <div class="recipe-card" style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); cursor: pointer;" onclick="navigationManager.showMealDetail('${meal.name}')">
                                <h3>${meal.name}</h3>
                                <p style="color: #666; font-size: 14px; margin: 10px 0;">${meal.cook_time_minutes} minutes • ${meal.ingredients.length} ingredients</p>
                                <div class="btn btn-outline" style="font-size: 12px; padding: 6px 12px;">View Recipe</div>
                            </div>
                        `).join('')}
                    </div>
                `;
            }
        } catch (error) {
            console.error('Error loading recipes:', error);
        }
    }

    loadIndividualMealPage() {
        // This will be called when showing meal details
        const mealName = localStorage.getItem('currentMeal');
        if (!mealName) return;
        
        this.loadMealDetail(mealName);
    }

    async loadMealDetail(mealName) {
        try {
            const meals = await window.apiManager.getMeals();
            const meal = meals.find(m => m.name === mealName);
            
            if (!meal) return;

            const mealPage = document.getElementById('individual-meal-page');
            mealPage.innerHTML = `
                <div class="meal-detail">
                    <button onclick="history.back()" class="btn btn-secondary" style="margin-bottom: 20px;">
                        <i class="fas fa-arrow-left"></i> Back
                    </button>
                    
                    <div class="meal-header">
                        <img src="https://via.placeholder.com/400x300/007bff/ffffff?text=${encodeURIComponent(meal.name)}" 
                             alt="${meal.name}" class="meal-image">
                        <h1>${meal.name}</h1>
                        <div style="display: flex; gap: 20px; justify-content: center; color: #666;">
                            <span><i class="fas fa-clock"></i> ${meal.cook_time_minutes} minutes</span>
                            <span><i class="fas fa-users"></i> 1-2 servings</span>
                        </div>
                    </div>

                    <div class="meal-info">
                        <div class="ingredients-section">
                            <h3><i class="fas fa-list"></i> Ingredients</h3>
                            <ul class="ingredients-list">
                                ${meal.ingredients.map(ingredient => `
                                    <li>
                                        <span>${ingredient.ingredient_name}</span>
                                        <span class="ingredient-amount">${ingredient.quantity} ${ingredient.unit}</span>
                                    </li>
                                `).join('')}
                            </ul>
                        </div>

                        <div class="equipment-section">
                            <h3><i class="fas fa-tools"></i> Equipment Needed</h3>
                            <ul class="equipment-list">
                                ${meal.equipment_required.map(equipment => `
                                    <li><i class="fas fa-check"></i> ${equipment}</li>
                                `).join('')}
                            </ul>
                        </div>
                    </div>

                    <div class="instructions-section">
                        <h3><i class="fas fa-list-ol"></i> Step-by-Step Instructions</h3>
                        <div class="instructions">
                            ${this.generateInstructions(meal).map((step, index) => `
                                <div class="step">
                                    <div class="step-number">Step ${index + 1}</div>
                                    <p>${step}</p>
                                </div>
                            `).join('')}
                        </div>
                    </div>

                    <div style="text-align: center; margin-top: 40px;">
                        <button class="btn btn-success" onclick="navigationManager.addToMealPlan('${meal.name}')">
                            <i class="fas fa-plus"></i> Add to Meal Plan
                        </button>
                        <button class="btn btn-primary" onclick="navigationManager.getShoppingList(['${meal.name}'])">
                            <i class="fas fa-shopping-cart"></i> Get Shopping List
                        </button>
                    </div>
                </div>
            `;
        } catch (error) {
            console.error('Error loading meal detail:', error);
        }
    }

    generateInstructions(meal) {
        // Generate basic instructions based on meal type
        const instructions = [
            "Gather all ingredients and equipment.",
            `Prepare your ${meal.equipment_required.join(' and ')}.`,
        ];

        if (meal.name.toLowerCase().includes('pasta')) {
            instructions.push(
                "Bring a pot of salted water to boil.",
                "Add pasta and cook according to package directions.",
                "While pasta cooks, prepare your sauce with the remaining ingredients.",
                "Drain pasta and combine with sauce.",
                "Serve hot and enjoy!"
            );
        } else if (meal.name.toLowerCase().includes('rice')) {
            instructions.push(
                "Rinse rice until water runs clear.",
                "Cook rice according to package directions.",
                "While rice cooks, prepare other ingredients.",
                "Combine everything and serve hot."
            );
        } else {
            instructions.push(
                "Follow your preferred cooking method for these ingredients.",
                "Cook until ingredients are properly heated and combined.",
                "Season to taste and serve."
            );
        }

        return instructions;
    }

    addToMealPlan(mealName) {
        if (!window.authManager.getIsLoggedIn()) {
            window.authManager.showAuthRequiredMessage('Meal Planning');
            return;
        }
        
        // TODO: Implement meal plan addition
        window.authManager.showSuccessMessage(`${mealName} added to your meal plan!`);
    }

    async getShoppingList(mealNames) {
        try {
            // This would typically get meals data and create shopping list
            window.authManager.showInfoMessage('Shopping list feature coming soon!');
        } catch (error) {
            console.error('Error creating shopping list:', error);
        }
    }
}

// Export for global use
window.NavigationManager = NavigationManager;