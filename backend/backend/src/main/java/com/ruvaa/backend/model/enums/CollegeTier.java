package com.ruvaa.backend.model.enums;

import lombok.Getter;
import java.util.List;

/**
 * Indian College/University Tier Classification
 * Used for career guidance and placement expectations
 */
@Getter
public enum CollegeTier {
    TIER_1("Tier 1", "Premier Institutions", List.of(
        "IIT", "IIM", "IIIT", "NIT", "BITS", "ISI", "ISB", "NLSIU", "SRCC", "LSR", "Hindu College"
    )),
    TIER_2("Tier 2", "Good State/Private Universities", List.of(
        "State Universities", "VIT", "SRM", "Manipal", "Amity", "DTU", "NSIT", "Regional Engineering Colleges"
    )),
    TIER_3("Tier 3", "Local/Regional Colleges", List.of(
        "Local Engineering Colleges", "Regional Universities", "District Colleges", "Private Institutes"
    )),
    AUTONOMOUS("Autonomous", "Autonomous Institutions", List.of(
        "Autonomous Colleges", "Deemed Universities", "Private Universities with Good Reputation"
    )),
    INTERNATIONAL("International", "Foreign Universities", List.of(
        "Universities abroad", "International campuses", "Foreign degree programs"
    ));

    private final String displayName;
    private final String description;
    private final List<String> examples;

    CollegeTier(String displayName, String description, List<String> examples) {
        this.displayName = displayName;
        this.description = description;
        this.examples = examples;
    }

    /**
     * Get expected placement package range in LPA
     */
    public String getExpectedPackageRange() {
        return switch (this) {
            case TIER_1 -> "15-50+ LPA";
            case TIER_2 -> "6-20 LPA";
            case TIER_3 -> "3-8 LPA";
            case AUTONOMOUS -> "4-12 LPA";
            case INTERNATIONAL -> "20-80 LPA";
        };
    }

    /**
     * Get typical recruiting companies
     */
    public List<String> getTypicalRecruiters() {
        return switch (this) {
            case TIER_1 -> List.of("Google", "Microsoft", "Amazon", "Goldman Sachs", "McKinsey", "BCG", "FAANG Companies");
            case TIER_2 -> List.of("TCS", "Infosys", "Wipro", "Accenture", "Cognizant", "HCL", "Capgemini");
            case TIER_3 -> List.of("Local Companies", "Startups", "Small-Medium IT Companies", "Regional Businesses");
            case AUTONOMOUS -> List.of("Mix of Tier 1 & Tier 2 Companies", "Product Companies", "Service Companies");
            case INTERNATIONAL -> List.of("MNCs", "Global Consulting Firms", "International Banks", "Tech Giants");
        };
    }

    /**
     * Get career guidance specific to this tier
     */
    public String getCareerGuidance() {
        return switch (this) {
            case TIER_1 -> "Focus on product companies, startups, and high-growth roles. Consider entrepreneurship and global opportunities.";
            case TIER_2 -> "Build strong technical skills, consider certifications, and aim for product companies after gaining experience.";
            case TIER_3 -> "Focus on skill development, gain certifications, build projects, and consider upskilling for better opportunities.";
            case AUTONOMOUS -> "Leverage college reputation while focusing on skill building and networking for diverse opportunities.";
            case INTERNATIONAL -> "Leverage global exposure for international roles, consulting, and leadership positions.";
        };
    }

    /**
     * Check if this tier typically gets direct campus placements
     */
    public boolean hasCampusPlacement() {
        return this != TIER_3; // Tier 3 colleges often have limited campus placements
    }
}