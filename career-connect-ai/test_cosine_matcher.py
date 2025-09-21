"""
Test suite for Cosine Career Matcher
"""

import pytest
import numpy as np
from core.cosine_matcher import CosineCareerMatcher, ProfileVector, CareerVector, CareerMatch

class TestCosineCareerMatcher:
    """Test cases for CosineCareerMatcher class."""
    
    @pytest.fixture
    def matcher(self):
        """Create cosine career matcher instance for testing."""
        return CosineCareerMatcher()
    
    @pytest.fixture
    def sample_profile(self):
        """Sample student profile for testing."""
        return {
            'academic_subjects': {
                'Mathematics': 'A',
                'Physics': 'A',
                'Computer Science': 'A+',
                'English': 'B'
            },
            'extracurricular_activities': ['Coding', 'Robotics'],
            'technical_skills': {
                'Programming': 'Advanced',
                'Data Analysis': 'Intermediate',
                'Web Development': 'Beginner'
            },
            'soft_skills': {
                'Communication': 'Advanced',
                'Problem Solving': 'Advanced',
                'Leadership': 'Intermediate'
            },
            'riasec_scores': {
                'Realistic': 3.5,
                'Investigative': 4.8,
                'Artistic': 2.1,
                'Social': 3.2,
                'Enterprising': 3.8,
                'Conventional': 4.2
            },
            'interests': ['Technology', 'Science', 'Mathematics'],
            'career_preferences': ['High Salary', 'Career Growth'],
            'location_preferences': ['Bangalore', 'Mumbai'],
            'salary_expectations': '10-15 LPA',
            'work_environment_preferences': ['Office', 'Hybrid']
        }
    
    def test_matcher_initialization(self, matcher):
        """Test matcher initialization."""
        assert matcher is not None
        assert len(matcher.career_database) > 0
        assert len(matcher.dimensions) == 10
        assert len(matcher.career_dimensions) == 8
        assert len(matcher.base_weights) == 10
    
    def test_feature_mappings(self, matcher):
        """Test feature mappings initialization."""
        # Test academic subjects mapping
        assert 'Mathematics' in matcher.academic_subjects_map
        assert 'Physics' in matcher.academic_subjects_map
        assert 'Computer Science' in matcher.academic_subjects_map
        
        # Test technical skills mapping
        assert 'Programming' in matcher.technical_skills_map
        assert 'Data Analysis' in matcher.technical_skills_map
        assert 'Machine Learning' in matcher.technical_skills_map
        
        # Test soft skills mapping
        assert 'Communication' in matcher.soft_skills_map
        assert 'Leadership' in matcher.soft_skills_map
        assert 'Problem Solving' in matcher.soft_skills_map
        
        # Test interests mapping
        assert 'Technology' in matcher.interests_map
        assert 'Science' in matcher.interests_map
        assert 'Mathematics' in matcher.interests_map
    
    def test_calculate_profile_vector(self, matcher, sample_profile):
        """Test profile vector calculation."""
        profile_vector = matcher.calculate_profile_vector(sample_profile)
        
        assert isinstance(profile_vector, ProfileVector)
        assert isinstance(profile_vector.academic_subjects, np.ndarray)
        assert isinstance(profile_vector.technical_skills, np.ndarray)
        assert isinstance(profile_vector.soft_skills, np.ndarray)
        assert isinstance(profile_vector.riasec_scores, np.ndarray)
        assert isinstance(profile_vector.interests, np.ndarray)
        
        # Check dimensions
        assert len(profile_vector.academic_subjects) == 20
        assert len(profile_vector.technical_skills) == 25
        assert len(profile_vector.soft_skills) == 20
        assert len(profile_vector.riasec_scores) == 6
        assert len(profile_vector.interests) == 30
        
        # Check that values are set correctly
        assert profile_vector.academic_subjects[matcher.academic_subjects_map['Mathematics']] > 0
        assert profile_vector.academic_subjects[matcher.academic_subjects_map['Computer Science']] > 0
        assert profile_vector.technical_skills[matcher.technical_skills_map['Programming']] > 0
        assert profile_vector.riasec_scores[1] == 4.8  # Investigative score
    
    def test_calculate_career_vectors(self, matcher):
        """Test career vector calculation."""
        career_vectors = matcher.calculate_career_vectors(matcher.career_database)
        
        assert isinstance(career_vectors, list)
        assert len(career_vectors) == len(matcher.career_database)
        
        for career_name, career_vector in career_vectors:
            assert isinstance(career_name, str)
            assert isinstance(career_vector, CareerVector)
            assert isinstance(career_vector.education_requirements, np.ndarray)
            assert isinstance(career_vector.essential_skills, np.ndarray)
            assert isinstance(career_vector.personality_fit, np.ndarray)
            
            # Check dimensions
            assert len(career_vector.education_requirements) == 20
            assert len(career_vector.essential_skills) == 25
            assert len(career_vector.personality_fit) == 6
    
    def test_compute_cosine_similarity(self, matcher, sample_profile):
        """Test cosine similarity calculation."""
        profile_vector = matcher.calculate_profile_vector(sample_profile)
        career_vectors = matcher.calculate_career_vectors(matcher.career_database)
        
        # Test with first career
        career_name, career_vector = career_vectors[0]
        similarity = matcher.compute_cosine_similarity(profile_vector, career_vector)
        
        assert isinstance(similarity, float)
        assert 0.0 <= similarity <= 1.0
        
        # Test with multiple careers
        similarities = []
        for career_name, career_vector in career_vectors:
            similarity = matcher.compute_cosine_similarity(profile_vector, career_vector)
            similarities.append(similarity)
        
        assert len(similarities) == len(career_vectors)
        assert all(0.0 <= s <= 1.0 for s in similarities)
    
    def test_rank_career_matches(self, matcher):
        """Test career ranking."""
        similarities = [
            ('Career A', 0.8),
            ('Career B', 0.6),
            ('Career C', 0.9),
            ('Career D', 0.3)
        ]
        
        ranked = matcher.rank_career_matches(similarities)
        
        assert len(ranked) == len(similarities)
        assert ranked[0][1] == 0.9  # Highest similarity first
        assert ranked[-1][1] == 0.3  # Lowest similarity last
        
        # Check that ranking is in descending order
        for i in range(len(ranked) - 1):
            assert ranked[i][1] >= ranked[i + 1][1]
    
    def test_generate_match_explanations(self, matcher):
        """Test match explanation generation."""
        top_matches = [
            ('Software Engineer', 0.85),
            ('Data Scientist', 0.75),
            ('Doctor', 0.45)
        ]
        
        matches = matcher.generate_match_explanations(top_matches)
        
        assert isinstance(matches, list)
        assert len(matches) == len(top_matches)
        
        for match in matches:
            assert isinstance(match, CareerMatch)
            assert isinstance(match.career_name, str)
            assert isinstance(match.match_score, float)
            assert isinstance(match.confidence_level, str)
            assert isinstance(match.match_percentage, float)
            assert isinstance(match.explanation, str)
            assert isinstance(match.skill_gaps, list)
            assert isinstance(match.improvement_suggestions, list)
            assert isinstance(match.indian_context, dict)
            assert isinstance(match.vector_similarity, float)
            
            assert 0.0 <= match.match_score <= 1.0
            assert 0.0 <= match.match_percentage <= 100.0
            assert match.confidence_level in ['Very High', 'High', 'Moderate', 'Low']
    
    def test_match_careers_pipeline(self, matcher, sample_profile):
        """Test complete career matching pipeline."""
        matches = matcher.match_careers(sample_profile, top_n=5)
        
        assert isinstance(matches, list)
        assert len(matches) <= 5
        
        for match in matches:
            assert isinstance(match, CareerMatch)
            assert match.career_name in [c['career'] for c in matcher.career_database]
        
        # Check that matches are sorted by similarity
        for i in range(len(matches) - 1):
            assert matches[i].match_score >= matches[i + 1].match_score
    
    def test_get_career_recommendations(self, matcher, sample_profile):
        """Test comprehensive career recommendations."""
        recommendations = matcher.get_career_recommendations(sample_profile)
        
        assert isinstance(recommendations, dict)
        assert 'primary_recommendations' in recommendations
        assert 'secondary_recommendations' in recommendations
        assert 'emerging_opportunities' in recommendations
        assert 'alternative_paths' in recommendations
        assert 'summary' in recommendations
        
        # Check primary recommendations
        primary = recommendations['primary_recommendations']
        assert isinstance(primary, list)
        for match in primary:
            assert match.match_percentage >= 80
        
        # Check secondary recommendations
        secondary = recommendations['secondary_recommendations']
        assert isinstance(secondary, list)
        for match in secondary:
            assert 60 <= match.match_percentage < 80
        
        # Check emerging opportunities
        emerging = recommendations['emerging_opportunities']
        assert isinstance(emerging, list)
        for match in emerging:
            assert 40 <= match.match_percentage < 60
        
        # Check alternative paths
        alternative = recommendations['alternative_paths']
        assert isinstance(alternative, list)
        for match in alternative:
            assert match.match_percentage < 40
        
        # Check summary
        summary = recommendations['summary']
        assert isinstance(summary, dict)
        assert 'total_careers_analyzed' in summary
        assert 'top_match' in summary
        assert 'average_match_score' in summary
        assert 'confidence_distribution' in summary
        
        assert isinstance(summary['total_careers_analyzed'], int)
        assert summary['total_careers_analyzed'] > 0
        assert isinstance(summary['average_match_score'], float)
        assert 0.0 <= summary['average_match_score'] <= 1.0
    
    def test_grade_to_score_conversion(self, matcher):
        """Test grade to score conversion."""
        assert matcher._grade_to_score('A+') == 5.0
        assert matcher._grade_to_score('A') == 4.5
        assert matcher._grade_to_score('B+') == 3.5
        assert matcher._grade_to_score('B') == 3.0
        assert matcher._grade_to_score('C') == 1.5
        assert matcher._grade_to_score('F') == 0.0
        assert matcher._grade_to_score('Invalid') == 3.0  # Default
    
    def test_skill_level_to_score_conversion(self, matcher):
        """Test skill level to score conversion."""
        assert matcher._skill_level_to_score('Expert') == 5.0
        assert matcher._skill_level_to_score('Advanced') == 4.0
        assert matcher._skill_level_to_score('Intermediate') == 3.0
        assert matcher._skill_level_to_score('Beginner') == 2.0
        assert matcher._skill_level_to_score('Novice') == 1.0
        assert matcher._skill_level_to_score('Invalid') == 2.0  # Default
    
    def test_confidence_level_classification(self, matcher):
        """Test confidence level classification."""
        assert matcher._get_confidence_level(0.9) == "Very High"
        assert matcher._get_confidence_level(0.7) == "High"
        assert matcher._get_confidence_level(0.5) == "Moderate"
        assert matcher._get_confidence_level(0.3) == "Low"
    
    def test_dynamic_weights_calculation(self, matcher, sample_profile):
        """Test dynamic weights calculation."""
        profile_vector = matcher.calculate_profile_vector(sample_profile)
        weights = matcher._calculate_dynamic_weights(profile_vector)
        
        assert isinstance(weights, np.ndarray)
        assert len(weights) == 149  # Total dimensions
        assert all(w > 0 for w in weights)  # All weights should be positive
        
        # Check that technical skills weights are increased
        if np.sum(profile_vector.technical_skills) > 0:
            start_idx = 35
            end_idx = start_idx + matcher.dimensions['technical_skills']
            assert np.all(weights[start_idx:end_idx] >= 1.0)
        
        # Check that RIASEC weights are increased
        if np.sum(profile_vector.riasec_scores) > 0:
            start_idx = 80
            end_idx = start_idx + matcher.dimensions['riasec_scores']
            assert np.all(weights[start_idx:end_idx] >= 1.0)
    
    def test_career_database_structure(self, matcher):
        """Test career database structure."""
        careers = matcher.career_database
        
        assert isinstance(careers, list)
        assert len(careers) > 0
        
        for career in careers:
            assert 'career' in career
            assert 'education_requirements' in career
            assert 'essential_skills' in career
            assert 'personality_fit' in career
            assert 'industry_trends' in career
            assert 'salary_range' in career
            assert 'job_market_demand' in career
            assert 'location_availability' in career
            assert 'growth_prospects' in career
            assert 'indian_context' in career
            
            # Check Indian context
            indian_context = career['indian_context']
            assert 'entrance_exams' in indian_context
            assert 'top_colleges' in indian_context
            assert 'companies' in indian_context
            assert 'startup_ecosystem' in indian_context
    
    def test_get_career_database(self, matcher):
        """Test getting career database."""
        careers = matcher.get_career_database()
        
        assert isinstance(careers, list)
        assert len(careers) > 0
        assert careers == matcher.career_database
    
    def test_get_feature_mappings(self, matcher):
        """Test getting feature mappings."""
        mappings = matcher.get_feature_mappings()
        
        assert isinstance(mappings, dict)
        assert 'academic_subjects' in mappings
        assert 'technical_skills' in mappings
        assert 'soft_skills' in mappings
        assert 'interests' in mappings
        assert 'career_preferences' in mappings
        assert 'locations' in mappings
        assert 'salary_ranges' in mappings
        assert 'work_environment' in mappings
        
        # Check that mappings are correct
        assert mappings['academic_subjects'] == matcher.academic_subjects_map
        assert mappings['technical_skills'] == matcher.technical_skills_map
        assert mappings['soft_skills'] == matcher.soft_skills_map
    
    def test_empty_profile_handling(self, matcher):
        """Test handling of empty profile."""
        empty_profile = {}
        
        profile_vector = matcher.calculate_profile_vector(empty_profile)
        assert isinstance(profile_vector, ProfileVector)
        
        # All vectors should be zeros
        assert np.all(profile_vector.academic_subjects == 0)
        assert np.all(profile_vector.technical_skills == 0)
        assert np.all(profile_vector.soft_skills == 0)
        assert np.all(profile_vector.riasec_scores == 0)
        assert np.all(profile_vector.interests == 0)
    
    def test_partial_profile_handling(self, matcher):
        """Test handling of partial profile."""
        partial_profile = {
            'academic_subjects': {'Mathematics': 'A'},
            'interests': ['Technology']
        }
        
        profile_vector = matcher.calculate_profile_vector(partial_profile)
        assert isinstance(profile_vector, ProfileVector)
        
        # Check that only specified fields are set
        assert profile_vector.academic_subjects[matcher.academic_subjects_map['Mathematics']] > 0
        assert profile_vector.interests[matcher.interests_map['Technology']] > 0
        
        # Other fields should be zeros
        assert np.all(profile_vector.technical_skills == 0)
        assert np.all(profile_vector.soft_skills == 0)
        assert np.all(profile_vector.riasec_scores == 0)

class TestProfileVector:
    """Test cases for ProfileVector dataclass."""
    
    def test_profile_vector_creation(self):
        """Test ProfileVector creation."""
        vector = ProfileVector(
            academic_subjects=np.zeros(20),
            extracurricular_activities=np.zeros(15),
            technical_skills=np.zeros(25),
            soft_skills=np.zeros(20),
            riasec_scores=np.zeros(6),
            interests=np.zeros(30),
            career_preferences=np.zeros(10),
            location_preferences=np.zeros(10),
            salary_expectations=np.zeros(5),
            work_environment=np.zeros(8)
        )
        
        assert isinstance(vector.academic_subjects, np.ndarray)
        assert len(vector.academic_subjects) == 20
        assert len(vector.to_array()) == 149  # Total dimensions
    
    def test_profile_vector_to_array(self):
        """Test ProfileVector to_array method."""
        vector = ProfileVector(
            academic_subjects=np.ones(20),
            extracurricular_activities=np.ones(15),
            technical_skills=np.ones(25),
            soft_skills=np.ones(20),
            riasec_scores=np.ones(6),
            interests=np.ones(30),
            career_preferences=np.ones(10),
            location_preferences=np.ones(10),
            salary_expectations=np.ones(5),
            work_environment=np.ones(8)
        )
        
        array = vector.to_array()
        assert isinstance(array, np.ndarray)
        assert len(array) == 149
        assert np.all(array == 1.0)

class TestCareerVector:
    """Test cases for CareerVector dataclass."""
    
    def test_career_vector_creation(self):
        """Test CareerVector creation."""
        vector = CareerVector(
            education_requirements=np.zeros(20),
            essential_skills=np.zeros(25),
            personality_fit=np.zeros(6),
            industry_trends=np.zeros(10),
            salary_ranges=np.zeros(5),
            job_market_demand=np.zeros(8),
            location_availability=np.zeros(10),
            growth_prospects=np.zeros(5)
        )
        
        assert isinstance(vector.education_requirements, np.ndarray)
        assert len(vector.education_requirements) == 20
        assert len(vector.to_array()) == 89  # Total dimensions
    
    def test_career_vector_to_array(self):
        """Test CareerVector to_array method."""
        vector = CareerVector(
            education_requirements=np.ones(20),
            essential_skills=np.ones(25),
            personality_fit=np.ones(6),
            industry_trends=np.ones(10),
            salary_ranges=np.ones(5),
            job_market_demand=np.ones(8),
            location_availability=np.ones(10),
            growth_prospects=np.ones(5)
        )
        
        array = vector.to_array()
        assert isinstance(array, np.ndarray)
        assert len(array) == 89
        assert np.all(array == 1.0)

class TestCareerMatch:
    """Test cases for CareerMatch dataclass."""
    
    def test_career_match_creation(self):
        """Test CareerMatch creation."""
        match = CareerMatch(
            career_name="Software Engineer",
            match_score=0.85,
            confidence_level="Very High",
            match_percentage=85.0,
            explanation="Excellent match",
            skill_gaps=["Learn Python"],
            improvement_suggestions=["Take coding courses"],
            indian_context={'salary_range': '₹6-25 LPA'},
            vector_similarity=0.85
        )
        
        assert match.career_name == "Software Engineer"
        assert match.match_score == 0.85
        assert match.confidence_level == "Very High"
        assert match.match_percentage == 85.0
        assert match.explanation == "Excellent match"
        assert match.skill_gaps == ["Learn Python"]
        assert match.improvement_suggestions == ["Take coding courses"]
        assert match.indian_context == {'salary_range': '₹6-25 LPA'}
        assert match.vector_similarity == 0.85

if __name__ == "__main__":
    pytest.main([__file__])
