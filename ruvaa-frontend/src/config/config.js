// Environment Configuration for CareerConnect Frontend
export const config = {
  // API Configuration
  apis: {
    springBoot: process.env.REACT_APP_SPRING_BOOT_API || 'https://ruvva-32l2.onrender.com/api',
    pythonAI: process.env.REACT_APP_PYTHON_AI_API || 'https://ruvva.onrender.com',
    local: process.env.REACT_APP_LOCAL_API || 'http://localhost:8000/api'
  },

  // Firebase Configuration
  firebase: {
    apiKey: process.env.REACT_APP_FIREBASE_API_KEY || "AIzaSyCGo2KpKAMGU7b52skjDvAiFd6CE-v7Ohs",
    projectId: process.env.REACT_APP_FIREBASE_PROJECT_ID || "ruvaa-cbcaa",
    databaseURL: process.env.REACT_APP_FIREBASE_DATABASE_URL || "https://ruvaa-cbcaa-default-rtdb.asia-southeast1.firebasedatabase.app/",
    storageBucket: process.env.REACT_APP_FIREBASE_STORAGE_BUCKET || "ruvaa-cbcaa.appspot.com"
  },

  // Google Services
  google: {
    mapsApiKey: process.env.REACT_APP_GOOGLE_MAPS_API_KEY,
    geminiApiKey: process.env.REACT_APP_GEMINI_API_KEY || "AIzaSyAdwZVfqlTUbxsCEaSZIJM7FMiC7eSajyY"
  },

  // Feature Flags
  features: {
    locationDetection: process.env.REACT_APP_ENABLE_LOCATION_DETECTION !== 'false',
    multiLanguage: process.env.REACT_APP_ENABLE_MULTILANGUAGE !== 'false',
    search: process.env.REACT_APP_ENABLE_SEARCH !== 'false',
    analytics: process.env.REACT_APP_ENABLE_ANALYTICS !== 'false'
  },

  // Application Limits
  limits: {
    maxCareerSelections: parseInt(process.env.REACT_APP_MAX_CAREER_SELECTIONS) || 2,
    tokenLimit: parseInt(process.env.REACT_APP_TOKEN_LIMIT) || 4000,
    cacheTTL: parseInt(process.env.REACT_APP_CACHE_TTL) || 3600,
    sessionTimeout: parseInt(process.env.REACT_APP_SESSION_TIMEOUT) || 1800000
  },

  // Internationalization
  i18n: {
    defaultLanguage: process.env.REACT_APP_DEFAULT_LANGUAGE || 'en',
    supportedLanguages: (process.env.REACT_APP_SUPPORTED_LANGUAGES || 'en,hi,ml,ta,te,bn,gu,mr,pa').split(','),
    fallbackLanguage: 'en'
  },

  // UI Configuration
  ui: {
    defaultTheme: process.env.REACT_APP_DEFAULT_THEME || 'light',
    animationsEnabled: process.env.REACT_APP_DISABLE_ANIMATIONS !== 'true'
  },

  // Development Settings
  dev: {
    debugMode: process.env.REACT_APP_DEBUG_MODE === 'true' || process.env.NODE_ENV === 'development',
    logLevel: process.env.REACT_APP_LOG_LEVEL || 'info'
  },

  // Location Services
  location: {
    autoDetect: true,
    fallbackCity: 'Mumbai',
    fallbackCountry: 'India',
    timeout: 10000
  },

  // Cache Configuration
  cache: {
    enabled: true,
    prefix: 'cc_',
    ttl: 3600000, // 1 hour in milliseconds
    maxSize: 50 // Max cached items
  }
};

export default config;