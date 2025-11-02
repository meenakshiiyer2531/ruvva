# CareerConnect AI - AI Service Flow

## Overview
CareerConnect AI uses Google Gemini 2.0 Flash as its core AI engine, integrated through multiple services for career counseling, analysis, and recommendations.

---

## 🔄 Complete AI Service Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        USER REQUEST ENTRY POINTS                        │
└─────────────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
  ┌──────────┐         ┌──────────┐         ┌──────────┐
  │   Chat   │         │ Career   │         │Assessment│
  │  Routes  │         │ Routes   │         │  Routes  │
  └──────────┘         └──────────┘         └──────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         SERVICE LAYER                                   │
│  ┌─────────────────┐  ┌──────────────────┐  ┌──────────────────┐     │
│  │ ChatService     │  │CareerDiscovery   │  │ RIASECAnalyzer   │     │
│  │                 │  │ Service          │  │                  │     │
│  │ - Process msg   │  │ - Profile match  │  │ - Score calc     │     │
│  │ - Manage session│  │ - Career search  │  │ - Analysis       │     │
│  │ - Context mgmt  │  │ - Recommendations│  │ - Career mapping│     │
│  └─────────────────┘  └──────────────────┘  └──────────────────┘     │
│                                 │                                     │
│  ┌─────────────────┐  ┌──────────────────┐                          │
│  │ProfileAnalyzer  │  │CosineMatcher     │                          │
│  │                 │  │                  │                          │
│  │ - Academic      │  │ - Vector calc    │                          │
│  │ - Skills        │  │ - Similarity     │                          │
│  │ - Interests     │  │ - Matching       │                          │
│  └─────────────────┘  └──────────────────┘                          │
└─────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    CORE AI LAYER - GeminiClient                          │
│  ┌──────────────────────────────────────────────────────────────┐      │
│  │                     GeminiClient                              │      │
│  │                                                               │      │
│  │  Methods:                                                     │      │
│  │  ├─ generate_response(prompt, context, temp=0.7, max=300)    │      │
│  │  ├─ chat_response(message, history, student_context)         │      │
│  │  ├─ analyze_student_profile(profile_data)                    │      │
│  │  ├─ generate_career_recommendations(profile, riasec)         │      │
│  │  └─ create_learning_path(career, skills, timeline)           │      │
│  │                                                               │      │
│  │  Features:                                                    │      │
│  │  ├─ Redis Caching (TTL: 3600s)                               │      │
│  │  ├─ Async/Await Support                                       │      │
│  │  ├─ Retry Logic (3 attempts, exponential backoff)            │      │
│  │  ├─ Prompt Templates (career counseling, RIASEC, etc.)       │      │
│  │  └─ Response Validation                                       │      │
│  └──────────────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    GOOGLE GEMINI 2.0 FLASH API                           │
│  ┌──────────────────────────────────────────────────────────────┐      │
│  │  Endpoint: /v1beta/models/gemini-2.0-flash:generateContent    │      │
│  │                                                               │      │
│  │  Request:                                                     │      │
│  │  {                                                            │      │
│  │    "contents": [{"parts": [{"text": "<prompt>"}]}],          │      │
│  │    "generationConfig": {                                      │      │
│  │      "temperature": 0.7,                                      │      │
│  │      "maxOutputTokens": 300,                                 │      │
│  │      "topP": 0.7,                                             │      │
│  │      "topK": 5                                                │      │
│  │    }                                                           │      │
│  │  }                                                            │      │
│  │                                                               │      │
│  │  Response:                                                    │      │
│  │  {                                                            │      │
│  │    "candidates": [{"content": {"parts": [...]}}],           │      │
│  │    "usageMetadata": {"totalTokenCount": 150}                 │      │
│  │  }                                                            │      │
│  └──────────────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  Process Response│
                    │  - Extract text │
                    │  - Cache result │
                    │  - Log usage    │
                    └─────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  Return to User  │
                    │  - Format JSON   │
                    │  - Add metadata  │
                    └─────────────────┘
```

---

## 📋 Detailed Flow by Use Case

### 1. AI Chat Counseling Flow

```
User Message
    │
    ▼
POST /api/v1/chat
    │
    ▼
ChatService.process_chat_message()
    │
    ├─► ConversationManager
    │   ├─ Get session context
    │   ├─ Add user message
    │   └─ Manage conversation history
    │
    ▼
ChatService._generate_ai_response()
    │
    ├─► Prepare context:
    │   ├─ Student profile
    │   ├─ Conversation history (last 10 messages)
    │   └─ Current message
    │
    ▼
GeminiClient.chat_response()
    │
    ├─► Check Redis cache
    │   ├─ Cache hit? → Return cached response
    │   └─ Cache miss? → Continue
    │
    ├─► Build prompt using 'career_counseling' template
    │   └─ Template: Simple, concise, Indian context
    │
    ├─► API Call (async):
    │   ├─ POST to Gemini API
    │   ├─ Retry on failure (3 attempts)
    │   └─ Exponential backoff
    │
    ├─► Cache response in Redis (TTL: 3600s)
    │
    └─► Return GeminiResponse(content, usage, cached)
    │
    ▼
ChatService
    ├─ Add AI response to conversation
    ├─ Update context (topics, keywords)
    ├─ Generate follow-up suggestions
    └─ Return formatted response
    │
    ▼
API Response
{
  "response": "AI-generated text...",
  "session_id": "uuid",
  "suggestions": ["Follow-up question 1", ...],
  "next_steps": ["Action 1", ...]
}
```

---

### 2. Career Analysis & Recommendations Flow

```
Profile Data
    │
    ▼
POST /api/v1/careers/analyze
    │
    ▼
CareerDiscoveryService.discover_careers_by_profile()
    │
    ├─► Extract profile components:
    │   ├─ Academic info
    │   ├─ Skills
    │   ├─ Interests
    │   ├─ RIASEC scores
    │   └─ Preferences
    │
    ▼
Multi-Factor Matching:
    │
    ├─► Skills matching (40% weight)
    ├─► Interests matching (30% weight)
    ├─► Education matching (20% weight)
    └─► Personality matching (10% weight)
    │
    ▼
Generate Career Matches
    │
    ▼
OPTIONAL: AI Enhancement
    │
    ├─► GeminiClient.generate_career_recommendations()
    │   ├─ Use 'career_counseling' template
    │   ├─ Include profile + top matches
    │   └─ Generate personalized insights
    │
    └─► Return top 2 careers (after tuning)
    │
    ▼
API Response
{
  "primary_matches": [...],
  "alternative_careers": [...],
  "recommendations": [...],
  "ai_insights": "AI-generated summary..."
}
```

---

### 3. RIASEC Assessment Flow

```
Assessment Responses
    │
    ▼
POST /api/v1/assessment/riasec/submit
    │
    ▼
RIASECAnalyzer.calculate_personality_scores()
    │
    ├─► Process 36 questions (6 per dimension)
    ├─► Calculate scores for:
    │   ├─ Realistic (R)
    │   ├─ Investigative (I)
    │   ├─ Artistic (A)
    │   ├─ Social (S)
    │   ├─ Enterprising (E)
    │   └─ Conventional (C)
    │
    ▼
RIASECAnalyzer.analyze_personality_profile()
    │
    ├─► Identify primary & secondary types
    ├─► Generate personality description
    ├─► Identify strengths
    ├─► Analyze communication style
    └─► Generate learning preferences
    │
    ▼
RIASECAnalyzer.map_careers_to_personality()
    │
    ├─► Match RIASEC codes to career database
    ├─► Calculate compatibility scores
    └─► Return top 2 career matches (after tuning)
    │
    ▼
OPTIONAL: AI Analysis
    │
    ├─► GeminiClient.generate_response()
    │   ├─ Use 'riasec_analysis' template
    │   ├─ Include scores + interests
    │   └─ Generate concise explanation
    │
    ▼
API Response
{
  "riasec_scores": {...},
  "primary_type": "Investigative",
  "career_matches": [top 2 careers],
  "personality_analysis": {...}
}
```

---

### 4. Profile Analysis Flow

```
Student Profile Data
    │
    ▼
ProfileAnalyzer.analyze_complete_profile()
    │
    ├─► Academic Analysis
    │   ├─ Extract strengths/weaknesses
    │   ├─ Performance trends
    │   └─ Stream recommendations
    │
    ├─► Extracurricular Analysis
    │   ├─ Leadership experience
    │   ├─ Activity preferences
    │   └─ Social impact score
    │
    ├─► Skills Assessment
    │   ├─ Technical skills
    │   ├─ Soft skills
    │   └─ Learning agility
    │
    └─► Interest Analysis
        ├─ Primary interests
        ├─ Interest clusters
        └─ Career pathway mapping
    │
    ▼
OPTIONAL: AI Summary Generation
    │
    ├─► GeminiClient.analyze_student_profile()
    │   ├─ Use profile analysis template
    │   ├─ Include all analysis results
    │   └─ Generate concise narrative
    │
    ▼
API Response
{
  "academic_analysis": {...},
  "extracurricular_analysis": {...},
  "skills_assessment": {...},
  "interest_analysis": {...},
  "ai_generated_summary": "Concise AI summary..."
}
```

---

## 🔧 Core Components

### GeminiClient
**Location**: `core/gemini_client.py`

**Key Methods**:
- `generate_response(prompt, context, temperature=0.7, max_tokens=300)`
  - Main method for AI text generation
  - Handles caching, retries, error handling
  
- `chat_response(message, history, student_context)`
  - Specialized for chat conversations
  - Maintains conversation context
  
- `analyze_student_profile(profile_data)`
  - Profile analysis with AI insights
  - Generates concise summaries
  
- `generate_career_recommendations(profile, riasec_scores)`
  - Career recommendations with AI explanation
  - Top 2 careers with reasons

**Configuration**:
- Model: `gemini-2.0-flash`
- Temperature: `0.7` (balanced creativity)
- Max Tokens: `300` (concise responses)
- TopP: `0.7`, TopK: `5` (focused outputs)
- Cache TTL: `3600 seconds` (1 hour)

**Prompt Templates**:
1. `career_counseling` - Chat conversations
2. `riasec_analysis` - Personality assessment analysis
3. `skill_gap_assessment` - Skills gap identification
4. `learning_path_generation` - Learning plan creation
5. `mentor_matching` - Mentor recommendations

---

## 💾 Caching Strategy

```
Request → Check Redis Cache
    │
    ├─► Cache Hit
    │   ├─ Return cached response
    │   └─ Log cache usage
    │
    └─► Cache Miss
        ├─ Call Gemini API
        ├─ Store in Redis (TTL: 3600s)
        └─ Return fresh response

Cache Key Format: "gemini:<prompt_hash>:<context_hash>"
```

---

## 🔄 Async Processing

```
Sync Request (Flask)
    │
    ▼
Create Event Loop
    │
    ▼
Run Async Gemini Call
    │
    ├─► asyncio.get_event_loop()
    ├─► loop.run_until_complete(gemini_client.generate_response())
    └─► Handle async response
    │
    ▼
Return Sync Response
```

---

## 📊 Response Format

All AI responses return:
```python
GeminiResponse(
    content: str,              # Main AI-generated text
    usage: Dict[str, int],     # Token usage stats
    model: str,                # "gemini-2.0-flash"
    correlation_id: str,       # Request tracking ID
    timestamp: datetime,       # Response time
    cached: bool               # Was response cached?
)
```

---

## 🛡️ Error Handling

```
API Call
    │
    ├─► Success → Return response
    │
    └─► Failure
        │
        ├─► Retry Attempt 1 (delay: 1s)
        │
        ├─► Retry Attempt 2 (delay: 2s)
        │
        ├─► Retry Attempt 3 (delay: 4s)
        │
        └─► Final Failure
            └─► Return error message
                "I apologize, but I'm having trouble processing..."
```

---

## 📈 Performance Optimization

1. **Redis Caching**: Reduces API calls for similar queries
2. **Async Processing**: Non-blocking AI calls
3. **Token Limits**: 300 tokens max (faster, cheaper)
4. **Prompt Templates**: Pre-optimized prompts
5. **Batch Processing**: Group similar requests

---

## 🔐 Security & Configuration

- API Key: Stored in environment/config
- Rate Limiting: Built into Gemini API
- Input Sanitization: All prompts sanitized
- Output Validation: Responses validated before return
- Logging: All requests logged with correlation IDs

---

## 📝 Key Files

- `core/gemini_client.py` - Main AI client
- `services/chat_service.py` - Chat integration
- `services/career_discovery.py` - Career matching
- `core/riasec_analyzer.py` - Personality analysis
- `core/cosine_matcher.py` - Career matching algorithm

