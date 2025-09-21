package com.ruvaa.backend.model.enums;

import lombok.Getter;

/**
 * Work preferences for Indian job market
 */
@Getter
public enum WorkPreference {
    GOVERNMENT("Government Job", "Stable government positions with job security"),
    PRIVATE_MNC("Private MNC", "Multinational companies with global exposure"),
    PRIVATE_INDIAN("Private Indian Company", "Indian private companies and startups"),
    STARTUP("Startup", "Early-stage companies with high growth potential"),
    ENTREPRENEURSHIP("Entrepreneurship", "Starting own business or venture"),
    FREELANCING("Freelancing", "Independent consulting and project-based work"),
    REMOTE_WORK("Remote Work", "Location-independent work opportunities"),
    HYBRID("Hybrid", "Mix of office and remote work"),
    RESEARCH_ACADEMIA("Research/Academia", "Academic institutions and research organizations"),
    NGO_SOCIAL("NGO/Social Sector", "Non-profit and social impact organizations");

    private final String displayName;
    private final String description;

    WorkPreference(String displayName, String description) {
        this.displayName = displayName;
        this.description = description;
    }

    /**
     * Get typical benefits associated with this work preference
     */
    public String getTypicalBenefits() {
        return switch (this) {
            case GOVERNMENT -> "Job security, pension, medical benefits, work-life balance";
            case PRIVATE_MNC -> "Good salary, international exposure, career growth, learning opportunities";
            case PRIVATE_INDIAN -> "Competitive salary, faster growth, Indian market understanding";
            case STARTUP -> "Equity participation, rapid learning, innovation, flexible culture";
            case ENTREPRENEURSHIP -> "Unlimited earning potential, independence, innovation, wealth creation";
            case FREELANCING -> "Flexibility, multiple income streams, work-life balance, skill diversity";
            case REMOTE_WORK -> "Location independence, cost savings, flexible schedule, global opportunities";
            case HYBRID -> "Best of both worlds, flexibility with collaboration, reduced commute";
            case RESEARCH_ACADEMIA -> "Intellectual satisfaction, research opportunities, tenure, academic freedom";
            case NGO_SOCIAL -> "Social impact, meaningful work, community development, personal satisfaction";
        };
    }

    /**
     * Get potential challenges
     */
    public String getChallenges() {
        return switch (this) {
            case GOVERNMENT -> "Slower career progression, bureaucracy, lower initial salary";
            case PRIVATE_MNC -> "High pressure, long hours, competition, potential layoffs";
            case PRIVATE_INDIAN -> "Variable growth opportunities, limited international exposure";
            case STARTUP -> "Job uncertainty, high stress, equity risk, long hours";
            case ENTREPRENEURSHIP -> "High risk, financial uncertainty, stress, responsibility";
            case FREELANCING -> "Income uncertainty, client acquisition, no employee benefits";
            case REMOTE_WORK -> "Isolation, communication challenges, self-discipline required";
            case HYBRID -> "Coordination challenges, technology dependence";
            case RESEARCH_ACADEMIA -> "Lower pay initially, competitive environment, funding challenges";
            case NGO_SOCIAL -> "Lower compensation, funding limitations, slow systemic change";
        };
    }

    /**
     * Get recommended skills for this work preference
     */
    public String getRecommendedSkills() {
        return switch (this) {
            case GOVERNMENT -> "Exam preparation, general knowledge, subject expertise, communication";
            case PRIVATE_MNC -> "Technical skills, soft skills, international business acumen, adaptability";
            case PRIVATE_INDIAN -> "Technical expertise, market understanding, networking, cultural fit";
            case STARTUP -> "Versatility, adaptability, risk-taking, innovation, learning agility";
            case ENTREPRENEURSHIP -> "Leadership, business acumen, risk management, networking, innovation";
            case FREELANCING -> "Self-marketing, client management, multiple skills, time management";
            case REMOTE_WORK -> "Self-discipline, digital communication, time management, tech-savviness";
            case HYBRID -> "Adaptability, communication, collaboration tools, time management";
            case RESEARCH_ACADEMIA -> "Research skills, analytical thinking, writing, presentation, patience";
            case NGO_SOCIAL -> "Social awareness, communication, fundraising, project management, empathy";
        };
    }
}