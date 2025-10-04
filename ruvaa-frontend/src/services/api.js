// API Service Layer for CareerConnect - Real Backend Integration
// Fully updated to work with deployed Spring Boot backend

// Deployed backend URLs
const SPRING_BOOT_BASE_URL = 'https://careerconnect-4bi9.onrender.com/api';
const PYTHON_AI_BASE_URL = 'https://ruvva.onrender.com'; // replace with deployed Python AI URL

class ApiService {
  constructor() {
    console.log("🚀 CareerConnect API Service initialized");
    console.log("📡 Spring Boot Backend:", SPRING_BOOT_BASE_URL);
    console.log("🤖 Python AI Backend:", PYTHON_AI_BASE_URL);
  }

  // ---------------- Authentication ----------------

  async login(credentials) {
    const endpoint = `${SPRING_BOOT_BASE_URL}/auth/login`;
    console.log("📤 API Request: POST", endpoint);

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify(credentials),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Login failed: ${response.status} - ${errorText}`);
      }

      const data = await response.json();
      if (data.token) localStorage.setItem('authToken', data.token);

      return data;
    } catch (error) {
      console.error("❌ Login API error:", error.message);
      throw error;
    }
  }

  async register(userData) {
    const endpoint = `${SPRING_BOOT_BASE_URL}/auth/register`;
    console.log("📤 API Request: POST", endpoint);

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify(userData),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Registration failed: ${response.status} - ${errorText}`);
      }

      return await response.json();
    } catch (error) {
      console.error("❌ Registration API error:", error.message);
      throw error;
    }
  }

  // ---------------- Python AI APIs ----------------

  async sendChatMessage(message, profileData = null) {
    if (!PYTHON_AI_BASE_URL) throw new Error("Python AI backend URL not set");

    const endpoint = `${PYTHON_AI_BASE_URL}/api/v1/chat`;
    console.log("📤 API Request: POST", endpoint);

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify({ message, profile: profileData }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Chat API failed: ${response.status} - ${errorText}`);
      }

      return await response.json();
    } catch (error) {
      console.error("❌ Chat API error:", error.message);
      throw error;
    }
  }

  async getCareerAnalysis(profileData) {
    if (!PYTHON_AI_BASE_URL) throw new Error("Python AI backend URL not set");

    const endpoint = `${PYTHON_AI_BASE_URL}/api/v1/careers/analyze`;

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify(profileData),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Career analysis failed: ${response.status} - ${errorText}`);
      }

      return await response.json();
    } catch (error) {
      console.error("❌ Career analysis API error:", error.message);
      throw error;
    }
  }

  // ---------------- CareerConnect APIs ----------------

  async getCareerRecommendations(profileData) {
    const endpoint = `${SPRING_BOOT_BASE_URL}/careers/recommendations`;

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('authToken') || ''}`,
        },
        body: JSON.stringify(profileData),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Career recommendations failed: ${response.status} - ${errorText}`);
      }

      return await response.json();
    } catch (error) {
      console.error("❌ Career recommendations API error:", error.message);
      throw error;
    }
  }

  async getColleges(filters = {}) {
    const params = new URLSearchParams(filters);
    const endpoint = `${SPRING_BOOT_BASE_URL}/colleges?${params}`;

    try {
      const response = await fetch(endpoint, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('authToken') || ''}`,
        },
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Get colleges failed: ${response.status} - ${errorText}`);
      }

      return await response.json();
    } catch (error) {
      console.error("❌ Get colleges API error:", error.message);
      throw error;
    }
  }

  async getMentors() {
    const endpoint = `${SPRING_BOOT_BASE_URL}/mentors`;

    try {
      const response = await fetch(endpoint, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('authToken') || ''}`,
        },
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Get mentors failed: ${response.status} - ${errorText}`);
      }

      return await response.json();
    } catch (error) {
      console.error("❌ Get mentors API error:", error.message);
      throw error;
    }
  }

  async bookMentorSession(bookingData) {
    const endpoint = `${SPRING_BOOT_BASE_URL}/mentors/book`;

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('authToken') || ''}`,
        },
        body: JSON.stringify(bookingData),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Book mentor failed: ${response.status} - ${errorText}`);
      }

      return await response.json();
    } catch (error) {
      console.error("❌ Book mentor API error:", error.message);
      throw error;
    }
  }

  async submitAssessment(assessmentData) {
    const endpoint = `${SPRING_BOOT_BASE_URL}/assessments/submit`;

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('authToken') || ''}`,
        },
        body: JSON.stringify(assessmentData),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Assessment submission failed: ${response.status} - ${errorText}`);
      }

      return await response.json();
    } catch (error) {
      console.error("❌ Assessment API error:", error.message);
      throw error;
    }
  }

  // ---------------- Health Checks ----------------

  async checkSpringBootHealth() {
    const endpoint = `${SPRING_BOOT_BASE_URL}/actuator/health`; // actuator endpoint
    try {
      const response = await fetch(endpoint, { method: 'GET' });
      return response.ok;
    } catch (error) {
      console.error("❌ Spring Boot Backend: Disconnected -", error.message);
      return false;
    }
  }

  async checkPythonAIHealth() {
    if (!PYTHON_AI_BASE_URL) return false;
    try {
      const response = await fetch(`${PYTHON_AI_BASE_URL}/health`, { method: 'GET' });
      return response.ok;
    } catch (error) {
      console.error("❌ Python AI Backend: Disconnected -", error.message);
      return false;
    }
  }

  async checkAllServices() {
    console.log("🔍 Checking all backend services...");
    const [springBoot, pythonAI] = await Promise.all([
      this.checkSpringBootHealth(),
      this.checkPythonAIHealth()
    ]);

    const status = { springBoot, pythonAI, allHealthy: springBoot && pythonAI };
    console.log("📊 Backend Status Summary:", status);
    return status;
  }
}

export default new ApiService();
