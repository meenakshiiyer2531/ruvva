#!/bin/bash
echo "Starting CareerConnect Backend in Development Mode..."
echo ""
echo "Application will be available at: http://localhost:8080/api"
echo "Swagger UI: http://localhost:8080/api/swagger-ui.html"
echo "H2 Console: http://localhost:8080/api/h2-console"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""
./mvnw spring-boot:run -Dspring.profiles.active=dev