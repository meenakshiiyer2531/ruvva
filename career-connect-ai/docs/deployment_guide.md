# Deployment Guide

## Overview

This guide covers deploying the Career Connect AI application to various environments, including local development, staging, and production.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git
- Database (PostgreSQL recommended)
- Redis (for caching and session management)
- Environment variables configured

## Local Development Setup

### 1. Clone Repository

```bash
git clone https://github.com/your-org/career-connect-ai.git
cd career-connect-ai
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Copy the example environment file and configure:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/career_connect_ai

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# Gemini API Configuration
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-pro

# External APIs
OPENAI_API_KEY=your-openai-api-key
LINKEDIN_API_KEY=your-linkedin-api-key

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

### 5. Database Setup

```bash
# Create database
createdb career_connect_ai

# Run migrations
flask db upgrade
```

### 6. Run Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`.

## Docker Deployment

### 1. Build Docker Image

```bash
docker build -t career-connect-ai .
```

### 2. Run with Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=postgresql://postgres:password@db:5432/career_connect_ai
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    volumes:
      - ./logs:/app/logs

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=career_connect_ai
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:6-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

Run with Docker Compose:

```bash
docker-compose up -d
```

## Cloud Deployment

### AWS Deployment

#### 1. Elastic Beanstalk

Create `Dockerrun.aws.json`:

```json
{
  "AWSEBDockerrunVersion": "1",
  "Image": {
    "Name": "career-connect-ai:latest",
    "Update": "true"
  },
  "Ports": [
    {
      "ContainerPort": "5000"
    }
  ],
  "Environment": [
    {
      "Name": "FLASK_ENV",
      "Value": "production"
    },
    {
      "Name": "DATABASE_URL",
      "Value": "postgresql://username:password@rds-endpoint:5432/career_connect_ai"
    }
  ]
}
```

Deploy to Elastic Beanstalk:

```bash
eb init
eb create production
eb deploy
```

#### 2. ECS with Fargate

Create `task-definition.json`:

```json
{
  "family": "career-connect-ai",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::account:role/ecsTaskRole",
  "containerDefinitions": [
    {
      "name": "career-connect-ai",
      "image": "your-account.dkr.ecr.region.amazonaws.com/career-connect-ai:latest",
      "portMappings": [
        {
          "containerPort": 5000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "FLASK_ENV",
          "value": "production"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/career-connect-ai",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

### Google Cloud Platform

#### 1. Cloud Run

Create `cloudbuild.yaml`:

```yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/career-connect-ai', '.']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/career-connect-ai']
  - name: 'gcr.io/cloud-builders/gcloud'
    args: ['run', 'deploy', 'career-connect-ai', '--image', 'gcr.io/$PROJECT_ID/career-connect-ai', '--region', 'us-central1', '--platform', 'managed']
```

Deploy:

```bash
gcloud builds submit --config cloudbuild.yaml
```

#### 2. App Engine

Create `app.yaml`:

```yaml
runtime: python38

env_variables:
  FLASK_ENV: production
  DATABASE_URL: postgresql://username:password@/career_connect_ai?host=/cloudsql/project:region:instance

automatic_scaling:
  min_instances: 1
  max_instances: 10

handlers:
  - url: /.*
    script: auto
```

Deploy:

```bash
gcloud app deploy
```

### Azure Deployment

#### 1. Container Instances

Create `azure-deploy.json`:

```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "containerName": {
      "type": "string",
      "defaultValue": "career-connect-ai"
    },
    "image": {
      "type": "string",
      "defaultValue": "your-registry.azurecr.io/career-connect-ai:latest"
    }
  },
  "resources": [
    {
      "type": "Microsoft.ContainerInstance/containerGroups",
      "apiVersion": "2021-03-01",
      "name": "[parameters('containerName')]",
      "location": "[resourceGroup().location]",
      "properties": {
        "containers": [
          {
            "name": "[parameters('containerName')]",
            "properties": {
              "image": "[parameters('image')]",
              "ports": [
                {
                  "port": 5000
                }
              ],
              "environmentVariables": [
                {
                  "name": "FLASK_ENV",
                  "value": "production"
                }
              ]
            }
          }
        ],
        "osType": "Linux",
        "ipAddress": {
          "type": "Public",
          "ports": [
            {
              "port": 5000,
              "protocol": "TCP"
            }
          ]
        }
      }
    }
  ]
}
```

Deploy:

```bash
az deployment group create --resource-group myResourceGroup --template-file azure-deploy.json
```

## Production Considerations

### 1. Security

- Use HTTPS in production
- Implement proper authentication and authorization
- Regularly update dependencies
- Use environment variables for sensitive data
- Implement rate limiting
- Use security headers

### 2. Performance

- Enable caching (Redis)
- Use CDN for static assets
- Implement database connection pooling
- Monitor application performance
- Use load balancing for high availability

### 3. Monitoring

- Set up application monitoring (e.g., New Relic, DataDog)
- Implement logging and log aggregation
- Set up health checks
- Monitor database performance
- Track API usage and errors

### 4. Backup and Recovery

- Regular database backups
- Test backup restoration procedures
- Implement disaster recovery plan
- Document recovery procedures

## Environment-Specific Configurations

### Development

```env
FLASK_ENV=development
DEBUG=True
LOG_LEVEL=DEBUG
DATABASE_URL=postgresql://localhost:5432/career_connect_ai_dev
```

### Staging

```env
FLASK_ENV=staging
DEBUG=False
LOG_LEVEL=INFO
DATABASE_URL=postgresql://staging-db:5432/career_connect_ai_staging
```

### Production

```env
FLASK_ENV=production
DEBUG=False
LOG_LEVEL=WARNING
DATABASE_URL=postgresql://prod-db:5432/career_connect_ai_prod
```

## Health Checks

Implement health check endpoints:

```python
@app.route('/health')
def health_check():
    return {
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    }

@app.route('/health/detailed')
def detailed_health_check():
    checks = {
        'database': check_database_connection(),
        'redis': check_redis_connection(),
        'external_apis': check_external_apis()
    }
    
    overall_status = 'healthy' if all(checks.values()) else 'unhealthy'
    
    return {
        'status': overall_status,
        'checks': checks,
        'timestamp': datetime.utcnow().isoformat()
    }
```

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Check database URL format
   - Verify database server is running
   - Check network connectivity

2. **Redis Connection Errors**
   - Verify Redis server is running
   - Check Redis URL format
   - Verify Redis configuration

3. **API Key Issues**
   - Verify API keys are correct
   - Check API key permissions
   - Monitor API usage limits

4. **Memory Issues**
   - Monitor memory usage
   - Implement memory optimization
   - Use memory profiling tools

### Log Analysis

Monitor application logs for:

- Error patterns
- Performance bottlenecks
- Security issues
- API usage patterns

### Performance Tuning

- Optimize database queries
- Implement caching strategies
- Use connection pooling
- Monitor resource usage

## Maintenance

### Regular Tasks

1. **Weekly**
   - Review application logs
   - Check system performance
   - Update dependencies

2. **Monthly**
   - Security updates
   - Performance optimization
   - Backup verification

3. **Quarterly**
   - Disaster recovery testing
   - Security audit
   - Capacity planning

### Updates and Patches

- Test updates in staging environment
- Implement blue-green deployment
- Monitor application after updates
- Rollback procedures if needed

## Support

For deployment support:

- **Documentation**: https://docs.careerconnectai.com/deployment
- **Issues**: https://github.com/your-org/career-connect-ai/issues
- **Email**: deployment-support@careerconnectai.com
