# Stage 1: Build the application with Maven
FROM maven:3.8.5-openjdk-17 AS build
WORKDIR /app
COPY pom.xml .
COPY . .
RUN mvn clean package -DskipTests

# Stage 2: Create the final, smaller image with only the Java runtime
FROM eclipse-temurin:17-jre-jammy
WORKDIR /app
# IMPORTANT: Make sure the .jar file name here matches the one in your 'target' folder!
COPY --from=build /app/target/ruvva-0.0.1-SNAPSHOT.jar app.jar
EXPOSE 8080
# This is the command to run your application
ENTRYPOINT ["java", "-jar", "app.jar"]
