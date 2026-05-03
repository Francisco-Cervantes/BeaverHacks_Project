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
        // Profile requires login
        if (page === 'profile' && !window.authManager.getIsLoggedIn()) {
            window.authManager.showAuthRequiredMessage('Profile');
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
            targetPage.classList.remove('hidden');
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
            
            // Send "start" to the server to get the personalized greeting
            setTimeout(() => {
                this.sendStartMessage();
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

    async sendStartMessage() {
        // Show a typing indicator while waiting for the server greeting
        const chatMessages = document.getElementById('chat-messages');
        if (!chatMessages) return;

        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot';
        typingDiv.id = 'chat-typing-indicator';
        typingDiv.innerHTML = '<i class="fas fa-ellipsis-h" style="color:#aaa;"></i>';
        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;

        try {
            const isLoggedIn = window.authManager?.getIsLoggedIn() || false;
            const username = window.authManager?.currentUser?.name || null;
            const zip = document.getElementById('zip-input')?.value || '00000';
            const radius = parseInt(document.getElementById('mile-range')?.value || '10');

            const payload = { message: 'start', logged_in: isLoggedIn, zip, radius };
            if (isLoggedIn && username) payload.username = username;

            const response = await fetch(`${window.apiManager.chatBaseURL}/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const data = await response.json();
            typingDiv.remove();
            this.addMessage(data.response || 'Hello! What would you like to cook today?', 'bot');
        } catch (e) {
            typingDiv.remove();
            // Fallback greeting if server is down
            const isLoggedIn = window.authManager?.getIsLoggedIn() || false;
            if (isLoggedIn) {
                const name = window.authManager?.currentUser?.name || 'there';
                this.addMessage(`Hello ${name}! What would you like to cook today?`, 'bot');
            } else {
                this.addMessage("Hello guest! Since you're not logged in, we'll jump straight into meal planning.\n\nWhat type of meals are you looking to prep?", 'bot');
            }
        }
    }

    async getBotResponse(userMessage) {
        try {
            // Use real API if available
            const response = await window.apiManager.sendChatMessage(userMessage, {
                current_page: 'chat',
                user_location: document.getElementById('zip-input')?.value || '97331'
            });
            this.addMessage(response, 'bot');
        } catch (error) {
            console.error('Chat API error:', error);
            // Fallback to local responses
            const localResponse = this.getLocalChatResponse(userMessage);
            this.addMessage(localResponse, 'bot');
        }
        
        // Trigger recipe search based on message
        await this.searchRecipes(userMessage);
    }

    getLocalChatResponse(userMessage) {
        const responses = {
            'budget': 'For budget-friendly meals, try our pasta dishes and rice bowls. They typically cost under $3 per serving!',
            'recipe': 'I can suggest recipes based on your preferences. What ingredients do you have available?',
            'meal plan': 'Meal planning saves time and money! Would you like me to help you create a weekly plan?',
            'grocery': 'Check our price comparison feature to find the best deals at nearby stores.',
            'cheap': 'Our cheapest meals include pasta with tomato sauce ($2.50) and scrambled eggs ($1.80).',
            'hello': 'Hello! I\'m your NomNomNomotron AI assistant. How can I help you with meal planning today?',
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
        
        return response;
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
        const favorites = JSON.parse(localStorage.getItem('recipe_favorites') || '[]');
        const isFav = favorites.includes(meal.name);
        const mealJson = JSON.stringify(JSON.stringify(meal));

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
                    <button class="make-it-btn btn btn-primary" data-meal-json="${mealJson.replace(/"/g, '&quot;')}">
                        <i class="fas fa-play"></i> Make It
                    </button>
                    <button class="chat-fav-btn ${isFav ? 'active' : ''}" data-meal="${meal.name.replace(/"/g, '&quot;')}" title="${isFav ? 'Remove from favourites' : 'Save to favourites'}">
                        <i class="fas fa-heart"></i>
                    </button>
                    <button class="add-to-plan-btn btn btn-success" data-meal="${meal.name.replace(/"/g, '&quot;')}" title="Add to meal plan">
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
        // Make It buttons — open recipe detail in Recipe tab
        document.querySelectorAll('.make-it-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const raw = e.target.closest('.make-it-btn').getAttribute('data-meal-json');
                try {
                    const meal = JSON.parse(raw);
                    this.openRecipe(meal);
                } catch (_) {}
            });
        });

        // Heart / favourite buttons — always available
        document.querySelectorAll('.chat-fav-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const b = e.target.closest('.chat-fav-btn');
                const mealName = b.getAttribute('data-meal');
                const favs = JSON.parse(localStorage.getItem('recipe_favorites') || '[]');
                const idx = favs.indexOf(mealName);
                if (idx === -1) {
                    favs.push(mealName);
                    b.classList.add('active');
                    b.title = 'Remove from favourites';
                    window.authManager?.showSuccessMessage(`${mealName} saved to favourites!`);
                } else {
                    favs.splice(idx, 1);
                    b.classList.remove('active');
                    b.title = 'Save to favourites';
                    window.authManager?.showInfoMessage(`${mealName} removed from favourites`);
                }
                localStorage.setItem('recipe_favorites', JSON.stringify(favs));
            });
        });

        // Add to plan buttons — open slot picker modal
        document.querySelectorAll('.add-to-plan-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const mealName = e.target.closest('.add-to-plan-btn').getAttribute('data-meal');
                if (window.authManager?.getIsLoggedIn()) {
                    this.showChatMealPlanPicker(mealName);
                } else {
                    this.showLoginPrompt();
                }
            });
        });
    }

    showChatMealPlanPicker(mealName) {
        // Remove any existing picker
        document.getElementById('chat-plan-picker')?.remove();

        const today = new Date();
        const DAY_NAMES   = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
        const MONTH_NAMES = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
        const MEAL_TYPES  = ['breakfast', 'lunch', 'dinner'];

        const days = Array.from({ length: 7 }, (_, i) => {
            const d = new Date(today);
            d.setDate(today.getDate() + i);
            return d;
        });

        const modal = document.createElement('div');
        modal.id = 'chat-plan-picker';
        modal.className = 'meal-picker-modal';
        modal.innerHTML = `
            <div class="meal-picker-backdrop"></div>
            <div class="meal-picker-dialog">
                <div class="meal-picker-header">
                    <h3><i class="fas fa-calendar-plus"></i> Add "${mealName}" to Meal Plan</h3>
                    <button class="meal-picker-close"><i class="fas fa-times"></i></button>
                </div>
                <div class="meal-picker-list">
                    ${days.map((day, i) => {
                        const dateKey = day.toISOString().split('T')[0];
                        const label = i === 0 ? 'Today' : i === 1 ? 'Tomorrow' : `${DAY_NAMES[day.getDay()]}, ${MONTH_NAMES[day.getMonth()]} ${day.getDate()}`;
                        return MEAL_TYPES.map(type => `
                            <button class="meal-picker-item" data-date="${dateKey}" data-type="${type}">
                                <span class="meal-picker-name">${label}</span>
                                <span class="meal-picker-meta">
                                    <i class="fas fa-${type === 'breakfast' ? 'sun' : type === 'lunch' ? 'cloud-sun' : 'moon'}"></i>
                                    ${type.charAt(0).toUpperCase() + type.slice(1)}
                                </span>
                            </button>
                        `).join('');
                    }).join('')}
                </div>
            </div>
        `;
        document.body.appendChild(modal);

        modal.querySelector('.meal-picker-close').addEventListener('click', () => modal.remove());
        modal.querySelector('.meal-picker-backdrop').addEventListener('click', () => modal.remove());
        modal.querySelectorAll('.meal-picker-item').forEach(btn => {
            btn.addEventListener('click', () => {
                this.saveMealToSlot(btn.dataset.date, btn.dataset.type, mealName);
                modal.remove();
                window.authManager?.showSuccessMessage(`${mealName} added to ${btn.dataset.type}!`);
            });
        });
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

    async loadInitialRecipes() {
        try {
            const meals = await window.apiManager.getMeals();
            this.displayRecipeResults(meals.slice(0, 6));
        } catch (e) {
            // Fallback to a minimal set so UI is never blank
            this.displayRecipeResults([
                { name: "Pasta with Tomato Sauce", cook_time_minutes: 15, equipment_required: ["stove"], ingredients: [{ ingredient_name: "pasta", quantity: 2 }, { ingredient_name: "tomato sauce", quantity: 1 }, { ingredient_name: "onion", quantity: 0.5 }] },
                { name: "Scrambled Eggs & Toast",  cook_time_minutes: 10, equipment_required: ["stove"], ingredients: [{ ingredient_name: "eggs", quantity: 3 }, { ingredient_name: "bread", quantity: 2 }, { ingredient_name: "butter", quantity: 1 }] },
                { name: "Rice Bowl with Vegetables", cook_time_minutes: 20, equipment_required: ["stove"], ingredients: [{ ingredient_name: "rice", quantity: 1 }, { ingredient_name: "mixed vegetables", quantity: 1 }, { ingredient_name: "soy sauce", quantity: 0.5 }] }
            ]);
        }
    }

    loadMealsPage() {
        const mealsPage = document.getElementById('meals-page');
        if (!mealsPage) return;

        // Build tab shell once; reload active tab every visit
        if (!mealsPage.hasAttribute('data-tab-shell')) {
            mealsPage.innerHTML = `
                <div class="meals-container">
                    <div class="meals-tab-bar">
                        <button class="meals-tab active" data-tab="meal-plan">
                            <i class="fas fa-calendar-week"></i> Meal Plan
                        </button>
                        <button class="meals-tab" data-tab="my-meals">
                            <i class="fas fa-heart"></i> My Meals
                        </button>
                        <button class="meals-tab" data-tab="browse">
                            <i class="fas fa-search"></i> Browse
                        </button>
                    </div>
                    <div id="meals-tab-content" class="meals-tab-content"></div>
                </div>
            `;
            mealsPage.setAttribute('data-tab-shell', 'true');

            mealsPage.querySelectorAll('.meals-tab').forEach(tab => {
                tab.addEventListener('click', () => {
                    mealsPage.querySelectorAll('.meals-tab').forEach(t => t.classList.remove('active'));
                    tab.classList.add('active');
                    this.loadMealsTab(tab.dataset.tab);
                });
            });
        }

        // Reload the currently active tab on every page visit
        const activeTab = mealsPage.querySelector('.meals-tab.active');
        this.loadMealsTab(activeTab ? activeTab.dataset.tab : 'meal-plan');
    }

    loadMealsTab(tab) {
        const content = document.getElementById('meals-tab-content');
        if (!content) return;
        if (tab === 'meal-plan') this.loadMealPlanTab(content);
        else if (tab === 'my-meals') this.loadMyMealsTab(content);
        else if (tab === 'browse') this.loadBrowseTab(content);
    }

    loadMealPlanTab(content) {
        const isLoggedIn = window.authManager && window.authManager.getIsLoggedIn();

        if (!isLoggedIn) {
            content.innerHTML = `
                <div class="meal-plan-guest">
                    <div class="meal-plan-guest-card">
                        <i class="fas fa-calendar-alt"></i>
                        <h2>Your Meal Plan</h2>
                        <p>Sign in to view and manage your personalized weekly meal plan with breakfast, lunch, and dinner for every day.</p>
                        <button class="btn btn-primary" style="justify-content:center;" onclick="window.authManager.showSignInPage()">
                            Sign In
                        </button>
                    </div>
                </div>
            `;
            return;
        }

        const schedule = JSON.parse(localStorage.getItem('meal_plan_schedule') || '{}');
        const today = new Date();
        const DAY_NAMES   = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
        const MONTH_NAMES = ['January','February','March','April','May','June','July','August','September','October','November','December'];
        const MEAL_TYPES  = ['breakfast', 'lunch', 'dinner'];
        const MEAL_ICONS  = { breakfast: 'fa-sun', lunch: 'fa-cloud-sun', dinner: 'fa-moon' };

        const days = Array.from({ length: 7 }, (_, i) => {
            const d = new Date(today);
            d.setDate(today.getDate() + i);
            return d;
        });

        const todayKey = today.toISOString().split('T')[0];

        content.innerHTML = `
            <div class="meal-plan-scroll">
                ${days.map(day => {
                    const dateKey = day.toISOString().split('T')[0];
                    const daySchedule = schedule[dateKey] || {};
                    const isToday = dateKey === todayKey;
                    const label = `${DAY_NAMES[day.getDay()]}, ${MONTH_NAMES[day.getMonth()]} ${day.getDate()}`;
                    return `
                        <div class="meal-plan-day${isToday ? ' today' : ''}">
                            <div class="meal-plan-day-header">
                                <span class="meal-plan-day-label">
                                    <i class="fas ${isToday ? 'fa-calendar-check' : 'fa-calendar'}"></i>
                                    ${isToday ? 'Today &mdash; ' : ''}${label}
                                </span>
                            </div>
                            <div class="meal-plan-day-cards">
                                ${MEAL_TYPES.map(type => {
                                    const meal = daySchedule[type] || null;
                                    return `
                                        <div class="meal-slot-card">
                                            <div class="meal-slot-label">
                                                <i class="fas ${MEAL_ICONS[type]}"></i>
                                                ${type.charAt(0).toUpperCase() + type.slice(1)}
                                            </div>
                                            ${meal ? `
                                                <div class="meal-slot-filled">
                                                    <span class="meal-slot-name">${meal}</span>
                                                    <div class="meal-slot-actions">
                                                        <button class="meal-slot-view-btn" title="View recipe"
                                                            onclick="window.navigationManager.openMealFromPlan('${meal.replace(/'/g, "\\'")}')">
                                                            <i class="fas fa-eye"></i>
                                                        </button>
                                                        <button class="meal-slot-remove-btn" title="Remove"
                                                            onclick="window.navigationManager.removeMealFromSlot('${dateKey}', '${type}')">
                                                            <i class="fas fa-times"></i>
                                                        </button>
                                                    </div>
                                                </div>
                                            ` : `
                                                <button class="meal-slot-add-btn"
                                                    onclick="window.navigationManager.pickMealForSlot('${dateKey}', '${type}')">
                                                    <i class="fas fa-plus"></i> Add meal
                                                </button>
                                            `}
                                        </div>
                                    `;
                                }).join('')}
                            </div>
                        </div>
                    `;
                }).join('')}
            </div>
        `;
    }

    async loadMyMealsTab(content) {
        content.innerHTML = `
            <div class="my-meals-container">
                <div class="my-meals-header">
                    <h2><i class="fas fa-heart"></i> My Meals</h2>
                    <p>Your saved favourite meals. Click any card to view the full recipe.</p>
                </div>
                <div id="my-meals-grid" class="my-meals-grid">
                    <div class="recipe-loading"><i class="fas fa-spinner fa-spin"></i> Loading...</div>
                </div>
            </div>
        `;

        const favorites = JSON.parse(localStorage.getItem('recipe_favorites') || '[]');
        const grid = document.getElementById('my-meals-grid');

        if (!favorites.length) {
            grid.innerHTML = `
                <div class="my-meals-empty">
                    <i class="fas fa-heart-broken"></i>
                    <p>No saved meals yet.</p>
                    <small>Open a recipe and tap the heart button to save it here.</small>
                </div>
            `;
            return;
        }

        try {
            const allMeals = await window.apiManager.getMeals();
            const favMeals = allMeals.filter(m => favorites.includes(m.name));
            if (!favMeals.length) {
                grid.innerHTML = `<div class="my-meals-empty"><i class="fas fa-heart-broken"></i><p>None of your saved meals were found.</p></div>`;
                return;
            }
            grid.innerHTML = favMeals.map(meal => `
                <div class="my-meal-card" onclick="window.navigationManager.openRecipe(${JSON.stringify(JSON.stringify(meal))})">
                    <div class="my-meal-img">
                        <img src="https://source.unsplash.com/300x200/?${encodeURIComponent(meal.name)},food"
                             onerror="this.src='https://via.placeholder.com/300x200/76b900/ffffff?text=${encodeURIComponent(meal.name)}'"
                             alt="${meal.name}">
                        <div class="my-meal-fav-badge"><i class="fas fa-heart"></i></div>
                    </div>
                    <div class="my-meal-info">
                        <h3>${meal.name}</h3>
                        <div class="my-meal-meta">
                            <span><i class="fas fa-clock"></i> ${meal.cook_time_minutes} min</span>
                            <span><i class="fas fa-list"></i> ${meal.ingredients.length} ingredients</span>
                        </div>
                    </div>
                </div>
            `).join('');
        } catch (e) {
            grid.innerHTML = `<p style="color:#666;padding:20px">Could not load meals. Make sure the meals backend is running.</p>`;
        }
    }

    loadBrowseTab(content) {
        content.innerHTML = `
            <div class="browse-container">
                <div class="browse-header">
                    <h2><i class="fas fa-search"></i> Browse Meals</h2>
                    <div class="browse-filters">
                        <select id="time-filter" class="browse-select">
                            <option value="">Any cooking time</option>
                            <option value="15">Under 15 min</option>
                            <option value="30">Under 30 min</option>
                            <option value="60">Under 1 hour</option>
                        </select>
                        <select id="equipment-filter" class="browse-select">
                            <option value="">Any equipment</option>
                            <option value="stove">Stove</option>
                            <option value="oven">Oven</option>
                            <option value="microwave">Microwave</option>
                        </select>
                        <button id="apply-filters" class="btn btn-primary">Apply Filters</button>
                    </div>
                </div>
                <div id="meals-grid" class="browse-grid">
                    <div class="recipe-loading"><i class="fas fa-spinner fa-spin"></i> Loading meals...</div>
                </div>
            </div>
        `;
        this.loadMealsData();
        this.setupMealsFilters();
    }

    async pickMealForSlot(dateKey, type) {
        let allMeals;
        try {
            allMeals = await window.apiManager.getMeals();
        } catch (e) {
            window.authManager.showInfoMessage('Could not load meals. Make sure the backend is running.');
            return;
        }

        const modal = document.createElement('div');
        modal.className = 'meal-picker-modal';
        modal.innerHTML = `
            <div class="meal-picker-backdrop"></div>
            <div class="meal-picker-dialog">
                <div class="meal-picker-header">
                    <h3>Add ${type.charAt(0).toUpperCase() + type.slice(1)}</h3>
                    <button class="meal-picker-close"><i class="fas fa-times"></i></button>
                </div>
                <div class="meal-picker-list">
                    ${allMeals.map(meal => `
                        <button class="meal-picker-item" data-name="${meal.name.replace(/"/g, '&quot;')}">
                            <span class="meal-picker-name">${meal.name}</span>
                            <span class="meal-picker-meta"><i class="fas fa-clock"></i> ${meal.cook_time_minutes} min</span>
                        </button>
                    `).join('')}
                </div>
            </div>
        `;

        document.body.appendChild(modal);
        modal.querySelector('.meal-picker-close').addEventListener('click', () => modal.remove());
        modal.querySelector('.meal-picker-backdrop').addEventListener('click', () => modal.remove());
        modal.querySelectorAll('.meal-picker-item').forEach(btn => {
            btn.addEventListener('click', () => {
                this.saveMealToSlot(dateKey, type, btn.dataset.name);
                modal.remove();
            });
        });
    }

    saveMealToSlot(dateKey, type, mealName) {
        const schedule = JSON.parse(localStorage.getItem('meal_plan_schedule') || '{}');
        if (!schedule[dateKey]) schedule[dateKey] = {};
        schedule[dateKey][type] = mealName;
        localStorage.setItem('meal_plan_schedule', JSON.stringify(schedule));
        const content = document.getElementById('meals-tab-content');
        if (content) this.loadMealPlanTab(content);
    }

    removeMealFromSlot(dateKey, type) {
        const schedule = JSON.parse(localStorage.getItem('meal_plan_schedule') || '{}');
        if (schedule[dateKey]) delete schedule[dateKey][type];
        localStorage.setItem('meal_plan_schedule', JSON.stringify(schedule));
        const content = document.getElementById('meals-tab-content');
        if (content) this.loadMealPlanTab(content);
    }

    async openMealFromPlan(mealName) {
        try {
            const allMeals = await window.apiManager.getMeals();
            const meal = allMeals.find(m => m.name === mealName);
            if (meal) this.openRecipe(meal);
        } catch (e) {
            console.error('Could not open meal', e);
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
            <div class="browse-meal-card" onclick="window.navigationManager.openRecipe(${JSON.stringify(JSON.stringify(meal))})">
                <div class="browse-meal-img">
                    <img src="https://source.unsplash.com/300x200/?${encodeURIComponent(meal.name)},food"
                         onerror="this.src='https://via.placeholder.com/300x200/76b900/ffffff?text=${encodeURIComponent(meal.name)}'"
                         alt="${meal.name}">
                </div>
                <div class="browse-meal-info">
                    <h3>${meal.name}</h3>
                    <div class="browse-meal-meta">
                        <span><i class="fas fa-clock"></i> ${meal.cook_time_minutes} min</span>
                        <span><i class="fas fa-tools"></i> ${meal.equipment_required.join(', ')}</span>
                    </div>
                    <p class="browse-meal-ingredients">${meal.ingredients.slice(0, 3).map(i => i.ingredient_name).join(', ')}${meal.ingredients.length > 3 ? '…' : ''}</p>
                    <div class="btn btn-primary" style="width:100%;text-align:center;margin-top:10px;">View Recipe</div>
                </div>
            </div>
        `).join('');

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
        const recipesPage = document.getElementById('recipes-page');
        if (!recipesPage) return;

        // If we have a recipe queued to display, show it
        const queued = window._pendingRecipe || JSON.parse(localStorage.getItem('currentRecipe') || 'null');
        window._pendingRecipe = null;

        if (queued) {
            this.renderRecipeDetail(recipesPage, queued);
        } else {
            // Otherwise show a browseable grid
            recipesPage.innerHTML = `
                <div class="recipe-browse">
                    <div class="recipe-browse-header">
                        <h1><i class="fas fa-book-open"></i> Recipe</h1>
                        <p>Select a meal from the chat or meals page, or browse below</p>
                    </div>
                    <div id="recipe-browse-grid" class="recipe-browse-grid">
                        <div class="recipe-loading"><i class="fas fa-spinner fa-spin"></i> Loading...</div>
                    </div>
                </div>
            `;
            this.loadRecipeBrowseGrid();
        }
    }

    async loadRecipeBrowseGrid() {
        const grid = document.getElementById('recipe-browse-grid');
        if (!grid) return;
        try {
            const meals = await window.apiManager.getMeals();
            grid.innerHTML = meals.map(meal => `
                <div class="recipe-browse-card" onclick="window.navigationManager.openRecipe(${JSON.stringify(JSON.stringify(meal))})">
                    <div class="recipe-browse-img">
                        <img src="https://source.unsplash.com/300x200/?${encodeURIComponent(meal.name)},food"
                             onerror="this.src='https://via.placeholder.com/300x200/76b900/ffffff?text=${encodeURIComponent(meal.name)}'"
                             alt="${meal.name}">
                    </div>
                    <div class="recipe-browse-info">
                        <h3>${meal.name}</h3>
                        <span><i class="fas fa-clock"></i> ${meal.cook_time_minutes} min</span>
                        <span><i class="fas fa-list"></i> ${meal.ingredients.length} ingredients</span>
                    </div>
                </div>
            `).join('');
        } catch (e) {
            grid.innerHTML = '<p style="color:#666;padding:20px">Could not load recipes. Make sure the meals backend is running.</p>';
        }
    }

    openRecipe(mealJson) {
        const meal = typeof mealJson === 'string' ? JSON.parse(mealJson) : mealJson;
        localStorage.setItem('currentRecipe', JSON.stringify(meal));
        window._pendingRecipe = meal;
        const recipesPage = document.getElementById('recipes-page');
        if (recipesPage) {
            recipesPage.removeAttribute('data-loaded');
            this.renderRecipeDetail(recipesPage, meal);
        }
        this.showPage('recipes', true);
    }

    renderRecipeDetail(container, meal) {
        const favorites = JSON.parse(localStorage.getItem('recipe_favorites') || '[]');
        const isFav = favorites.includes(meal.name);
        const instructions = this.generateInstructions(meal);

        container.innerHTML = `
            <div class="recipe-page">

                <!-- Back button -->
                <button class="recipe-back-btn" onclick="window.navigationManager.clearRecipeAndBrowse()">
                    <i class="fas fa-arrow-left"></i> Back to Recipes
                </button>

                <div class="recipe-layout">

                    <!-- LEFT: Image + meta + actions -->
                    <div class="recipe-left">
                        <div class="recipe-image-wrap">
                            <img
                                src="https://source.unsplash.com/500x380/?${encodeURIComponent(meal.name)},food"
                                onerror="this.src='https://via.placeholder.com/500x380/76b900/ffffff?text=${encodeURIComponent(meal.name)}'"
                                alt="${meal.name}"
                                class="recipe-main-img"
                            >
                        </div>

                        <div class="recipe-meta-bar">
                            <div class="recipe-meta-item">
                                <i class="fas fa-clock"></i>
                                <span>${meal.cook_time_minutes} min</span>
                                <small>Cook Time</small>
                            </div>
                            <div class="recipe-meta-item">
                                <i class="fas fa-utensils"></i>
                                <span>${meal.ingredients.length}</span>
                                <small>Ingredients</small>
                            </div>
                            <div class="recipe-meta-item">
                                <i class="fas fa-tools"></i>
                                <span>${meal.equipment_required.length}</span>
                                <small>Tools</small>
                            </div>
                        </div>

                        <div class="recipe-action-btns">
                            <button class="recipe-action-btn recipe-fav-btn ${isFav ? 'active' : ''}"
                                    id="fav-btn"
                                    onclick="window.navigationManager.toggleFavorite('${meal.name.replace(/'/g, "\\'")}')">
                                <i class="fas fa-heart"></i>
                                <span>${isFav ? 'Saved to Favorites' : 'Save to Favorites'}</span>
                            </button>
                            <button class="recipe-action-btn recipe-plan-btn"
                                    onclick="window.navigationManager.addToMealPlan('${meal.name.replace(/'/g, "\\'")}')">
                                <i class="fas fa-calendar-plus"></i>
                                <span>Save to Meal Plan</span>
                            </button>
                        </div>
                    </div>

                    <!-- RIGHT: Title + ingredients + tools + instructions -->
                    <div class="recipe-right">
                        <h1 class="recipe-title">${meal.name}</h1>

                        <div class="recipe-section">
                            <h2><i class="fas fa-shopping-basket"></i> Ingredients</h2>
                            <ul class="recipe-ingredients-list">
                                ${meal.ingredients.map(ing => `
                                    <li>
                                        <span class="ing-name">${ing.ingredient_name}</span>
                                        <span class="ing-amount">${ing.quantity} ${ing.unit}</span>
                                    </li>
                                `).join('')}
                            </ul>
                        </div>

                        <div class="recipe-section">
                            <h2><i class="fas fa-tools"></i> Tools Needed</h2>
                            <div class="recipe-tools">
                                ${meal.equipment_required.map(eq => `
                                    <span class="recipe-tool-tag"><i class="fas fa-check-circle"></i> ${eq}</span>
                                `).join('')}
                            </div>
                        </div>

                        <div class="recipe-section">
                            <h2><i class="fas fa-list-ol"></i> Instructions</h2>
                            <ol class="recipe-steps">
                                ${instructions.map(step => `<li>${step}</li>`).join('')}
                            </ol>
                        </div>
                    </div>

                </div>
            </div>
        `;
        container.setAttribute('data-loaded', 'true');
    }

    clearRecipeAndBrowse() {
        localStorage.removeItem('currentRecipe');
        window._pendingRecipe = null;
        const recipesPage = document.getElementById('recipes-page');
        if (recipesPage) recipesPage.removeAttribute('data-loaded');
        this.loadRecipesPage();
    }

    toggleFavorite(mealName) {
        const favorites = JSON.parse(localStorage.getItem('recipe_favorites') || '[]');
        const idx = favorites.indexOf(mealName);
        if (idx === -1) {
            favorites.push(mealName);
        } else {
            favorites.splice(idx, 1);
        }
        localStorage.setItem('recipe_favorites', JSON.stringify(favorites));

        const btn = document.getElementById('fav-btn');
        if (btn) {
            const isFav = favorites.includes(mealName);
            btn.classList.toggle('active', isFav);
            btn.querySelector('span').textContent = isFav ? 'Saved to Favorites' : 'Save to Favorites';
        }
    }

    generateInstructions(meal) {
        const name = meal.name.toLowerCase();
        const ingredients = meal.ingredients.map(i => i.ingredient_name);
        const hasStove = meal.equipment_required.some(e => e.toLowerCase().includes('stove'));
        const hasMicrowave = meal.equipment_required.some(e => e.toLowerCase().includes('microwave'));
        const hasOven = meal.equipment_required.some(e => e.toLowerCase().includes('oven'));

        const steps = [`Gather all ingredients: ${ingredients.join(', ')}.`];

        if (name.includes('pasta')) {
            steps.push(
                'Bring a large pot of salted water to a boil.',
                'Add pasta and cook per package directions until al dente.',
                'While pasta cooks, heat olive oil in a pan over medium heat.',
                'Sauté onion and garlic until softened (about 3 minutes).',
                'Add canned tomatoes and simmer for 10 minutes, season with salt and pepper.',
                'Drain pasta and toss with sauce.',
                'Serve immediately, optionally topped with cheese.'
            );
        } else if (name.includes('rice') || name.includes('bowl')) {
            steps.push(
                'Rinse rice under cold water until it runs clear.',
                'Cook rice in a pot with 2 cups of water per 1 cup of rice — bring to boil then simmer covered for 18 minutes.',
                'While rice cooks, prepare your protein and vegetables.',
                'Heat oil in a pan, cook protein until fully cooked through.',
                'Add vegetables and stir-fry for 3–4 minutes.',
                'Season with soy sauce or your preferred seasoning.',
                'Serve protein and vegetables over rice.'
            );
        } else if (name.includes('egg') || name.includes('scramble')) {
            steps.push(
                'Crack eggs into a bowl and whisk until combined.',
                'Heat a non-stick pan over medium-low heat and add butter or oil.',
                'Pour in eggs and gently stir with a spatula as they cook.',
                'Remove from heat while still slightly wet — residual heat will finish them.',
                'Season with salt and pepper and serve immediately.'
            );
        } else if (name.includes('sandwich') || name.includes('wrap')) {
            steps.push(
                'Lay out your bread or wrap on a clean surface.',
                'Spread any sauces or condiments evenly.',
                'Layer your fillings — proteins first, then vegetables.',
                'Close and press gently. Cut in half if desired.',
                'Serve immediately or wrap tightly for later.'
            );
        } else if (name.includes('stir') || name.includes('fry')) {
            steps.push(
                'Prep all vegetables and proteins — cut into uniform bite-sized pieces.',
                'Heat oil in a wok or large pan over high heat until shimmering.',
                'Add proteins first and cook until browned. Remove and set aside.',
                'Add vegetables to the hot pan, starting with the firmest ones.',
                'Return protein to the pan, add sauce and toss everything together.',
                'Cook for 1–2 more minutes until sauce coats everything.',
                'Serve immediately over rice or noodles.'
            );
        } else if (name.includes('mac') || name.includes('cheese')) {
            steps.push(
                hasMicrowave
                    ? 'Pour mac and cheese into a microwave-safe bowl. Add water as directed.'
                    : 'Bring a pot of water to boil and cook pasta until tender.',
                hasMicrowave
                    ? 'Microwave on high for 3–4 minutes, stir halfway through.'
                    : 'Drain pasta and return to pot.',
                'Stir in the cheese sauce packet with a splash of milk and butter.',
                'Mix until creamy and serve hot.'
            );
        } else if (hasOven) {
            steps.push(
                'Preheat oven to 375°F (190°C).',
                'Prepare all ingredients and arrange in a baking dish.',
                'Season generously with salt, pepper, and any desired spices.',
                'Bake for the recommended time, checking occasionally.',
                'Remove when golden and cooked through. Let rest 5 minutes before serving.'
            );
        } else {
            steps.push(
                `Prepare all ${meal.ingredients.length} ingredients — wash, chop, and measure as needed.`,
                hasStove ? 'Heat your pan or pot over medium heat.' : 'Set up your equipment.',
                'Combine ingredients in the order that requires the longest cooking time first.',
                'Cook until everything is fully heated and well combined.',
                'Season to taste with salt and pepper before serving.'
            );
        }

        return steps;
    }

    addToMealPlan(mealName) {
        const saved = JSON.parse(localStorage.getItem('meal_plan') || '[]');
        if (!saved.includes(mealName)) {
            saved.push(mealName);
            localStorage.setItem('meal_plan', JSON.stringify(saved));
        }
        window.authManager.showSuccessMessage(`${mealName} saved to your meal plan!`);
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