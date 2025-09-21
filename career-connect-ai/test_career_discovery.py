"""
Test suite for Career Discovery Service
"""

import pytest
from datetime import datetime
from services.career_discovery import (
    CareerDiscoveryService, 
    CareerInfo, 
    CareerMatch, 
    CareerDiscoveryResult
)

class TestCareerDiscoveryService:
    """Test cases for CareerDiscoveryService class."""
    
    @pytest.fixture
    def service(self):
        """Create career discovery service instance for testing."""
        return CareerDiscoveryService()
    
    @pytest.fixture
    def sample_profile(self):
        """Sample student profile for testing."""
        return {
            'academic_info': {
                'stream': 'Science',
                'class_10_marks': {'Mathematics': 90, 'Physics': 85, 'Chemistry': 88},
                'class_12_marks': {'Mathematics': 92, 'Physics': 88, 'Chemistry': 90}
            },
            'skill_assessments': {
                'technical_skills': {
                    'Programming': 4,
                    'Data Analysis': 3,
                    'Problem Solving': 4
                },
                'soft_skills': {
                    'Communication': 3,
                    'Leadership': 2,
                    'Teamwork': 4
                }
            },
            'interests': [
                'Technology', 'Programming', 'Data Science', 'Artificial Intelligence'
            ],
            'riasec_scores': {
                'Realistic': 3.5,
                'Investigative': 4.8,
                'Artistic': 2.1,
                'Social': 3.2,
                'Enterprising': 3.8,
                'Conventional': 4.2
            },
            'preferences': {
                'salary_expectation': 'high',
                'work_location': 'Bangalore',
                'work_environment': 'tech_company'
            }
        }
    
    def test_service_initialization(self, service):
        """Test service initialization."""
        assert service is not None
        assert len(service.career_database) > 0
        assert len(service.career_categories) > 0
        assert len(service.skill_mappings) > 0
        assert len(service.industry_mappings) > 0
        assert len(service.matching_weights) > 0
        assert len(service.trending_careers) > 0
    
    def test_discover_careers_by_profile(self, service, sample_profile):
        """Test career discovery by profile."""
        result = service.discover_careers_by_profile(sample_profile)
        
        assert isinstance(result, CareerDiscoveryResult)
        assert isinstance(result.primary_matches, list)
        assert isinstance(result.alternative_careers, list)
        assert isinstance(result.recommendations, list)
        assert isinstance(result.discovery_timestamp, datetime)
        
        # Should find matches for technology-focused profile
        assert len(result.primary_matches) > 0
        assert len(result.recommendations) > 0
    
    def test_search_careers_by_keywords(self, service):
        """Test keyword-based career search."""
        search_terms = ['software', 'programming', 'technology']
        matches = service.search_careers_by_keywords(search_terms)
        
        assert isinstance(matches, list)
        assert len(matches) > 0
        
        # Check that matches are sorted by score
        for i in range(len(matches) - 1):
            assert matches[i].match_score >= matches[i + 1].match_score
        
        # Check match structure
        for match in matches:
            assert isinstance(match, CareerMatch)
            assert isinstance(match.career_id, str)
            assert isinstance(match.match_score, float)
            assert isinstance(match.match_reasons, list)
            assert isinstance(match.skill_gaps, list)
    
    def test_get_career_details(self, service):
        """Test getting career details."""
        # Test existing career
        career = service.get_career_details('software_engineer')
        assert career is not None
        assert isinstance(career, CareerInfo)
        assert career.career_id == 'software_engineer'
        assert career.title == 'Software Engineer'
        assert isinstance(career.required_education, list)
        assert isinstance(career.essential_skills, list)
        assert isinstance(career.salary_ranges, dict)
        assert isinstance(career.indian_context, dict)
        
        # Test non-existing career
        career = service.get_career_details('non_existing_career')
        assert career is None
    
    def test_find_similar_careers(self, service):
        """Test finding similar careers."""
        similar = service.find_similar_careers('software_engineer')
        
        assert isinstance(similar, list)
        assert len(similar) > 0
        
        # Check that similar careers are sorted by similarity score
        for i in range(len(similar) - 1):
            assert similar[i].match_score >= similar[i + 1].match_score
        
        # Check that no career is similar to itself
        for match in similar:
            assert match.career_id != 'software_engineer'
    
    def test_get_trending_careers(self, service):
        """Test getting trending careers."""
        trending = service.get_trending_careers()
        
        assert isinstance(trending, list)
        assert len(trending) > 0
        
        # Check that all returned careers are trending
        for career in trending:
            assert isinstance(career, CareerInfo)
            assert career.indian_context.get('trending', False)
    
    def test_analyze_career_growth(self, service):
        """Test career growth analysis."""
        growth_analysis = service.analyze_career_growth('software_engineer')
        
        assert isinstance(growth_analysis, dict)
        assert 'growth_rate' in growth_analysis
        assert 'market_demand' in growth_analysis
        assert 'future_outlook' in growth_analysis
        assert 'trending' in growth_analysis
        assert 'top_companies' in growth_analysis
        assert 'growth_cities' in growth_analysis
        
        # Test non-existing career
        growth_analysis = service.analyze_career_growth('non_existing_career')
        assert growth_analysis == {}
    
    def test_calculate_skill_match(self, service):
        """Test skill matching calculation."""
        required_skills = ['Programming', 'Problem Solving', 'Data Structures']
        user_skills = {'Programming': 4, 'Problem Solving': 3, 'Communication': 2}
        
        match_score = service._calculate_skill_match(required_skills, user_skills)
        
        assert isinstance(match_score, float)
        assert 0.0 <= match_score <= 1.0
        assert match_score > 0.5  # Should have good match
    
    def test_calculate_interest_match(self, service):
        """Test interest matching calculation."""
        industry = 'Technology'
        interests = ['Technology', 'Programming', 'Data Science', 'Art']
        
        match_score = service._calculate_interest_match(industry, interests)
        
        assert isinstance(match_score, float)
        assert 0.0 <= match_score <= 1.0
        assert match_score > 0.5  # Should have good match
    
    def test_calculate_education_match(self, service):
        """Test education matching calculation."""
        required_education = ['Bachelor in Computer Science', 'Bachelor in Engineering']
        academic_info = {'stream': 'Science'}
        
        match_score = service._calculate_education_match(required_education, academic_info)
        
        assert isinstance(match_score, float)
        assert 0.0 <= match_score <= 1.0
        assert match_score > 0.5  # Should have good match
    
    def test_calculate_personality_match(self, service):
        """Test personality matching calculation."""
        career = service.career_database['software_engineer']
        riasec_scores = {
            'Realistic': 3.5,
            'Investigative': 4.8,
            'Artistic': 2.1,
            'Social': 3.2,
            'Enterprising': 3.8,
            'Conventional': 4.2
        }
        
        match_score = service._calculate_personality_match(career, riasec_scores)
        
        assert isinstance(match_score, float)
        assert 0.0 <= match_score <= 1.0
    
    def test_identify_skill_gaps(self, service):
        """Test skill gap identification."""
        required_skills = ['Programming', 'Problem Solving', 'Data Structures', 'Algorithms']
        user_skills = {'Programming': 4, 'Problem Solving': 3}
        
        gaps = service._identify_skill_gaps(required_skills, user_skills)
        
        assert isinstance(gaps, list)
        assert len(gaps) <= 3
        assert 'Data Structures' in gaps
        assert 'Algorithms' in gaps
    
    def test_calculate_keyword_match_score(self, service):
        """Test keyword match score calculation."""
        career = service.career_database['software_engineer']
        search_terms = ['software', 'programming', 'technology']
        
        match_score = service._calculate_keyword_match_score(career, search_terms)
        
        assert isinstance(match_score, float)
        assert 0.0 <= match_score <= 1.0
        assert match_score > 0.5  # Should have good match
    
    def test_generate_keyword_match_reasons(self, service):
        """Test keyword match reasons generation."""
        career = service.career_database['software_engineer']
        search_terms = ['software', 'programming']
        
        reasons = service._generate_keyword_match_reasons(career, search_terms)
        
        assert isinstance(reasons, list)
        assert len(reasons) > 0
    
    def test_calculate_career_similarity(self, service):
        """Test career similarity calculation."""
        career1 = service.career_database['software_engineer']
        career2 = service.career_database['data_scientist']
        
        similarity = service._calculate_career_similarity(career1, career2)
        
        assert isinstance(similarity, float)
        assert 0.0 <= similarity <= 1.0
    
    def test_generate_similarity_reasons(self, service):
        """Test similarity reasons generation."""
        career1 = service.career_database['software_engineer']
        career2 = service.career_database['data_scientist']
        
        reasons = service._generate_similarity_reasons(career1, career2)
        
        assert isinstance(reasons, list)
    
    def test_empty_profile_handling(self, service):
        """Test handling of empty profile."""
        empty_profile = {}
        
        result = service.discover_careers_by_profile(empty_profile)
        
        assert isinstance(result, CareerDiscoveryResult)
        assert isinstance(result.primary_matches, list)
        assert isinstance(result.alternative_careers, list)
        assert isinstance(result.recommendations, list)
    
    def test_partial_profile_handling(self, service):
        """Test handling of partial profile."""
        partial_profile = {
            'interests': ['Technology'],
            'skill_assessments': {'technical_skills': {'Programming': 3}}
        }
        
        result = service.discover_careers_by_profile(partial_profile)
        
        assert isinstance(result, CareerDiscoveryResult)
        assert len(result.primary_matches) > 0
    
    def test_career_database_structure(self, service):
        """Test career database structure."""
        database = service.get_career_database()
        
        assert isinstance(database, dict)
        assert len(database) > 0
        
        for career_id, career in database.items():
            assert isinstance(career, CareerInfo)
            assert career.career_id == career_id
            assert isinstance(career.title, str)
            assert isinstance(career.description, str)
            assert isinstance(career.required_education, list)
            assert isinstance(career.essential_skills, list)
            assert isinstance(career.salary_ranges, dict)
            assert isinstance(career.indian_context, dict)
    
    def test_career_categories_structure(self, service):
        """Test career categories structure."""
        categories = service.get_career_categories()
        
        assert isinstance(categories, dict)
        assert len(categories) > 0
        
        for category, careers in categories.items():
            assert isinstance(category, str)
            assert isinstance(careers, list)
            assert len(careers) > 0
    
    def test_skill_mappings_structure(self, service):
        """Test skill mappings structure."""
        mappings = service.get_skill_mappings()
        
        assert isinstance(mappings, dict)
        assert len(mappings) > 0
        
        for skill, careers in mappings.items():
            assert isinstance(skill, str)
            assert isinstance(careers, list)
            assert len(careers) > 0
    
    def test_industry_mappings_structure(self, service):
        """Test industry mappings structure."""
        mappings = service.get_industry_mappings()
        
        assert isinstance(mappings, dict)
        assert len(mappings) > 0
        
        for industry, careers in mappings.items():
            assert isinstance(industry, str)
            assert isinstance(careers, list)
            assert len(careers) > 0

if __name__ == "__main__":
    pytest.main([__file__])
