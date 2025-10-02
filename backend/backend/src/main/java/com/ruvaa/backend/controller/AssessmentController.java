package com.ruvaa.backend.controller;

import com.ruvaa.backend.dto.AssessmentRequest;
import com.ruvaa.backend.entity.Assessment;
import com.ruvaa.backend.entity.User;
import com.ruvaa.backend.repository.AssessmentRepository;
import com.ruvaa.backend.repository.UserRepository;
import com.ruvaa.backend.service.AIService;
import com.ruvaa.backend.service.FirebaseUserService;
import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;

import java.util.List;
import java.util.Map;

@Slf4j
@RestController
@RequestMapping("/assessments")
@RequiredArgsConstructor
@CrossOrigin(origins = "*")
@ConditionalOnProperty(name = "firebase.enabled", havingValue = "true", matchIfMissing = false)
public class AssessmentController {

    private final AssessmentRepository assessmentRepository;
    private final UserRepository userRepository;
    private final AIService aiService;
    private final FirebaseUserService firebaseUserService;
    private final ObjectMapper objectMapper;

    @GetMapping("/questions")
    public ResponseEntity<List<Map<String, Object>>> getQuestions() {
        List<Map<String, Object>> questions = List.of(
            Map.of(
                "text", "Do you enjoy solving logical problems?",
                "options", List.of(
                    Map.of("text", "Yes", "points", 2),
                    Map.of("text", "No", "points", 0)
                )
            ),
            Map.of(
                "text", "Do you like creative arts?",
                "options", List.of(
                    Map.of("text", "Yes", "points", 2),
                    Map.of("text", "No", "points", 0)
                )
            ),
            Map.of(
                "text", "Do you enjoy working in teams?",
                "options", List.of(
                    Map.of("text", "Yes", "points", 2),
                    Map.of("text", "No", "points", 0)
                )
            ),
            Map.of(
                "text", "Are you interested in technology and computers?",
                "options", List.of(
                    Map.of("text", "Very interested", "points", 3),
                    Map.of("text", "Somewhat interested", "points", 2),
                    Map.of("text", "Not interested", "points", 0)
                )
            ),
            Map.of(
                "text", "Do you prefer working with data and numbers?",
                "options", List.of(
                    Map.of("text", "Yes", "points", 2),
                    Map.of("text", "No", "points", 0)
                )
            )
        );
        
        return ResponseEntity.ok(questions);
    }

    @PostMapping("/submit")
    public ResponseEntity<Map<String, Object>> submitAssessment(@Valid @RequestBody AssessmentRequest request,
                                                              Authentication authentication) {
        try {
            String username = authentication.getName();

            int totalScore = request.getAnswers().stream()
                    .mapToInt(AssessmentRequest.AnswerDto::getPoints)
                    .sum();

            int maxScore = 12; // 5 questions with max 3 points each (approximation)

            String recommendations = aiService.generateAssessmentRecommendations(totalScore, maxScore);

            // Prepare assessment data for Firebase
            Map<String, Object> assessmentData = new HashMap<>();
            assessmentData.put("totalScore", totalScore);
            assessmentData.put("maxScore", maxScore);
            assessmentData.put("answers", request.getAnswers());
            assessmentData.put("recommendations", recommendations);
            assessmentData.put("percentage", (double) totalScore / maxScore * 100);

            // Save to Firebase
            try {
                firebaseUserService.saveAssessmentResults(username, assessmentData);
                log.info("Assessment results saved to Firebase for user: {}", username);
            } catch (Exception e) {
                log.warn("Failed to save assessment to Firebase: {}", e.getMessage());
            }

            // Save to local DB as backup
            try {
                User user = userRepository.findByUsername(username)
                        .orElseThrow(() -> new RuntimeException("User not found"));

                Assessment assessment = new Assessment();
                assessment.setUser(user);
                assessment.setTotalScore(totalScore);
                assessment.setMaxScore(maxScore);
                assessment.setAnswers(objectMapper.writeValueAsString(request.getAnswers()));
                assessment.setRecommendations(recommendations);

                assessmentRepository.save(assessment);
                log.debug("Assessment saved to local DB for user: {}", username);
            } catch (Exception e) {
                log.warn("Failed to save assessment to local DB: {}", e.getMessage());
            }

            return ResponseEntity.ok(Map.of(
                "score", totalScore,
                "maxScore", maxScore,
                "recommendations", recommendations,
                "percentage", (double) totalScore / maxScore * 100
            ));
        } catch (Exception e) {
            log.error("Assessment submission failed: {}", e.getMessage());
            return ResponseEntity.badRequest().build();
        }
    }

    @GetMapping("/results")
    public ResponseEntity<Map<String, Object>> getResults(Authentication authentication) {
        try {
            String username = authentication.getName();

            // Try to get from Firebase first
            Map<String, Object> latestResults = null;
            try {
                if (firebaseUserService.isFirestoreHealthy()) {
                    latestResults = firebaseUserService.getLatestAssessmentResults(username);
                    if (!latestResults.isEmpty()) {
                        log.debug("Retrieved assessment results from Firebase for user: {}", username);
                        return ResponseEntity.ok(latestResults);
                    }
                }
            } catch (Exception e) {
                log.warn("Failed to get assessment results from Firebase: {}", e.getMessage());
            }

            // Fallback to local database
            try {
                User user = userRepository.findByUsername(username)
                        .orElseThrow(() -> new RuntimeException("User not found"));

                List<Assessment> assessments = assessmentRepository.findByUserOrderByCreatedAtDesc(user);
                if (!assessments.isEmpty()) {
                    Assessment latest = assessments.get(0);
                    Map<String, Object> result = Map.of(
                        "totalScore", latest.getTotalScore(),
                        "maxScore", latest.getMaxScore(),
                        "recommendations", latest.getRecommendations(),
                        "percentage", (double) latest.getTotalScore() / latest.getMaxScore() * 100,
                        "createdAt", latest.getCreatedAt()
                    );
                    log.debug("Retrieved assessment results from local DB for user: {}", username);
                    return ResponseEntity.ok(result);
                }
            } catch (Exception e) {
                log.error("Failed to get assessment results from local DB: {}", e.getMessage());
            }

            // Return empty result if no assessments found
            return ResponseEntity.ok(Map.of("message", "No assessment results found"));

        } catch (Exception e) {
            log.error("Get assessment results failed: {}", e.getMessage());
            return ResponseEntity.badRequest().build();
        }
    }

    @GetMapping("/health")
    public ResponseEntity<Map<String, Object>> healthCheck() {
        Map<String, Object> health = new HashMap<>();
        health.put("status", "UP");
        health.put("firebase_db", firebaseUserService.isFirestoreHealthy());
        health.put("ai_service", aiService.isPythonAIServiceAvailable());
        return ResponseEntity.ok(health);
    }
}