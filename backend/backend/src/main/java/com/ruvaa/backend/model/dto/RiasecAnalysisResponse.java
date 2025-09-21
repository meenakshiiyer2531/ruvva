package com.ruvaa.backend.model.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

/**
 * Response DTO for RIASEC personality analysis
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class RiasecAnalysisResponse {
    
    private Integer realistic;
    private Integer investigative;
    private Integer artistic;
    private Integer social;
    private Integer enterprising;
    private Integer conventional;
    
    private String dominantTypes;
    private String analysis;
    private List<String> careerSuggestions;
    
    /**
     * Get the personality type description
     */
    public String getPersonalityDescription() {
        if (dominantTypes == null || dominantTypes.length() < 3) {
            return "Balanced personality with diverse interests";
        }
        
        return switch (dominantTypes.substring(0, 3)) {
            case "RIA" -> "Practical and creative problem solver";
            case "RIC" -> "Systematic and analytical thinker";
            case "IRE" -> "Research-oriented entrepreneur";
            case "IRA" -> "Creative researcher and innovator";
            case "ARS" -> "Creative helper and communicator";
            case "ASE" -> "Social entrepreneur and leader";
            case "SER" -> "People-focused leader";
            case "SEC" -> "Organized people manager";
            case "ERC" -> "Business-minded organizer";
            case "ERS" -> "Enterprising people person";
            default -> "Unique combination of interests and skills";
        };
    }
    
    /**
     * Get career fields based on dominant types
     */
    public List<String> getRecommendedFields() {
        if (dominantTypes == null || dominantTypes.length() < 2) {
            return List.of("Technology", "Business", "Healthcare");
        }
        
        char first = dominantTypes.charAt(0);
        char second = dominantTypes.charAt(1);
        
        return switch ("" + first + second) {
            case "RI" -> List.of("Engineering", "Computer Science", "Research & Development");
            case "RA" -> List.of("Architecture", "Industrial Design", "Creative Engineering");
            case "RS" -> List.of("Healthcare", "Social Work", "Education");
            case "RE" -> List.of("Business Operations", "Project Management", "Entrepreneurship");
            case "RC" -> List.of("Quality Control", "Technical Writing", "Systems Analysis");
            case "IR" -> List.of("Scientific Research", "Data Science", "Technology Innovation");
            case "IA" -> List.of("UX Research", "Creative Technology", "Design Thinking");
            case "IS" -> List.of("Psychology", "Social Research", "Educational Technology");
            case "IE" -> List.of("Business Analysis", "Consulting", "Strategic Planning");
            case "IC" -> List.of("Data Analysis", "Research Management", "Technical Documentation");
            case "AR" -> List.of("Product Design", "Media Technology", "Creative Engineering");
            case "AI" -> List.of("Creative Research", "Innovation Design", "Digital Arts");
            case "AS" -> List.of("Art Therapy", "Creative Education", "Community Arts");
            case "AE" -> List.of("Creative Direction", "Arts Management", "Entertainment Business");
            case "AC" -> List.of("Graphic Design", "Content Creation", "Digital Media");
            case "SR" -> List.of("Healthcare", "Community Development", "Environmental Science");
            case "SI" -> List.of("Social Research", "Educational Psychology", "Human Services");
            case "SA" -> List.of("Art Therapy", "Creative Education", "Cultural Programs");
            case "SE" -> List.of("Sales", "Human Resources", "Public Relations");
            case "SC" -> List.of("Administration", "Event Management", "Customer Service");
            case "ER" -> List.of("Business Operations", "Sales Engineering", "Technical Sales");
            case "EI" -> List.of("Business Strategy", "Market Research", "Management Consulting");
            case "EA" -> List.of("Marketing", "Brand Management", "Creative Direction");
            case "ES" -> List.of("Sales", "Marketing", "Public Relations");
            case "EC" -> List.of("Business Administration", "Finance", "Operations Management");
            case "CR" -> List.of("Operations", "Quality Assurance", "Technical Documentation");
            case "CI" -> List.of("Data Analysis", "Information Systems", "Research Administration");
            case "CA" -> List.of("Design", "Content Management", "Digital Marketing");
            case "CS" -> List.of("Administration", "Human Resources", "Customer Service");
            case "CE" -> List.of("Business Administration", "Project Management", "Operations");
            default -> List.of("Technology", "Business", "Creative Industries");
        };
    }
}