#!/bin/bash

# Backend startup script for Ruvva project
# This script sets up the environment and starts the Spring Boot backend on port 8000

echo "🚀 Starting Ruvva Backend on port 8000..."

# Navigate to backend directory
cd "$(dirname "$0")/backend/backend"

# Set environment variables
export FIREBASE_DATABASE_URL=https://ruvaa-cbcaa-default-rtdb.asia-southeast1.firebasedatabase.app/
export FIREBASE_PROJECT_ID=ruvaa-cbcaa
export GEMINI_API_KEY=AIzaSyCGo2KpKAMGU7b52skjDvAiFd6CE-v7Ohs
export JWT_SECRET=ruvaaDevSecretKeyForJWTTokenGenerationAndValidation123456789
export GOOGLE_APPLICATION_CREDENTIALS=./credentials/serviceAccountKey.json
export SERVER_PORT=8000

echo "Environment variables set:"
echo "FIREBASE_PROJECT_ID: $FIREBASE_PROJECT_ID"
echo "SERVER_PORT: $SERVER_PORT"

# Try different methods to start the backend
if [ -f "./mvnw" ]; then
    echo "Using Maven wrapper..."
    chmod +x ./mvnw
    ./mvnw spring-boot:run -Dspring.profiles.active=dev -Dserver.port=8000
elif command -v mvn &> /dev/null; then
    echo "Using system Maven..."
    mvn spring-boot:run -Dspring.profiles.active=dev -Dserver.port=8000
elif [ -f "./run-dev.sh" ]; then
    echo "Using run-dev script..."
    chmod +x ./run-dev.sh
    PORT=8000 ./run-dev.sh
else
    echo "❌ No suitable method found to run the backend"
    echo "Please ensure Maven is installed and try again"
    exit 1
fi