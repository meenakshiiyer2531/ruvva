package com.ruvaa.backend.model.entity;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.google.cloud.Timestamp;
import com.ruvaa.backend.model.enums.EducationLevel;
import com.ruvaa.backend.model.enums.CollegeTier;
import com.ruvaa.backend.model.enums.WorkPreference;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

import jakarta.validation.constraints.*;

import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.Collection;
import java.util.Date;
import java.util.List;
import java.util.Map;

/**
 * Student Entity for CareerConnect
 * 
 * Represents a student user with comprehensive profile information
 * including RIASEC personality scores, academic background, and preferences
 * specifically tailored for the Indian education and job market.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Student implements UserDetails {

    // Basic Information
    private String id; // Firebase document ID
    
    @NotBlank(message = "Email is required")
    @Email(message = "Invalid email format")
    private String email;
    
    @JsonIgnore
    @NotBlank(message = "Password is required")
    @Size(min = 8, message = "Password must be at least 8 characters")
    private String password;
    
    @NotBlank(message = "Full name is required")
    @Size(min = 2, max = 100, message = "Name must be between 2 and 100 characters")
    private String fullName;
    
    @Pattern(regexp = "^[6-9]\\d{9}$", message = "Invalid Indian mobile number")
    private String phoneNumber;
    
    @Min(value = 13, message = "Age must be at least 13")
    @Max(value = 35, message = "Age must be at most 35")
    private Integer age;
    
    @NotBlank(message = "City is required")
    private String city;
    
    @NotBlank(message = "State is required")
    private String state;
    
    // Academic Information
    @NotNull(message = "Education level is required")
    private EducationLevel educationLevel;
    
    private String institutionName;
    
    private CollegeTier collegeTier;
    
    @Pattern(regexp = "^[A-Za-z\\s,]+$", message = "Invalid stream format")
    private String stream; // Science, Commerce, Arts, Engineering, etc.
    
    @DecimalMin(value = "0.0", message = "CGPA must be non-negative")
    @DecimalMax(value = "10.0", message = "CGPA must be at most 10.0")
    private Double cgpa;
    
    @Min(value = 0)
    @Max(value = 100)
    private Integer percentage;
    
    private Integer graduationYear;
    
    // RIASEC Personality Scores (0-100)
    @Builder.Default
    private RiasecScores riasecScores = new RiasecScores();
    
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class RiasecScores {
        @Min(0) @Max(100)
        private Integer realistic = 0;
        
        @Min(0) @Max(100)
        private Integer investigative = 0;
        
        @Min(0) @Max(100)
        private Integer artistic = 0;
        
        @Min(0) @Max(100)
        private Integer social = 0;
        
        @Min(0) @Max(100)
        private Integer enterprising = 0;
        
        @Min(0) @Max(100)
        private Integer conventional = 0;
        
        public String getDominantTypes() {
            Map<String, Integer> scores = Map.of(
                "R", realistic, "I", investigative, "A", artistic,
                "S", social, "E", enterprising, "C", conventional
            );
            
            return scores.entrySet().stream()
                .sorted(Map.Entry.<String, Integer>comparingByValue().reversed())
                .limit(3)
                .map(Map.Entry::getKey)
                .reduce("", String::concat);
        }
    }
    
    // Career Preferences
    @Builder.Default
    private List<String> interestedDomains = List.of();
    
    @Builder.Default
    private List<String> skillsAssessment = List.of();
    
    @Builder.Default
    private List<String> preferredLocations = List.of();
    
    private WorkPreference workPreference;
    
    @Min(value = 0, message = "Expected salary must be non-negative")
    private Double expectedSalaryLPA; // In Lakhs Per Annum
    
    // Learning Preferences
    @Builder.Default
    private List<String> learningStyle = List.of(); // Visual, Auditory, Kinesthetic, etc.
    
    @Builder.Default
    private List<String> preferredLanguages = List.of("English", "Hindi");
    
    // Assessment History
    @Builder.Default
    private List<String> completedAssessments = List.of();
    
    private com.google.cloud.Timestamp lastAssessmentDate;
    
    private Integer totalAssessmentScore;
    
    // Career Journey
    @Builder.Default
    private List<String> recommendedCareers = List.of();
    
    @Builder.Default
    private List<String> bookmarkedCareers = List.of();
    
    private String currentCareerGoal;
    
    // Mentorship
    @Builder.Default
    private List<String> mentorInteractions = List.of();
    
    private String assignedMentorId;
    
    // System Fields
    private boolean emailVerified = false;
    
    private boolean profileCompleted = false;
    
    private boolean onboardingCompleted = false;
    
    private com.google.cloud.Timestamp createdAt;
    
    private com.google.cloud.Timestamp updatedAt;
    
    private com.google.cloud.Timestamp lastLoginAt;
    
    @Builder.Default
    private boolean active = true;

    // Additional Metadata
    @Builder.Default
    private Map<String, Object> metadata = Map.of();

    // Spring Security UserDetails Implementation
    @Override
    @JsonIgnore
    public Collection<? extends GrantedAuthority> getAuthorities() {
        return List.of(() -> "ROLE_STUDENT");
    }

    @Override
    @JsonIgnore
    public String getUsername() {
        return email;
    }

    @Override
    @JsonIgnore
    public boolean isAccountNonExpired() {
        return active;
    }

    @Override
    @JsonIgnore
    public boolean isAccountNonLocked() {
        return active;
    }

    @Override
    @JsonIgnore
    public boolean isCredentialsNonExpired() {
        return true;
    }

    @Override
    @JsonIgnore
    public boolean isEnabled() {
        return active && emailVerified;
    }

    // Utility Methods
    
    /**
     * Calculate profile completion percentage
     */
    public int getProfileCompletionPercentage() {
        int totalFields = 15;
        int completedFields = 0;
        
        if (fullName != null && !fullName.isBlank()) completedFields++;
        if (phoneNumber != null && !phoneNumber.isBlank()) completedFields++;
        if (age != null) completedFields++;
        if (city != null && !city.isBlank()) completedFields++;
        if (state != null && !state.isBlank()) completedFields++;
        if (educationLevel != null) completedFields++;
        if (institutionName != null && !institutionName.isBlank()) completedFields++;
        if (stream != null && !stream.isBlank()) completedFields++;
        if (cgpa != null || percentage != null) completedFields++;
        if (!interestedDomains.isEmpty()) completedFields++;
        if (!skillsAssessment.isEmpty()) completedFields++;
        if (!preferredLocations.isEmpty()) completedFields++;
        if (workPreference != null) completedFields++;
        if (expectedSalaryLPA != null) completedFields++;
        if (riasecScores.getDominantTypes().length() > 0) completedFields++;
        
        return (completedFields * 100) / totalFields;
    }

    /**
     * Check if student needs career assessment
     */
    public boolean needsCareerAssessment() {
        if (lastAssessmentDate == null) {
            return true;
        }

        // Calculate 6 months ago
        Instant sixMonthsAgo = Instant.now().minus(6, ChronoUnit.MONTHS);
        Timestamp sixMonthsAgoTimestamp = Timestamp.of(Date.from(sixMonthsAgo));

        return lastAssessmentDate.compareTo(sixMonthsAgoTimestamp) < 0 ||
                riasecScores.getDominantTypes().length() < 3;
    }

    /**
     * Get display name for UI
     */
    public String getDisplayName() {
        return fullName != null && !fullName.isBlank() ? fullName : email;
    }
}