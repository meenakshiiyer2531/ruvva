# API Documentation

## Overview

The Career Connect AI API provides endpoints for career guidance, assessment, and learning path generation. This document describes all available endpoints, their parameters, and responses.

## Base URL

```
https://api.careerconnectai.com
```

## Authentication

All API endpoints require authentication using a Bearer token in the Authorization header:

```
Authorization: Bearer <your-token>
```

## Endpoints

### Profile Management

#### Create Student Profile

**POST** `/api/profile/create`

Creates a new student profile with analysis.

**Request Body:**
```json
{
  "name": "John Doe",
  "age": 20,
  "grade": "12th",
  "interests": ["Technology", "Science"],
  "skills": ["Python", "Communication"],
  "learning_style": "Visual",
  "career_goals": ["Software Engineer"],
  "location": "New York",
  "contact_info": {
    "email": "john@example.com",
    "phone": "+1234567890"
  }
}
```

**Response:**
```json
{
  "success": true,
  "profile": {
    "id": 1,
    "name": "John Doe",
    "age": 20,
    "grade": "12th",
    "interests": ["Technology", "Science"],
    "skills": ["Python", "Communication"],
    "learning_style": "Visual",
    "career_goals": ["Software Engineer"],
    "location": "New York",
    "contact_info": {
      "email": "john@example.com",
      "phone": "+1234567890"
    },
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  },
  "analysis": {
    "personality_analysis": {
      "traits": ["Analytical", "Creative", "Detail-oriented"],
      "strengths": ["Problem-solving", "Communication", "Technical skills"],
      "areas_for_improvement": ["Leadership", "Time management"]
    },
    "career_analysis": {
      "suitable_careers": ["Software Engineer", "Data Scientist", "Product Manager"],
      "career_paths": ["Technical", "Management", "Entrepreneurship"],
      "recommendations": ["Focus on technical skills", "Develop leadership abilities"]
    }
  }
}
```

#### Get Student Profile

**GET** `/api/profile/{profile_id}`

Retrieves a student profile by ID.

**Response:**
```json
{
  "success": true,
  "profile": {
    "id": 1,
    "name": "John Doe",
    "age": 20,
    "grade": "12th",
    "interests": ["Technology", "Science"],
    "skills": ["Python", "Communication"],
    "learning_style": "Visual",
    "career_goals": ["Software Engineer"],
    "location": "New York",
    "contact_info": {
      "email": "john@example.com",
      "phone": "+1234567890"
    },
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
}
```

#### Update Student Profile

**PUT** `/api/profile/{profile_id}`

Updates a student profile with new analysis.

**Request Body:**
```json
{
  "skills": ["Python", "JavaScript", "Communication", "Leadership"],
  "interests": ["Technology", "Science", "Business"]
}
```

**Response:**
```json
{
  "success": true,
  "profile": {
    "id": 1,
    "name": "John Doe",
    "age": 20,
    "grade": "12th",
    "interests": ["Technology", "Science", "Business"],
    "skills": ["Python", "JavaScript", "Communication", "Leadership"],
    "learning_style": "Visual",
    "career_goals": ["Software Engineer"],
    "location": "New York",
    "contact_info": {
      "email": "john@example.com",
      "phone": "+1234567890"
    },
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  },
  "analysis": {
    "personality_analysis": {
      "traits": ["Analytical", "Creative", "Detail-oriented", "Leadership"],
      "strengths": ["Problem-solving", "Communication", "Technical skills", "Leadership"],
      "areas_for_improvement": ["Time management", "Strategic thinking"]
    },
    "career_analysis": {
      "suitable_careers": ["Software Engineer", "Data Scientist", "Product Manager", "Tech Lead"],
      "career_paths": ["Technical", "Management", "Entrepreneurship"],
      "recommendations": ["Focus on technical skills", "Develop leadership abilities", "Consider management roles"]
    }
  }
}
```

#### Get Profile Analysis

**GET** `/api/profile/{profile_id}/analysis`

Retrieves detailed analysis of a student profile.

**Response:**
```json
{
  "success": true,
  "profile_analysis": {
    "personality_analysis": {
      "traits": ["Analytical", "Creative", "Detail-oriented"],
      "strengths": ["Problem-solving", "Communication", "Technical skills"],
      "areas_for_improvement": ["Leadership", "Time management"]
    },
    "career_analysis": {
      "suitable_careers": ["Software Engineer", "Data Scientist", "Product Manager"],
      "career_paths": ["Technical", "Management", "Entrepreneurship"],
      "recommendations": ["Focus on technical skills", "Develop leadership abilities"]
    }
  }
}
```

### Assessment Management

#### Submit RIASEC Assessment

**POST** `/api/assessment/riasec`

Submits RIASEC assessment responses for analysis.

**Request Body:**
```json
{
  "responses": {
    "question_1": "A",
    "question_2": "B",
    "question_3": "C"
  },
  "assessment_type": "riasec"
}
```

**Response:**
```json
{
  "success": true,
  "riasec_scores": {
    "Realistic": 85,
    "Investigative": 90,
    "Artistic": 70,
    "Social": 60,
    "Enterprising": 75,
    "Conventional": 65
  },
  "personality_analysis": {
    "primary_type": "Investigative",
    "secondary_type": "Realistic",
    "personality_description": "Analytical and practical, enjoys problem-solving and technical challenges",
    "career_recommendations": ["Software Engineer", "Data Scientist", "Research Scientist"]
  }
}
```

#### Submit Skills Assessment

**POST** `/api/assessment/skills`

Submits skills assessment responses for analysis.

**Request Body:**
```json
{
  "responses": {
    "Python": {"level": "intermediate", "confidence": 80},
    "JavaScript": {"level": "beginner", "confidence": 60},
    "Communication": {"level": "advanced", "confidence": 90}
  },
  "assessment_type": "skills"
}
```

**Response:**
```json
{
  "success": true,
  "skills_scores": {
    "Python": {"level": "intermediate", "confidence": 80, "score": 80},
    "JavaScript": {"level": "beginner", "confidence": 60, "score": 60},
    "Communication": {"level": "advanced", "confidence": 90, "score": 90}
  },
  "overall_scores": {
    "technical_skills": 70,
    "soft_skills": 90,
    "overall_score": 80
  }
}
```

#### Get Assessment Results

**GET** `/api/assessment/results/{assessment_id}`

Retrieves assessment results by ID.

**Response:**
```json
{
  "success": true,
  "assessment_result": {
    "id": 1,
    "assessment_type": "riasec",
    "responses": {
      "question_1": "A",
      "question_2": "B",
      "question_3": "C"
    },
    "scores": {
      "Realistic": 85,
      "Investigative": 90,
      "Artistic": 70,
      "Social": 60,
      "Enterprising": 75,
      "Conventional": 65
    },
    "analysis": {
      "primary_type": "Investigative",
      "secondary_type": "Realistic",
      "personality_description": "Analytical and practical, enjoys problem-solving and technical challenges",
      "career_recommendations": ["Software Engineer", "Data Scientist", "Research Scientist"]
    },
    "created_at": "2024-01-01T00:00:00Z"
  }
}
```

#### Get Available Assessments

**GET** `/api/assessment/available`

Retrieves list of available assessments.

**Response:**
```json
{
  "success": true,
  "available_assessments": [
    {
      "id": 1,
      "name": "RIASEC Personality Assessment",
      "description": "Assesses personality traits and career preferences",
      "duration": "15 minutes",
      "questions_count": 60
    },
    {
      "id": 2,
      "name": "Skills Assessment",
      "description": "Evaluates technical and soft skills",
      "duration": "20 minutes",
      "questions_count": 50
    }
  ]
}
```

### Career Discovery

#### Get Career Recommendations

**GET** `/api/career/recommendations/{profile_id}`

Retrieves personalized career recommendations for a student.

**Response:**
```json
{
  "success": true,
  "career_recommendations": [
    {
      "id": 1,
      "title": "Software Engineer",
      "description": "Designs and develops software applications",
      "match_score": 95,
      "salary_range": "$70,000 - $120,000",
      "education_requirements": "Bachelor's in Computer Science",
      "skills_required": ["Programming", "Problem-solving", "Communication"],
      "growth_outlook": "High",
      "work_environment": "Office, Remote"
    }
  ]
}
```

#### Search Careers

**GET** `/api/career/search`

Searches for careers based on query parameters.

**Query Parameters:**
- `q`: Search query
- `industry`: Industry filter
- `salary_min`: Minimum salary
- `salary_max`: Maximum salary

**Response:**
```json
{
  "success": true,
  "search_results": [
    {
      "id": 1,
      "title": "Software Engineer",
      "description": "Designs and develops software applications",
      "industry": "Technology",
      "salary_range": "$70,000 - $120,000",
      "match_score": 95
    }
  ]
}
```

#### Get Career Details

**GET** `/api/career/{career_id}`

Retrieves detailed information about a specific career.

**Response:**
```json
{
  "success": true,
  "career_details": {
    "id": 1,
    "title": "Software Engineer",
    "description": "Designs and develops software applications",
    "industry": "Technology",
    "salary_range": "$70,000 - $120,000",
    "education_requirements": "Bachelor's in Computer Science",
    "skills_required": ["Programming", "Problem-solving", "Communication"],
    "growth_outlook": "High",
    "work_environment": "Office, Remote",
    "job_responsibilities": ["Design software", "Write code", "Test applications"],
    "career_paths": ["Senior Developer", "Tech Lead", "Architect"]
  }
}
```

#### Get Career Trends

**GET** `/api/career/trends`

Retrieves current career trends and market insights.

**Response:**
```json
{
  "success": true,
  "career_trends": [
    {
      "career": "Software Engineer",
      "trend": "Growing",
      "growth_rate": "15%",
      "market_demand": "High",
      "emerging_skills": ["AI/ML", "Cloud Computing", "Cybersecurity"]
    }
  ]
}
```

#### Compare Careers

**POST** `/api/career/compare`

Compares multiple careers side by side.

**Request Body:**
```json
{
  "career_ids": [1, 2]
}
```

**Response:**
```json
{
  "success": true,
  "career_comparison": [
    {
      "id": 1,
      "title": "Software Engineer",
      "salary_range": "$70,000 - $120,000",
      "growth_outlook": "High",
      "skills_required": ["Programming", "Problem-solving"],
      "education_requirements": "Bachelor's in Computer Science"
    },
    {
      "id": 2,
      "title": "Data Scientist",
      "salary_range": "$80,000 - $130,000",
      "growth_outlook": "Very High",
      "skills_required": ["Statistics", "Machine Learning", "Programming"],
      "education_requirements": "Master's in Data Science"
    }
  ]
}
```

### Chat Interface

#### Create Chat Session

**POST** `/api/chat/session`

Creates a new chat session for career guidance.

**Request Body:**
```json
{
  "initial_context": {"topic": "career_guidance"}
}
```

**Response:**
```json
{
  "success": true,
  "session_id": "session-123",
  "student_profile": {
    "id": 1,
    "name": "John Doe",
    "interests": ["Technology", "Science"],
    "skills": ["Python", "Communication"]
  }
}
```

#### Send Chat Message

**POST** `/api/chat/message`

Sends a message in a chat session.

**Request Body:**
```json
{
  "message": "What careers match my personality?",
  "session_id": "session-123"
}
```

**Response:**
```json
{
  "success": true,
  "response_data": {
    "message": "Based on your personality and interests, I recommend exploring careers in technology and science. Here are some options that might interest you...",
    "suggestions": [
      "Tell me more about software engineering",
      "What skills do I need for data science?",
      "How can I improve my technical skills?"
    ]
  }
}
```

#### Get Chat History

**GET** `/api/chat/history/{session_id}`

Retrieves chat history for a session.

**Response:**
```json
{
  "success": true,
  "chat_history": [
    {
      "id": 1,
      "message": "What careers match my personality?",
      "response": "Based on your personality and interests, I recommend exploring careers in technology and science...",
      "timestamp": "2024-01-01T00:00:00Z"
    }
  ]
}
```

#### Get Chat Suggestions

**GET** `/api/chat/suggestions`

Retrieves suggested conversation topics.

**Response:**
```json
{
  "success": true,
  "chat_suggestions": [
    "What careers match my personality?",
    "How can I improve my skills?",
    "What education do I need for my dream career?",
    "Tell me about career trends in technology"
  ]
}
```

### Learning Paths

#### Get Learning Path

**GET** `/api/learning/path/{profile_id}`

Retrieves personalized learning path for a student.

**Response:**
```json
{
  "success": true,
  "learning_path": {
    "id": 1,
    "title": "Software Engineering Path",
    "description": "Comprehensive path to become a software engineer",
    "duration": "12 months",
    "difficulty": "Intermediate",
    "modules": [
      {
        "id": 1,
        "title": "Programming Fundamentals",
        "description": "Learn basic programming concepts",
        "duration": "2 months",
        "resources": ["Online courses", "Books", "Practice projects"]
      }
    ]
  }
}
```

#### Get Learning Resources

**GET** `/api/learning/resources/{profile_id}`

Retrieves learning resources for a student.

**Response:**
```json
{
  "success": true,
  "learning_resources": [
    {
      "id": 1,
      "title": "Python Programming Course",
      "type": "Online Course",
      "provider": "Coursera",
      "duration": "4 weeks",
      "difficulty": "Beginner",
      "cost": "Free",
      "rating": 4.5
    }
  ]
}
```

#### Create Skill Development Path

**POST** `/api/learning/skill-development`

Creates a personalized skill development path.

**Request Body:**
```json
{
  "skill": "Python",
  "current_level": "beginner",
  "target_level": "intermediate",
  "learning_style": "visual"
}
```

**Response:**
```json
{
  "success": true,
  "skill_development_path": {
    "skill": "Python",
    "current_level": "beginner",
    "target_level": "intermediate",
    "learning_style": "visual",
    "path": [
      {
        "step": 1,
        "title": "Learn Python Basics",
        "description": "Master fundamental Python concepts",
        "duration": "2 weeks",
        "resources": ["Python tutorial", "Practice exercises"]
      }
    ]
  }
}
```

#### Get Learning Recommendations

**GET** `/api/learning/recommendations`

Retrieves learning recommendations based on profile.

**Response:**
```json
{
  "success": true,
  "learning_recommendations": [
    {
      "id": 1,
      "title": "Advanced Python Programming",
      "description": "Take your Python skills to the next level",
      "match_score": 95,
      "estimated_time": "6 weeks",
      "difficulty": "Intermediate"
    }
  ]
}
```

### Mentor Matching

#### Get Mentor Recommendations

**GET** `/api/mentor/recommendations/{profile_id}`

Retrieves personalized mentor recommendations.

**Response:**
```json
{
  "success": true,
  "mentor_recommendations": [
    {
      "id": 1,
      "name": "Jane Smith",
      "title": "Senior Software Engineer",
      "company": "Tech Corp",
      "experience": "10 years",
      "match_score": 95,
      "specialties": ["Python", "Web Development", "Career Guidance"],
      "availability": "Weekdays 6-8 PM"
    }
  ]
}
```

#### Get Mentor Profile

**GET** `/api/mentor/{mentor_id}`

Retrieves detailed mentor profile.

**Response:**
```json
{
  "success": true,
  "mentor_profile": {
    "id": 1,
    "name": "Jane Smith",
    "title": "Senior Software Engineer",
    "company": "Tech Corp",
    "experience": "10 years",
    "specialties": ["Python", "Web Development", "Career Guidance"],
    "availability": "Weekdays 6-8 PM",
    "bio": "Passionate about helping students succeed in tech careers",
    "education": "MS Computer Science",
    "achievements": ["Published author", "Conference speaker"]
  },
  "profile_analysis": {
    "mentoring_style": "Supportive and encouraging",
    "communication_style": "Clear and direct",
    "expertise_areas": ["Technical skills", "Career development", "Industry insights"]
  }
}
```

#### Search Mentors

**GET** `/api/mentor/search`

Searches for mentors based on criteria.

**Query Parameters:**
- `q`: Search query
- `specialty`: Specialty filter
- `experience_min`: Minimum experience
- `availability`: Availability filter

**Response:**
```json
{
  "success": true,
  "search_results": [
    {
      "id": 1,
      "name": "Jane Smith",
      "title": "Senior Software Engineer",
      "company": "Tech Corp",
      "experience": "10 years",
      "specialties": ["Python", "Web Development"],
      "match_score": 95
    }
  ]
}
```

#### Check Mentor Availability

**GET** `/api/mentor/availability/{mentor_id}`

Checks mentor availability for booking.

**Response:**
```json
{
  "success": true,
  "mentor_availability": {
    "mentor_id": 1,
    "available_slots": [
      {
        "date": "2024-01-15",
        "time": "18:00",
        "duration": "60 minutes",
        "type": "Video Call"
      }
    ],
    "booking_policy": "24-hour advance notice required"
  }
}
```

## Error Responses

All endpoints may return error responses in the following format:

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "field": "email",
      "issue": "Invalid email format"
    }
  }
}
```

### Common Error Codes

- `VALIDATION_ERROR`: Input validation failed
- `AUTHENTICATION_ERROR`: Authentication failed
- `AUTHORIZATION_ERROR`: Insufficient permissions
- `NOT_FOUND`: Resource not found
- `RATE_LIMIT_EXCEEDED`: Rate limit exceeded
- `INTERNAL_ERROR`: Internal server error

## Rate Limiting

API requests are rate limited to prevent abuse:

- **Free Tier**: 100 requests per hour
- **Premium Tier**: 1000 requests per hour
- **Enterprise Tier**: 10000 requests per hour

Rate limit headers are included in responses:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995200
```

## Pagination

List endpoints support pagination using query parameters:

- `page`: Page number (default: 1)
- `limit`: Items per page (default: 20, max: 100)

Response includes pagination metadata:

```json
{
  "success": true,
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "pages": 5
  }
}
```

## SDKs and Libraries

Official SDKs are available for:

- **Python**: `pip install career-connect-ai`
- **JavaScript**: `npm install career-connect-ai`
- **Java**: Available in Maven Central
- **C#**: Available in NuGet

## Support

For API support and questions:

- **Email**: api-support@careerconnectai.com
- **Documentation**: https://docs.careerconnectai.com
- **Status Page**: https://status.careerconnectai.com
