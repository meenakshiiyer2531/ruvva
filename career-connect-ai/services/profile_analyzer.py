"""
Student Profile Analyzer for CareerConnect AI
Comprehensive student profile processing and analysis specifically designed for Indian students.
"""

import json
import logging
import math
from typing import Dict, List, Tuple, Any, Optional, Union
from dataclasses import dataclass
from datetime import datetime
import numpy as np
from config import get_config

logger = logging.getLogger(__name__)

@dataclass
class AcademicAnalysis:
    """Academic analysis results."""
    strong_subjects: List[str]
    weak_subjects: List[str]
    performance_trends: Dict[str, str]
    stream_recommendation: str
    competitive_exam_suitability: List[str]
    academic_trajectory: str
    subject_correlations: Dict[str, List[str]]
    overall_performance: str

@dataclass
class ExtracurricularAnalysis:
    """Extracurricular analysis results."""
    leadership_experience: List[str]
    activity_preferences: Dict[str, float]
    creative_vs_technical: str
    social_impact_score: float
    sports_participation: List[str]
    team_vs_individual: str
    activity_diversity_score: float

@dataclass
class SkillsAssessment:
    """Skills assessment results."""
    technical_skills: Dict[str, float]
    soft_skills: Dict[str, float]
    learning_agility: float
    problem_solving_approach: str
    digital_literacy: float
    skill_gaps: List[str]
    skill_strengths: List[str]

@dataclass
class InterestAnalysis:
    """Interest analysis results."""
    primary_interests: List[str]
    interest_intensity: Dict[str, float]
    cross_domain_connections: Dict[str, List[str]]
    emerging_interests: List[str]
    career_pathway_mapping: Dict[str, List[str]]
    interest_clusters: Dict[str, List[str]]

@dataclass
class ProfileInsights:
    """Comprehensive profile insights."""
    natural_talents: List[str]
    career_clusters: List[str]
    skill_development_recommendations: List[str]
    academic_pathway_suggestions: List[str]
    work_environment_preferences: List[str]
    personality_insights: str
    motivational_message: str
    next_steps: List[str]

@dataclass
class ProfileCompleteness:
    """Profile completeness assessment."""
    completeness_score: float
    missing_information: List[str]
    profile_improvements: List[str]
    priority_areas: List[str]
    completion_suggestions: List[str]

@dataclass
class CompleteProfileAnalysis:
    """Complete profile analysis results."""
    academic_analysis: AcademicAnalysis
    extracurricular_analysis: ExtracurricularAnalysis
    skills_assessment: SkillsAssessment
    interest_analysis: InterestAnalysis
    profile_insights: ProfileInsights
    completeness_assessment: ProfileCompleteness
    ai_generated_summary: str
    analysis_timestamp: datetime

class StudentProfileAnalyzer:
    """
    Comprehensive student profile analyzer for Indian students.
    
    Features:
    - Academic performance analysis
    - Extracurricular pattern recognition
    - Skills assessment processing
    - Interest cluster identification
    - Comprehensive insights generation
    - Profile completeness assessment
    - AI-powered narrative generation
    """
    
    def __init__(self):
        """Initialize profile analyzer."""
        self.config = get_config()
        
        # Initialize analysis components
        self.academic_subjects = self._initialize_academic_subjects()
        self.extracurricular_categories = self._initialize_extracurricular_categories()
        self.skill_categories = self._initialize_skill_categories()
        self.interest_categories = self._initialize_interest_categories()
        
        # Initialize analysis weights
        self.analysis_weights = self._initialize_analysis_weights()
        
        logger.info("StudentProfileAnalyzer initialized successfully")
    
    def analyze_complete_profile(self, profile_data: Dict[str, Any]) -> CompleteProfileAnalysis:
        """
        Perform comprehensive profile analysis.
        
        Args:
            profile_data: Complete student profile data
            
        Returns:
            CompleteProfileAnalysis: Comprehensive analysis results
        """
        try:
            logger.info("Starting comprehensive profile analysis")
            
            # Step 1: Academic Analysis
            academic_analysis = self.extract_academic_strengths(profile_data.get('academic_info', {}))
            
            # Step 2: Extracurricular Analysis
            extracurricular_analysis = self.analyze_extracurricular_patterns(profile_data.get('extracurricular_activities', []))
            
            # Step 3: Skills Assessment
            skills_assessment = self.assess_skill_levels(profile_data.get('skill_assessments', {}))
            
            # Step 4: Interest Analysis
            interest_analysis = self.identify_interest_clusters(profile_data.get('interests', []))
            
            # Step 5: Generate Insights
            analysis_results = {
                'academic': academic_analysis,
                'extracurricular': extracurricular_analysis,
                'skills': skills_assessment,
                'interests': interest_analysis
            }
            profile_insights = self.generate_profile_insights(analysis_results)
            
            # Step 6: Profile Completeness Assessment
            completeness_assessment = self._assess_profile_completeness(profile_data)
            
            # Step 7: AI-Generated Summary
            ai_summary = self._generate_ai_summary(analysis_results, profile_data)
            
            return CompleteProfileAnalysis(
                academic_analysis=academic_analysis,
                extracurricular_analysis=extracurricular_analysis,
                skills_assessment=skills_assessment,
                interest_analysis=interest_analysis,
                profile_insights=profile_insights,
                completeness_assessment=completeness_assessment,
                ai_generated_summary=ai_summary,
                analysis_timestamp=datetime.utcnow()
            )
            
        except Exception as e:
            logger.error(f"Error in complete profile analysis: {e}")
            raise Exception(f"Failed to analyze profile: {e}")
    
    def extract_academic_strengths(self, academic_info: Dict[str, Any]) -> AcademicAnalysis:
        """
        Analyze academic performance and identify strengths.
        
        Args:
            academic_info: Academic information dictionary
            
        Returns:
            AcademicAnalysis: Academic analysis results
        """
        # Extract academic data
        class_10_marks = academic_info.get('class_10_marks', {})
        class_12_marks = academic_info.get('class_12_marks', {})
        stream = academic_info.get('stream', '')
        competitive_exams = academic_info.get('competitive_exams', [])
        
        # Analyze subject performance
        strong_subjects = self._identify_strong_subjects(class_10_marks, class_12_marks)
        weak_subjects = self._identify_weak_subjects(class_10_marks, class_12_marks)
        
        # Analyze performance trends
        performance_trends = self._analyze_performance_trends(class_10_marks, class_12_marks)
        
        # Generate stream recommendation
        stream_recommendation = self._recommend_stream(strong_subjects, weak_subjects, academic_info)
        
        # Assess competitive exam suitability
        competitive_exam_suitability = self._assess_competitive_exam_suitability(strong_subjects, academic_info)
        
        # Predict academic trajectory
        academic_trajectory = self._predict_academic_trajectory(strong_subjects, performance_trends)
        
        # Analyze subject correlations
        subject_correlations = self._analyze_subject_correlations(strong_subjects, weak_subjects)
        
        # Overall performance assessment
        overall_performance = self._assess_overall_performance(class_10_marks, class_12_marks)
        
        return AcademicAnalysis(
            strong_subjects=strong_subjects,
            weak_subjects=weak_subjects,
            performance_trends=performance_trends,
            stream_recommendation=stream_recommendation,
            competitive_exam_suitability=competitive_exam_suitability,
            academic_trajectory=academic_trajectory,
            subject_correlations=subject_correlations,
            overall_performance=overall_performance
        )
    
    def analyze_extracurricular_patterns(self, activities: List[Dict[str, Any]]) -> ExtracurricularAnalysis:
        """
        Analyze extracurricular activities and identify patterns.
        
        Args:
            activities: List of extracurricular activities
            
        Returns:
            ExtracurricularAnalysis: Extracurricular analysis results
        """
        # Identify leadership experience
        leadership_experience = self._identify_leadership_experience(activities)
        
        # Analyze activity preferences
        activity_preferences = self._analyze_activity_preferences(activities)
        
        # Determine creative vs technical orientation
        creative_vs_technical = self._determine_creative_vs_technical(activities)
        
        # Calculate social impact score
        social_impact_score = self._calculate_social_impact_score(activities)
        
        # Identify sports participation
        sports_participation = self._identify_sports_participation(activities)
        
        # Determine team vs individual preference
        team_vs_individual = self._determine_team_vs_individual(activities)
        
        # Calculate activity diversity score
        activity_diversity_score = self._calculate_activity_diversity_score(activities)
        
        return ExtracurricularAnalysis(
            leadership_experience=leadership_experience,
            activity_preferences=activity_preferences,
            creative_vs_technical=creative_vs_technical,
            social_impact_score=social_impact_score,
            sports_participation=sports_participation,
            team_vs_individual=team_vs_individual,
            activity_diversity_score=activity_diversity_score
        )
    
    def assess_skill_levels(self, skill_assessments: Dict[str, Any]) -> SkillsAssessment:
        """
        Assess current skill levels and identify gaps.
        
        Args:
            skill_assessments: Skill assessment data
            
        Returns:
            SkillsAssessment: Skills assessment results
        """
        # Extract skill data
        technical_skills = skill_assessments.get('technical_skills', {})
        soft_skills = skill_assessments.get('soft_skills', {})
        
        # Assess learning agility
        learning_agility = self._assess_learning_agility(skill_assessments)
        
        # Analyze problem-solving approach
        problem_solving_approach = self._analyze_problem_solving_approach(skill_assessments)
        
        # Assess digital literacy
        digital_literacy = self._assess_digital_literacy(skill_assessments)
        
        # Identify skill gaps
        skill_gaps = self._identify_skill_gaps(technical_skills, soft_skills)
        
        # Identify skill strengths
        skill_strengths = self._identify_skill_strengths(technical_skills, soft_skills)
        
        return SkillsAssessment(
            technical_skills=technical_skills,
            soft_skills=soft_skills,
            learning_agility=learning_agility,
            problem_solving_approach=problem_solving_approach,
            digital_literacy=digital_literacy,
            skill_gaps=skill_gaps,
            skill_strengths=skill_strengths
        )
    
    def identify_interest_clusters(self, interests: List[str]) -> InterestAnalysis:
        """
        Identify interest clusters and patterns.
        
        Args:
            interests: List of student interests
            
        Returns:
            InterestAnalysis: Interest analysis results
        """
        # Identify primary interests
        primary_interests = self._identify_primary_interests(interests)
        
        # Calculate interest intensity
        interest_intensity = self._calculate_interest_intensity(interests)
        
        # Identify cross-domain connections
        cross_domain_connections = self._identify_cross_domain_connections(interests)
        
        # Identify emerging interests
        emerging_interests = self._identify_emerging_interests(interests)
        
        # Map interests to career pathways
        career_pathway_mapping = self._map_interests_to_career_pathways(interests)
        
        # Cluster similar interests
        interest_clusters = self._cluster_similar_interests(interests)
        
        return InterestAnalysis(
            primary_interests=primary_interests,
            interest_intensity=interest_intensity,
            cross_domain_connections=cross_domain_connections,
            emerging_interests=emerging_interests,
            career_pathway_mapping=career_pathway_mapping,
            interest_clusters=interest_clusters
        )
    
    def generate_profile_insights(self, analysis_results: Dict[str, Any]) -> ProfileInsights:
        """
        Generate comprehensive profile insights.
        
        Args:
            analysis_results: Results from all analysis components
            
        Returns:
            ProfileInsights: Comprehensive insights
        """
        # Identify natural talents
        natural_talents = self._identify_natural_talents(analysis_results)
        
        # Identify career clusters
        career_clusters = self._identify_career_clusters(analysis_results)
        
        # Generate skill development recommendations
        skill_development_recommendations = self._generate_skill_development_recommendations(analysis_results)
        
        # Generate academic pathway suggestions
        academic_pathway_suggestions = self._generate_academic_pathway_suggestions(analysis_results)
        
        # Identify work environment preferences
        work_environment_preferences = self._identify_work_environment_preferences(analysis_results)
        
        # Generate personality insights
        personality_insights = self._generate_personality_insights(analysis_results)
        
        # Generate motivational message
        motivational_message = self._generate_motivational_message(analysis_results)
        
        # Generate next steps
        next_steps = self._generate_next_steps(analysis_results)
        
        return ProfileInsights(
            natural_talents=natural_talents,
            career_clusters=career_clusters,
            skill_development_recommendations=skill_development_recommendations,
            academic_pathway_suggestions=academic_pathway_suggestions,
            work_environment_preferences=work_environment_preferences,
            personality_insights=personality_insights,
            motivational_message=motivational_message,
            next_steps=next_steps
        )
    
    def _initialize_academic_subjects(self) -> Dict[str, Dict[str, Any]]:
        """Initialize academic subjects mapping."""
        return {
            'Mathematics': {'category': 'STEM', 'difficulty': 'high', 'correlations': ['Physics', 'Chemistry']},
            'Physics': {'category': 'STEM', 'difficulty': 'high', 'correlations': ['Mathematics', 'Chemistry']},
            'Chemistry': {'category': 'STEM', 'difficulty': 'high', 'correlations': ['Mathematics', 'Physics', 'Biology']},
            'Biology': {'category': 'STEM', 'difficulty': 'medium', 'correlations': ['Chemistry']},
            'English': {'category': 'Language', 'difficulty': 'medium', 'correlations': ['Literature']},
            'Hindi': {'category': 'Language', 'difficulty': 'medium', 'correlations': ['English']},
            'Computer Science': {'category': 'STEM', 'difficulty': 'medium', 'correlations': ['Mathematics']},
            'Economics': {'category': 'Social Science', 'difficulty': 'medium', 'correlations': ['Mathematics', 'Business Studies']},
            'Business Studies': {'category': 'Commerce', 'difficulty': 'medium', 'correlations': ['Economics', 'Accountancy']},
            'Accountancy': {'category': 'Commerce', 'difficulty': 'medium', 'correlations': ['Mathematics', 'Business Studies']},
            'History': {'category': 'Social Science', 'difficulty': 'medium', 'correlations': ['Geography', 'Political Science']},
            'Geography': {'category': 'Social Science', 'difficulty': 'medium', 'correlations': ['History']},
            'Political Science': {'category': 'Social Science', 'difficulty': 'medium', 'correlations': ['History']},
            'Psychology': {'category': 'Social Science', 'difficulty': 'medium', 'correlations': ['Biology']},
            'Sociology': {'category': 'Social Science', 'difficulty': 'medium', 'correlations': ['Psychology']},
            'Philosophy': {'category': 'Humanities', 'difficulty': 'high', 'correlations': ['Literature']},
            'Literature': {'category': 'Humanities', 'difficulty': 'medium', 'correlations': ['English', 'Philosophy']},
            'Art': {'category': 'Creative', 'difficulty': 'medium', 'correlations': ['Music']},
            'Music': {'category': 'Creative', 'difficulty': 'medium', 'correlations': ['Art']},
            'Physical Education': {'category': 'Sports', 'difficulty': 'low', 'correlations': []}
        }
    
    def _initialize_extracurricular_categories(self) -> Dict[str, Dict[str, Any]]:
        """Initialize extracurricular categories."""
        return {
            'Sports': {'type': 'physical', 'leadership_potential': 'medium', 'team_oriented': True},
            'Debate': {'type': 'intellectual', 'leadership_potential': 'high', 'team_oriented': False},
            'Drama': {'type': 'creative', 'leadership_potential': 'medium', 'team_oriented': True},
            'Music': {'type': 'creative', 'leadership_potential': 'low', 'team_oriented': True},
            'Art': {'type': 'creative', 'leadership_potential': 'low', 'team_oriented': False},
            'Science Club': {'type': 'academic', 'leadership_potential': 'high', 'team_oriented': True},
            'Math Olympiad': {'type': 'academic', 'leadership_potential': 'low', 'team_oriented': False},
            'Robotics': {'type': 'technical', 'leadership_potential': 'high', 'team_oriented': True},
            'Volunteering': {'type': 'social', 'leadership_potential': 'high', 'team_oriented': True},
            'Student Council': {'type': 'leadership', 'leadership_potential': 'very_high', 'team_oriented': True},
            'Journalism': {'type': 'communication', 'leadership_potential': 'medium', 'team_oriented': True},
            'Photography': {'type': 'creative', 'leadership_potential': 'low', 'team_oriented': False},
            'Dance': {'type': 'creative', 'leadership_potential': 'medium', 'team_oriented': True},
            'Chess': {'type': 'intellectual', 'leadership_potential': 'low', 'team_oriented': False},
            'Coding': {'type': 'technical', 'leadership_potential': 'medium', 'team_oriented': False}
        }
    
    def _initialize_skill_categories(self) -> Dict[str, Dict[str, Any]]:
        """Initialize skill categories."""
        return {
            'Programming': {'category': 'technical', 'importance': 'high', 'difficulty': 'high'},
            'Data Analysis': {'category': 'technical', 'importance': 'high', 'difficulty': 'medium'},
            'Web Development': {'category': 'technical', 'importance': 'medium', 'difficulty': 'medium'},
            'Mobile Development': {'category': 'technical', 'importance': 'medium', 'difficulty': 'high'},
            'Database Management': {'category': 'technical', 'importance': 'medium', 'difficulty': 'medium'},
            'Machine Learning': {'category': 'technical', 'importance': 'high', 'difficulty': 'very_high'},
            'Artificial Intelligence': {'category': 'technical', 'importance': 'high', 'difficulty': 'very_high'},
            'Cybersecurity': {'category': 'technical', 'importance': 'high', 'difficulty': 'high'},
            'Cloud Computing': {'category': 'technical', 'importance': 'medium', 'difficulty': 'medium'},
            'DevOps': {'category': 'technical', 'importance': 'medium', 'difficulty': 'high'},
            'Communication': {'category': 'soft', 'importance': 'very_high', 'difficulty': 'medium'},
            'Leadership': {'category': 'soft', 'importance': 'high', 'difficulty': 'medium'},
            'Teamwork': {'category': 'soft', 'importance': 'high', 'difficulty': 'low'},
            'Problem Solving': {'category': 'soft', 'importance': 'very_high', 'difficulty': 'medium'},
            'Critical Thinking': {'category': 'soft', 'importance': 'high', 'difficulty': 'medium'},
            'Creativity': {'category': 'soft', 'importance': 'medium', 'difficulty': 'medium'},
            'Time Management': {'category': 'soft', 'importance': 'high', 'difficulty': 'low'},
            'Adaptability': {'category': 'soft', 'importance': 'high', 'difficulty': 'medium'},
            'Emotional Intelligence': {'category': 'soft', 'importance': 'medium', 'difficulty': 'medium'}
        }
    
    def _initialize_interest_categories(self) -> Dict[str, Dict[str, Any]]:
        """Initialize interest categories."""
        return {
            'Technology': {'category': 'STEM', 'career_relevance': 'high', 'growth_potential': 'very_high'},
            'Science': {'category': 'STEM', 'career_relevance': 'high', 'growth_potential': 'high'},
            'Mathematics': {'category': 'STEM', 'career_relevance': 'high', 'growth_potential': 'high'},
            'Engineering': {'category': 'STEM', 'career_relevance': 'very_high', 'growth_potential': 'high'},
            'Medicine': {'category': 'Healthcare', 'career_relevance': 'very_high', 'growth_potential': 'high'},
            'Business': {'category': 'Commerce', 'career_relevance': 'high', 'growth_potential': 'medium'},
            'Finance': {'category': 'Commerce', 'career_relevance': 'high', 'growth_potential': 'medium'},
            'Marketing': {'category': 'Commerce', 'career_relevance': 'medium', 'growth_potential': 'medium'},
            'Design': {'category': 'Creative', 'career_relevance': 'medium', 'growth_potential': 'medium'},
            'Art': {'category': 'Creative', 'career_relevance': 'low', 'growth_potential': 'low'},
            'Music': {'category': 'Creative', 'career_relevance': 'low', 'growth_potential': 'low'},
            'Literature': {'category': 'Humanities', 'career_relevance': 'low', 'growth_potential': 'low'},
            'History': {'category': 'Humanities', 'career_relevance': 'low', 'growth_potential': 'low'},
            'Psychology': {'category': 'Social Science', 'career_relevance': 'medium', 'growth_potential': 'medium'},
            'Sociology': {'category': 'Social Science', 'career_relevance': 'low', 'growth_potential': 'low'},
            'Philosophy': {'category': 'Humanities', 'career_relevance': 'low', 'growth_potential': 'low'},
            'Sports': {'category': 'Physical', 'career_relevance': 'low', 'growth_potential': 'low'},
            'Fitness': {'category': 'Physical', 'career_relevance': 'low', 'growth_potential': 'medium'},
            'Travel': {'category': 'Lifestyle', 'career_relevance': 'low', 'growth_potential': 'low'},
            'Photography': {'category': 'Creative', 'career_relevance': 'low', 'growth_potential': 'low'},
            'Cooking': {'category': 'Lifestyle', 'career_relevance': 'low', 'growth_potential': 'low'},
            'Gardening': {'category': 'Lifestyle', 'career_relevance': 'low', 'growth_potential': 'low'},
            'Gaming': {'category': 'Entertainment', 'career_relevance': 'low', 'growth_potential': 'medium'},
            'Movies': {'category': 'Entertainment', 'career_relevance': 'low', 'growth_potential': 'low'},
            'Politics': {'category': 'Social Science', 'career_relevance': 'medium', 'growth_potential': 'low'},
            'Environment': {'category': 'Social Science', 'career_relevance': 'medium', 'growth_potential': 'high'},
            'Social Work': {'category': 'Social Science', 'career_relevance': 'medium', 'growth_potential': 'medium'},
            'Education': {'category': 'Social Science', 'career_relevance': 'high', 'growth_potential': 'medium'},
            'Law': {'category': 'Professional', 'career_relevance': 'high', 'growth_potential': 'medium'},
            'Agriculture': {'category': 'STEM', 'career_relevance': 'medium', 'growth_potential': 'medium'}
        }
    
    def _initialize_analysis_weights(self) -> Dict[str, float]:
        """Initialize analysis weights."""
        return {
            'academic_performance': 0.25,
            'extracurricular_activities': 0.15,
            'technical_skills': 0.20,
            'soft_skills': 0.15,
            'interests': 0.15,
            'personality_traits': 0.10
        }
    
    # Academic Analysis Helper Methods
    def _identify_strong_subjects(self, class_10_marks: Dict[str, Any], class_12_marks: Dict[str, Any]) -> List[str]:
        """Identify strong subjects based on marks."""
        strong_subjects = []
        
        # Analyze class 10 marks
        for subject, marks in class_10_marks.items():
            if isinstance(marks, (int, float)) and marks >= 85:
                strong_subjects.append(subject)
        
        # Analyze class 12 marks
        for subject, marks in class_12_marks.items():
            if isinstance(marks, (int, float)) and marks >= 80:
                if subject not in strong_subjects:
                    strong_subjects.append(subject)
        
        return strong_subjects
    
    def _identify_weak_subjects(self, class_10_marks: Dict[str, Any], class_12_marks: Dict[str, Any]) -> List[str]:
        """Identify weak subjects based on marks."""
        weak_subjects = []
        
        # Analyze class 10 marks
        for subject, marks in class_10_marks.items():
            if isinstance(marks, (int, float)) and marks < 70:
                weak_subjects.append(subject)
        
        # Analyze class 12 marks
        for subject, marks in class_12_marks.items():
            if isinstance(marks, (int, float)) and marks < 65:
                if subject not in weak_subjects:
                    weak_subjects.append(subject)
        
        return weak_subjects
    
    def _analyze_performance_trends(self, class_10_marks: Dict[str, Any], class_12_marks: Dict[str, Any]) -> Dict[str, str]:
        """Analyze performance trends between class 10 and 12."""
        trends = {}
        
        for subject in class_10_marks.keys():
            if subject in class_12_marks:
                class_10_score = class_10_marks[subject] if isinstance(class_10_marks[subject], (int, float)) else 0
                class_12_score = class_12_marks[subject] if isinstance(class_12_marks[subject], (int, float)) else 0
                
                if class_12_score > class_10_score + 5:
                    trends[subject] = "Improving"
                elif class_12_score < class_10_score - 5:
                    trends[subject] = "Declining"
                else:
                    trends[subject] = "Stable"
        
        return trends
    
    def _recommend_stream(self, strong_subjects: List[str], weak_subjects: List[str], academic_info: Dict[str, Any]) -> str:
        """Recommend academic stream based on subject performance."""
        science_subjects = ['Mathematics', 'Physics', 'Chemistry', 'Biology']
        commerce_subjects = ['Economics', 'Business Studies', 'Accountancy']
        arts_subjects = ['History', 'Geography', 'Political Science', 'Literature', 'Psychology', 'Sociology']
        
        science_score = sum(1 for subject in strong_subjects if subject in science_subjects)
        commerce_score = sum(1 for subject in strong_subjects if subject in commerce_subjects)
        arts_score = sum(1 for subject in strong_subjects if subject in arts_subjects)
        
        # Check for weak subjects that might disqualify certain streams
        science_weak = sum(1 for subject in weak_subjects if subject in science_subjects)
        commerce_weak = sum(1 for subject in weak_subjects if subject in commerce_subjects)
        
        if science_score >= 2 and science_weak == 0:
            return "Science"
        elif commerce_score >= 2 and commerce_weak == 0:
            return "Commerce"
        elif arts_score >= 2:
            return "Arts"
        else:
            return "Mixed"
    
    def _assess_competitive_exam_suitability(self, strong_subjects: List[str], academic_info: Dict[str, Any]) -> List[str]:
        """Assess suitability for competitive exams."""
        suitable_exams = []
        
        # JEE (Engineering)
        if 'Mathematics' in strong_subjects and 'Physics' in strong_subjects:
            suitable_exams.append("JEE Main")
            if 'Chemistry' in strong_subjects:
                suitable_exams.append("JEE Advanced")
        
        # NEET (Medical)
        if 'Biology' in strong_subjects and 'Chemistry' in strong_subjects and 'Physics' in strong_subjects:
            suitable_exams.append("NEET")
        
        # CAT (Management)
        if 'Mathematics' in strong_subjects and ('Economics' in strong_subjects or 'Business Studies' in strong_subjects):
            suitable_exams.append("CAT")
        
        # CLAT (Law)
        if 'English' in strong_subjects and ('History' in strong_subjects or 'Political Science' in strong_subjects):
            suitable_exams.append("CLAT")
        
        # UPSC (Civil Services)
        if len(strong_subjects) >= 3 and 'English' in strong_subjects:
            suitable_exams.append("UPSC Civil Services")
        
        return suitable_exams
    
    def _predict_academic_trajectory(self, strong_subjects: List[str], performance_trends: Dict[str, str]) -> str:
        """Predict academic trajectory."""
        improving_count = sum(1 for trend in performance_trends.values() if trend == "Improving")
        declining_count = sum(1 for trend in performance_trends.values() if trend == "Declining")
        
        if improving_count > declining_count:
            return "Upward trajectory - likely to excel in higher education"
        elif declining_count > improving_count:
            return "Needs attention - consider additional support"
        else:
            return "Stable performance - consistent academic growth"
    
    def _analyze_subject_correlations(self, strong_subjects: List[str], weak_subjects: List[str]) -> Dict[str, List[str]]:
        """Analyze subject correlations."""
        correlations = {}
        
        for subject in strong_subjects:
            if subject in self.academic_subjects:
                correlations[subject] = self.academic_subjects[subject]['correlations']
        
        return correlations
    
    def _assess_overall_performance(self, class_10_marks: Dict[str, Any], class_12_marks: Dict[str, Any]) -> str:
        """Assess overall academic performance."""
        total_marks = 0
        count = 0
        
        # Calculate average from class 10
        for marks in class_10_marks.values():
            if isinstance(marks, (int, float)):
                total_marks += marks
                count += 1
        
        # Calculate average from class 12
        for marks in class_12_marks.values():
            if isinstance(marks, (int, float)):
                total_marks += marks
                count += 1
        
        if count == 0:
            return "Insufficient Data"
        
        average = total_marks / count
        
        if average >= 90:
            return "Excellent"
        elif average >= 80:
            return "Very Good"
        elif average >= 70:
            return "Good"
        elif average >= 60:
            return "Average"
        else:
            return "Below Average"
    
    # Extracurricular Analysis Helper Methods
    def _identify_leadership_experience(self, activities: List[Dict[str, Any]]) -> List[str]:
        """Identify leadership experience from activities."""
        leadership_activities = []
        
        for activity in activities:
            activity_name = activity.get('name', '').lower()
            role = activity.get('role', '').lower()
            
            # Check for leadership roles
            if any(leadership_word in role for leadership_word in ['president', 'captain', 'leader', 'head', 'coordinator']):
                leadership_activities.append(activity.get('name', ''))
            elif activity_name in self.extracurricular_categories:
                category_info = self.extracurricular_categories[activity_name]
                if category_info['leadership_potential'] in ['high', 'very_high']:
                    leadership_activities.append(activity.get('name', ''))
        
        return leadership_activities
    
    def _analyze_activity_preferences(self, activities: List[Dict[str, Any]]) -> Dict[str, float]:
        """Analyze activity preferences."""
        preferences = {
            'physical': 0.0,
            'intellectual': 0.0,
            'creative': 0.0,
            'technical': 0.0,
            'social': 0.0,
            'leadership': 0.0
        }
        
        for activity in activities:
            activity_name = activity.get('name', '')
            if activity_name in self.extracurricular_categories:
                category_info = self.extracurricular_categories[activity_name]
                activity_type = category_info['type']
                
                if activity_type in preferences:
                    preferences[activity_type] += 1.0
        
        # Normalize preferences
        total_activities = len(activities)
        if total_activities > 0:
            for key in preferences:
                preferences[key] = preferences[key] / total_activities
        
        return preferences
    
    def _determine_creative_vs_technical(self, activities: List[Dict[str, Any]]) -> str:
        """Determine creative vs technical orientation."""
        creative_count = 0
        technical_count = 0
        
        for activity in activities:
            activity_name = activity.get('name', '')
            if activity_name in self.extracurricular_categories:
                category_info = self.extracurricular_categories[activity_name]
                activity_type = category_info['type']
                
                if activity_type == 'creative':
                    creative_count += 1
                elif activity_type == 'technical':
                    technical_count += 1
        
        if creative_count > technical_count:
            return "Creative-oriented"
        elif technical_count > creative_count:
            return "Technical-oriented"
        else:
            return "Balanced"
    
    def _calculate_social_impact_score(self, activities: List[Dict[str, Any]]) -> float:
        """Calculate social impact score."""
        social_activities = ['Volunteering', 'Social Work', 'Community Service']
        social_count = 0
        
        for activity in activities:
            activity_name = activity.get('name', '')
            if activity_name in social_activities:
                social_count += 1
        
        return min(social_count / 3.0, 1.0)  # Normalize to 0-1
    
    def _identify_sports_participation(self, activities: List[Dict[str, Any]]) -> List[str]:
        """Identify sports participation."""
        sports_activities = []
        
        for activity in activities:
            activity_name = activity.get('name', '')
            if activity_name in self.extracurricular_categories:
                category_info = self.extracurricular_categories[activity_name]
                if category_info['type'] == 'physical':
                    sports_activities.append(activity_name)
        
        return sports_activities
    
    def _determine_team_vs_individual(self, activities: List[Dict[str, Any]]) -> str:
        """Determine team vs individual preference."""
        team_count = 0
        individual_count = 0
        
        for activity in activities:
            activity_name = activity.get('name', '')
            if activity_name in self.extracurricular_categories:
                category_info = self.extracurricular_categories[activity_name]
                if category_info['team_oriented']:
                    team_count += 1
                else:
                    individual_count += 1
        
        if team_count > individual_count:
            return "Team-oriented"
        elif individual_count > team_count:
            return "Individual-oriented"
        else:
            return "Balanced"
    
    def _calculate_activity_diversity_score(self, activities: List[Dict[str, Any]]) -> float:
        """Calculate activity diversity score."""
        activity_types = set()
        
        for activity in activities:
            activity_name = activity.get('name', '')
            if activity_name in self.extracurricular_categories:
                category_info = self.extracurricular_categories[activity_name]
                activity_types.add(category_info['type'])
        
        return len(activity_types) / 6.0  # Normalize to 0-1 (6 types max)
    
    # Skills Assessment Helper Methods
    def _assess_learning_agility(self, skill_assessments: Dict[str, Any]) -> float:
        """Assess learning agility."""
        # Simple heuristic based on skill diversity and levels
        technical_skills = skill_assessments.get('technical_skills', {})
        soft_skills = skill_assessments.get('soft_skills', {})
        
        total_skills = len(technical_skills) + len(soft_skills)
        if total_skills == 0:
            return 0.0
        
        # Calculate average skill level
        total_level = 0
        skill_count = 0
        
        for skill, level in technical_skills.items():
            if isinstance(level, (int, float)):
                total_level += level
                skill_count += 1
        
        for skill, level in soft_skills.items():
            if isinstance(level, (int, float)):
                total_level += level
                skill_count += 1
        
        if skill_count == 0:
            return 0.0
        
        average_level = total_level / skill_count
        diversity_score = min(total_skills / 10.0, 1.0)  # Normalize to 0-1
        
        return (average_level / 5.0) * 0.6 + diversity_score * 0.4  # Weighted combination
    
    def _analyze_problem_solving_approach(self, skill_assessments: Dict[str, Any]) -> str:
        """Analyze problem-solving approach."""
        soft_skills = skill_assessments.get('soft_skills', {})
        
        analytical_score = soft_skills.get('Critical Thinking', 0)
        creative_score = soft_skills.get('Creativity', 0)
        practical_score = soft_skills.get('Problem Solving', 0)
        
        if analytical_score >= 4:
            return "Analytical - prefers systematic, logical approaches"
        elif creative_score >= 4:
            return "Creative - prefers innovative, out-of-the-box solutions"
        elif practical_score >= 4:
            return "Practical - prefers hands-on, solution-focused approaches"
        else:
            return "Balanced - adapts approach based on situation"
    
    def _assess_digital_literacy(self, skill_assessments: Dict[str, Any]) -> float:
        """Assess digital literacy."""
        technical_skills = skill_assessments.get('technical_skills', {})
        
        digital_skills = ['Programming', 'Web Development', 'Database Management', 'Cloud Computing']
        digital_score = 0
        
        for skill in digital_skills:
            if skill in technical_skills:
                level = technical_skills[skill]
                if isinstance(level, (int, float)):
                    digital_score += level
        
        return min(digital_score / (len(digital_skills) * 5.0), 1.0)  # Normalize to 0-1
    
    def _identify_skill_gaps(self, technical_skills: Dict[str, float], soft_skills: Dict[str, float]) -> List[str]:
        """Identify skill gaps."""
        gaps = []
        
        # Check for missing critical technical skills
        critical_technical = ['Programming', 'Data Analysis', 'Communication']
        for skill in critical_technical:
            if skill not in technical_skills and skill not in soft_skills:
                gaps.append(f"Develop {skill} skills")
        
        # Check for low-level skills
        for skill, level in technical_skills.items():
            if isinstance(level, (int, float)) and level < 3:
                gaps.append(f"Improve {skill} proficiency")
        
        for skill, level in soft_skills.items():
            if isinstance(level, (int, float)) and level < 3:
                gaps.append(f"Strengthen {skill} abilities")
        
        return gaps[:5]  # Return top 5 gaps
    
    def _identify_skill_strengths(self, technical_skills: Dict[str, float], soft_skills: Dict[str, float]) -> List[str]:
        """Identify skill strengths."""
        strengths = []
        
        # Identify high-level skills
        for skill, level in technical_skills.items():
            if isinstance(level, (int, float)) and level >= 4:
                strengths.append(skill)
        
        for skill, level in soft_skills.items():
            if isinstance(level, (int, float)) and level >= 4:
                strengths.append(skill)
        
        return strengths[:5]  # Return top 5 strengths
    
    # Interest Analysis Helper Methods
    def _identify_primary_interests(self, interests: List[str]) -> List[str]:
        """Identify primary interests."""
        # Simple heuristic - interests with high career relevance
        primary_interests = []
        
        for interest in interests:
            if interest in self.interest_categories:
                category_info = self.interest_categories[interest]
                if category_info['career_relevance'] in ['high', 'very_high']:
                    primary_interests.append(interest)
        
        return primary_interests[:5]  # Return top 5
    
    def _calculate_interest_intensity(self, interests: List[str]) -> Dict[str, float]:
        """Calculate interest intensity."""
        intensity = {}
        
        for interest in interests:
            if interest in self.interest_categories:
                category_info = self.interest_categories[interest]
                # Base intensity on career relevance and growth potential
                base_score = 0.5
                if category_info['career_relevance'] == 'very_high':
                    base_score += 0.3
                elif category_info['career_relevance'] == 'high':
                    base_score += 0.2
                
                if category_info['growth_potential'] == 'very_high':
                    base_score += 0.2
                elif category_info['growth_potential'] == 'high':
                    base_score += 0.1
                
                intensity[interest] = min(base_score, 1.0)
        
        return intensity
    
    def _identify_cross_domain_connections(self, interests: List[str]) -> Dict[str, List[str]]:
        """Identify cross-domain connections."""
        connections = {}
        
        # Group interests by category
        categories = {}
        for interest in interests:
            if interest in self.interest_categories:
                category = self.interest_categories[interest]['category']
                if category not in categories:
                    categories[category] = []
                categories[category].append(interest)
        
        # Find connections between categories
        for category, interest_list in categories.items():
            if len(interest_list) > 1:
                connections[category] = interest_list
        
        return connections
    
    def _identify_emerging_interests(self, interests: List[str]) -> List[str]:
        """Identify emerging interests."""
        emerging = []
        
        for interest in interests:
            if interest in self.interest_categories:
                category_info = self.interest_categories[interest]
                if category_info['growth_potential'] == 'very_high':
                    emerging.append(interest)
        
        return emerging
    
    def _map_interests_to_career_pathways(self, interests: List[str]) -> Dict[str, List[str]]:
        """Map interests to career pathways."""
        pathway_mapping = {
            'Technology': ['Software Engineer', 'Data Scientist', 'Cybersecurity Analyst'],
            'Science': ['Research Scientist', 'Lab Technician', 'Science Teacher'],
            'Mathematics': ['Data Analyst', 'Statistician', 'Actuary'],
            'Engineering': ['Mechanical Engineer', 'Civil Engineer', 'Electrical Engineer'],
            'Medicine': ['Doctor', 'Nurse', 'Pharmacist'],
            'Business': ['Business Analyst', 'Management Consultant', 'Entrepreneur'],
            'Finance': ['Financial Analyst', 'Investment Banker', 'Accountant'],
            'Design': ['Graphic Designer', 'UI/UX Designer', 'Architect'],
            'Education': ['Teacher', 'Professor', 'Educational Consultant'],
            'Law': ['Lawyer', 'Legal Advisor', 'Judge']
        }
        
        mapped_pathways = {}
        for interest in interests:
            if interest in pathway_mapping:
                mapped_pathways[interest] = pathway_mapping[interest]
        
        return mapped_pathways
    
    def _cluster_similar_interests(self, interests: List[str]) -> Dict[str, List[str]]:
        """Cluster similar interests."""
        clusters = {}
        
        for interest in interests:
            if interest in self.interest_categories:
                category = self.interest_categories[interest]['category']
                if category not in clusters:
                    clusters[category] = []
                clusters[category].append(interest)
        
        return clusters
    
    # Profile Insights Helper Methods
    def _identify_natural_talents(self, analysis_results: Dict[str, Any]) -> List[str]:
        """Identify natural talents."""
        talents = []
        
        academic = analysis_results.get('academic')
        if academic:
            if academic.overall_performance in ['Excellent', 'Very Good']:
                talents.append("Academic Excellence")
            
            if len(academic.strong_subjects) >= 3:
                talents.append("Multi-subject Proficiency")
            
            if 'Mathematics' in academic.strong_subjects:
                talents.append("Mathematical Aptitude")
            
            if 'Physics' in academic.strong_subjects:
                talents.append("Scientific Thinking")
        
        extracurricular = analysis_results.get('extracurricular')
        if extracurricular:
            if extracurricular.activity_diversity_score >= 0.7:
                talents.append("Versatile Interests")
            
            if extracurricular.social_impact_score >= 0.7:
                talents.append("Social Leadership")
        
        skills = analysis_results.get('skills')
        if skills:
            if skills.learning_agility >= 0.7:
                talents.append("Quick Learning")
            
            if skills.digital_literacy >= 0.7:
                talents.append("Digital Proficiency")
        
        return talents
    
    def _identify_career_clusters(self, analysis_results: Dict[str, Any]) -> List[str]:
        """Identify career clusters."""
        clusters = []
        
        academic = analysis_results.get('academic')
        if academic:
            if 'Mathematics' in academic.strong_subjects and 'Physics' in academic.strong_subjects:
                clusters.append("Engineering and Technology")
            
            if 'Biology' in academic.strong_subjects and 'Chemistry' in academic.strong_subjects:
                clusters.append("Medicine and Healthcare")
            
            if 'Economics' in academic.strong_subjects or 'Business Studies' in academic.strong_subjects:
                clusters.append("Business and Management")
        
        interests = analysis_results.get('interests')
        if interests:
            for cluster_name, interest_list in interests.interest_clusters.items():
                if len(interest_list) >= 2:
                    clusters.append(f"{cluster_name.title()} Careers")
        
        return list(set(clusters))  # Remove duplicates
    
    def _generate_skill_development_recommendations(self, analysis_results: Dict[str, Any]) -> List[str]:
        """Generate skill development recommendations."""
        recommendations = []
        
        skills = analysis_results.get('skills')
        if skills:
            recommendations.extend(skills.skill_gaps)
        
        academic = analysis_results.get('academic')
        if academic:
            if len(academic.weak_subjects) > 0:
                recommendations.append(f"Focus on improving {', '.join(academic.weak_subjects)}")
        
        extracurricular = analysis_results.get('extracurricular')
        if extracurricular:
            if extracurricular.activity_diversity_score < 0.5:
                recommendations.append("Explore diverse extracurricular activities")
        
        return recommendations[:5]  # Return top 5 recommendations
    
    def _generate_academic_pathway_suggestions(self, analysis_results: Dict[str, Any]) -> List[str]:
        """Generate academic pathway suggestions."""
        suggestions = []
        
        academic = analysis_results.get('academic')
        if academic:
            suggestions.append(f"Consider {academic.stream_recommendation} stream")
            
            if academic.competitive_exam_suitability:
                suggestions.append(f"Prepare for {', '.join(academic.competitive_exam_suitability)}")
            
            suggestions.append(academic.academic_trajectory)
        
        return suggestions
    
    def _identify_work_environment_preferences(self, analysis_results: Dict[str, Any]) -> List[str]:
        """Identify work environment preferences."""
        preferences = []
        
        extracurricular = analysis_results.get('extracurricular')
        if extracurricular:
            if extracurricular.team_vs_individual == "Team-oriented":
                preferences.append("Collaborative team environment")
            elif extracurricular.team_vs_individual == "Individual-oriented":
                preferences.append("Independent work environment")
            
            if extracurricular.creative_vs_technical == "Creative-oriented":
                preferences.append("Creative and flexible workspace")
            elif extracurricular.creative_vs_technical == "Technical-oriented":
                preferences.append("Technical and structured environment")
        
        return preferences
    
    def _generate_personality_insights(self, analysis_results: Dict[str, Any]) -> str:
        """Generate personality insights."""
        insights = []
        
        academic = analysis_results.get('academic')
        if academic:
            if academic.overall_performance == "Excellent":
                insights.append("You demonstrate exceptional academic ability")
            elif academic.overall_performance == "Very Good":
                insights.append("You show strong academic potential")
        
        extracurricular = analysis_results.get('extracurricular')
        if extracurricular:
            if extracurricular.social_impact_score >= 0.7:
                insights.append("You have a strong social conscience")
            
            if extracurricular.activity_diversity_score >= 0.7:
                insights.append("You are well-rounded and versatile")
        
        skills = analysis_results.get('skills')
        if skills:
            if skills.learning_agility >= 0.7:
                insights.append("You are a quick learner and adaptable")
        
        if not insights:
            insights.append("You have unique strengths waiting to be discovered")
        
        return ". ".join(insights) + "."
    
    def _generate_motivational_message(self, analysis_results: Dict[str, Any]) -> str:
        """Generate motivational message."""
        academic = analysis_results.get('academic')
        if academic and academic.overall_performance in ['Excellent', 'Very Good']:
            return "Your academic excellence shows great potential. Continue building on your strengths while exploring new opportunities."
        else:
            return "Every student has unique talents and potential. Focus on your strengths and don't be afraid to explore new areas of interest."
    
    def _generate_next_steps(self, analysis_results: Dict[str, Any]) -> List[str]:
        """Generate next steps."""
        steps = []
        
        academic = analysis_results.get('academic')
        if academic:
            if academic.competitive_exam_suitability:
                steps.append(f"Start preparing for {academic.competitive_exam_suitability[0]}")
            
            if len(academic.weak_subjects) > 0:
                steps.append(f"Get additional help in {', '.join(academic.weak_subjects[:2])}")
        
        skills = analysis_results.get('skills')
        if skills and skills.skill_gaps:
            steps.append(f"Develop {skills.skill_gaps[0]}")
        
        steps.append("Research career options in your interest areas")
        steps.append("Connect with professionals in your field of interest")
        steps.append("Create a personal development plan")
        
        return steps
    
    # Profile Completeness Assessment
    def _assess_profile_completeness(self, profile_data: Dict[str, Any]) -> ProfileCompleteness:
        """Assess profile completeness."""
        required_fields = ['academic_info', 'interests', 'skill_assessments']
        optional_fields = ['extracurricular_activities', 'riasec_scores', 'career_goals']
        
        required_score = sum(1 for field in required_fields if profile_data.get(field)) / len(required_fields)
        optional_score = sum(1 for field in optional_fields if profile_data.get(field)) / len(optional_fields)
        
        completeness_score = (required_score * 0.7) + (optional_score * 0.3)
        
        missing_information = []
        for field in required_fields:
            if not profile_data.get(field):
                missing_information.append(field.replace('_', ' ').title())
        
        profile_improvements = [
            "Add detailed academic performance data",
            "Include comprehensive skill assessments",
            "Specify career goals and aspirations"
        ]
        
        priority_areas = []
        if completeness_score < 0.5:
            priority_areas.append("Complete basic profile information")
        if completeness_score < 0.7:
            priority_areas.append("Add detailed academic and skill data")
        
        completion_suggestions = [
            "Complete all required profile sections",
            "Add detailed academic performance data",
            "Include comprehensive skill assessments",
            "Specify career interests and goals"
        ]
        
        return ProfileCompleteness(
            completeness_score=completeness_score,
            missing_information=missing_information,
            profile_improvements=profile_improvements,
            priority_areas=priority_areas,
            completion_suggestions=completion_suggestions
        )
    
    def _generate_ai_summary(self, analysis_results: Dict[str, Any], profile_data: Dict[str, Any]) -> str:
        """Generate AI-powered summary."""
        # This would typically integrate with Gemini AI
        # For now, return a basic summary
        academic = analysis_results.get('academic')
        if academic:
            return f"This student shows {academic.overall_performance.lower()} academic performance with strengths in {', '.join(academic.strong_subjects[:3])}. The recommended stream is {academic.stream_recommendation}."
        else:
            return "This student profile shows potential for growth and development across multiple areas."
