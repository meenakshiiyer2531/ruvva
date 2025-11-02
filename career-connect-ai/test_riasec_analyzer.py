"""
Test suite for RIASEC Analyzer
"""

import pytest
import json
from core.riasec_analyzer import RIASECAnalyzer, RIASECScore, PersonalityProfile, CareerMatch

class TestRIASECAnalyzer:
    """Test cases for RIASECAnalyzer class."""
    
    @pytest.fixture
    def analyzer(self):
        """Create RIASEC analyzer instance for testing."""
        return RIASECAnalyzer()
    
    @pytest.fixture
    def sample_responses(self):
        """Sample assessment responses for testing."""
        return {
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
    
    def test_analyzer_initialization(self, analyzer):
        """Test analyzer initialization."""
        assert analyzer is not None
        assert len(analyzer.assessment_questions) == 36  # 6 questions per dimension
        assert len(analyzer.career_database) > 0
        assert len(analyzer.dimensions) == 6
    
    def test_assessment_questions_structure(self, analyzer):
        """Test assessment questions structure."""
        questions = analyzer.assessment_questions
        
        # Check that all questions have required fields
        for question in questions:
            assert 'id' in question
            assert 'question' in question
            assert 'dimension' in question
            assert 'type' in question
            assert 'indian_context' in question
            
            # Check dimension is valid
            assert question['dimension'] in ['Realistic', 'Investigative', 'Artistic', 'Social', 'Enterprising', 'Conventional']
            
            # Check type is valid
            assert question['type'] in ['agreement', 'preference']
    
    def test_career_database_structure(self, analyzer):
        """Test career database structure."""
        careers = analyzer.career_database
        
        for career in careers:
            assert 'career' in career
            assert 'riasec_codes' in career
            assert 'description' in career
            assert 'indian_context' in career
            
            # Check RIASEC codes are valid
            valid_codes = ['R', 'I', 'A', 'S', 'E', 'C']
            for code in career['riasec_codes']:
                assert code in valid_codes
            
            # Check Indian context has required fields
            indian_context = career['indian_context']
            assert 'entrance_exams' in indian_context
            assert 'top_colleges' in indian_context
            assert 'salary_range' in indian_context
            assert 'growth_prospects' in indian_context
            assert 'job_market' in indian_context
    
    def test_calculate_personality_scores(self, analyzer, sample_responses):
        """Test personality score calculation."""
        scores = analyzer.calculate_personality_scores(sample_responses)
        
        assert isinstance(scores, RIASECScore)
        assert 0 <= scores.realistic <= 5
        assert 0 <= scores.investigative <= 5
        assert 0 <= scores.artistic <= 5
        assert 0 <= scores.social <= 5
        assert 0 <= scores.enterprising <= 5
        assert 0 <= scores.conventional <= 5
        
        # Check that scores are reasonable based on sample responses
        assert scores.investigative > scores.artistic  # Sample has high I, low A
        assert scores.conventional > scores.artistic  # Sample has high C, low A
    
    def test_riasec_score_methods(self, analyzer, sample_responses):
        """Test RIASEC score methods."""
        scores = analyzer.calculate_personality_scores(sample_responses)
        
        # Test to_dict method
        scores_dict = scores.to_dict()
        assert isinstance(scores_dict, dict)
        assert len(scores_dict) == 6
        assert all(key in scores_dict for key in ['Realistic', 'Investigative', 'Artistic', 'Social', 'Enterprising', 'Conventional'])
        
        # Test get_primary_type method
        primary_type = scores.get_primary_type()
        assert primary_type in ['Realistic', 'Investigative', 'Artistic', 'Social', 'Enterprising', 'Conventional']
        
        # Test get_secondary_type method
        secondary_type = scores.get_secondary_type()
        assert secondary_type in ['Realistic', 'Investigative', 'Artistic', 'Social', 'Enterprising', 'Conventional']
        assert secondary_type != primary_type
    
    def test_generate_personality_profile(self, analyzer, sample_responses):
        """Test personality profile generation."""
        scores = analyzer.calculate_personality_scores(sample_responses)
        profile = analyzer.generate_personality_profile(scores)
        
        assert isinstance(profile, PersonalityProfile)
        assert profile.riasec_scores == scores
        assert profile.primary_type in ['Realistic', 'Investigative', 'Artistic', 'Social', 'Enterprising', 'Conventional']
        assert profile.secondary_type in ['Realistic', 'Investigative', 'Artistic', 'Social', 'Enterprising', 'Conventional']
        assert isinstance(profile.strengths, list)
        assert isinstance(profile.work_environment_preferences, list)
        assert isinstance(profile.communication_style, str)
        assert isinstance(profile.learning_preferences, list)
        assert isinstance(profile.career_clusters, list)
        assert isinstance(profile.personality_description, str)
        assert isinstance(profile.indian_context_insights, dict)
    
    def test_map_careers_to_personality(self, analyzer, sample_responses):
        """Test career mapping functionality."""
        scores = analyzer.calculate_personality_scores(sample_responses)
        career_matches = analyzer.map_careers_to_personality(scores)
        
        assert isinstance(career_matches, list)
        assert len(career_matches) <= 2  # Should return top 2 matches
        
        for match in career_matches:
            assert isinstance(match, CareerMatch)
            assert isinstance(match.career_name, str)
            assert isinstance(match.riasec_codes, list)
            assert isinstance(match.compatibility_score, float)
            assert isinstance(match.match_percentage, float)
            assert isinstance(match.explanation, str)
            assert isinstance(match.indian_relevance, dict)
            
            assert 0 <= match.compatibility_score <= 1
            assert 0 <= match.match_percentage <= 100
        
        # Check that matches are sorted by compatibility score
        for i in range(len(career_matches) - 1):
            assert career_matches[i].compatibility_score >= career_matches[i + 1].compatibility_score
    
    def test_generate_visualization_data(self, analyzer, sample_responses):
        """Test visualization data generation."""
        scores = analyzer.calculate_personality_scores(sample_responses)
        career_matches = analyzer.map_careers_to_personality(scores)
        viz_data = analyzer.generate_visualization_data(scores, career_matches)
        
        assert isinstance(viz_data, dict)
        assert 'radar_chart' in viz_data
        assert 'career_matches' in viz_data
        assert 'trait_explanations' in viz_data
        assert 'summary_stats' in viz_data
        
        # Check radar chart data
        radar_data = viz_data['radar_chart']
        assert 'labels' in radar_data
        assert 'datasets' in radar_data
        assert len(radar_data['labels']) == 6
        assert len(radar_data['datasets'][0]['data']) == 6
        
        # Check career match data
        career_data = viz_data['career_matches']
        assert 'careers' in career_data
        assert 'percentages' in career_data
        assert 'colors' in career_data
        assert len(career_data['careers']) == len(career_data['percentages'])
        
        # Check trait explanations
        trait_explanations = viz_data['trait_explanations']
        assert len(trait_explanations) == 6
        for dimension, explanation in trait_explanations.items():
            assert 'score' in explanation
            assert 'level' in explanation
            assert 'description' in explanation
            assert 'characteristics' in explanation
            assert 'indian_context' in explanation
    
    def test_individual_dimension_scoring(self, analyzer, sample_responses):
        """Test individual dimension scoring methods."""
        # Test each dimension scoring method
        realistic_score = analyzer.score_realistic_dimension(sample_responses)
        investigative_score = analyzer.score_investigative_dimension(sample_responses)
        artistic_score = analyzer.score_artistic_dimension(sample_responses)
        social_score = analyzer.score_social_dimension(sample_responses)
        enterprising_score = analyzer.score_enterprising_dimension(sample_responses)
        conventional_score = analyzer.score_conventional_dimension(sample_responses)
        
        # Check that scores are within valid range
        for score in [realistic_score, investigative_score, artistic_score, social_score, enterprising_score, conventional_score]:
            assert 0 <= score <= 5
        
        # Check that scores match expected values based on sample responses
        assert investigative_score > artistic_score  # Sample has high I, low A
        assert conventional_score > artistic_score  # Sample has high C, low A
    
    def test_analyze_responses_complete(self, analyzer, sample_responses):
        """Test complete analysis workflow."""
        analysis = analyzer.analyze_responses(sample_responses)
        
        assert isinstance(analysis, dict)
        assert 'riasec_scores' in analysis
        assert 'personality_profile' in analysis
        assert 'career_matches' in analysis
        assert 'visualization_data' in analysis
        assert 'analysis_timestamp' in analysis
        assert 'assessment_summary' in analysis
        
        # Check that all components are properly structured
        assert isinstance(analysis['riasec_scores'], dict)
        assert isinstance(analysis['personality_profile'], PersonalityProfile)
        assert isinstance(analysis['career_matches'], list)
        assert isinstance(analysis['visualization_data'], dict)
        assert isinstance(analysis['assessment_summary'], dict)
    
    def test_question_score_calculation(self, analyzer):
        """Test question score calculation."""
        # Test agreement type questions
        assert analyzer._calculate_question_score(1, 'agreement') == 1.0
        assert analyzer._calculate_question_score(5, 'agreement') == 5.0
        assert analyzer._calculate_question_score('strongly agree', 'agreement') == 5.0
        assert analyzer._calculate_question_score('disagree', 'agreement') == 2.0
        
        # Test preference type questions
        assert analyzer._calculate_question_score(1, 'preference') == 1.0
        assert analyzer._calculate_question_score(5, 'preference') == 5.0
        
        # Test invalid input
        assert analyzer._calculate_question_score('invalid', 'agreement') == 3.0
        assert analyzer._calculate_question_score(None, 'agreement') == 3.0
    
    def test_career_compatibility_calculation(self, analyzer):
        """Test career compatibility calculation."""
        scores_dict = {
            'Realistic': 4.0,
            'Investigative': 5.0,
            'Artistic': 2.0,
            'Social': 3.0,
            'Enterprising': 3.5,
            'Conventional': 4.5
        }
        
        # Test with different career codes
        compatibility1 = analyzer._calculate_career_compatibility(scores_dict, ['I', 'R', 'C'])
        compatibility2 = analyzer._calculate_career_compatibility(scores_dict, ['A', 'S'])
        
        assert 0 <= compatibility1 <= 1
        assert 0 <= compatibility2 <= 1
        assert compatibility1 > compatibility2  # I+R+C should score higher than A+S
    
    def test_dimension_name_conversion(self, analyzer):
        """Test RIASEC code to dimension name conversion."""
        assert analyzer._get_dimension_name_from_code('R') == 'Realistic'
        assert analyzer._get_dimension_name_from_code('I') == 'Investigative'
        assert analyzer._get_dimension_name_from_code('A') == 'Artistic'
        assert analyzer._get_dimension_name_from_code('S') == 'Social'
        assert analyzer._get_dimension_name_from_code('E') == 'Enterprising'
        assert analyzer._get_dimension_name_from_code('C') == 'Conventional'
        assert analyzer._get_dimension_name_from_code('X') == 'Unknown'
    
    def test_score_level_classification(self, analyzer):
        """Test score level classification."""
        assert analyzer._get_score_level(4.8) == "Very High"
        assert analyzer._get_score_level(4.2) == "High"
        assert analyzer._get_score_level(3.7) == "Above Average"
        assert analyzer._get_score_level(3.2) == "Average"
        assert analyzer._get_score_level(2.7) == "Below Average"
        assert analyzer._get_score_level(2.0) == "Low"
    
    def test_get_assessment_questions(self, analyzer):
        """Test getting assessment questions."""
        questions = analyzer.get_assessment_questions()
        assert isinstance(questions, list)
        assert len(questions) == 36
        assert all('id' in q for q in questions)
    
    def test_get_career_database(self, analyzer):
        """Test getting career database."""
        careers = analyzer.get_career_database()
        assert isinstance(careers, list)
        assert len(careers) > 0
        assert all('career' in c for c in careers)

class TestRIASECScore:
    """Test cases for RIASECScore dataclass."""
    
    def test_riasec_score_creation(self):
        """Test RIASECScore creation."""
        score = RIASECScore(
            realistic=4.0,
            investigative=5.0,
            artistic=2.0,
            social=3.0,
            enterprising=3.5,
            conventional=4.5
        )
        
        assert score.realistic == 4.0
        assert score.investigative == 5.0
        assert score.artistic == 2.0
        assert score.social == 3.0
        assert score.enterprising == 3.5
        assert score.conventional == 4.5
    
    def test_riasec_score_to_dict(self):
        """Test RIASECScore to_dict method."""
        score = RIASECScore(
            realistic=4.0,
            investigative=5.0,
            artistic=2.0,
            social=3.0,
            enterprising=3.5,
            conventional=4.5
        )
        
        score_dict = score.to_dict()
        assert isinstance(score_dict, dict)
        assert score_dict['Realistic'] == 4.0
        assert score_dict['Investigative'] == 5.0
        assert score_dict['Artistic'] == 2.0
        assert score_dict['Social'] == 3.0
        assert score_dict['Enterprising'] == 3.5
        assert score_dict['Conventional'] == 4.5
    
    def test_riasec_score_primary_type(self):
        """Test RIASECScore get_primary_type method."""
        score = RIASECScore(
            realistic=4.0,
            investigative=5.0,
            artistic=2.0,
            social=3.0,
            enterprising=3.5,
            conventional=4.5
        )
        
        primary_type = score.get_primary_type()
        assert primary_type == 'Investigative'  # Highest score
    
    def test_riasec_score_secondary_type(self):
        """Test RIASECScore get_secondary_type method."""
        score = RIASECScore(
            realistic=4.0,
            investigative=5.0,
            artistic=2.0,
            social=3.0,
            enterprising=3.5,
            conventional=4.5
        )
        
        secondary_type = score.get_secondary_type()
        assert secondary_type == 'Conventional'  # Second highest score

class TestCareerMatch:
    """Test cases for CareerMatch dataclass."""
    
    def test_career_match_creation(self):
        """Test CareerMatch creation."""
        match = CareerMatch(
            career_name="Software Engineer",
            riasec_codes=['I', 'R', 'C'],
            compatibility_score=0.85,
            match_percentage=85.0,
            explanation="Strong investigative and realistic traits",
            indian_relevance={'entrance_exams': ['JEE'], 'salary_range': '₹6-25 LPA'}
        )
        
        assert match.career_name == "Software Engineer"
        assert match.riasec_codes == ['I', 'R', 'C']
        assert match.compatibility_score == 0.85
        assert match.match_percentage == 85.0
        assert match.explanation == "Strong investigative and realistic traits"
        assert match.indian_relevance['entrance_exams'] == ['JEE']

if __name__ == "__main__":
    pytest.main([__file__])


        trait_explanations = viz_data['trait_explanations']

        assert len(trait_explanations) == 6

        for dimension, explanation in trait_explanations.items():

            assert 'score' in explanation

            assert 'level' in explanation

            assert 'description' in explanation

            assert 'characteristics' in explanation

            assert 'indian_context' in explanation

    

    def test_individual_dimension_scoring(self, analyzer, sample_responses):

        """Test individual dimension scoring methods."""

        # Test each dimension scoring method

        realistic_score = analyzer.score_realistic_dimension(sample_responses)

        investigative_score = analyzer.score_investigative_dimension(sample_responses)

        artistic_score = analyzer.score_artistic_dimension(sample_responses)

        social_score = analyzer.score_social_dimension(sample_responses)

        enterprising_score = analyzer.score_enterprising_dimension(sample_responses)

        conventional_score = analyzer.score_conventional_dimension(sample_responses)

        

        # Check that scores are within valid range

        for score in [realistic_score, investigative_score, artistic_score, social_score, enterprising_score, conventional_score]:

            assert 0 <= score <= 5

        

        # Check that scores match expected values based on sample responses

        assert investigative_score > artistic_score  # Sample has high I, low A

        assert conventional_score > artistic_score  # Sample has high C, low A

    

    def test_analyze_responses_complete(self, analyzer, sample_responses):

        """Test complete analysis workflow."""

        analysis = analyzer.analyze_responses(sample_responses)

        

        assert isinstance(analysis, dict)

        assert 'riasec_scores' in analysis

        assert 'personality_profile' in analysis

        assert 'career_matches' in analysis

        assert 'visualization_data' in analysis

        assert 'analysis_timestamp' in analysis

        assert 'assessment_summary' in analysis

        

        # Check that all components are properly structured

        assert isinstance(analysis['riasec_scores'], dict)

        assert isinstance(analysis['personality_profile'], PersonalityProfile)

        assert isinstance(analysis['career_matches'], list)

        assert isinstance(analysis['visualization_data'], dict)

        assert isinstance(analysis['assessment_summary'], dict)

    

    def test_question_score_calculation(self, analyzer):

        """Test question score calculation."""

        # Test agreement type questions

        assert analyzer._calculate_question_score(1, 'agreement') == 1.0

        assert analyzer._calculate_question_score(5, 'agreement') == 5.0

        assert analyzer._calculate_question_score('strongly agree', 'agreement') == 5.0

        assert analyzer._calculate_question_score('disagree', 'agreement') == 2.0

        

        # Test preference type questions

        assert analyzer._calculate_question_score(1, 'preference') == 1.0

        assert analyzer._calculate_question_score(5, 'preference') == 5.0

        

        # Test invalid input

        assert analyzer._calculate_question_score('invalid', 'agreement') == 3.0

        assert analyzer._calculate_question_score(None, 'agreement') == 3.0

    

    def test_career_compatibility_calculation(self, analyzer):

        """Test career compatibility calculation."""

        scores_dict = {

            'Realistic': 4.0,

            'Investigative': 5.0,

            'Artistic': 2.0,

            'Social': 3.0,

            'Enterprising': 3.5,

            'Conventional': 4.5

        }

        

        # Test with different career codes

        compatibility1 = analyzer._calculate_career_compatibility(scores_dict, ['I', 'R', 'C'])

        compatibility2 = analyzer._calculate_career_compatibility(scores_dict, ['A', 'S'])

        

        assert 0 <= compatibility1 <= 1

        assert 0 <= compatibility2 <= 1

        assert compatibility1 > compatibility2  # I+R+C should score higher than A+S

    

    def test_dimension_name_conversion(self, analyzer):

        """Test RIASEC code to dimension name conversion."""

        assert analyzer._get_dimension_name_from_code('R') == 'Realistic'

        assert analyzer._get_dimension_name_from_code('I') == 'Investigative'

        assert analyzer._get_dimension_name_from_code('A') == 'Artistic'

        assert analyzer._get_dimension_name_from_code('S') == 'Social'

        assert analyzer._get_dimension_name_from_code('E') == 'Enterprising'

        assert analyzer._get_dimension_name_from_code('C') == 'Conventional'

        assert analyzer._get_dimension_name_from_code('X') == 'Unknown'

    

    def test_score_level_classification(self, analyzer):

        """Test score level classification."""

        assert analyzer._get_score_level(4.8) == "Very High"

        assert analyzer._get_score_level(4.2) == "High"

        assert analyzer._get_score_level(3.7) == "Above Average"

        assert analyzer._get_score_level(3.2) == "Average"

        assert analyzer._get_score_level(2.7) == "Below Average"

        assert analyzer._get_score_level(2.0) == "Low"

    

    def test_get_assessment_questions(self, analyzer):

        """Test getting assessment questions."""

        questions = analyzer.get_assessment_questions()

        assert isinstance(questions, list)

        assert len(questions) == 36

        assert all('id' in q for q in questions)

    

    def test_get_career_database(self, analyzer):

        """Test getting career database."""

        careers = analyzer.get_career_database()

        assert isinstance(careers, list)

        assert len(careers) > 0

        assert all('career' in c for c in careers)



class TestRIASECScore:

    """Test cases for RIASECScore dataclass."""

    

    def test_riasec_score_creation(self):

        """Test RIASECScore creation."""

        score = RIASECScore(

            realistic=4.0,

            investigative=5.0,

            artistic=2.0,

            social=3.0,

            enterprising=3.5,

            conventional=4.5

        )

        

        assert score.realistic == 4.0

        assert score.investigative == 5.0

        assert score.artistic == 2.0

        assert score.social == 3.0

        assert score.enterprising == 3.5

        assert score.conventional == 4.5

    

    def test_riasec_score_to_dict(self):

        """Test RIASECScore to_dict method."""

        score = RIASECScore(

            realistic=4.0,

            investigative=5.0,

            artistic=2.0,

            social=3.0,

            enterprising=3.5,

            conventional=4.5

        )

        

        score_dict = score.to_dict()

        assert isinstance(score_dict, dict)

        assert score_dict['Realistic'] == 4.0

        assert score_dict['Investigative'] == 5.0

        assert score_dict['Artistic'] == 2.0

        assert score_dict['Social'] == 3.0

        assert score_dict['Enterprising'] == 3.5

        assert score_dict['Conventional'] == 4.5

    

    def test_riasec_score_primary_type(self):

        """Test RIASECScore get_primary_type method."""

        score = RIASECScore(

            realistic=4.0,

            investigative=5.0,

            artistic=2.0,

            social=3.0,

            enterprising=3.5,

            conventional=4.5

        )

        

        primary_type = score.get_primary_type()

        assert primary_type == 'Investigative'  # Highest score

    

    def test_riasec_score_secondary_type(self):

        """Test RIASECScore get_secondary_type method."""

        score = RIASECScore(

            realistic=4.0,

            investigative=5.0,

            artistic=2.0,

            social=3.0,

            enterprising=3.5,

            conventional=4.5

        )

        

        secondary_type = score.get_secondary_type()

        assert secondary_type == 'Conventional'  # Second highest score



class TestCareerMatch:

    """Test cases for CareerMatch dataclass."""

    

    def test_career_match_creation(self):

        """Test CareerMatch creation."""

        match = CareerMatch(

            career_name="Software Engineer",

            riasec_codes=['I', 'R', 'C'],

            compatibility_score=0.85,

            match_percentage=85.0,

            explanation="Strong investigative and realistic traits",

            indian_relevance={'entrance_exams': ['JEE'], 'salary_range': '₹6-25 LPA'}

        )

        

        assert match.career_name == "Software Engineer"

        assert match.riasec_codes == ['I', 'R', 'C']

        assert match.compatibility_score == 0.85

        assert match.match_percentage == 85.0

        assert match.explanation == "Strong investigative and realistic traits"

        assert match.indian_relevance['entrance_exams'] == ['JEE']



if __name__ == "__main__":

    pytest.main([__file__])


