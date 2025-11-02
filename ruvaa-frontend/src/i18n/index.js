import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';
import Backend from 'i18next-http-backend';

// Import translation resources
import en from './locales/en.json';
import hi from './locales/hi.json';
import bn from './locales/bn.json';
import te from './locales/te.json';
import mr from './locales/mr.json';
import ta from './locales/ta.json';
import gu from './locales/gu.json';
import kn from './locales/kn.json';
import ml from './locales/ml.json';
import pa from './locales/pa.json';
import es from './locales/es.json';
import fr from './locales/fr.json';
import de from './locales/de.json';
import zh from './locales/zh.json';
import ja from './locales/ja.json';
import ar from './locales/ar.json';

// Location-based language mapping
const LOCATION_LANGUAGE_MAP = {
  // India - Default Hindi, but detect regional languages based on location
  'IN': 'hi',
  // Indian States with their primary languages
  'IN-WB': 'bn', // West Bengal - Bengali
  'IN-AP': 'te', // Andhra Pradesh - Telugu  
  'IN-TG': 'te', // Telangana - Telugu
  'IN-MH': 'mr', // Maharashtra - Marathi
  'IN-TN': 'ta', // Tamil Nadu - Tamil
  'IN-GJ': 'gu', // Gujarat - Gujarati
  'IN-KA': 'kn', // Karnataka - Kannada
  'IN-KL': 'ml', // Kerala - Malayalam
  'IN-PB': 'pa', // Punjab - Punjabi
  // Bangladesh
  'BD': 'bn',
  // Spanish-speaking countries
  'ES': 'es', 'MX': 'es', 'AR': 'es', 'CO': 'es', 'PE': 'es', 
  'VE': 'es', 'CL': 'es', 'EC': 'es', 'BO': 'es', 'PY': 'es',
  'UY': 'es', 'GY': 'es', 'SR': 'es', 'GF': 'es',
  // French-speaking countries
  'FR': 'fr', 'BE': 'fr', 'CH': 'fr', 'CA': 'fr', 'LU': 'fr',
  'MC': 'fr', 'SN': 'fr', 'CI': 'fr', 'BF': 'fr', 'ML': 'fr',
  // German-speaking countries  
  'DE': 'de', 'AT': 'de', 'LI': 'de',
  // Chinese-speaking regions
  'CN': 'zh', 'TW': 'zh', 'HK': 'zh', 'SG': 'zh', 'MO': 'zh',
  // Japanese
  'JP': 'ja',
  // Arabic-speaking countries
  'SA': 'ar', 'AE': 'ar', 'EG': 'ar', 'JO': 'ar', 'LB': 'ar',
  'SY': 'ar', 'IQ': 'ar', 'KW': 'ar', 'QA': 'ar', 'BH': 'ar',
  'OM': 'ar', 'YE': 'ar', 'LY': 'ar', 'TN': 'ar', 'DZ': 'ar',
  'MA': 'ar', 'SD': 'ar', 'SO': 'ar', 'DJ': 'ar', 'KM': 'ar'
};

// Get language based on location
const getLanguageFromLocation = () => {
  try {
    const location = JSON.parse(localStorage.getItem('cc_user_location') || '{}');
    const countryCode = location.country_code || location.countryCode;
    
    if (countryCode && LOCATION_LANGUAGE_MAP[countryCode.toUpperCase()]) {
      return LOCATION_LANGUAGE_MAP[countryCode.toUpperCase()];
    }
  } catch (error) {
    console.warn('Could not detect language from location:', error);
  }
  return 'en'; // Default to English
};

// Custom language detector that prioritizes location
const customLanguageDetector = {
  name: 'locationDetector',
  lookup() {
    // Priority: stored preference > location > browser > default
    const stored = localStorage.getItem('cc_language');
    if (stored) return stored;
    
    const locationLang = getLanguageFromLocation();
    if (locationLang !== 'en') return locationLang;
    
    // Fallback to browser language
    const browserLang = navigator.language?.split('-')[0];
    return ['en', 'hi', 'bn', 'te', 'mr', 'ta', 'gu', 'kn', 'ml', 'pa', 'es', 'fr', 'de', 'zh', 'ja', 'ar'].includes(browserLang) 
      ? browserLang 
      : 'en';
  },
  cacheUserLanguage(lng) {
    localStorage.setItem('cc_language', lng);
  }
};

i18n
  // Load translation resources directly
  .use({
    type: 'backend',
    read(language, namespace, callback) {
      const resources = { en, hi, bn, te, mr, ta, gu, kn, ml, pa, es, fr, de, zh, ja, ar };
      if (resources[language]) {
        callback(null, resources[language]);
      } else {
        callback(new Error(`Translation for ${language} not found`), null);
      }
    }
  })
  // Detect user language
  .use({
    ...LanguageDetector,
    detect: customLanguageDetector.lookup,
    cacheUserLanguage: customLanguageDetector.cacheUserLanguage
  })
  // Pass the i18n instance to react-i18next
  .use(initReactI18next)
  // Initialize i18next
  .init({
    lng: customLanguageDetector.lookup(), // Set initial language
    fallbackLng: 'en',
    debug: process.env.NODE_ENV === 'development',
    
    interpolation: {
      escapeValue: false // React already does escaping
    },

    // Language detection configuration
    detection: {
      order: ['localStorage', 'navigator', 'htmlTag'],
      lookupLocalStorage: 'cc_language',
      caches: ['localStorage'],
      excludeCacheFor: ['cimode']
    },

    // Backend configuration
    backend: {
      loadPath: '/locales/{{lng}}.json',
      crossDomain: true
    },

    // React configuration
    react: {
      useSuspense: false,
      bindI18n: 'languageChanged',
      bindI18nStore: '',
      transEmptyNodeValue: '',
      transSupportBasicHtmlNodes: true,
      transKeepBasicHtmlNodesFor: ['br', 'strong', 'i', 'em']
    }
  });

// Listen for location updates to adjust language
window.addEventListener('storage', (e) => {
  if (e.key === 'cc_user_location' && e.newValue) {
    const newLang = getLanguageFromLocation();
    const currentLang = i18n.language;
    
    // Only change if not manually set and different from current
    const isManuallySet = localStorage.getItem('cc_language_manual') === 'true';
    if (!isManuallySet && newLang !== currentLang) {
      i18n.changeLanguage(newLang);
    }
  }
});

export { LOCATION_LANGUAGE_MAP, getLanguageFromLocation };
export default i18n;