// API Service Layer for CareerConnect MVP Integration

const SPRING_BOOT_BASE_URL = 'http://localhost:8080/api';
const PYTHON_AI_BASE_URL = 'http://localhost:5000';

class ApiService {
  // Spring Boot Auth API
  async login(credentials) {
    try {
      const response = await fetch(`${SPRING_BOOT_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Cache-Control': 'no-cache',
        },
        credentials: 'include',
        body: JSON.stringify(credentials),
      });

      if (!response.ok) {
        throw new Error(`Login failed: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Login API error:', error);
      // Fallback to mock for MVP
      return {
        token: 'mock_jwt_token_' + Date.now(),
        user: {
          id: 'u_' + Date.now(),
          name: credentials.username,
          email: credentials.username + '@example.com'
        }
      };
    }
  }

  async register(userData) {
    try {
      const response = await fetch(`${SPRING_BOOT_BASE_URL}/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Cache-Control': 'no-cache',
        },
        credentials: 'include',
        body: JSON.stringify(userData),
      });

      if (!response.ok) {
        throw new Error(`Registration failed: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Registration API error:', error);
      // Fallback to mock for MVP
      return {
        id: 'u_' + Date.now(),
        name: userData.name,
        email: userData.email
      };
    }
  }

  // Python AI Chat API
  async sendChatMessage(message, profileData = null) {
    try {
      const response = await fetch(`${PYTHON_AI_BASE_URL}/api/v1/chat`, {
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

      if (!response.ok) {
        throw new Error(`Chat API failed: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Chat API error:', error);
      // Fallback to mock response for MVP
      return {
        response: this.generateMockChatResponse(message),
        timestamp: new Date().toISOString()
      };
    }
  }

  // Spring Boot Assessment API
  async submitAssessment(assessmentData) {
    try {
      const response = await fetch(`${SPRING_BOOT_BASE_URL}/assessments/submit`, {
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

      if (!response.ok) {
        throw new Error(`Assessment submission failed: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Assessment API error:', error);
      // Fallback to mock for MVP
      return {
        score: Math.floor(Math.random() * 100) + 1,
        recommendations: this.generateMockRecommendations(assessmentData),
        analysisId: 'analysis_' + Date.now()
      };
    }
  }

  // Python AI Career Analysis
  async getCareerAnalysis(profileData) {
    try {
      const response = await fetch(`${PYTHON_AI_BASE_URL}/api/v1/careers/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Cache-Control': 'no-cache',
        },
        credentials: 'include',
        body: JSON.stringify(profileData),
      });

      if (!response.ok) {
        throw new Error(`Career analysis failed: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Career analysis API error:', error);
      // Fallback to mock for MVP
      return {
        topCareers: [
          { name: 'Software Engineer', match: 85, description: 'Build software applications and systems' },
          { name: 'Data Scientist', match: 78, description: 'Analyze data to extract insights' },
          { name: 'Product Manager', match: 72, description: 'Manage product development lifecycle' }
        ],
        personalityProfile: 'RIASEC Analysis based on your interests and skills',
        learningPath: 'Recommended courses and skills to develop'
      };
    }
  }

  // Health check endpoints
  async checkSpringBootHealth() {
    try {
      const response = await fetch(`${SPRING_BOOT_BASE_URL}/health`);
      return response.ok;
    } catch (error) {
      console.log('Spring Boot service not available');
      return false;
    }
  }

  async checkPythonAIHealth() {
    try {
      const response = await fetch(`${PYTHON_AI_BASE_URL}/health`);
      return response.ok;
    } catch (error) {
      console.log('Python AI service not available');
      return false;
    }
  }

  // Mock response generators for fallback
  generateMockChatResponse(message) {
    const responses = [
      "That's a great question about your career! Based on your interests, I'd suggest exploring technology and innovation fields.",
      "Career planning is important. Have you considered taking our assessment to discover your strengths?",
      "Your career journey is unique. I'm here to help you navigate the possibilities ahead.",
      "Let's explore different career paths that match your personality and skills.",
      "Education and continuous learning are key to career success. What subjects interest you most?"
    ];

    if (message.toLowerCase().includes('career')) {
      return "🎯 " + responses[0];
    } else if (message.toLowerCase().includes('college') || message.toLowerCase().includes('education')) {
      return "🎓 " + responses[4];
    } else if (message.toLowerCase().includes('assessment') || message.toLowerCase().includes('test')) {
      return "📊 " + responses[1];
    } else {
      return responses[Math.floor(Math.random() * responses.length)];
    }
  }

  generateMockRecommendations(assessmentData) {
    return [
      'Consider exploring careers in Technology and Engineering',
      'Your analytical skills suggest Data Science or Research roles',
      'Leadership qualities indicate Management or Entrepreneurship potential',
      'Creative thinking aligns with Design or Media careers'
    ];
  }
}

export default new ApiService();