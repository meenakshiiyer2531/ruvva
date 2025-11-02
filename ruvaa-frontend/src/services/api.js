// API Service Layer for CareerConnect - Real Backend Integration
// Fully updated to work with deployed Spring Boot backend

// Environment-based configuration
const SPRING_BOOT_BASE_URL = process.env.REACT_APP_API_BASE || 'http://localhost:8080/api';
const PYTHON_AI_BASE_URL = process.env.REACT_APP_AI_BASE || '';

class ApiService {
  constructor() {
    this.baseUrl = SPRING_BOOT_BASE_URL;
    console.log('🚀 CareerConnect API Service initialized');
    console.log('📡 Spring Boot Backend:', this.baseUrl);
    if (PYTHON_AI_BASE_URL) console.log('🤖 Python AI Backend:', PYTHON_AI_BASE_URL);
  }

  async apiFetch(endpoint, options = {}) {
    const fullUrl = `${this.baseUrl}${endpoint}`;
    console.log('📤 API Request:', options.method || 'GET', fullUrl);
    const response = await fetch(fullUrl, options);
    if (!response.ok) {
      const text = await response.text().catch(() => '');
      throw new Error(`HTTP ${response.status}: ${response.statusText} - ${text}`);
    }
    return response;
  }
  // ---------------- Authentication ----------------
  async login(credentials) {
    try {
      const response = await this.apiFetch('/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify(credentials),
      });

      const data = await response.json();
      if (data.token) localStorage.setItem('authToken', data.token);
      console.log('✅ Login successful:', data);
      // Fetch user + profile if available (mock /auth/me uses email query)
      if (data.user && data.user.email) {
        const token = localStorage.getItem('authToken');
        try {
          const meResp = await this.apiFetch(`/auth/me?email=${encodeURIComponent(data.user.email)}`, {
            method: 'GET',
            headers: { 'Accept': 'application/json', 'Authorization': token ? `Bearer ${token}` : undefined }
          });
          const meData = await meResp.json();
          data.profile = meData.profile || {};
        } catch (e) {
          console.warn('⚠️ Unable to fetch /auth/me profile via email query:', e.message);
          // Attempt bearer-only resolution if first attempt failed
          if (token) {
            try {
              const bearerResp = await this.apiFetch('/auth/me', {
                method: 'GET',
                headers: { 'Accept': 'application/json', 'Authorization': `Bearer ${token}` }
              });
              const bearerData = await bearerResp.json();
              data.profile = bearerData.profile || data.profile || {};
            } catch (e2) {
              console.warn('⚠️ Bearer token /auth/me fallback failed:', e2.message);
            }
          }
        }
      }
      return data;
    } catch (error) {
      console.error('❌ Login API error:', error.message);
      throw error;
    }
  }

  async getCurrentUser(email) {
    if (!email) throw new Error('Email required to fetch current user in mock mode');
    const resp = await this.apiFetch(`/auth/me?email=${encodeURIComponent(email)}`, {
      method: 'GET',
      headers: { 'Accept': 'application/json' }
    });
    return resp.json();
  }
  async register(userData) {
    try {
      const response = await this.apiFetch('/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify(userData),
      });

      const result = await response.json();
      console.log("✅ Registration successful:", result);
      return result;
    } catch (error) {
      console.error("❌ Registration API error:", error.message);
      throw error;
    }
  }

  async studentRegister(studentData) {
    try {
      const response = await this.apiFetch('/students/register', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json', 
          'Accept': 'application/json'
        },
        body: JSON.stringify(studentData),
      });

      const result = await response.json();
      console.log("✅ Student Registration Response:", result);
      
      // Extract token if available in the response
      if (result.data && result.data.token) {
        localStorage.setItem('authToken', result.data.token);
      }
      
      return result;
    } catch (error) {
      console.error("❌ Student Registration API error:", error.message);
      throw error;
    }
  }

  async updateStudentProfile(studentId, profileData) {
    try {
      const response = await this.apiFetch(`/students/${studentId}/profile`, {
        method: 'PUT',
        headers: { 
          'Content-Type': 'application/json', 
          'Accept': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('authToken')}`
        },
        body: JSON.stringify(profileData),
      });

      const result = await response.json();
      console.log("✅ Profile Update Response:", result);
      return result;
    } catch (error) {
      console.error("❌ Profile Update API error:", error.message);
      throw error;
    }
  }

  // ----------- Student Profile CRUD (Mock Mode) -----------
  async createStudentProfile(studentId, profileData = {}) {
    const response = await this.apiFetch(`/students/${studentId}/profile`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('authToken') || ''}`
      },
      body: JSON.stringify(profileData)
    });
    return response.json();
  }

  async replaceStudentProfile(studentId, profileData = {}) {
    const response = await this.apiFetch(`/students/${studentId}/profile/replace`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('authToken') || ''}`
      },
      body: JSON.stringify(profileData)
    });
    return response.json();
  }

  async patchStudentProfile(studentId, partialProfile = {}) {
    const response = await this.apiFetch(`/students/${studentId}/profile`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('authToken') || ''}`
      },
      body: JSON.stringify(partialProfile)
    });
    return response.json();
  }

  async deleteStudentProfile(studentId) {
    const response = await this.apiFetch(`/students/${studentId}/profile`, {
      method: 'DELETE',
      headers: {
        'Accept': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('authToken') || ''}`
      }
    });
    return response.json();
  }

  async getStudentProfile(studentId) {
    const response = await this.apiFetch(`/students/${studentId}/profile`, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('authToken') || ''}`
      }
    });
    return response.json();
  }

  // Combined student retrieval (basic + profile) using new backend endpoint
  async getStudentCombined(studentId) {
    const response = await this.apiFetch(`/students/${studentId}`, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('authToken') || ''}`
      }
    });
    return response.json();
  }

  // ----- Assessment History (Mock Mode) -----
  async addAssessmentRun(studentId, runPayload) {
    const response = await this.apiFetch(`/students/${studentId}/assessments`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('authToken') || ''}`
      },
      body: JSON.stringify(runPayload || {})
    });
    return response.json();
  }
  async listAssessmentRuns(studentId) {
    const response = await this.apiFetch(`/students/${studentId}/assessments`, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('authToken') || ''}`
      }
    });
    return response.json();
  }

  async listStudentProfiles() {
    const response = await this.apiFetch('/students/profiles', {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('authToken') || ''}`
      }
    });
    return response.json();
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

  // --- Mentor Extended APIs (Mock Mode) ---
  async getMentor(mentorId) {
    const endpoint = `${SPRING_BOOT_BASE_URL}/mentors/${mentorId}`;
    const response = await fetch(endpoint, {
      method: 'GET',
      headers: { 'Accept': 'application/json', 'Authorization': `Bearer ${localStorage.getItem('authToken') || ''}` }
    });
    if (!response.ok) {
      throw new Error(`Get mentor failed: ${response.status}`);
    }
    return response.json();
  }

  async getMentorAvailability(mentorId) {
    const endpoint = `${SPRING_BOOT_BASE_URL}/mentors/${mentorId}/availability`;
    const response = await fetch(endpoint, {
      method: 'GET',
      headers: { 'Accept': 'application/json', 'Authorization': `Bearer ${localStorage.getItem('authToken') || ''}` }
    });
    if (!response.ok) throw new Error(`Get availability failed: ${response.status}`);
    return response.json();
  }

  async createMentorBooking(mentorId, { date, studentId, studentEmail }) {
    const endpoint = `${SPRING_BOOT_BASE_URL}/mentors/${mentorId}/bookings`;
    const payload = { date, studentId, studentEmail };
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('authToken') || ''}`,
      },
      body: JSON.stringify(payload)
    });
    if (!response.ok) {
      const text = await response.text();
      throw new Error(`Create mentor booking failed: ${response.status} - ${text}`);
    }
    return response.json();
  }

  async listMentorBookings(mentorId) {
    const endpoint = `${SPRING_BOOT_BASE_URL}/mentors/${mentorId}/bookings`;
    const response = await fetch(endpoint, {
      method: 'GET',
      headers: { 'Accept': 'application/json', 'Authorization': `Bearer ${localStorage.getItem('authToken') || ''}` }
    });
    if (!response.ok) throw new Error(`List mentor bookings failed: ${response.status}`);
    return response.json();
  }

  async listStudentBookings(studentId) {
    const endpoint = `${SPRING_BOOT_BASE_URL}/mentors/students/${studentId}/bookings`;
    const response = await fetch(endpoint, {
      method: 'GET',
      headers: { 'Accept': 'application/json', 'Authorization': `Bearer ${localStorage.getItem('authToken') || ''}` }
    });
    if (!response.ok) throw new Error(`List student bookings failed: ${response.status}`);
    return response.json();
  }
  // Booking detail
  async getBookingDetail(bookingId) {
    const endpoint = `${SPRING_BOOT_BASE_URL}/mentors/bookings/${bookingId}`;
    const response = await fetch(endpoint, {
      method: 'GET',
      headers: { 'Accept': 'application/json', 'Authorization': `Bearer ${localStorage.getItem('authToken') || ''}` }
    });
    if (!response.ok) throw new Error(`Get booking detail failed: ${response.status}`);
    return response.json();
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

const apiService = new ApiService();
export default apiService;
