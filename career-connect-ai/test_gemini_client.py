"""
Test suite for Gemini Client
"""

import pytest
import asyncio
import json
from unittest.mock import Mock, patch, AsyncMock
from core.gemini_client import GeminiClient, GeminiResponse, GeminiRequest

class TestGeminiClient:
    """Test cases for GeminiClient class."""
    
    @pytest.fixture
    def mock_redis_client(self):
        """Mock Redis client."""
        mock_redis = Mock()
        mock_redis.get.return_value = None
        mock_redis.setex.return_value = True
        return mock_redis
    
    @pytest.fixture
    def gemini_client(self, mock_redis_client):
        """Create Gemini client instance for testing."""
        with patch('core.gemini_client.get_config') as mock_config:
            mock_config.return_value.GEMINI_API_KEY = "test-api-key"
            mock_config.return_value.CACHE_TTL = 3600
            return GeminiClient(api_key="test-api-key", redis_client=mock_redis_client)
    
    def test_client_initialization(self, gemini_client):
        """Test client initialization."""
        assert gemini_client.api_key == "test-api-key"
        assert gemini_client.base_url == "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        assert gemini_client.headers['X-goog-api-key'] == "test-api-key"
        assert gemini_client.max_retries == 3
        assert gemini_client.timeout == 30.0
    
    def test_prompt_templates_initialization(self, gemini_client):
        """Test prompt templates are properly initialized."""
        templates = gemini_client.prompt_templates
        assert 'career_counseling' in templates
        assert 'riasec_analysis' in templates
        assert 'skill_gap_assessment' in templates
        assert 'learning_path_generation' in templates
        assert 'mentor_matching' in templates
        
        # Check that templates contain expected placeholders
        assert '{context}' in templates['career_counseling']
        assert '{question}' in templates['career_counseling']
        assert '{riasec_scores}' in templates['riasec_analysis']
        assert '{interests}' in templates['riasec_analysis']
    
    def test_sanitize_text(self, gemini_client):
        """Test text sanitization."""
        # Test normal text
        assert gemini_client._sanitize_text("Hello World") == "Hello World"
        
        # Test text with whitespace
        assert gemini_client._sanitize_text("  Hello World  ") == "Hello World"
        
        # Test long text (should be truncated)
        long_text = "A" * 15000
        sanitized = gemini_client._sanitize_text(long_text)
        assert len(sanitized) == 10000
        
        # Test non-string input
        assert gemini_client._sanitize_text(123) == "123"
        assert gemini_client._sanitize_text(None) == "None"
    
    def test_sanitize_profile_data(self, gemini_client):
        """Test profile data sanitization."""
        profile_data = {
            "name": "  John Doe  ",
            "age": 20,
            "interests": ["Technology", "Science"],
            "skills": {"programming": "Python", "level": "intermediate"},
            "description": "A" * 15000  # Long text
        }
        
        sanitized = gemini_client._sanitize_profile_data(profile_data)
        
        assert sanitized["name"] == "John Doe"  # Whitespace removed
        assert sanitized["age"] == "20"  # Converted to string
        assert sanitized["interests"] == ["Technology", "Science"]  # List preserved
        assert sanitized["skills"] == {"programming": "Python", "level": "intermediate"}  # Dict preserved
        assert len(sanitized["description"]) == 10000  # Truncated
    
    def test_generate_cache_key(self, gemini_client):
        """Test cache key generation."""
        request1 = GeminiRequest(
            prompt="Hello",
            context={"user": "test"},
            temperature=0.7,
            max_tokens=100
        )
        
        request2 = GeminiRequest(
            prompt="Hello",
            context={"user": "test"},
            temperature=0.7,
            max_tokens=100
        )
        
        # Same request should generate same key
        key1 = gemini_client._generate_cache_key(request1)
        key2 = gemini_client._generate_cache_key(request2)
        assert key1 == key2
        
        # Different request should generate different key
        request3 = GeminiRequest(
            prompt="Hello",
            context={"user": "test"},
            temperature=0.8,  # Different temperature
            max_tokens=100
        )
        key3 = gemini_client._generate_cache_key(request3)
        assert key1 != key3
    
    @pytest.mark.asyncio
    async def test_initialize_client_success(self, gemini_client):
        """Test successful client initialization."""
        with patch.object(gemini_client, '_make_request') as mock_request:
            mock_response = GeminiResponse(
                content="Test response",
                usage={"totalTokenCount": 10},
                model="gemini-2.0-flash",
                correlation_id="test-id",
                timestamp=gemini_client.config.LOG_LEVEL  # This will be fixed
            )
            mock_request.return_value = mock_response
            
            result = await gemini_client.initialize_client("new-api-key")
            
            assert result is True
            assert gemini_client.api_key == "new-api-key"
            assert gemini_client.headers['X-goog-api-key'] == "new-api-key"
    
    @pytest.mark.asyncio
    async def test_initialize_client_failure(self, gemini_client):
        """Test failed client initialization."""
        with patch.object(gemini_client, '_make_request') as mock_request:
            mock_request.side_effect = Exception("API Error")
            
            result = await gemini_client.initialize_client("invalid-key")
            
            assert result is False
    
    @pytest.mark.asyncio
    async def test_generate_response_with_cache(self, gemini_client):
        """Test response generation with cache hit."""
        # Mock cached response
        cached_response = GeminiResponse(
            content="Cached response",
            usage={"totalTokenCount": 5},
            model="gemini-2.0-flash",
            correlation_id="cache-id",
            timestamp=gemini_client.config.LOG_LEVEL,  # This will be fixed
            cached=True
        )
        
        with patch.object(gemini_client, '_get_cached_response', return_value=cached_response):
            response = await gemini_client.generate_response("Test prompt")
            
            assert response.content == "Cached response"
            assert response.cached is True
    
    @pytest.mark.asyncio
    async def test_generate_response_without_cache(self, gemini_client):
        """Test response generation without cache."""
        # Mock API response
        api_response = GeminiResponse(
            content="API response",
            usage={"totalTokenCount": 10},
            model="gemini-2.0-flash",
            correlation_id="api-id",
            timestamp=gemini_client.config.LOG_LEVEL,  # This will be fixed
            cached=False
        )
        
        with patch.object(gemini_client, '_get_cached_response', return_value=None), \
             patch.object(gemini_client, '_make_request', return_value=api_response), \
             patch.object(gemini_client, '_cache_response'):
            
            response = await gemini_client.generate_response("Test prompt")
            
            assert response.content == "API response"
            assert response.cached is False
    
    @pytest.mark.asyncio
    async def test_analyze_student_profile(self, gemini_client):
        """Test student profile analysis."""
        profile_data = {
            "name": "Rajesh Kumar",
            "age": 17,
            "grade": "12th",
            "interests": ["Technology", "Mathematics"],
            "skills": ["Python", "Problem Solving"],
            "location": "Mumbai"
        }
        
        mock_response = GeminiResponse(
            content="Profile analysis result",
            usage={"totalTokenCount": 50},
            model="gemini-2.0-flash",
            correlation_id="profile-id",
            timestamp=gemini_client.config.LOG_LEVEL,  # This will be fixed
            cached=False
        )
        
        with patch.object(gemini_client, 'generate_response', return_value=mock_response):
            response = await gemini_client.analyze_student_profile(profile_data)
            
            assert response.content == "Profile analysis result"
    
    @pytest.mark.asyncio
    async def test_generate_career_recommendations(self, gemini_client):
        """Test career recommendations generation."""
        riasec_scores = {
            "Realistic": 85,
            "Investigative": 90,
            "Artistic": 70,
            "Social": 60,
            "Enterprising": 75,
            "Conventional": 65
        }
        interests = ["Technology", "Science"]
        
        mock_response = GeminiResponse(
            content="Career recommendations result",
            usage={"totalTokenCount": 40},
            model="gemini-2.0-flash",
            correlation_id="career-id",
            timestamp=gemini_client.config.LOG_LEVEL,  # This will be fixed
            cached=False
        )
        
        with patch.object(gemini_client, 'generate_response', return_value=mock_response):
            response = await gemini_client.generate_career_recommendations(riasec_scores, interests)
            
            assert response.content == "Career recommendations result"
    
    def test_generate_career_recommendations_invalid_riasec(self, gemini_client):
        """Test career recommendations with invalid RIASEC scores."""
        invalid_riasec_scores = {
            "Invalid": 85,
            "Investigative": 90
        }
        interests = ["Technology"]
        
        with pytest.raises(ValueError, match="Invalid RIASEC score keys"):
            asyncio.run(gemini_client.generate_career_recommendations(invalid_riasec_scores, interests))
    
    @pytest.mark.asyncio
    async def test_create_learning_path(self, gemini_client):
        """Test learning path creation."""
        career_choice = "Software Engineer"
        current_skills = ["Python", "Basic Programming"]
        
        mock_response = GeminiResponse(
            content="Learning path result",
            usage={"totalTokenCount": 60},
            model="gemini-2.0-flash",
            correlation_id="learning-id",
            timestamp=gemini_client.config.LOG_LEVEL,  # This will be fixed
            cached=False
        )
        
        with patch.object(gemini_client, 'generate_response', return_value=mock_response):
            response = await gemini_client.create_learning_path(career_choice, current_skills)
            
            assert response.content == "Learning path result"
    
    @pytest.mark.asyncio
    async def test_chat_response(self, gemini_client):
        """Test chat response generation."""
        message = "What careers match my personality?"
        conversation_history = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi! How can I help you?"}
        ]
        student_context = {
            "name": "Priya",
            "interests": ["Art", "Design"]
        }
        
        mock_response = GeminiResponse(
            content="Chat response result",
            usage={"totalTokenCount": 30},
            model="gemini-2.0-flash",
            correlation_id="chat-id",
            timestamp=gemini_client.config.LOG_LEVEL,  # This will be fixed
            cached=False
        )
        
        with patch.object(gemini_client, 'generate_response', return_value=mock_response):
            response = await gemini_client.chat_response(message, conversation_history, student_context)
            
            assert response.content == "Chat response result"

class TestGeminiRequest:
    """Test cases for GeminiRequest dataclass."""
    
    def test_gemini_request_creation(self):
        """Test GeminiRequest creation."""
        request = GeminiRequest(
            prompt="Test prompt",
            context={"user": "test"},
            temperature=0.7,
            max_tokens=1000,
            correlation_id="test-id"
        )
        
        assert request.prompt == "Test prompt"
        assert request.context == {"user": "test"}
        assert request.temperature == 0.7
        assert request.max_tokens == 1000
        assert request.correlation_id == "test-id"
    
    def test_gemini_request_defaults(self):
        """Test GeminiRequest with default values."""
        request = GeminiRequest(prompt="Test prompt")
        
        assert request.prompt == "Test prompt"
        assert request.context is None
        assert request.temperature == 0.7
        assert request.max_tokens == 1500
        assert request.correlation_id is None

class TestGeminiResponse:
    """Test cases for GeminiResponse dataclass."""
    
    def test_gemini_response_creation(self):
        """Test GeminiResponse creation."""
        response = GeminiResponse(
            content="Test response",
            usage={"totalTokenCount": 10},
            model="gemini-2.0-flash",
            correlation_id="test-id",
            timestamp=gemini_client.config.LOG_LEVEL,  # This will be fixed
            cached=False
        )
        
        assert response.content == "Test response"
        assert response.usage == {"totalTokenCount": 10}
        assert response.model == "gemini-2.0-flash"
        assert response.correlation_id == "test-id"
        assert response.cached is False
    
    def test_gemini_response_defaults(self):
        """Test GeminiResponse with default values."""
        response = GeminiResponse(
            content="Test response",
            usage={"totalTokenCount": 10},
            model="gemini-2.0-flash",
            correlation_id="test-id",
            timestamp=gemini_client.config.LOG_LEVEL  # This will be fixed
        )
        
        assert response.cached is False

if __name__ == "__main__":
    pytest.main([__file__])
