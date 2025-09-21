package com.ruvaa.backend;

import io.swagger.v3.oas.annotations.OpenAPIDefinition;
import io.swagger.v3.oas.annotations.info.Contact;
import io.swagger.v3.oas.annotations.info.Info;
import io.swagger.v3.oas.annotations.info.License;
import io.swagger.v3.oas.annotations.servers.Server;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cache.annotation.EnableCaching;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.annotation.EnableScheduling;

/**
 * CareerConnect AI Career Counseling System
 * 
 * A production-ready Spring Boot application for AI-powered career counseling
 * specifically designed for Indian students and job market.
 * 
 * Key Features:
 * - Google Gemini AI integration for intelligent career analysis
 * - Firebase backend for scalable data storage
 * - RIASEC personality analysis
 * - Mentor matching using cosine similarity
 * - Real-time chat counseling
 * - Indian job market specific recommendations
 * 
 * @author CareerConnect Team
 * @version 2.0.0
 */
@Slf4j
@SpringBootApplication
@EnableCaching
@EnableAsync
@EnableScheduling
@OpenAPIDefinition(
    info = @Info(
        title = "CareerConnect API",
        version = "2.0.0",
        description = "AI-Powered Career Counseling System for Indian Students",
        contact = @Contact(
            name = "CareerConnect Support",
            email = "support@careerconnect.ai",
            url = "https://careerconnect.ai"
        ),
        license = @License(
            name = "MIT License",
            url = "https://opensource.org/licenses/MIT"
        )
    ),
    servers = {
        @Server(url = "/api", description = "Development Server"),
        @Server(url = "https://api.careerconnect.ai", description = "Production Server")
    }
)
public class CareerConnectApplication {

    /**
     * Main entry point for the CareerConnect application.
     * 
     * @param args command line arguments
     */
    public static void main(String[] args) {
        log.info("Starting CareerConnect AI Career Counseling System...");
        
        try {
            SpringApplication application = new SpringApplication(CareerConnectApplication.class);
            
            // Set default profile if none specified
            application.setDefaultProperties(
                java.util.Map.of("spring.profiles.default", "dev")
            );
            
            application.run(args);
            
            log.info("CareerConnect application started successfully!");
            
        } catch (Exception e) {
            log.error("Failed to start CareerConnect application", e);
            System.exit(1);
        }
    }
}