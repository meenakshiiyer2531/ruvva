"""
Main career recommendation engine
"""

from typing import Dict, List, Any, Optional
import json
import logging
from utils.logger import get_logger
from .riasec_analyzer import RIASECAnalyzer
from .cosine_matcher import CosineMatcher
from .gemini_client import GeminiClient

logger = get_logger(__name__)

class CareerRecommender:
    """Main career recommendation engine"""
    
    def __init__(self):
        """Initialize career recommender"""
        self.riasec_analyzer = RIASECAnalyzer()
        self.cosine_matcher = CosineMatcher()
        self.gemini_client = GeminiClient()
        
    def generate_career_recommendations(self, 
                                     student_profile: Dict[str, Any], 
                                     career_database: List[Dict[str, Any]],
                                     preferences: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate comprehensive career recommendations"""
        try:
            # Analyze student profile
            profile_analysis = self._analyze_student_profile(student_profile)
            
            # Find career matches
            career_matches = self.cosine_matcher.find_top_career_matches(
                student_profile, career_database, top_n=10
            )
            
            # Generate AI insights
            ai_insights = self._generate_ai_insights(student_profile, career_matches)
            
            # Apply preferences if provided
            if preferences:
                career_matches = self._apply_preferences(career_matches, preferences)
            
            # Generate recommendations
            recommendations = {
                'profile_analysis': profile_analysis,
                'career_matches': [
                    {
                        'career': match[0],
                        'match_score': match[1],
                        'explanation': self.cosine_matcher.get_match_explanation(student_profile, match[0])
                    }
                    for match in career_matches
                ],
                'ai_insights': ai_insights,
                'next_steps': self._generate_next_steps(student_profile, career_matches),
                'learning_recommendations': self._generate_learning_recommendations(student_profile, career_matches)
            }
            
            return recommendations
        except Exception as e:
            logger.error(f"Error generating career recommendations: {str(e)}")
            raise
    
    def analyze_career_fit(self, 
                         student_profile: Dict[str, Any], 
                         career_id: str,
                         career_database: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze fit for a specific career"""
        try:
            # Find career in database
            career = next((c for c in career_database if c.get('id') == career_id), None)
            if not career:
                raise ValueError(f"Career with ID {career_id} not found")
            
            # Calculate match score
            match_score = self.cosine_matcher.calculate_career_match_score(student_profile, career)
            
            # Get detailed explanation
            explanation = self.cosine_matcher.get_match_explanation(student_profile, career)
            
            # Generate AI analysis
            ai_analysis = self.gemini_client.generate_career_advice(
                student_profile, 
                f"Analyze my fit for {career.get('title', 'this career')}",
                f"Match score: {match_score:.2f}"
            )
            
            return {
                'career': career,
                'match_score': match_score,
                'explanation': explanation,
                'ai_analysis': ai_analysis,
                'recommendations': self._generate_career_specific_recommendations(student_profile, career)
            }
        except Exception as e:
            logger.error(f"Error analyzing career fit: {str(e)}")
            raise
    
    def suggest_career_transitions(self, 
                                 current_career: str,
                                 student_profile: Dict[str, Any],
                                 career_database: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Suggest career transitions from current career"""
        try:
            # Find current career
            current_career_data = next((c for c in career_database if c.get('title', '').lower() == current_career.lower()), None)
            
            if not current_career_data:
                # If current career not found, use student profile
                current_career_data = student_profile
            
            # Find transition opportunities
            transition_careers = []
            for career in career_database:
                if career.get('title', '').lower() != current_career.lower():
                    match_score = self.cosine_matcher.calculate_career_match_score(student_profile, career)
                    transition_careers.append((career, match_score))
            
            # Sort by match score
            transition_careers.sort(key=lambda x: x[1], reverse=True)
            
            # Generate AI insights for transitions
            ai_insights = self.gemini_client.generate_career_advice(
                student_profile,
                f"What are the best career transition options from {current_career}?",
                f"Current skills: {', '.join(student_profile.get('skills', []))}"
            )
            
            return {
                'current_career': current_career,
                'transition_options': [
                    {
                        'career': career,
                        'match_score': score,
                        'transition_difficulty': self._calculate_transition_difficulty(current_career_data, career),
                        'explanation': self.cosine_matcher.get_match_explanation(student_profile, career)
                    }
                    for career, score in transition_careers[:10]
                ],
                'ai_insights': ai_insights,
                'transition_strategy': self._generate_transition_strategy(student_profile, transition_careers[:5])
            }
        except Exception as e:
            logger.error(f"Error suggesting career transitions: {str(e)}")
            raise
    
    def _analyze_student_profile(self, student_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze student profile for insights"""
        try:
            analysis = {
                'riasec_analysis': {},
                'skills_analysis': {},
                'interests_analysis': {},
                'overall_insights': {}
            }
            
            # RIASEC analysis
            if 'riasec_scores' in student_profile:
                analysis['riasec_analysis'] = self.riasec_analyzer.analyze_personality_profile(
                    student_profile['riasec_scores']
                )
            
            # Skills analysis
            skills = student_profile.get('skills', [])
            analysis['skills_analysis'] = {
                'skill_count': len(skills),
                'skill_categories': self._categorize_skills(skills),
                'strengths': self._identify_skill_strengths(skills)
            }
            
            # Interests analysis
            interests = student_profile.get('interests', [])
            analysis['interests_analysis'] = {
                'interest_count': len(interests),
                'interest_categories': self._categorize_interests(interests),
                'dominant_themes': self._identify_interest_themes(interests)
            }
            
            # Overall insights
            analysis['overall_insights'] = {
                'profile_completeness': self._calculate_profile_completeness(student_profile),
                'career_readiness': self._assess_career_readiness(student_profile),
                'development_priorities': self._identify_development_priorities(student_profile)
            }
            
            return analysis
        except Exception as e:
            logger.error(f"Error analyzing student profile: {str(e)}")
            return {}
    
    def _generate_ai_insights(self, 
                            student_profile: Dict[str, Any], 
                            career_matches: List[tuple]) -> Dict[str, Any]:
        """Generate AI-powered insights"""
        try:
            top_careers = [match[0]['title'] for match in career_matches[:3]]
            
            insights = self.gemini_client.generate_career_advice(
                student_profile,
                f"Based on my profile, what are the key insights about my career path? Top matches: {', '.join(top_careers)}"
            )
            
            return {
                'career_insights': insights,
                'market_trends': self._get_market_trends(top_careers),
                'growth_opportunities': self._identify_growth_opportunities(student_profile, career_matches)
            }
        except Exception as e:
            logger.error(f"Error generating AI insights: {str(e)}")
            return {}
    
    def _apply_preferences(self, 
                         career_matches: List[tuple], 
                         preferences: Dict[str, Any]) -> List[tuple]:
        """Apply user preferences to career matches"""
        try:
            # Filter by salary range
            if 'salary_range' in preferences:
                min_salary = preferences['salary_range'].get('min', 0)
                max_salary = preferences['salary_range'].get('max', float('inf'))
                
                career_matches = [
                    match for match in career_matches
                    if min_salary <= match[0].get('salary', {}).get('median', 0) <= max_salary
                ]
            
            # Filter by location
            if 'location' in preferences:
                preferred_location = preferences['location'].lower()
                career_matches = [
                    match for match in career_matches
                    if preferred_location in match[0].get('location', '').lower()
                ]
            
            # Filter by work_environment
            if 'work_environment' in preferences:
                preferred_env = preferences['work_environment'].lower()
                career_matches = [
                    match for match in career_matches
                    if preferred_env in match[0].get('work_environment', '').lower()
                ]
            
            return career_matches
        except Exception as e:
            logger.error(f"Error applying preferences: {str(e)}")
            return career_matches
    
    def _generate_next_steps(self, 
                           student_profile: Dict[str, Any], 
                           career_matches: List[tuple]) -> List[str]:
        """Generate actionable next steps"""
        steps = []
        
        # Based on top career match
        if career_matches:
            top_career = career_matches[0][0]
            steps.append(f"Research {top_career.get('title', 'your top career match')} in detail")
            steps.append("Identify skill gaps and create a learning plan")
            steps.append("Connect with professionals in your target field")
        
        # General steps
        steps.extend([
            "Complete additional assessments to refine your profile",
            "Build a professional network in your areas of interest",
            "Gain practical experience through internships or projects",
            "Create a career development timeline with milestones"
        ])
        
        return steps
    
    def _generate_learning_recommendations(self, 
                                         student_profile: Dict[str, Any], 
                                         career_matches: List[tuple]) -> Dict[str, Any]:
        """Generate learning recommendations"""
        try:
            if not career_matches:
                return {}
            
            # Get skills needed for top careers
            top_careers = career_matches[:3]
            required_skills = set()
            
            for career, _ in top_careers:
                required_skills.update(career.get('required_skills', []))
            
            # Generate AI learning recommendations
            learning_recs = self.gemini_client.generate_learning_recommendations(
                [match[0].get('title', '') for match, _ in top_careers],
                student_profile.get('skills', []),
                student_profile.get('learning_style', 'visual')
            )
            
            return learning_recs
        except Exception as e:
            logger.error(f"Error generating learning recommendations: {str(e)}")
            return {}
    
    def _generate_career_specific_recommendations(self, 
                                               student_profile: Dict[str, Any], 
                                               career: Dict[str, Any]) -> List[str]:
        """Generate career-specific recommendations"""
        recommendations = []
        
        # Skills recommendations
        student_skills = [skill.lower() for skill in student_profile.get('skills', [])]
        required_skills = [skill.lower() for skill in career.get('required_skills', [])]
        
        missing_skills = set(required_skills) - set(student_skills)
        if missing_skills:
            recommendations.append(f"Develop these skills: {', '.join(list(missing_skills)[:3])}")
        
        # Education recommendations
        if career.get('education_requirements'):
            recommendations.append(f"Consider {career['education_requirements']} education")
        
        # Experience recommendations
        if career.get('experience_required'):
            recommendations.append("Gain relevant work experience")
        
        return recommendations
    
    def _calculate_transition_difficulty(self, 
                                       current_career: Dict[str, Any], 
                                       target_career: Dict[str, Any]) -> str:
        """Calculate difficulty of career transition"""
        # Simple heuristic based on skill overlap
        current_skills = set([skill.lower() for skill in current_career.get('required_skills', [])])
        target_skills = set([skill.lower() for skill in target_career.get('required_skills', [])])
        
        overlap = len(current_skills & target_skills)
        total_skills = len(current_skills | target_skills)
        
        if total_skills == 0:
            return "unknown"
        
        similarity = overlap / total_skills
        
        if similarity > 0.7:
            return "easy"
        elif similarity > 0.4:
            return "moderate"
        else:
            return "difficult"
    
    def _generate_transition_strategy(self, 
                                   student_profile: Dict[str, Any], 
                                   transition_careers: List[tuple]) -> Dict[str, Any]:
        """Generate transition strategy"""
        return {
            'immediate_steps': [
                "Assess current skills and identify transferable ones",
                "Research target careers and their requirements",
                "Network with professionals in target fields"
            ],
            'short_term_goals': [
                "Develop missing skills through courses or projects",
                "Gain relevant experience through side projects",
                "Build a portfolio showcasing relevant work"
            ],
            'long_term_goals': [
                "Secure entry-level position in target field",
                "Continue professional development",
                "Advance to senior roles"
            ]
        }
    
    def _categorize_skills(self, skills: List[str]) -> Dict[str, List[str]]:
        """Categorize skills into groups"""
        categories = {
            'technical': [],
            'soft': [],
            'creative': [],
            'analytical': [],
            'leadership': []
        }
        
        for skill in skills:
            skill_lower = skill.lower()
            if any(tech in skill_lower for tech in ['programming', 'coding', 'software', 'technical']):
                categories['technical'].append(skill)
            elif any(soft in skill_lower for soft in ['communication', 'teamwork', 'leadership']):
                categories['soft'].append(skill)
            elif any(creative in skill_lower for creative in ['design', 'creative', 'artistic']):
                categories['creative'].append(skill)
            elif any(analytical in skill_lower for analytical in ['analysis', 'data', 'research']):
                categories['analytical'].append(skill)
            else:
                categories['soft'].append(skill)  # Default to soft skills
        
        return categories
    
    def _categorize_interests(self, interests: List[str]) -> Dict[str, List[str]]:
        """Categorize interests into themes"""
        themes = {
            'technology': [],
            'business': [],
            'creative': [],
            'healthcare': [],
            'education': [],
            'other': []
        }
        
        for interest in interests:
            interest_lower = interest.lower()
            if any(tech in interest_lower for tech in ['technology', 'computing', 'software']):
                themes['technology'].append(interest)
            elif any(business in interest_lower for business in ['business', 'finance', 'marketing']):
                themes['business'].append(interest)
            elif any(creative in interest_lower for creative in ['art', 'design', 'music']):
                themes['creative'].append(interest)
            elif any(health in interest_lower for health in ['health', 'medical', 'wellness']):
                themes['healthcare'].append(interest)
            elif any(edu in interest_lower for edu in ['education', 'teaching', 'learning']):
                themes['education'].append(interest)
            else:
                themes['other'].append(interest)
        
        return themes
    
    def _identify_skill_strengths(self, skills: List[str]) -> List[str]:
        """Identify skill strengths"""
        # Simple heuristic - skills mentioned multiple times or with strong keywords
        strengths = []
        for skill in skills:
            if len(skill.split()) > 1:  # Multi-word skills often indicate depth
                strengths.append(skill)
        return strengths[:5]  # Top 5 strengths
    
    def _identify_interest_themes(self, interests: List[str]) -> List[str]:
        """Identify dominant interest themes"""
        themes = self._categorize_interests(interests)
        dominant_themes = [theme for theme, interest_list in themes.items() if len(interest_list) > 0]
        return dominant_themes[:3]  # Top 3 themes
    
    def _calculate_profile_completeness(self, student_profile: Dict[str, Any]) -> float:
        """Calculate profile completeness score"""
        required_fields = ['skills', 'interests', 'education_level']
        optional_fields = ['riasec_scores', 'career_goals', 'work_experience']
        
        required_score = sum(1 for field in required_fields if student_profile.get(field)) / len(required_fields)
        optional_score = sum(1 for field in optional_fields if student_profile.get(field)) / len(optional_fields)
        
        return (required_score * 0.7) + (optional_score * 0.3)
    
    def _assess_career_readiness(self, student_profile: Dict[str, Any]) -> str:
        """Assess career readiness level"""
        skills_count = len(student_profile.get('skills', []))
        experience = student_profile.get('work_experience', [])
        
        if skills_count >= 10 and len(experience) >= 2:
            return "high"
        elif skills_count >= 5 and len(experience) >= 1:
            return "medium"
        else:
            return "developing"
    
    def _identify_development_priorities(self, student_profile: Dict[str, Any]) -> List[str]:
        """Identify development priorities"""
        priorities = []
        
        if len(student_profile.get('skills', [])) < 5:
            priorities.append("Develop core skills")
        
        if not student_profile.get('work_experience'):
            priorities.append("Gain work experience")
        
        if not student_profile.get('riasec_scores'):
            priorities.append("Complete personality assessment")
        
        return priorities
    
    def _get_market_trends(self, careers: List[str]) -> Dict[str, Any]:
        """Get market trends for careers"""
        # This would typically connect to external APIs or databases
        return {
            'growth_rate': 'positive',
            'demand_level': 'high',
            'salary_trends': 'increasing',
            'remote_work': 'available'
        }
    
    def _identify_growth_opportunities(self, 
                                     student_profile: Dict[str, Any], 
                                     career_matches: List[tuple]) -> List[str]:
        """Identify growth opportunities"""
        opportunities = []
        
        for career, score in career_matches[:3]:
            if score > 0.8:
                opportunities.append(f"Strong match with {career.get('title', 'career')}")
        
        return opportunities
