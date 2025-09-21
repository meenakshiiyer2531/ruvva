package com.ruvaa.backend.controller;

import com.ruvaa.backend.model.dto.*;
import com.ruvaa.backend.model.entity.Student;
import com.ruvaa.backend.service.StudentService;
import com.ruvaa.backend.service.GeminiAIService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import jakarta.validation.Valid;
import java.util.concurrent.CompletableFuture;

/**
 * Student Controller for CareerConnect
 * 
 * Handles all student-related operations including registration, profile management,
 * career analysis, and RIASEC assessments.
 */
@Slf4j
@RestController
@RequestMapping("/students")
@RequiredArgsConstructor
@Validated
@Tag(name = "Student Management", description = "Student registration, profile management, and career analysis")
public class StudentController {

    private final StudentService studentService;
    private final GeminiAIService geminiAIService;

    /**
     * Register a new student
     */
    @PostMapping("/register")
    @Operation(
        summary = "Register a new student",
        description = "Create a new student account with basic profile information",
        responses = {
            @io.swagger.v3.oas.annotations.responses.ApiResponse(responseCode = "201", description = "Student registered successfully"),
            @io.swagger.v3.oas.annotations.responses.ApiResponse(responseCode = "400", description = "Invalid registration data"),
            @io.swagger.v3.oas.annotations.responses.ApiResponse(responseCode = "409", description = "Student already exists")
        }
    )
    public CompletableFuture<ResponseEntity<ApiResponse<Student>>> registerStudent(
            @Valid @RequestBody StudentRegistrationRequest request) {
        
        log.info("Student registration request for email: {}", request.getEmail());
        
        return studentService.registerStudent(request)
            .thenApply(student -> {
                // Remove sensitive information
                student.setPassword(null);
                
                ApiResponse<Student> response = ApiResponse.<Student>builder()
                    .success(true)
                    .message("Student registered successfully")
                    .data(student)
                    .build();
                
                return ResponseEntity.status(HttpStatus.CREATED).body(response);
            })
            .exceptionally(throwable -> {
                log.error("Student registration failed", throwable);
                
                ApiResponse<Student> response = ApiResponse.<Student>builder()
                    .success(false)
                    .message("Registration failed: " + throwable.getMessage())
                    .build();
                
                return ResponseEntity.badRequest().body(response);
            });
    }

    /**
     * Get student profile
     */
    @GetMapping("/{studentId}/profile")
    @SecurityRequirement(name = "bearerAuth")
    @Operation(
        summary = "Get student profile",
        description = "Retrieve complete student profile information",
        responses = {
            @io.swagger.v3.oas.annotations.responses.ApiResponse(responseCode = "200", description = "Profile retrieved successfully"),
            @io.swagger.v3.oas.annotations.responses.ApiResponse(responseCode = "404", description = "Student not found"),
            @io.swagger.v3.oas.annotations.responses.ApiResponse(responseCode = "403", description = "Access denied")
        }
    )
    public CompletableFuture<ResponseEntity<ApiResponse<Student>>> getProfile(
            @Parameter(description = "Student ID") @PathVariable String studentId) {
        
        log.debug("Profile request for student: {}", studentId);
        
        return studentService.findById(studentId)
            .thenApply(student -> {
                // Remove sensitive information
                student.setPassword(null);
                
                ApiResponse<Student> response = ApiResponse.<Student>builder()
                    .success(true)
                    .message("Profile retrieved successfully")
                    .data(student)
                    .build();
                
                return ResponseEntity.ok(response);
            })
            .exceptionally(throwable -> {
                log.error("Failed to retrieve profile for student: {}", studentId, throwable);
                
                ApiResponse<Student> response = ApiResponse.<Student>builder()
                    .success(false)
                    .message("Failed to retrieve profile: " + throwable.getMessage())
                    .build();
                
                return ResponseEntity.notFound().build();
            });
    }

    /**
     * Update student profile
     */
    @PutMapping("/{studentId}/profile")
    @SecurityRequirement(name = "bearerAuth")
    @Operation(
        summary = "Update student profile",
        description = "Update student profile information",
        responses = {
            @io.swagger.v3.oas.annotations.responses.ApiResponse(responseCode = "200", description = "Profile updated successfully"),
            @io.swagger.v3.oas.annotations.responses.ApiResponse(responseCode = "400", description = "Invalid update data"),
            @io.swagger.v3.oas.annotations.responses.ApiResponse(responseCode = "404", description = "Student not found")
        }
    )
    public CompletableFuture<ResponseEntity<ApiResponse<Student>>> updateProfile(
            @Parameter(description = "Student ID") @PathVariable String studentId,
            @Valid @RequestBody StudentProfileUpdateRequest request) {
        
        log.info("Profile update request for student: {}", studentId);
        
        return studentService.updateProfile(studentId, request)
            .thenApply(student -> {
                // Remove sensitive information
                student.setPassword(null);
                
                ApiResponse<Student> response = ApiResponse.<Student>builder()
                    .success(true)
                    .message("Profile updated successfully")
                    .data(student)
                    .build();
                
                return ResponseEntity.ok(response);
            })
            .exceptionally(throwable -> {
                log.error("Failed to update profile for student: {}", studentId, throwable);
                
                ApiResponse<Student> response = ApiResponse.<Student>builder()
                    .success(false)
                    .message("Failed to update profile: " + throwable.getMessage())
                    .build();
                
                return ResponseEntity.badRequest().body(response);
            });
    }

    /**
     * Submit RIASEC assessment and get personality analysis
     */
    @PostMapping("/{studentId}/riasec-analysis")
    @SecurityRequirement(name = "bearerAuth")
    @Operation(
        summary = "Submit RIASEC assessment",
        description = "Submit assessment responses and get RIASEC personality analysis using AI",
        responses = {
            @io.swagger.v3.oas.annotations.responses.ApiResponse(responseCode = "200", description = "Analysis completed successfully"),
            @io.swagger.v3.oas.annotations.responses.ApiResponse(responseCode = "400", description = "Invalid assessment data"),
            @io.swagger.v3.oas.annotations.responses.ApiResponse(responseCode = "404", description = "Student not found")
        }
    )
    public CompletableFuture<ResponseEntity<ApiResponse<RiasecAnalysisResponse>>> submitRiasecAssessment(
            @Parameter(description = "Student ID") @PathVariable String studentId,
            @Valid @RequestBody CareerAnalysisRequest request) {
        
        log.info("RIASEC assessment submission for student: {}", studentId);
        
        return geminiAIService.analyzeRiasecPersonality(request.getAssessmentResponses())
            .thenCompose(riasecAnalysis -> {
                // Update student's RIASEC scores
                Student.RiasecScores riasecScores = Student.RiasecScores.builder()
                    .realistic(riasecAnalysis.getRealistic())
                    .investigative(riasecAnalysis.getInvestigative())
                    .artistic(riasecAnalysis.getArtistic())
                    .social(riasecAnalysis.getSocial())
                    .enterprising(riasecAnalysis.getEnterprising())
                    .conventional(riasecAnalysis.getConventional())
                    .build();
                
                return studentService.updateRiasecScores(studentId, riasecScores)
                    .thenApply(student -> riasecAnalysis);
            })
            .thenApply(riasecAnalysis -> {
                ApiResponse<RiasecAnalysisResponse> response = ApiResponse.<RiasecAnalysisResponse>builder()
                    .success(true)
                    .message("RIASEC analysis completed successfully")
                    .data(riasecAnalysis)
                    .build();
                
                return ResponseEntity.ok(response);
            })
            .exceptionally(throwable -> {
                log.error("RIASEC analysis failed for student: {}", studentId, throwable);
                
                ApiResponse<RiasecAnalysisResponse> response = ApiResponse.<RiasecAnalysisResponse>builder()
                    .success(false)
                    .message("Analysis failed: " + throwable.getMessage())
                    .build();
                
                return ResponseEntity.badRequest().body(response);
            });
    }

    /**
     * Get comprehensive career recommendations
     */
    @PostMapping("/{studentId}/career-recommendations")
    @SecurityRequirement(name = "bearerAuth")
    @Operation(
        summary = "Get career recommendations",
        description = "Generate AI-powered career recommendations based on student profile and RIASEC scores",
        responses = {
            @io.swagger.v3.oas.annotations.responses.ApiResponse(responseCode = "200", description = "Recommendations generated successfully"),
            @io.swagger.v3.oas.annotations.responses.ApiResponse(responseCode = "400", description = "Invalid request"),
            @io.swagger.v3.oas.annotations.responses.ApiResponse(responseCode = "404", description = "Student not found")
        }
    )
    public CompletableFuture<ResponseEntity<ApiResponse<CareerAnalysisResponse>>> getCareerRecommendations(
            @Parameter(description = "Student ID") @PathVariable String studentId) {
        
        log.info("Career recommendations request for student: {}", studentId);
        
        return studentService.findById(studentId)
            .thenCompose(student -> geminiAIService.generateCareerRecommendations(student))
            .thenApply(careerAnalysis -> {
                ApiResponse<CareerAnalysisResponse> response = ApiResponse.<CareerAnalysisResponse>builder()
                    .success(true)
                    .message("Career recommendations generated successfully")
                    .data(careerAnalysis)
                    .build();
                
                return ResponseEntity.ok(response);
            })
            .exceptionally(throwable -> {
                log.error("Career recommendations failed for student: {}", studentId, throwable);
                
                ApiResponse<CareerAnalysisResponse> response = ApiResponse.<CareerAnalysisResponse>builder()
                    .success(false)
                    .message("Failed to generate recommendations: " + throwable.getMessage())
                    .build();
                
                return ResponseEntity.badRequest().body(response);
            });
    }

    /**
     * Generate personalized learning path
     */
    @PostMapping("/{studentId}/learning-path")
    @SecurityRequirement(name = "bearerAuth")
    @Operation(
        summary = "Generate learning path",
        description = "Create a personalized learning path for a specific career goal",
        responses = {
            @io.swagger.v3.oas.annotations.responses.ApiResponse(responseCode = "200", description = "Learning path generated successfully"),
            @io.swagger.v3.oas.annotations.responses.ApiResponse(responseCode = "400", description = "Invalid request"),
            @io.swagger.v3.oas.annotations.responses.ApiResponse(responseCode = "404", description = "Student not found")
        }
    )
    public CompletableFuture<ResponseEntity<ApiResponse<String>>> generateLearningPath(
            @Parameter(description = "Student ID") @PathVariable String studentId,
            @Parameter(description = "Target career") @RequestParam String targetCareer) {
        
        log.info("Learning path request for student: {} targeting: {}", studentId, targetCareer);
        
        return studentService.findById(studentId)
            .thenCompose(student -> geminiAIService.generateLearningPath(student, targetCareer))
            .thenApply(learningPath -> {
                ApiResponse<String> response = ApiResponse.<String>builder()
                    .success(true)
                    .message("Learning path generated successfully")
                    .data(learningPath)
                    .build();
                
                return ResponseEntity.ok(response);
            })
            .exceptionally(throwable -> {
                log.error("Learning path generation failed for student: {}", studentId, throwable);
                
                ApiResponse<String> response = ApiResponse.<String>builder()
                    .success(false)
                    .message("Failed to generate learning path: " + throwable.getMessage())
                    .build();
                
                return ResponseEntity.badRequest().body(response);
            });
    }

    /**
     * Bookmark a career
     */
    @PostMapping("/{studentId}/bookmarks")
    @SecurityRequirement(name = "bearerAuth")
    @Operation(
        summary = "Bookmark a career",
        description = "Add a career to student's bookmarks",
        responses = {
            @io.swagger.v3.oas.annotations.responses.ApiResponse(responseCode = "200", description = "Career bookmarked successfully"),
            @io.swagger.v3.oas.annotations.responses.ApiResponse(responseCode = "404", description = "Student not found")
        }
    )
    public CompletableFuture<ResponseEntity<ApiResponse<Void>>> bookmarkCareer(
            @Parameter(description = "Student ID") @PathVariable String studentId,
            @Parameter(description = "Career to bookmark") @RequestParam String career) {
        
        log.info("Bookmark request for student: {} career: {}", studentId, career);
        
        return studentService.bookmarkCareer(studentId, career)
            .thenApply(result -> {
                ApiResponse<Void> response = ApiResponse.<Void>builder()
                    .success(true)
                    .message("Career bookmarked successfully")
                    .build();
                
                return ResponseEntity.ok(response);
            })
            .exceptionally(throwable -> {
                log.error("Bookmark failed for student: {}", studentId, throwable);
                
                ApiResponse<Void> response = ApiResponse.<Void>builder()
                    .success(false)
                    .message("Failed to bookmark career: " + throwable.getMessage())
                    .build();
                
                return ResponseEntity.badRequest().body(response);
            });
    }

    /**
     * Verify student email
     */
    @PostMapping("/{studentId}/verify-email")
    @Operation(
        summary = "Verify student email",
        description = "Verify student's email address",
        responses = {
            @io.swagger.v3.oas.annotations.responses.ApiResponse(responseCode = "200", description = "Email verified successfully"),
            @io.swagger.v3.oas.annotations.responses.ApiResponse(responseCode = "404", description = "Student not found")
        }
    )
    public CompletableFuture<ResponseEntity<ApiResponse<Void>>> verifyEmail(
            @Parameter(description = "Student ID") @PathVariable String studentId) {
        
        log.info("Email verification for student: {}", studentId);
        
        return studentService.verifyEmail(studentId)
            .thenApply(result -> {
                ApiResponse<Void> response = ApiResponse.<Void>builder()
                    .success(true)
                    .message("Email verified successfully")
                    .build();
                
                return ResponseEntity.ok(response);
            })
            .exceptionally(throwable -> {
                log.error("Email verification failed for student: {}", studentId, throwable);
                
                ApiResponse<Void> response = ApiResponse.<Void>builder()
                    .success(false)
                    .message("Email verification failed: " + throwable.getMessage())
                    .build();
                
                return ResponseEntity.badRequest().body(response);
            });
    }

    /**
     * Complete onboarding
     */
    @PostMapping("/{studentId}/complete-onboarding")
    @SecurityRequirement(name = "bearerAuth")
    @Operation(
        summary = "Complete onboarding",
        description = "Mark student onboarding as completed",
        responses = {
            @io.swagger.v3.oas.annotations.responses.ApiResponse(responseCode = "200", description = "Onboarding completed successfully"),
            @io.swagger.v3.oas.annotations.responses.ApiResponse(responseCode = "404", description = "Student not found")
        }
    )
    public CompletableFuture<ResponseEntity<ApiResponse<Void>>> completeOnboarding(
            @Parameter(description = "Student ID") @PathVariable String studentId) {
        
        log.info("Onboarding completion for student: {}", studentId);
        
        return studentService.completeOnboarding(studentId)
            .thenApply(result -> {
                ApiResponse<Void> response = ApiResponse.<Void>builder()
                    .success(true)
                    .message("Onboarding completed successfully")
                    .build();
                
                return ResponseEntity.ok(response);
            })
            .exceptionally(throwable -> {
                log.error("Onboarding completion failed for student: {}", studentId, throwable);
                
                ApiResponse<Void> response = ApiResponse.<Void>builder()
                    .success(false)
                    .message("Onboarding completion failed: " + throwable.getMessage())
                    .build();
                
                return ResponseEntity.badRequest().body(response);
            });
    }
}