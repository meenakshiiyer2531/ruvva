"""
Career Discovery Service for CareerConnect AI
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class CareerInfo:
    """Career information structure."""
    career_id: str
    title: str
    description: str
    required_education: List[str]
    essential_skills: List[str]
    salary_ranges: Dict[str, Dict[str, int]]
    industry: str
    indian_context: Dict[str, Any]

@dataclass
class CareerMatch:
    """Career matching result."""
    career_id: str
    match_score: float
    match_reasons: List[str]
    skill_gaps: List[str]

@dataclass
class CareerDiscoveryResult:
    """Career discovery result."""
    primary_matches: List[CareerMatch]
    alternative_careers: List[CareerMatch]
    recommendations: List[str]
    discovery_timestamp: datetime

class CareerDiscoveryService:
    """Career discovery service for Indian students."""
    
    def __init__(self):
        """Initialize service."""
        self.career_database = self._load_career_database()
        self.career_categories = self._initialize_career_categories()
        self.skill_mappings = self._initialize_skill_mappings()
        self.industry_mappings = self._initialize_industry_mappings()
        self.matching_weights = self._initialize_matching_weights()
        self.trending_careers = self._initialize_trending_careers()
        logger.info("CareerDiscoveryService initialized")
    
    def discover_careers_by_profile(self, student_profile: Dict[str, Any]) -> CareerDiscoveryResult:
        """Discover careers by profile."""
        try:
            logger.info("Starting career discovery by profile")
            
            # Extract profile components
            academic_info = student_profile.get('academic_info', {})
            skills = student_profile.get('skill_assessments', {})
            interests = student_profile.get('interests', [])
            riasec_scores = student_profile.get('riasec_scores', {})
            preferences = student_profile.get('preferences', {})
            
            # Perform multi-factor career matching
            primary_matches = self._match_careers_by_profile(
                academic_info, skills, interests, riasec_scores, preferences
            )
            
            # Find alternative career paths
            alternative_careers = self._find_alternative_careers(primary_matches, preferences)
            
            # Generate recommendations
            recommendations = self._generate_discovery_recommendations(primary_matches)
            
            return CareerDiscoveryResult(
                primary_matches=primary_matches,
                alternative_careers=alternative_careers,
                recommendations=recommendations,
                discovery_timestamp=datetime.utcnow()
            )
            
        except Exception as e:
            logger.error(f"Error in career discovery by profile: {e}")
            raise Exception(f"Failed to discover careers: {e}")
    
    def search_careers_by_keywords(self, search_terms: List[str]) -> List[CareerMatch]:
        """Search careers by keywords."""
        try:
            logger.info(f"Searching careers by keywords: {search_terms}")
            
            matches = []
            search_terms_lower = [term.lower() for term in search_terms]
            
            for career_id, career in self.career_database.items():
                match_score = self._calculate_keyword_match_score(career, search_terms_lower)
                
                if match_score > 0.3:  # Threshold for relevance
                    match_reasons = self._generate_keyword_match_reasons(career, search_terms_lower)
                    
                    match = CareerMatch(
                        career_id=career_id,
                        match_score=match_score,
                        match_reasons=match_reasons,
                        skill_gaps=[]
                    )
                    matches.append(match)
            
            # Sort by match score
            matches.sort(key=lambda x: x.match_score, reverse=True)
            return matches[:20]  # Return top 20 matches
            
        except Exception as e:
            logger.error(f"Error in keyword search: {e}")
            return []
    
    def get_career_details(self, career_id: str) -> Optional[CareerInfo]:
        """Get career details."""
        return self.career_database.get(career_id)
    
    def find_similar_careers(self, career_id: str) -> List[CareerMatch]:
        """Find similar careers."""
        try:
            logger.info(f"Finding similar careers for: {career_id}")
            
            if career_id not in self.career_database:
                logger.warning(f"Career not found: {career_id}")
                return []
            
            base_career = self.career_database[career_id]
            similar_careers = []
            
            for other_id, other_career in self.career_database.items():
                if other_id == career_id:
                    continue
                
                similarity_score = self._calculate_career_similarity(base_career, other_career)
                
                if similarity_score > 0.6:  # High similarity threshold
                    match_reasons = self._generate_similarity_reasons(base_career, other_career)
                    
                    match = CareerMatch(
                        career_id=other_id,
                        match_score=similarity_score,
                        match_reasons=match_reasons,
                        skill_gaps=[]
                    )
                    similar_careers.append(match)
            
            # Sort by similarity score
            similar_careers.sort(key=lambda x: x.match_score, reverse=True)
            return similar_careers[:10]  # Return top 10 similar careers
            
        except Exception as e:
            logger.error(f"Error finding similar careers: {e}")
            return []
    
    def get_trending_careers(self, timeframe: str = "1year") -> List[CareerInfo]:
        """Get trending careers."""
        try:
            logger.info(f"Getting trending careers for timeframe: {timeframe}")
            
            trending_careers = []
            for career_id, career in self.career_database.items():
                if career.indian_context.get('trending', False):
                    trending_careers.append(career)
            
            # Sort by growth rate
            trending_careers.sort(key=lambda x: x.indian_context.get('growth_rate', 0), reverse=True)
            return trending_careers[:20]  # Return top 20 trending careers
            
        except Exception as e:
            logger.error(f"Error getting trending careers: {e}")
            return []
    
    def get_career_database(self) -> Dict[str, CareerInfo]:
        """Get career database."""
        return self.career_database
    
    def get_career_categories(self) -> Dict[str, List[str]]:
        """Get career categories."""
        return self.career_categories
    
    def get_skill_mappings(self) -> Dict[str, List[str]]:
        """Get skill mappings."""
        return self.skill_mappings
    
    def get_industry_mappings(self) -> Dict[str, List[str]]:
        """Get industry mappings."""
        return self.industry_mappings
    
    def analyze_career_growth(self, career_id: str) -> Dict[str, Any]:
        """Analyze career growth."""
        try:
            logger.info(f"Analyzing career growth for: {career_id}")
            
            if career_id not in self.career_database:
                logger.warning(f"Career not found: {career_id}")
                return {}
            
            career = self.career_database[career_id]
            indian_context = career.indian_context
            
            return {
                'growth_rate': indian_context.get('growth_rate', 0.0),
                'market_demand': indian_context.get('market_demand', 'stable'),
                'future_outlook': indian_context.get('future_outlook', 'positive'),
                'trending': indian_context.get('trending', False),
                'top_companies': indian_context.get('top_companies', []),
                'growth_cities': indian_context.get('cities', [])
            }
            
        except Exception as e:
            logger.error(f"Error analyzing career growth: {e}")
            return {}
    
    def _load_career_database(self) -> Dict[str, CareerInfo]:
        """Load career database."""
        return {
            'software_engineer': CareerInfo(
                career_id='software_engineer',
                title='Software Engineer',
                description='Design and develop software applications and systems',
                required_education=['Bachelor in Computer Science', 'Bachelor in Engineering'],
                essential_skills=['Programming', 'Problem Solving', 'Data Structures', 'Algorithms'],
                salary_ranges={
                    'entry': {'min': 300000, 'max': 600000},
                    'mid': {'min': 600000, 'max': 1200000},
                    'senior': {'min': 1200000, 'max': 2500000}
                },
                industry='Technology',
                indian_context={
                    'trending': True,
                    'growth_rate': 0.15,
                    'market_demand': 'high',
                    'future_outlook': 'excellent',
                    'top_companies': ['TCS', 'Infosys', 'Wipro', 'Google', 'Microsoft'],
                    'cities': ['Bangalore', 'Hyderabad', 'Pune', 'Chennai', 'Mumbai']
                }
            ),
            'data_scientist': CareerInfo(
                career_id='data_scientist',
                title='Data Scientist',
                description='Analyze data to extract insights and build predictive models',
                required_education=['Bachelor in Statistics', 'Master in Data Science', 'Bachelor in Mathematics'],
                essential_skills=['Statistics', 'Machine Learning', 'Python', 'R', 'SQL'],
                salary_ranges={
                    'entry': {'min': 400000, 'max': 800000},
                    'mid': {'min': 800000, 'max': 1500000},
                    'senior': {'min': 1500000, 'max': 3000000}
                },
                industry='Technology',
                indian_context={
                    'trending': True,
                    'growth_rate': 0.20,
                    'market_demand': 'very_high',
                    'future_outlook': 'excellent',
                    'top_companies': ['Amazon', 'Flipkart', 'Paytm', 'Ola', 'Uber'],
                    'cities': ['Bangalore', 'Mumbai', 'Delhi', 'Hyderabad', 'Pune']
                }
            ),
            'doctor': CareerInfo(
                career_id='doctor',
                title='Doctor',
                description='Diagnose and treat medical conditions, provide healthcare services',
                required_education=['MBBS', 'MD/MS for specialization'],
                essential_skills=['Medical Knowledge', 'Communication', 'Empathy', 'Problem Solving'],
                salary_ranges={
                    'entry': {'min': 200000, 'max': 500000},
                    'mid': {'min': 500000, 'max': 1000000},
                    'senior': {'min': 1000000, 'max': 2000000}
                },
                industry='Healthcare',
                indian_context={
                    'trending': False,
                    'growth_rate': 0.08,
                    'market_demand': 'high',
                    'future_outlook': 'stable',
                    'top_companies': ['Apollo Hospitals', 'Fortis Healthcare', 'Max Healthcare'],
                    'cities': ['Delhi', 'Mumbai', 'Bangalore', 'Chennai', 'Kolkata']
                }
            )
        }
    
    def _initialize_career_categories(self) -> Dict[str, List[str]]:
        """Initialize career categories."""
        return {
            'Technology': ['Software Engineer', 'Data Scientist', 'AI Engineer'],
            'Healthcare': ['Doctor', 'Nurse', 'Pharmacist'],
            'Business': ['Business Analyst', 'Management Consultant', 'Entrepreneur']
        }
    
    def _initialize_skill_mappings(self) -> Dict[str, List[str]]:
        """Initialize skill mappings."""
        return {
            'Programming': ['Software Engineer', 'Data Scientist', 'AI Engineer'],
            'Communication': ['Business Analyst', 'Management Consultant', 'Doctor'],
            'Problem Solving': ['Software Engineer', 'Data Scientist', 'Business Analyst']
        }
    
    def _initialize_industry_mappings(self) -> Dict[str, List[str]]:
        """Initialize industry mappings."""
        return {
            'Technology': ['Software Engineer', 'Data Scientist', 'AI Engineer'],
            'Healthcare': ['Doctor', 'Nurse', 'Pharmacist'],
            'Finance': ['Business Analyst', 'Management Consultant', 'Financial Analyst']
        }
    
    def _initialize_matching_weights(self) -> Dict[str, float]:
        """Initialize matching weights."""
        return {
            'skills': 0.4,
            'interests': 0.3,
            'education': 0.2,
            'personality': 0.1
        }
    
    def _initialize_trending_careers(self) -> List[str]:
        """Initialize trending careers."""
        return ['Data Scientist', 'AI Engineer', 'Cybersecurity Analyst']
    
    def _match_careers_by_profile(self, academic_info: Dict[str, Any], skills: Dict[str, Any], 
                                 interests: List[str], riasec_scores: Dict[str, float], 
                                 preferences: Dict[str, Any]) -> List[CareerMatch]:
        """Match careers by profile."""
        matches = []
        
        for career_id, career in self.career_database.items():
            match_score = 0.0
            match_reasons = []
            
            # Skills matching (40% weight)
            if skills:
                skill_match = self._calculate_skill_match(career.essential_skills, skills)
                match_score += skill_match * self.matching_weights['skills']
                if skill_match > 0.5:
                    match_reasons.append("Strong skill alignment")
            
            # Interests matching (30% weight)
            if interests:
                interest_match = self._calculate_interest_match(career.industry, interests)
                match_score += interest_match * self.matching_weights['interests']
                if interest_match > 0.5:
                    match_reasons.append("Interest alignment")
            
            # Education matching (20% weight)
            if academic_info:
                education_match = self._calculate_education_match(career.required_education, academic_info)
                match_score += education_match * self.matching_weights['education']
                if education_match > 0.5:
                    match_reasons.append("Education alignment")
            
            # Personality matching (10% weight)
            if riasec_scores:
                personality_match = self._calculate_personality_match(career, riasec_scores)
                match_score += personality_match * self.matching_weights['personality']
                if personality_match > 0.5:
                    match_reasons.append("Personality fit")
            
            if match_score > 0.4:  # Threshold for relevance
                skill_gaps = self._identify_skill_gaps(career.essential_skills, skills)
                
                match = CareerMatch(
                    career_id=career_id,
                    match_score=match_score,
                    match_reasons=match_reasons,
                    skill_gaps=skill_gaps
                )
                matches.append(match)
        
        # Sort by match score
        matches.sort(key=lambda x: x.match_score, reverse=True)
        return matches[:10]  # Return top 10 matches
    
    def _find_alternative_careers(self, primary_matches: List[CareerMatch], preferences: Dict[str, Any]) -> List[CareerMatch]:
        """Find alternative career paths."""
        alternatives = []
        
        for match in primary_matches:
            similar = self.find_similar_careers(match.career_id)
            alternatives.extend(similar)
        
        # Remove duplicates and sort
        unique_alternatives = {}
        for alt in alternatives:
            if alt.career_id not in unique_alternatives:
                unique_alternatives[alt.career_id] = alt
        
        return list(unique_alternatives.values())[:5]
    
    def _generate_discovery_recommendations(self, matches: List[CareerMatch]) -> List[str]:
        """Generate discovery recommendations."""
        recommendations = []
        
        if matches:
            top_match = matches[0]
            career = self.career_database[top_match.career_id]
            recommendations.append(f"Consider {career.title} as your primary career choice")
            
            if top_match.skill_gaps:
                recommendations.append(f"Develop skills in: {', '.join(top_match.skill_gaps[:3])}")
            
            if career.indian_context.get('trending', False):
                recommendations.append(f"{career.title} is a trending career with excellent growth prospects")
        
        recommendations.append("Research career requirements and market trends")
        recommendations.append("Connect with professionals in your field of interest")
        
        return recommendations
    
    def _calculate_skill_match(self, required_skills: List[str], user_skills: Dict[str, Any]) -> float:
        """Calculate skill match score."""
        if not user_skills or not required_skills:
            return 0.0
        
        user_skill_list = list(user_skills.keys())
        matches = len(set(required_skills) & set(user_skill_list))
        return matches / len(required_skills)
    
    def _calculate_interest_match(self, industry: str, interests: List[str]) -> float:
        """Calculate interest match score."""
        if not interests:
            return 0.0
        
        industry_keywords = {
            'Technology': ['technology', 'software', 'programming', 'data', 'ai', 'computer'],
            'Healthcare': ['medicine', 'health', 'biology', 'medical', 'healthcare'],
            'Business': ['business', 'finance', 'management', 'marketing', 'commerce']
        }
        
        if industry not in industry_keywords:
            return 0.0
        
        keywords = industry_keywords[industry]
        matches = sum(1 for interest in interests if any(keyword in interest.lower() for keyword in keywords))
        return matches / len(interests)
    
    def _calculate_education_match(self, required_education: List[str], academic_info: Dict[str, Any]) -> float:
        """Calculate education match score."""
        # Simple heuristic based on stream
        stream = academic_info.get('stream', '').lower()
        
        if 'science' in stream and any('engineering' in edu.lower() or 'computer' in edu.lower() for edu in required_education):
            return 0.8
        elif 'commerce' in stream and any('business' in edu.lower() or 'commerce' in edu.lower() for edu in required_education):
            return 0.8
        elif 'arts' in stream and any('arts' in edu.lower() or 'humanities' in edu.lower() for edu in required_education):
            return 0.8
        
        return 0.3  # Base match
    
    def _calculate_personality_match(self, career: CareerInfo, riasec_scores: Dict[str, float]) -> float:
        """Calculate personality match score."""
        # Simple heuristic based on industry
        industry_personality_map = {
            'Technology': ['Investigative', 'Realistic'],
            'Healthcare': ['Social', 'Investigative'],
            'Business': ['Enterprising', 'Conventional']
        }
        
        if career.industry not in industry_personality_map:
            return 0.5
        
        preferred_types = industry_personality_map[career.industry]
        max_score = max(riasec_scores.get(ptype, 0) for ptype in preferred_types)
        return max_score / 5.0  # Normalize to 0-1
    
    def _identify_skill_gaps(self, required_skills: List[str], user_skills: Dict[str, Any]) -> List[str]:
        """Identify skill gaps."""
        if not user_skills:
            return required_skills[:3]
        
        user_skill_list = list(user_skills.keys())
        gaps = [skill for skill in required_skills if skill not in user_skill_list]
        return gaps[:3]
    
    def _calculate_keyword_match_score(self, career: CareerInfo, search_terms: List[str]) -> float:
        """Calculate keyword match score."""
        career_text = f"{career.title} {career.description} {career.industry}".lower()
        matches = sum(1 for term in search_terms if term.lower() in career_text)
        return matches / len(search_terms) if search_terms else 0.0
    
    def _generate_keyword_match_reasons(self, career: CareerInfo, search_terms: List[str]) -> List[str]:
        """Generate keyword match reasons."""
        reasons = []
        career_text = f"{career.title} {career.description} {career.industry}".lower()
        
        for term in search_terms:
            if term.lower() in career_text:
                if term.lower() in career.title.lower():
                    reasons.append(f"Career title matches '{term}'")
                elif term.lower() in career.description.lower():
                    reasons.append(f"Description matches '{term}'")
                elif term.lower() in career.industry.lower():
                    reasons.append(f"Industry matches '{term}'")
        
        return reasons
    
    def _calculate_career_similarity(self, career1: CareerInfo, career2: CareerInfo) -> float:
        """Calculate career similarity."""
        # Industry similarity
        industry_match = 1.0 if career1.industry == career2.industry else 0.0
        
        # Skills similarity
        skill_match = len(set(career1.essential_skills) & set(career2.essential_skills)) / max(len(career1.essential_skills), len(career2.essential_skills))
        
        # Education similarity
        education_match = len(set(career1.required_education) & set(career2.required_education)) / max(len(career1.required_education), len(career2.required_education))
        
        # Weighted combination
        return (industry_match * 0.5) + (skill_match * 0.3) + (education_match * 0.2)
    
    def _generate_similarity_reasons(self, career1: CareerInfo, career2: CareerInfo) -> List[str]:
        """Generate similarity reasons."""
        reasons = []
        
        if career1.industry == career2.industry:
            reasons.append(f"Same industry: {career1.industry}")
        
        common_skills = set(career1.essential_skills) & set(career2.essential_skills)
        if common_skills:
            reasons.append(f"Shared skills: {', '.join(list(common_skills)[:3])}")
        
        common_education = set(career1.required_education) & set(career2.required_education)
        if common_education:
            reasons.append(f"Similar education requirements")
        
        return reasons