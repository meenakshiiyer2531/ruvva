package com.ruvaa.backend.service;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class AIService {

    private final PythonAIIntegrationService pythonAIService;

    public String generateResponse(String userMessage) {
        return generateResponse(userMessage, null);
    }

    public String generateResponse(String userMessage, Object profileData) {
        // Try Python AI service first, fallback to local logic
        return pythonAIService.sendChatMessage(userMessage, profileData);
    }

    public String generateAssessmentRecommendations(int score, int maxScore) {
        // Try to get AI-powered recommendations
        try {
            var assessmentData = java.util.Map.of(
                "score", score,
                "maxScore", maxScore,
                "percentage", (double) score / maxScore * 100
            );

            var result = pythonAIService.submitAssessment(assessmentData);
            if (result.containsKey("recommendations")) {
                var recommendations = result.get("recommendations");
                if (recommendations instanceof java.util.List) {
                    return String.join(". ", (java.util.List<String>) recommendations);
                }
            }
        } catch (Exception e) {
            // Fall through to local recommendations
        }

        // Fallback to local recommendations
        double percentage = (double) score / maxScore * 100;

        if (percentage >= 80) {
            return "🌟 Excellent! You show strong aptitude for analytical and creative thinking. " +
                   "Consider careers in Engineering, Data Science, Design, or Research fields.";
        } else if (percentage >= 60) {
            return "👍 Good potential! You have balanced skills. Explore careers in Business, " +
                   "Education, Healthcare, or Project Management.";
        } else if (percentage >= 40) {
            return "💪 You're on the right track! Focus on developing your strengths. " +
                   "Consider careers in Sales, Customer Service, or Administrative roles.";
        } else {
            return "🎯 Everyone has unique talents! Let's work together to identify your strengths " +
                   "and find the perfect career path for you.";
        }
    }

    public java.util.Map<String, Object> getCareerAnalysis(Object profileData) {
        return pythonAIService.getCareerAnalysis(profileData);
    }

    public boolean isPythonAIServiceAvailable() {
        return pythonAIService.isServiceAvailable();
    }
}