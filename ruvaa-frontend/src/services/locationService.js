import { useState, useEffect } from 'react';
import config from '../config/config';

export const LocationService = {
  // Get current location using browser geolocation API
  getCurrentLocation: () => {
    return new Promise((resolve, reject) => {
      if (!navigator.geolocation) {
        reject(new Error('Geolocation is not supported by this browser'));
        return;
      }

      const options = {
        enableHighAccuracy: true,
        timeout: config.location.timeout,
        maximumAge: 600000 // 10 minutes
      };

      navigator.geolocation.getCurrentPosition(
        async (position) => {
          const { latitude, longitude } = position.coords;
          
          try {
            // Reverse geocoding to get city and state
            const locationData = await LocationService.reverseGeocode(latitude, longitude);
            resolve({
              coords: { latitude, longitude },
              ...locationData
            });
          } catch (error) {
            // Fallback to coordinates only
            resolve({
              coords: { latitude, longitude },
              city: config.location.fallbackCity,
              state: '',
              country: config.location.fallbackCountry
            });
          }
        },
        (error) => {
          reject(new Error(`Location access denied: ${error.message}`));
        },
        options
      );
    });
  },

  // Reverse geocoding using a public API
  reverseGeocode: async (lat, lng) => {
    try {
      // Using OpenStreetMap Nominatim API (free, no API key required)
      const response = await fetch(
        `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&addressdetails=1`
      );
      
      if (!response.ok) throw new Error('Geocoding failed');
      
      const data = await response.json();
      const address = data.address || {};
      
      return {
        city: address.city || address.town || address.village || address.hamlet || '',
        state: address.state || address.province || '',
        country: address.country || 'India',
        postal_code: address.postcode || '',
        formatted_address: data.display_name || ''
      };
    } catch (error) {
      console.warn('Reverse geocoding failed:', error);
      throw error;
    }
  },

  // Indian cities database for manual selection
  getIndianCities: () => [
    // Metro Cities
    'Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Ahmedabad',
    
    // Major Cities
    'Surat', 'Jaipur', 'Lucknow', 'Kanpur', 'Nagpur', 'Indore', 'Thane', 'Bhopal', 'Visakhapatnam', 'Pimpri-Chinchwad',
    'Patna', 'Vadodara', 'Ghaziabad', 'Ludhiana', 'Agra', 'Nashik', 'Faridabad', 'Meerut', 'Rajkot', 'Kalyan-Dombivali',
    
    // Other Important Cities
    'Vasai-Virar', 'Varanasi', 'Srinagar', 'Dhanbad', 'Jodhpur', 'Amritsar', 'Raipur', 'Allahabad', 'Coimbatore', 'Jabalpur',
    'Gwalior', 'Vijayawada', 'Madurai', 'Guwahati', 'Chandigarh', 'Hubli-Dharwad', 'Mysore', 'Tiruchirappalli', 'Bareilly', 'Aligarh',
    
    // State Capitals and Important Cities
    'Moradabad', 'Jalandhar', 'Bhubaneswar', 'Salem', 'Warangal', 'Guntur', 'Bhiwandi', 'Saharanpur', 'Gorakhpur', 'Bikaner',
    'Amravati', 'Noida', 'Jamshedpur', 'Bhilai', 'Cuttack', 'Firozabad', 'Kochi', 'Nellore', 'Bhavnagar', 'Dehradun',
    'Durgapur', 'Asansol', 'Rourkela', 'Nanded', 'Kolhapur', 'Ajmer', 'Akola', 'Gulbarga', 'Jamnagar', 'Ujjain',
    'Loni', 'Siliguri', 'Jhansi', 'Ulhasnagar', 'Jammu', 'Sangli-Miraj & Kupwad', 'Mangalore', 'Erode', 'Belgaum', 'Ambattur',
    'Tirunelveli', 'Malegaon', 'Gaya', 'Jalgaon', 'Udaipur', 'Maheshtala', 'Davanagere', 'Kozhikode', 'Kurnool', 'Rajpur Sonarpur'
  ],

  // Get states and their languages
  getStatesWithLanguages: () => ({
    'Andhra Pradesh': ['te', 'en'], // Telugu, English
    'Arunachal Pradesh': ['en', 'hi'], // English, Hindi
    'Assam': ['as', 'bn', 'en'], // Assamese, Bengali, English
    'Bihar': ['hi', 'bh', 'en'], // Hindi, Bhojpuri, English
    'Chhattisgarh': ['hi', 'en'], // Hindi, English
    'Goa': ['ko', 'mr', 'en'], // Konkani, Marathi, English
    'Gujarat': ['gu', 'hi', 'en'], // Gujarati, Hindi, English
    'Haryana': ['hi', 'pa', 'en'], // Hindi, Punjabi, English
    'Himachal Pradesh': ['hi', 'en'], // Hindi, English
    'Jharkhand': ['hi', 'en'], // Hindi, English
    'Karnataka': ['kn', 'en'], // Kannada, English
    'Kerala': ['ml', 'en'], // Malayalam, English
    'Madhya Pradesh': ['hi', 'en'], // Hindi, English
    'Maharashtra': ['mr', 'hi', 'en'], // Marathi, Hindi, English
    'Manipur': ['mni', 'en'], // Manipuri, English
    'Meghalaya': ['en'], // English
    'Mizoram': ['lus', 'en'], // Mizo, English
    'Nagaland': ['en'], // English
    'Odisha': ['or', 'hi', 'en'], // Odia, Hindi, English
    'Punjab': ['pa', 'hi', 'en'], // Punjabi, Hindi, English
    'Rajasthan': ['hi', 'en'], // Hindi, English
    'Sikkim': ['ne', 'hi', 'en'], // Nepali, Hindi, English
    'Tamil Nadu': ['ta', 'en'], // Tamil, English
    'Telangana': ['te', 'hi', 'en'], // Telugu, Hindi, English
    'Tripura': ['bn', 'ko', 'en'], // Bengali, Kokborok, English
    'Uttar Pradesh': ['hi', 'ur', 'en'], // Hindi, Urdu, English
    'Uttarakhand': ['hi', 'en'], // Hindi, English
    'West Bengal': ['bn', 'hi', 'en'], // Bengali, Hindi, English
    'Delhi': ['hi', 'pa', 'ur', 'en'], // Hindi, Punjabi, Urdu, English
  }),

  // Detect language based on location
  getLanguageFromLocation: (state) => {
    const stateLanguages = LocationService.getStatesWithLanguages();
    const languages = stateLanguages[state];
    
    if (languages && languages.length > 0) {
      // Return the primary local language (first in array)
      return languages[0];
    }
    
    // Fallback to English
    return 'en';
  }
};

// Location Hook for React Components
export const useLocation = () => {
  const [location, setLocation] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const detectLocation = async () => {
    if (!config.features.locationDetection) {
      setError('Location detection is disabled');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const locationData = await LocationService.getCurrentLocation();
      setLocation(locationData);
      
      // Save to localStorage
      localStorage.setItem('cc_location', JSON.stringify(locationData));
      
      return locationData;
    } catch (err) {
      setError(err.message);
      console.error('Location detection failed:', err);
    } finally {
      setLoading(false);
    }
  };

  const setManualLocation = (city, state, country = 'India') => {
    const locationData = {
      city,
      state,
      country,
      manual: true,
      timestamp: Date.now()
    };
    
    setLocation(locationData);
    localStorage.setItem('cc_location', JSON.stringify(locationData));
    setError(null);
    
    return locationData;
  };

  const clearLocation = () => {
    setLocation(null);
    setError(null);
    localStorage.removeItem('cc_location');
  };

  // Load saved location on mount
  useEffect(() => {
    const savedLocation = localStorage.getItem('cc_location');
    if (savedLocation) {
      try {
        const locationData = JSON.parse(savedLocation);
        // Check if location is less than 24 hours old
        const isRecent = locationData.timestamp && 
          (Date.now() - locationData.timestamp) < 24 * 60 * 60 * 1000;
        
        if (isRecent || locationData.manual) {
          setLocation(locationData);
        }
      } catch (error) {
        console.error('Failed to parse saved location:', error);
        localStorage.removeItem('cc_location');
      }
    }
  }, []);

  return {
    location,
    loading,
    error,
    detectLocation,
    setManualLocation,
    clearLocation,
    cities: LocationService.getIndianCities(),
    states: Object.keys(LocationService.getStatesWithLanguages())
  };
};

export default LocationService;