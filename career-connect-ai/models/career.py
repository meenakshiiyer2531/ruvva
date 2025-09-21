"""
Career information models
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime
from typing import Dict, List, Any, Optional

Base = declarative_base()

class Career(Base):
    """Career information model"""
    __tablename__ = 'careers'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    
    # Basic Information
    category = Column(String(100))
    industry = Column(String(100))
    job_level = Column(String(50))  # 'entry', 'mid', 'senior', 'executive'
    
    # Requirements
    education_requirements = Column(String(100))
    experience_required = Column(String(100))
    required_skills = Column(JSON)  # List of required skills
    preferred_skills = Column(JSON)  # List of preferred skills
    certifications = Column(JSON)  # List of certifications
    
    # Compensation
    salary_min = Column(Integer)
    salary_max = Column(Integer)
    salary_median = Column(Integer)
    salary_currency = Column(String(10), default='USD')
    benefits = Column(JSON)  # List of benefits
    
    # Work Environment
    workplace_type = Column(String(50))  # 'office', 'remote', 'hybrid', 'field'
    work_schedule = Column(String(50))  # 'full-time', 'part-time', 'contract'
    travel_required = Column(Boolean, default=False)
    remote_possible = Column(Boolean, default=False)
    
    # Career Path
    entry_level_positions = Column(JSON)
    mid_level_positions = Column(JSON)
    senior_level_positions = Column(JSON)
    advancement_opportunities = Column(JSON)
    
    # Market Information
    demand_level = Column(String(50))  # 'low', 'medium', 'high'
    growth_rate = Column(String(50))  # 'declining', 'stable', 'growing', 'high_growth'
    competition_level = Column(String(50))  # 'low', 'medium', 'high'
    job_security = Column(String(50))  # 'low', 'medium', 'high'
    
    # RIASEC Requirements
    riasec_requirements = Column(JSON)  # RIASEC scores for this career
    
    # Additional Information
    technology_impact = Column(String(50))  # 'low', 'moderate', 'high'
    automation_risk = Column(String(50))  # 'low', 'medium', 'high'
    future_outlook = Column(String(50))  # 'positive', 'neutral', 'negative'
    
    # Metadata
    is_active = Column(Boolean, default=True)
    last_updated = Column(DateTime, default=func.now())
    created_at = Column(DateTime, default=func.now())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'industry': self.industry,
            'job_level': self.job_level,
            'education_requirements': self.education_requirements,
            'experience_required': self.experience_required,
            'required_skills': self.required_skills or [],
            'preferred_skills': self.preferred_skills or [],
            'certifications': self.certifications or [],
            'salary': {
                'min': self.salary_min,
                'max': self.salary_max,
                'median': self.salary_median,
                'currency': self.salary_currency
            },
            'benefits': self.benefits or [],
            'workplace_type': self.workplace_type,
            'work_schedule': self.work_schedule,
            'travel_required': self.travel_required,
            'remote_possible': self.remote_possible,
            'entry_level_positions': self.entry_level_positions or [],
            'mid_level_positions': self.mid_level_positions or [],
            'senior_level_positions': self.senior_level_positions or [],
            'advancement_opportunities': self.advancement_opportunities or [],
            'demand_level': self.demand_level,
            'growth_rate': self.growth_rate,
            'competition_level': self.competition_level,
            'job_security': self.job_security,
            'riasec_requirements': self.riasec_requirements or {},
            'technology_impact': self.technology_impact,
            'automation_risk': self.automation_risk,
            'future_outlook': self.future_outlook,
            'is_active': self.is_active,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class CareerRecommendation(Base):
    """Career recommendation model"""
    __tablename__ = 'career_recommendations'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, nullable=False)
    career_id = Column(Integer, nullable=False)
    
    # Recommendation Details
    match_score = Column(Float, nullable=False)
    recommendation_type = Column(String(50))  # 'primary', 'secondary', 'alternative'
    recommendation_reason = Column(Text)
    
    # Analysis Results
    compatibility_factors = Column(JSON)  # Detailed compatibility analysis
    skill_gaps = Column(JSON)  # Identified skill gaps
    strengths = Column(JSON)  # Student strengths for this career
    development_areas = Column(JSON)  # Areas for development
    
    # Recommendations
    learning_recommendations = Column(JSON)
    skill_development_plan = Column(JSON)
    career_transition_strategy = Column(JSON)
    
    # Status
    is_viewed = Column(Boolean, default=False)
    is_saved = Column(Boolean, default=False)
    is_applied = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    last_updated = Column(DateTime, default=func.now())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'student_id': self.student_id,
            'career_id': self.career_id,
            'match_score': self.match_score,
            'recommendation_type': self.recommendation_type,
            'recommendation_reason': self.recommendation_reason,
            'compatibility_factors': self.compatibility_factors or {},
            'skill_gaps': self.skill_gaps or [],
            'strengths': self.strengths or [],
            'development_areas': self.development_areas or [],
            'learning_recommendations': self.learning_recommendations or {},
            'skill_development_plan': self.skill_development_plan or {},
            'career_transition_strategy': self.career_transition_strategy or {},
            'is_viewed': self.is_viewed,
            'is_saved': self.is_saved,
            'is_applied': self.is_applied,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None
        }

class CareerTrend(Base):
    """Career trend and market data model"""
    __tablename__ = 'career_trends'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    career_id = Column(Integer, nullable=False)
    
    # Trend Data
    trend_period = Column(String(50))  # 'monthly', 'quarterly', 'yearly'
    trend_date = Column(DateTime, nullable=False)
    
    # Market Metrics
    job_postings_count = Column(Integer)
    salary_trend = Column(String(50))  # 'increasing', 'stable', 'decreasing'
    demand_trend = Column(String(50))  # 'increasing', 'stable', 'decreasing'
    competition_trend = Column(String(50))  # 'increasing', 'stable', 'decreasing'
    
    # Industry Insights
    industry_growth_rate = Column(Float)
    technology_adoption_rate = Column(Float)
    remote_work_percentage = Column(Float)
    
    # Skills Trends
    emerging_skills = Column(JSON)
    declining_skills = Column(JSON)
    in_demand_skills = Column(JSON)
    
    # Geographic Data
    top_locations = Column(JSON)
    salary_by_location = Column(JSON)
    
    # Metadata
    data_source = Column(String(100))
    confidence_score = Column(Float)
    created_at = Column(DateTime, default=func.now())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'career_id': self.career_id,
            'trend_period': self.trend_period,
            'trend_date': self.trend_date.isoformat() if self.trend_date else None,
            'job_postings_count': self.job_postings_count,
            'salary_trend': self.salary_trend,
            'demand_trend': self.demand_trend,
            'competition_trend': self.competition_trend,
            'industry_growth_rate': self.industry_growth_rate,
            'technology_adoption_rate': self.technology_adoption_rate,
            'remote_work_percentage': self.remote_work_percentage,
            'emerging_skills': self.emerging_skills or [],
            'declining_skills': self.declining_skills or [],
            'in_demand_skills': self.in_demand_skills or [],
            'top_locations': self.top_locations or [],
            'salary_by_location': self.salary_by_location or {},
            'data_source': self.data_source,
            'confidence_score': self.confidence_score,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class CareerPath(Base):
    """Career path and progression model"""
    __tablename__ = 'career_paths'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    career_id = Column(Integer, nullable=False)
    
    # Path Information
    path_name = Column(String(200))
    path_description = Column(Text)
    path_type = Column(String(50))  # 'traditional', 'alternative', 'entrepreneurial'
    
    # Progression Levels
    entry_level = Column(JSON)  # Entry level requirements and positions
    mid_level = Column(JSON)  # Mid level requirements and positions
    senior_level = Column(JSON)  # Senior level requirements and positions
    executive_level = Column(JSON)  # Executive level requirements and positions
    
    # Transition Requirements
    skill_requirements = Column(JSON)  # Skills needed for each level
    experience_requirements = Column(JSON)  # Experience needed for each level
    education_requirements = Column(JSON)  # Education needed for each level
    
    # Timeline and Milestones
    typical_timeline = Column(JSON)  # Typical time to reach each level
    key_milestones = Column(JSON)  # Key milestones in the career path
    advancement_triggers = Column(JSON)  # What triggers advancement
    
    # Alternative Paths
    alternative_paths = Column(JSON)  # Alternative career paths
    lateral_moves = Column(JSON)  # Possible lateral moves
    exit_strategies = Column(JSON)  # Exit strategies from this career
    
    # Metadata
    is_active = Column(Boolean, default=True)
    last_updated = Column(DateTime, default=func.now())
    created_at = Column(DateTime, default=func.now())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'career_id': self.career_id,
            'path_name': self.path_name,
            'path_description': self.path_description,
            'path_type': self.path_type,
            'entry_level': self.entry_level or {},
            'mid_level': self.mid_level or {},
            'senior_level': self.senior_level or {},
            'executive_level': self.executive_level or {},
            'skill_requirements': self.skill_requirements or {},
            'experience_requirements': self.experience_requirements or {},
            'education_requirements': self.education_requirements or {},
            'typical_timeline': self.typical_timeline or {},
            'key_milestones': self.key_milestones or [],
            'advancement_triggers': self.advancement_triggers or [],
            'alternative_paths': self.alternative_paths or [],
            'lateral_moves': self.lateral_moves or [],
            'exit_strategies': self.exit_strategies or [],
            'is_active': self.is_active,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
