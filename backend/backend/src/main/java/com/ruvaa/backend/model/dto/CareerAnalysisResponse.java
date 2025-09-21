package com.ruvaa.backend.model.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;
import java.util.Map;

/**
 * Response DTO for comprehensive career analysis
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CareerAnalysisResponse {
    
    private List<Map<String, Object>> recommendations;
    private List<String> skillsTodevelop;
    private String industryInsights;
    private List<String> actionPlan;
    private String analysisDate;
    private Integer confidenceScore;
    
    /**
     * Get top career recommendation
     */
    public String getTopRecommendation() {
        if (recommendations == null || recommendations.isEmpty()) {
            return "No recommendations available";
        }
        
        Map<String, Object> topRec = recommendations.get(0);
        return (String) topRec.get("title");
    }
    
    /**
     * Get salary range for top recommendation
     */
    public String getTopSalaryRange() {
        if (recommendations == null || recommendations.isEmpty()) {
            return "Not available";
        }
        
        Map<String, Object> topRec = recommendations.get(0);
        return (String) topRec.get("salaryRange");
    }
    
    /**
     * Get growth potential for top recommendation
     */
    public String getTopGrowthPotential() {
        if (recommendations == null || recommendations.isEmpty()) {
            return "Not available";
        }
        
        Map<String, Object> topRec = recommendations.get(0);
        return (String) topRec.get("growth");
    }
}