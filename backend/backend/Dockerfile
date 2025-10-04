# Stage 1: Build the application with Maven that has Java 21
FROM maven:3.9.6-eclipse-temurin-21 AS build
WORKDIR /app
COPY pom.xml .
COPY . .
RUN mvn clean package -DskipTests

# Stage 2: Create the final image with the Java 21 runtime
FROM eclipse-temurin:21-jre
WORKDIR /app
# CORRECTED: Use the actual JAR filename from the build
COPY --from=build /app/target/careerconnect-backend-2.0.0.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]