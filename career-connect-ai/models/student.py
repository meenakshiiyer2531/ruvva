"""
Student data models
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime
from typing import Dict, List, Any, Optional

Base = declarative_base()

class Student(Base):
    """Student profile model"""
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    age = Column(Integer)
    phone = Column(String(20))
    
    # Profile Information
    education_level = Column(String(50))
    current_occupation = Column(String(100))
    experience_level = Column(String(50))
    location = Column(String(100))
    
    # Skills and Interests
    skills = Column(JSON)  # List of skills
    interests = Column(JSON)  # List of interests
    career_goals = Column(JSON)  # List of career goals
    
    # Assessment Results
    riasec_scores = Column(JSON)  # RIASEC personality scores
    personality_traits = Column(JSON)  # Detailed personality analysis
    skill_assessments = Column(JSON)  # Skill assessment results
    
    # Learning Preferences
    learning_style = Column(String(50))
    preferred_learning_methods = Column(JSON)
    availability_hours = Column(Integer)
    
    # Career Development
    target_careers = Column(JSON)  # List of target careers
    career_readiness_score = Column(Float)
    development_priorities = Column(JSON)
    
    # Profile Metadata
    profile_completeness = Column(Float, default=0.0)
    last_updated = Column(DateTime, default=func.now())
    created_at = Column(DateTime, default=func.now())
    is_active = Column(Boolean, default=True)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'age': self.age,
            'phone': self.phone,
            'education_level': self.education_level,
            'current_occupation': self.current_occupation,
            'experience_level': self.experience_level,
            'location': self.location,
            'skills': self.skills or [],
            'interests': self.interests or [],
            'career_goals': self.career_goals or [],
            'riasec_scores': self.riasec_scores or {},
            'personality_traits': self.personality_traits or {},
            'skill_assessments': self.skill_assessments or {},
            'learning_style': self.learning_style,
            'preferred_learning_methods': self.preferred_learning_methods or [],
            'availability_hours': self.availability_hours,
            'target_careers': self.target_careers or [],
            'career_readiness_score': self.career_readiness_score,
            'development_priorities': self.development_priorities or [],
            'profile_completeness': self.profile_completeness,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Student':
        """Create model from dictionary"""
        student = cls()
        for key, value in data.items():
            if hasattr(student, key):
                setattr(student, key, value)
        return student

class StudentProgress(Base):
    """Student progress tracking model"""
    __tablename__ = 'student_progress'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, nullable=False)
    
    # Progress Tracking
    skill_progress = Column(JSON)  # Skill development progress
    learning_progress = Column(JSON)  # Learning path progress
    career_progress = Column(JSON)  # Career development progress
    
    # Achievements
    completed_assessments = Column(JSON)
    completed_courses = Column(JSON)
    earned_certifications = Column(JSON)
    completed_projects = Column(JSON)
    
    # Goals and Milestones
    current_goals = Column(JSON)
    achieved_milestones = Column(JSON)
    upcoming_milestones = Column(JSON)
    
    # Performance Metrics
    overall_progress_score = Column(Float, default=0.0)
    skill_improvement_rate = Column(Float, default=0.0)
    goal_completion_rate = Column(Float, default=0.0)
    
    # Timestamps
    last_updated = Column(DateTime, default=func.now())
    created_at = Column(DateTime, default=func.now())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'student_id': self.student_id,
            'skill_progress': self.skill_progress or {},
            'learning_progress': self.learning_progress or {},
            'career_progress': self.career_progress or {},
            'completed_assessments': self.completed_assessments or [],
            'completed_courses': self.completed_courses or [],
            'earned_certifications': self.earned_certifications or [],
            'completed_projects': self.completed_projects or [],
            'current_goals': self.current_goals or [],
            'achieved_milestones': self.achieved_milestones or [],
            'upcoming_milestones': self.upcoming_milestones or [],
            'overall_progress_score': self.overall_progress_score,
            'skill_improvement_rate': self.skill_improvement_rate,
            'goal_completion_rate': self.goal_completion_rate,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class StudentFeedback(Base):
    """Student feedback model"""
    __tablename__ = 'student_feedback'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, nullable=False)
    
    # Feedback Content
    feedback_type = Column(String(50))  # 'assessment', 'recommendation', 'mentor', 'general'
    feedback_category = Column(String(50))  # 'positive', 'negative', 'suggestion'
    feedback_text = Column(Text)
    rating = Column(Integer)  # 1-5 scale
    
    # Context
    related_item_id = Column(Integer)  # ID of related assessment, recommendation, etc.
    related_item_type = Column(String(50))
    
    # Metadata
    is_anonymous = Column(Boolean, default=False)
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'student_id': self.student_id,
            'feedback_type': self.feedback_type,
            'feedback_category': self.feedback_category,
            'feedback_text': self.feedback_text,
            'rating': self.rating,
            'related_item_id': self.related_item_id,
            'related_item_type': self.related_item_type,
            'is_anonymous': self.is_anonymous,
            'is_public': self.is_public,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class StudentSession(Base):
    """Student session tracking model"""
    __tablename__ = 'student_sessions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, nullable=False)
    session_id = Column(String(100), unique=True, nullable=False)
    
    # Session Information
    session_type = Column(String(50))  # 'chat', 'assessment', 'mentor', 'learning'
    session_status = Column(String(50))  # 'active', 'completed', 'cancelled'
    
    # Session Data
    session_data = Column(JSON)  # Session-specific data
    conversation_history = Column(JSON)  # Chat conversation history
    
    # Performance Metrics
    session_duration = Column(Integer)  # Duration in minutes
    engagement_score = Column(Float)
    satisfaction_score = Column(Float)
    
    # Timestamps
    started_at = Column(DateTime, default=func.now())
    ended_at = Column(DateTime)
    last_activity = Column(DateTime, default=func.now())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'student_id': self.student_id,
            'session_id': self.session_id,
            'session_type': self.session_type,
            'session_status': self.session_status,
            'session_data': self.session_data or {},
            'conversation_history': self.conversation_history or [],
            'session_duration': self.session_duration,
            'engagement_score': self.engagement_score,
            'satisfaction_score': self.satisfaction_score,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'ended_at': self.ended_at.isoformat() if self.ended_at else None,
            'last_activity': self.last_activity.isoformat() if self.last_activity else None
        }
