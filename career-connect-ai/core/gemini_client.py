"""
Google Gemini 2.0 Flash API Client for CareerConnect AI
Production-ready client with comprehensive error handling, caching, and async support.
"""

import asyncio
import json
import logging
import time
import uuid
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from datetime import datetime, timedelta
import aiohttp
import redis
from config import get_config

# Configure logging
logger = logging.getLogger(__name__)

@dataclass
class GeminiResponse:
    """Structured response from Gemini API."""
    content: str
    usage: Dict[str, int]
    model: str
    correlation_id: str
    timestamp: datetime
    cached: bool = False

@dataclass
class GeminiRequest:
    """Structured request to Gemini API."""
    prompt: str
    context: Optional[Dict[str, Any]] = None
    temperature: float = 0.7
    max_tokens: int = 1500
    correlation_id: Optional[str] = None

class GeminiClient:
    """
    Production-ready Google Gemini 2.0 Flash API client for CareerConnect AI.
    
    Features:
    - Async/await support for better performance
    - Comprehensive error handling with exponential backoff
    - Redis caching for repeated queries
    - Request/response logging with correlation IDs
    - Specialized prompt templates for career counseling
    - Input sanitization and output validation
    """
    
    def __init__(self, api_key: Optional[str] = None, redis_client: Optional[redis.Redis] = None):
        """
        Initialize Gemini client.
        
        Args:
            api_key: Google Gemini API key
            redis_client: Redis client for caching
        """
        self.config = get_config()
        self.api_key = api_key or self.config.GEMINI_API_KEY
        self.redis_client = redis_client
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        self.headers = {
            'Content-Type': 'application/json',
            'X-goog-api-key': self.api_key
        }
        
        # Rate limiting and retry configuration
        self.max_retries = 3
        self.base_delay = 1.0
        self.max_delay = 60.0
        self.timeout = 30.0
        
        # Cache configuration
        self.cache_ttl = self.config.CACHE_TTL
        self.cache_prefix = "gemini:"
        
        # Prompt templates
        self.prompt_templates = self._initialize_prompt_templates()
        
        # Validate API key
        if not self.api_key:
            raise ValueError("Gemini API key is required")
        
        logger.info("GeminiClient initialized successfully")
    
    def _initialize_prompt_templates(self) -> Dict[str, str]:
        """Initialize specialized prompt templates for career counseling."""
        return {
            'career_counseling': """
You are an expert career counselor specializing in Indian education and career paths. 
Provide personalized, culturally relevant career guidance for Indian students.

Student Context: {context}
Question: {question}

Guidelines:
- Consider Indian education system (10th, 12th, graduation, post-graduation)
- Factor in Indian job market trends and opportunities
- Suggest careers aligned with Indian economic growth sectors
- Include information about entrance exams (JEE, NEET, CAT, etc.)
- Mention top Indian universities and colleges
- Consider regional preferences and family expectations
- Provide practical, actionable advice

Response should be encouraging, detailed, and culturally sensitive.
""",
            
            'riasec_analysis': """
Analyze the following RIASEC personality assessment results for an Indian student:

RIASEC Scores: {riasec_scores}
Interests: {interests}
Background: {background}

Provide:
1. Personality type interpretation (primary and secondary)
2. Suitable career categories for Indian market
3. Specific career recommendations with Indian context
4. Required education paths (Indian system)
5. Top colleges/universities in India
6. Entrance exam requirements
7. Career growth prospects in India

Format as structured JSON with detailed explanations.
""",
            
            'skill_gap_assessment': """
Analyze skill gaps for an Indian student pursuing this career path:

Current Skills: {current_skills}
Target Career: {target_career}
Current Education Level: {education_level}
Location: {location}

Provide:
1. Critical skill gaps identified
2. Priority order for skill development
3. Learning resources available in India
4. Online courses and certifications
5. Practical projects and internships
6. Timeline for skill development
7. Cost-effective learning options

Consider Indian education system and local opportunities.
""",
            
            'learning_path_generation': """
Create a comprehensive learning path for an Indian student:

Career Choice: {career_choice}
Current Skills: {current_skills}
Education Level: {education_level}
Learning Style: {learning_style}
Time Available: {time_available}
Budget: {budget}

Generate:
1. Step-by-step learning roadmap
2. Required courses and certifications
3. Indian educational institutions
4. Online learning platforms
5. Practical projects and portfolios
6. Internship opportunities
7. Networking and mentorship
8. Timeline and milestones
9. Cost breakdown
10. Success metrics

Format as structured learning path with actionable steps.
""",
            
            'mentor_matching': """
Match this Indian student with suitable mentors:

Student Profile: {student_profile}
Career Interests: {career_interests}
Location: {location}
Communication Preferences: {communication_preferences}

Find mentors who:
1. Work in relevant Indian industries
2. Have experience with Indian education system
3. Can provide culturally relevant guidance
4. Are available for regular mentoring
5. Have track record of student success

Provide mentor profiles with:
- Professional background
- Mentoring experience
- Availability and communication style
- Success stories with Indian students
- Specific areas of expertise
"""
        }
    
    async def initialize_client(self, api_key: str) -> bool:
        """
        Initialize client with new API key.
        
        Args:
            api_key: Google Gemini API key
            
        Returns:
            bool: True if initialization successful
        """
        try:
            self.api_key = api_key
            self.headers['X-goog-api-key'] = api_key
            
            # Test API key with a simple request
            test_response = await self._make_request(
                GeminiRequest(prompt="Test connection", max_tokens=10)
            )
            
            logger.info("Gemini client initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {e}")
            return False
    
    async def generate_response(
        self, 
        prompt: str, 
        context: Optional[Dict[str, Any]] = None,
        temperature: float = 0.7,
        max_tokens: int = 1500
    ) -> GeminiResponse:
        """
        Generate response from Gemini API.
        
        Args:
            prompt: Input prompt
            context: Additional context
            temperature: Response creativity (0.0-1.0)
            max_tokens: Maximum response length
            
        Returns:
            GeminiResponse: Structured response
        """
        correlation_id = str(uuid.uuid4())
        
        # Create request object
        request = GeminiRequest(
            prompt=prompt,
            context=context,
            temperature=temperature,
            max_tokens=max_tokens,
            correlation_id=correlation_id
        )
        
        # Check cache first
        cached_response = await self._get_cached_response(request)
        if cached_response:
            logger.info(f"Returning cached response for correlation_id: {correlation_id}")
            return cached_response
        
        # Make API request
        response = await self._make_request(request)
        
        # Cache the response
        await self._cache_response(request, response)
        
        return response
    
    async def analyze_student_profile(self, profile_data: Dict[str, Any]) -> GeminiResponse:
        """
        Analyze student profile for career guidance.
        
        Args:
            profile_data: Student profile information
            
        Returns:
            GeminiResponse: Analysis results
        """
        # Sanitize input
        sanitized_profile = self._sanitize_profile_data(profile_data)
        
        # Create context
        context = {
            'profile': sanitized_profile,
            'analysis_type': 'student_profile',
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # Generate prompt
        prompt = f"""
Analyze this Indian student's profile and provide comprehensive career guidance:

Profile Data: {json.dumps(sanitized_profile, indent=2)}

Provide detailed analysis including:
1. Personality assessment
2. Strengths and areas for improvement
3. Suitable career paths for Indian market
4. Educational recommendations
5. Skill development suggestions
6. Cultural and family considerations
7. Regional opportunities
8. Actionable next steps

Format response as structured analysis with clear sections.
"""
        
        return await self.generate_response(prompt, context, temperature=0.6)
    
    async def generate_career_recommendations(
        self, 
        riasec_scores: Dict[str, float], 
        interests: List[str]
    ) -> GeminiResponse:
        """
        Generate career recommendations based on RIASEC scores and interests.
        
        Args:
            riasec_scores: RIASEC personality scores
            interests: Student interests
            
        Returns:
            GeminiResponse: Career recommendations
        """
        # Validate RIASEC scores
        valid_types = ['Realistic', 'Investigative', 'Artistic', 'Social', 'Enterprising', 'Conventional']
        if not all(key in valid_types for key in riasec_scores.keys()):
            raise ValueError("Invalid RIASEC score keys")
        
        # Create context
        context = {
            'riasec_scores': riasec_scores,
            'interests': interests,
            'analysis_type': 'career_recommendations',
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # Use template
        prompt = self.prompt_templates['riasec_analysis'].format(
            riasec_scores=json.dumps(riasec_scores, indent=2),
            interests=', '.join(interests),
            background="Indian student seeking career guidance"
        )
        
        return await self.generate_response(prompt, context, temperature=0.5)
    
    async def create_learning_path(
        self, 
        career_choice: str, 
        current_skills: List[str],
        education_level: str = "12th",
        learning_style: str = "mixed",
        time_available: str = "6 months",
        budget: str = "moderate"
    ) -> GeminiResponse:
        """
        Create personalized learning path.
        
        Args:
            career_choice: Target career
            current_skills: Current skill set
            education_level: Current education level
            learning_style: Preferred learning style
            time_available: Available time for learning
            budget: Budget constraints
            
        Returns:
            GeminiResponse: Learning path
        """
        # Create context
        context = {
            'career_choice': career_choice,
            'current_skills': current_skills,
            'education_level': education_level,
            'learning_style': learning_style,
            'time_available': time_available,
            'budget': budget,
            'analysis_type': 'learning_path',
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # Use template
        prompt = self.prompt_templates['learning_path_generation'].format(
            career_choice=career_choice,
            current_skills=', '.join(current_skills),
            education_level=education_level,
            learning_style=learning_style,
            time_available=time_available,
            budget=budget
        )
        
        return await self.generate_response(prompt, context, temperature=0.6)
    
    async def chat_response(
        self, 
        message: str, 
        conversation_history: List[Dict[str, str]],
        student_context: Dict[str, Any]
    ) -> GeminiResponse:
        """
        Generate chat response for career counseling conversation.
        
        Args:
            message: User message
            conversation_history: Previous conversation
            student_context: Student context
            
        Returns:
            GeminiResponse: Chat response
        """
        # Sanitize inputs
        sanitized_message = self._sanitize_text(message)
        sanitized_context = self._sanitize_profile_data(student_context)
        
        # Create context
        context = {
            'message': sanitized_message,
            'conversation_history': conversation_history,
            'student_context': sanitized_context,
            'analysis_type': 'chat_response',
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # Build conversation context
        conversation_context = ""
        if conversation_history:
            conversation_context = "\n".join([
                f"{msg.get('role', 'user')}: {msg.get('content', '')}" 
                for msg in conversation_history[-5:]  # Last 5 messages
            ])
        
        # Use template
        prompt = self.prompt_templates['career_counseling'].format(
            context=f"Student Context: {json.dumps(sanitized_context, indent=2)}\n\nConversation History:\n{conversation_context}",
            question=sanitized_message
        )
        
        return await self.generate_response(prompt, context, temperature=0.7)
    
    async def _make_request(self, request: GeminiRequest) -> GeminiResponse:
        """
        Make request to Gemini API with retry logic.
        
        Args:
            request: Gemini request object
            
        Returns:
            GeminiResponse: API response
            
        Raises:
            Exception: If all retries fail
        """
        correlation_id = request.correlation_id or str(uuid.uuid4())
        
        # Log request
        logger.info(f"Making Gemini API request - correlation_id: {correlation_id}")
        
        # Prepare request data
        request_data = {
            "contents": [{
                "parts": [{"text": request.prompt}]
            }],
            "generationConfig": {
                "temperature": request.temperature,
                "maxOutputTokens": request.max_tokens,
                "topP": 0.8,
                "topK": 10
            }
        }
        
        # Add context if provided
        if request.context:
            request_data["systemInstruction"] = {
                "parts": [{"text": f"Context: {json.dumps(request.context)}"}]
            }
        
        # Retry logic with exponential backoff
        for attempt in range(self.max_retries):
            try:
                async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                    async with session.post(
                        self.base_url,
                        headers=self.headers,
                        json=request_data
                    ) as response:
                        
                        # Handle different response codes
                        if response.status == 200:
                            response_data = await response.json()
                            return self._parse_response(response_data, correlation_id)
                        
                        elif response.status == 401:
                            logger.error(f"Authentication failed - correlation_id: {correlation_id}")
                            raise Exception("Invalid API key")
                        
                        elif response.status == 429:
                            # Rate limit exceeded
                            retry_after = int(response.headers.get('Retry-After', 60))
                            logger.warning(f"Rate limit exceeded, retrying after {retry_after}s - correlation_id: {correlation_id}")
                            
                            if attempt < self.max_retries - 1:
                                await asyncio.sleep(retry_after)
                                continue
                            else:
                                raise Exception("Rate limit exceeded")
                        
                        elif response.status >= 500:
                            # Server error
                            logger.warning(f"Server error {response.status}, attempt {attempt + 1} - correlation_id: {correlation_id}")
                            
                            if attempt < self.max_retries - 1:
                                delay = min(self.base_delay * (2 ** attempt), self.max_delay)
                                await asyncio.sleep(delay)
                                continue
                            else:
                                raise Exception(f"Server error: {response.status}")
                        
                        else:
                            error_text = await response.text()
                            logger.error(f"API error {response.status}: {error_text} - correlation_id: {correlation_id}")
                            raise Exception(f"API error: {response.status}")
            
            except asyncio.TimeoutError:
                logger.warning(f"Request timeout, attempt {attempt + 1} - correlation_id: {correlation_id}")
                if attempt < self.max_retries - 1:
                    delay = min(self.base_delay * (2 ** attempt), self.max_delay)
                    await asyncio.sleep(delay)
                    continue
                else:
                    raise Exception("Request timeout")
            
            except aiohttp.ClientError as e:
                logger.warning(f"Client error: {e}, attempt {attempt + 1} - correlation_id: {correlation_id}")
                if attempt < self.max_retries - 1:
                    delay = min(self.base_delay * (2 ** attempt), self.max_delay)
                    await asyncio.sleep(delay)
                    continue
                else:
                    raise Exception(f"Client error: {e}")
        
        raise Exception("All retry attempts failed")
    
    def _parse_response(self, response_data: Dict[str, Any], correlation_id: str) -> GeminiResponse:
        """
        Parse Gemini API response.
        
        Args:
            response_data: Raw API response
            correlation_id: Request correlation ID
            
        Returns:
            GeminiResponse: Parsed response
        """
        try:
            # Extract content
            if 'candidates' in response_data and len(response_data['candidates']) > 0:
                candidate = response_data['candidates'][0]
                if 'content' in candidate and 'parts' in candidate['content']:
                    content = candidate['content']['parts'][0].get('text', '')
                else:
                    content = "No content generated"
            else:
                content = "No candidates in response"
            
            # Extract usage information
            usage = response_data.get('usageMetadata', {})
            
            # Create response object
            response = GeminiResponse(
                content=content,
                usage=usage,
                model="gemini-2.0-flash",
                correlation_id=correlation_id,
                timestamp=datetime.utcnow()
            )
            
            # Log response
            logger.info(f"Gemini API response received - correlation_id: {correlation_id}, tokens: {usage.get('totalTokenCount', 0)}")
            
            return response
            
        except Exception as e:
            logger.error(f"Failed to parse Gemini response: {e} - correlation_id: {correlation_id}")
            raise Exception(f"Failed to parse response: {e}")
    
    async def _get_cached_response(self, request: GeminiRequest) -> Optional[GeminiResponse]:
        """Get cached response if available."""
        if not self.redis_client:
            return None
        
        try:
            cache_key = self._generate_cache_key(request)
            cached_data = self.redis_client.get(cache_key)
            
            if cached_data:
                response_data = json.loads(cached_data)
                response_data['cached'] = True
                return GeminiResponse(**response_data)
            
        except Exception as e:
            logger.warning(f"Cache retrieval failed: {e}")
        
        return None
    
    async def _cache_response(self, request: GeminiRequest, response: GeminiResponse):
        """Cache response for future use."""
        if not self.redis_client:
            return
        
        try:
            cache_key = self._generate_cache_key(request)
            response_data = {
                'content': response.content,
                'usage': response.usage,
                'model': response.model,
                'correlation_id': response.correlation_id,
                'timestamp': response.timestamp.isoformat(),
                'cached': False
            }
            
            self.redis_client.setex(
                cache_key,
                self.cache_ttl,
                json.dumps(response_data)
            )
            
            logger.debug(f"Response cached with key: {cache_key}")
            
        except Exception as e:
            logger.warning(f"Cache storage failed: {e}")
    
    def _generate_cache_key(self, request: GeminiRequest) -> str:
        """Generate cache key for request."""
        # Create hash of request parameters
        request_hash = hash(json.dumps({
            'prompt': request.prompt,
            'context': request.context,
            'temperature': request.temperature,
            'max_tokens': request.max_tokens
        }, sort_keys=True))
        
        return f"{self.cache_prefix}{request_hash}"
    
    def _sanitize_text(self, text: str) -> str:
        """Sanitize input text."""
        if not isinstance(text, str):
            return str(text)
        
        # Remove potentially harmful content
        text = text.strip()
        text = text[:10000]  # Limit length
        
        return text
    
    def _sanitize_profile_data(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize profile data."""
        if not isinstance(profile_data, dict):
            return {}
        
        sanitized = {}
        for key, value in profile_data.items():
            if isinstance(value, str):
                sanitized[key] = self._sanitize_text(value)
            elif isinstance(value, (list, dict)):
                sanitized[key] = value
            else:
                sanitized[key] = str(value)
        
        return sanitized

# Convenience functions for synchronous usage
def create_gemini_client(api_key: Optional[str] = None, redis_client: Optional[redis.Redis] = None) -> GeminiClient:
    """Create Gemini client instance."""
    return GeminiClient(api_key, redis_client)

async def analyze_student_profile_async(profile_data: Dict[str, Any], api_key: Optional[str] = None) -> GeminiResponse:
    """Convenience function for profile analysis."""
    client = GeminiClient(api_key)
    return await client.analyze_student_profile(profile_data)

async def generate_career_recommendations_async(
    riasec_scores: Dict[str, float], 
    interests: List[str], 
    api_key: Optional[str] = None
) -> GeminiResponse:
    """Convenience function for career recommendations."""
    client = GeminiClient(api_key)
    return await client.generate_career_recommendations(riasec_scores, interests)

# Example usage
if __name__ == "__main__":
    async def main():
        # Initialize client
        client = GeminiClient()
        
        # Test basic functionality
        response = await client.generate_response("Hello, how are you?")
        print(f"Response: {response.content}")
        
        # Test profile analysis
        profile = {
            "name": "Rajesh Kumar",
            "age": 17,
            "grade": "12th",
            "interests": ["Technology", "Mathematics"],
            "skills": ["Python", "Problem Solving"],
            "location": "Mumbai"
        }
        
        analysis = await client.analyze_student_profile(profile)
        print(f"Analysis: {analysis.content}")
    
    # Run example
    asyncio.run(main())