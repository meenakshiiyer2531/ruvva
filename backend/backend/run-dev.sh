#!/bin/bash
if [ -f .env ]; then
  set -a
  source .env
  set +a
fi
echo "--- Checking environment variables ---"
echo "JWT_SECRET: $JWT_SECRET"
echo "FIREBASE_DATABASE_URL: $FIREBASE_DATABASE_URL"
echo "FIREBASE_PROJECT_ID: $FIREBASE_PROJECT_ID"
echo "GEMINI_API_KEY: $GEMINI_API_KEY"
echo "------------------------------------"
echo "Starting CareerConnect Backend in Development Mode..."
echo ""
echo "Application will be available at: http://localhost:8080/api"
echo "Swagger UI: http://localhost:8080/api/swagger-ui.html"
echo "H2 Console: http://localhost:8080/api/h2-console"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""
./mvnw clean spring-boot:run -Dspring.profiles.active=dev -Dspring.main.allow-circular-references=true