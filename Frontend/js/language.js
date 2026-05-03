// Language Support System for NomNomNomotron
class LanguageManager {
    constructor() {
        this.currentLanguage = 'en';
        this.translations = {
            en: {
                // Navigation
                'nav.home': 'Home',
                'nav.chat': 'AI Chat',
                'nav.meals': 'Meals',
                'nav.profile': 'Profile',
                'nav.meal-plan': 'Meal Plan',
                'nav.recipes': 'Recipes',
                
                // Auth
                'auth.welcome': 'Welcome to NomNomNomotron',
                'auth.subtitle': 'AI-powered meal planning for busy families and students',
                'auth.email': 'Email',
                'auth.password': 'Password',
                'auth.signin': 'Sign In',
                'auth.guest': 'Continue as Guest',
                'auth.note': 'Advanced meal planning and personalized features require an account',
                
                // Home
                'home.title': 'AI-Powered Meal Planning Made Easy',
                'home.subtitle': 'Perfect for busy families and college students - find affordable groceries, discover budget-friendly recipes, and plan your meals with AI assistance',
                'home.about': 'About NomNomNomotron',
                'home.feature1.title': 'NVIDIA-Powered AI Assistant',
                'home.feature1.desc': 'Get intelligent meal suggestions tailored for busy families and students based on your schedule, budget, and dietary needs',
                'home.feature2.title': 'Local Store Prices',
                'home.feature2.desc': 'Compare prices from nearby grocery stores to find the best deals',
                'home.feature3.title': 'Family & Student-Friendly Recipes',
                'home.feature3.desc': 'Simple recipes perfect for busy lifestyles with minimal equipment and maximum nutrition for the whole family',
                
                // Chat
                'chat.title': 'NomNomNomotron AI Assistant',
                'chat.subtitle': 'Ask me about recipes, meal planning, or grocery shopping tips!',
                'chat.placeholder': 'Type your message here...',
                'chat.intro': 'Hi! I\'m your NomNomNomotron AI assistant powered by NVIDIA technology. I can help you:',
                
                // Common
                'common.loading': 'Loading...',
                'common.error': 'Error loading content',
                'common.save': 'Save',
                'common.cancel': 'Cancel',
                'common.clear': 'Clear',
                'common.apply': 'Apply',
                
                // Price disclaimer
                'disclaimer.title': 'Price Disclaimer:',
                'disclaimer.text': 'Prices shown are generalized estimates based on available store data and recent trends. Deals, sales, and in‑store pricing may change and may not be reflected in real time. Use this as a planning and comparison tool, not a guarantee of final price.'
            },
            es: {
                // Navigation
                'nav.home': 'Inicio',
                'nav.chat': 'Chat IA',
                'nav.meals': 'Comidas',
                'nav.profile': 'Perfil',
                'nav.meal-plan': 'Plan de Comidas',
                'nav.recipes': 'Recetas',
                
                // Auth
                'auth.welcome': 'Bienvenido a NomNomNomotron',
                'auth.subtitle': 'Planificación de comidas con IA para familias ocupadas y estudiantes',
                'auth.email': 'Correo Electrónico',
                'auth.password': 'Contraseña',
                'auth.signin': 'Iniciar Sesión',
                'auth.guest': 'Continuar como Invitado',
                'auth.note': 'La planificación avanzada de comidas y las características personalizadas requieren una cuenta',
                
                // Home
                'home.title': 'Planificación de Comidas con IA Hecha Fácil',
                'home.subtitle': 'Perfecto para familias ocupadas y estudiantes universitarios - encuentra comestibles asequibles, descubre recetas económicas, y planifica tus comidas con asistencia de IA',
                'home.about': 'Acerca de NomNomNomotron',
                'home.feature1.title': 'Asistente IA con NVIDIA',
                'home.feature1.desc': 'Obtén sugerencias inteligentes de comidas adaptadas para familias ocupadas y estudiantes basadas en tu horario, presupuesto y necesidades dietéticas',
                'home.feature2.title': 'Precios de Tiendas Locales',
                'home.feature2.desc': 'Compara precios de supermercados cercanos para encontrar las mejores ofertas',
                'home.feature3.title': 'Recetas para Familias y Estudiantes',
                'home.feature3.desc': 'Recetas simples perfectas para estilos de vida ocupados con equipo mínimo y máxima nutrición para toda la familia',
                
                // Chat
                'chat.title': 'Asistente IA NomNomNomotron',
                'chat.subtitle': '¡Pregúntame sobre recetas, planificación de comidas o consejos de compras!',
                'chat.placeholder': 'Escribe tu mensaje aquí...',
                'chat.intro': '¡Hola! Soy tu asistente IA NomNomNomotron impulsado por tecnología NVIDIA. Puedo ayudarte con:',
                
                // Common
                'common.loading': 'Cargando...',
                'common.error': 'Error al cargar contenido',
                'common.save': 'Guardar',
                'common.cancel': 'Cancelar',
                'common.clear': 'Limpiar',
                'common.apply': 'Aplicar',
                
                // Price disclaimer
                'disclaimer.title': 'Descargo de Precios:',
                'disclaimer.text': 'Los precios mostrados son estimaciones generalizadas basadas en datos disponibles de tiendas y tendencias recientes. Las ofertas, ventas y precios en tienda pueden cambiar y no se reflejan en tiempo real. Usa esto como una herramienta de planificación y comparación, no como garantía del precio final.'
            },
            zh: {
                // Navigation
                'nav.home': '主页',
                'nav.chat': 'AI 聊天',
                'nav.meals': '餐食',
                'nav.profile': '个人资料',
                'nav.meal-plan': '膳食计划',
                'nav.recipes': '食谱',
                
                // Auth
                'auth.welcome': '欢迎来到 NomNomNomotron',
                'auth.subtitle': '为忙碌的家庭和学生提供AI驱动的膳食计划',
                'auth.email': '邮箱',
                'auth.password': '密码',
                'auth.signin': '登录',
                'auth.guest': '访客继续',
                'auth.note': '高级膳食计划和个性化功能需要账户',
                
                // Home
                'home.title': 'AI驱动的膳食计划变得简单',
                'home.subtitle': '完美适合忙碌的家庭和大学生 - 找到实惠的杂货，发现预算友好的食谱，并通过AI助手规划您的膳食',
                'home.about': '关于 NomNomNomotron',
                'home.feature1.title': 'NVIDIA驱动的AI助手',
                'home.feature1.desc': '根据您的时间表、预算和饮食需求，为忙碌的家庭和学生提供智能膳食建议',
                'home.feature2.title': '本地商店价格',
                'home.feature2.desc': '比较附近杂货店的价格，找到最好的优惠',
                'home.feature3.title': '适合家庭和学生的食谱',
                'home.feature3.desc': '完美适合忙碌生活方式的简单食谱，设备要求最少，营养最大化',
                
                // Chat
                'chat.title': 'NomNomNomotron AI助手',
                'chat.subtitle': '向我询问食谱、膳食计划或购物技巧！',
                'chat.placeholder': '在这里输入您的消息...',
                'chat.intro': '你好！我是您的NomNomNomotron AI助手，由NVIDIA技术支持。我可以帮助您：',
                
                // Common
                'common.loading': '加载中...',
                'common.error': '加载内容错误',
                'common.save': '保存',
                'common.cancel': '取消',
                'common.clear': '清除',
                'common.apply': '应用',
                
                // Price disclaimer
                'disclaimer.title': '价格免责声明：',
                'disclaimer.text': '显示的价格是基于可用商店数据和近期趋势的综合估算。优惠、销售和店内价格可能会发生变化，不会实时反映。请将此作为计划和比较工具使用，而不是最终价格的保证。'
            },
            'zh-hk': {
                // Navigation
                'nav.home': '主頁',
                'nav.chat': 'AI 對話',
                'nav.meals': '餐食',
                'nav.profile': '個人檔案',
                'nav.meal-plan': '膳食計劃',
                'nav.recipes': '食譜',
                
                // Auth
                'auth.welcome': '歡迎來到 NomNomNomotron',
                'auth.subtitle': '為繁忙家庭和學生提供AI驅動的膳食計劃',
                'auth.email': '電郵',
                'auth.password': '密碼',
                'auth.signin': '登入',
                'auth.guest': '訪客繼續',
                'auth.note': '進階膳食計劃和個人化功能需要帳戶',
                
                // Home
                'home.title': 'AI驅動的膳食計劃變得簡單',
                'home.subtitle': '完美適合繁忙的家庭和大學生 - 找到實惠的雜貨，發現預算友好的食譜，並透過AI助手規劃您的膳食',
                'home.about': '關於 NomNomNomotron',
                'home.feature1.title': 'NVIDIA驅動的AI助手',
                'home.feature1.desc': '根據您的時間表、預算和飲食需求，為繁忙的家庭和學生提供智能膳食建議',
                'home.feature2.title': '本地商店價格',
                'home.feature2.desc': '比較附近雜貨店的價格，找到最好的優惠',
                'home.feature3.title': '適合家庭和學生的食譜',
                'home.feature3.desc': '完美適合繁忙生活方式的簡單食譜，設備要求最少，營養最大化',
                
                // Chat
                'chat.title': 'NomNomNomotron AI助手',
                'chat.subtitle': '向我詢問食譜、膳食計劃或購物技巧！',
                'chat.placeholder': '在這裡輸入您的消息...',
                'chat.intro': '您好！我是您的NomNomNomotron AI助手，由NVIDIA技術支援。我可以幫助您：',
                
                // Common
                'common.loading': '載入中...',
                'common.error': '載入內容錯誤',
                'common.save': '保存',
                'common.cancel': '取消',
                'common.clear': '清除',
                'common.apply': '應用',
                
                // Price disclaimer
                'disclaimer.title': '價格免責聲明：',
                'disclaimer.text': '顯示的價格是基於可用商店數據和近期趨勢的綜合估算。優惠、銷售和店內價格可能會發生變化，不會實時反映。請將此作為計劃和比較工具使用，而不是最終價格的保證。'
            },
            vi: {
                // Navigation
                'nav.home': 'Trang chủ',
                'nav.chat': 'Trò chuyện AI',
                'nav.meals': 'Bữa ăn',
                'nav.profile': 'Hồ sơ',
                'nav.meal-plan': 'Kế hoạch ăn uống',
                'nav.recipes': 'Công thức',
                
                // Auth
                'auth.welcome': 'Chào mừng đến với NomNomNomotron',
                'auth.subtitle': 'Lập kế hoạch bữa ăn được hỗ trợ AI cho gia đình bận rộn và sinh viên',
                'auth.email': 'Email',
                'auth.password': 'Mật khẩu',
                'auth.signin': 'Đăng nhập',
                'auth.guest': 'Tiếp tục với tư cách khách',
                'auth.note': 'Lập kế hoạch bữa ăn nâng cao và các tính năng cá nhân hóa yêu cầu tài khoản',
                
                // Home
                'home.title': 'Lập kế hoạch bữa ăn được hỗ trợ AI trở nên dễ dàng',
                'home.subtitle': 'Hoàn hảo cho gia đình bận rộn và sinh viên đại học - tìm thực phẩm giá cả phải chăng, khám phá công thức tiết kiệm, và lập kế hoạch bữa ăn với sự hỗ trợ AI',
                'home.about': 'Giới thiệu NomNomNomotron',
                'home.feature1.title': 'Trợ lý AI được hỗ trợ bởi NVIDIA',
                'home.feature1.desc': 'Nhận gợi ý bữa ăn thông minh được thiết kế riêng cho gia đình bận rộn và sinh viên dựa trên lịch trình, ngân sách và nhu cầu dinh dưỡng của bạn',
                'home.feature2.title': 'Giá cửa hàng địa phương',
                'home.feature2.desc': 'So sánh giá từ các cửa hàng tạp hóa gần đó để tìm ưu đãi tốt nhất',
                'home.feature3.title': 'Công thức phù hợp với gia đình và sinh viên',
                'home.feature3.desc': 'Công thức đơn giản hoàn hảo cho lối sống bận rộn với thiết bị tối thiểu và dinh dưỡng tối đa cho cả gia đình',
                
                // Chat
                'chat.title': 'Trợ lý AI NomNomNomotron',
                'chat.subtitle': 'Hỏi tôi về công thức, lập kế hoạch bữa ăn, hoặc mẹo mua sắm!',
                'chat.placeholder': 'Nhập tin nhắn của bạn ở đây...',
                'chat.intro': 'Xin chào! Tôi là trợ lý AI NomNomNomotron được hỗ trợ bởi công nghệ NVIDIA. Tôi có thể giúp bạn:',
                
                // Common
                'common.loading': 'Đang tải...',
                'common.error': 'Lỗi tải nội dung',
                'common.save': 'Lưu',
                'common.cancel': 'Hủy',
                'common.clear': 'Xóa',
                'common.apply': 'Áp dụng',
                
                // Price disclaimer
                'disclaimer.title': 'Tuyên bố từ chối trách nhiệm về giá:',
                'disclaimer.text': 'Giá hiển thị là ước tính tổng quát dựa trên dữ liệu cửa hàng có sẵn và xu hướng gần đây. Ưu đãi, khuyến mãi và giá trong cửa hàng có thể thay đổi và có thể không được phản ánh theo thời gian thực. Sử dụng điều này như một công cụ lập kế hoạch và so sánh, không phải là đảm bảo về giá cuối cùng.'
            }
        };
        this.init();
    }

    init() {
        // Set up language selector
        const languageSelect = document.getElementById('language-select');
        if (languageSelect) {
            languageSelect.addEventListener('change', (e) => {
                this.changeLanguage(e.target.value);
            });
        }

        // Load saved language
        const savedLang = localStorage.getItem('nomnomn_language');
        if (savedLang && this.translations[savedLang]) {
            this.changeLanguage(savedLang);
        }
    }

    changeLanguage(langCode) {
        if (!this.translations[langCode]) return;
        
        this.currentLanguage = langCode;
        localStorage.setItem('nomnomn_language', langCode);
        
        // Update language selector
        const languageSelect = document.getElementById('language-select');
        if (languageSelect) {
            languageSelect.value = langCode;
        }
        
        // Translate all elements with data-translate attribute
        this.translatePage();
        
        // Update page title
        this.updatePageTitle();
    }

    translate(key) {
        const translation = this.translations[this.currentLanguage];
        return translation && translation[key] ? translation[key] : key;
    }

    translatePage() {
        // Find all elements with data-translate attribute
        document.querySelectorAll('[data-translate]').forEach(element => {
            const key = element.getAttribute('data-translate');
            const translation = this.translate(key);
            
            if (element.tagName === 'INPUT' && element.type === 'text') {
                element.placeholder = translation;
            } else {
                element.textContent = translation;
            }
        });

        // Special handling for specific elements
        this.translateSpecialElements();
    }

    translateSpecialElements() {
        // Update navigation
        const navLinks = {
            'home': 'nav.home',
            'chat': 'nav.chat',
            'meals': 'nav.meals',
            'profile': 'nav.profile',
            'meal-plan': 'nav.meal-plan',
            'recipes': 'nav.recipes'
        };

        Object.entries(navLinks).forEach(([page, key]) => {
            const link = document.querySelector(`[data-page="${page}"]`);
            if (link) {
                const icon = link.querySelector('i');
                const iconClass = icon ? icon.className : '';
                const translation = this.translate(key);
                if (icon) {
                    link.innerHTML = `<i class="${iconClass}"></i> ${translation}`;
                } else {
                    link.textContent = translation;
                }
            }
        });

        // Update brand name (keep as is - it's a brand name)
        // Update page content based on current page
        this.updateCurrentPageContent();
    }

    updateCurrentPageContent() {
        // Update content based on which page is currently active
        const activePage = document.querySelector('.page.active');
        if (!activePage) return;

        const pageId = activePage.id;
        
        if (pageId === 'sign-in-page') {
            this.updateSignInPage();
        } else if (pageId === 'home-page') {
            this.updateHomePage();
        } else if (pageId === 'chat-page') {
            this.updateChatPage();
        }
    }

    updateSignInPage() {
        // Update auth page elements
        const welcomeTitle = document.querySelector('.auth-card h2');
        if (welcomeTitle) {
            welcomeTitle.innerHTML = `<i class="fas fa-robot"></i> ${this.translate('auth.welcome')}`;
        }

        const subtitle = document.querySelector('.auth-subtitle');
        if (subtitle) {
            subtitle.textContent = this.translate('auth.subtitle');
        }

        // Update form labels and buttons
        const emailLabel = document.querySelector('label[for="email"]');
        if (emailLabel) emailLabel.textContent = this.translate('auth.email');

        const passwordLabel = document.querySelector('label[for="password"]');
        if (passwordLabel) passwordLabel.textContent = this.translate('auth.password');

        const signInBtn = document.querySelector('button[type="submit"]');
        if (signInBtn) signInBtn.textContent = this.translate('auth.signin');

        const guestBtn = document.getElementById('guest-continue');
        if (guestBtn) guestBtn.textContent = this.translate('auth.guest');

        const note = document.querySelector('.auth-note strong');
        if (note && note.parentNode) {
            note.parentNode.innerHTML = `<strong>Note:</strong> ${this.translate('auth.note')}`;
        }
    }

    updateHomePage() {
        const heroTitle = document.querySelector('.hero-content h1');
        if (heroTitle) heroTitle.textContent = this.translate('home.title');

        const heroSubtitle = document.querySelector('.hero-content p');
        if (heroSubtitle) heroSubtitle.textContent = this.translate('home.subtitle');

        const aboutTitle = document.querySelector('.about-section h2');
        if (aboutTitle) aboutTitle.textContent = this.translate('home.about');

        // Update disclaimer
        const disclaimerTitle = document.querySelector('.price-disclaimer h4');
        if (disclaimerTitle) {
            disclaimerTitle.innerHTML = `<i class="fas fa-exclamation-triangle"></i> ${this.translate('disclaimer.title')}`;
        }

        const disclaimerText = document.querySelector('.price-disclaimer p');
        if (disclaimerText) disclaimerText.textContent = this.translate('disclaimer.text');
    }

    updateChatPage() {
        const chatTitle = document.querySelector('.chat-header h2');
        if (chatTitle) {
            chatTitle.innerHTML = `<i class="fas fa-robot"></i> ${this.translate('chat.title')}`;
        }

        const chatSubtitle = document.querySelector('.chat-header p');
        if (chatSubtitle) chatSubtitle.textContent = this.translate('chat.subtitle');

        const chatInput = document.getElementById('chat-input');
        if (chatInput) chatInput.placeholder = this.translate('chat.placeholder');
    }

    updatePageTitle() {
        // Update browser title
        document.title = document.title.replace(/^.*? - /, `${this.translate('nav.home')} - `);
    }

    // Location functionality
    setupLocationHandling() {
        const zipInput = document.getElementById('zip-input');
        const mileRange = document.getElementById('mile-range');
        
        if (zipInput) {
            zipInput.addEventListener('change', () => {
                this.updateLocation(zipInput.value, mileRange.value);
            });
        }
        
        if (mileRange) {
            mileRange.addEventListener('change', () => {
                this.updateLocation(zipInput.value, mileRange.value);
            });
        }
    }
    
    updateLocation(zipCode, mileRange) {
        // Save location preferences
        localStorage.setItem('nomnomn_zip', zipCode);
        localStorage.setItem('nomnomn_miles', mileRange);
        
        // Update UI or trigger search updates
        console.log(`Location updated: ${zipCode}, ${mileRange} miles`);
        
        // Could trigger nearby store updates, price updates, etc.
        if (window.apiManager) {
            // window.apiManager.updateLocation(zipCode, mileRange);
        }
    }
}

// Initialize language manager
window.languageManager = new LanguageManager();

// Set up location handling when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    if (window.languageManager) {
        window.languageManager.setupLocationHandling();
    }
});