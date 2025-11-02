"""
Cosine Career Matcher for CareerConnect AI
Intelligent career matching using cosine similarity and multi-dimensional analysis
specifically designed for Indian students' career exploration.
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
class ProfileVector:
    """Student profile vector representation."""
    academic_subjects: np.ndarray
    extracurricular_activities: np.ndarray
    technical_skills: np.ndarray
    soft_skills: np.ndarray
    riasec_scores: np.ndarray
    interests: np.ndarray
    career_preferences: np.ndarray
    location_preferences: np.ndarray
    salary_expectations: np.ndarray
    work_environment: np.ndarray
    
    def to_array(self) -> np.ndarray:
        """Convert to single numpy array."""
        return np.concatenate([
            self.academic_subjects,
            self.extracurricular_activities,
            self.technical_skills,
            self.soft_skills,
            self.riasec_scores,
            self.interests,
            self.career_preferences,
            self.location_preferences,
            self.salary_expectations,
            self.work_environment
        ])

@dataclass
class CareerVector:
    """Career requirements vector representation."""
    education_requirements: np.ndarray
    essential_skills: np.ndarray
    personality_fit: np.ndarray
    industry_trends: np.ndarray
    salary_ranges: np.ndarray
    job_market_demand: np.ndarray
    location_availability: np.ndarray
    growth_prospects: np.ndarray
    
    def to_array(self) -> np.ndarray:
        """Convert to single numpy array."""
        return np.concatenate([
            self.education_requirements,
            self.essential_skills,
            self.personality_fit,
            self.industry_trends,
            self.salary_ranges,
            self.job_market_demand,
            self.location_availability,
            self.growth_prospects
        ])

@dataclass
class CareerMatch:
    """Career match result with detailed information."""
    career_name: str
    match_score: float
    confidence_level: str
    match_percentage: float
    explanation: str
    skill_gaps: List[str]
    improvement_suggestions: List[str]
    indian_context: Dict[str, Any]
    vector_similarity: float

class CosineCareerMatcher:
    """
    Intelligent career matching using cosine similarity and multi-dimensional analysis.
    
    Features:
    - Profile vectorization with multiple dimensions
    - Career database vectorization
    - Weighted cosine similarity calculation
    - Dynamic weighting based on student profile
    - Indian job market integration
    - Performance optimization with NumPy
    """
    
    def __init__(self):
        """Initialize cosine career matcher."""
        self.config = get_config()
        
        # Define vector dimensions
        self.dimensions = {
            'academic_subjects': 20,
            'extracurricular_activities': 15,
            'technical_skills': 25,
            'soft_skills': 20,
            'riasec_scores': 6,
            'interests': 30,
            'career_preferences': 10,
            'location_preferences': 10,
            'salary_expectations': 5,
            'work_environment': 8
        }
        
        # Define career vector dimensions
        self.career_dimensions = {
            'education_requirements': 20,
            'essential_skills': 25,
            'personality_fit': 6,
            'industry_trends': 10,
            'salary_ranges': 5,
            'job_market_demand': 8,
            'location_availability': 10,
            'growth_prospects': 5
        }
        
        # Initialize feature mappings
        self.academic_subjects_map = self._initialize_academic_subjects()
        self.extracurricular_map = self._initialize_extracurricular_activities()
        self.technical_skills_map = self._initialize_technical_skills()
        self.soft_skills_map = self._initialize_soft_skills()
        self.interests_map = self._initialize_interests()
        self.career_preferences_map = self._initialize_career_preferences()
        self.location_map = self._initialize_locations()
        self.salary_ranges_map = self._initialize_salary_ranges()
        self.work_environment_map = self._initialize_work_environment()
        
        # Load career database
        self.career_database = self._load_career_database()
        
        # Initialize weights
        self.base_weights = self._initialize_base_weights()
        
        logger.info("CosineCareerMatcher initialized successfully")
    
    def _initialize_academic_subjects(self) -> Dict[str, int]:
        """Initialize academic subjects mapping."""
        return {
            'Mathematics': 0, 'Physics': 1, 'Chemistry': 2, 'Biology': 3,
            'English': 4, 'Hindi': 5, 'Computer Science': 6, 'Economics': 7,
            'Business Studies': 8, 'Accountancy': 9, 'History': 10,
            'Geography': 11, 'Political Science': 12, 'Psychology': 13,
            'Sociology': 14, 'Philosophy': 15, 'Literature': 16,
            'Art': 17, 'Music': 18, 'Physical Education': 19
        }
    
    def _initialize_extracurricular_activities(self) -> Dict[str, int]:
        """Initialize extracurricular activities mapping."""
        return {
            'Sports': 0, 'Debate': 1, 'Drama': 2, 'Music': 3, 'Art': 4,
            'Science Club': 5, 'Math Olympiad': 6, 'Robotics': 7,
            'Volunteering': 8, 'Student Council': 9, 'Journalism': 10,
            'Photography': 11, 'Dance': 12, 'Chess': 13, 'Coding': 14
        }
    
    def _initialize_technical_skills(self) -> Dict[str, int]:
        """Initialize technical skills mapping."""
        return {
            'Programming': 0, 'Data Analysis': 1, 'Web Development': 2,
            'Mobile Development': 3, 'Database Management': 4,
            'Machine Learning': 5, 'Artificial Intelligence': 6,
            'Cybersecurity': 7, 'Cloud Computing': 8, 'DevOps': 9,
            'Software Testing': 10, 'UI/UX Design': 11, 'Digital Marketing': 12,
            'Project Management': 13, 'System Administration': 14,
            'Network Administration': 15, 'Game Development': 16,
            'Blockchain': 17, 'IoT': 18, 'AR/VR': 19, 'Automation': 20,
            'Data Science': 21, 'Business Intelligence': 22,
            'Quality Assurance': 23, 'Technical Writing': 24
        }
    
    def _initialize_soft_skills(self) -> Dict[str, int]:
        """Initialize soft skills mapping."""
        return {
            'Communication': 0, 'Leadership': 1, 'Teamwork': 2,
            'Problem Solving': 3, 'Critical Thinking': 4, 'Creativity': 5,
            'Time Management': 6, 'Adaptability': 7, 'Emotional Intelligence': 8,
            'Negotiation': 9, 'Presentation Skills': 10, 'Writing': 11,
            'Public Speaking': 12, 'Conflict Resolution': 13, 'Decision Making': 14,
            'Mentoring': 15, 'Customer Service': 16, 'Sales': 17,
            'Research': 18, 'Analytical Thinking': 19
        }
    
    def _initialize_interests(self) -> Dict[str, int]:
        """Initialize interests mapping."""
        return {
            'Technology': 0, 'Science': 1, 'Mathematics': 2, 'Engineering': 3,
            'Medicine': 4, 'Business': 5, 'Finance': 6, 'Marketing': 7,
            'Design': 8, 'Art': 9, 'Music': 10, 'Literature': 11,
            'History': 12, 'Psychology': 13, 'Sociology': 14, 'Philosophy': 15,
            'Sports': 16, 'Fitness': 17, 'Travel': 18, 'Photography': 19,
            'Cooking': 20, 'Gardening': 21, 'Gaming': 22, 'Movies': 23,
            'Politics': 24, 'Environment': 25, 'Social Work': 26,
            'Education': 27, 'Law': 28, 'Agriculture': 29
        }
    
    def _initialize_career_preferences(self) -> Dict[str, int]:
        """Initialize career preferences mapping."""
        return {
            'High Salary': 0, 'Job Security': 1, 'Career Growth': 2,
            'Work-Life Balance': 3, 'Creative Freedom': 4, 'Social Impact': 5,
            'Innovation': 6, 'Leadership Opportunities': 7, 'Travel': 8,
            'Flexible Schedule': 9
        }
    
    def _initialize_locations(self) -> Dict[str, int]:
        """Initialize location preferences mapping."""
        return {
            'Mumbai': 0, 'Delhi': 1, 'Bangalore': 2, 'Chennai': 3,
            'Hyderabad': 4, 'Pune': 5, 'Kolkata': 6, 'Ahmedabad': 7,
            'Gurgaon': 8, 'Noida': 9
        }
    
    def _initialize_salary_ranges(self) -> Dict[str, int]:
        """Initialize salary ranges mapping."""
        return {
            '0-3 LPA': 0, '3-6 LPA': 1, '6-10 LPA': 2, '10-15 LPA': 3,
            '15+ LPA': 4
        }
    
    def _initialize_work_environment(self) -> Dict[str, int]:
        """Initialize work environment preferences mapping."""
        return {
            'Office': 0, 'Remote': 1, 'Hybrid': 2, 'Field Work': 3,
            'Laboratory': 4, 'Studio': 5, 'Hospital': 6, 'School': 7
        }
    
    def _initialize_base_weights(self) -> Dict[str, float]:
        """Initialize base weights for different dimensions."""
        return {
            'academic_subjects': 0.15,
            'extracurricular_activities': 0.10,
            'technical_skills': 0.20,
            'soft_skills': 0.15,
            'riasec_scores': 0.15,
            'interests': 0.10,
            'career_preferences': 0.08,
            'location_preferences': 0.03,
            'salary_expectations': 0.02,
            'work_environment': 0.02
        }
    
    def calculate_profile_vector(self, student_profile: Dict[str, Any]) -> ProfileVector:
        """
        Convert student profile to numerical vector.
        
        Args:
            student_profile: Dictionary containing student information
            
        Returns:
            ProfileVector: Vectorized representation of student profile
        """
        # Initialize vectors
        academic_subjects = np.zeros(self.dimensions['academic_subjects'])
        extracurricular_activities = np.zeros(self.dimensions['extracurricular_activities'])
        technical_skills = np.zeros(self.dimensions['technical_skills'])
        soft_skills = np.zeros(self.dimensions['soft_skills'])
        riasec_scores = np.zeros(self.dimensions['riasec_scores'])
        interests = np.zeros(self.dimensions['interests'])
        career_preferences = np.zeros(self.dimensions['career_preferences'])
        location_preferences = np.zeros(self.dimensions['location_preferences'])
        salary_expectations = np.zeros(self.dimensions['salary_expectations'])
        work_environment = np.zeros(self.dimensions['work_environment'])
        
        # Process academic subjects
        if 'academic_subjects' in student_profile:
            for subject, grade in student_profile['academic_subjects'].items():
                if subject in self.academic_subjects_map:
                    idx = self.academic_subjects_map[subject]
                    academic_subjects[idx] = self._grade_to_score(grade)
        
        # Process extracurricular activities
        if 'extracurricular_activities' in student_profile:
            for activity in student_profile['extracurricular_activities']:
                if activity in self.extracurricular_map:
                    idx = self.extracurricular_map[activity]
                    extracurricular_activities[idx] = 1.0
        
        # Process technical skills
        if 'technical_skills' in student_profile:
            for skill, level in student_profile['technical_skills'].items():
                if skill in self.technical_skills_map:
                    idx = self.technical_skills_map[skill]
                    technical_skills[idx] = self._skill_level_to_score(level)
        
        # Process soft skills
        if 'soft_skills' in student_profile:
            for skill, level in student_profile['soft_skills'].items():
                if skill in self.soft_skills_map:
                    idx = self.soft_skills_map[skill]
                    soft_skills[idx] = self._skill_level_to_score(level)
        
        # Process RIASEC scores
        if 'riasec_scores' in student_profile:
            riasec_order = ['Realistic', 'Investigative', 'Artistic', 'Social', 'Enterprising', 'Conventional']
            for i, dimension in enumerate(riasec_order):
                if dimension in student_profile['riasec_scores']:
                    riasec_scores[i] = student_profile['riasec_scores'][dimension]
        
        # Process interests
        if 'interests' in student_profile:
            for interest in student_profile['interests']:
                if interest in self.interests_map:
                    idx = self.interests_map[interest]
                    interests[idx] = 1.0
        
        # Process career preferences
        if 'career_preferences' in student_profile:
            for preference in student_profile['career_preferences']:
                if preference in self.career_preferences_map:
                    idx = self.career_preferences_map[preference]
                    career_preferences[idx] = 1.0
        
        # Process location preferences
        if 'location_preferences' in student_profile:
            for location in student_profile['location_preferences']:
                if location in self.location_map:
                    idx = self.location_map[location]
                    location_preferences[idx] = 1.0
        
        # Process salary expectations
        if 'salary_expectations' in student_profile:
            salary_range = student_profile['salary_expectations']
            if salary_range in self.salary_ranges_map:
                idx = self.salary_ranges_map[salary_range]
                salary_expectations[idx] = 1.0
        
        # Process work environment preferences
        if 'work_environment_preferences' in student_profile:
            for env in student_profile['work_environment_preferences']:
                if env in self.work_environment_map:
                    idx = self.work_environment_map[env]
                    work_environment[idx] = 1.0
        
        return ProfileVector(
            academic_subjects=academic_subjects,
            extracurricular_activities=extracurricular_activities,
            technical_skills=technical_skills,
            soft_skills=soft_skills,
            riasec_scores=riasec_scores,
            interests=interests,
            career_preferences=career_preferences,
            location_preferences=location_preferences,
            salary_expectations=salary_expectations,
            work_environment=work_environment
        )
    
    def calculate_career_vectors(self, career_database: List[Dict[str, Any]]) -> List[Tuple[str, CareerVector]]:
        """
        Process career requirements into vectors.
        
        Args:
            career_database: List of career dictionaries
            
        Returns:
            List of tuples (career_name, CareerVector)
        """
        career_vectors = []
        
        for career in career_database:
            career_vector = self._create_career_vector(career)
            career_vectors.append((career['career'], career_vector))
        
        return career_vectors
    
    def compute_cosine_similarity(self, profile_vector: ProfileVector, career_vector: CareerVector) -> float:
        """
        Calculate weighted cosine similarity between profile and career vectors.
        
        Args:
            profile_vector: Student profile vector
            career_vector: Career requirements vector
            
        Returns:
            float: Cosine similarity score (0-1)
        """
        # Map profile to career-aligned dimensions for comparison
        # Profile: academic(20) + extra(15) + tech(25) + soft(20) + riasec(6) + interests(30) + career_pref(10) + location(10) + salary(5) + work_env(8) = 149
        # Career: education(20) + skills(25) + personality(6) + trends(10) + salary(5) + demand(8) + location(10) + growth(5) = 89
        
        aligned_profile = np.concatenate([
            profile_vector.academic_subjects[:20],  # Match education
            np.concatenate([profile_vector.technical_skills, profile_vector.soft_skills[:5]])[:25],  # Match skills
            profile_vector.riasec_scores,  # Match personality
            profile_vector.interests[:10],  # Match trends
            profile_vector.salary_expectations,  # Match salary
            np.zeros(8),  # Demand
            profile_vector.location_preferences[:10],  # Match location
            np.zeros(5)  # Growth
        ])
        
        career_array = career_vector.to_array()
        
        # Apply weights based on base weights (not dynamic for now)
        base_weights = np.array([
            *[self.base_weights.get('academic_subjects', 0.15)] * 20,
            *[self.base_weights.get('technical_skills', 0.20)] * 25,
            *[self.base_weights.get('riasec_scores', 0.15)] * 6,
            *[self.base_weights.get('interests', 0.10)] * 10,
            *[self.base_weights.get('salary_expectations', 0.02)] * 5,
            *[0.05] * 8,  # job_market_demand weight
            *[self.base_weights.get('location_preferences', 0.03)] * 10,
            *[0.05] * 5   # growth_prospects weight
        ])
        
        weighted_profile = aligned_profile * base_weights
        weighted_career = career_array * base_weights
        
        # Calculate cosine similarity
        dot_product = np.dot(weighted_profile, weighted_career)
        norm_profile = np.linalg.norm(weighted_profile)
        norm_career = np.linalg.norm(weighted_career)
        
        if norm_profile == 0 or norm_career == 0:
            return 0.0
        
        similarity = dot_product / (norm_profile * norm_career)
        return max(0.0, min(1.0, similarity))  # Clamp between 0 and 1
    
    def rank_career_matches(self, similarities: List[Tuple[str, float]]) -> List[Tuple[str, float]]:
        """
        Sort and rank careers by similarity score.
        
        Args:
            similarities: List of (career_name, similarity_score) tuples
            
        Returns:
            List of sorted tuples by similarity (highest first)
        """
        return sorted(similarities, key=lambda x: x[1], reverse=True)
    
    def generate_match_explanations(self, top_matches: List[Tuple[str, float]]) -> List[CareerMatch]:
        """
        Generate detailed explanations for career matches.
        
        Args:
            top_matches: List of (career_name, similarity_score) tuples
            
        Returns:
            List of CareerMatch objects with detailed information
        """
        matches = []
        
        for career_name, similarity in top_matches:
            # Find career in database
            career_info = next((c for c in self.career_database if c['career'] == career_name), None)
            
            if career_info:
                match_percentage = similarity * 100
                confidence_level = self._get_confidence_level(similarity)
                explanation = self._generate_explanation(career_name, similarity, career_info)
                skill_gaps = self._identify_skill_gaps(career_info)
                improvement_suggestions = self._generate_improvement_suggestions(career_info, skill_gaps)
                
                match = CareerMatch(
                    career_name=career_name,
                    match_score=similarity,
                    confidence_level=confidence_level,
                    match_percentage=match_percentage,
                    explanation=explanation,
                    skill_gaps=skill_gaps,
                    improvement_suggestions=improvement_suggestions,
                    indian_context=career_info.get('indian_context', {}),
                    vector_similarity=similarity
                )
                matches.append(match)
        
        return matches
    
    def _load_career_database(self) -> List[Dict[str, Any]]:
        """Load comprehensive career database with Indian context."""
        return [
            # Engineering Careers
            {
                'career': 'Software Engineer',
                'education_requirements': ['Computer Science', 'Information Technology', 'Electronics'],
                'essential_skills': ['Programming', 'Data Analysis', 'Web Development', 'Database Management'],
                'personality_fit': ['I', 'R', 'C'],
                'industry_trends': ['AI/ML', 'Cloud Computing', 'Cybersecurity'],
                'salary_range': '6-25 LPA',
                'job_market_demand': 'Very High',
                'location_availability': ['Bangalore', 'Hyderabad', 'Pune', 'Chennai', 'Mumbai'],
                'growth_prospects': 'Excellent',
                'indian_context': {
                    'entrance_exams': ['JEE Main', 'JEE Advanced', 'GATE'],
                    'top_colleges': ['IITs', 'NITs', 'IIITs'],
                    'companies': ['TCS', 'Infosys', 'Wipro', 'Google', 'Microsoft'],
                    'startup_ecosystem': 'Very Active'
                }
            },
            {
                'career': 'Data Scientist',
                'education_requirements': ['Mathematics', 'Statistics', 'Computer Science'],
                'essential_skills': ['Data Analysis', 'Machine Learning', 'Programming', 'Statistics'],
                'personality_fit': ['I', 'A', 'C'],
                'industry_trends': ['Big Data', 'AI', 'Analytics'],
                'salary_range': '8-30 LPA',
                'job_market_demand': 'High',
                'location_availability': ['Bangalore', 'Mumbai', 'Delhi', 'Hyderabad'],
                'growth_prospects': 'Excellent',
                'indian_context': {
                    'entrance_exams': ['JEE Main', 'GATE', 'CAT'],
                    'top_colleges': ['IITs', 'IIMs', 'ISI'],
                    'companies': ['Flipkart', 'Amazon', 'Google', 'Microsoft'],
                    'startup_ecosystem': 'Active'
                }
            },
            {
                'career': 'Mechanical Engineer',
                'education_requirements': ['Physics', 'Mathematics', 'Chemistry'],
                'essential_skills': ['CAD', 'Manufacturing', 'Project Management'],
                'personality_fit': ['R', 'I', 'C'],
                'industry_trends': ['Automation', 'Renewable Energy', 'IoT'],
                'salary_range': '4-15 LPA',
                'job_market_demand': 'Moderate',
                'location_availability': ['Pune', 'Chennai', 'Bangalore', 'Mumbai'],
                'growth_prospects': 'Good',
                'indian_context': {
                    'entrance_exams': ['JEE Main', 'JEE Advanced', 'GATE'],
                    'top_colleges': ['IITs', 'NITs', 'BITS Pilani'],
                    'companies': ['Tata Motors', 'Mahindra', 'Maruti Suzuki'],
                    'startup_ecosystem': 'Growing'
                }
            },
            
            # Medical Careers
            {
                'career': 'Doctor',
                'education_requirements': ['Biology', 'Chemistry', 'Physics'],
                'essential_skills': ['Communication', 'Problem Solving', 'Research'],
                'personality_fit': ['I', 'S', 'C'],
                'industry_trends': ['Telemedicine', 'AI in Healthcare', 'Precision Medicine'],
                'salary_range': '8-50 LPA',
                'job_market_demand': 'High',
                'location_availability': ['All Major Cities'],
                'growth_prospects': 'Excellent',
                'indian_context': {
                    'entrance_exams': ['NEET', 'AIIMS', 'JIPMER'],
                    'top_colleges': ['AIIMS', 'CMC Vellore', 'JIPMER'],
                    'companies': ['Apollo', 'Fortis', 'Max Healthcare'],
                    'startup_ecosystem': 'Active'
                }
            },
            
            # Business and Management
            {
                'career': 'Business Analyst',
                'education_requirements': ['Business Studies', 'Economics', 'Mathematics'],
                'essential_skills': ['Data Analysis', 'Communication', 'Problem Solving'],
                'personality_fit': ['I', 'E', 'C'],
                'industry_trends': ['Digital Transformation', 'Business Intelligence'],
                'salary_range': '6-20 LPA',
                'job_market_demand': 'High',
                'location_availability': ['Mumbai', 'Delhi', 'Bangalore', 'Chennai'],
                'growth_prospects': 'Very Good',
                'indian_context': {
                    'entrance_exams': ['CAT', 'XAT', 'GMAT'],
                    'top_colleges': ['IIMs', 'ISB', 'XLRI'],
                    'companies': ['McKinsey', 'BCG', 'Deloitte', 'Accenture'],
                    'startup_ecosystem': 'Very Active'
                }
            },
            
            # Arts and Design
            {
                'career': 'Graphic Designer',
                'education_requirements': ['Art', 'Computer Science'],
                'essential_skills': ['UI/UX Design', 'Creativity', 'Communication'],
                'personality_fit': ['A', 'E', 'I'],
                'industry_trends': ['Digital Design', 'Branding', 'User Experience'],
                'salary_range': '3-12 LPA',
                'job_market_demand': 'Moderate',
                'location_availability': ['Mumbai', 'Delhi', 'Bangalore', 'Chennai'],
                'growth_prospects': 'Good',
                'indian_context': {
                    'entrance_exams': ['NID', 'CEED', 'UCEED'],
                    'top_colleges': ['NID', 'IITs', 'Srishti Institute'],
                    'companies': ['Ogilvy', 'Leo Burnett', 'WPP'],
                    'startup_ecosystem': 'Active'
                }
            },
            
            # Education and Social Work
            {
                'career': 'Teacher',
                'education_requirements': ['Education', 'Subject Specialization'],
                'essential_skills': ['Communication', 'Mentoring', 'Presentation Skills'],
                'personality_fit': ['S', 'A', 'I'],
                'industry_trends': ['Online Education', 'EdTech', 'Personalized Learning'],
                'salary_range': '3-10 LPA',
                'job_market_demand': 'Stable',
                'location_availability': ['All Cities'],
                'growth_prospects': 'Stable',
                'indian_context': {
                    'entrance_exams': ['CTET', 'TET', 'NET'],
                    'top_colleges': ['DU', 'JNU', 'TISS'],
                    'companies': ['Khan Academy', 'Byju\'s', 'Vedantu'],
                    'startup_ecosystem': 'Very Active'
                }
            },
            
            # Government and Administration
            {
                'career': 'IAS Officer',
                'education_requirements': ['Any Graduate'],
                'essential_skills': ['Leadership', 'Communication', 'Decision Making'],
                'personality_fit': ['E', 'S', 'C'],
                'industry_trends': ['Digital Governance', 'Policy Making'],
                'salary_range': '8-25 LPA',
                'job_market_demand': 'Competitive',
                'location_availability': ['All States'],
                'growth_prospects': 'Stable',
                'indian_context': {
                    'entrance_exams': ['UPSC Civil Services'],
                    'top_colleges': ['Any Graduate'],
                    'companies': ['Government of India'],
                    'startup_ecosystem': 'N/A'
                }
            }
        ]
    
    def _create_career_vector(self, career: Dict[str, Any]) -> CareerVector:
        """Create vector for career requirements."""
        # Initialize vectors
        education_requirements = np.zeros(self.career_dimensions['education_requirements'])
        essential_skills = np.zeros(self.career_dimensions['essential_skills'])
        personality_fit = np.zeros(self.career_dimensions['personality_fit'])
        industry_trends = np.zeros(self.career_dimensions['industry_trends'])
        salary_ranges = np.zeros(self.career_dimensions['salary_ranges'])
        job_market_demand = np.zeros(self.career_dimensions['job_market_demand'])
        location_availability = np.zeros(self.career_dimensions['location_availability'])
        growth_prospects = np.zeros(self.career_dimensions['growth_prospects'])
        
        # Map education requirements
        if 'education_requirements' in career:
            for subject in career['education_requirements']:
                if subject in self.academic_subjects_map:
                    idx = self.academic_subjects_map[subject]
                    education_requirements[idx] = 1.0
        
        # Map essential skills
        if 'essential_skills' in career:
            for skill in career['essential_skills']:
                if skill in self.technical_skills_map:
                    idx = self.technical_skills_map[skill]
                    essential_skills[idx] = 1.0
                elif skill in self.soft_skills_map:
                    idx = self.soft_skills_map[skill]
                    essential_skills[idx] = 1.0
        
        # Map personality fit
        if 'personality_fit' in career:
            riasec_order = ['R', 'I', 'A', 'S', 'E', 'C']
            for code in career['personality_fit']:
                if code in riasec_order:
                    idx = riasec_order.index(code)
                    personality_fit[idx] = 1.0
        
        # Map industry trends
        if 'industry_trends' in career:
            trend_map = {
                'AI/ML': 0, 'Cloud Computing': 1, 'Cybersecurity': 2,
                'Big Data': 3, 'Analytics': 4, 'Automation': 5,
                'Renewable Energy': 6, 'IoT': 7, 'Telemedicine': 8,
                'Digital Transformation': 9
            }
            for trend in career['industry_trends']:
                if trend in trend_map:
                    idx = trend_map[trend]
                    industry_trends[idx] = 1.0
        
        # Map salary ranges
        if 'salary_range' in career:
            salary_map = {
                '0-3 LPA': 0, '3-6 LPA': 1, '6-10 LPA': 2,
                '10-15 LPA': 3, '15+ LPA': 4
            }
            salary_range = career['salary_range']
            if salary_range in salary_map:
                idx = salary_map[salary_range]
                salary_ranges[idx] = 1.0
        
        # Map job market demand
        if 'job_market_demand' in career:
            demand_map = {
                'Very High': 0, 'High': 1, 'Moderate': 2, 'Low': 3,
                'Stable': 4, 'Competitive': 5, 'Growing': 6, 'Declining': 7
            }
            demand = career['job_market_demand']
            if demand in demand_map:
                idx = demand_map[demand]
                job_market_demand[idx] = 1.0
        
        # Map location availability
        if 'location_availability' in career:
            for location in career['location_availability']:
                if location in self.location_map:
                    idx = self.location_map[location]
                    location_availability[idx] = 1.0
        
        # Map growth prospects
        if 'growth_prospects' in career:
            growth_map = {
                'Excellent': 0, 'Very Good': 1, 'Good': 2,
                'Stable': 3, 'Declining': 4
            }
            growth = career['growth_prospects']
            if growth in growth_map:
                idx = growth_map[growth]
                growth_prospects[idx] = 1.0
        
        return CareerVector(
            education_requirements=education_requirements,
            essential_skills=essential_skills,
            personality_fit=personality_fit,
            industry_trends=industry_trends,
            salary_ranges=salary_ranges,
            job_market_demand=job_market_demand,
            location_availability=location_availability,
            growth_prospects=growth_prospects
        )
    
    def _calculate_dynamic_weights(self, profile_vector: ProfileVector) -> np.ndarray:
        """Calculate dynamic weights based on student profile."""
        weights = np.ones(149)  # Total dimensions
        
        # Adjust weights based on student's strengths
        if np.sum(profile_vector.technical_skills) > 0:
            # Increase weight for technical skills if student has them
            start_idx = 35  # Start of technical skills
            end_idx = start_idx + self.dimensions['technical_skills']
            weights[start_idx:end_idx] *= 1.2
        
        if np.sum(profile_vector.riasec_scores) > 0:
            # Increase weight for RIASEC scores if available
            start_idx = 80  # Start of RIASEC scores
            end_idx = start_idx + self.dimensions['riasec_scores']
            weights[start_idx:end_idx] *= 1.3
        
        return weights
    
    def _grade_to_score(self, grade: str) -> float:
        """Convert grade to numerical score."""
        grade_map = {
            'A+': 5.0, 'A': 4.5, 'A-': 4.0,
            'B+': 3.5, 'B': 3.0, 'B-': 2.5,
            'C+': 2.0, 'C': 1.5, 'C-': 1.0,
            'D': 0.5, 'F': 0.0
        }
        return grade_map.get(grade, 3.0)
    
    def _skill_level_to_score(self, level: str) -> float:
        """Convert skill level to numerical score."""
        level_map = {
            'Expert': 5.0, 'Advanced': 4.0, 'Intermediate': 3.0,
            'Beginner': 2.0, 'Novice': 1.0
        }
        return level_map.get(level, 2.0)
    
    def _get_confidence_level(self, similarity: float) -> str:
        """Get confidence level based on similarity score."""
        if similarity >= 0.8:
            return "High"
        elif similarity >= 0.6:
            return "Good"
        elif similarity >= 0.4:
            return "Fair"
        else:
            return "Low"
    
    def _generate_explanation(self, career_name: str, similarity: float, career_info: Dict[str, Any]) -> str:
        """Generate explanation for career match."""
        percentage = similarity * 100
        
        if similarity >= 0.8:
            return f"Excellent ({percentage:.0f}%)"
        elif similarity >= 0.6:
            return f"Good ({percentage:.0f}%)"
        elif similarity >= 0.4:
            return f"Moderate ({percentage:.0f}%)"
        else:
            return f"Low ({percentage:.0f}%)"
    
    def _identify_skill_gaps(self, career_info: Dict[str, Any]) -> List[str]:
        """Identify skill gaps for career."""
        gaps = []
        
        if 'essential_skills' in career_info:
            for skill in career_info['essential_skills'][:3]:  # Only first 3
                gaps.append(f"Learn {skill}")
        
        return gaps[:3]  # Return top 3 gaps
    
    def _generate_improvement_suggestions(self, career_info: Dict[str, Any], skill_gaps: List[str]) -> List[str]:
        """Generate improvement suggestions."""
        suggestions = []
        
        # Add skill gap suggestions
        suggestions.extend(skill_gaps)
        
        # Add general suggestions
        suggestions.extend([
            "Take courses",
            "Build portfolio",
            "Get internship"
        ])
        
        return suggestions[:3]  # Return top 3 suggestions
    
    def match_careers(self, student_profile: Dict[str, Any], top_n: int = 10) -> List[CareerMatch]:
        """
        Complete career matching pipeline.
        
        Args:
            student_profile: Student profile dictionary
            top_n: Number of top matches to return
            
        Returns:
            List of CareerMatch objects
        """
        # Step 1: Convert profile to vector
        profile_vector = self.calculate_profile_vector(student_profile)
        
        # Step 2: Calculate career vectors
        career_vectors = self.calculate_career_vectors(self.career_database)
        
        # Step 3: Compute similarities
        similarities = []
        for career_name, career_vector in career_vectors:
            similarity = self.compute_cosine_similarity(profile_vector, career_vector)
            similarities.append((career_name, similarity))
        
        # Step 4: Rank matches
        ranked_matches = self.rank_career_matches(similarities)
        
        # Step 5: Generate explanations
        top_matches = ranked_matches[:top_n]
        matches = self.generate_match_explanations(top_matches)
        
        return matches
    
    def get_career_recommendations(self, student_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get comprehensive career recommendations with categorization.
        
        Args:
            student_profile: Student profile dictionary
            
        Returns:
            Dictionary with categorized recommendations
        """
        matches = self.match_careers(student_profile, top_n=15)
        
        # Categorize matches
        primary_recommendations = [m for m in matches if m.match_percentage >= 80]
        secondary_recommendations = [m for m in matches if 60 <= m.match_percentage < 80]
        emerging_opportunities = [m for m in matches if 40 <= m.match_percentage < 60]
        alternative_paths = [m for m in matches if m.match_percentage < 40]
        
        return {
            'primary_recommendations': primary_recommendations,
            'secondary_recommendations': secondary_recommendations,
            'emerging_opportunities': emerging_opportunities,
            'alternative_paths': alternative_paths,
            'summary': {
                'total_careers_analyzed': len(self.career_database),
                'top_match': matches[0] if matches else None,
                'average_match_score': sum(m.match_score for m in matches) / len(matches) if matches else 0,
                'confidence_distribution': self._get_confidence_distribution(matches)
            }
        }
    
    def _get_confidence_distribution(self, matches: List[CareerMatch]) -> Dict[str, int]:
        """Get distribution of confidence levels."""
        distribution = {'High': 0, 'Good': 0, 'Fair': 0, 'Low': 0}
        for match in matches:
            if match.confidence_level in distribution:
                distribution[match.confidence_level] += 1
        return distribution
    
    def get_career_database(self) -> List[Dict[str, Any]]:
        """Get career database."""
        return self.career_database
    
    def get_feature_mappings(self) -> Dict[str, Dict[str, int]]:
        """Get all feature mappings."""
        return {
            'academic_subjects': self.academic_subjects_map,
            'extracurricular_activities': self.extracurricular_map,
            'technical_skills': self.technical_skills_map,
            'soft_skills': self.soft_skills_map,
            'interests': self.interests_map,
            'career_preferences': self.career_preferences_map,
            'locations': self.location_map,
            'salary_ranges': self.salary_ranges_map,
            'work_environment': self.work_environment_map
        }

# Example usage and testing
if __name__ == "__main__":
    # Initialize matcher
    matcher = CosineCareerMatcher()
    
    # Sample student profile
    sample_profile = {
        'academic_subjects': {
            'Mathematics': 'A',
            'Physics': 'A',
            'Chemistry': 'B+',
            'Computer Science': 'A+',
            'English': 'B'
        },
        'extracurricular_activities': ['Coding', 'Robotics', 'Debate'],
        'technical_skills': {
            'Programming': 'Advanced',
            'Data Analysis': 'Intermediate',
            'Web Development': 'Beginner',
            'Machine Learning': 'Novice'
        },
        'soft_skills': {
            'Communication': 'Advanced',
            'Problem Solving': 'Advanced',
            'Leadership': 'Intermediate',
            'Teamwork': 'Advanced'
        },
        'riasec_scores': {
            'Realistic': 3.5,
            'Investigative': 4.8,
            'Artistic': 2.1,
            'Social': 3.2,
            'Enterprising': 3.8,
            'Conventional': 4.2
        },
        'interests': ['Technology', 'Science', 'Mathematics', 'Engineering'],
        'career_preferences': ['High Salary', 'Career Growth', 'Innovation'],
        'location_preferences': ['Bangalore', 'Mumbai', 'Delhi'],
        'salary_expectations': '10-15 LPA',
        'work_environment_preferences': ['Office', 'Hybrid']
    }
    
    print("CareerConnect AI - Cosine Career Matcher Example")
    print("=" * 60)
    
    # Get career recommendations
    recommendations = matcher.get_career_recommendations(sample_profile)
    
    print("\nPrimary Recommendations (80%+ match):")
    for match in recommendations['primary_recommendations']:
        print(f"  {match.career_name} - {match.match_percentage:.1f}% ({match.confidence_level})")
        print(f"    {match.explanation}")
        print(f"    Indian Context: {match.indian_context.get('salary_range', 'N/A')}")
        print()
    
    print("\nSecondary Recommendations (60-79% match):")
    for match in recommendations['secondary_recommendations']:
        print(f"  {match.career_name} - {match.match_percentage:.1f}% ({match.confidence_level})")
        print(f"    {match.explanation}")
        print()
    
    print("\nEmerging Opportunities (40-59% match):")
    for match in recommendations['emerging_opportunities']:
        print(f"  {match.career_name} - {match.match_percentage:.1f}% ({match.confidence_level})")
        print(f"    {match.explanation}")
        print()
    
    print("\nSummary:")
    summary = recommendations['summary']
    print(f"  Total Careers Analyzed: {summary['total_careers_analyzed']}")
    if summary['top_match']:
        print(f"  Top Match: {summary['top_match'].career_name} ({summary['top_match'].match_percentage:.1f}%)")
    print(f"  Average Match Score: {summary['average_match_score']:.3f}")
    print(f"  Confidence Distribution: {summary['confidence_distribution']}")
    
    print("\n" + "=" * 60)
    print("Example Complete")
    print("=" * 60)