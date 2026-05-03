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
                <div class="chat-layout">
                    <!-- Left Column: AI Chat -->
                    <div class="chat-column" id="chat-column">
                        <div class="chat-header">
                            <h2><i class="fas fa-robot"></i> NomNomNomotron AI Assistant</h2>
                            <p>Ask me about recipes, meal planning, or grocery shopping tips!</p>
                        </div>
                        
                        <div class="chat-messages" id="chat-messages">
                            <div class="message bot">
                                <p>Hi! I'm your NomNomNomotron AI assistant powered by NVIDIA technology. I can help you:</p>
                                <ul style="margin: 10px 0; padding-left: 20px;">
                                    <li>Find budget-friendly recipes</li>
                                    <li>Plan your weekly meals</li>
                                    <li>Suggest grocery shopping tips</li>
                                    <li>Find stores with the best prices</li>
                                </ul>
                                <p>What would you like to cook today?</p>
                            </div>
                        </div>
                        
                        <div class="chat-input-container">
                            <input 
                                type="text" 
                                id="chat-input" 
                                class="chat-input" 
                                placeholder="Ask for recipe suggestions..."
                            >
                            <button id="send-btn" class="send-btn">
                                <i class="fas fa-paper-plane"></i>
                            </button>
                        </div>
                    </div>

                    <!-- Resizable Divider -->
                    <div class="chat-divider" id="chat-divider">
                        <div class="divider-handle">
                            <i class="fas fa-grip-vertical"></i>
                        </div>
                    </div>

                    <!-- Right Column: Recipe Results -->
                    <div class="recipes-column" id="recipes-column">
                        <div class="recipes-header">
                            <h3><i class="fas fa-utensils"></i> Recipe Suggestions</h3>
                            <div class="recipe-mode-toggle">
                                <label class="toggle-switch">
                                    <input type="checkbox" id="individual-meal-mode">
                                    <span class="slider"></span>
                                </label>
                                <span class="toggle-label">Individual Meal Mode</span>
                            </div>
                        </div>
                        
                        <div class="recipes-container" id="recipes-container">
                            <div class="no-results">
                                <i class="fas fa-search" style="font-size: 3rem; color: #ccc; margin-bottom: 20px;"></i>
                                <p style="color: #666;">Ask the AI for recipe suggestions to see results here!</p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Meal Plan Dropdown Modal -->
                <div id="meal-plan-dropdown" class="dropdown-modal" style="display: none;">
                    <div class="dropdown-content">
                        <h4>Add to Meal Plan</h4>
                        <div class="meal-options">
                            <button class="meal-option-btn" data-meal="breakfast">
                                <i class="fas fa-sun"></i> Breakfast
                            </button>
                            <button class="meal-option-btn" data-meal="lunch">
                                <i class="fas fa-cloud-sun"></i> Lunch
                            </button>
                            <button class="meal-option-btn" data-meal="dinner">
                                <i class="fas fa-moon"></i> Dinner
                            </button>
                        </div>
                        <button class="close-dropdown">Cancel</button>
                    </div>
                </div>

                <!-- Login Prompt Modal -->
                <div id="login-prompt-modal" class="login-modal" style="display: none;">
                    <div class="login-modal-content">
                        <h3><i class="fas fa-lock"></i> Login Required</h3>
                        <p>You need to sign in to access meal planning features and save recipes to your plan.</p>
                        <div class="login-modal-actions">
                            <button id="go-to-login" class="btn btn-primary">Sign In</button>
                            <button id="close-login-modal" class="btn btn-secondary">Cancel</button>
                        </div>
                    </div>
                </div>
            `;
            this.setupChatFunctionality();
            this.setupRecipesFunctionality();
            this.setupResizableDivider();
            
            // Load some initial recipes to show the interface working
            setTimeout(() => {
                this.loadInitialRecipes();
            }, 100);
            
            chatPage.setAttribute('data-loaded', 'true');
        }
    }

    setupChatFunctionality() {
        // Wait a brief moment to ensure elements are in DOM
        setTimeout(() => {
            const chatInput = document.getElementById('chat-input');
            const sendBtn = document.getElementById('send-btn');
            const chatMessages = document.getElementById('chat-messages');

            if (!chatInput || !sendBtn || !chatMessages) {
                console.error('Chat elements not found in DOM');
                return;
            }

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
        }, 50);
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
            'hello': 'Hello! How can I help you with your meal planning today?',
            'chicken': 'I found some great chicken recipes for you!',
            'pasta': 'Here are some delicious pasta recipes!',
            'quick': 'Here are some quick meal options for busy days!',
            'breakfast': 'Here are some healthy breakfast ideas!',
            'vegetarian': 'I found some tasty vegetarian options for you!'
        };

        const lowerMessage = userMessage.toLowerCase();
        let response = "I'm here to help with meals, recipes, and grocery shopping. Let me find some recipe suggestions for you!";

        for (const [keyword, reply] of Object.entries(responses)) {
            if (lowerMessage.includes(keyword)) {
                response = reply;
                break;
            }
        }

        this.addMessage(response, 'bot');
        
        // Trigger recipe search based on message
        await this.searchRecipes(userMessage);
    }

    async searchRecipes(query) {
        try {
            const meals = await window.apiManager.getMeals();
            // Filter meals based on query keywords
            const filteredMeals = this.filterMealsByQuery(meals, query);
            this.displayRecipeResults(filteredMeals);
        } catch (error) {
            console.error('Error searching recipes:', error);
        }
    }

    filterMealsByQuery(meals, query) {
        const lowerQuery = query.toLowerCase();
        const keywords = lowerQuery.split(' ');
        
        return meals.filter(meal => {
            const mealText = (meal.name + ' ' + meal.ingredients.map(i => i.ingredient_name).join(' ')).toLowerCase();
            return keywords.some(keyword => {
                if (keyword.length < 3) return false; // Skip very short words
                return mealText.includes(keyword);
            });
        }).slice(0, 6); // Limit to 6 results
    }

    displayRecipeResults(meals) {
        const container = document.getElementById('recipes-container');
        if (!container) return;

        if (meals.length === 0) {
            container.innerHTML = `
                <div class="no-results">
                    <i class="fas fa-search" style="font-size: 3rem; color: #ccc; margin-bottom: 20px;"></i>
                    <p style="color: #666;">No recipes found. Try a different search term!</p>
                </div>
            `;
            return;
        }

        container.innerHTML = `
            <div class="recipes-grid">
                ${meals.map(meal => this.createRecipeCard(meal)).join('')}
            </div>
        `;

        // Add event listeners to buttons
        this.setupRecipeCardListeners();
    }

    createRecipeCard(meal) {
        const cost = this.estimateMealCost(meal);
        const isLoggedIn = window.authManager?.getIsLoggedIn() || false;
        
        return `
            <div class="recipe-card" data-meal="${meal.name}">
                <div class="recipe-image">
                    <div class="placeholder-image">
                        <i class="fas fa-utensils"></i>
                    </div>
                </div>
                <div class="recipe-info">
                    <h4 class="recipe-title">${meal.name}</h4>
                    <div class="recipe-details">
                        <div class="detail-item">
                            <i class="fas fa-clock"></i>
                            <span>${meal.cook_time_minutes} min</span>
                        </div>
                        <div class="detail-item">
                            <i class="fas fa-dollar-sign"></i>
                            <span>$${cost}</span>
                        </div>
                        <div class="detail-item">
                            <i class="fas fa-users"></i>
                            <span>1-2 servings</span>
                        </div>
                    </div>
                    <div class="ingredients-preview">
                        <strong>Ingredients:</strong>
                        <span>${meal.ingredients.slice(0, 3).map(i => i.ingredient_name).join(', ')}${meal.ingredients.length > 3 ? '...' : ''}</span>
                    </div>
                </div>
                <div class="recipe-actions">
                    <button class="make-it-btn btn btn-primary" data-meal="${meal.name}">
                        <i class="fas fa-play"></i> Make It
                    </button>
                    <button class="add-to-plan-btn btn ${isLoggedIn ? 'btn-success' : 'btn-disabled'}" 
                            data-meal="${meal.name}" ${!isLoggedIn ? 'disabled' : ''}>
                        <i class="fas fa-plus"></i>
                    </button>
                </div>
            </div>
        `;
    }

    estimateMealCost(meal) {
        // Simple cost estimation based on ingredients
        const baseCosts = {
            'pasta': 0.50, 'chicken': 2.00, 'eggs': 0.30, 'rice': 0.25,
            'onion': 0.25, 'tomato': 0.50, 'cheese': 1.00, 'bread': 0.15
        };
        
        let totalCost = 0;
        meal.ingredients.forEach(ingredient => {
            const name = ingredient.ingredient_name.toLowerCase();
            const matchedCost = Object.entries(baseCosts).find(([key]) => name.includes(key));
            totalCost += matchedCost ? matchedCost[1] * ingredient.quantity : 0.50;
        });
        
        return Math.max(totalCost, 1.50).toFixed(2);
    }

    setupRecipeCardListeners() {
        // Make It buttons
        document.querySelectorAll('.make-it-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const mealName = e.target.closest('.make-it-btn').getAttribute('data-meal');
                this.goToMealDetail(mealName);
            });
        });

        // Add to Plan buttons
        document.querySelectorAll('.add-to-plan-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const mealName = e.target.closest('.add-to-plan-btn').getAttribute('data-meal');
                if (window.authManager?.getIsLoggedIn()) {
                    this.showMealPlanDropdown(e.target, mealName);
                } else {
                    this.showLoginPrompt();
                }
            });
        });
    }

    goToMealDetail(mealName) {
        localStorage.setItem('currentMeal', mealName);
        this.navigateTo('individual-meal');
    }

    showMealPlanDropdown(button, mealName) {
        const dropdown = document.getElementById('meal-plan-dropdown');
        const rect = button.getBoundingClientRect();
        
        dropdown.style.display = 'block';
        dropdown.style.left = `${rect.left}px`;
        dropdown.style.top = `${rect.bottom + 10}px`;
        
        // Store meal name for when option is selected
        dropdown.setAttribute('data-meal', mealName);
        
        // Set up meal option listeners
        document.querySelectorAll('.meal-option-btn').forEach(btn => {
            btn.onclick = (e) => {
                const mealType = e.target.closest('.meal-option-btn').getAttribute('data-meal');
                this.addToMealPlan(mealName, mealType);
                dropdown.style.display = 'none';
            };
        });
        
        document.querySelector('.close-dropdown').onclick = () => {
            dropdown.style.display = 'none';
        };
    }

    addToMealPlan(mealName, mealType) {
        // Store in localStorage for now (would typically use backend)
        const currentWeek = 0; // Current week
        const today = new Date().getDay(); // 0 = Sunday, 1 = Monday, etc.
        const days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'];
        const targetDay = days[today];
        
        const weekKey = `week_${currentWeek}`;
        let mealPlan = JSON.parse(localStorage.getItem(`nomnomn_mealplan_${weekKey}`) || '{}');
        
        if (!mealPlan[targetDay]) mealPlan[targetDay] = {};
        mealPlan[targetDay][mealType] = {
            name: mealName,
            cookTime: '20'
        };
        
        localStorage.setItem(`nomnomn_mealplan_${weekKey}`, JSON.stringify(mealPlan));
        window.authManager?.showSuccessMessage(`${mealName} added to today's ${mealType}!`);
    }

    showLoginPrompt() {
        const modal = document.getElementById('login-prompt-modal');
        modal.style.display = 'flex';
        
        document.getElementById('go-to-login').onclick = () => {
            modal.style.display = 'none';
            window.authManager?.showSignInPage();
        };
        
        document.getElementById('close-login-modal').onclick = () => {
            modal.style.display = 'none';
        };
        
        // Close on backdrop click
        modal.onclick = (e) => {
            if (e.target === modal) {
                modal.style.display = 'none';
            }
        };
    }

    setupRecipesFunctionality() {
        // Individual meal mode toggle
        const individualModeToggle = document.getElementById('individual-meal-mode');
        if (individualModeToggle) {
            individualModeToggle.addEventListener('change', (e) => {
                // Could add different behavior for individual meal mode
                if (e.target.checked) {
                    console.log('Individual meal mode enabled');
                } else {
                    console.log('Regular mode enabled');
                }
            });
        }
    }

    setupResizableDivider() {
        const divider = document.getElementById('chat-divider');
        const chatColumn = document.getElementById('chat-column');
        const recipesColumn = document.getElementById('recipes-column');
        let isResizing = false;
        let isMobile = window.innerWidth <= 768;

        // Check if mobile and adjust behavior
        window.addEventListener('resize', () => {
            isMobile = window.innerWidth <= 768;
            if (!isMobile) {
                // Reset to side-by-side layout
                chatColumn.style.width = '40%';
                recipesColumn.style.width = '60%';
                chatColumn.style.height = 'auto';
                recipesColumn.style.height = 'auto';
            }
        });

        // Desktop resizing (horizontal)
        divider.addEventListener('mousedown', (e) => {
            if (isMobile) return;
            isResizing = true;
            document.addEventListener('mousemove', handleDesktopResize);
            document.addEventListener('mouseup', stopResize);
            e.preventDefault();
        });

        // Mobile resizing (vertical) - touch events
        divider.addEventListener('touchstart', (e) => {
            if (!isMobile) return;
            isResizing = true;
            document.addEventListener('touchmove', handleMobileResize);
            document.addEventListener('touchend', stopResize);
            e.preventDefault();
        }, { passive: false });

        function handleDesktopResize(e) {
            if (!isResizing || isMobile) return;
            
            const containerWidth = divider.parentElement.offsetWidth;
            const newLeftWidth = (e.clientX / containerWidth) * 100;
            
            // Enforce constraints: chat column 25-75%, recipes column 25-75%
            const constrainedLeft = Math.max(25, Math.min(75, newLeftWidth));
            const constrainedRight = 100 - constrainedLeft;
            
            chatColumn.style.width = `${constrainedLeft}%`;
            recipesColumn.style.width = `${constrainedRight}%`;
        }

        function handleMobileResize(e) {
            if (!isResizing || !isMobile) return;
            
            const touch = e.touches[0];
            const containerHeight = divider.parentElement.offsetHeight;
            const newTopHeight = (touch.clientY / containerHeight) * 100;
            
            // Enforce constraints: each section 25-75%
            const constrainedTop = Math.max(25, Math.min(75, newTopHeight));
            const constrainedBottom = 100 - constrainedTop;
            
            chatColumn.style.height = `${constrainedTop}vh`;
            recipesColumn.style.height = `${constrainedBottom}vh`;
        }

        function stopResize() {
            isResizing = false;
            document.removeEventListener('mousemove', handleDesktopResize);
            document.removeEventListener('touchmove', handleMobileResize);
            document.removeEventListener('mouseup', stopResize);
            document.removeEventListener('touchend', stopResize);
        }

        // Close dropdowns when clicking outside
        document.addEventListener('click', (e) => {
            const dropdown = document.getElementById('meal-plan-dropdown');
            if (dropdown && !dropdown.contains(e.target) && !e.target.closest('.add-to-plan-btn')) {
                dropdown.style.display = 'none';
            }
        });
    }

    loadInitialRecipes() {
        // Display some sample recipes so users can see the interface working
        const sampleRecipes = [
            {
                name: "Quick Pasta with Tomato Sauce",
                cook_time_minutes: 15,
                ingredients: [
                    { ingredient_name: "pasta", quantity: 2 },
                    { ingredient_name: "tomato sauce", quantity: 1 },
                    { ingredient_name: "onion", quantity: 0.5 }
                ]
            },
            {
                name: "Scrambled Eggs & Toast",
                cook_time_minutes: 10,
                ingredients: [
                    { ingredient_name: "eggs", quantity: 3 },
                    { ingredient_name: "bread", quantity: 2 },
                    { ingredient_name: "butter", quantity: 1 }
                ]
            },
            {
                name: "Rice Bowl with Vegetables",
                cook_time_minutes: 20,
                ingredients: [
                    { ingredient_name: "rice", quantity: 1 },
                    { ingredient_name: "mixed vegetables", quantity: 1 },
                    { ingredient_name: "soy sauce", quantity: 0.5 }
                ]
            },
            {
                name: "Simple Chicken Sandwich",
                cook_time_minutes: 12,
                ingredients: [
                    { ingredient_name: "chicken breast", quantity: 1 },
                    { ingredient_name: "bread", quantity: 2 },
                    { ingredient_name: "lettuce", quantity: 1 }
                ]
            }
        ];
        
        this.displayRecipeResults(sampleRecipes);
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