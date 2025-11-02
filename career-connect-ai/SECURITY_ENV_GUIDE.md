# CareerConnect AI Environment & Secrets Guide

This project uses environment variables and external credential files for configuration. DO NOT commit real secrets (API keys, private keys, JWT secrets) to version control.

## 1. Creating Your `.env`
Copy `env.example` to `.env`:

```
cp career-connect-ai/env.example career-connect-ai/.env
```

Edit the values:

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| SECRET_KEY | Flask session encryption | Yes | generate with `openssl rand -hex 32` |
| FLASK_ENV | Environment mode | Yes | development |
| FLASK_PORT | Port for Flask server | Yes | 5000 |
| GEMINI_API_KEY | Google Gemini API Key | Optional (degraded without) | `AIza...` |
| GEMINI_MODEL | Gemini model name | Optional | gemini-pro |
| CORS_ORIGINS | Allowed front-end origins | Yes | http://localhost:3000 |
| REDIS_URL | Redis connection | Optional | redis://localhost:6379 |
| REDIS_DB | Redis database index | Optional | 0 |
| LOG_LEVEL | Logging verbosity | Yes | INFO |
| LOG_FILE | Log file path | Optional | logs/careerconnect.log |
| DATABASE_URL | SQLAlchemy database URL | Optional | sqlite:///careerconnect.db |
| OPENAI_API_KEY | OpenAI API key | Optional | sk-*** |
| LINKEDIN_API_KEY | LinkedIn API key | Optional | *** |
| MAIL_* | SMTP settings | Optional | see example |
| MAX_PROFILE_SIZE | Max profile JSON bytes | Yes | 10000 |
| MAX_ASSESSMENT_QUESTIONS | Limit assessment size | Yes | 100 |
| CACHE_TTL | Cache default expiration (s) | Yes | 3600 |
| FIREBASE_PROJECT_ID | Firebase project ID | Optional | ruvva-cbcaa |
| FIREBASE_DATABASE_URL | Firebase RTDB URL | Optional | https://...firebaseio.com/ |
| FIREBASE_CREDENTIALS_PATH | Path to service account JSON | Yes if Firebase used | credentials/serviceAccountKey.json |
| JWT_SECRET | JWT signing secret | Yes | long random string |

## 2. Service Account Credentials
Place Google service account JSON at:

```
career-connect-ai/credentials/serviceAccountKey.json
```

Ensure `.gitignore` excludes it (already configured). Never embed the JSON content directly in `.env`.

## 3. Generating Safe Secrets
```
# Strong secret keys
openssl rand -hex 32

# JWT secret example
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

## 4. Front-end Environment Variables
Create `ruvaa-frontend/.env` (not committed):

```
REACT_APP_SPRING_BOOT_API=http://localhost:8000/api
REACT_APP_PYTHON_AI_API=http://localhost:5000
REACT_APP_DEFAULT_LANGUAGE=en
REACT_APP_SUPPORTED_LANGUAGES=en,hi,ml,ta,te,bn,gu,mr,pa
REACT_APP_ENABLE_MULTILANGUAGE=true
REACT_APP_ENABLE_SEARCH=true
```

Restart the React dev server after changes.

## 5. Running Locally
Backend:
```
cd career-connect-ai
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

Frontend:
```
cd ruvaa-frontend
npm install
npm start
```

## 6. Health Checks
- Flask: http://localhost:5000/health
- Python AI endpoints: http://localhost:5000/api/v1/*
- Spring Boot (if running separately): http://localhost:8000/api/actuator/health

## 7. Common Issues
| Issue | Cause | Fix |
|-------|-------|-----|
| CORS error | Origin not in CORS_ORIGINS | Add origin to .env and restart backend |
| 401 Unauthorized | Missing/BAD JWT token | Re-login; ensure JWT_SECRET matches signing code |
| Redis unavailable | Redis not running | Start Redis or remove dependent features |
| Gemini degraded | Missing GEMINI_API_KEY | Add key or disable Gemini features |

## 8. Security Notes
- Rotate API keys regularly.
- Use separate keys for dev and prod.
- Never post private keys in chat or commit history.
- Consider Vault or AWS/GCP Secret Manager for production.

## 9. Deployment Considerations
- Use environment variables in hosting platform (Render/Heroku/Vercel).
- Provide separate `.env.production` locally only (never commit).
- Configure logging to external service for observability.

## 10. Next Steps
- Implement secure secret fetch (e.g., AWS SSM) for prod.
- Add automated lint check to reject accidental secret commits.
- Integrate health dashboard into frontend UI.
