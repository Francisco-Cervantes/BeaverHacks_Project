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
        const registerForm = document.getElementById('register-form');
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

        if (registerForm) {
            registerForm.addEventListener('submit', (e) => this.handleRegister(e));
        }

        if (showRegister) {
            showRegister.addEventListener('click', () => {
                document.getElementById('login-section').classList.add('hidden');
                document.getElementById('register-section').classList.remove('hidden');
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

    async handleRegister(e) {
        e.preventDefault();
        const username = document.getElementById('reg-username').value.trim();
        const password = document.getElementById('reg-password').value;
        const zip = document.getElementById('zip-input')?.value || '97331';
        const radius = parseInt(document.getElementById('mile-range')?.value || '10');

        if (!username || password.length < 6) {
            this.showError('Username required and password must be at least 6 characters');
            return;
        }

        try {
            await window.apiManager.registerUser(username, password, zip, radius);
            const user = { id: username, email: username, name: username, zipCode: zip, dietaryRestrictions: [], dailyCalories: 2000 };
            this.signIn(user);
        } catch (error) {
            this.showError(error.message || 'Registration failed');
        }
    }

    handleAuthButton() {
        if (this.isLoggedIn) {
            this.signOut();
        } else {
            this.showSignInPage();
        }
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
        if (this.isLoggedIn) {
            this.showHomePage();
        } else {
            this.showSignInPage();
        }
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