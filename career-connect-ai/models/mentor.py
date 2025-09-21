"""
Mentor profile models
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime
from typing import Dict, List, Any, Optional

Base = declarative_base()

class Mentor(Base):
    """Mentor profile model"""
    __tablename__ = 'mentors'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    
    # Professional Information
    current_position = Column(String(200))
    company = Column(String(200))
    industry = Column(String(100))
    years_experience = Column(Integer)
    experience_level = Column(String(50))  # 'mid', 'senior', 'executive', 'expert'
    
    # Expertise Areas
    expertise_areas = Column(JSON)  # List of expertise areas
    skills = Column(JSON)  # List of skills
    specializations = Column(JSON)  # List of specializations
    
    # Education and Certifications
    education_background = Column(JSON)  # Education history
    certifications = Column(JSON)  # Professional certifications
    achievements = Column(JSON)  # Professional achievements
    
    # Mentoring Information
    mentoring_experience = Column(Integer)  # Years of mentoring experience
    mentoring_style = Column(String(50))  # 'structured', 'casual', 'collaborative'
    mentoring_approach = Column(String(100))  # Approach to mentoring
    preferred_mentoring_topics = Column(JSON)  # Topics they prefer to mentor on
    
    # Availability and Preferences
    availability_status = Column(String(50))  # 'available', 'busy', 'unavailable'
    current_mentees = Column(Integer, default=0)
    max_mentees = Column(Integer, default=5)
    preferred_meeting_frequency = Column(String(50))  # 'weekly', 'bi-weekly', 'monthly'
    preferred_meeting_duration = Column(Integer)  # Duration in minutes
    timezone = Column(String(50))
    
    # Communication Preferences
    communication_preference = Column(String(50))  # 'email', 'video', 'phone', 'in-person'
    response_time = Column(String(50))  # 'immediate', '24 hours', '48 hours'
    preferred_communication_style = Column(String(50))  # 'formal', 'casual', 'friendly'
    
    # Location and Work Environment
    location = Column(String(100))
    workplace_type = Column(String(50))  # 'office', 'remote', 'hybrid'
    willing_to_travel = Column(Boolean, default=False)
    remote_mentoring_available = Column(Boolean, default=True)
    
    # Profile Information
    bio = Column(Text)
    profile_picture_url = Column(String(500))
    linkedin_url = Column(String(500))
    portfolio_url = Column(String(500))
    
    # Performance Metrics
    average_rating = Column(Float, default=0.0)
    total_mentees_helped = Column(Integer, default=0)
    success_rate = Column(Float, default=0.0)
    testimonials_count = Column(Integer, default=0)
    
    # Status and Verification
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    verification_date = Column(DateTime)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    last_updated = Column(DateTime, default=func.now())
    last_active = Column(DateTime, default=func.now())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'current_position': self.current_position,
            'company': self.company,
            'industry': self.industry,
            'years_experience': self.years_experience,
            'experience_level': self.experience_level,
            'expertise_areas': self.expertise_areas or [],
            'skills': self.skills or [],
            'specializations': self.specializations or [],
            'education_background': self.education_background or [],
            'certifications': self.certifications or [],
            'achievements': self.achievements or [],
            'mentoring_experience': self.mentoring_experience,
            'mentoring_style': self.mentoring_style,
            'mentoring_approach': self.mentoring_approach,
            'preferred_mentoring_topics': self.preferred_mentoring_topics or [],
            'availability_status': self.availability_status,
            'current_mentees': self.current_mentees,
            'max_mentees': self.max_mentees,
            'preferred_meeting_frequency': self.preferred_meeting_frequency,
            'preferred_meeting_duration': self.preferred_meeting_duration,
            'timezone': self.timezone,
            'communication_preference': self.communication_preference,
            'response_time': self.response_time,
            'preferred_communication_style': self.preferred_communication_style,
            'location': self.location,
            'workplace_type': self.workplace_type,
            'willing_to_travel': self.willing_to_travel,
            'remote_mentoring_available': self.remote_mentoring_available,
            'bio': self.bio,
            'profile_picture_url': self.profile_picture_url,
            'linkedin_url': self.linkedin_url,
            'portfolio_url': self.portfolio_url,
            'average_rating': self.average_rating,
            'total_mentees_helped': self.total_mentees_helped,
            'success_rate': self.success_rate,
            'testimonials_count': self.testimonials_count,
            'is_verified': self.is_verified,
            'is_active': self.is_active,
            'verification_date': self.verification_date.isoformat() if self.verification_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
            'last_active': self.last_active.isoformat() if self.last_active else None
        }

class Mentorship(Base):
    """Mentorship relationship model"""
    __tablename__ = 'mentorships'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    mentor_id = Column(Integer, nullable=False)
    student_id = Column(Integer, nullable=False)
    
    # Mentorship Details
    mentorship_type = Column(String(50))  # 'career', 'skill', 'general', 'project'
    mentorship_title = Column(String(200))
    mentorship_description = Column(Text)
    
    # Goals and Objectives
    primary_goals = Column(JSON)  # Primary mentorship goals
    secondary_goals = Column(JSON)  # Secondary goals
    success_metrics = Column(JSON)  # How success will be measured
    
    # Structure and Timeline
    mentorship_duration = Column(Integer)  # Duration in weeks
    meeting_frequency = Column(String(50))  # 'weekly', 'bi-weekly', 'monthly'
    meeting_duration = Column(Integer)  # Duration in minutes
    total_sessions = Column(Integer)  # Total planned sessions
    
    # Status and Progress
    status = Column(String(50), default='active')  # 'active', 'completed', 'paused', 'cancelled'
    progress_percentage = Column(Float, default=0.0)
    sessions_completed = Column(Integer, default=0)
    goals_achieved = Column(Integer, default=0)
    
    # Communication and Logistics
    communication_method = Column(String(50))  # 'video', 'phone', 'email', 'in-person'
    meeting_platform = Column(String(100))  # Platform used for meetings
    shared_resources = Column(JSON)  # Shared documents and resources
    
    # Performance and Feedback
    mentor_rating = Column(Float)  # Student's rating of mentor
    student_rating = Column(Float)  # Mentor's rating of student
    overall_satisfaction = Column(Float)  # Overall satisfaction score
    feedback_exchanged = Column(JSON)  # Feedback between mentor and student
    
    # Timestamps
    started_at = Column(DateTime, default=func.now())
    last_meeting = Column(DateTime)
    ended_at = Column(DateTime)
    next_meeting = Column(DateTime)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'mentor_id': self.mentor_id,
            'student_id': self.student_id,
            'mentorship_type': self.mentorship_type,
            'mentorship_title': self.mentorship_title,
            'mentorship_description': self.mentorship_description,
            'primary_goals': self.primary_goals or [],
            'secondary_goals': self.secondary_goals or [],
            'success_metrics': self.success_metrics or {},
            'mentorship_duration': self.mentorship_duration,
            'meeting_frequency': self.meeting_frequency,
            'meeting_duration': self.meeting_duration,
            'total_sessions': self.total_sessions,
            'status': self.status,
            'progress_percentage': self.progress_percentage,
            'sessions_completed': self.sessions_completed,
            'goals_achieved': self.goals_achieved,
            'communication_method': self.communication_method,
            'meeting_platform': self.meeting_platform,
            'shared_resources': self.shared_resources or [],
            'mentor_rating': self.mentor_rating,
            'student_rating': self.student_rating,
            'overall_satisfaction': self.overall_satisfaction,
            'feedback_exchanged': self.feedback_exchanged or [],
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'last_meeting': self.last_meeting.isoformat() if self.last_meeting else None,
            'ended_at': self.ended_at.isoformat() if self.ended_at else None,
            'next_meeting': self.next_meeting.isoformat() if self.next_meeting else None
        }

class MentorshipSession(Base):
    """Individual mentorship session model"""
    __tablename__ = 'mentorship_sessions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    mentorship_id = Column(Integer, nullable=False)
    session_number = Column(Integer, nullable=False)
    
    # Session Details
    session_type = Column(String(50))  # 'introduction', 'goal_setting', 'progress_review', 'skill_focus'
    session_title = Column(String(200))
    session_description = Column(Text)
    
    # Session Content
    agenda = Column(JSON)  # Session agenda
    topics_covered = Column(JSON)  # Topics discussed
    action_items = Column(JSON)  # Action items from session
    resources_shared = Column(JSON)  # Resources shared during session
    
    # Session Logistics
    scheduled_at = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer)
    meeting_platform = Column(String(100))
    meeting_link = Column(String(500))
    
    # Session Status
    status = Column(String(50), default='scheduled')  # 'scheduled', 'completed', 'cancelled', 'rescheduled'
    actual_start_time = Column(DateTime)
    actual_end_time = Column(DateTime)
    actual_duration = Column(Integer)  # Actual duration in minutes
    
    # Session Outcomes
    goals_discussed = Column(JSON)  # Goals discussed in session
    progress_made = Column(JSON)  # Progress made during session
    challenges_identified = Column(JSON)  # Challenges identified
    next_steps = Column(JSON)  # Next steps planned
    
    # Feedback and Evaluation
    mentor_feedback = Column(Text)  # Mentor's feedback on session
    student_feedback = Column(Text)  # Student's feedback on session
    mentor_rating = Column(Integer)  # Mentor's rating of session (1-5)
    student_rating = Column(Integer)  # Student's rating of session (1-5)
    
    # Follow-up
    follow_up_required = Column(Boolean, default=False)
    follow_up_notes = Column(Text)
    next_session_scheduled = Column(DateTime)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'mentorship_id': self.mentorship_id,
            'session_number': self.session_number,
            'session_type': self.session_type,
            'session_title': self.session_title,
            'session_description': self.session_description,
            'agenda': self.agenda or [],
            'topics_covered': self.topics_covered or [],
            'action_items': self.action_items or [],
            'resources_shared': self.resources_shared or [],
            'scheduled_at': self.scheduled_at.isoformat() if self.scheduled_at else None,
            'duration_minutes': self.duration_minutes,
            'meeting_platform': self.meeting_platform,
            'meeting_link': self.meeting_link,
            'status': self.status,
            'actual_start_time': self.actual_start_time.isoformat() if self.actual_start_time else None,
            'actual_end_time': self.actual_end_time.isoformat() if self.actual_end_time else None,
            'actual_duration': self.actual_duration,
            'goals_discussed': self.goals_discussed or [],
            'progress_made': self.progress_made or [],
            'challenges_identified': self.challenges_identified or [],
            'next_steps': self.next_steps or [],
            'mentor_feedback': self.mentor_feedback,
            'student_feedback': self.student_feedback,
            'mentor_rating': self.mentor_rating,
            'student_rating': self.student_rating,
            'follow_up_required': self.follow_up_required,
            'follow_up_notes': self.follow_up_notes,
            'next_session_scheduled': self.next_session_scheduled.isoformat() if self.next_session_scheduled else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class MentorFeedback(Base):
    """Mentor feedback model"""
    __tablename__ = 'mentor_feedback'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    mentor_id = Column(Integer, nullable=False)
    student_id = Column(Integer, nullable=False)
    mentorship_id = Column(Integer, nullable=False)
    
    # Feedback Details
    feedback_type = Column(String(50))  # 'session', 'mentorship', 'mentor', 'general'
    feedback_category = Column(String(50))  # 'positive', 'negative', 'suggestion', 'complaint'
    feedback_text = Column(Text, nullable=False)
    
    # Ratings
    overall_rating = Column(Integer, nullable=False)  # 1-5 scale
    communication_rating = Column(Integer)  # 1-5 scale
    helpfulness_rating = Column(Integer)  # 1-5 scale
    professionalism_rating = Column(Integer)  # 1-5 scale
    knowledge_rating = Column(Integer)  # 1-5 scale
    
    # Specific Feedback Areas
    strengths = Column(JSON)  # What the mentor did well
    areas_for_improvement = Column(JSON)  # Areas for improvement
    suggestions = Column(JSON)  # Suggestions for improvement
    
    # Impact and Outcomes
    impact_on_career = Column(String(100))  # Impact on student's career
    goals_achieved = Column(JSON)  # Goals achieved through mentorship
    skills_developed = Column(JSON)  # Skills developed through mentorship
    
    # Recommendation
    would_recommend = Column(Boolean)  # Would recommend this mentor
    recommendation_reason = Column(Text)  # Reason for recommendation
    
    # Metadata
    is_anonymous = Column(Boolean, default=False)
    is_public = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'mentor_id': self.mentor_id,
            'student_id': self.student_id,
            'mentorship_id': self.mentorship_id,
            'feedback_type': self.feedback_type,
            'feedback_category': self.feedback_category,
            'feedback_text': self.feedback_text,
            'ratings': {
                'overall': self.overall_rating,
                'communication': self.communication_rating,
                'helpfulness': self.helpfulness_rating,
                'professionalism': self.professionalism_rating,
                'knowledge': self.knowledge_rating
            },
            'strengths': self.strengths or [],
            'areas_for_improvement': self.areas_for_improvement or [],
            'suggestions': self.suggestions or [],
            'impact_on_career': self.impact_on_career,
            'goals_achieved': self.goals_achieved or [],
            'skills_developed': self.skills_developed or [],
            'would_recommend': self.would_recommend,
            'recommendation_reason': self.recommendation_reason,
            'is_anonymous': self.is_anonymous,
            'is_public': self.is_public,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
