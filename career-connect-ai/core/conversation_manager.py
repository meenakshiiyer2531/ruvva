"""
Chat conversation context management
"""

from typing import Dict, List, Any, Optional
import json
import uuid
from datetime import datetime, timedelta
import logging
from utils.logger import get_logger

logger = get_logger(__name__)

class ConversationManager:
    """Manages chat conversation context and history"""
    
    def __init__(self):
        """Initialize conversation manager"""
        self.active_sessions = {}
        self.conversation_history = {}
        
    def create_session(self, 
                      student_profile: Dict[str, Any], 
                      initial_context: Optional[Dict[str, Any]] = None) -> str:
        """Create a new conversation session"""
        try:
            session_id = str(uuid.uuid4())
            
            session_data = {
                'session_id': session_id,
                'created_at': datetime.now().isoformat(),
                'last_activity': datetime.now().isoformat(),
                'student_profile': student_profile,
                'context': initial_context or {},
                'messages': [],
                'topics_discussed': [],
                'recommendations_given': [],
                'session_metadata': {
                    'message_count': 0,
                    'avg_response_time': 0,
                    'user_satisfaction': None
                }
            }
            
            self.active_sessions[session_id] = session_data
            self.conversation_history[session_id] = []
            
            logger.info(f"Created new conversation session: {session_id}")
            return session_id
        except Exception as e:
            logger.error(f"Error creating conversation session: {str(e)}")
            raise
    
    def add_message(self, 
                   session_id: str, 
                   message: str, 
                   sender: str, 
                   message_type: str = 'text') -> Dict[str, Any]:
        """Add a message to the conversation"""
        try:
            if session_id not in self.active_sessions:
                raise ValueError(f"Session {session_id} not found")
            
            message_data = {
                'message_id': str(uuid.uuid4()),
                'timestamp': datetime.now().isoformat(),
                'sender': sender,  # 'user' or 'assistant'
                'message_type': message_type,
                'content': message,
                'metadata': {}
            }
            
            # Add to active session
            self.active_sessions[session_id]['messages'].append(message_data)
            self.active_sessions[session_id]['last_activity'] = datetime.now().isoformat()
            self.active_sessions[session_id]['session_metadata']['message_count'] += 1
            
            # Add to history
            self.conversation_history[session_id].append(message_data)
            
            # Update context based on message
            self._update_context(session_id, message_data)
            
            logger.info(f"Added message to session {session_id}")
            return message_data
        except Exception as e:
            logger.error(f"Error adding message: {str(e)}")
            raise
    
    def get_session_context(self, session_id: str) -> Dict[str, Any]:
        """Get current session context"""
        try:
            if session_id not in self.active_sessions:
                raise ValueError(f"Session {session_id} not found")
            
            session = self.active_sessions[session_id]
            
            return {
                'session_id': session_id,
                'student_profile': session['student_profile'],
                'context': session['context'],
                'recent_messages': session['messages'][-10:],  # Last 10 messages
                'topics_discussed': session['topics_discussed'],
                'recommendations_given': session['recommendations_given'],
                'session_metadata': session['session_metadata']
            }
        except Exception as e:
            logger.error(f"Error getting session context: {str(e)}")
            raise
    
    def get_conversation_history(self, 
                               session_id: str, 
                               limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get conversation history"""
        try:
            if session_id not in self.conversation_history:
                raise ValueError(f"Session {session_id} not found")
            
            history = self.conversation_history[session_id]
            
            if limit:
                return history[-limit:]
            
            return history
        except Exception as e:
            logger.error(f"Error getting conversation history: {str(e)}")
            raise
    
    def update_context(self, 
                      session_id: str, 
                      context_updates: Dict[str, Any]) -> None:
        """Update session context"""
        try:
            if session_id not in self.active_sessions:
                raise ValueError(f"Session {session_id} not found")
            
            self.active_sessions[session_id]['context'].update(context_updates)
            self.active_sessions[session_id]['last_activity'] = datetime.now().isoformat()
            
            logger.info(f"Updated context for session {session_id}")
        except Exception as e:
            logger.error(f"Error updating context: {str(e)}")
            raise
    
    def add_recommendation(self, 
                         session_id: str, 
                         recommendation: Dict[str, Any]) -> None:
        """Add a recommendation to the session"""
        try:
            if session_id not in self.active_sessions:
                raise ValueError(f"Session {session_id} not found")
            
            recommendation_data = {
                'recommendation_id': str(uuid.uuid4()),
                'timestamp': datetime.now().isoformat(),
                'recommendation': recommendation,
                'user_feedback': None
            }
            
            self.active_sessions[session_id]['recommendations_given'].append(recommendation_data)
            
            logger.info(f"Added recommendation to session {session_id}")
        except Exception as e:
            logger.error(f"Error adding recommendation: {str(e)}")
            raise
    
    def add_topic(self, session_id: str, topic: str) -> None:
        """Add a topic to the discussed topics list"""
        try:
            if session_id not in self.active_sessions:
                raise ValueError(f"Session {session_id} not found")
            
            if topic not in self.active_sessions[session_id]['topics_discussed']:
                self.active_sessions[session_id]['topics_discussed'].append(topic)
            
            logger.info(f"Added topic '{topic}' to session {session_id}")
        except Exception as e:
            logger.error(f"Error adding topic: {str(e)}")
            raise
    
    def end_session(self, session_id: str, feedback: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """End a conversation session"""
        try:
            if session_id not in self.active_sessions:
                raise ValueError(f"Session {session_id} not found")
            
            session = self.active_sessions[session_id]
            
            # Add feedback if provided
            if feedback:
                session['session_metadata']['user_satisfaction'] = feedback.get('satisfaction')
                session['session_metadata']['feedback_comments'] = feedback.get('comments')
            
            # Calculate session statistics
            session['ended_at'] = datetime.now().isoformat()
            session['duration'] = self._calculate_session_duration(session)
            session['summary'] = self._generate_session_summary(session)
            
            # Move to history (keep in active for a while for potential follow-up)
            logger.info(f"Ended session {session_id}")
            
            return session
        except Exception as e:
            logger.error(f"Error ending session: {str(e)}")
            raise
    
    def cleanup_old_sessions(self, hours: int = 24) -> int:
        """Clean up sessions older than specified hours"""
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            sessions_to_remove = []
            
            for session_id, session in self.active_sessions.items():
                last_activity = datetime.fromisoformat(session['last_activity'])
                if last_activity < cutoff_time:
                    sessions_to_remove.append(session_id)
            
            for session_id in sessions_to_remove:
                del self.active_sessions[session_id]
            
            logger.info(f"Cleaned up {len(sessions_to_remove)} old sessions")
            return len(sessions_to_remove)
        except Exception as e:
            logger.error(f"Error cleaning up sessions: {str(e)}")
            return 0
    
    def get_session_statistics(self, session_id: str) -> Dict[str, Any]:
        """Get session statistics"""
        try:
            if session_id not in self.active_sessions:
                raise ValueError(f"Session {session_id} not found")
            
            session = self.active_sessions[session_id]
            
            return {
                'session_id': session_id,
                'duration': self._calculate_session_duration(session),
                'message_count': len(session['messages']),
                'topics_count': len(session['topics_discussed']),
                'recommendations_count': len(session['recommendations_given']),
                'user_messages': len([m for m in session['messages'] if m['sender'] == 'user']),
                'assistant_messages': len([m for m in session['messages'] if m['sender'] == 'assistant']),
                'avg_response_time': session['session_metadata']['avg_response_time']
            }
        except Exception as e:
            logger.error(f"Error getting session statistics: {str(e)}")
            raise
    
    def _update_context(self, session_id: str, message_data: Dict[str, Any]) -> None:
        """Update context based on message content"""
        try:
            content = message_data['content'].lower()
            
            # Extract topics from message
            topics = self._extract_topics(content)
            for topic in topics:
                self.add_topic(session_id, topic)
            
            # Update context based on message type
            if 'career' in content:
                self.active_sessions[session_id]['context']['career_discussed'] = True
            
            if 'assessment' in content:
                self.active_sessions[session_id]['context']['assessment_discussed'] = True
            
            if 'learning' in content or 'skill' in content:
                self.active_sessions[session_id]['context']['learning_discussed'] = True
            
        except Exception as e:
            logger.error(f"Error updating context: {str(e)}")
    
    def _extract_topics(self, content: str) -> List[str]:
        """Extract topics from message content"""
        topics = []
        
        topic_keywords = {
            'career_planning': ['career', 'job', 'profession', 'work'],
            'education': ['education', 'degree', 'school', 'university', 'college'],
            'skills': ['skill', 'ability', 'competency', 'expertise'],
            'assessment': ['assessment', 'test', 'evaluation', 'quiz'],
            'learning': ['learning', 'study', 'course', 'training'],
            'mentorship': ['mentor', 'mentorship', 'guidance', 'advice']
        }
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in content for keyword in keywords):
                topics.append(topic)
        
        return topics
    
    def _calculate_session_duration(self, session: Dict[str, Any]) -> str:
        """Calculate session duration"""
        try:
            created_at = datetime.fromisoformat(session['created_at'])
            ended_at = datetime.fromisoformat(session.get('ended_at', datetime.now().isoformat()))
            
            duration = ended_at - created_at
            return str(duration)
        except Exception as e:
            logger.error(f"Error calculating session duration: {str(e)}")
            return "0:00:00"
    
    def _generate_session_summary(self, session: Dict[str, Any]) -> Dict[str, Any]:
        """Generate session summary"""
        try:
            return {
                'topics_discussed': session['topics_discussed'],
                'recommendations_given': len(session['recommendations_given']),
                'message_count': len(session['messages']),
                'key_insights': self._extract_key_insights(session['messages']),
                'next_steps': self._suggest_next_steps(session)
            }
        except Exception as e:
            logger.error(f"Error generating session summary: {str(e)}")
            return {}
    
    def _extract_key_insights(self, messages: List[Dict[str, Any]]) -> List[str]:
        """Extract key insights from conversation"""
        insights = []
        
        # Simple heuristic - look for assistant messages with key phrases
        for message in messages:
            if message['sender'] == 'assistant':
                content = message['content'].lower()
                if 'recommend' in content or 'suggest' in content:
                    insights.append(message['content'][:100] + "...")
        
        return insights[:3]  # Top 3 insights
    
    def _suggest_next_steps(self, session: Dict[str, Any]) -> List[str]:
        """Suggest next steps based on session"""
        next_steps = []
        
        if 'career_discussed' in session['context']:
            next_steps.append("Research specific careers mentioned")
        
        if 'assessment_discussed' in session['context']:
            next_steps.append("Complete recommended assessments")
        
        if 'learning_discussed' in session['context']:
            next_steps.append("Create a learning plan")
        
        return next_steps
