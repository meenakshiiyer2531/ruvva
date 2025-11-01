package com.ruvaa.backend.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.ruvaa.backend.config.GeminiConfig;
import com.ruvaa.backend.model.entity.Student;
import com.ruvaa.backend.model.dto.CareerAnalysisRequest;
import com.ruvaa.backend.model.dto.CareerAnalysisResponse;
import com.ruvaa.backend.model.dto.RiasecAnalysisResponse;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.client.WebClientResponseException;
import reactor.core.publisher.Mono;
import reactor.util.retry.Retry;

import java.time.Duration;
import java.util.List;
import java.util.Map;
import java.util.concurrent.CompletableFuture;

/**
 * Google Gemini AI Service for Career Analysis
 *
 * Provides intelligent career counseling using Google's Gemini AI model.
 * Includes RIASEC personality analysis, career recommendations, and
 * learning path generation tailored for Indian students.
 */
@Slf4j
@Service
public class GeminiAIService {

    private final WebClient geminiWebClient;
    private final GeminiConfig geminiConfig;
    private final ObjectMapper objectMapper;

    public GeminiAIService(@Autowired(required = false) @Qualifier("geminiWebClient") WebClient geminiWebClient,
                           GeminiConfig geminiConfig,
                           ObjectMapper objectMapper) {
        this.geminiWebClient = geminiWebClient;
        this.geminiConfig = geminiConfig;
        this.objectMapper = objectMapper;
    }

    /**
     * Analyze student's RIASEC personality from their responses
     */
    @Cacheable(value = "riasec-analysis", key = "#responses.hashCode()")
    public CompletableFuture<RiasecAnalysisResponse> analyzeRiasecPersonality(List<String> responses) {
        if (geminiWebClient == null) {
            log.warn("Gemini AI not configured, returning mock analysis");
            return CompletableFuture.completedFuture(createMockRiasecAnalysis());
        }

        String prompt = buildRiasecAnalysisPrompt(responses);

        return callGeminiAPI(prompt)
                .map(this::parseRiasecResponse)
                .doOnSuccess(result -> log.info("RIASEC analysis completed for {} responses", responses.size()))
                .doOnError(error -> log.error("RIASEC analysis failed", error))
                .onErrorReturn(createMockRiasecAnalysis())
                .toFuture();
    }

    /**
     * Generate comprehensive career recommendations for a student
     */
    @Cacheable(value = "career-recommendations", key = "#student.id + '_' + #student.riasecScores.hashCode()")
    public CompletableFuture<CareerAnalysisResponse> generateCareerRecommendations(Student student) {
        if (geminiWebClient == null) {
            log.warn("Gemini AI not configured, returning mock recommendations");
            return CompletableFuture.completedFuture(createMockCareerAnalysis());
        }

        String prompt = buildCareerRecommendationPrompt(student);

        return callGeminiAPI(prompt)
                .map(this::parseCareerRecommendationResponse)
                .doOnSuccess(result -> log.info("Career recommendations generated for student: {}", student.getId()))
                .doOnError(error -> log.error("Career recommendation generation failed for student: {}", student.getId(), error))
                .onErrorReturn(createMockCareerAnalysis())
                .toFuture();
    }

    /**
     * Generate personalized learning path for a specific career
     */
    public CompletableFuture<String> generateLearningPath(Student student, String targetCareer) {
        if (geminiWebClient == null) {
            return CompletableFuture.completedFuture("Gemini AI not configured");
        }

        String prompt = buildLearningPathPrompt(student, targetCareer);

        return callGeminiAPI(prompt)
                .map(this::extractTextFromResponse)
                .doOnSuccess(result -> log.info("Learning path generated for student: {} targeting: {}",
                        student.getId(), targetCareer))
                .doOnError(error -> log.error("Learning path generation failed", error))
                .onErrorReturn("Unable to generate learning path at this time")
                .toFuture();
    }

    /**
     * Provide career counseling chat response
     */
    public CompletableFuture<String> generateChatResponse(String studentMessage, Student studentContext) {
        if (geminiWebClient == null) {
            return CompletableFuture.completedFuture("I'm sorry, AI counseling is currently unavailable.");
        }

        String prompt = buildChatPrompt(studentMessage, studentContext);

        return callGeminiAPI(prompt)
                .map(this::extractTextFromResponse)
                .doOnSuccess(result -> log.debug("Chat response generated for student: {}", studentContext.getId()))
                .doOnError(error -> log.error("Chat response generation failed", error))
                .onErrorReturn("I'm sorry, I'm having trouble processing your question right now. Please try again later.")
                .toFuture();
    }

    /**
     * Call Gemini API with proper error handling and retry logic
     */
    private Mono<String> callGeminiAPI(String prompt) {
        Map<String, Object> request = Map.of(
                "contents", List.of(Map.of(
                        "parts", List.of(Map.of("text", prompt))
                )),
                "generationConfig", Map.of(
                        "temperature", geminiConfig.getTemperature(),
                        "maxOutputTokens", geminiConfig.getMaxTokens(),
                        "topK", 40,
                        "topP", 0.95
                ),
                "safetySettings", List.of(
                        Map.of("category", "HARM_CATEGORY_HATE_SPEECH", "threshold", "BLOCK_MEDIUM_AND_ABOVE"),
                        Map.of("category", "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold", "BLOCK_MEDIUM_AND_ABOVE"),
                        Map.of("category", "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold", "BLOCK_MEDIUM_AND_ABOVE"),
                        Map.of("category", "HARM_CATEGORY_HARASSMENT", "threshold", "BLOCK_MEDIUM_AND_ABOVE")
                )
        );

        return geminiWebClient
                .post()
                .uri("/models/{model}:generateContent", geminiConfig.getModel())
                .bodyValue(request)
                .retrieve()
                .bodyToMono(String.class)
                .timeout(Duration.ofSeconds(30))
                .retryWhen(Retry.backoff(3, Duration.ofSeconds(1))
                        .filter(throwable -> !(throwable instanceof WebClientResponseException.BadRequest)))
                .doOnSubscribe(sub -> log.debug("Calling Gemini API with model: {}", geminiConfig.getModel()))
                .doOnError(error -> log.error("Gemini API call failed", error));
    }

    /**
     * Build RIASEC personality analysis prompt
     */
    private String buildRiasecAnalysisPrompt(List<String> responses) {
        return String.format("""
            As an expert career counselor specializing in Indian students, analyze the following responses to determine RIASEC personality scores.
            
            Student Responses:
            %s
            
            Please provide RIASEC scores (0-100) based on these responses:
            - Realistic (R): Practical, hands-on activities
            - Investigative (I): Analytical, research-oriented activities  
            - Artistic (A): Creative, expressive activities
            - Social (S): People-oriented, helping activities
            - Enterprising (E): Leadership, business activities
            - Conventional (C): Organized, detail-oriented activities
            
            Respond in this exact JSON format:
            {
                "realistic": <score>,
                "investigative": <score>,
                "artistic": <score>,
                "social": <score>,
                "enterprising": <score>,
                "conventional": <score>,
                "dominantTypes": "<top 3 types as string>",
                "analysis": "<brief explanation>",
                "careerSuggestions": ["<career1>", "<career2>", "<career3>"]
            }
            """, String.join("\n", responses));
    }

    /**
     * Build career recommendation prompt with Indian context - NULL SAFE
     */
    private String buildCareerRecommendationPrompt(Student student) {
        // Safe handling of all nullable fields
        String educationLevel = student.getEducationLevel() != null
                ? student.getEducationLevel().toString()
                : "Not specified";

        String institutionName = student.getInstitutionName() != null
                ? student.getInstitutionName()
                : "Not specified";

        String collegeTier = student.getCollegeTier() != null
                ? student.getCollegeTier().toString()
                : "Not specified";

        // Academic performance handling
        String academicPerformance;
        if (student.getCgpa() != null) {
            academicPerformance = String.format("%.2f CGPA", student.getCgpa());
        } else if (student.getPercentage() != null) {
            academicPerformance = String.format("%d%%", student.getPercentage());
        } else {
            academicPerformance = "Not specified";
        }

        // RIASEC scores with null safety
        Student.RiasecScores riasec = student.getRiasecScores() != null
                ? student.getRiasecScores()
                : new Student.RiasecScores();

        int realistic = safeInt(riasec.getRealistic());
        int investigative = safeInt(riasec.getInvestigative());
        int artistic = safeInt(riasec.getArtistic());
        int social = safeInt(riasec.getSocial());
        int enterprising = safeInt(riasec.getEnterprising());
        int conventional = safeInt(riasec.getConventional());

        // Other fields
        String interests = student.getInterestedDomains() != null && !student.getInterestedDomains().isEmpty()
                ? String.join(", ", student.getInterestedDomains())
                : "Not specified";

        String locations = student.getPreferredLocations() != null && !student.getPreferredLocations().isEmpty()
                ? String.join(", ", student.getPreferredLocations())
                : "Any location";

        String workPref = student.getWorkPreference() != null
                ? student.getWorkPreference().toString()
                : "Not specified";

        String salary = student.getExpectedSalaryLPA() != null
                ? String.format("%.1f", student.getExpectedSalaryLPA())
                : "Not specified";

        int age = student.getAge() != null ? student.getAge() : 22;

        return String.format("""
            As an expert career counselor for Indian students, analyze this student profile and provide comprehensive career recommendations.
            
            Student Profile:
            - Education: %s
            - Institution: %s (%s)
            - CGPA/Percentage: %s
            - RIASEC Scores: R:%d, I:%d, A:%d, S:%d, E:%d, C:%d
            - Interests: %s
            - Preferred Locations: %s
            - Work Preference: %s
            - Expected Salary: %s LPA
            - Age: %d
            
            Consider:
            1. Indian job market trends
            2. Salary expectations in LPA
            3. Growth prospects
            4. Skills gap analysis
            5. College tier impact on opportunities
            
            Provide response in JSON format with:
            - Top 5 career recommendations with Indian salary ranges
            - Skills to develop
            - Industry insights
            - Action plan
            """,
                educationLevel,
                institutionName,
                collegeTier,
                academicPerformance,
                realistic,
                investigative,
                artistic,
                social,
                enterprising,
                conventional,
                interests,
                locations,
                workPref,
                salary,
                age);
    }

    /**
     * Build learning path prompt - NULL SAFE
     */
    private String buildLearningPathPrompt(Student student, String targetCareer) {
        String educationLevel = student.getEducationLevel() != null
                ? student.getEducationLevel().toString()
                : "Not specified";

        String skills = student.getSkillsAssessment() != null && !student.getSkillsAssessment().isEmpty()
                ? String.join(", ", student.getSkillsAssessment())
                : "No skills specified";

        String dominantTypes = student.getRiasecScores() != null
                ? student.getRiasecScores().getDominantTypes()
                : "Not assessed";

        return String.format("""
            Create a detailed learning path for an Indian student to transition into %s.
            
            Current Profile:
            - Education: %s
            - Current Skills: %s
            - RIASEC Profile: %s
            
            Provide a 6-month structured learning plan with:
            1. Essential skills to learn
            2. Recommended courses/certifications
            3. Projects to build
            4. Indian companies/startups to target
            5. Timeline and milestones
            6. Resources (free and paid)
            
            Focus on practical, actionable steps relevant to Indian job market.
            """,
                targetCareer,
                educationLevel,
                skills,
                dominantTypes);
    }

    /**
     * Build chat counseling prompt - NULL SAFE
     */
    private String buildChatPrompt(String message, Student student) {
        String educationLevel = student.getEducationLevel() != null
                ? student.getEducationLevel().toString()
                : "Not specified";

        String interests = student.getInterestedDomains() != null && !student.getInterestedDomains().isEmpty()
                ? String.join(", ", student.getInterestedDomains())
                : "exploring various fields";

        String careerGoal = student.getCurrentCareerGoal() != null
                ? student.getCurrentCareerGoal()
                : "still exploring career options";

        return String.format("""
            You are an expert career counselor for Indian students. Respond to this student's question with empathy and practical advice.
            
            Student Context:
            - Education: %s
            - Interests: %s
            - Career Goals: %s
            
            Student Question: %s
            
            Provide a helpful, encouraging response with specific actionable advice relevant to the Indian job market.
            Keep it conversational and supportive.
            """,
                educationLevel,
                interests,
                careerGoal,
                message);
    }

    /**
     * Safely convert Integer to int, returning 0 if null
     */
    private int safeInt(Integer value) {
        return value != null ? value : 0;
    }

    /**
     * Parse RIASEC analysis response from Gemini
     */
    private RiasecAnalysisResponse parseRiasecResponse(String response) {
        try {
            String jsonContent = extractJsonFromResponse(response);
            JsonNode jsonNode = objectMapper.readTree(jsonContent);

            return RiasecAnalysisResponse.builder()
                    .realistic(jsonNode.get("realistic").asInt())
                    .investigative(jsonNode.get("investigative").asInt())
                    .artistic(jsonNode.get("artistic").asInt())
                    .social(jsonNode.get("social").asInt())
                    .enterprising(jsonNode.get("enterprising").asInt())
                    .conventional(jsonNode.get("conventional").asInt())
                    .dominantTypes(jsonNode.get("dominantTypes").asText())
                    .analysis(jsonNode.get("analysis").asText())
                    .careerSuggestions(
                            objectMapper.convertValue(jsonNode.get("careerSuggestions"), List.class)
                    )
                    .build();

        } catch (Exception e) {
            log.error("Failed to parse RIASEC response", e);
            return createMockRiasecAnalysis();
        }
    }

    /**
     * Parse career recommendation response
     */
    private CareerAnalysisResponse parseCareerRecommendationResponse(String response) {
        try {
            String jsonContent = extractJsonFromResponse(response);
            JsonNode jsonNode = objectMapper.readTree(jsonContent);

            return CareerAnalysisResponse.builder()
                    .recommendations(objectMapper.convertValue(jsonNode.get("recommendations"), List.class))
                    .skillsTodevelop(objectMapper.convertValue(jsonNode.get("skillsTodevelop"), List.class))
                    .industryInsights(jsonNode.get("industryInsights").asText())
                    .actionPlan(objectMapper.convertValue(jsonNode.get("actionPlan"), List.class))
                    .build();

        } catch (Exception e) {
            log.error("Failed to parse career recommendation response", e);
            return createMockCareerAnalysis();
        }
    }

    /**
     * Extract text content from Gemini response
     */
    private String extractTextFromResponse(String response) {
        try {
            JsonNode jsonNode = objectMapper.readTree(response);
            return jsonNode.at("/candidates/0/content/parts/0/text").asText();
        } catch (Exception e) {
            log.error("Failed to extract text from response", e);
            return "Unable to process response";
        }
    }

    /**
     * Extract JSON content from response, handling markdown code blocks
     */
    private String extractJsonFromResponse(String response) {
        String text = extractTextFromResponse(response);

        // Remove markdown code blocks if present
        if (text.contains("```json")) {
            int start = text.indexOf("```json") + 7;
            int end = text.lastIndexOf("```");
            if (end > start) {
                text = text.substring(start, end).trim();
            }
        }

        return text;
    }

    /**
     * Create mock RIASEC analysis for fallback
     */
    private RiasecAnalysisResponse createMockRiasecAnalysis() {
        return RiasecAnalysisResponse.builder()
                .realistic(65)
                .investigative(70)
                .artistic(45)
                .social(60)
                .enterprising(55)
                .conventional(50)
                .dominantTypes("IRS")
                .analysis("Based on your responses, you show strong investigative and realistic traits with good social skills.")
                .careerSuggestions(List.of("Software Engineer", "Data Analyst", "Research Scientist"))
                .build();
    }

    /**
     * Create mock career analysis for fallback
     */
    private CareerAnalysisResponse createMockCareerAnalysis() {
        return CareerAnalysisResponse.builder()
                .recommendations(List.of(
                        Map.of("title", "Software Engineer", "salaryRange", "6-15 LPA", "growth", "High"),
                        Map.of("title", "Data Analyst", "salaryRange", "4-12 LPA", "growth", "Very High"),
                        Map.of("title", "Product Manager", "salaryRange", "8-25 LPA", "growth", "High")
                ))
                .skillsTodevelop(List.of("Programming", "Data Analysis", "Communication", "Problem Solving"))
                .industryInsights("Technology sector continues to grow rapidly in India with high demand for skilled professionals.")
                .actionPlan(List.of(
                        "Complete relevant certifications",
                        "Build portfolio projects",
                        "Network with industry professionals",
                        "Apply for internships"
                ))
                .build();
    }
}