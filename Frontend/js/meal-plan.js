// Meal planning page functionality
function loadMealPlanPage() {
    const mealPlanPage = document.getElementById('meal-plan-page');
    if (mealPlanPage && !mealPlanPage.hasAttribute('data-loaded')) {
        mealPlanPage.innerHTML = `
            <div class="meal-plan-container">
                <div class="meal-plan-header">
                    <h1><i class="fas fa-calendar-alt"></i> Your Weekly Meal Plan</h1>
                    <p>Plan your meals for the week and create smart shopping lists</p>
                    
                    <div class="week-navigation">
                        <button id="prev-week" class="btn btn-secondary">
                            <i class="fas fa-chevron-left"></i> Previous Week
                        </button>
                        <h3 id="current-week-display">Week of March 3, 2024</h3>
                        <button id="next-week" class="btn btn-secondary">
                            Next Week <i class="fas fa-chevron-right"></i>
                        </button>
                    </div>
                </div>

                <div class="meal-plan-controls" style="margin-bottom: 30px; text-align: center;">
                    <button id="auto-fill-week" class="btn btn-primary" style="margin-right: 15px;">
                        <i class="fas fa-magic"></i> Auto-Fill Week
                    </button>
                    <button id="generate-shopping-list" class="btn btn-success" style="margin-right: 15px;">
                        <i class="fas fa-shopping-cart"></i> Generate Shopping List
                    </button>
                    <button id="clear-week" class="btn btn-secondary">
                        <i class="fas fa-trash"></i> Clear Week
                    </button>
                </div>

                <div class="meal-plan-week">
                    <!-- Monday -->
                    <div class="day-column">
                        <h3>Monday</h3>
                        <div class="day-date" id="monday-date">Mar 3</div>
                        <div class="meals-column">
                            <div class="meal-slot" data-day="monday" data-meal="breakfast">
                                <div class="meal-label">Breakfast</div>
                                <div class="meal-content">
                                    <i class="fas fa-plus add-meal-btn"></i>
                                    <span class="meal-placeholder">Add meal</span>
                                </div>
                            </div>
                            <div class="meal-slot" data-day="monday" data-meal="lunch">
                                <div class="meal-label">Lunch</div>
                                <div class="meal-content">
                                    <i class="fas fa-plus add-meal-btn"></i>
                                    <span class="meal-placeholder">Add meal</span>
                                </div>
                            </div>
                            <div class="meal-slot" data-day="monday" data-meal="dinner">
                                <div class="meal-label">Dinner</div>
                                <div class="meal-content">
                                    <i class="fas fa-plus add-meal-btn"></i>
                                    <span class="meal-placeholder">Add meal</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Tuesday -->
                    <div class="day-column">
                        <h3>Tuesday</h3>
                        <div class="day-date" id="tuesday-date">Mar 4</div>
                        <div class="meals-column">
                            <div class="meal-slot" data-day="tuesday" data-meal="breakfast">
                                <div class="meal-label">Breakfast</div>
                                <div class="meal-content">
                                    <i class="fas fa-plus add-meal-btn"></i>
                                    <span class="meal-placeholder">Add meal</span>
                                </div>
                            </div>
                            <div class="meal-slot" data-day="tuesday" data-meal="lunch">
                                <div class="meal-label">Lunch</div>
                                <div class="meal-content">
                                    <i class="fas fa-plus add-meal-btn"></i>
                                    <span class="meal-placeholder">Add meal</span>
                                </div>
                            </div>
                            <div class="meal-slot" data-day="tuesday" data-meal="dinner">
                                <div class="meal-label">Dinner</div>
                                <div class="meal-content">
                                    <i class="fas fa-plus add-meal-btn"></i>
                                    <span class="meal-placeholder">Add meal</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Wednesday -->
                    <div class="day-column">
                        <h3>Wednesday</h3>
                        <div class="day-date" id="wednesday-date">Mar 5</div>
                        <div class="meals-column">
                            <div class="meal-slot" data-day="wednesday" data-meal="breakfast">
                                <div class="meal-label">Breakfast</div>
                                <div class="meal-content">
                                    <i class="fas fa-plus add-meal-btn"></i>
                                    <span class="meal-placeholder">Add meal</span>
                                </div>
                            </div>
                            <div class="meal-slot" data-day="wednesday" data-meal="lunch">
                                <div class="meal-label">Lunch</div>
                                <div class="meal-content">
                                    <i class="fas fa-plus add-meal-btn"></i>
                                    <span class="meal-placeholder">Add meal</span>
                                </div>
                            </div>
                            <div class="meal-slot" data-day="wednesday" data-meal="dinner">
                                <div class="meal-label">Dinner</div>
                                <div class="meal-content">
                                    <i class="fas fa-plus add-meal-btn"></i>
                                    <span class="meal-placeholder">Add meal</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Thursday -->
                    <div class="day-column">
                        <h3>Thursday</h3>
                        <div class="day-date" id="thursday-date">Mar 6</div>
                        <div class="meals-column">
                            <div class="meal-slot" data-day="thursday" data-meal="breakfast">
                                <div class="meal-label">Breakfast</div>
                                <div class="meal-content">
                                    <i class="fas fa-plus add-meal-btn"></i>
                                    <span class="meal-placeholder">Add meal</span>
                                </div>
                            </div>
                            <div class="meal-slot" data-day="thursday" data-meal="lunch">
                                <div class="meal-label">Lunch</div>
                                <div class="meal-content">
                                    <i class="fas fa-plus add-meal-btn"></i>
                                    <span class="meal-placeholder">Add meal</span>
                                </div>
                            </div>
                            <div class="meal-slot" data-day="thursday" data-meal="dinner">
                                <div class="meal-label">Dinner</div>
                                <div class="meal-content">
                                    <i class="fas fa-plus add-meal-btn"></i>
                                    <span class="meal-placeholder">Add meal</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Friday -->
                    <div class="day-column">
                        <h3>Friday</h3>
                        <div class="day-date" id="friday-date">Mar 7</div>
                        <div class="meals-column">
                            <div class="meal-slot" data-day="friday" data-meal="breakfast">
                                <div class="meal-label">Breakfast</div>
                                <div class="meal-content">
                                    <i class="fas fa-plus add-meal-btn"></i>
                                    <span class="meal-placeholder">Add meal</span>
                                </div>
                            </div>
                            <div class="meal-slot" data-day="friday" data-meal="lunch">
                                <div class="meal-label">Lunch</div>
                                <div class="meal-content">
                                    <i class="fas fa-plus add-meal-btn"></i>
                                    <span class="meal-placeholder">Add meal</span>
                                </div>
                            </div>
                            <div class="meal-slot" data-day="friday" data-meal="dinner">
                                <div class="meal-label">Dinner</div>
                                <div class="meal-content">
                                    <i class="fas fa-plus add-meal-btn"></i>
                                    <span class="meal-placeholder">Add meal</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Saturday -->
                    <div class="day-column">
                        <h3>Saturday</h3>
                        <div class="day-date" id="saturday-date">Mar 8</div>
                        <div class="meals-column">
                            <div class="meal-slot" data-day="saturday" data-meal="breakfast">
                                <div class="meal-label">Breakfast</div>
                                <div class="meal-content">
                                    <i class="fas fa-plus add-meal-btn"></i>
                                    <span class="meal-placeholder">Add meal</span>
                                </div>
                            </div>
                            <div class="meal-slot" data-day="saturday" data-meal="lunch">
                                <div class="meal-label">Lunch</div>
                                <div class="meal-content">
                                    <i class="fas fa-plus add-meal-btn"></i>
                                    <span class="meal-placeholder">Add meal</span>
                                </div>
                            </div>
                            <div class="meal-slot" data-day="saturday" data-meal="dinner">
                                <div class="meal-label">Dinner</div>
                                <div class="meal-content">
                                    <i class="fas fa-plus add-meal-btn"></i>
                                    <span class="meal-placeholder">Add meal</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Sunday -->
                    <div class="day-column">
                        <h3>Sunday</h3>
                        <div class="day-date" id="sunday-date">Mar 9</div>
                        <div class="meals-column">
                            <div class="meal-slot" data-day="sunday" data-meal="breakfast">
                                <div class="meal-label">Breakfast</div>
                                <div class="meal-content">
                                    <i class="fas fa-plus add-meal-btn"></i>
                                    <span class="meal-placeholder">Add meal</span>
                                </div>
                            </div>
                            <div class="meal-slot" data-day="sunday" data-meal="lunch">
                                <div class="meal-label">Lunch</div>
                                <div class="meal-content">
                                    <i class="fas fa-plus add-meal-btn"></i>
                                    <span class="meal-placeholder">Add meal</span>
                                </div>
                            </div>
                            <div class="meal-slot" data-day="sunday" data-meal="dinner">
                                <div class="meal-label">Dinner</div>
                                <div class="meal-content">
                                    <i class="fas fa-plus add-meal-btn"></i>
                                    <span class="meal-placeholder">Add meal</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Weekly Summary -->
                <div class="weekly-summary" style="margin-top: 40px; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 5px 15px rgba(0,0,0,0.1);">
                    <h3><i class="fas fa-chart-line"></i> Weekly Summary</h3>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-top: 20px;">
                        <div class="summary-card">
                            <div style="font-size: 2rem; color: #007bff;"><i class="fas fa-utensils"></i></div>
                            <div style="font-size: 1.5rem; font-weight: bold;" id="total-meals">0</div>
                            <div style="color: #666;">Planned Meals</div>
                        </div>
                        <div class="summary-card">
                            <div style="font-size: 2rem; color: #28a745;"><i class="fas fa-dollar-sign"></i></div>
                            <div style="font-size: 1.5rem; font-weight: bold;" id="estimated-cost">$0.00</div>
                            <div style="color: #666;">Estimated Cost</div>
                        </div>
                        <div class="summary-card">
                            <div style="font-size: 2rem; color: #ffc107;"><i class="fas fa-shopping-cart"></i></div>
                            <div style="font-size: 1.5rem; font-weight: bold;" id="total-ingredients">0</div>
                            <div style="color: #666;">Unique Ingredients</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Meal Selection Modal -->
            <div id="meal-selection-modal" class="modal" style="display: none;">
                <div class="modal-content">
                    <div class="modal-header">
                        <h3>Choose a Meal</h3>
                        <span class="modal-close">&times;</span>
                    </div>
                    <div class="modal-body">
                        <div class="meal-search">
                            <input type="text" id="meal-search" placeholder="Search meals..." style="width: 100%; padding: 10px; margin-bottom: 20px; border: 2px solid #e0e0e0; border-radius: 6px;">
                        </div>
                        <div id="available-meals-list">
                            <!-- Meals will be loaded here -->
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        setupMealPlanFunctionality();
        loadMealPlanData();
        updateWeekDisplay();
        mealPlanPage.setAttribute('data-loaded', 'true');
    }
}

let currentWeekOffset = 0;
let mealPlanData = {};

function setupMealPlanFunctionality() {
    // Week navigation
    document.getElementById('prev-week')?.addEventListener('click', () => {
        currentWeekOffset--;
        updateWeekDisplay();
        loadMealPlanData();
    });

    document.getElementById('next-week')?.addEventListener('click', () => {
        currentWeekOffset++;
        updateWeekDisplay();
        loadMealPlanData();
    });

    // Control buttons
    document.getElementById('auto-fill-week')?.addEventListener('click', autoFillWeek);
    document.getElementById('generate-shopping-list')?.addEventListener('click', generateShoppingList);
    document.getElementById('clear-week')?.addEventListener('click', clearWeek);

    // Meal slot clicks
    document.querySelectorAll('.meal-slot').forEach(slot => {
        slot.addEventListener('click', () => showMealSelectionModal(slot));
    });

    // Modal functionality
    setupMealSelectionModal();
}

function updateWeekDisplay() {
    const today = new Date();
    const mondayDate = new Date(today);
    mondayDate.setDate(today.getDate() - today.getDay() + 1 + (currentWeekOffset * 7));

    const weekDisplay = document.getElementById('current-week-display');
    if (weekDisplay) {
        const options = { month: 'long', day: 'numeric', year: 'numeric' };
        weekDisplay.textContent = `Week of ${mondayDate.toLocaleDateString('en-US', options)}`;
    }

    // Update individual day dates
    const days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];
    days.forEach((day, index) => {
        const dayDate = new Date(mondayDate);
        dayDate.setDate(mondayDate.getDate() + index);
        
        const dateElement = document.getElementById(`${day}-date`);
        if (dateElement) {
            dateElement.textContent = `${dayDate.getMonth() + 1}/${dayDate.getDate()}`;
        }
    });
}

function loadMealPlanData() {
    const weekKey = `week_${currentWeekOffset}`;
    const savedPlan = localStorage.getItem(`nomnomn_mealplan_${weekKey}`);
    
    if (savedPlan) {
        mealPlanData = JSON.parse(savedPlan);
        displayMealPlan();
    } else {
        mealPlanData = {};
        clearMealPlanDisplay();
    }
    
    updateWeeklySummary();
}

function saveMealPlanData() {
    const weekKey = `week_${currentWeekOffset}`;
    localStorage.setItem(`nomnomn_mealplan_${weekKey}`, JSON.stringify(mealPlanData));
    updateWeeklySummary();
}

function displayMealPlan() {
    const days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];
    const meals = ['breakfast', 'lunch', 'dinner'];

    days.forEach(day => {
        meals.forEach(meal => {
            const slot = document.querySelector(`[data-day="${day}"][data-meal="${meal}"]`);
            const mealData = mealPlanData[day]?.[meal];
            
            if (slot && mealData) {
                const content = slot.querySelector('.meal-content');
                content.innerHTML = `
                    <div class="assigned-meal">
                        <div class="meal-name">${mealData.name}</div>
                        <div class="meal-time">${mealData.cookTime || '20'} min</div>
                        <button class="remove-meal" onclick="removeMeal('${day}', '${meal}')">&times;</button>
                    </div>
                `;
                slot.classList.add('filled');
            }
        });
    });
}

function clearMealPlanDisplay() {
    document.querySelectorAll('.meal-slot').forEach(slot => {
        const content = slot.querySelector('.meal-content');
        content.innerHTML = `
            <i class="fas fa-plus add-meal-btn"></i>
            <span class="meal-placeholder">Add meal</span>
        `;
        slot.classList.remove('filled');
    });
}

function showMealSelectionModal(slot) {
    const day = slot.getAttribute('data-day');
    const meal = slot.getAttribute('data-meal');
    
    const modal = document.getElementById('meal-selection-modal');
    modal.style.display = 'block';
    modal.setAttribute('data-target-day', day);
    modal.setAttribute('data-target-meal', meal);
    
    loadAvailableMeals();
}

function setupMealSelectionModal() {
    const modal = document.getElementById('meal-selection-modal');
    const closeBtn = modal.querySelector('.modal-close');

    closeBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });

    const searchInput = document.getElementById('meal-search');
    searchInput.addEventListener('input', filterAvailableMeals);
}

async function loadAvailableMeals() {
    try {
        const meals = await window.apiManager.getMeals();
        displayAvailableMeals(meals);
    } catch (error) {
        console.error('Error loading meals:', error);
    }
}

function displayAvailableMeals(meals) {
    const container = document.getElementById('available-meals-list');
    container.innerHTML = meals.map(meal => `
        <div class="modal-meal-option" onclick="selectMeal('${meal.name}')">
            <div class="meal-info">
                <div class="meal-name">${meal.name}</div>
                <div class="meal-details">${meal.cook_time_minutes} min • ${meal.ingredients.length} ingredients</div>
            </div>
            <div class="meal-icon">
                <i class="fas fa-utensils"></i>
            </div>
        </div>
    `).join('');
}

function filterAvailableMeals() {
    const searchTerm = document.getElementById('meal-search').value.toLowerCase();
    const options = document.querySelectorAll('.modal-meal-option');
    
    options.forEach(option => {
        const mealName = option.querySelector('.meal-name').textContent.toLowerCase();
        if (mealName.includes(searchTerm)) {
            option.style.display = 'block';
        } else {
            option.style.display = 'none';
        }
    });
}

function selectMeal(mealName) {
    const modal = document.getElementById('meal-selection-modal');
    const day = modal.getAttribute('data-target-day');
    const meal = modal.getAttribute('data-target-meal');
    
    // Initialize day object if it doesn't exist
    if (!mealPlanData[day]) {
        mealPlanData[day] = {};
    }
    
    // Add meal to plan
    mealPlanData[day][meal] = {
        name: mealName,
        cookTime: '20' // Default, would get from meal data
    };
    
    saveMealPlanData();
    displayMealPlan();
    
    modal.style.display = 'none';
    window.authManager.showSuccessMessage(`${mealName} added to ${day} ${meal}!`);
}

function removeMeal(day, meal) {
    if (mealPlanData[day] && mealPlanData[day][meal]) {
        delete mealPlanData[day][meal];
        
        // Clean up empty day objects
        if (Object.keys(mealPlanData[day]).length === 0) {
            delete mealPlanData[day];
        }
        
        saveMealPlanData();
        displayMealPlan();
    }
}

async function autoFillWeek() {
    try {
        const meals = await window.apiManager.getMeals();
        const days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];
        const mealTypes = ['breakfast', 'lunch', 'dinner'];
        
        // Simple auto-fill logic
        const breakfastMeals = ['Scrambled Eggs', 'Peanut Butter Sandwich'];
        const lunchMeals = ['Pasta with Tomato Sauce', 'Microwave Mac and Cheese'];
        const dinnerMeals = ['Chicken Rice Bowl', 'Vegetable Stir Fry'];
        
        days.forEach(day => {
            if (!mealPlanData[day]) mealPlanData[day] = {};
            
            // Only fill empty slots
            if (!mealPlanData[day].breakfast) {
                mealPlanData[day].breakfast = {
                    name: breakfastMeals[Math.floor(Math.random() * breakfastMeals.length)],
                    cookTime: '10'
                };
            }
            if (!mealPlanData[day].lunch) {
                mealPlanData[day].lunch = {
                    name: lunchMeals[Math.floor(Math.random() * lunchMeals.length)],
                    cookTime: '15'
                };
            }
            if (!mealPlanData[day].dinner) {
                mealPlanData[day].dinner = {
                    name: dinnerMeals[Math.floor(Math.random() * dinnerMeals.length)],
                    cookTime: '30'
                };
            }
        });
        
        saveMealPlanData();
        displayMealPlan();
        window.authManager.showSuccessMessage('Week auto-filled with balanced meals!');
        
    } catch (error) {
        console.error('Error auto-filling week:', error);
        window.authManager.showError('Failed to auto-fill week');
    }
}

async function generateShoppingList() {
    try {
        const plannedMeals = [];
        Object.values(mealPlanData).forEach(dayMeals => {
            Object.values(dayMeals).forEach(meal => {
                plannedMeals.push(meal.name);
            });
        });
        
        if (plannedMeals.length === 0) {
            window.authManager.showInfoMessage('Add some meals to your plan first!');
            return;
        }
        
        // In a real app, this would call the backend API
        // For now, show a success message
        window.authManager.showSuccessMessage(
            `Shopping list generated for ${plannedMeals.length} meals! (Feature coming soon)`
        );
        
    } catch (error) {
        console.error('Error generating shopping list:', error);
        window.authManager.showError('Failed to generate shopping list');
    }
}

function clearWeek() {
    if (confirm('Are you sure you want to clear all meals for this week?')) {
        mealPlanData = {};
        saveMealPlanData();
        clearMealPlanDisplay();
        window.authManager.showInfoMessage('Week cleared');
    }
}

function updateWeeklySummary() {
    let totalMeals = 0;
    let estimatedCost = 0;
    const uniqueIngredients = new Set();
    
    Object.values(mealPlanData).forEach(dayMeals => {
        Object.values(dayMeals).forEach(meal => {
            totalMeals++;
            estimatedCost += 4.50; // Average meal cost
        });
    });
    
    document.getElementById('total-meals').textContent = totalMeals;
    document.getElementById('estimated-cost').textContent = `$${estimatedCost.toFixed(2)}`;
    document.getElementById('total-ingredients').textContent = Math.floor(totalMeals * 3.5);
}

// Add CSS for meal planning
const mealPlanStyles = `
<style>
.meal-plan-week {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 15px;
    margin-bottom: 30px;
}

.day-column {
    background: white;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.day-column h3 {
    background: #007bff;
    color: white;
    padding: 15px;
    margin: 0;
    text-align: center;
    font-size: 1rem;
}

.day-date {
    padding: 10px;
    text-align: center;
    font-weight: bold;
    color: #666;
    border-bottom: 1px solid #f0f0f0;
}

.meals-column {
    padding: 15px;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.meal-slot {
    min-height: 80px;
    border: 2px dashed #e0e0e0;
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    cursor: pointer;
    transition: all 0.3s ease;
    position: relative;
}

.meal-slot:hover {
    border-color: #007bff;
    background-color: #f8f9ff;
}

.meal-slot.filled {
    border-style: solid;
    border-color: #28a745;
    background-color: #f8fff9;
}

.meal-label {
    font-size: 12px;
    font-weight: bold;
    color: #666;
    padding: 5px 10px;
    background: #f8f9fa;
    border-radius: 6px 6px 0 0;
}

.meal-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 10px;
}

.add-meal-btn {
    font-size: 24px;
    color: #ccc;
    margin-bottom: 5px;
}

.meal-placeholder {
    font-size: 12px;
    color: #999;
}

.assigned-meal {
    text-align: center;
    position: relative;
    width: 100%;
}

.meal-name {
    font-weight: bold;
    font-size: 13px;
    color: #333;
    margin-bottom: 4px;
}

.meal-time {
    font-size: 11px;
    color: #666;
}

.remove-meal {
    position: absolute;
    top: -8px;
    right: -8px;
    background: #dc3545;
    color: white;
    border: none;
    border-radius: 50%;
    width: 20px;
    height: 20px;
    font-size: 12px;
    cursor: pointer;
    display: none;
}

.assigned-meal:hover .remove-meal {
    display: block;
}

.modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0,0,0,0.5);
    z-index: 1000;
}

.modal-content {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: white;
    border-radius: 12px;
    width: 90%;
    max-width: 600px;
    max-height: 80vh;
    overflow: hidden;
}

.modal-header {
    padding: 20px;
    border-bottom: 1px solid #e0e0e0;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.modal-close {
    font-size: 24px;
    cursor: pointer;
    color: #666;
}

.modal-body {
    padding: 20px;
    max-height: 60vh;
    overflow-y: auto;
}

.modal-meal-option {
    padding: 15px;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    margin-bottom: 10px;
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: all 0.3s ease;
}

.modal-meal-option:hover {
    background-color: #f8f9ff;
    border-color: #007bff;
}

.meal-info .meal-name {
    font-weight: bold;
    margin-bottom: 4px;
}

.meal-details {
    font-size: 14px;
    color: #666;
}

.summary-card {
    text-align: center;
    padding: 20px;
    background: #f8f9fa;
    border-radius: 8px;
}

@media (max-width: 1200px) {
    .meal-plan-week {
        grid-template-columns: repeat(4, 1fr);
    }
}

@media (max-width: 768px) {
    .meal-plan-week {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 480px) {
    .meal-plan-week {
        grid-template-columns: 1fr;
    }
}
</style>
`;

// Inject styles
document.head.insertAdjacentHTML('beforeend', mealPlanStyles);

// Export functions
window.loadMealPlanPage = loadMealPlanPage;
window.removeMeal = removeMeal;
window.selectMeal = selectMeal;