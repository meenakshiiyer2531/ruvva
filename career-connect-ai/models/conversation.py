"""
Conversation and chat models
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime
from typing import Dict, List, Any, Optional

Base = declarative_base()

class Conversation(Base):
    """Conversation model"""
    __tablename__ = 'conversations'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, nullable=False)
    session_id = Column(String(100), unique=True, nullable=False)
    
    # Conversation Details
    conversation_type = Column(String(50))  # 'chat', 'assessment', 'mentor', 'learning'
    title = Column(String(200))
    description = Column(Text)
    
    # Status and Progress
    status = Column(String(50), default='active')  # 'active', 'completed', 'archived'
    progress_percentage = Column(Float, default=0.0)
    
    # Context and Data
    initial_context = Column(JSON)  # Initial conversation context
    conversation_context = Column(JSON)  # Current conversation context
    topics_discussed = Column(JSON)  # Topics covered in conversation
    
    # Performance Metrics
    message_count = Column(Integer, default=0)
    user_message_count = Column(Integer, default=0)
    assistant_message_count = Column(Integer, default=0)
    average_response_time = Column(Float)  # Average response time in seconds
    
    # Quality Metrics
    engagement_score = Column(Float)  # User engagement score
    satisfaction_score = Column(Float)  # User satisfaction score
    helpfulness_score = Column(Float)  # Perceived helpfulness score
    
    # Timestamps
    started_at = Column(DateTime, default=func.now())
    last_activity = Column(DateTime, default=func.now())
    ended_at = Column(DateTime)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'student_id': self.student_id,
            'session_id': self.session_id,
            'conversation_type': self.conversation_type,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'progress_percentage': self.progress_percentage,
            'initial_context': self.initial_context or {},
            'conversation_context': self.conversation_context or {},
            'topics_discussed': self.topics_discussed or [],
            'message_count': self.message_count,
            'user_message_count': self.user_message_count,
            'assistant_message_count': self.assistant_message_count,
            'average_response_time': self.average_response_time,
            'engagement_score': self.engagement_score,
            'satisfaction_score': self.satisfaction_score,
            'helpfulness_score': self.helpfulness_score,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'last_activity': self.last_activity.isoformat() if self.last_activity else None,
            'ended_at': self.ended_at.isoformat() if self.ended_at else None
        }

class Message(Base):
    """Message model"""
    __tablename__ = 'messages'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(Integer, nullable=False)
    message_id = Column(String(100), unique=True, nullable=False)
    
    # Message Content
    sender = Column(String(50), nullable=False)  # 'user', 'assistant', 'system'
    message_type = Column(String(50), default='text')  # 'text', 'image', 'file', 'assessment'
    content = Column(Text, nullable=False)
    
    # Message Metadata
    message_order = Column(Integer)  # Order within conversation
    parent_message_id = Column(String(100))  # For threaded conversations
    reply_to_message_id = Column(String(100))  # Message being replied to
    
    # Processing Information
    processing_time = Column(Float)  # Time to process/generate response
    tokens_used = Column(Integer)  # AI tokens used for this message
    model_version = Column(String(50))  # AI model version used
    
    # Message Analysis
    sentiment = Column(String(50))  # 'positive', 'negative', 'neutral'
    intent = Column(String(100))  # Detected user intent
    entities = Column(JSON)  # Extracted entities
    topics = Column(JSON)  # Topics mentioned in message
    
    # Quality and Feedback
    helpfulness_rating = Column(Integer)  # 1-5 rating
    accuracy_rating = Column(Integer)  # 1-5 rating
    user_feedback = Column(Text)  # User feedback on message
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'conversation_id': self.conversation_id,
            'message_id': self.message_id,
            'sender': self.sender,
            'message_type': self.message_type,
            'content': self.content,
            'message_order': self.message_order,
            'parent_message_id': self.parent_message_id,
            'reply_to_message_id': self.reply_to_message_id,
            'processing_time': self.processing_time,
            'tokens_used': self.tokens_used,
            'model_version': self.model_version,
            'sentiment': self.sentiment,
            'intent': self.intent,
            'entities': self.entities or [],
            'topics': self.topics or [],
            'helpfulness_rating': self.helpfulness_rating,
            'accuracy_rating': self.accuracy_rating,
            'user_feedback': self.user_feedback,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class ConversationInsight(Base):
    """Conversation insight model"""
    __tablename__ = 'conversation_insights'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(Integer, nullable=False)
    
    # Insight Details
    insight_type = Column(String(50))  # 'sentiment', 'topic', 'intent', 'recommendation'
    insight_category = Column(String(50))  # 'positive', 'negative', 'neutral', 'actionable'
    insight_text = Column(Text)
    
    # Analysis Data
    confidence_score = Column(Float)  # Confidence in the insight
    supporting_evidence = Column(JSON)  # Evidence supporting the insight
    related_messages = Column(JSON)  # Message IDs related to this insight
    
    # Recommendations
    recommended_actions = Column(JSON)  # Actions based on insight
    follow_up_suggestions = Column(JSON)  # Suggested follow-up topics
    
    # Metadata
    generated_at = Column(DateTime, default=func.now())
    is_actionable = Column(Boolean, default=False)
    priority_level = Column(String(50))  # 'low', 'medium', 'high'
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'conversation_id': self.conversation_id,
            'insight_type': self.insight_type,
            'insight_category': self.insight_category,
            'insight_text': self.insight_text,
            'confidence_score': self.confidence_score,
            'supporting_evidence': self.supporting_evidence or [],
            'related_messages': self.related_messages or [],
            'recommended_actions': self.recommended_actions or [],
            'follow_up_suggestions': self.follow_up_suggestions or [],
            'generated_at': self.generated_at.isoformat() if self.generated_at else None,
            'is_actionable': self.is_actionable,
            'priority_level': self.priority_level
        }

class ConversationRecommendation(Base):
    """Conversation recommendation model"""
    __tablename__ = 'conversation_recommendations'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(Integer, nullable=False)
    
    # Recommendation Details
    recommendation_type = Column(String(50))  # 'career', 'learning', 'assessment', 'mentor'
    recommendation_category = Column(String(50))  # 'immediate', 'short_term', 'long_term'
    recommendation_text = Column(Text)
    
    # Recommendation Data
    recommendation_data = Column(JSON)  # Structured recommendation data
    target_careers = Column(JSON)  # Recommended careers
    learning_resources = Column(JSON)  # Recommended learning resources
    skill_development = Column(JSON)  # Skill development recommendations
    
    # Context and Reasoning
    reasoning = Column(Text)  # Why this recommendation was made
    supporting_evidence = Column(JSON)  # Evidence supporting the recommendation
    confidence_score = Column(Float)  # Confidence in the recommendation
    
    # User Interaction
    is_viewed = Column(Boolean, default=False)
    is_accepted = Column(Boolean, default=False)
    is_implemented = Column(Boolean, default=False)
    user_feedback = Column(Text)
    user_rating = Column(Integer)  # 1-5 rating
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    last_updated = Column(DateTime, default=func.now())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'conversation_id': self.conversation_id,
            'recommendation_type': self.recommendation_type,
            'recommendation_category': self.recommendation_category,
            'recommendation_text': self.recommendation_text,
            'recommendation_data': self.recommendation_data or {},
            'target_careers': self.target_careers or [],
            'learning_resources': self.learning_resources or [],
            'skill_development': self.skill_development or [],
            'reasoning': self.reasoning,
            'supporting_evidence': self.supporting_evidence or [],
            'confidence_score': self.confidence_score,
            'is_viewed': self.is_viewed,
            'is_accepted': self.is_accepted,
            'is_implemented': self.is_implemented,
            'user_feedback': self.user_feedback,
            'user_rating': self.user_rating,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None
        }

class ConversationAnalytics(Base):
    """Conversation analytics model"""
    __tablename__ = 'conversation_analytics'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(Integer, nullable=False)
    
    # Analytics Period
    analytics_period = Column(String(50))  # 'session', 'daily', 'weekly', 'monthly'
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    
    # Engagement Metrics
    total_messages = Column(Integer)
    user_messages = Column(Integer)
    assistant_messages = Column(Integer)
    average_message_length = Column(Float)
    response_time_avg = Column(Float)
    response_time_median = Column(Float)
    
    # Quality Metrics
    user_satisfaction_avg = Column(Float)
    helpfulness_avg = Column(Float)
    accuracy_avg = Column(Float)
    engagement_score = Column(Float)
    
    # Topic Analysis
    topics_covered = Column(JSON)
    topic_frequency = Column(JSON)
    topic_engagement = Column(JSON)
    
    # Sentiment Analysis
    overall_sentiment = Column(String(50))
    sentiment_distribution = Column(JSON)
    sentiment_trend = Column(JSON)
    
    # Recommendations
    recommendations_given = Column(Integer)
    recommendations_accepted = Column(Integer)
    recommendations_implemented = Column(Integer)
    recommendation_success_rate = Column(Float)
    
    # Metadata
    generated_at = Column(DateTime, default=func.now())
    data_quality_score = Column(Float)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'conversation_id': self.conversation_id,
            'analytics_period': self.analytics_period,
            'period_start': self.period_start.isoformat() if self.period_start else None,
            'period_end': self.period_end.isoformat() if self.period_end else None,
            'engagement_metrics': {
                'total_messages': self.total_messages,
                'user_messages': self.user_messages,
                'assistant_messages': self.assistant_messages,
                'average_message_length': self.average_message_length,
                'response_time_avg': self.response_time_avg,
                'response_time_median': self.response_time_median
            },
            'quality_metrics': {
                'user_satisfaction_avg': self.user_satisfaction_avg,
                'helpfulness_avg': self.helpfulness_avg,
                'accuracy_avg': self.accuracy_avg,
                'engagement_score': self.engagement_score
            },
            'topic_analysis': {
                'topics_covered': self.topics_covered or [],
                'topic_frequency': self.topic_frequency or {},
                'topic_engagement': self.topic_engagement or {}
            },
            'sentiment_analysis': {
                'overall_sentiment': self.overall_sentiment,
                'sentiment_distribution': self.sentiment_distribution or {},
                'sentiment_trend': self.sentiment_trend or {}
            },
            'recommendations': {
                'recommendations_given': self.recommendations_given,
                'recommendations_accepted': self.recommendations_accepted,
                'recommendations_implemented': self.recommendations_implemented,
                'recommendation_success_rate': self.recommendation_success_rate
            },
            'generated_at': self.generated_at.isoformat() if self.generated_at else None,
            'data_quality_score': self.data_quality_score
        }
