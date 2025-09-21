package com.ruvaa.backend.model.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.Size;
import java.util.List;

/**
 * Request DTO for career analysis
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CareerAnalysisRequest {
    
    @NotBlank(message = "Student ID is required")
    private String studentId;
    
    @NotEmpty(message = "Assessment responses are required")
    @Size(min = 3, message = "At least 3 responses are required")
    private List<String> assessmentResponses;
    
    private List<String> additionalInterests;
    private String specificCareerInquiry;
    private boolean includeSkillsGap;
    private boolean includeLearningPath;
}