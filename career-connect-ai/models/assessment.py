"""
Assessment result models
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime
from typing import Dict, List, Any, Optional

Base = declarative_base()

class Assessment(Base):
    """Assessment model"""
    __tablename__ = 'assessments'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    
    # Assessment Details
    assessment_type = Column(String(50))  # 'riasec', 'skills', 'personality', 'aptitude'
    category = Column(String(100))
    difficulty_level = Column(String(50))  # 'beginner', 'intermediate', 'advanced'
    
    # Questions and Structure
    questions = Column(JSON)  # List of questions
    question_count = Column(Integer)
    estimated_duration = Column(Integer)  # Duration in minutes
    
    # Scoring and Results
    scoring_method = Column(String(100))
    result_categories = Column(JSON)  # Categories for results
    interpretation_guide = Column(JSON)  # Guide for interpreting results
    
    # Metadata
    is_active = Column(Boolean, default=True)
    version = Column(String(20), default='1.0')
    created_at = Column(DateTime, default=func.now())
    last_updated = Column(DateTime, default=func.now())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'assessment_type': self.assessment_type,
            'category': self.category,
            'difficulty_level': self.difficulty_level,
            'questions': self.questions or [],
            'question_count': self.question_count,
            'estimated_duration': self.estimated_duration,
            'scoring_method': self.scoring_method,
            'result_categories': self.result_categories or [],
            'interpretation_guide': self.interpretation_guide or {},
            'is_active': self.is_active,
            'version': self.version,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None
        }

class AssessmentResult(Base):
    """Assessment result model"""
    __tablename__ = 'assessment_results'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, nullable=False)
    assessment_id = Column(Integer, nullable=False)
    
    # Assessment Session
    session_id = Column(String(100))
    started_at = Column(DateTime, default=func.now())
    completed_at = Column(DateTime)
    duration_minutes = Column(Integer)
    
    # Responses and Scores
    responses = Column(JSON)  # Student responses
    raw_scores = Column(JSON)  # Raw assessment scores
    normalized_scores = Column(JSON)  # Normalized scores
    percentile_scores = Column(JSON)  # Percentile scores
    
    # Results and Analysis
    primary_result = Column(String(100))  # Primary result category
    secondary_results = Column(JSON)  # Secondary result categories
    detailed_analysis = Column(JSON)  # Detailed analysis results
    recommendations = Column(JSON)  # Recommendations based on results
    
    # Quality Metrics
    completion_rate = Column(Float)  # Percentage of questions answered
    response_consistency = Column(Float)  # Consistency of responses
    validity_score = Column(Float)  # Validity of the assessment
    
    # Status
    status = Column(String(50), default='completed')  # 'in_progress', 'completed', 'abandoned'
    is_valid = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    last_updated = Column(DateTime, default=func.now())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'student_id': self.student_id,
            'assessment_id': self.assessment_id,
            'session_id': self.session_id,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'duration_minutes': self.duration_minutes,
            'responses': self.responses or {},
            'raw_scores': self.raw_scores or {},
            'normalized_scores': self.normalized_scores or {},
            'percentile_scores': self.percentile_scores or {},
            'primary_result': self.primary_result,
            'secondary_results': self.secondary_results or [],
            'detailed_analysis': self.detailed_analysis or {},
            'recommendations': self.recommendations or [],
            'completion_rate': self.completion_rate,
            'response_consistency': self.response_consistency,
            'validity_score': self.validity_score,
            'status': self.status,
            'is_valid': self.is_valid,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None
        }

class RIASECResult(Base):
    """RIASEC personality assessment result model"""
    __tablename__ = 'riasec_results'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, nullable=False)
    assessment_result_id = Column(Integer, nullable=False)
    
    # RIASEC Scores
    realistic_score = Column(Float, nullable=False)
    investigative_score = Column(Float, nullable=False)
    artistic_score = Column(Float, nullable=False)
    social_score = Column(Float, nullable=False)
    enterprising_score = Column(Float, nullable=False)
    conventional_score = Column(Float, nullable=False)
    
    # Dominant Types
    primary_type = Column(String(50))
    secondary_type = Column(String(50))
    tertiary_type = Column(String(50))
    
    # Analysis Results
    personality_description = Column(Text)
    work_preferences = Column(JSON)
    communication_style = Column(String(100))
    leadership_style = Column(String(100))
    
    # Career Implications
    recommended_careers = Column(JSON)
    career_suitability = Column(JSON)
    development_areas = Column(JSON)
    
    # Metadata
    assessment_date = Column(DateTime, default=func.now())
    is_valid = Column(Boolean, default=True)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'student_id': self.student_id,
            'assessment_result_id': self.assessment_result_id,
            'riasec_scores': {
                'realistic': self.realistic_score,
                'investigative': self.investigative_score,
                'artistic': self.artistic_score,
                'social': self.social_score,
                'enterprising': self.enterprising_score,
                'conventional': self.conventional_score
            },
            'dominant_types': {
                'primary': self.primary_type,
                'secondary': self.secondary_type,
                'tertiary': self.tertiary_type
            },
            'personality_description': self.personality_description,
            'work_preferences': self.work_preferences or [],
            'communication_style': self.communication_style,
            'leadership_style': self.leadership_style,
            'recommended_careers': self.recommended_careers or [],
            'career_suitability': self.career_suitability or {},
            'development_areas': self.development_areas or [],
            'assessment_date': self.assessment_date.isoformat() if self.assessment_date else None,
            'is_valid': self.is_valid
        }

class SkillAssessment(Base):
    """Skill assessment model"""
    __tablename__ = 'skill_assessments'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, nullable=False)
    assessment_result_id = Column(Integer, nullable=False)
    
    # Skill Categories
    technical_skills = Column(JSON)  # Technical skill scores
    soft_skills = Column(JSON)  # Soft skill scores
    domain_skills = Column(JSON)  # Domain-specific skill scores
    
    # Overall Scores
    overall_technical_score = Column(Float)
    overall_soft_score = Column(Float)
    overall_domain_score = Column(Float)
    overall_skill_score = Column(Float)
    
    # Skill Analysis
    skill_strengths = Column(JSON)  # Strongest skills
    skill_gaps = Column(JSON)  # Skills needing development
    skill_priorities = Column(JSON)  # Priority skills for development
    
    # Recommendations
    skill_development_plan = Column(JSON)
    learning_recommendations = Column(JSON)
    practice_recommendations = Column(JSON)
    
    # Metadata
    assessment_date = Column(DateTime, default=func.now())
    assessment_version = Column(String(20))
    is_valid = Column(Boolean, default=True)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'student_id': self.student_id,
            'assessment_result_id': self.assessment_result_id,
            'technical_skills': self.technical_skills or {},
            'soft_skills': self.soft_skills or {},
            'domain_skills': self.domain_skills or {},
            'overall_scores': {
                'technical': self.overall_technical_score,
                'soft': self.overall_soft_score,
                'domain': self.overall_domain_score,
                'overall': self.overall_skill_score
            },
            'skill_strengths': self.skill_strengths or [],
            'skill_gaps': self.skill_gaps or [],
            'skill_priorities': self.skill_priorities or [],
            'skill_development_plan': self.skill_development_plan or {},
            'learning_recommendations': self.learning_recommendations or [],
            'practice_recommendations': self.practice_recommendations or [],
            'assessment_date': self.assessment_date.isoformat() if self.assessment_date else None,
            'assessment_version': self.assessment_version,
            'is_valid': self.is_valid
        }

class AssessmentSession(Base):
    """Assessment session tracking model"""
    __tablename__ = 'assessment_sessions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, nullable=False)
    assessment_id = Column(Integer, nullable=False)
    session_id = Column(String(100), unique=True, nullable=False)
    
    # Session Information
    session_status = Column(String(50))  # 'started', 'in_progress', 'completed', 'abandoned'
    current_question = Column(Integer, default=0)
    total_questions = Column(Integer)
    
    # Progress Tracking
    answered_questions = Column(JSON)  # List of answered question IDs
    skipped_questions = Column(JSON)  # List of skipped question IDs
    progress_percentage = Column(Float, default=0.0)
    
    # Session Data
    responses = Column(JSON)  # Current responses
    session_data = Column(JSON)  # Additional session data
    
    # Timestamps
    started_at = Column(DateTime, default=func.now())
    last_activity = Column(DateTime, default=func.now())
    completed_at = Column(DateTime)
    expires_at = Column(DateTime)  # Session expiration time
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'student_id': self.student_id,
            'assessment_id': self.assessment_id,
            'session_id': self.session_id,
            'session_status': self.session_status,
            'current_question': self.current_question,
            'total_questions': self.total_questions,
            'answered_questions': self.answered_questions or [],
            'skipped_questions': self.skipped_questions or [],
            'progress_percentage': self.progress_percentage,
            'responses': self.responses or {},
            'session_data': self.session_data or {},
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'last_activity': self.last_activity.isoformat() if self.last_activity else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None
        }
