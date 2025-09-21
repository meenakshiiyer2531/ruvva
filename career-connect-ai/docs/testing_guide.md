# Testing Guide

## Overview

This guide covers testing strategies, setup, and best practices for the Career Connect AI application.

## Testing Framework

The application uses pytest as the primary testing framework with the following structure:

```
tests/
├── __init__.py
├── conftest.py
├── test_gemini_integration.py
├── test_riasec_analysis.py
├── test_career_matching.py
├── test_api_endpoints.py
└── test_data_validation.py
```

## Setup

### 1. Install Testing Dependencies

```bash
pip install pytest pytest-cov pytest-mock pytest-flask
```

### 2. Test Configuration

Create `pytest.ini`:

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --verbose
    --cov=.
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
```

### 3. Test Environment

Set up test environment variables:

```env
# Test Configuration
FLASK_ENV=testing
TESTING=True
DATABASE_URL=postgresql://localhost:5432/career_connect_ai_test
REDIS_URL=redis://localhost:6379/1
GEMINI_API_KEY=test-key
```

## Test Types

### 1. Unit Tests

Test individual components in isolation.

#### Example: Testing RIASEC Analysis

```python
def test_riasec_analysis():
    analyzer = RIASECAnalyzer()
    responses = {
        'question_1': 'A',
        'question_2': 'B',
        'question_3': 'C'
    }
    
    result = analyzer.analyze_responses(responses)
    
    assert 'scores' in result
    assert 'primary_type' in result
    assert 'personality_description' in result
    assert result['primary_type'] in ['Realistic', 'Investigative', 'Artistic', 'Social', 'Enterprising', 'Conventional']
```

#### Example: Testing Career Matching

```python
def test_career_matching():
    matcher = CosineMatcher()
    student_profile = {
        'interests': ['Technology', 'Science'],
        'skills': ['Python', 'Communication'],
        'personality_traits': ['Analytical', 'Creative']
    }
    
    careers = [
        {'id': 1, 'title': 'Software Engineer', 'skills': ['Python', 'Problem-solving']},
        {'id': 2, 'title': 'Data Scientist', 'skills': ['Python', 'Statistics']}
    ]
    
    matches = matcher.find_matches(student_profile, careers)
    
    assert len(matches) > 0
    assert matches[0]['match_score'] > 0
    assert matches[0]['career_id'] in [1, 2]
```

### 2. Integration Tests

Test component interactions and external services.

#### Example: Testing Gemini Integration

```python
def test_gemini_integration():
    client = GeminiClient()
    prompt = "Analyze this student profile and provide career recommendations."
    
    response = client.generate_response(prompt)
    
    assert response is not None
    assert len(response) > 0
    assert 'career' in response.lower() or 'recommendation' in response.lower()
```

#### Example: Testing API Endpoints

```python
def test_profile_creation():
    client = app.test_client()
    profile_data = {
        'name': 'John Doe',
        'age': 20,
        'grade': '12th',
        'interests': ['Technology', 'Science'],
        'skills': ['Python', 'Communication'],
        'learning_style': 'Visual',
        'career_goals': ['Software Engineer'],
        'location': 'New York',
        'contact_info': {
            'email': 'john@example.com',
            'phone': '+1234567890'
        }
    }
    
    response = client.post('/api/profile/create', json=profile_data)
    
    assert response.status_code == 201
    data = response.get_json()
    assert 'profile' in data
    assert 'analysis' in data
    assert data['profile']['name'] == 'John Doe'
```

### 3. End-to-End Tests

Test complete user workflows.

#### Example: Complete Career Guidance Flow

```python
def test_complete_career_guidance_flow():
    client = app.test_client()
    
    # 1. Create profile
    profile_data = {
        'name': 'Jane Smith',
        'age': 19,
        'grade': '11th',
        'interests': ['Technology', 'Art'],
        'skills': ['JavaScript', 'Design'],
        'learning_style': 'Visual',
        'career_goals': ['Web Developer'],
        'location': 'California',
        'contact_info': {
            'email': 'jane@example.com',
            'phone': '+1234567891'
        }
    }
    
    profile_response = client.post('/api/profile/create', json=profile_data)
    assert profile_response.status_code == 201
    profile_id = profile_response.get_json()['profile']['id']
    
    # 2. Take RIASEC assessment
    assessment_data = {
        'responses': {
            'question_1': 'A',
            'question_2': 'B',
            'question_3': 'C'
        },
        'assessment_type': 'riasec'
    }
    
    assessment_response = client.post('/api/assessment/riasec', json=assessment_data)
    assert assessment_response.status_code == 201
    
    # 3. Get career recommendations
    recommendations_response = client.get(f'/api/career/recommendations/{profile_id}')
    assert recommendations_response.status_code == 200
    recommendations = recommendations_response.get_json()['career_recommendations']
    assert len(recommendations) > 0
    
    # 4. Get learning path
    learning_path_response = client.get(f'/api/learning/path/{profile_id}')
    assert learning_path_response.status_code == 200
    learning_path = learning_path_response.get_json()['learning_path']
    assert 'modules' in learning_path
    
    # 5. Chat with AI counselor
    chat_data = {
        'initial_context': {'topic': 'career_guidance'}
    }
    
    chat_session_response = client.post('/api/chat/session', json=chat_data)
    assert chat_session_response.status_code == 201
    session_id = chat_session_response.get_json()['session_id']
    
    message_data = {
        'message': 'What skills do I need for web development?',
        'session_id': session_id
    }
    
    message_response = client.post('/api/chat/message', json=message_data)
    assert message_response.status_code == 200
    response_data = message_response.get_json()['response_data']
    assert 'message' in response_data
```

## Test Data Management

### 1. Fixtures

Use pytest fixtures for test data:

```python
@pytest.fixture
def sample_student_profile():
    return {
        'name': 'John Doe',
        'age': 20,
        'grade': '12th',
        'interests': ['Technology', 'Science'],
        'skills': ['Python', 'Communication'],
        'learning_style': 'Visual',
        'career_goals': ['Software Engineer'],
        'location': 'New York',
        'contact_info': {
            'email': 'john@example.com',
            'phone': '+1234567890'
        }
    }

@pytest.fixture
def sample_assessment_responses():
    return {
        'question_1': 'A',
        'question_2': 'B',
        'question_3': 'C'
    }

@pytest.fixture
def sample_careers():
    return [
        {
            'id': 1,
            'title': 'Software Engineer',
            'description': 'Designs and develops software applications',
            'skills': ['Programming', 'Problem-solving', 'Communication'],
            'salary_range': '$70,000 - $120,000',
            'education_requirements': 'Bachelor\'s in Computer Science',
            'growth_outlook': 'High',
            'work_environment': 'Office, Remote'
        },
        {
            'id': 2,
            'title': 'Data Scientist',
            'description': 'Analyzes data to extract insights',
            'skills': ['Statistics', 'Machine Learning', 'Programming'],
            'salary_range': '$80,000 - $130,000',
            'education_requirements': 'Master\'s in Data Science',
            'growth_outlook': 'Very High',
            'work_environment': 'Office, Remote'
        }
    ]
```

### 2. Test Database

Set up test database with fixtures:

```python
@pytest.fixture
def test_db():
    """Create test database"""
    db.create_all()
    yield db
    db.drop_all()

@pytest.fixture
def sample_profile_in_db(test_db):
    """Create sample profile in test database"""
    profile = StudentProfile(
        name='John Doe',
        age=20,
        grade='12th',
        interests=['Technology', 'Science'],
        skills=['Python', 'Communication'],
        learning_style='Visual',
        career_goals=['Software Engineer'],
        location='New York',
        contact_info={
            'email': 'john@example.com',
            'phone': '+1234567890'
        }
    )
    db.session.add(profile)
    db.session.commit()
    return profile
```

## Mocking External Services

### 1. Mock Gemini API

```python
@pytest.fixture
def mock_gemini_client():
    with patch('core.gemini_client.GeminiClient') as mock:
        mock_instance = mock.return_value
        mock_instance.generate_response.return_value = "Based on your profile, I recommend exploring careers in technology and science."
        yield mock_instance
```

### 2. Mock External APIs

```python
@pytest.fixture
def mock_external_apis():
    with patch('services.career_discovery.CareerDiscoveryService') as mock:
        mock_instance = mock.return_value
        mock_instance.get_career_trends.return_value = [
            {
                'career': 'Software Engineer',
                'trend': 'Growing',
                'growth_rate': '15%',
                'market_demand': 'High'
            }
        ]
        yield mock_instance
```

## Test Coverage

### 1. Coverage Configuration

Configure coverage in `pytest.ini`:

```ini
[tool:pytest]
addopts = 
    --cov=.
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
    --cov-exclude=tests/*
    --cov-exclude=venv/*
    --cov-exclude=*.pyc
```

### 2. Coverage Reports

Generate coverage reports:

```bash
# HTML report
pytest --cov=. --cov-report=html

# Terminal report
pytest --cov=. --cov-report=term-missing

# XML report for CI/CD
pytest --cov=. --cov-report=xml
```

### 3. Coverage Targets

- **Overall Coverage**: 80%+
- **Core Modules**: 90%+
- **API Endpoints**: 85%+
- **Services**: 85%+
- **Models**: 90%+

## Continuous Integration

### 1. GitHub Actions

Create `.github/workflows/test.yml`:

```yaml
name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: career_connect_ai_test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      
      redis:
        image: redis:6-alpine
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.8
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov pytest-mock pytest-flask
    
    - name: Run tests
      env:
        FLASK_ENV: testing
        TESTING: True
        DATABASE_URL: postgresql://postgres:postgres@localhost:5432/career_connect_ai_test
        REDIS_URL: redis://localhost:6379/1
        GEMINI_API_KEY: test-key
      run: |
        pytest --cov=. --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v1
      with:
        file: ./coverage.xml
```

### 2. Pre-commit Hooks

Create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.0.1
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict
  
  - repo: https://github.com/psf/black
    rev: 22.3.0
    hooks:
      - id: black
        language_version: python3
  
  - repo: https://github.com/pycqa/flake8
    rev: 4.0.1
    hooks:
      - id: flake8
  
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v0.950
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
```

## Performance Testing

### 1. Load Testing

Use pytest-benchmark for performance testing:

```python
def test_profile_creation_performance(benchmark):
    client = app.test_client()
    profile_data = {
        'name': 'John Doe',
        'age': 20,
        'grade': '12th',
        'interests': ['Technology', 'Science'],
        'skills': ['Python', 'Communication'],
        'learning_style': 'Visual',
        'career_goals': ['Software Engineer'],
        'location': 'New York',
        'contact_info': {
            'email': 'john@example.com',
            'phone': '+1234567890'
        }
    }
    
    result = benchmark(client.post, '/api/profile/create', json=profile_data)
    assert result.status_code == 201
```

### 2. Stress Testing

Use pytest-xdist for parallel testing:

```bash
pytest -n auto  # Run tests in parallel
```

## Test Maintenance

### 1. Test Organization

- Group related tests in classes
- Use descriptive test names
- Keep tests focused and atomic
- Avoid test interdependencies

### 2. Test Data

- Use realistic test data
- Keep test data minimal
- Use factories for complex data
- Clean up test data after tests

### 3. Test Documentation

- Document test scenarios
- Explain complex test logic
- Keep test documentation updated
- Use docstrings for test methods

## Troubleshooting

### Common Issues

1. **Test Database Issues**
   - Ensure test database is properly configured
   - Check database connection settings
   - Verify test data cleanup

2. **Mock Issues**
   - Check mock setup and teardown
   - Verify mock return values
   - Ensure mocks are properly patched

3. **Coverage Issues**
   - Check coverage configuration
   - Verify excluded files
   - Review coverage targets

### Debugging Tests

Use pytest debugging features:

```bash
# Run specific test with verbose output
pytest -v tests/test_specific.py::test_specific_function

# Run tests with debugging
pytest --pdb tests/test_specific.py

# Run tests with logging
pytest --log-cli-level=DEBUG tests/test_specific.py
```

## Best Practices

### 1. Test Design

- Write tests before code (TDD)
- Keep tests simple and focused
- Use descriptive test names
- Test edge cases and error conditions

### 2. Test Maintenance

- Keep tests up to date
- Remove obsolete tests
- Refactor tests when needed
- Monitor test performance

### 3. Test Quality

- Aim for high test coverage
- Ensure tests are reliable
- Use appropriate test types
- Follow testing conventions

## Resources

- **pytest Documentation**: https://docs.pytest.org/
- **Testing Best Practices**: https://docs.python.org/3/library/unittest.html
- **Mock Documentation**: https://docs.python.org/3/library/unittest.mock.html
- **Coverage Documentation**: https://coverage.readthedocs.io/
