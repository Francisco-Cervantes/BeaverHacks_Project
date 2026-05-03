// Authentication management
class AuthManager {
    constructor() {
        this.currentUser = this.loadUserFromStorage();
        this.isLoggedIn = !!this.currentUser;
        this.init();
    }

    init() {
        // Set up auth button listeners
        const authBtn = document.getElementById('auth-btn');
        const signInForm = document.getElementById('sign-in-form');
        const guestContinue = document.getElementById('guest-continue');
        const showRegister = document.getElementById('show-register');
        const showLogin = document.getElementById('show-login');

        if (authBtn) {
            authBtn.addEventListener('click', () => this.handleAuthButton());
        }

        if (signInForm) {
            signInForm.addEventListener('submit', (e) => this.handleSignIn(e));
        }

        if (guestContinue) {
            guestContinue.addEventListener('click', () => this.continueAsGuest());
        }

        if (showRegister) {
            showRegister.addEventListener('click', () => {
                document.getElementById('login-section').classList.add('hidden');
                document.getElementById('register-section').classList.remove('hidden');
                this.resetRegForm();
            });
        }

        if (showLogin) {
            showLogin.addEventListener('click', () => {
                document.getElementById('register-section').classList.add('hidden');
                document.getElementById('login-section').classList.remove('hidden');
            });
        }

        // Update UI based on auth state
        this.updateAuthUI();
        
        // Show appropriate initial page
        this.showInitialPage();
    }

    // ── Registration wizard ──────────────────────────────────

    resetRegForm() {
        // Reset all panels back to step 1
        for (let i = 1; i <= 4; i++) {
            const panel = document.getElementById(`reg-panel-${i}`);
            const dot   = document.getElementById(`reg-dot-${i}`);
            if (panel) panel.classList.toggle('hidden', i !== 1);
            if (dot) {
                dot.classList.remove('active', 'done');
                if (i === 1) dot.classList.add('active');
            }
        }
        // Clear inputs
        ['reg-username','reg-email','reg-password','reg-confirm-password','reg-phone',
         'reg-zip','reg-weekly-budget','reg-meal-budget','reg-diet','reg-calorie-target',
         'reg-protein','reg-fat','reg-carbs','reg-cooking-skill','reg-max-cook-time']
            .forEach(id => { const el = document.getElementById(id); if (el) el.value = ''; });
        document.querySelectorAll('input[name="reg-allergy"], input[name="reg-equipment"]')
            .forEach(cb => { cb.checked = false; });
        const btn = document.getElementById('reg-submit-btn');
        if (btn) { btn.disabled = false; btn.textContent = 'Create Account'; }
    }

    regNext(step) {
        if (!this.regValidate(step)) return;
        document.getElementById(`reg-panel-${step}`).classList.add('hidden');
        document.getElementById(`reg-panel-${step + 1}`).classList.remove('hidden');
        const cur  = document.getElementById(`reg-dot-${step}`);
        const next = document.getElementById(`reg-dot-${step + 1}`);
        if (cur)  { cur.classList.remove('active'); cur.classList.add('done'); }
        if (next) next.classList.add('active');
    }

    regBack(step) {
        document.getElementById(`reg-panel-${step}`).classList.add('hidden');
        document.getElementById(`reg-panel-${step - 1}`).classList.remove('hidden');
        const cur  = document.getElementById(`reg-dot-${step}`);
        const prev = document.getElementById(`reg-dot-${step - 1}`);
        if (cur)  cur.classList.remove('active');
        if (prev) { prev.classList.remove('done'); prev.classList.add('active'); }
    }

    regValidate(step) {
        if (step === 1) {
            const username = document.getElementById('reg-username').value.trim();
            const email    = document.getElementById('reg-email').value.trim();
            const password = document.getElementById('reg-password').value;
            const confirm  = document.getElementById('reg-confirm-password').value;
            if (!username)                          { this.showError('Username is required'); return false; }
            if (!email || !email.includes('@'))     { this.showError('A valid email is required'); return false; }
            if (password.length < 6)                { this.showError('Password must be at least 6 characters'); return false; }
            if (password !== confirm)               { this.showError('Passwords do not match'); return false; }
        }
        if (step === 2) {
            const zip    = document.getElementById('reg-zip').value.trim();
            const weekly = document.getElementById('reg-weekly-budget').value;
            const meal   = document.getElementById('reg-meal-budget').value;
            if (!zip || zip.length !== 5 || !/^\d+$/.test(zip)) { this.showError('A valid 5-digit ZIP code is required'); return false; }
            if (!weekly) { this.showError('Weekly budget is required'); return false; }
            if (!meal)   { this.showError('Per-meal budget is required'); return false; }
        }
        if (step === 3) {
            const diet     = document.getElementById('reg-diet').value;
            const allergies = document.querySelectorAll('input[name="reg-allergy"]:checked');
            const calories = document.getElementById('reg-calorie-target').value;
            if (!diet)              { this.showError('Please select a diet type'); return false; }
            if (!allergies.length)  { this.showError('Please select at least one allergy option (or "None")'); return false; }
            if (!calories)          { this.showError('Daily calorie target is required'); return false; }
        }
        if (step === 4) {
            const equipment = document.querySelectorAll('input[name="reg-equipment"]:checked');
            const skill     = document.getElementById('reg-cooking-skill').value;
            const time      = document.getElementById('reg-max-cook-time').value;
            if (!equipment.length) { this.showError('Please select at least one piece of equipment'); return false; }
            if (!skill)            { this.showError('Please select your cooking skill level'); return false; }
            if (!time)             { this.showError('Please select your max cook time'); return false; }
        }
        return true;
    }

    async regSubmit() {
        if (!this.regValidate(4)) return;

        const username     = document.getElementById('reg-username').value.trim();
        const email        = document.getElementById('reg-email').value.trim();
        const password     = document.getElementById('reg-password').value;
        const phone        = document.getElementById('reg-phone').value.trim();
        const zip          = document.getElementById('reg-zip').value.trim();
        const radius       = parseInt(document.getElementById('reg-radius').value);
        const weeklyBudget = parseFloat(document.getElementById('reg-weekly-budget').value);
        const mealBudget   = parseFloat(document.getElementById('reg-meal-budget').value);
        const diet         = document.getElementById('reg-diet').value;
        const allergies    = [...document.querySelectorAll('input[name="reg-allergy"]:checked')].map(el => el.value);
        const calories     = parseInt(document.getElementById('reg-calorie-target').value);
        const protein      = document.getElementById('reg-protein').value;
        const fat          = document.getElementById('reg-fat').value;
        const carbs        = document.getElementById('reg-carbs').value;
        const equipment    = [...document.querySelectorAll('input[name="reg-equipment"]:checked')].map(el => el.value);
        const cookingSkill = document.getElementById('reg-cooking-skill').value;
        const maxCookTime  = parseInt(document.getElementById('reg-max-cook-time').value);

        const btn = document.getElementById('reg-submit-btn');
        btn.disabled = true;
        btn.textContent = 'Creating Account…';

        try {
            const profileData = {
                password,
                email,
                phone,
                zip,
                radius,
                weekly_budget: weeklyBudget,
                meal_budget:   mealBudget,
                keywords: {
                    diet,
                    dieting:        diet !== 'none' && diet !== '',
                    calorie_target: calories,
                    protein_goal:   protein ? parseInt(protein) : null,
                    fat_goal:       fat     ? parseInt(fat)     : null,
                    carb_goal:      carbs   ? parseInt(carbs)   : null
                },
                allergies,
                equipment,
                cooking_skill:  cookingSkill,
                max_cook_time:  maxCookTime,
                display_name:   username,
                guest_mode:     false
            };

            await window.apiManager.registerUser(username, profileData);

            const user = {
                id:                  username,
                email,
                name:                username,
                zipCode:             zip,
                dietaryRestrictions: allergies,
                dailyCalories:       calories
            };
            this.signIn(user);
            this.showSuccessMessage(`Welcome, ${username}! Your account has been created.`);
        } catch (error) {
            btn.disabled = false;
            btn.textContent = 'Create Account';
            this.showError(error.message || 'Registration failed. Please try again.');
        }
    }

    handleAuthButton() {
        if (this.isLoggedIn) {
            this.confirmSignOut();
        } else {
            this.showSignInPage();
        }
    }

    confirmSignOut() {
        // Remove any existing dialog
        document.getElementById('signout-confirm-dialog')?.remove();

        const dialog = document.createElement('div');
        dialog.id = 'signout-confirm-dialog';
        dialog.style.cssText = `
            position:fixed;inset:0;z-index:99999;display:flex;
            align-items:center;justify-content:center;
            background:rgba(0,0,0,0.5);
        `;
        dialog.innerHTML = `
            <div style="
                background:white;border-radius:16px;padding:36px 32px;
                max-width:380px;width:90%;text-align:center;
                box-shadow:0 8px 40px rgba(0,0,0,0.2);
            ">
                <i class="fas fa-sign-out-alt" style="font-size:40px;color:#dc3545;margin-bottom:16px;display:block;"></i>
                <h3 style="margin:0 0 12px;color:#1a1a1a;font-size:20px;">Sign Out?</h3>
                <p style="color:#666;margin:0 0 28px;line-height:1.5;">
                    Are you sure you want to sign out? Your chat history will be cleared.
                </p>
                <div style="display:flex;gap:12px;justify-content:center;">
                    <button id="signout-no"  style="flex:1;padding:12px;border:2px solid #e0e0e0;background:white;border-radius:8px;font-size:15px;font-weight:600;cursor:pointer;">No, stay signed in</button>
                    <button id="signout-yes" style="flex:1;padding:12px;border:none;background:#dc3545;color:white;border-radius:8px;font-size:15px;font-weight:600;cursor:pointer;">Yes, sign out</button>
                </div>
            </div>
        `;
        document.body.appendChild(dialog);

        dialog.querySelector('#signout-no').addEventListener('click', () => dialog.remove());
        dialog.querySelector('#signout-yes').addEventListener('click', () => {
            dialog.remove();
            this.signOut();
        });
        // Close on backdrop click
        dialog.addEventListener('click', e => { if (e.target === dialog) dialog.remove(); });
    }

    async handleSignIn(e) {
        e.preventDefault();
        const formData = new FormData(e.target);
        const email = formData.get('email');
        const password = formData.get('password');

        try {
            // In a real app, this would make an API call
            const user = await this.authenticateUser(email, password);
            this.signIn(user);
        } catch (error) {
            this.showError('Invalid email or password');
        }
    }

    async authenticateUser(email, password) {
        // Use real Flask login endpoint
        const username = email.includes('@') ? email.split('@')[0] : email;
        await window.apiManager.loginUser(username, password);
        const zip = document.getElementById('zip-input')?.value || '97331';
        return {
            id: username,
            email: email,
            name: username,
            zipCode: zip,
            dietaryRestrictions: [],
            dailyCalories: 2000
        };
    }

    signIn(user) {
        this.currentUser = user;
        this.isLoggedIn = true;
        this.saveUserToStorage(user);
        this.updateAuthUI();
        this.showHomePage();
        this.showSuccessMessage('Welcome back!');
    }

    continueAsGuest() {
        this.currentUser = null;
        this.isLoggedIn = false;
        this.updateAuthUI();
        this.showHomePage();
        this.showInfoMessage('You\'re browsing as a guest. Sign in for personalized features!');
    }

    signOut() {
        this.currentUser = null;
        this.isLoggedIn = false;
        this.clearUserStorage();
        this.updateAuthUI();

        // Reset chat page so next visit starts fresh
        const chatPage = document.getElementById('chat-page');
        if (chatPage) {
            chatPage.removeAttribute('data-loaded');
            chatPage.innerHTML = '';
        }

        // Reset meals page tabs (meal plan is auth-gated)
        const mealsPage = document.getElementById('meals-page');
        if (mealsPage) {
            mealsPage.removeAttribute('data-tab-shell');
            mealsPage.innerHTML = '';
        }

        this.showSignInPage();
        this.showInfoMessage('You\'ve been signed out');
    }

    updateAuthUI() {
        const authBtn = document.getElementById('auth-btn');
        const userInfo = document.getElementById('user-info');
        const userZip = document.getElementById('user-zip');

        if (authBtn) {
            if (this.isLoggedIn) {
                authBtn.textContent = 'Sign Out';
                authBtn.classList.remove('btn-primary');
                authBtn.classList.add('btn-secondary');
            } else {
                authBtn.textContent = 'Sign In';
                authBtn.classList.remove('btn-secondary');
                authBtn.classList.add('btn-primary');
            }
        }

        if (userInfo && userZip) {
            if (this.isLoggedIn && this.currentUser) {
                userInfo.classList.remove('hidden');
                userZip.textContent = this.currentUser.zipCode || '97331';
            } else {
                userInfo.classList.add('hidden');
            }
        }

        // Update navigation based on auth state
        this.updateNavigationForAuth();
    }

    updateNavigationForAuth() {
        // Auth guards are handled centrally in navigation.js navigateTo()
    }

    showAuthRequiredMessage(feature) {
        this.showInfoMessage(
            `${feature} requires an account. Please sign in to access this feature.`
            // No callback — notification just dismisses, doesn't redirect
        );
    }

    showInitialPage() {
        // Always start on home (as guest if not logged in).
        // The sign-in page is only shown when the user explicitly clicks Sign In.
        this.showHomePage();
    }

    showSignInPage() {
        // Hide all pages
        document.querySelectorAll('.page').forEach(page => {
            page.classList.remove('active');
        });
        
        // Show sign in page
        const signInPage = document.getElementById('sign-in-page');
        if (signInPage) {
            signInPage.classList.add('active');
        }
    }

    showHomePage() {
        // Hide all pages
        document.querySelectorAll('.page').forEach(page => {
            page.classList.remove('active');
        });
        
        // Show home page
        const homePage = document.getElementById('home-page');
        if (homePage) {
            homePage.classList.add('active');
        }

        // Update active nav link
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });
        const homeLink = document.querySelector('[data-page="home"]');
        if (homeLink) {
            homeLink.classList.add('active');
        }
    }

    // Storage methods
    saveUserToStorage(user) {
        localStorage.setItem('nomnomn_user', JSON.stringify(user));
    }

    loadUserFromStorage() {
        const userStr = localStorage.getItem('nomnomn_user');
        return userStr ? JSON.parse(userStr) : null;
    }

    clearUserStorage() {
        localStorage.removeItem('nomnomn_user');
    }

    // Utility methods
    showError(message) {
        this.showMessage(message, 'error');
    }

    showSuccessMessage(message) {
        this.showMessage(message, 'success');
    }

    showInfoMessage(message, callback = null) {
        this.showMessage(message, 'info', callback);
    }

    showMessage(message, type = 'info', callback = null) {
        // Create and show notification
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <span>${message}</span>
            <button class="notification-close">&times;</button>
        `;

        // Add notification styles if they don't exist
        if (!document.getElementById('notification-styles')) {
            const styles = document.createElement('style');
            styles.id = 'notification-styles';
            styles.textContent = `
                .notification {
                    position: fixed;
                    top: 90px;
                    right: 20px;
                    padding: 15px 20px;
                    border-radius: 6px;
                    color: white;
                    z-index: 10000;
                    max-width: 400px;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    cursor: pointer;
                    transform: translateX(100%);
                    transition: transform 0.3s ease;
                }
                .notification.show {
                    transform: translateX(0);
                }
                .notification-error { background-color: #dc3545; }
                .notification-success { background-color: #28a745; }
                .notification-info { background-color: #76b900; }
                .notification-close {
                    background: none;
                    border: none;
                    color: white;
                    font-size: 18px;
                    cursor: pointer;
                    margin-left: auto;
                }
            `;
            document.head.appendChild(styles);
        }

        document.body.appendChild(notification);
        
        // Show notification
        setTimeout(() => notification.classList.add('show'), 100);

        // Add click handlers
        const closeBtn = notification.querySelector('.notification-close');
        const closeNotification = () => {
            notification.classList.remove('show');
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
                if (callback) callback();
            }, 300);
        };

        closeBtn.addEventListener('click', closeNotification);
        notification.addEventListener('click', closeNotification);

        // Auto-hide after 5 seconds
        setTimeout(closeNotification, 5000);
    }

    // Getter methods for other modules
    getCurrentUser() {
        return this.currentUser;
    }

    getIsLoggedIn() {
        return this.isLoggedIn;
    }
}

// Export for use in other modules
window.AuthManager = AuthManager;