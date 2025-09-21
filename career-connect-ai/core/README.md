# Gemini Client for CareerConnect AI

A production-ready Google Gemini 2.0 Flash API client specifically designed for AI-powered career counseling services for Indian students.

## Features

- **Async/Await Support**: High-performance asynchronous operations
- **Comprehensive Error Handling**: Exponential backoff, rate limiting, and timeout management
- **Redis Caching**: Intelligent response caching to reduce API costs and improve performance
- **Request/Response Logging**: Full correlation ID tracking for debugging and monitoring
- **Specialized Prompt Templates**: Pre-built templates for Indian career counseling scenarios
- **Input Sanitization**: Security-focused input validation and sanitization
- **Production Ready**: Robust error handling, logging, and performance optimization

## Installation

The client is included in the main CareerConnect AI project. Install dependencies:

```bash
pip install -r requirements.txt
```

## Quick Start

### Basic Usage

```python
import asyncio
from core.gemini_client import GeminiClient

async def main():
    # Initialize client
    client = GeminiClient(api_key="your-gemini-api-key")
    
    # Generate basic response
    response = await client.generate_response("Hello, how are you?")
    print(response.content)

# Run the async function
asyncio.run(main())
```

### Student Profile Analysis

```python
async def analyze_student():
    client = GeminiClient()
    
    profile = {
        "name": "Rajesh Kumar",
        "age": 17,
        "grade": "12th",
        "interests": ["Technology", "Mathematics"],
        "skills": ["Python", "Problem Solving"],
        "location": "Mumbai"
    }
    
    analysis = await client.analyze_student_profile(profile)
    print(analysis.content)
```

### Career Recommendations

```python
async def get_career_recommendations():
    client = GeminiClient()
    
    riasec_scores = {
        "Realistic": 85,
        "Investigative": 90,
        "Artistic": 70,
        "Social": 60,
        "Enterprising": 75,
        "Conventional": 65
    }
    interests = ["Technology", "Science"]
    
    recommendations = await client.generate_career_recommendations(riasec_scores, interests)
    print(recommendations.content)
```

### Learning Path Generation

```python
async def create_learning_path():
    client = GeminiClient()
    
    learning_path = await client.create_learning_path(
        career_choice="Software Engineer",
        current_skills=["Python", "Basic Programming"],
        education_level="12th",
        learning_style="Visual",
        time_available="6 months",
        budget="moderate"
    )
    print(learning_path.content)
```

### Chat Counseling

```python
async def chat_counseling():
    client = GeminiClient()
    
    conversation_history = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi! How can I help you?"}
    ]
    
    student_context = {
        "name": "Priya",
        "interests": ["Art", "Design"],
        "grade": "11th"
    }
    
    response = await client.chat_response(
        message="What careers match my personality?",
        conversation_history=conversation_history,
        student_context=student_context
    )
    print(response.content)
```

## Configuration

### Environment Variables

Set these environment variables in your `.env` file:

```env
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-2.0-flash
REDIS_URL=redis://localhost:6379
CACHE_TTL=3600
```

### Client Configuration

```python
from core.gemini_client import GeminiClient
import redis

# With Redis caching
redis_client = redis.from_url("redis://localhost:6379")
client = GeminiClient(
    api_key="your-api-key",
    redis_client=redis_client
)

# Without Redis (caching disabled)
client = GeminiClient(api_key="your-api-key")
```

## API Reference

### GeminiClient Class

#### Constructor

```python
GeminiClient(api_key: Optional[str] = None, redis_client: Optional[redis.Redis] = None)
```

- `api_key`: Google Gemini API key (required)
- `redis_client`: Redis client for caching (optional)

#### Methods

##### `async initialize_client(api_key: str) -> bool`

Initialize client with a new API key and test the connection.

```python
success = await client.initialize_client("new-api-key")
```

##### `async generate_response(prompt: str, context: Optional[Dict] = None, temperature: float = 0.7, max_tokens: int = 1500) -> GeminiResponse`

Generate a response from the Gemini API.

**Parameters:**
- `prompt`: Input prompt text
- `context`: Additional context data
- `temperature`: Response creativity (0.0-1.0)
- `max_tokens`: Maximum response length

**Returns:** `GeminiResponse` object

##### `async analyze_student_profile(profile_data: Dict[str, Any]) -> GeminiResponse`

Analyze a student's profile for career guidance.

**Parameters:**
- `profile_data`: Student profile information

**Returns:** `GeminiResponse` with analysis

##### `async generate_career_recommendations(riasec_scores: Dict[str, float], interests: List[str]) -> GeminiResponse`

Generate career recommendations based on RIASEC scores.

**Parameters:**
- `riasec_scores`: Dictionary with RIASEC personality scores
- `interests`: List of student interests

**Returns:** `GeminiResponse` with recommendations

##### `async create_learning_path(career_choice: str, current_skills: List[str], education_level: str = "12th", learning_style: str = "mixed", time_available: str = "6 months", budget: str = "moderate") -> GeminiResponse`

Create a personalized learning path.

**Parameters:**
- `career_choice`: Target career
- `current_skills`: Current skill set
- `education_level`: Current education level
- `learning_style`: Preferred learning style
- `time_available`: Available time for learning
- `budget`: Budget constraints

**Returns:** `GeminiResponse` with learning path

##### `async chat_response(message: str, conversation_history: List[Dict[str, str]], student_context: Dict[str, Any]) -> GeminiResponse`

Generate chat response for career counseling.

**Parameters:**
- `message`: User message
- `conversation_history`: Previous conversation
- `student_context`: Student context

**Returns:** `GeminiResponse` with chat response

### GeminiResponse Class

```python
@dataclass
class GeminiResponse:
    content: str                    # Generated content
    usage: Dict[str, int]           # Token usage information
    model: str                      # Model used
    correlation_id: str             # Request correlation ID
    timestamp: datetime             # Response timestamp
    cached: bool = False            # Whether response was cached
```

### GeminiRequest Class

```python
@dataclass
class GeminiRequest:
    prompt: str                     # Input prompt
    context: Optional[Dict] = None  # Additional context
    temperature: float = 0.7         # Response creativity
    max_tokens: int = 1500         # Maximum tokens
    correlation_id: Optional[str] = None  # Request ID
```

## Error Handling

The client includes comprehensive error handling:

### Rate Limiting (429)

```python
try:
    response = await client.generate_response("Test prompt")
except Exception as e:
    if "Rate limit exceeded" in str(e):
        print("Rate limit exceeded, please wait")
```

### Authentication Errors (401)

```python
try:
    response = await client.generate_response("Test prompt")
except Exception as e:
    if "Invalid API key" in str(e):
        print("Check your API key")
```

### Network Timeouts

```python
try:
    response = await client.generate_response("Test prompt")
except Exception as e:
    if "Request timeout" in str(e):
        print("Network timeout, please try again")
```

## Caching

The client supports Redis-based caching to improve performance and reduce API costs:

```python
import redis
from core.gemini_client import GeminiClient

# Initialize Redis client
redis_client = redis.from_url("redis://localhost:6379")

# Initialize Gemini client with caching
client = GeminiClient(
    api_key="your-api-key",
    redis_client=redis_client
)

# Responses will be automatically cached
response1 = await client.generate_response("What is AI?")
response2 = await client.generate_response("What is AI?")  # This will be cached
```

## Logging

The client includes comprehensive logging:

```python
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Client logs will include:
# - Request/response correlation IDs
# - Token usage information
# - Error details
# - Cache hit/miss information
```

## Prompt Templates

The client includes specialized prompt templates for Indian career counseling:

### Career Counseling Template

```
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
```

### RIASEC Analysis Template

```
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
```

## Testing

Run the test suite:

```bash
pytest test_gemini_client.py -v
```

Run the example:

```bash
export GEMINI_API_KEY="your-api-key"
python example_gemini_usage.py
```

## Performance Optimization

### Async Operations

Use async/await for better performance:

```python
# Good: Async operations
async def process_multiple_requests():
    tasks = [
        client.generate_response("Prompt 1"),
        client.generate_response("Prompt 2"),
        client.generate_response("Prompt 3")
    ]
    responses = await asyncio.gather(*tasks)
    return responses
```

### Caching Strategy

Enable Redis caching for repeated queries:

```python
# Cache frequently asked questions
common_questions = [
    "What is artificial intelligence?",
    "How to become a software engineer?",
    "What are the best engineering colleges in India?"
]

for question in common_questions:
    response = await client.generate_response(question)
    # Response will be cached for future use
```

## Troubleshooting

### Common Issues

1. **API Key Not Working**
   ```python
   # Test API key
   try:
       await client.initialize_client("your-api-key")
       print("API key is valid")
   except Exception as e:
       print(f"API key error: {e}")
   ```

2. **Redis Connection Issues**
   ```python
   # Test Redis connection
   try:
       redis_client.ping()
       print("Redis connected")
   except redis.ConnectionError:
       print("Redis connection failed")
   ```

3. **Rate Limiting**
   ```python
   # Handle rate limiting
   try:
       response = await client.generate_response("Test")
   except Exception as e:
       if "Rate limit exceeded" in str(e):
           await asyncio.sleep(60)  # Wait 1 minute
           response = await client.generate_response("Test")
   ```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License.
