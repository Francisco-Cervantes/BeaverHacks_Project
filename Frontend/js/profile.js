// Profile page functionality
function loadProfilePage() {
    const profilePage = document.getElementById('profile-page');
    if (profilePage && !profilePage.hasAttribute('data-loaded')) {
        profilePage.innerHTML = `
            <div class="profile-container">
                <div class="profile-header" style="text-align: center; margin-bottom: 40px;">
                    <h1><i class="fas fa-user"></i> Your Profile</h1>
                    <p>Manage your dietary preferences and personal information</p>
                </div>

                <form id="profile-form" class="profile-sections">
                    <!-- Personal Information Section -->
                    <div class="profile-section">
                        <h2><i class="fas fa-id-card"></i> Personal Information</h2>
                        <div class="form-grid">
                            <div class="form-group">
                                <label for="profile-name">Full Name</label>
                                <input type="text" id="profile-name" name="name" placeholder="Enter your name">
                            </div>
                            <div class="form-group">
                                <label for="profile-email">Email</label>
                                <input type="email" id="profile-email" name="email" placeholder="your.email@oregonstate.edu">
                            </div>
                            <div class="form-group">
                                <label for="profile-zip">ZIP Code</label>
                                <input type="text" id="profile-zip" name="zipCode" placeholder="97331" maxlength="5">
                            </div>
                            <div class="form-group">
                                <label for="profile-phone">Phone (optional)</label>
                                <input type="tel" id="profile-phone" name="phone" placeholder="(541) 555-0123">
                            </div>
                        </div>
                    </div>

                    <!-- Dietary Preferences Section -->
                    <div class="profile-section">
                        <h2><i class="fas fa-utensils"></i> Dietary Preferences</h2>
                        
                        <div class="form-group">
                            <label for="daily-calories">Daily Calorie Target</label>
                            <select id="daily-calories" name="dailyCalories">
                                <option value="">Select calorie target</option>
                                <option value="1500">1,500 calories</option>
                                <option value="1800">1,800 calories</option>
                                <option value="2000">2,000 calories</option>
                                <option value="2200">2,200 calories</option>
                                <option value="2500">2,500 calories</option>
                                <option value="3000">3,000+ calories</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label>Dietary Restrictions</label>
                            <div class="checkbox-group">
                                <div class="checkbox-item">
                                    <input type="checkbox" id="vegetarian" name="dietaryRestrictions" value="vegetarian">
                                    <label for="vegetarian">Vegetarian</label>
                                </div>
                                <div class="checkbox-item">
                                    <input type="checkbox" id="vegan" name="dietaryRestrictions" value="vegan">
                                    <label for="vegan">Vegan</label>
                                </div>
                                <div class="checkbox-item">
                                    <input type="checkbox" id="gluten-free" name="dietaryRestrictions" value="gluten-free">
                                    <label for="gluten-free">Gluten-Free</label>
                                </div>
                                <div class="checkbox-item">
                                    <input type="checkbox" id="dairy-free" name="dietaryRestrictions" value="dairy-free">
                                    <label for="dairy-free">Dairy-Free</label>
                                </div>
                                <div class="checkbox-item">
                                    <input type="checkbox" id="nut-free" name="dietaryRestrictions" value="nut-free">
                                    <label for="nut-free">Nut-Free</label>
                                </div>
                                <div class="checkbox-item">
                                    <input type="checkbox" id="low-sodium" name="dietaryRestrictions" value="low-sodium">
                                    <label for="low-sodium">Low Sodium</label>
                                </div>
                            </div>
                        </div>

                        <div class="form-group">
                            <label for="allergies">Food Allergies (optional)</label>
                            <textarea id="allergies" name="allergies" rows="3" placeholder="List any specific food allergies..."></textarea>
                        </div>
                    </div>

                    <!-- Cooking Preferences Section -->
                    <div class="profile-section">
                        <h2><i class="fas fa-tools"></i> Cooking Setup</h2>
                        
                        <div class="form-group">
                            <label>Available Equipment</label>
                            <div class="checkbox-group">
                                <div class="checkbox-item">
                                    <input type="checkbox" id="stove" name="equipment" value="stove">
                                    <label for="stove">Stove/Cooktop</label>
                                </div>
                                <div class="checkbox-item">
                                    <input type="checkbox" id="oven" name="equipment" value="oven">
                                    <label for="oven">Oven</label>
                                </div>
                                <div class="checkbox-item">
                                    <input type="checkbox" id="microwave" name="equipment" value="microwave">
                                    <label for="microwave">Microwave</label>
                                </div>
                                <div class="checkbox-item">
                                    <input type="checkbox" id="toaster" name="equipment" value="toaster">
                                    <label for="toaster">Toaster/Toaster Oven</label>
                                </div>
                                <div class="checkbox-item">
                                    <input type="checkbox" id="blender" name="equipment" value="blender">
                                    <label for="blender">Blender</label>
                                </div>
                                <div class="checkbox-item">
                                    <input type="checkbox" id="slow-cooker" name="equipment" value="slow-cooker">
                                    <label for="slow-cooker">Slow Cooker</label>
                                </div>
                            </div>
                        </div>

                        <div class="form-group">
                            <label for="cooking-skill">Cooking Experience</label>
                            <select id="cooking-skill" name="cookingSkill">
                                <option value="">Select experience level</option>
                                <option value="beginner">Beginner (just started)</option>
                                <option value="basic">Basic (can follow simple recipes)</option>
                                <option value="intermediate">Intermediate (comfortable cooking)</option>
                                <option value="advanced">Advanced (experienced cook)</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label for="max-cook-time">Maximum Cooking Time</label>
                            <select id="max-cook-time" name="maxCookTime">
                                <option value="">No preference</option>
                                <option value="10">10 minutes or less</option>
                                <option value="20">20 minutes or less</option>
                                <option value="30">30 minutes or less</option>
                                <option value="60">1 hour or less</option>
                                <option value="120">2 hours or less</option>
                            </select>
                        </div>
                    </div>

                    <!-- Budget Section -->
                    <div class="profile-section">
                        <h2><i class="fas fa-dollar-sign"></i> Budget Preferences</h2>
                        
                        <div class="form-grid">
                            <div class="form-group">
                                <label for="weekly-budget">Weekly Food Budget</label>
                                <select id="weekly-budget" name="weeklyBudget">
                                    <option value="">Select budget range</option>
                                    <option value="25">$25 or less</option>
                                    <option value="50">$25 - $50</option>
                                    <option value="75">$50 - $75</option>
                                    <option value="100">$75 - $100</option>
                                    <option value="150">$100 - $150</option>
                                    <option value="200">$150+</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label for="meal-budget">Target Cost per Meal</label>
                                <select id="meal-budget" name="mealBudget">
                                    <option value="">No preference</option>
                                    <option value="2">Under $2</option>
                                    <option value="3">Under $3</option>
                                    <option value="5">Under $5</option>
                                    <option value="8">Under $8</option>
                                    <option value="10">Under $10</option>
                                </select>
                            </div>
                        </div>
                    </div>

                    <!-- Action Buttons -->
                    <div style="text-align: center; margin-top: 40px;">
                        <button type="submit" class="btn btn-success" style="margin-right: 15px;">
                            <i class="fas fa-save"></i> Save Profile
                        </button>
                        <button type="button" id="clear-profile" class="btn btn-secondary">
                            <i class="fas fa-undo"></i> Reset Form
                        </button>
                    </div>
                </form>
            </div>
        `;
        
        setupProfileFunctionality();
        loadUserProfile();
        profilePage.setAttribute('data-loaded', 'true');
    }
}

function setupProfileFunctionality() {
    const profileForm = document.getElementById('profile-form');
    const clearBtn = document.getElementById('clear-profile');

    if (profileForm) {
        profileForm.addEventListener('submit', saveProfile);
    }

    if (clearBtn) {
        clearBtn.addEventListener('click', clearProfileForm);
    }
}

function loadUserProfile() {
    const currentUser = window.authManager?.getCurrentUser();
    if (!currentUser) return;

    // Populate form with user data
    const fields = ['name', 'email', 'zipCode', 'phone', 'dailyCalories', 'cookingSkill', 'maxCookTime', 'weeklyBudget', 'mealBudget'];
    
    fields.forEach(field => {
        const element = document.getElementById(`profile-${field}`) || document.getElementById(field.replace(/([A-Z])/g, '-$1').toLowerCase());
        if (element && currentUser[field]) {
            element.value = currentUser[field];
        }
    });

    // Handle checkboxes
    if (currentUser.dietaryRestrictions) {
        currentUser.dietaryRestrictions.forEach(restriction => {
            const checkbox = document.getElementById(restriction);
            if (checkbox) checkbox.checked = true;
        });
    }

    if (currentUser.equipment) {
        currentUser.equipment.forEach(equipment => {
            const checkbox = document.getElementById(equipment);
            if (checkbox) checkbox.checked = true;
        });
    }

    // Handle textarea
    const allergiesField = document.getElementById('allergies');
    if (allergiesField && currentUser.allergies) {
        allergiesField.value = currentUser.allergies;
    }
}

async function saveProfile(e) {
    e.preventDefault();
    
    try {
        const formData = new FormData(e.target);
        const profileData = {};

        // Get regular form fields
        ['name', 'email', 'zipCode', 'phone', 'dailyCalories', 'cookingSkill', 'maxCookTime', 'weeklyBudget', 'mealBudget', 'allergies'].forEach(field => {
            const value = formData.get(field);
            if (value) profileData[field] = value;
        });

        // Get checkboxes
        profileData.dietaryRestrictions = formData.getAll('dietaryRestrictions');
        profileData.equipment = formData.getAll('equipment');

        // Update user object
        const currentUser = window.authManager.getCurrentUser();
        const updatedUser = { ...currentUser, ...profileData };
        
        // Save to localStorage (in real app, would save to backend)
        window.authManager.saveUserToStorage(updatedUser);
        window.authManager.currentUser = updatedUser;
        window.authManager.updateAuthUI();

        window.authManager.showSuccessMessage('Profile saved successfully!');
        
    } catch (error) {
        console.error('Error saving profile:', error);
        window.authManager.showError('Failed to save profile. Please try again.');
    }
}

function clearProfileForm() {
    const form = document.getElementById('profile-form');
    if (form) {
        form.reset();
        window.authManager.showInfoMessage('Form cleared');
    }
}

// Export functions
window.loadProfilePage = loadProfilePage;