package com.ruvaa.backend.controller;

import com.ruvaa.backend.dto.AssessmentRequest;
import com.ruvaa.backend.entity.Assessment;
import com.ruvaa.backend.entity.User;
import com.ruvaa.backend.repository.AssessmentRepository;
import com.ruvaa.backend.repository.UserRepository;
import com.ruvaa.backend.service.AIService;
import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/assessments")
@RequiredArgsConstructor
@CrossOrigin(origins = "*")
public class AssessmentController {

    private final AssessmentRepository assessmentRepository;
    private final UserRepository userRepository;
    private final AIService aiService;
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
            User user = userRepository.findByUsername(authentication.getName())
                    .orElseThrow(() -> new RuntimeException("User not found"));

            int totalScore = request.getAnswers().stream()
                    .mapToInt(AssessmentRequest.AnswerDto::getPoints)
                    .sum();
            
            int maxScore = 12; // 5 questions with max 3 points each (approximation)
            
            String recommendations = aiService.generateAssessmentRecommendations(totalScore, maxScore);
            
            Assessment assessment = new Assessment();
            assessment.setUser(user);
            assessment.setTotalScore(totalScore);
            assessment.setMaxScore(maxScore);
            assessment.setAnswers(objectMapper.writeValueAsString(request.getAnswers()));
            assessment.setRecommendations(recommendations);
            
            assessmentRepository.save(assessment);
            
            return ResponseEntity.ok(Map.of(
                "score", totalScore,
                "maxScore", maxScore,
                "recommendations", recommendations
            ));
        } catch (Exception e) {
            return ResponseEntity.badRequest().build();
        }
    }

    @GetMapping("/results")
    public ResponseEntity<List<Assessment>> getResults(Authentication authentication) {
        try {
            User user = userRepository.findByUsername(authentication.getName())
                    .orElseThrow(() -> new RuntimeException("User not found"));

            List<Assessment> assessments = assessmentRepository.findByUserOrderByCreatedAtDesc(user);
            return ResponseEntity.ok(assessments);
        } catch (Exception e) {
            return ResponseEntity.badRequest().build();
        }
    }
}