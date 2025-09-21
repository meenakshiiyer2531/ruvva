package com.ruvaa.backend.model.enums;

import lombok.Getter;

/**
 * Education levels in the Indian education system
 */
@Getter
public enum EducationLevel {
    CLASS_10("Class 10", "Secondary School Certificate (SSC)"),
    CLASS_12_SCIENCE("Class 12 - Science", "Higher Secondary Certificate - Science Stream"),
    CLASS_12_COMMERCE("Class 12 - Commerce", "Higher Secondary Certificate - Commerce Stream"),
    CLASS_12_ARTS("Class 12 - Arts", "Higher Secondary Certificate - Arts Stream"),
    
    DIPLOMA("Diploma", "Diploma in Engineering/Other Fields"),
    
    BACHELOR_ENGINEERING("Bachelor's - Engineering", "B.Tech/B.E."),
    BACHELOR_MEDICAL("Bachelor's - Medical", "MBBS/BDS/BAMS/BHMS"),
    BACHELOR_COMMERCE("Bachelor's - Commerce", "B.Com/BBA"),
    BACHELOR_SCIENCE("Bachelor's - Science", "B.Sc."),
    BACHELOR_ARTS("Bachelor's - Arts", "B.A."),
    BACHELOR_LAW("Bachelor's - Law", "LLB"),
    BACHELOR_OTHER("Bachelor's - Other", "Other Bachelor's Degree"),
    
    MASTER_ENGINEERING("Master's - Engineering", "M.Tech/M.E."),
    MASTER_MANAGEMENT("Master's - Management", "MBA/PGDM"),
    MASTER_SCIENCE("Master's - Science", "M.Sc."),
    MASTER_ARTS("Master's - Arts", "M.A."),
    MASTER_COMMERCE("Master's - Commerce", "M.Com"),
    MASTER_LAW("Master's - Law", "LLM"),
    MASTER_OTHER("Master's - Other", "Other Master's Degree"),
    
    DOCTORATE("Doctorate", "Ph.D./Other Doctoral Degree"),
    
    PROFESSIONAL_COURSE("Professional Course", "CA/CS/CMA/Other Professional Courses");

    private final String displayName;
    private final String description;

    EducationLevel(String displayName, String description) {
        this.displayName = displayName;
        this.description = description;
    }

    /**
     * Get education level category for grouping
     */
    public String getCategory() {
        if (name().startsWith("CLASS_")) return "School";
        if (name().equals("DIPLOMA")) return "Diploma";
        if (name().startsWith("BACHELOR_")) return "Undergraduate";
        if (name().startsWith("MASTER_")) return "Postgraduate";
        if (name().equals("DOCTORATE")) return "Doctoral";
        if (name().equals("PROFESSIONAL_COURSE")) return "Professional";
        return "Other";
    }

    /**
     * Check if this level qualifies for job applications
     */
    public boolean isJobEligible() {
        return !name().equals("CLASS_10") && !name().equals("CLASS_12_SCIENCE") && 
               !name().equals("CLASS_12_COMMERCE") && !name().equals("CLASS_12_ARTS");
    }

    /**
     * Get typical age range for this education level
     */
    public String getTypicalAgeRange() {
        return switch (getCategory()) {
            case "School" -> "14-18";
            case "Diploma" -> "17-20";
            case "Undergraduate" -> "18-22";
            case "Postgraduate" -> "22-26";
            case "Doctoral" -> "25-30";
            case "Professional" -> "20-28";
            default -> "18-30";
        };
    }
}