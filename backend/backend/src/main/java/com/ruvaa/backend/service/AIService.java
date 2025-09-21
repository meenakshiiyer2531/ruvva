package com.ruvaa.backend.service;

import org.springframework.stereotype.Service;

@Service
public class AIService {

    public String generateResponse(String userMessage) {
        if (userMessage.toLowerCase().contains("career") || userMessage.toLowerCase().contains("job")) {
            return "🎯 Based on your interests, I'd recommend exploring careers in technology, healthcare, or creative fields. " +
                   "Would you like me to help you discover specific career paths that match your personality?";
        }
        
        if (userMessage.toLowerCase().contains("college") || userMessage.toLowerCase().contains("education")) {
            return "🎓 Choosing the right college is crucial for your career. Consider factors like course curriculum, " +
                   "faculty expertise, placement records, and location. Would you like help finding colleges for a specific field?";
        }
        
        if (userMessage.toLowerCase().contains("skill") || userMessage.toLowerCase().contains("learn")) {
            return "📚 Continuous learning is key to career success! Focus on both technical and soft skills. " +
                   "I can help you identify which skills are most important for your chosen career path.";
        }
        
        if (userMessage.toLowerCase().contains("mentor") || userMessage.toLowerCase().contains("guidance")) {
            return "👨‍🏫 Having a mentor can accelerate your career growth significantly. Our platform connects you " +
                   "with experienced professionals who can provide personalized guidance. Would you like to book a session?";
        }
        
        return "💡 I'm here to help with your career counselling needs! You can ask me about careers, colleges, " +
               "skills development, or book a mentor session. How can I assist you today?";
    }
    
    public String generateAssessmentRecommendations(int score, int maxScore) {
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
}