"""
Backend Integration Service for CareerConnect AI
Handles communication with Spring Boot backend and database operations
"""

import requests
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from flask import current_app

logger = logging.getLogger(__name__)

class BackendIntegrationService:
    """Service to handle integration with Spring Boot backend"""

    def __init__(self):
        self.backend_url = None
        self.integration_enabled = False
        self.timeout = 10  # seconds

    def init_app(self, app):
        """Initialize the service with Flask app configuration"""
        self.backend_url = app.config.get('BACKEND_API_URL', 'http://localhost:8080/api')
        self.integration_enabled = app.config.get('BACKEND_INTEGRATION_ENABLED', True)
        logger.info(f"Backend integration {'enabled' if self.integration_enabled else 'disabled'}")
        logger.info(f"Backend URL: {self.backend_url}")

    def is_backend_available(self) -> bool:
        """Check if the Spring Boot backend is available"""
        if not self.integration_enabled:
            return False

        try:
            response = requests.get(f"{self.backend_url}/health", timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.debug(f"Backend not available: {e}")
            return False

    def save_user_profile(self, user_id: str, profile_data: Dict[str, Any]) -> bool:
        """Save user profile to backend database"""
        if not self.integration_enabled or not self.is_backend_available():
            logger.debug("Backend not available, skipping profile save")
            return False

        try:
            endpoint = f"{self.backend_url}/profiles/{user_id}"
            response = requests.put(
                endpoint,
                json=profile_data,
                timeout=self.timeout,
                headers={'Content-Type': 'application/json'}
            )

            if response.status_code in [200, 201]:
                logger.info(f"Profile saved for user {user_id}")
                return True
            else:
                logger.warn(f"Failed to save profile for user {user_id}: {response.status_code}")
                return False

        except Exception as e:
            logger.error(f"Error saving user profile: {e}")
            return False

    def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user profile from backend database"""
        if not self.integration_enabled or not self.is_backend_available():
            logger.debug("Backend not available, cannot get profile")
            return None

        try:
            endpoint = f"{self.backend_url}/profiles/{user_id}"
            response = requests.get(endpoint, timeout=self.timeout)

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                logger.debug(f"No profile found for user {user_id}")
                return None
            else:
                logger.warn(f"Failed to get profile for user {user_id}: {response.status_code}")
                return None

        except Exception as e:
            logger.error(f"Error getting user profile: {e}")
            return None

    def save_chat_history(self, user_id: str, message: str, response: str) -> bool:
        """Save chat interaction to backend database"""
        if not self.integration_enabled or not self.is_backend_available():
            return False

        try:
            endpoint = f"{self.backend_url}/chat/save"
            data = {
                'userId': user_id,
                'userMessage': message,
                'aiResponse': response,
                'timestamp': datetime.utcnow().isoformat()
            }

            response = requests.post(
                endpoint,
                json=data,
                timeout=self.timeout,
                headers={'Content-Type': 'application/json'}
            )

            return response.status_code in [200, 201]

        except Exception as e:
            logger.error(f"Error saving chat history: {e}")
            return False

    def get_chat_history(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get chat history from backend database"""
        if not self.integration_enabled or not self.is_backend_available():
            return []

        try:
            endpoint = f"{self.backend_url}/chat/history/{user_id}"
            params = {'limit': limit}

            response = requests.get(endpoint, params=params, timeout=self.timeout)

            if response.status_code == 200:
                return response.json()
            else:
                logger.warn(f"Failed to get chat history for user {user_id}: {response.status_code}")
                return []

        except Exception as e:
            logger.error(f"Error getting chat history: {e}")
            return []

    def save_assessment_results(self, user_id: str, assessment_data: Dict[str, Any]) -> bool:
        """Save assessment results to backend database"""
        if not self.integration_enabled or not self.is_backend_available():
            return False

        try:
            endpoint = f"{self.backend_url}/assessments/save"
            data = {
                'userId': user_id,
                'assessmentData': assessment_data,
                'timestamp': datetime.utcnow().isoformat()
            }

            response = requests.post(
                endpoint,
                json=data,
                timeout=self.timeout,
                headers={'Content-Type': 'application/json'}
            )

            return response.status_code in [200, 201]

        except Exception as e:
            logger.error(f"Error saving assessment results: {e}")
            return False

    def get_assessment_results(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get latest assessment results from backend database"""
        if not self.integration_enabled or not self.is_backend_available():
            return None

        try:
            endpoint = f"{self.backend_url}/assessments/results/{user_id}"
            response = requests.get(endpoint, timeout=self.timeout)

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                logger.debug(f"No assessment results found for user {user_id}")
                return None
            else:
                logger.warn(f"Failed to get assessment results for user {user_id}: {response.status_code}")
                return None

        except Exception as e:
            logger.error(f"Error getting assessment results: {e}")
            return None

    def notify_backend_ai_response(self, user_id: str, request_type: str, response_data: Dict[str, Any]) -> bool:
        """Notify backend about AI response for analytics"""
        if not self.integration_enabled or not self.is_backend_available():
            return False

        try:
            endpoint = f"{self.backend_url}/ai/analytics"
            data = {
                'userId': user_id,
                'requestType': request_type,  # chat, assessment, career_analysis
                'responseData': response_data,
                'timestamp': datetime.utcnow().isoformat()
            }

            response = requests.post(
                endpoint,
                json=data,
                timeout=self.timeout,
                headers={'Content-Type': 'application/json'}
            )

            return response.status_code in [200, 201]

        except Exception as e:
            logger.error(f"Error notifying backend: {e}")
            return False

    def get_backend_health(self) -> Dict[str, Any]:
        """Get comprehensive health status from backend"""
        health_data = {
            'backend_available': False,
            'database_connected': False,
            'firebase_connected': False,
            'response_time_ms': None
        }

        if not self.integration_enabled:
            health_data['status'] = 'disabled'
            return health_data

        try:
            start_time = datetime.now()
            response = requests.get(f"{self.backend_url}/health", timeout=5)
            end_time = datetime.now()

            health_data['response_time_ms'] = (end_time - start_time).total_seconds() * 1000

            if response.status_code == 200:
                backend_health = response.json()
                health_data.update({
                    'backend_available': True,
                    'database_connected': backend_health.get('database_connected', False),
                    'firebase_connected': backend_health.get('firebase_connected', False),
                    'status': 'connected'
                })
            else:
                health_data['status'] = f'error_{response.status_code}'

        except Exception as e:
            health_data['status'] = f'error: {str(e)}'
            logger.error(f"Backend health check failed: {e}")

        return health_data

# Global service instance
backend_service = BackendIntegrationService()