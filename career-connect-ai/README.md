# CareerConnect AI

AI-powered career counseling service designed specifically for Indian students to help them discover their ideal career paths.

## Features

- **AI-Powered Career Counseling**: Intelligent career guidance using advanced AI models
- **Personality Assessment**: RIASEC-based personality analysis for career matching
- **Learning Path Generation**: Personalized educational roadmaps
- **Mentor Matching**: Connect students with industry professionals
- **Indian Education System**: Tailored for Indian academic structure and career opportunities
- **Real-time Chat**: Interactive AI counselor for instant guidance

## Quick Start

### Prerequisites

- Python 3.8 or higher
- Redis server (for caching and rate limiting)
- Gemini API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd career-connect-ai
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

The application will be available at `http://localhost:5000`

## Configuration

### Environment Variables

Copy `env.example` to `.env` and configure:

- `GEMINI_API_KEY`: Your Gemini AI API key
- `FLASK_ENV`: Environment (development/production)
- `REDIS_URL`: Redis server URL
- `CORS_ORIGINS`: Allowed frontend origins

### API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /status` - Application status
- `GET /api/docs` - API documentation

## Development

### Project Structure

```
career-connect-ai/
├── app.py              # Main Flask application
├── config.py           # Configuration management
├── requirements.txt    # Python dependencies
├── env.example         # Environment variables template
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

### Running Tests

```bash
pytest
```

### Code Style

The project follows PEP 8 guidelines. Use black for code formatting:

```bash
black .
```

## Deployment

### Production Deployment

1. Set `FLASK_ENV=production` in your environment
2. Configure a production Redis instance
3. Set a secure `SECRET_KEY`
4. Use a production WSGI server like Gunicorn:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker Deployment

```bash
docker build -t careerconnect-ai .
docker run -p 5000:5000 careerconnect-ai
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions:
- Email: support@careerconnectai.com
- Documentation: https://docs.careerconnectai.com
- Issues: https://github.com/your-org/career-connect-ai/issues

## Roadmap

- [ ] Student profile management
- [ ] Career assessment tools
- [ ] Learning path generation
- [ ] Mentor matching system
- [ ] Real-time chat interface
- [ ] Mobile app integration
- [ ] Analytics dashboard