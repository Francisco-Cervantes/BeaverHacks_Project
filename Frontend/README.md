# BeaverEats Frontend

A modern, responsive web application for student meal planning and grocery shopping, designed for BeaverHacks 2026.

## Features

- **Smart Meal Planning**: Weekly meal planning with drag-and-drop interface
- **Recipe Discovery**: Browse and filter recipes by cooking time, equipment, and dietary restrictions
- **AI Chat Assistant**: Get personalized meal suggestions and cooking tips
- **User Profiles**: Manage dietary restrictions, preferences, and cooking equipment
- **Shopping Lists**: Generate smart shopping lists based on meal plans
- **Price Comparison**: Find the best deals at nearby grocery stores
- **Mobile-First Design**: Fully responsive interface for all devices

## Pages

1. **Sign-In Page**: Authentication with guest mode option
2. **Home Page**: Landing page with features overview  
3. **Meals Page**: Browse available recipes with filtering
4. **Chat Page**: AI assistant for meal planning help
5. **Profile Page**: User preferences and dietary restrictions
6. **Meal Plan Page**: Weekly calendar with meal scheduling
7. **Individual Meal Page**: Detailed recipe view with instructions

## Quick Start

### Backend Setup
1. Navigate to the Backend directory:
   ```bash
   cd Backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the FastAPI server:
   ```bash
   python main.py
   # or
   uvicorn main:app --reload
   ```

The backend will run on `http://localhost:8000`

### Frontend Setup
1. Navigate to the Frontend directory:
   ```bash
   cd Frontend
   ```

2. Serve the files using a local server:
   ```bash
   # Using Python
   python -m http.server 8080
   
   # Using Node.js
   npx serve .
   
   # Using VS Code Live Server extension
   # Right-click index.html → "Open with Live Server"
   ```

3. Open your browser to `http://localhost:8080`

## Architecture

### Frontend Structure
```
Frontend/
├── index.html          # Main HTML file
├── styles/
│   └── main.css       # Complete styling
└── js/
    ├── app.js         # Main application initialization
    ├── auth.js        # Authentication management
    ├── navigation.js  # Page routing and navigation
    ├── api.js         # Backend API communication
    ├── profile.js     # User profile management
    └── meal-plan.js   # Meal planning functionality
```

### Backend Integration
The frontend communicates with the FastAPI backend through:
- `/meals` - Get all available meals
- `/available-meals` - Get filtered meals
- `/meal-costs` - Get pricing information
- `/shopping-list` - Generate shopping lists
- `/total-cost` - Calculate total meal costs

### Offline Mode
If the backend is unavailable, the frontend automatically switches to mock data mode, allowing full functionality during development or network issues.

## Key Features

### Authentication System
- Sign in with email/password
- Guest mode for limited features
- Persistent login state
- Protected routes for meal planning

### Meal Planning
- Weekly calendar view
- Drag-and-drop meal assignment
- Auto-fill week functionality
- Shopping list generation
- Cost estimation

### Recipe Management
- Filter by cooking time
- Filter by available equipment
- Dietary restriction filtering
- Detailed recipe view with step-by-step instructions

### User Profile
- Dietary preferences and restrictions
- Available cooking equipment
- Budget settings
- Calorie targets

### Chat Assistant
- AI-powered meal suggestions
- Cooking tips and advice
- Recipe recommendations
- Ingredient substitutions

## Browser Compatibility

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Mobile Support

The application is fully responsive and optimized for:
- Phones (320px+)
- Tablets (768px+)
- Desktops (1024px+)

## Development

### Adding New Features
1. Create new JavaScript modules in `/js/`
2. Add CSS styles to `/styles/main.css`
3. Register page loaders in `navigation.js`
4. Update API endpoints in `api.js`

### Testing
- Use browser developer tools for debugging
- Check console for error messages
- Test offline mode by stopping the backend
- Use mobile device simulation for responsive testing

## Performance Features

- Lazy loading of page content
- Efficient DOM manipulation
- Local storage for user preferences
- Service worker ready (for PWA conversion)
- Optimized for Core Web Vitals

## Security

- XSS protection through safe DOM manipulation
- Input validation and sanitization
- Secure authentication flow
- Local storage encryption ready

## Deployment

### Production Build
1. Minify CSS and JavaScript files
2. Optimize images and assets
3. Configure proper CORS headers
4. Set up HTTPS
5. Configure service worker for caching

### Hosting Options
- GitHub Pages (static hosting)
- Netlify or Vercel (with backend proxy)
- Traditional web hosting
- Docker containerization

## Contributing

This project was created for BeaverHacks 2026. To contribute:

1. Follow the existing code structure
2. Add comments for complex functionality
3. Test on multiple devices and browsers
4. Update documentation as needed

## License

Created for BeaverHacks 2026 - Oregon State University