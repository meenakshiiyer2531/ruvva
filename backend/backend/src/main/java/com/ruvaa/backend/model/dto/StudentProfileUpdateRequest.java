package com.ruvaa.backend.model.dto;

import com.ruvaa.backend.model.enums.CollegeTier;
import com.ruvaa.backend.model.enums.EducationLevel;
import com.ruvaa.backend.model.enums.WorkPreference;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import jakarta.validation.constraints.*;
import java.util.List;

/**
 * Request DTO for student profile updates
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class StudentProfileUpdateRequest {
    
    @Size(min = 2, max = 100, message = "Name must be between 2 and 100 characters")
    private String fullName;
    
    @Pattern(regexp = "^[6-9]\\d{9}$", message = "Invalid Indian mobile number")
    private String phoneNumber;
    
    @Min(value = 13, message = "Age must be at least 13")
    @Max(value = 35, message = "Age must be at most 35")
    private Integer age;
    
    private String city;
    private String state;
    
    private EducationLevel educationLevel;
    private String institutionName;
    private CollegeTier collegeTier;
    private String stream;
    
    @DecimalMin(value = "0.0", message = "CGPA must be non-negative")
    @DecimalMax(value = "10.0", message = "CGPA must be at most 10.0")
    private Double cgpa;
    
    @Min(value = 0)
    @Max(value = 100)
    private Integer percentage;
    
    private Integer graduationYear;
    
    private List<String> interestedDomains;
    private List<String> skillsAssessment;
    private List<String> preferredLocations;
    
    private WorkPreference workPreference;
    
    @Min(value = 0, message = "Expected salary must be non-negative")
    private Double expectedSalaryLPA;
    
    private String currentCareerGoal;
    
    private List<String> learningStyle;
    private List<String> preferredLanguages;
}