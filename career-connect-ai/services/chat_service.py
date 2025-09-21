"""
AI chat service for career counseling
"""

from typing import Dict, List, Any, Optional
import json
import logging
from utils.logger import get_logger
from core.gemini_client import GeminiClient
from core.conversation_manager import ConversationManager

logger = get_logger(__name__)

class ChatService:
    """Service for AI-powered career counseling chat"""
    
    def __init__(self):
        """Initialize chat service"""
        self.gemini_client = GeminiClient()
        self.conversation_manager = ConversationManager()
        
    def process_chat_message(self, 
                           message: str, 
                           session_id: str,
                           student_profile: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process chat message and generate response"""
        try:
            # Get session context
            session_context = self.conversation_manager.get_session_context(session_id)
            
            # Add user message to conversation
            self.conversation_manager.add_message(session_id, message, 'user')
            
            # Generate AI response
            ai_response = self._generate_ai_response(message, session_context)
            
            # Add AI response to conversation
            self.conversation_manager.add_message(session_id, ai_response, 'assistant')
            
            # Update context based on conversation
            self._update_conversation_context(session_id, message, ai_response)
            
            # Generate response data
            response_data = {
                'session_id': session_id,
                'user_message': message,
                'ai_response': ai_response,
                'conversation_context': session_context,
                'suggestions': self._generate_response_suggestions(ai_response),
                'next_steps': self._suggest_next_steps(session_context)
            }
            
            return response_data
        except Exception as e:
            logger.error(f"Error processing chat message: {str(e)}")
            raise
    
    def create_chat_session(self, 
                          student_profile: Dict[str, Any], 
                          initial_context: Optional[Dict[str, Any]] = None) -> str:
        """Create new chat session"""
        try:
            session_id = self.conversation_manager.create_session(student_profile, initial_context)
            
            # Send welcome message
            welcome_message = self._generate_welcome_message(student_profile)
            self.conversation_manager.add_message(session_id, welcome_message, 'assistant')
            
            return session_id
        except Exception as e:
            logger.error(f"Error creating chat session: {str(e)}")
            raise
    
    def get_chat_history(self, 
                        session_id: str, 
                        limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get chat history for session"""
        try:
            return self.conversation_manager.get_conversation_history(session_id, limit)
        except Exception as e:
            logger.error(f"Error getting chat history: {str(e)}")
            raise
    
    def end_chat_session(self, 
                        session_id: str, 
                        feedback: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """End chat session with feedback"""
        try:
            session_summary = self.conversation_manager.end_session(session_id, feedback)
            
            # Generate session insights
            insights = self._generate_session_insights(session_summary)
            
            return {
                'session_summary': session_summary,
                'insights': insights,
                'recommendations': self._generate_session_recommendations(session_summary)
            }
        except Exception as e:
            logger.error(f"Error ending chat session: {str(e)}")
            raise
    
    def analyze_conversation_sentiment(self, 
                                     session_id: str) -> Dict[str, Any]:
        """Analyze conversation sentiment and engagement"""
        try:
            conversation_history = self.conversation_manager.get_conversation_history(session_id)
            
            sentiment_analysis = {
                'overall_sentiment': 'positive',
                'engagement_level': 'high',
                'conversation_flow': 'smooth',
                'key_topics': [],
                'student_needs': [],
                'recommendations': []
            }
            
            # Analyze user messages for sentiment
            user_messages = [msg for msg in conversation_history if msg['sender'] == 'user']
            
            if user_messages:
                sentiment_analysis['overall_sentiment'] = self._analyze_message_sentiment(user_messages)
                sentiment_analysis['engagement_level'] = self._assess_engagement_level(user_messages)
                sentiment_analysis['key_topics'] = self._extract_key_topics(user_messages)
                sentiment_analysis['student_needs'] = self._identify_student_needs(user_messages)
            
            # Generate recommendations based on analysis
            sentiment_analysis['recommendations'] = self._generate_sentiment_recommendations(sentiment_analysis)
            
            return sentiment_analysis
        except Exception as e:
            logger.error(f"Error analyzing conversation sentiment: {str(e)}")
            raise
    
    def generate_conversation_summary(self, session_id: str) -> Dict[str, Any]:
        """Generate comprehensive conversation summary"""
        try:
            conversation_history = self.conversation_manager.get_conversation_history(session_id)
            session_context = self.conversation_manager.get_session_context(session_id)
            
            summary = {
                'session_overview': {},
                'key_conversations': [],
                'topics_discussed': [],
                'recommendations_given': [],
                'student_insights': {},
                'next_steps': []
            }
            
            # Generate session overview
            summary['session_overview'] = self._generate_session_overview(conversation_history, session_context)
            
            # Extract key conversations
            summary['key_conversations'] = self._extract_key_conversations(conversation_history)
            
            # Identify topics discussed
            summary['topics_discussed'] = session_context.get('topics_discussed', [])
            
            # Get recommendations given
            summary['recommendations_given'] = session_context.get('recommendations_given', [])
            
            # Generate student insights
            summary['student_insights'] = self._generate_student_insights(conversation_history, session_context)
            
            # Suggest next steps
            summary['next_steps'] = self._suggest_conversation_next_steps(summary)
            
            return summary
        except Exception as e:
            logger.error(f"Error generating conversation summary: {str(e)}")
            raise
    
    def _generate_ai_response(self, 
                            message: str, 
                            session_context: Dict[str, Any]) -> str:
        """Generate AI response using Gemini"""
        try:
            response = self.gemini_client.chat_with_counselor(message, session_context)
            return response
        except Exception as e:
            logger.error(f"Error generating AI response: {str(e)}")
            return "I apologize, but I'm having trouble processing your message right now. Please try again."
    
    def _update_conversation_context(self, 
                                   session_id: str, 
                                   user_message: str, 
                                   ai_response: str) -> None:
        """Update conversation context based on messages"""
        try:
            # Extract topics from messages
            topics = self._extract_topics_from_messages([user_message, ai_response])
            for topic in topics:
                self.conversation_manager.add_topic(session_id, topic)
            
            # Update context based on message content
            context_updates = {}
            
            if 'career' in user_message.lower():
                context_updates['career_discussed'] = True
            
            if 'assessment' in user_message.lower():
                context_updates['assessment_discussed'] = True
            
            if 'learning' in user_message.lower() or 'skill' in user_message.lower():
                context_updates['learning_discussed'] = True
            
            if 'mentor' in user_message.lower():
                context_updates['mentorship_discussed'] = True
            
            if context_updates:
                self.conversation_manager.update_context(session_id, context_updates)
                
        except Exception as e:
            logger.error(f"Error updating conversation context: {str(e)}")
    
    def _generate_response_suggestions(self, ai_response: str) -> List[str]:
        """Generate follow-up suggestions based on AI response"""
        suggestions = []
        
        response_lower = ai_response.lower()
        
        if 'career' in response_lower:
            suggestions.extend([
                "Tell me more about career options",
                "What skills do I need to develop?",
                "How do I choose the right career?"
            ])
        
        if 'assessment' in response_lower:
            suggestions.extend([
                "Take a personality assessment",
                "Complete a skills assessment",
                "What do assessments tell me?"
            ])
        
        if 'learning' in response_lower or 'skill' in response_lower:
            suggestions.extend([
                "Create a learning plan",
                "Find learning resources",
                "Track my progress"
            ])
        
        if 'mentor' in response_lower:
            suggestions.extend([
                "Find a mentor",
                "What should I look for in a mentor?",
                "How do I approach potential mentors?"
            ])
        
        # Default suggestions
        if not suggestions:
            suggestions.extend([
                "What are my next steps?",
                "How can I improve my career prospects?",
                "What resources do you recommend?"
            ])
        
        return suggestions[:3]  # Return top 3 suggestions
    
    def _suggest_next_steps(self, session_context: Dict[str, Any]) -> List[str]:
        """Suggest next steps based on session context"""
        next_steps = []
        
        context = session_context.get('context', {})
        
        if context.get('career_discussed'):
            next_steps.append("Research specific careers mentioned")
        
        if context.get('assessment_discussed'):
            next_steps.append("Complete recommended assessments")
        
        if context.get('learning_discussed'):
            next_steps.append("Create a learning plan")
        
        if context.get('mentorship_discussed'):
            next_steps.append("Find a suitable mentor")
        
        # Default next steps
        if not next_steps:
            next_steps.extend([
                "Continue exploring career options",
                "Take personality assessments",
                "Develop relevant skills"
            ])
        
        return next_steps
    
    def _generate_welcome_message(self, student_profile: Dict[str, Any]) -> str:
        """Generate personalized welcome message"""
        name = student_profile.get('name', 'there')
        interests = student_profile.get('interests', [])
        
        welcome = f"Hello {name}! I'm your AI career counselor. I'm here to help you explore career options, develop your skills, and plan your professional future."
        
        if interests:
            welcome += f" I see you're interested in {', '.join(interests[:3])}. That's a great starting point for our conversation!"
        
        welcome += " What would you like to explore today? You can ask me about career options, take assessments, get learning recommendations, or find mentors."
        
        return welcome
    
    def _generate_session_insights(self, session_summary: Dict[str, Any]) -> Dict[str, Any]:
        """Generate insights from session summary"""
        return {
            'conversation_quality': 'engaging',
            'topics_coverage': 'comprehensive',
            'student_engagement': 'high',
            'key_insights': [
                "Student shows strong interest in technology careers",
                "Good foundation of soft skills",
                "Ready for skill development"
            ],
            'areas_for_improvement': [
                "Complete personality assessment",
                "Define specific career goals"
            ]
        }
    
    def _generate_session_recommendations(self, session_summary: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on session"""
        recommendations = []
        
        topics_discussed = session_summary.get('topics_discussed', [])
        
        if 'career_planning' in topics_discussed:
            recommendations.append("Continue career exploration with specific research")
        
        if 'assessment' in topics_discussed:
            recommendations.append("Complete recommended assessments")
        
        if 'learning' in topics_discussed:
            recommendations.append("Create a structured learning plan")
        
        if 'mentorship' in topics_discussed:
            recommendations.append("Begin mentor search process")
        
        return recommendations
    
    def _analyze_message_sentiment(self, user_messages: List[Dict[str, Any]]) -> str:
        """Analyze sentiment of user messages"""
        positive_keywords = ['great', 'excellent', 'helpful', 'thank', 'love', 'excited']
        negative_keywords = ['difficult', 'hard', 'confused', 'frustrated', 'worried', 'concerned']
        
        positive_count = 0
        negative_count = 0
        
        for message in user_messages:
            content = message['content'].lower()
            positive_count += sum(1 for keyword in positive_keywords if keyword in content)
            negative_count += sum(1 for keyword in negative_keywords if keyword in content)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
    
    def _assess_engagement_level(self, user_messages: List[Dict[str, Any]]) -> str:
        """Assess student engagement level"""
        if len(user_messages) >= 10:
            return 'high'
        elif len(user_messages) >= 5:
            return 'medium'
        else:
            return 'low'
    
    def _extract_key_topics(self, user_messages: List[Dict[str, Any]]) -> List[str]:
        """Extract key topics from user messages"""
        topics = []
        
        for message in user_messages:
            content = message['content'].lower()
            
            if 'career' in content:
                topics.append('career_planning')
            if 'skill' in content:
                topics.append('skill_development')
            if 'assessment' in content:
                topics.append('assessment')
            if 'learning' in content:
                topics.append('learning')
            if 'mentor' in content:
                topics.append('mentorship')
        
        return list(set(topics))
    
    def _identify_student_needs(self, user_messages: List[Dict[str, Any]]) -> List[str]:
        """Identify student needs from messages"""
        needs = []
        
        for message in user_messages:
            content = message['content'].lower()
            
            if 'help' in content or 'guidance' in content:
                needs.append('guidance')
            if 'confused' in content or 'unclear' in content:
                needs.append('clarity')
            if 'skill' in content or 'learn' in content:
                needs.append('skill_development')
            if 'career' in content or 'job' in content:
                needs.append('career_guidance')
        
        return list(set(needs))
    
    def _generate_sentiment_recommendations(self, sentiment_analysis: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on sentiment analysis"""
        recommendations = []
        
        sentiment = sentiment_analysis.get('overall_sentiment', 'neutral')
        engagement = sentiment_analysis.get('engagement_level', 'medium')
        
        if sentiment == 'negative':
            recommendations.append("Provide additional support and encouragement")
        
        if engagement == 'low':
            recommendations.append("Increase engagement with interactive content")
        
        if 'guidance' in sentiment_analysis.get('student_needs', []):
            recommendations.append("Offer more structured guidance")
        
        return recommendations
    
    def _generate_session_overview(self, 
                                 conversation_history: List[Dict[str, Any]], 
                                 session_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate session overview"""
        return {
            'total_messages': len(conversation_history),
            'session_duration': session_context.get('session_metadata', {}).get('duration', 'Unknown'),
            'topics_covered': len(session_context.get('topics_discussed', [])),
            'recommendations_given': len(session_context.get('recommendations_given', [])),
            'student_profile': session_context.get('student_profile', {}).get('name', 'Student')
        }
    
    def _extract_key_conversations(self, conversation_history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract key conversations from history"""
        key_conversations = []
        
        # Find conversations with significant exchanges
        for i in range(len(conversation_history) - 1):
            current_msg = conversation_history[i]
            next_msg = conversation_history[i + 1]
            
            if (current_msg['sender'] == 'user' and next_msg['sender'] == 'assistant' and
                len(current_msg['content']) > 50 and len(next_msg['content']) > 100):
                
                key_conversations.append({
                    'user_message': current_msg['content'][:100] + "...",
                    'ai_response': next_msg['content'][:150] + "...",
                    'timestamp': current_msg['timestamp']
                })
        
        return key_conversations[:5]  # Top 5 key conversations
    
    def _generate_student_insights(self, 
                                 conversation_history: List[Dict[str, Any]], 
                                 session_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate insights about the student"""
        user_messages = [msg for msg in conversation_history if msg['sender'] == 'user']
        
        insights = {
            'communication_style': 'professional',
            'engagement_level': 'high' if len(user_messages) > 5 else 'medium',
            'primary_concerns': [],
            'interests_expressed': [],
            'goals_mentioned': []
        }
        
        # Analyze user messages for insights
        for message in user_messages:
            content = message['content'].lower()
            
            if 'career' in content:
                insights['primary_concerns'].append('career_planning')
            if 'skill' in content:
                insights['primary_concerns'].append('skill_development')
            if 'confused' in content:
                insights['primary_concerns'].append('clarity_needed')
            
            # Extract interests and goals (simplified)
            if 'interested' in content:
                insights['interests_expressed'].append('general_interest')
            if 'goal' in content:
                insights['goals_mentioned'].append('goal_setting')
        
        return insights
    
    def _suggest_conversation_next_steps(self, summary: Dict[str, Any]) -> List[str]:
        """Suggest next steps based on conversation summary"""
        next_steps = []
        
        topics_discussed = summary.get('topics_discussed', [])
        student_insights = summary.get('student_insights', {})
        
        if 'career_planning' in topics_discussed:
            next_steps.append("Research specific career options")
        
        if 'skill_development' in topics_discussed:
            next_steps.append("Create a skill development plan")
        
        if 'assessment' in topics_discussed:
            next_steps.append("Complete recommended assessments")
        
        if 'clarity_needed' in student_insights.get('primary_concerns', []):
            next_steps.append("Schedule follow-up session for clarification")
        
        return next_steps
    
    def _extract_topics_from_messages(self, messages: List[str]) -> List[str]:
        """Extract topics from messages"""
        topics = []
        
        for message in messages:
            message_lower = message.lower()
            
            if 'career' in message_lower:
                topics.append('career_planning')
            if 'skill' in message_lower:
                topics.append('skill_development')
            if 'assessment' in message_lower:
                topics.append('assessment')
            if 'learning' in message_lower:
                topics.append('learning')
            if 'mentor' in message_lower:
                topics.append('mentorship')
        
        return list(set(topics))
