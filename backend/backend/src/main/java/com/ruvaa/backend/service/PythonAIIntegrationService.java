package com.ruvaa.backend.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.client.ResourceAccessException;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.extern.slf4j.Slf4j;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Service for integrating with Python AI Career Connect service
 * Provides communication between Spring Boot backend and Python Flask AI service
 */
@Slf4j
@Service
public class PythonAIIntegrationService {

    @Value("${python.ai.service.url:http://localhost:5000}")
    private String pythonAIServiceUrl;

    private final RestTemplate restTemplate;
    private final ObjectMapper objectMapper;

    public PythonAIIntegrationService() {
        this.restTemplate = new RestTemplate();
        this.objectMapper = new ObjectMapper();
    }

    /**
     * Send chat message to Python AI service
     */
    public String sendChatMessage(String message, Object profileData) {
        try {
            Map<String, Object> request = new HashMap<>();
            request.put("message", message);
            if (profileData != null) {
                request.put("profile", profileData);
            }

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<Map<String, Object>> entity = new HttpEntity<>(request, headers);

            ResponseEntity<Map> response = restTemplate.exchange(
                pythonAIServiceUrl + "/api/v1/chat",
                HttpMethod.POST,
                entity,
                Map.class
            );

            if (response.getBody() != null && response.getBody().containsKey("response")) {
                return (String) response.getBody().get("response");
            }

            log.warn("Invalid response from Python AI service");
            return generateFallbackChatResponse(message);

        } catch (ResourceAccessException e) {
            log.info("Python AI service not available at {}, using fallback", pythonAIServiceUrl);
            return generateFallbackChatResponse(message);
        } catch (Exception e) {
            log.error("Error calling Python AI chat service: {}", e.getMessage());
            return generateFallbackChatResponse(message);
        }
    }

    /**
     * Get career analysis from Python AI service
     */
    public Map<String, Object> getCareerAnalysis(Object profileData) {
        try {
            Map<String, Object> request = new HashMap<>();
            request.put("profile", profileData);

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<Map<String, Object>> entity = new HttpEntity<>(request, headers);

            ResponseEntity<Map> response = restTemplate.exchange(
                pythonAIServiceUrl + "/api/v1/careers/analyze",
                HttpMethod.POST,
                entity,
                Map.class
            );

            if (response.getBody() != null) {
                return response.getBody();
            }

        } catch (ResourceAccessException e) {
            log.info("Python AI service not available for career analysis");
        } catch (Exception e) {
            log.error("Error getting career analysis from Python AI: {}", e.getMessage());
        }

        // Return fallback career analysis
        Map<String, Object> fallback = new HashMap<>();
        fallback.put("status", "fallback");
        fallback.put("topCareers", List.of(
            Map.of("name", "Software Engineer", "match", 85, "description", "Build software applications"),
            Map.of("name", "Data Scientist", "match", 78, "description", "Analyze data for insights"),
            Map.of("name", "Product Manager", "match", 72, "description", "Manage product development")
        ));
        fallback.put("message", "Career analysis from fallback service");
        return fallback;
    }

    /**
     * Submit assessment to Python AI service
     */
    public Map<String, Object> submitAssessment(Object assessmentData) {
        try {
            Map<String, Object> request = new HashMap<>();
            request.put("assessment", assessmentData);

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<Map<String, Object>> entity = new HttpEntity<>(request, headers);

            ResponseEntity<Map> response = restTemplate.exchange(
                pythonAIServiceUrl + "/api/v1/assessment/analyze",
                HttpMethod.POST,
                entity,
                Map.class
            );

            if (response.getBody() != null) {
                return response.getBody();
            }

        } catch (ResourceAccessException e) {
            log.info("Python AI service not available for assessment");
        } catch (Exception e) {
            log.error("Error submitting assessment to Python AI: {}", e.getMessage());
        }

        // Return fallback assessment result
        Map<String, Object> fallback = new HashMap<>();
        fallback.put("status", "fallback");
        fallback.put("score", 75);
        fallback.put("recommendations", List.of(
            "Consider technology and engineering careers",
            "Develop analytical and problem-solving skills",
            "Explore data science and AI fields"
        ));
        return fallback;
    }

    /**
     * Check if Python AI service is available
     */
    public boolean isServiceAvailable() {
        try {
            ResponseEntity<Map> response = restTemplate.exchange(
                pythonAIServiceUrl + "/health",
                HttpMethod.GET,
                null,
                Map.class
            );
            return response.getStatusCode().is2xxSuccessful();
        } catch (Exception e) {
            return false;
        }
    }

    /**
     * Generate fallback chat response when Python AI service is unavailable
     */
    private String generateFallbackChatResponse(String message) {
        String lowerMessage = message.toLowerCase();

        if (lowerMessage.contains("career") || lowerMessage.contains("job")) {
            return "🎯 I'd love to help you explore career options! Based on your interests and skills, " +
                   "there are many exciting paths in technology, healthcare, business, and creative fields. " +
                   "What areas interest you most?";
        }

        if (lowerMessage.contains("college") || lowerMessage.contains("education")) {
            return "🎓 Choosing the right educational path is crucial for your career success. Consider factors like " +
                   "course curriculum, faculty quality, placement records, and location. What field of study interests you?";
        }

        if (lowerMessage.contains("skill") || lowerMessage.contains("learn")) {
            return "📚 Continuous learning is the key to career growth! Focus on developing both technical skills " +
                   "specific to your field and soft skills like communication and leadership. What skills would you like to develop?";
        }

        if (lowerMessage.contains("assessment") || lowerMessage.contains("test")) {
            return "📊 Career assessments can provide valuable insights into your personality, interests, and aptitudes. " +
                   "They help match you with suitable career paths. Would you like to take our comprehensive assessment?";
        }

        if (lowerMessage.contains("salary") || lowerMessage.contains("money")) {
            return "💰 Salary is an important consideration, but also think about growth potential, job satisfaction, " +
                   "and learning opportunities. Different careers have varying salary ranges - what field interests you?";
        }

        return "💡 I'm here to help with your career journey! You can ask me about career options, educational paths, " +
               "skill development, or take our assessment to discover careers that match your personality. " +
               "How can I assist you today?";
    }
}