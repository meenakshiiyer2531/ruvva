"""
RIASEC Personality Assessment Analyzer for CareerConnect AI
Scientific personality analysis specifically designed for Indian students' career exploration.
"""

import json
import logging
import math
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import numpy as np
from config import get_config

# Configure logging
logger = logging.getLogger(__name__)

@dataclass
class RIASECScore:
    """RIASEC personality dimension scores."""
    realistic: float
    investigative: float
    artistic: float
    social: float
    enterprising: float
    conventional: float
    
    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary."""
        return {
            'Realistic': self.realistic,
            'Investigative': self.investigative,
            'Artistic': self.artistic,
            'Social': self.social,
            'Enterprising': self.enterprising,
            'Conventional': self.conventional
        }
    
    def get_primary_type(self) -> str:
        """Get primary personality type."""
        scores = self.to_dict()
        return max(scores, key=scores.get)
    
    def get_secondary_type(self) -> str:
        """Get secondary personality type."""
        scores = self.to_dict()
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_scores[1][0] if len(sorted_scores) > 1 else sorted_scores[0][0]

@dataclass
class PersonalityProfile:
    """Comprehensive personality profile."""
    riasec_scores: RIASECScore
    primary_type: str
    secondary_type: str
    strengths: List[str]
    work_environment_preferences: List[str]
    communication_style: str
    learning_preferences: List[str]
    career_clusters: List[str]
    personality_description: str
    indian_context_insights: Dict[str, Any]

@dataclass
class CareerMatch:
    """Career match with compatibility score."""
    career_name: str
    riasec_codes: List[str]
    compatibility_score: float
    match_percentage: float
    explanation: str
    indian_relevance: Dict[str, Any]

class RIASECAnalyzer:
    """
    Scientific RIASEC personality assessment analyzer for Indian students.
    
    Features:
    - Comprehensive RIASEC dimension analysis
    - Career mapping with Indian context
    - Personality insights generation
    - Assessment question processing
    - Visualization data generation
    """
    
    def __init__(self):
        """Initialize RIASEC analyzer."""
        self.config = get_config()
        
        # RIASEC dimension definitions
        self.dimensions = {
            'Realistic': {
                'description': 'Practical, hands-on activities',
                'characteristics': ['Practical', 'Mechanical', 'Athletic', 'Outdoor-oriented'],
                'indian_context': 'Engineering, Agriculture, Defense, Sports'
            },
            'Investigative': {
                'description': 'Research, analysis, problem-solving',
                'characteristics': ['Analytical', 'Scientific', 'Intellectual', 'Curious'],
                'indian_context': 'Research, Medicine, Data Science, Academia'
            },
            'Artistic': {
                'description': 'Creative, expressive activities',
                'characteristics': ['Creative', 'Imaginative', 'Expressive', 'Original'],
                'indian_context': 'Design, Media, Arts, Entertainment'
            },
            'Social': {
                'description': 'Helping, teaching, working with people',
                'characteristics': ['Helpful', 'Friendly', 'Cooperative', 'Empathetic'],
                'indian_context': 'Teaching, Healthcare, Social Work, Counseling'
            },
            'Enterprising': {
                'description': 'Leadership, business, persuading',
                'characteristics': ['Ambitious', 'Confident', 'Persuasive', 'Leadership-oriented'],
                'indian_context': 'Business, Management, Sales, Entrepreneurship'
            },
            'Conventional': {
                'description': 'Organization, detail-oriented work',
                'characteristics': ['Organized', 'Detail-oriented', 'Reliable', 'Systematic'],
                'indian_context': 'Banking, Administration, Accounting, Government'
            }
        }
        
        # Load assessment questions
        self.assessment_questions = self._load_assessment_questions()
        
        # Load career database
        self.career_database = self._load_career_database()
        
        logger.info("RIASECAnalyzer initialized successfully")
    
    def _load_assessment_questions(self) -> List[Dict[str, Any]]:
        """Load comprehensive RIASEC assessment questions."""
        return [
            # Realistic Questions
            {
                'id': 'R1',
                'question': 'You enjoy working with your hands and building things',
                'dimension': 'Realistic',
                'type': 'agreement',
                'indian_context': 'Engineering projects, agricultural work, construction'
            },
            {
                'id': 'R2',
                'question': 'You prefer outdoor activities over indoor work',
                'dimension': 'Realistic',
                'type': 'preference',
                'indian_context': 'Field work, agricultural activities, outdoor sports'
            },
            {
                'id': 'R3',
                'question': 'You like working with tools and machinery',
                'dimension': 'Realistic',
                'type': 'agreement',
                'indian_context': 'Technical work, manufacturing, automotive repair'
            },
            {
                'id': 'R4',
                'question': 'You enjoy physical activities and sports',
                'dimension': 'Realistic',
                'type': 'agreement',
                'indian_context': 'Sports, physical education, fitness training'
            },
            {
                'id': 'R5',
                'question': 'You prefer concrete, practical solutions over abstract ideas',
                'dimension': 'Realistic',
                'type': 'preference',
                'indian_context': 'Engineering solutions, practical problem-solving'
            },
            {
                'id': 'R6',
                'question': 'You like working with animals or plants',
                'dimension': 'Realistic',
                'type': 'agreement',
                'indian_context': 'Veterinary science, agriculture, horticulture'
            },
            
            # Investigative Questions
            {
                'id': 'I1',
                'question': 'You enjoy solving complex problems and puzzles',
                'dimension': 'Investigative',
                'type': 'agreement',
                'indian_context': 'Research, data analysis, scientific investigation'
            },
            {
                'id': 'I2',
                'question': 'You like to understand how things work',
                'dimension': 'Investigative',
                'type': 'agreement',
                'indian_context': 'Scientific research, technical analysis'
            },
            {
                'id': 'I3',
                'question': 'You prefer working independently on research projects',
                'dimension': 'Investigative',
                'type': 'preference',
                'indian_context': 'Academic research, laboratory work'
            },
            {
                'id': 'I4',
                'question': 'You enjoy reading scientific articles and journals',
                'dimension': 'Investigative',
                'type': 'agreement',
                'indian_context': 'Academic studies, research publications'
            },
            {
                'id': 'I5',
                'question': 'You like to analyze data and find patterns',
                'dimension': 'Investigative',
                'type': 'agreement',
                'indian_context': 'Data science, statistical analysis, research'
            },
            {
                'id': 'I6',
                'question': 'You prefer theoretical discussions over practical applications',
                'dimension': 'Investigative',
                'type': 'preference',
                'indian_context': 'Academic discourse, theoretical research'
            },
            
            # Artistic Questions
            {
                'id': 'A1',
                'question': 'You enjoy creating art, music, or writing',
                'dimension': 'Artistic',
                'type': 'agreement',
                'indian_context': 'Fine arts, music, literature, creative writing'
            },
            {
                'id': 'A2',
                'question': 'You like to express yourself through creative means',
                'dimension': 'Artistic',
                'type': 'agreement',
                'indian_context': 'Creative arts, performance, design'
            },
            {
                'id': 'A3',
                'question': 'You prefer flexible, unstructured work environments',
                'dimension': 'Artistic',
                'type': 'preference',
                'indian_context': 'Creative industries, freelance work'
            },
            {
                'id': 'A4',
                'question': 'You enjoy designing and creating new things',
                'dimension': 'Artistic',
                'type': 'agreement',
                'indian_context': 'Product design, graphic design, architecture'
            },
            {
                'id': 'A5',
                'question': 'You like to work with colors, shapes, and aesthetics',
                'dimension': 'Artistic',
                'type': 'agreement',
                'indian_context': 'Visual arts, interior design, fashion design'
            },
            {
                'id': 'A6',
                'question': 'You prefer original, unique approaches over conventional methods',
                'dimension': 'Artistic',
                'type': 'preference',
                'indian_context': 'Innovation, creative problem-solving'
            },
            
            # Social Questions
            {
                'id': 'S1',
                'question': 'You enjoy helping others and making a difference in their lives',
                'dimension': 'Social',
                'type': 'agreement',
                'indian_context': 'Social work, healthcare, teaching, counseling'
            },
            {
                'id': 'S2',
                'question': 'You like working in teams and collaborating with others',
                'dimension': 'Social',
                'type': 'agreement',
                'indian_context': 'Team projects, community work, group activities'
            },
            {
                'id': 'S3',
                'question': 'You enjoy teaching and explaining things to others',
                'dimension': 'Social',
                'type': 'agreement',
                'indian_context': 'Education, training, mentoring, coaching'
            },
            {
                'id': 'S4',
                'question': 'You prefer working with people rather than things',
                'dimension': 'Social',
                'type': 'preference',
                'indian_context': 'Human services, customer relations, community work'
            },
            {
                'id': 'S5',
                'question': 'You like to listen to others and understand their problems',
                'dimension': 'Social',
                'type': 'agreement',
                'indian_context': 'Counseling, psychology, social work, healthcare'
            },
            {
                'id': 'S6',
                'question': 'You enjoy organizing events and bringing people together',
                'dimension': 'Social',
                'type': 'agreement',
                'indian_context': 'Event management, community organizing, social work'
            },
            
            # Enterprising Questions
            {
                'id': 'E1',
                'question': 'You enjoy leading and managing others',
                'dimension': 'Enterprising',
                'type': 'agreement',
                'indian_context': 'Management, leadership roles, team leadership'
            },
            {
                'id': 'E2',
                'question': 'You like to persuade and influence others',
                'dimension': 'Enterprising',
                'type': 'agreement',
                'indian_context': 'Sales, marketing, business development'
            },
            {
                'id': 'E3',
                'question': 'You enjoy taking risks and trying new ventures',
                'dimension': 'Enterprising',
                'type': 'agreement',
                'indian_context': 'Entrepreneurship, business innovation, startups'
            },
            {
                'id': 'E4',
                'question': 'You prefer competitive environments',
                'dimension': 'Enterprising',
                'type': 'preference',
                'indian_context': 'Business competition, sales targets, performance metrics'
            },
            {
                'id': 'E5',
                'question': 'You like to make decisions and take responsibility',
                'dimension': 'Enterprising',
                'type': 'agreement',
                'indian_context': 'Management, leadership, decision-making roles'
            },
            {
                'id': 'E6',
                'question': 'You enjoy networking and building professional relationships',
                'dimension': 'Enterprising',
                'type': 'agreement',
                'indian_context': 'Business networking, professional development, partnerships'
            },
            
            # Conventional Questions
            {
                'id': 'C1',
                'question': 'You enjoy organizing and maintaining systems',
                'dimension': 'Conventional',
                'type': 'agreement',
                'indian_context': 'Administration, operations, system management'
            },
            {
                'id': 'C2',
                'question': 'You like working with numbers and data',
                'dimension': 'Conventional',
                'type': 'agreement',
                'indian_context': 'Accounting, finance, data management, statistics'
            },
            {
                'id': 'C3',
                'question': 'You prefer structured, predictable work environments',
                'dimension': 'Conventional',
                'type': 'preference',
                'indian_context': 'Government jobs, banking, corporate administration'
            },
            {
                'id': 'C4',
                'question': 'You enjoy following established procedures and protocols',
                'dimension': 'Conventional',
                'type': 'agreement',
                'indian_context': 'Compliance, quality control, standard operating procedures'
            },
            {
                'id': 'C5',
                'question': 'You like to work with computers and technology systems',
                'dimension': 'Conventional',
                'type': 'agreement',
                'indian_context': 'IT support, system administration, database management'
            },
            {
                'id': 'C6',
                'question': 'You prefer clear instructions and well-defined tasks',
                'dimension': 'Conventional',
                'type': 'preference',
                'indian_context': 'Process-oriented work, administrative tasks, documentation'
            }
        ]
    
    def _load_career_database(self) -> List[Dict[str, Any]]:
        """Load career database with RIASEC codes and Indian context."""
        return [
            # Engineering Careers
            {
                'career': 'Software Engineer',
                'riasec_codes': ['I', 'R', 'C'],
                'description': 'Designs and develops software applications',
                'indian_context': {
                    'entrance_exams': ['JEE Main', 'JEE Advanced', 'GATE'],
                    'top_colleges': ['IITs', 'NITs', 'IIITs'],
                    'salary_range': '₹6-25 LPA',
                    'growth_prospects': 'Very High',
                    'job_market': 'Excellent'
                }
            },
            {
                'career': 'Mechanical Engineer',
                'riasec_codes': ['R', 'I', 'C'],
                'description': 'Designs and maintains mechanical systems',
                'indian_context': {
                    'entrance_exams': ['JEE Main', 'JEE Advanced', 'GATE'],
                    'top_colleges': ['IITs', 'NITs', 'BITS Pilani'],
                    'salary_range': '₹4-15 LPA',
                    'growth_prospects': 'High',
                    'job_market': 'Good'
                }
            },
            {
                'career': 'Civil Engineer',
                'riasec_codes': ['R', 'C', 'E'],
                'description': 'Designs and constructs infrastructure projects',
                'indian_context': {
                    'entrance_exams': ['JEE Main', 'JEE Advanced', 'GATE'],
                    'top_colleges': ['IITs', 'NITs', 'Delhi Technological University'],
                    'salary_range': '₹3-12 LPA',
                    'growth_prospects': 'High',
                    'job_market': 'Good'
                }
            },
            
            # Medical Careers
            {
                'career': 'Doctor',
                'riasec_codes': ['I', 'S', 'C'],
                'description': 'Diagnoses and treats medical conditions',
                'indian_context': {
                    'entrance_exams': ['NEET', 'AIIMS', 'JIPMER'],
                    'top_colleges': ['AIIMS', 'CMC Vellore', 'JIPMER'],
                    'salary_range': '₹8-50 LPA',
                    'growth_prospects': 'Very High',
                    'job_market': 'Excellent'
                }
            },
            {
                'career': 'Nurse',
                'riasec_codes': ['S', 'C', 'R'],
                'description': 'Provides patient care and medical support',
                'indian_context': {
                    'entrance_exams': ['NEET', 'State Nursing Exams'],
                    'top_colleges': ['CMC Vellore', 'AIIMS', 'PGIMER'],
                    'salary_range': '₹2-8 LPA',
                    'growth_prospects': 'High',
                    'job_market': 'Good'
                }
            },
            
            # Business and Management
            {
                'career': 'Business Analyst',
                'riasec_codes': ['I', 'E', 'C'],
                'description': 'Analyzes business processes and recommends improvements',
                'indian_context': {
                    'entrance_exams': ['CAT', 'XAT', 'GMAT'],
                    'top_colleges': ['IIMs', 'ISB', 'XLRI'],
                    'salary_range': '₹6-20 LPA',
                    'growth_prospects': 'Very High',
                    'job_market': 'Excellent'
                }
            },
            {
                'career': 'Marketing Manager',
                'riasec_codes': ['E', 'A', 'S'],
                'description': 'Develops and implements marketing strategies',
                'indian_context': {
                    'entrance_exams': ['CAT', 'XAT', 'GMAT'],
                    'top_colleges': ['IIMs', 'ISB', 'XLRI'],
                    'salary_range': '₹5-18 LPA',
                    'growth_prospects': 'High',
                    'job_market': 'Good'
                }
            },
            
            # Arts and Design
            {
                'career': 'Graphic Designer',
                'riasec_codes': ['A', 'E', 'I'],
                'description': 'Creates visual designs for various media',
                'indian_context': {
                    'entrance_exams': ['NID', 'CEED', 'UCEED'],
                    'top_colleges': ['NID', 'IITs', 'Srishti Institute'],
                    'salary_range': '₹3-12 LPA',
                    'growth_prospects': 'High',
                    'job_market': 'Good'
                }
            },
            {
                'career': 'Architect',
                'riasec_codes': ['A', 'R', 'I'],
                'description': 'Designs buildings and structures',
                'indian_context': {
                    'entrance_exams': ['NATA', 'JEE Main', 'AAT'],
                    'top_colleges': ['IITs', 'SPA Delhi', 'CEPT'],
                    'salary_range': '₹4-15 LPA',
                    'growth_prospects': 'High',
                    'job_market': 'Good'
                }
            },
            
            # Education and Social Work
            {
                'career': 'Teacher',
                'riasec_codes': ['S', 'A', 'I'],
                'description': 'Educates and mentors students',
                'indian_context': {
                    'entrance_exams': ['CTET', 'TET', 'NET'],
                    'top_colleges': ['DU', 'JNU', 'TISS'],
                    'salary_range': '₹3-10 LPA',
                    'growth_prospects': 'Stable',
                    'job_market': 'Good'
                }
            },
            {
                'career': 'Social Worker',
                'riasec_codes': ['S', 'E', 'A'],
                'description': 'Helps individuals and communities overcome challenges',
                'indian_context': {
                    'entrance_exams': ['TISS', 'DU', 'JNU'],
                    'top_colleges': ['TISS', 'DU', 'JNU'],
                    'salary_range': '₹2-8 LPA',
                    'growth_prospects': 'Growing',
                    'job_market': 'Moderate'
                }
            },
            
            # Government and Administration
            {
                'career': 'IAS Officer',
                'riasec_codes': ['E', 'S', 'C'],
                'description': 'Administers government policies and programs',
                'indian_context': {
                    'entrance_exams': ['UPSC Civil Services'],
                    'top_colleges': ['Any Graduate'],
                    'salary_range': '₹8-25 LPA',
                    'growth_prospects': 'Stable',
                    'job_market': 'Competitive'
                }
            },
            {
                'career': 'Bank Manager',
                'riasec_codes': ['C', 'E', 'S'],
                'description': 'Manages banking operations and customer relations',
                'indian_context': {
                    'entrance_exams': ['IBPS', 'SBI PO', 'RBI Grade B'],
                    'top_colleges': ['Any Graduate'],
                    'salary_range': '₹5-15 LPA',
                    'growth_prospects': 'Stable',
                    'job_market': 'Good'
                }
            }
        ]
    
    def analyze_responses(self, assessment_answers: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process RIASEC assessment responses and generate comprehensive analysis.
        
        Args:
            assessment_answers: Dictionary with question IDs and responses
            
        Returns:
            Dictionary with complete analysis results
        """
        try:
            # Calculate RIASEC scores
            riasec_scores = self.calculate_personality_scores(assessment_answers)
            
            # Generate personality profile
            personality_profile = self.generate_personality_profile(riasec_scores)
            
            # Map careers to personality
            career_matches = self.map_careers_to_personality(riasec_scores)
            
            # Generate visualization data
            visualization_data = self.generate_visualization_data(riasec_scores, career_matches)
            
            return {
                'riasec_scores': riasec_scores.to_dict(),
                'personality_profile': personality_profile,
                'career_matches': career_matches,
                'visualization_data': visualization_data,
                'analysis_timestamp': datetime.utcnow().isoformat(),
                'assessment_summary': self._generate_assessment_summary(riasec_scores, personality_profile)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing RIASEC responses: {e}")
            raise Exception(f"Failed to analyze assessment: {e}")
    
    def calculate_personality_scores(self, responses: Dict[str, Any]) -> RIASECScore:
        """
        Calculate RIASEC dimension scores from assessment responses.
        
        Args:
            responses: Dictionary with question responses
            
        Returns:
            RIASECScore object with dimension scores
        """
        # Initialize score counters
        dimension_scores = {
            'Realistic': 0,
            'Investigative': 0,
            'Artistic': 0,
            'Social': 0,
            'Enterprising': 0,
            'Conventional': 0
        }
        
        dimension_counts = {
            'Realistic': 0,
            'Investigative': 0,
            'Artistic': 0,
            'Social': 0,
            'Enterprising': 0,
            'Conventional': 0
        }
        
        # Process each response
        for question_id, response in responses.items():
            # Find the question in our database
            question = next((q for q in self.assessment_questions if q['id'] == question_id), None)
            
            if question:
                dimension = question['dimension']
                score = self._calculate_question_score(response, question['type'])
                
                dimension_scores[dimension] += score
                dimension_counts[dimension] += 1
        
        # Calculate average scores for each dimension
        final_scores = {}
        for dimension in dimension_scores:
            if dimension_counts[dimension] > 0:
                final_scores[dimension.lower()] = dimension_scores[dimension] / dimension_counts[dimension]
            else:
                final_scores[dimension.lower()] = 0.0
        
        return RIASECScore(**final_scores)
    
    def _calculate_question_score(self, response: Any, question_type: str) -> float:
        """Calculate score for individual question response."""
        if question_type == 'agreement':
            # Likert scale: Strongly Disagree (1) to Strongly Agree (5)
            if isinstance(response, (int, float)):
                return float(response)
            elif isinstance(response, str):
                # Convert text responses to numeric
                response_lower = response.lower()
                if 'strongly disagree' in response_lower or response_lower == '1':
                    return 1.0
                elif 'disagree' in response_lower or response_lower == '2':
                    return 2.0
                elif 'neutral' in response_lower or response_lower == '3':
                    return 3.0
                elif 'agree' in response_lower or response_lower == '4':
                    return 4.0
                elif 'strongly agree' in response_lower or response_lower == '5':
                    return 5.0
                else:
                    return 3.0  # Default neutral
            else:
                return 3.0  # Default neutral
        
        elif question_type == 'preference':
            # Preference scale: Strongly Prefer A (1) to Strongly Prefer B (5)
            if isinstance(response, (int, float)):
                return float(response)
            elif isinstance(response, str):
                response_lower = response.lower()
                if 'strongly prefer' in response_lower and 'first' in response_lower:
                    return 1.0
                elif 'prefer' in response_lower and 'first' in response_lower:
                    return 2.0
                elif 'neutral' in response_lower or 'no preference' in response_lower:
                    return 3.0
                elif 'prefer' in response_lower and 'second' in response_lower:
                    return 4.0
                elif 'strongly prefer' in response_lower and 'second' in response_lower:
                    return 5.0
                else:
                    return 3.0  # Default neutral
            else:
                return 3.0  # Default neutral
        
        else:
            return 3.0  # Default neutral
    
    def generate_personality_profile(self, riasec_scores: RIASECScore) -> PersonalityProfile:
        """
        Generate comprehensive personality profile from RIASEC scores.
        
        Args:
            riasec_scores: RIASEC dimension scores
            
        Returns:
            PersonalityProfile object
        """
        primary_type = riasec_scores.get_primary_type()
        secondary_type = riasec_scores.get_secondary_type()
        
        # Generate strengths based on top dimensions
        strengths = self._identify_strengths(riasec_scores)
        
        # Generate work environment preferences
        work_env_prefs = self._generate_work_environment_preferences(riasec_scores)
        
        # Generate communication style
        communication_style = self._analyze_communication_style(riasec_scores)
        
        # Generate learning preferences
        learning_prefs = self._generate_learning_preferences(riasec_scores)
        
        # Generate career clusters
        career_clusters = self._identify_career_clusters(riasec_scores)
        
        # Generate personality description
        personality_description = self._generate_personality_description(riasec_scores, primary_type, secondary_type)
        
        # Generate Indian context insights
        indian_context_insights = self._generate_indian_context_insights(riasec_scores, primary_type, secondary_type)
        
        return PersonalityProfile(
            riasec_scores=riasec_scores,
            primary_type=primary_type,
            secondary_type=secondary_type,
            strengths=strengths,
            work_environment_preferences=work_env_prefs,
            communication_style=communication_style,
            learning_preferences=learning_prefs,
            career_clusters=career_clusters,
            personality_description=personality_description,
            indian_context_insights=indian_context_insights
        )
    
    def map_careers_to_personality(self, riasec_scores: RIASECScore) -> List[CareerMatch]:
        """
        Map careers to personality based on RIASEC compatibility.
        
        Args:
            riasec_scores: RIASEC dimension scores
            
        Returns:
            List of CareerMatch objects sorted by compatibility
        """
        career_matches = []
        scores_dict = riasec_scores.to_dict()
        
        for career in self.career_database:
            compatibility_score = self._calculate_career_compatibility(scores_dict, career['riasec_codes'])
            match_percentage = compatibility_score * 100
            
            explanation = self._generate_career_explanation(scores_dict, career['riasec_codes'], career['career'])
            
            career_match = CareerMatch(
                career_name=career['career'],
                riasec_codes=career['riasec_codes'],
                compatibility_score=compatibility_score,
                match_percentage=match_percentage,
                explanation=explanation,
                indian_relevance=career['indian_context']
            )
            
            career_matches.append(career_match)
        
        # Sort by compatibility score (highest first)
        career_matches.sort(key=lambda x: x.compatibility_score, reverse=True)
        
        return career_matches[:10]  # Return top 10 matches
    
    def generate_visualization_data(self, riasec_scores: RIASECScore, career_matches: List[CareerMatch]) -> Dict[str, Any]:
        """
        Generate visualization data for frontend charts and graphs.
        
        Args:
            riasec_scores: RIASEC dimension scores
            career_matches: List of career matches
            
        Returns:
            Dictionary with visualization data
        """
        scores_dict = riasec_scores.to_dict()
        
        # Radar chart data for RIASEC scores
        radar_chart_data = {
            'labels': list(scores_dict.keys()),
            'datasets': [{
                'label': 'RIASEC Scores',
                'data': list(scores_dict.values()),
                'backgroundColor': 'rgba(54, 162, 235, 0.2)',
                'borderColor': 'rgba(54, 162, 235, 1)',
                'borderWidth': 2
            }]
        }
        
        # Career match percentages
        career_match_data = {
            'careers': [match.career_name for match in career_matches],
            'percentages': [match.match_percentage for match in career_matches],
            'colors': self._generate_chart_colors(len(career_matches))
        }
        
        # Personality trait explanations
        trait_explanations = self._generate_trait_explanations(scores_dict)
        
        return {
            'radar_chart': radar_chart_data,
            'career_matches': career_match_data,
            'trait_explanations': trait_explanations,
            'summary_stats': {
                'primary_type': riasec_scores.get_primary_type(),
                'secondary_type': riasec_scores.get_secondary_type(),
                'highest_score': max(scores_dict.values()),
                'lowest_score': min(scores_dict.values()),
                'score_range': max(scores_dict.values()) - min(scores_dict.values())
            }
        }
    
    # Helper methods for personality analysis
    def _identify_strengths(self, riasec_scores: RIASECScore) -> List[str]:
        """Identify personality strengths based on RIASEC scores."""
        scores_dict = riasec_scores.to_dict()
        sorted_scores = sorted(scores_dict.items(), key=lambda x: x[1], reverse=True)
        
        strengths = []
        for dimension, score in sorted_scores[:3]:  # Top 3 dimensions
            if score >= 4.0:  # High score threshold
                strengths.extend(self.dimensions[dimension]['characteristics'])
        
        return list(set(strengths))  # Remove duplicates
    
    def _generate_work_environment_preferences(self, riasec_scores: RIASECScore) -> List[str]:
        """Generate work environment preferences based on RIASEC scores."""
        preferences = []
        scores_dict = riasec_scores.to_dict()
        
        if scores_dict['Realistic'] >= 4.0:
            preferences.extend(['Outdoor work', 'Hands-on activities', 'Physical work'])
        
        if scores_dict['Investigative'] >= 4.0:
            preferences.extend(['Research environment', 'Independent work', 'Analytical tasks'])
        
        if scores_dict['Artistic'] >= 4.0:
            preferences.extend(['Creative freedom', 'Flexible schedule', 'Innovative projects'])
        
        if scores_dict['Social'] >= 4.0:
            preferences.extend(['Team collaboration', 'People interaction', 'Helping others'])
        
        if scores_dict['Enterprising'] >= 4.0:
            preferences.extend(['Leadership roles', 'Competitive environment', 'Decision making'])
        
        if scores_dict['Conventional'] >= 4.0:
            preferences.extend(['Structured environment', 'Clear procedures', 'Organized tasks'])
        
        return list(set(preferences))
    
    def _analyze_communication_style(self, riasec_scores: RIASECScore) -> str:
        """Analyze communication style based on RIASEC scores."""
        scores_dict = riasec_scores.to_dict()
        
        if scores_dict['Social'] >= 4.0:
            return "Collaborative and empathetic communicator"
        elif scores_dict['Enterprising'] >= 4.0:
            return "Persuasive and confident communicator"
        elif scores_dict['Investigative'] >= 4.0:
            return "Analytical and precise communicator"
        elif scores_dict['Artistic'] >= 4.0:
            return "Creative and expressive communicator"
        elif scores_dict['Conventional'] >= 4.0:
            return "Structured and formal communicator"
        else:
            return "Balanced and adaptable communicator"
    
    def _generate_learning_preferences(self, riasec_scores: RIASECScore) -> List[str]:
        """Generate learning preferences based on RIASEC scores."""
        preferences = []
        scores_dict = riasec_scores.to_dict()
        
        if scores_dict['Realistic'] >= 4.0:
            preferences.extend(['Hands-on learning', 'Practical applications', 'Experiential learning'])
        
        if scores_dict['Investigative'] >= 4.0:
            preferences.extend(['Research-based learning', 'Independent study', 'Analytical approach'])
        
        if scores_dict['Artistic'] >= 4.0:
            preferences.extend(['Creative projects', 'Visual learning', 'Self-expression'])
        
        if scores_dict['Social'] >= 4.0:
            preferences.extend(['Group learning', 'Discussion-based', 'Peer interaction'])
        
        if scores_dict['Enterprising'] >= 4.0:
            preferences.extend(['Case studies', 'Leadership roles', 'Real-world applications'])
        
        if scores_dict['Conventional'] >= 4.0:
            preferences.extend(['Structured curriculum', 'Step-by-step learning', 'Traditional methods'])
        
        return list(set(preferences))
    
    def _identify_career_clusters(self, riasec_scores: RIASECScore) -> List[str]:
        """Identify career clusters based on RIASEC scores."""
        clusters = []
        scores_dict = riasec_scores.to_dict()
        
        if scores_dict['Realistic'] >= 4.0:
            clusters.append('Engineering and Technology')
        
        if scores_dict['Investigative'] >= 4.0:
            clusters.append('Research and Science')
        
        if scores_dict['Artistic'] >= 4.0:
            clusters.append('Arts and Design')
        
        if scores_dict['Social'] >= 4.0:
            clusters.append('Education and Social Services')
        
        if scores_dict['Enterprising'] >= 4.0:
            clusters.append('Business and Management')
        
        if scores_dict['Conventional'] >= 4.0:
            clusters.append('Administration and Finance')
        
        return clusters
    
    def _generate_personality_description(self, riasec_scores: RIASECScore, primary_type: str, secondary_type: str) -> str:
        """Generate comprehensive personality description."""
        primary_desc = self.dimensions[primary_type]['description']
        secondary_desc = self.dimensions[secondary_type]['description']
        
        return f"You are primarily {primary_type.lower()} ({primary_desc}) with strong {secondary_type.lower()} tendencies ({secondary_desc}). This combination suggests you are well-suited for careers that combine these two personality dimensions."
    
    def _generate_indian_context_insights(self, riasec_scores: RIASECScore, primary_type: str, secondary_type: str) -> Dict[str, Any]:
        """Generate Indian context insights for personality types."""
        insights = {
            'primary_type_context': self.dimensions[primary_type]['indian_context'],
            'secondary_type_context': self.dimensions[secondary_type]['indian_context'],
            'entrance_exam_recommendations': self._get_entrance_exam_recommendations(primary_type, secondary_type),
            'regional_opportunities': self._get_regional_opportunities(primary_type, secondary_type),
            'family_expectations': self._analyze_family_expectations(primary_type, secondary_type)
        }
        
        return insights
    
    def _calculate_career_compatibility(self, scores_dict: Dict[str, float], career_riasec_codes: List[str]) -> float:
        """Calculate compatibility score between personality and career."""
        if not career_riasec_codes:
            return 0.0
        
        # Calculate weighted average of relevant dimensions
        total_score = 0.0
        weight_sum = 0.0
        
        for i, code in enumerate(career_riasec_codes):
            # Higher weight for primary and secondary codes
            weight = 3.0 - i  # 3.0, 2.0, 1.0 for first, second, third codes
            dimension_name = self._get_dimension_name_from_code(code)
            
            if dimension_name in scores_dict:
                total_score += scores_dict[dimension_name] * weight
                weight_sum += weight
        
        if weight_sum == 0:
            return 0.0
        
        # Normalize to 0-1 scale
        compatibility = (total_score / weight_sum) / 5.0
        return min(compatibility, 1.0)
    
    def _generate_career_explanation(self, scores_dict: Dict[str, float], career_riasec_codes: List[str], career_name: str) -> str:
        """Generate explanation for career match."""
        explanations = []
        
        for i, code in enumerate(career_riasec_codes):
            dimension_name = self._get_dimension_name_from_code(code)
            if dimension_name in scores_dict:
                score = scores_dict[dimension_name]
                if score >= 4.0:
                    explanations.append(f"Strong {dimension_name.lower()} traits ({score:.1f}/5.0)")
                elif score >= 3.0:
                    explanations.append(f"Moderate {dimension_name.lower()} traits ({score:.1f}/5.0)")
                else:
                    explanations.append(f"Weak {dimension_name.lower()} traits ({score:.1f}/5.0)")
        
        if explanations:
            return f"This career matches your personality because: {', '.join(explanations)}"
        else:
            return f"This career may not be the best fit for your current personality profile."
    
    def _get_dimension_name_from_code(self, code: str) -> str:
        """Convert RIASEC code to full dimension name."""
        code_map = {
            'R': 'Realistic',
            'I': 'Investigative',
            'A': 'Artistic',
            'S': 'Social',
            'E': 'Enterprising',
            'C': 'Conventional'
        }
        return code_map.get(code, 'Unknown')
    
    def _generate_chart_colors(self, count: int) -> List[str]:
        """Generate colors for charts."""
        colors = [
            '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
            '#FF9F40', '#FF6384', '#C9CBCF', '#4BC0C0', '#FF6384'
        ]
        return colors[:count]
    
    def _generate_trait_explanations(self, scores_dict: Dict[str, float]) -> Dict[str, Dict[str, Any]]:
        """Generate explanations for personality traits."""
        explanations = {}
        
        for dimension, score in scores_dict.items():
            explanations[dimension] = {
                'score': score,
                'level': self._get_score_level(score),
                'description': self.dimensions[dimension]['description'],
                'characteristics': self.dimensions[dimension]['characteristics'],
                'indian_context': self.dimensions[dimension]['indian_context']
            }
        
        return explanations
    
    def _get_score_level(self, score: float) -> str:
        """Get score level description."""
        if score >= 4.5:
            return "Very High"
        elif score >= 4.0:
            return "High"
        elif score >= 3.5:
            return "Above Average"
        elif score >= 3.0:
            return "Average"
        elif score >= 2.5:
            return "Below Average"
        else:
            return "Low"
    
    def _get_entrance_exam_recommendations(self, primary_type: str, secondary_type: str) -> List[str]:
        """Get entrance exam recommendations based on personality types."""
        exams = []
        
        if primary_type in ['Realistic', 'Investigative']:
            exams.extend(['JEE Main', 'JEE Advanced', 'GATE'])
        
        if primary_type == 'Investigative':
            exams.extend(['NEET', 'AIIMS', 'JIPMER'])
        
        if primary_type in ['Enterprising', 'Conventional']:
            exams.extend(['CAT', 'XAT', 'GMAT'])
        
        if primary_type == 'Artistic':
            exams.extend(['NID', 'CEED', 'UCEED'])
        
        if primary_type == 'Social':
            exams.extend(['CTET', 'TET', 'NET'])
        
        return list(set(exams))
    
    def _get_regional_opportunities(self, primary_type: str, secondary_type: str) -> List[str]:
        """Get regional opportunities based on personality types."""
        opportunities = []
        
        if primary_type in ['Realistic', 'Investigative']:
            opportunities.extend(['Bangalore', 'Hyderabad', 'Pune', 'Chennai'])
        
        if primary_type == 'Enterprising':
            opportunities.extend(['Mumbai', 'Delhi', 'Gurgaon', 'Bangalore'])
        
        if primary_type == 'Artistic':
            opportunities.extend(['Mumbai', 'Delhi', 'Bangalore', 'Chennai'])
        
        if primary_type == 'Social':
            opportunities.extend(['Delhi', 'Mumbai', 'Bangalore', 'Kolkata'])
        
        return list(set(opportunities))
    
    def _analyze_family_expectations(self, primary_type: str, secondary_type: str) -> Dict[str, str]:
        """Analyze family expectations based on personality types."""
        analysis = {
            'alignment': 'Moderate',
            'explanation': 'Your personality type aligns moderately with traditional Indian family expectations.',
            'recommendations': []
        }
        
        if primary_type in ['Realistic', 'Investigative']:
            analysis['alignment'] = 'High'
            analysis['explanation'] = 'Your personality type aligns well with traditional Indian family expectations for stable, respected careers.'
            analysis['recommendations'] = ['Engineering', 'Medicine', 'Government jobs']
        
        elif primary_type == 'Enterprising':
            analysis['alignment'] = 'High'
            analysis['explanation'] = 'Your personality type aligns well with Indian family expectations for leadership and success.'
            analysis['recommendations'] = ['Business', 'Management', 'Government services']
        
        elif primary_type == 'Artistic':
            analysis['alignment'] = 'Low'
            analysis['explanation'] = 'Your personality type may require more explanation to align with traditional family expectations.'
            analysis['recommendations'] = ['Design', 'Architecture', 'Media']
        
        return analysis
    
    def _generate_assessment_summary(self, riasec_scores: RIASECScore, personality_profile: PersonalityProfile) -> Dict[str, Any]:
        """Generate assessment summary."""
        return {
            'total_questions': len(self.assessment_questions),
            'primary_type': personality_profile.primary_type,
            'secondary_type': personality_profile.secondary_type,
            'top_strengths': personality_profile.strengths[:5],
            'career_clusters': personality_profile.career_clusters,
            'communication_style': personality_profile.communication_style,
            'indian_context': personality_profile.indian_context_insights
        }
    
    # Individual dimension scoring methods
    def score_realistic_dimension(self, responses: Dict[str, Any]) -> float:
        """Score Realistic dimension from responses."""
        realistic_responses = {}
        for question_id, response in responses.items():
            question = next((q for q in self.assessment_questions if q['id'] == question_id and q['dimension'] == 'Realistic'), None)
            if question:
                realistic_responses[question_id] = response
        
        if not realistic_responses:
            return 0.0
        
        total_score = sum(self._calculate_question_score(response, 'agreement') for response in realistic_responses.values())
        return total_score / len(realistic_responses)
    
    def score_investigative_dimension(self, responses: Dict[str, Any]) -> float:
        """Score Investigative dimension from responses."""
        investigative_responses = {}
        for question_id, response in responses.items():
            question = next((q for q in self.assessment_questions if q['id'] == question_id and q['dimension'] == 'Investigative'), None)
            if question:
                investigative_responses[question_id] = response
        
        if not investigative_responses:
            return 0.0
        
        total_score = sum(self._calculate_question_score(response, 'agreement') for response in investigative_responses.values())
        return total_score / len(investigative_responses)
    
    def score_artistic_dimension(self, responses: Dict[str, Any]) -> float:
        """Score Artistic dimension from responses."""
        artistic_responses = {}
        for question_id, response in responses.items():
            question = next((q for q in self.assessment_questions if q['id'] == question_id and q['dimension'] == 'Artistic'), None)
            if question:
                artistic_responses[question_id] = response
        
        if not artistic_responses:
            return 0.0
        
        total_score = sum(self._calculate_question_score(response, 'agreement') for response in artistic_responses.values())
        return total_score / len(artistic_responses)
    
    def score_social_dimension(self, responses: Dict[str, Any]) -> float:
        """Score Social dimension from responses."""
        social_responses = {}
        for question_id, response in responses.items():
            question = next((q for q in self.assessment_questions if q['id'] == question_id and q['dimension'] == 'Social'), None)
            if question:
                social_responses[question_id] = response
        
        if not social_responses:
            return 0.0
        
        total_score = sum(self._calculate_question_score(response, 'agreement') for response in social_responses.values())
        return total_score / len(social_responses)
    
    def score_enterprising_dimension(self, responses: Dict[str, Any]) -> float:
        """Score Enterprising dimension from responses."""
        enterprising_responses = {}
        for question_id, response in responses.items():
            question = next((q for q in self.assessment_questions if q['id'] == question_id and q['dimension'] == 'Enterprising'), None)
            if question:
                enterprising_responses[question_id] = response
        
        if not enterprising_responses:
            return 0.0
        
        total_score = sum(self._calculate_question_score(response, 'agreement') for response in enterprising_responses.values())
        return total_score / len(enterprising_responses)
    
    def score_conventional_dimension(self, responses: Dict[str, Any]) -> float:
        """Score Conventional dimension from responses."""
        conventional_responses = {}
        for question_id, response in responses.items():
            question = next((q for q in self.assessment_questions if q['id'] == question_id and q['dimension'] == 'Conventional'), None)
            if question:
                conventional_responses[question_id] = response
        
        if not conventional_responses:
            return 0.0
        
        total_score = sum(self._calculate_question_score(response, 'agreement') for response in conventional_responses.values())
        return total_score / len(conventional_responses)
    
    def get_assessment_questions(self) -> List[Dict[str, Any]]:
        """Get all assessment questions."""
        return self.assessment_questions
    
    def get_career_database(self) -> List[Dict[str, Any]]:
        """Get career database."""
        return self.career_database

# Example usage and testing
if __name__ == "__main__":
    # Initialize analyzer
    analyzer = RIASECAnalyzer()
    
    # Sample assessment responses
    sample_responses = {
        'R1': 4,  # Agree
        'R2': 3,  # Neutral
        'R3': 5,  # Strongly Agree
        'R4': 4,  # Agree
        'R5': 4,  # Agree
        'R6': 2,  # Disagree
        'I1': 5,  # Strongly Agree
        'I2': 4,  # Agree
        'I3': 4,  # Agree
        'I4': 3,  # Neutral
        'I5': 5,  # Strongly Agree
        'I6': 3,  # Neutral
        'A1': 2,  # Disagree
        'A2': 3,  # Neutral
        'A3': 2,  # Disagree
        'A4': 3,  # Neutral
        'A5': 2,  # Disagree
        'A6': 3,  # Neutral
        'S1': 3,  # Neutral
        'S2': 4,  # Agree
        'S3': 3,  # Neutral
        'S4': 3,  # Neutral
        'S5': 3,  # Neutral
        'S6': 3,  # Neutral
        'E1': 4,  # Agree
        'E2': 3,  # Neutral
        'E3': 3,  # Neutral
        'E4': 3,  # Neutral
        'E5': 4,  # Agree
        'E6': 3,  # Neutral
        'C1': 4,  # Agree
        'C2': 5,  # Strongly Agree
        'C3': 4,  # Agree
        'C4': 4,  # Agree
        'C5': 5,  # Strongly Agree
        'C6': 4   # Agree
    }
    
    # Analyze responses
    print("=== RIASEC Personality Assessment Analysis ===")
    analysis = analyzer.analyze_responses(sample_responses)
    
    print(f"RIASEC Scores: {analysis['riasec_scores']}")
    print(f"Primary Type: {analysis['personality_profile'].primary_type}")
    print(f"Secondary Type: {analysis['personality_profile'].secondary_type}")
    print(f"Strengths: {analysis['personality_profile'].strengths}")
    print(f"Communication Style: {analysis['personality_profile'].communication_style}")
    
    print("\n=== Top Career Matches ===")
    for i, match in enumerate(analysis['career_matches'][:5], 1):
        print(f"{i}. {match.career_name} - {match.match_percentage:.1f}% match")
        print(f"   Explanation: {match.explanation}")
        print(f"   Indian Context: {match.indian_relevance}")
        print()
    
    print("=== Visualization Data ===")
    print(f"Radar Chart Labels: {analysis['visualization_data']['radar_chart']['labels']}")
    print(f"Career Match Percentages: {analysis['visualization_data']['career_matches']['percentages'][:5]}")
    
    print("\n=== Assessment Summary ===")
    summary = analysis['assessment_summary']
    print(f"Total Questions: {summary['total_questions']}")
    print(f"Career Clusters: {summary['career_clusters']}")
    print(f"Indian Context: {summary['indian_context']}")