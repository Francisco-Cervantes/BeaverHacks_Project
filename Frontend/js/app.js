// Main application initialization and coordination
class BeaverEatsApp {
    constructor() {
        this.isInitialized = false;
        this.init();
    }

    async init() {
        try {
            console.log('Initializing NomNomNomotron App...');
            
            // Wait for DOM to be ready
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', () => this.initializeApp());
            } else {
                await this.initializeApp();
            }
        } catch (error) {
            console.error('Error initializing app:', error);
            this.showErrorMessage('Failed to initialize application');
        }
    }

    async initializeApp() {
        try {
            // Initialize core managers
            console.log('Creating managers...');
            
            // Initialize API manager first
            window.apiManager = new APIManager();
            
            // Initialize authentication manager
            window.authManager = new AuthManager();
            
            // Initialize navigation manager
            window.navigationManager = new NavigationManager();
            
            // Test backend connection
            await this.testBackendConnection();
            
            // Set up global error handling
            this.setupErrorHandling();
            
            // Set up keyboard shortcuts
            this.setupKeyboardShortcuts();
            
            // Initialize service worker for offline support (optional)
            this.initializeServiceWorker();
            
            console.log('NomNomNomotron App initialized successfully!');
            this.isInitialized = true;
            
            // Show welcome message for first-time users
            this.checkFirstTimeUser();
            
        } catch (error) {
            console.error('Error in initializeApp:', error);
            this.showErrorMessage('Application initialization failed');
        }
    }

    async testBackendConnection() {
        try {
            const isConnected = await window.apiManager.testConnection();
            if (isConnected) {
                console.log('✓ Connected to backend successfully');
                this.showConnectionStatus('online');
            } else {
                console.log('⚠ Backend not available, using mock data');
                this.showConnectionStatus('offline');
            }
        } catch (error) {
            console.log('⚠ Backend connection failed, using mock data');
            this.showConnectionStatus('offline');
        }
    }

    showConnectionStatus(status) {
        // Add connection indicator to the navbar
        const navbar = document.querySelector('.nav-container');
        if (navbar) {
            const existingIndicator = navbar.querySelector('.connection-indicator');
            if (existingIndicator) {
                existingIndicator.remove();
            }

            const indicator = document.createElement('div');
            indicator.className = `connection-indicator ${status}`;
            indicator.innerHTML = status === 'online' 
                ? '<i class="fas fa-circle" style="color: #28a745; font-size: 8px;"></i>' 
                : '<i class="fas fa-circle" style="color: #ffc107; font-size: 8px;"></i>';
            indicator.title = status === 'online' ? 'Connected to backend' : 'Using offline mode';
            indicator.style.cssText = 'margin-left: 10px; display: flex; align-items: center;';
            
            const userActions = navbar.querySelector('.user-actions');
            if (userActions) {
                userActions.insertBefore(indicator, userActions.firstChild);
            }
        }
    }

    setupErrorHandling() {
        // Global error handler
        window.addEventListener('error', (e) => {
            console.error('Global error:', e.error);
            this.logError('JavaScript Error', e.error);
        });

        // Unhandled promise rejection handler
        window.addEventListener('unhandledrejection', (e) => {
            console.error('Unhandled promise rejection:', e.reason);
            this.logError('Promise Rejection', e.reason);
            e.preventDefault(); // Prevent default browser behavior
        });

        // API error handler
        window.addEventListener('apierror', (e) => {
            console.error('API error:', e.detail);
            this.handleAPIError(e.detail);
        });
    }

    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Only handle shortcuts when not typing in inputs
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
                return;
            }

            // Keyboard shortcuts
            if (e.ctrlKey || e.metaKey) {
                switch (e.key) {
                    case '1':
                        e.preventDefault();
                        window.navigationManager.navigateTo('home');
                        break;
                    case '2':
                        e.preventDefault();
                        window.navigationManager.navigateTo('meals');
                        break;
                    case '3':
                        e.preventDefault();
                        window.navigationManager.navigateTo('chat');
                        break;
                    case '4':
                        e.preventDefault();
                        if (window.authManager.getIsLoggedIn()) {
                            window.navigationManager.navigateTo('meal-plan');
                        }
                        break;
                    case '/':
                        e.preventDefault();
                        this.focusSearchOrChat();
                        break;
                }
            }

            // ESC key to close modals or go back
            if (e.key === 'Escape') {
                this.handleEscapeKey();
            }
        });
    }

    focusSearchOrChat() {
        // Focus on chat input if on chat page, otherwise navigate to chat
        const chatInput = document.getElementById('chat-input');
        if (chatInput && !chatInput.closest('.hidden')) {
            chatInput.focus();
        } else {
            window.navigationManager.navigateTo('chat');
        }
    }

    handleEscapeKey() {
        // Close any open modals or notifications
        const notifications = document.querySelectorAll('.notification');
        notifications.forEach(notification => {
            notification.remove();
        });

        // If on individual meal page, go back
        if (window.navigationManager.currentPage === 'individual-meal') {
            history.back();
        }
    }

    initializeServiceWorker() {
        // Service worker disabled — causes stale cache issues during development
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.getRegistrations().then((registrations) => {
                for (const reg of registrations) reg.unregister();
            });
        }
    }

    checkFirstTimeUser() {
        const hasVisited = localStorage.getItem('nomnomn_visited');
        if (!hasVisited) {
            localStorage.setItem('nomnomn_visited', 'true');
            this.showWelcomeMessage();
        }
    }

    showWelcomeMessage() {
        setTimeout(() => {
            if (window.authManager) {
                window.authManager.showInfoMessage(
                    'Welcome to NomNomNomotron! Your AI-powered meal planning companion for busy families and students. \ud83e\udd16'
                );
            }
        }, 1000);
    }

    // Error handling methods
    logError(type, error) {
        const errorData = {
            type,
            message: error.message,
            stack: error.stack,
            timestamp: new Date().toISOString(),
            url: window.location.href,
            userAgent: navigator.userAgent
        };

        // In production, send to error tracking service
        console.error('Logged error:', errorData);
        
        // Store locally for debugging
        const errors = JSON.parse(localStorage.getItem('nomnomn_errors') || '[]');
        errors.push(errorData);
        // Keep only last 10 errors
        if (errors.length > 10) {
            errors.shift();
        }
        localStorage.setItem('nomnomn_errors', JSON.stringify(errors));
    }

    handleAPIError(error) {
        // Show user-friendly error messages
        const userMessage = this.getAPIErrorMessage(error);
        if (window.authManager) {
            window.authManager.showError(userMessage);
        }
    }

    getAPIErrorMessage(error) {
        if (error.status === 404) {
            return 'The requested information was not found.';
        } else if (error.status === 500) {
            return 'Server error. Please try again later.';
        } else if (error.status === 401) {
            return 'Authentication required. Please sign in.';
        } else if (error.name === 'TypeError' && error.message.includes('fetch')) {
            return 'Network error. Please check your connection.';
        }
        return 'An unexpected error occurred. Please try again.';
    }

    showErrorMessage(message) {
        // Fallback error display if AuthManager isn't available
        const errorDiv = document.createElement('div');
        errorDiv.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background-color: #dc3545;
            color: white;
            padding: 20px;
            border-radius: 8px;
            z-index: 10000;
            max-width: 400px;
            text-align: center;
        `;
        errorDiv.textContent = message;
        document.body.appendChild(errorDiv);

        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.parentNode.removeChild(errorDiv);
            }
        }, 5000);
    }

    // Utility methods
    isMobile() {
        return window.innerWidth <= 768;
    }

    getDeviceType() {
        if (window.innerWidth <= 480) return 'mobile';
        if (window.innerWidth <= 768) return 'tablet';
        return 'desktop';
    }

    // Performance monitoring
    measurePerformance() {
        if (performance && performance.timing) {
            const timing = performance.timing;
            const loadTime = timing.loadEventEnd - timing.navigationStart;
            console.log(`Page load time: ${loadTime}ms`);
            
            // Log performance metrics
            const perfData = {
                loadTime,
                domContentLoaded: timing.domContentLoadedEventEnd - timing.navigationStart,
                firstPaint: performance.getEntriesByName('first-paint')[0]?.startTime || 0
            };
            
            localStorage.setItem('nomnomn_perf', JSON.stringify(perfData));
        }
    }

    // Development helpers
    getDebugInfo() {
        return {
            initialized: this.isInitialized,
            currentUser: window.authManager?.getCurrentUser(),
            currentPage: window.navigationManager?.currentPage,
            errors: JSON.parse(localStorage.getItem('nomnomn_errors') || '[]'),
            performance: JSON.parse(localStorage.getItem('nomnomn_perf') || '{}')
        };
    }

    // Cleanup on page unload
    destroy() {
        console.log('Cleaning up NomNomNomotron App...');
        // Remove event listeners
        // Clear timers
        // Save state if needed
    }
}

// Initialize the app
console.log('Loading NomNomNomotron...');
const app = new BeaverEatsApp();

// Handle page unload
window.addEventListener('beforeunload', () => {
    if (window.beaverEatsApp) {
        window.beaverEatsApp.destroy();
    }
});

// Performance monitoring
window.addEventListener('load', () => {
    setTimeout(() => {
        if (app && app.measurePerformance) {
            app.measurePerformance();
        }
    }, 1000);
});

// Make app available globally for debugging
window.beaverEatsApp = app;

// Development helpers (remove in production)
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    window.debug = () => app.getDebugInfo();
    console.log('Development mode: Use debug() in console for app information');
}