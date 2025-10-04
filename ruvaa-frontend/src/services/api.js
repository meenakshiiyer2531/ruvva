// API Service Layer for CareerConnect - Real Backend Integration
// All mock data removed - requires backend connection
// Use deployed Spring Boot Backend
const SPRING_BOOT_BASE_URL = 'https://careerconnect-4bi9.onrender.com/api';
const PYTHON_AI_BASE_URL = 'http://localhost:5000';

class ApiService {
  constructor() {
    console.log("🚀 CareerConnect API Service initialized");
    console.log("📡 Spring Boot Backend:", SPRING_BOOT_BASE_URL);
    console.log("🤖 Python AI Backend:", PYTHON_AI_BASE_URL);
  }

  // Spring Boot Auth API - Login
  async login(credentials) {
    const endpoint = `${SPRING_BOOT_BASE_URL}/auth/login`;
    console.log("📤 API Request: POST", endpoint);
    console.log("📦 Payload:", { username: credentials.username, password: "***" });

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Cache-Control': 'no-cache',
        },
        credentials: 'include',
        body: JSON.stringify(credentials),
      });

      console.log("📥 Response Status:", response.status, response.statusText);

      if (!response.ok) {
        const errorText = await response.text();
        console.error("❌ Login failed:", response.status, errorText);
        throw new Error(`Login failed: ${response.status} - ${errorText}`);
      }

      const data = await response.json();
      console.log("✅ Login successful:", data);
      console.log("🔑 Token received:", data.token ? "Yes" : "No");

      // Store token
      if (data.token) {
        localStorage.setItem('authToken', data.token);
      }

      return data;
    } catch (error) {
      console.error("❌ Login API error:", error.message);
      console.error("🔌 Backend Status: Spring Boot appears to be disconnected");
      throw error;
    }
  }

  // Spring Boot Auth API - Register
  async register(userData) {
    const endpoint = `${SPRING_BOOT_BASE_URL}/auth/register`;
    console.log("📤 API Request: POST", endpoint);
    console.log("📦 Payload:", { name: userData.name, email: userData.email, password: "***" });

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Cache-Control': 'no-cache',
        },
        credentials: 'include',
        body: JSON.stringify(userData),
      });

      console.log("📥 Response Status:", response.status, response.statusText);

      if (!response.ok) {
        const errorText = await response.text();
        console.error("❌ Registration failed:", response.status, errorText);
        throw new Error(`Registration failed: ${response.status} - ${errorText}`);
      }

      const data = await response.json();
      console.log("✅ Registration successful:", data);

      return data;
    } catch (error) {
      console.error("❌ Registration API error:", error.message);
      console.error("🔌 Backend Status: Spring Boot appears to be disconnected");
      throw error;
    }
  }

  // Python AI Chat API
  async sendChatMessage(message, profileData = null) {
    const endpoint = `${PYTHON_AI_BASE_URL}/api/v1/chat`;
    console.log("📤 API Request: POST", endpoint);
    console.log("📦 Payload:", { message, profile: profileData ? "included" : "none" });

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Cache-Control': 'no-cache',
        },
        credentials: 'include',
        body: JSON.stringify({
          message: message,
          profile: profileData
        }),
      });

      console.log("📥 Response Status:", response.status, response.statusText);

      if (!response.ok) {
        const errorText = await response.text();
        console.error("❌ Chat API failed:", response.status, errorText);
        throw new Error(`Chat failed: ${response.status} - ${errorText}`);
      }

      const data = await response.json();
      console.log("✅ Chat response received:", data);

      return data;
    } catch (error) {
      console.error("❌ Chat API error:", error.message);
      console.error("🔌 Backend Status: Python AI appears to be disconnected");
      throw error;
    }
  }

  // Spring Boot Assessment API
  async submitAssessment(assessmentData) {
    const endpoint = `${SPRING_BOOT_BASE_URL}/assessments/submit`;
    console.log("📤 API Request: POST", endpoint);
    console.log("📦 Payload:", assessmentData);

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Authorization': 'Bearer ' + (localStorage.getItem('authToken') || ''),
          'Cache-Control': 'no-cache',
        },
        credentials: 'include',
        body: JSON.stringify(assessmentData),
      });

      console.log("📥 Response Status:", response.status, response.statusText);

      if (!response.ok) {
        const errorText = await response.text();
        console.error("❌ Assessment submission failed:", response.status, errorText);
        throw new Error(`Assessment failed: ${response.status} - ${errorText}`);
      }

      const data = await response.json();
      console.log("✅ Assessment submitted:", data);

      return data;
    } catch (error) {
      console.error("❌ Assessment API error:", error.message);
      console.error("🔌 Backend Status: Spring Boot appears to be disconnected");
      throw error;
    }
  }

  // Python AI Career Analysis
  async getCareerAnalysis(profileData) {
    const endpoint = `${PYTHON_AI_BASE_URL}/api/v1/careers/analyze`;
    console.log("📤 API Request: POST", endpoint);
    console.log("📦 Payload:", profileData);

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Cache-Control': 'no-cache',
        },
        credentials: 'include',
        body: JSON.stringify(profileData),
      });

      console.log("📥 Response Status:", response.status, response.statusText);

      if (!response.ok) {
        const errorText = await response.text();
        console.error("❌ Career analysis failed:", response.status, errorText);
        throw new Error(`Career analysis failed: ${response.status} - ${errorText}`);
      }

      const data = await response.json();
      console.log("✅ Career analysis received:", data);

      return data;
    } catch (error) {
      console.error("❌ Career analysis API error:", error.message);
      console.error("🔌 Backend Status: Python AI appears to be disconnected");
      throw error;
    }
  }

  // Get Career Recommendations
  async getCareerRecommendations(profileData) {
    const endpoint = `${SPRING_BOOT_BASE_URL}/careers/recommendations`;
    console.log("📤 API Request: POST", endpoint);
    console.log("📦 Payload:", profileData);

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Authorization': 'Bearer ' + (localStorage.getItem('authToken') || ''),
          'Cache-Control': 'no-cache',
        },
        credentials: 'include',
        body: JSON.stringify(profileData),
      });

      console.log("📥 Response Status:", response.status, response.statusText);

      if (!response.ok) {
        const errorText = await response.text();
        console.error("❌ Career recommendations failed:", response.status, errorText);
        throw new Error(`Career recommendations failed: ${response.status} - ${errorText}`);
      }

      const data = await response.json();
      console.log("✅ Career recommendations received:", data);

      return data;
    } catch (error) {
      console.error("❌ Career recommendations API error:", error.message);
      console.error("🔌 Backend Status: Spring Boot appears to be disconnected");
      throw error;
    }
  }

  // Get Colleges
  async getColleges(filters = {}) {
    const params = new URLSearchParams(filters);
    const endpoint = `${SPRING_BOOT_BASE_URL}/colleges?${params}`;
    console.log("📤 API Request: GET", endpoint);

    try {
      const response = await fetch(endpoint, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
          'Authorization': 'Bearer ' + (localStorage.getItem('authToken') || ''),
          'Cache-Control': 'no-cache',
        },
        credentials: 'include',
      });

      console.log("📥 Response Status:", response.status, response.statusText);

      if (!response.ok) {
        const errorText = await response.text();
        console.error("❌ Get colleges failed:", response.status, errorText);
        throw new Error(`Get colleges failed: ${response.status} - ${errorText}`);
      }

      const data = await response.json();
      console.log("✅ Colleges data received:", data);

      return data;
    } catch (error) {
      console.error("❌ Get colleges API error:", error.message);
      console.error("🔌 Backend Status: Spring Boot appears to be disconnected");
      throw error;
    }
  }

  // Get Mentors
  async getMentors() {
    const endpoint = `${SPRING_BOOT_BASE_URL}/mentors`;
    console.log("📤 API Request: GET", endpoint);

    try {
      const response = await fetch(endpoint, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
          'Authorization': 'Bearer ' + (localStorage.getItem('authToken') || ''),
          'Cache-Control': 'no-cache',
        },
        credentials: 'include',
      });

      console.log("📥 Response Status:", response.status, response.statusText);

      if (!response.ok) {
        const errorText = await response.text();
        console.error("❌ Get mentors failed:", response.status, errorText);
        throw new Error(`Get mentors failed: ${response.status} - ${errorText}`);
      }

      const data = await response.json();
      console.log("✅ Mentors data received:", data);

      return data;
    } catch (error) {
      console.error("❌ Get mentors API error:", error.message);
      console.error("🔌 Backend Status: Spring Boot appears to be disconnected");
      throw error;
    }
  }

  // Book Mentor Session
  async bookMentorSession(bookingData) {
    const endpoint = `${SPRING_BOOT_BASE_URL}/mentors/book`;
    console.log("📤 API Request: POST", endpoint);
    console.log("📦 Payload:", bookingData);

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Authorization': 'Bearer ' + (localStorage.getItem('authToken') || ''),
          'Cache-Control': 'no-cache',
        },
        credentials: 'include',
        body: JSON.stringify(bookingData),
      });

      console.log("📥 Response Status:", response.status, response.statusText);

      if (!response.ok) {
        const errorText = await response.text();
        console.error("❌ Book mentor failed:", response.status, errorText);
        throw new Error(`Book mentor failed: ${response.status} - ${errorText}`);
      }

      const data = await response.json();
      console.log("✅ Mentor session booked:", data);

      return data;
    } catch (error) {
      console.error("❌ Book mentor API error:", error.message);
      console.error("🔌 Backend Status: Spring Boot appears to be disconnected");
      throw error;
    }
  }

  // Health check endpoints
  async checkSpringBootHealth() {
    try {
      const response = await fetch(`${SPRING_BOOT_BASE_URL}/health`, {
        method: 'GET',
        cache: 'no-cache'
      });
      const isHealthy = response.ok;
      console.log(isHealthy ? "✅ Spring Boot Backend: Connected" : "❌ Spring Boot Backend: Unhealthy");
      return isHealthy;
    } catch (error) {
      console.log("❌ Spring Boot Backend: Disconnected -", error.message);
      return false;
    }
  }

  async checkPythonAIHealth() {
    try {
      const response = await fetch(`${PYTHON_AI_BASE_URL}/health`, {
        method: 'GET',
        cache: 'no-cache'
      });
      const isHealthy = response.ok;
      console.log(isHealthy ? "✅ Python AI Backend: Connected" : "❌ Python AI Backend: Unhealthy");
      return isHealthy;
    } catch (error) {
      console.log("❌ Python AI Backend: Disconnected -", error.message);
      return false;
    }
  }

  // Check all backend services
  async checkAllServices() {
    console.log("🔍 Checking all backend services...");
    const [springBoot, pythonAI] = await Promise.all([
      this.checkSpringBootHealth(),
      this.checkPythonAIHealth()
    ]);

    const status = {
      springBoot,
      pythonAI,
      allHealthy: springBoot && pythonAI
    };

    console.log("📊 Backend Status Summary:", status);
    return status;
  }
}

export default new ApiService();
