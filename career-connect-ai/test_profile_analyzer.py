"""
Test suite for Student Profile Analyzer
"""

import pytest
from datetime import datetime
from services.profile_analyzer import (
    StudentProfileAnalyzer, 
    AcademicAnalysis, 
    ExtracurricularAnalysis, 
    SkillsAssessment, 
    InterestAnalysis, 
    ProfileInsights, 
    ProfileCompleteness, 
    CompleteProfileAnalysis
)

class TestStudentProfileAnalyzer:
    """Test cases for StudentProfileAnalyzer class."""
    
    @pytest.fixture
    def analyzer(self):
        """Create profile analyzer instance for testing."""
        return StudentProfileAnalyzer()
    
    @pytest.fixture
    def sample_profile_data(self):
        """Sample profile data for testing."""
        return {
            'academic_info': {
                'class_10_marks': {
                    'Mathematics': 92,
                    'Physics': 88,
                    'Chemistry': 85,
                    'Biology': 90,
                    'English': 82,
                    'Hindi': 78
                },
                'class_12_marks': {
                    'Mathematics': 95,
                    'Physics': 90,
                    'Chemistry': 87,
                    'Biology': 92,
                    'English': 85,
                    'Hindi': 80
                },
                'stream': 'Science',
                'competitive_exams': ['JEE Main', 'NEET']
            },
            'extracurricular_activities': [
                {'name': 'Science Club', 'role': 'President', 'duration': '2 years'},
                {'name': 'Robotics', 'role': 'Member', 'duration': '1 year'},
                {'name': 'Volunteering', 'role': 'Coordinator', 'duration': '3 years'},
                {'name': 'Debate', 'role': 'Captain', 'duration': '2 years'}
            ],
            'skill_assessments': {
                'technical_skills': {
                    'Programming': 4,
                    'Data Analysis': 3,
                    'Web Development': 2,
                    'Machine Learning': 1
                },
                'soft_skills': {
                    'Communication': 4,
                    'Leadership': 4,
                    'Problem Solving': 3,
                    'Teamwork': 4,
                    'Critical Thinking': 3
                }
            },
            'interests': [
                'Technology', 'Science', 'Mathematics', 'Engineering', 
                'Medicine', 'Business', 'Design', 'Art'
            ],
            'riasec_scores': {
                'Realistic': 3.5,
                'Investigative': 4.8,
                'Artistic': 2.1,
                'Social': 3.2,
                'Enterprising': 3.8,
                'Conventional': 4.2
            },
            'career_goals': [
                'Become a software engineer',
                'Work in healthcare technology',
                'Start my own tech company'
            ]
        }
    
    def test_analyzer_initialization(self, analyzer):
        """Test analyzer initialization."""
        assert analyzer is not None
        assert len(analyzer.academic_subjects) > 0
        assert len(analyzer.extracurricular_categories) > 0
        assert len(analyzer.skill_categories) > 0
        assert len(analyzer.interest_categories) > 0
        assert len(analyzer.analysis_weights) > 0
    
    def test_analyze_complete_profile(self, analyzer, sample_profile_data):
        """Test complete profile analysis."""
        analysis = analyzer.analyze_complete_profile(sample_profile_data)
        
        assert isinstance(analysis, CompleteProfileAnalysis)
        assert isinstance(analysis.academic_analysis, AcademicAnalysis)
        assert isinstance(analysis.extracurricular_analysis, ExtracurricularAnalysis)
        assert isinstance(analysis.skills_assessment, SkillsAssessment)
        assert isinstance(analysis.interest_analysis, InterestAnalysis)
        assert isinstance(analysis.profile_insights, ProfileInsights)
        assert isinstance(analysis.completeness_assessment, ProfileCompleteness)
        assert isinstance(analysis.ai_generated_summary, str)
        assert isinstance(analysis.analysis_timestamp, datetime)
    
    def test_extract_academic_strengths(self, analyzer, sample_profile_data):
        """Test academic strengths extraction."""
        academic_info = sample_profile_data['academic_info']
        analysis = analyzer.extract_academic_strengths(academic_info)
        
        assert isinstance(analysis, AcademicAnalysis)
        assert isinstance(analysis.strong_subjects, list)
        assert isinstance(analysis.weak_subjects, list)
        assert isinstance(analysis.performance_trends, dict)
        assert isinstance(analysis.stream_recommendation, str)
        assert isinstance(analysis.competitive_exam_suitability, list)
        assert isinstance(analysis.academic_trajectory, str)
        assert isinstance(analysis.subject_correlations, dict)
        assert isinstance(analysis.overall_performance, str)
        
        # Check that strong subjects are identified
        assert len(analysis.strong_subjects) > 0
        assert 'Mathematics' in analysis.strong_subjects
        assert 'Physics' in analysis.strong_subjects
        
        # Check stream recommendation
        assert analysis.stream_recommendation in ['Science', 'Commerce', 'Arts', 'Mixed']
        
        # Check competitive exam suitability
        assert len(analysis.competitive_exam_suitability) > 0
    
    def test_analyze_extracurricular_patterns(self, analyzer, sample_profile_data):
        """Test extracurricular patterns analysis."""
        activities = sample_profile_data['extracurricular_activities']
        analysis = analyzer.analyze_extracurricular_patterns(activities)
        
        assert isinstance(analysis, ExtracurricularAnalysis)
        assert isinstance(analysis.leadership_experience, list)
        assert isinstance(analysis.activity_preferences, dict)
        assert isinstance(analysis.creative_vs_technical, str)
        assert isinstance(analysis.social_impact_score, float)
        assert isinstance(analysis.sports_participation, list)
        assert isinstance(analysis.team_vs_individual, str)
        assert isinstance(analysis.activity_diversity_score, float)
        
        # Check that leadership experience is identified
        assert len(analysis.leadership_experience) > 0
        
        # Check activity preferences
        assert 0.0 <= analysis.social_impact_score <= 1.0
        assert 0.0 <= analysis.activity_diversity_score <= 1.0
    
    def test_assess_skill_levels(self, analyzer, sample_profile_data):
        """Test skill levels assessment."""
        skill_assessments = sample_profile_data['skill_assessments']
        analysis = analyzer.assess_skill_levels(skill_assessments)
        
        assert isinstance(analysis, SkillsAssessment)
        assert isinstance(analysis.technical_skills, dict)
        assert isinstance(analysis.soft_skills, dict)
        assert isinstance(analysis.learning_agility, float)
        assert isinstance(analysis.problem_solving_approach, str)
        assert isinstance(analysis.digital_literacy, float)
        assert isinstance(analysis.skill_gaps, list)
        assert isinstance(analysis.skill_strengths, list)
        
        # Check learning agility
        assert 0.0 <= analysis.learning_agility <= 1.0
        
        # Check digital literacy
        assert 0.0 <= analysis.digital_literacy <= 1.0
        
        # Check skill gaps and strengths
        assert len(analysis.skill_gaps) >= 0
        assert len(analysis.skill_strengths) >= 0
    
    def test_identify_interest_clusters(self, analyzer, sample_profile_data):
        """Test interest cluster identification."""
        interests = sample_profile_data['interests']
        analysis = analyzer.identify_interest_clusters(interests)
        
        assert isinstance(analysis, InterestAnalysis)
        assert isinstance(analysis.primary_interests, list)
        assert isinstance(analysis.interest_intensity, dict)
        assert isinstance(analysis.cross_domain_connections, dict)
        assert isinstance(analysis.emerging_interests, list)
        assert isinstance(analysis.career_pathway_mapping, dict)
        assert isinstance(analysis.interest_clusters, dict)
        
        # Check that primary interests are identified
        assert len(analysis.primary_interests) > 0
        
        # Check interest intensity
        for interest, intensity in analysis.interest_intensity.items():
            assert 0.0 <= intensity <= 1.0
        
        # Check career pathway mapping
        assert len(analysis.career_pathway_mapping) > 0
    
    def test_generate_profile_insights(self, analyzer, sample_profile_data):
        """Test profile insights generation."""
        # First get analysis results
        academic_analysis = analyzer.extract_academic_strengths(sample_profile_data['academic_info'])
        extracurricular_analysis = analyzer.analyze_extracurricular_patterns(sample_profile_data['extracurricular_activities'])
        skills_assessment = analyzer.assess_skill_levels(sample_profile_data['skill_assessments'])
        interest_analysis = analyzer.identify_interest_clusters(sample_profile_data['interests'])
        
        analysis_results = {
            'academic': academic_analysis,
            'extracurricular': extracurricular_analysis,
            'skills': skills_assessment,
            'interests': interest_analysis
        }
        
        insights = analyzer.generate_profile_insights(analysis_results)
        
        assert isinstance(insights, ProfileInsights)
        assert isinstance(insights.natural_talents, list)
        assert isinstance(insights.career_clusters, list)
        assert isinstance(insights.skill_development_recommendations, list)
        assert isinstance(insights.academic_pathway_suggestions, list)
        assert isinstance(insights.work_environment_preferences, list)
        assert isinstance(insights.personality_insights, str)
        assert isinstance(insights.motivational_message, str)
        assert isinstance(insights.next_steps, list)
        
        # Check that insights are generated
        assert len(insights.natural_talents) > 0
        assert len(insights.career_clusters) > 0
        assert len(insights.next_steps) > 0
    
    def test_identify_strong_subjects(self, analyzer):
        """Test strong subjects identification."""
        class_10_marks = {'Mathematics': 92, 'Physics': 88, 'Chemistry': 85}
        class_12_marks = {'Mathematics': 95, 'Physics': 90, 'Chemistry': 87}
        
        strong_subjects = analyzer._identify_strong_subjects(class_10_marks, class_12_marks)
        
        assert isinstance(strong_subjects, list)
        assert 'Mathematics' in strong_subjects
        assert 'Physics' in strong_subjects
        assert 'Chemistry' in strong_subjects
    
    def test_identify_weak_subjects(self, analyzer):
        """Test weak subjects identification."""
        class_10_marks = {'Mathematics': 65, 'Physics': 70, 'Chemistry': 68}
        class_12_marks = {'Mathematics': 60, 'Physics': 70, 'Chemistry': 62}
        
        weak_subjects = analyzer._identify_weak_subjects(class_10_marks, class_12_marks)
        
        assert isinstance(weak_subjects, list)
        assert 'Mathematics' in weak_subjects
        assert 'Chemistry' in weak_subjects
    
    def test_analyze_performance_trends(self, analyzer):
        """Test performance trends analysis."""
        class_10_marks = {'Mathematics': 80, 'Physics': 85, 'Chemistry': 75}
        class_12_marks = {'Mathematics': 90, 'Physics': 80, 'Chemistry': 85}
        
        trends = analyzer._analyze_performance_trends(class_10_marks, class_12_marks)
        
        assert isinstance(trends, dict)
        assert trends['Mathematics'] == "Improving"
        assert trends['Physics'] == "Declining"
        assert trends['Chemistry'] == "Improving"
    
    def test_recommend_stream(self, analyzer):
        """Test stream recommendation."""
        strong_subjects = ['Mathematics', 'Physics', 'Chemistry']
        weak_subjects = ['English']
        academic_info = {'stream': 'Science'}
        
        recommendation = analyzer._recommend_stream(strong_subjects, weak_subjects, academic_info)
        
        assert recommendation in ['Science', 'Commerce', 'Arts', 'Mixed']
        assert recommendation == 'Science'  # Should recommend Science for this case
    
    def test_assess_competitive_exam_suitability(self, analyzer):
        """Test competitive exam suitability assessment."""
        strong_subjects = ['Mathematics', 'Physics', 'Chemistry', 'Biology']
        academic_info = {'stream': 'Science'}
        
        suitable_exams = analyzer._assess_competitive_exam_suitability(strong_subjects, academic_info)
        
        assert isinstance(suitable_exams, list)
        assert 'JEE Main' in suitable_exams
        assert 'JEE Advanced' in suitable_exams
        assert 'NEET' in suitable_exams
    
    def test_predict_academic_trajectory(self, analyzer):
        """Test academic trajectory prediction."""
        strong_subjects = ['Mathematics', 'Physics', 'Chemistry']
        performance_trends = {'Mathematics': 'Improving', 'Physics': 'Stable', 'Chemistry': 'Improving'}
        
        trajectory = analyzer._predict_academic_trajectory(strong_subjects, performance_trends)
        
        assert isinstance(trajectory, str)
        assert "trajectory" in trajectory.lower()
    
    def test_assess_overall_performance(self, analyzer):
        """Test overall performance assessment."""
        class_10_marks = {'Mathematics': 92, 'Physics': 88, 'Chemistry': 85}
        class_12_marks = {'Mathematics': 95, 'Physics': 90, 'Chemistry': 87}
        
        performance = analyzer._assess_overall_performance(class_10_marks, class_12_marks)
        
        assert performance in ['Excellent', 'Very Good', 'Good', 'Average', 'Below Average']
        assert performance == 'Excellent'  # Should be excellent for this case
    
    def test_identify_leadership_experience(self, analyzer):
        """Test leadership experience identification."""
        activities = [
            {'name': 'Science Club', 'role': 'President'},
            {'name': 'Debate', 'role': 'Captain'},
            {'name': 'Robotics', 'role': 'Member'}
        ]
        
        leadership = analyzer._identify_leadership_experience(activities)
        
        assert isinstance(leadership, list)
        assert 'Science Club' in leadership
        assert 'Debate' in leadership
    
    def test_analyze_activity_preferences(self, analyzer):
        """Test activity preferences analysis."""
        activities = [
            {'name': 'Science Club'},
            {'name': 'Robotics'},
            {'name': 'Volunteering'},
            {'name': 'Debate'}
        ]
        
        preferences = analyzer._analyze_activity_preferences(activities)
        
        assert isinstance(preferences, dict)
        assert all(0.0 <= score <= 1.0 for score in preferences.values())
        assert sum(preferences.values()) <= 1.0  # Should be normalized
    
    def test_determine_creative_vs_technical(self, analyzer):
        """Test creative vs technical determination."""
        activities = [
            {'name': 'Robotics'},
            {'name': 'Coding'},
            {'name': 'Art'},
            {'name': 'Music'}
        ]
        
        orientation = analyzer._determine_creative_vs_technical(activities)
        
        assert orientation in ['Creative-oriented', 'Technical-oriented', 'Balanced']
    
    def test_calculate_social_impact_score(self, analyzer):
        """Test social impact score calculation."""
        activities = [
            {'name': 'Volunteering'},
            {'name': 'Social Work'},
            {'name': 'Science Club'}
        ]
        
        score = analyzer._calculate_social_impact_score(activities)
        
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0
    
    def test_assess_learning_agility(self, analyzer):
        """Test learning agility assessment."""
        skill_assessments = {
            'technical_skills': {'Programming': 4, 'Data Analysis': 3},
            'soft_skills': {'Communication': 4, 'Leadership': 3}
        }
        
        agility = analyzer._assess_learning_agility(skill_assessments)
        
        assert isinstance(agility, float)
        assert 0.0 <= agility <= 1.0
    
    def test_analyze_problem_solving_approach(self, analyzer):
        """Test problem-solving approach analysis."""
        skill_assessments = {
            'soft_skills': {
                'Critical Thinking': 4,
                'Creativity': 2,
                'Problem Solving': 3
            }
        }
        
        approach = analyzer._analyze_problem_solving_approach(skill_assessments)
        
        assert isinstance(approach, str)
        assert "analytical" in approach.lower() or "creative" in approach.lower() or "practical" in approach.lower() or "balanced" in approach.lower()
    
    def test_assess_digital_literacy(self, analyzer):
        """Test digital literacy assessment."""
        skill_assessments = {
            'technical_skills': {
                'Programming': 4,
                'Web Development': 3,
                'Database Management': 2,
                'Cloud Computing': 1
            }
        }
        
        literacy = analyzer._assess_digital_literacy(skill_assessments)
        
        assert isinstance(literacy, float)
        assert 0.0 <= literacy <= 1.0
    
    def test_identify_skill_gaps(self, analyzer):
        """Test skill gaps identification."""
        technical_skills = {'Programming': 2, 'Data Analysis': 1}
        soft_skills = {'Communication': 3, 'Leadership': 2}
        
        gaps = analyzer._identify_skill_gaps(technical_skills, soft_skills)
        
        assert isinstance(gaps, list)
        assert len(gaps) <= 5
    
    def test_identify_skill_strengths(self, analyzer):
        """Test skill strengths identification."""
        technical_skills = {'Programming': 4, 'Data Analysis': 5}
        soft_skills = {'Communication': 4, 'Leadership': 3}
        
        strengths = analyzer._identify_skill_strengths(technical_skills, soft_skills)
        
        assert isinstance(strengths, list)
        assert 'Programming' in strengths
        assert 'Data Analysis' in strengths
        assert 'Communication' in strengths
    
    def test_identify_primary_interests(self, analyzer):
        """Test primary interests identification."""
        interests = ['Technology', 'Science', 'Mathematics', 'Art', 'Music']
        
        primary = analyzer._identify_primary_interests(interests)
        
        assert isinstance(primary, list)
        assert len(primary) <= 5
        assert 'Technology' in primary
        assert 'Science' in primary
        assert 'Mathematics' in primary
    
    def test_calculate_interest_intensity(self, analyzer):
        """Test interest intensity calculation."""
        interests = ['Technology', 'Science', 'Mathematics', 'Art']
        
        intensity = analyzer._calculate_interest_intensity(interests)
        
        assert isinstance(intensity, dict)
        for interest, score in intensity.items():
            assert 0.0 <= score <= 1.0
    
    def test_identify_cross_domain_connections(self, analyzer):
        """Test cross-domain connections identification."""
        interests = ['Technology', 'Science', 'Mathematics', 'Art', 'Music']
        
        connections = analyzer._identify_cross_domain_connections(interests)
        
        assert isinstance(connections, dict)
    
    def test_identify_emerging_interests(self, analyzer):
        """Test emerging interests identification."""
        interests = ['Technology', 'Science', 'Mathematics', 'Art']
        
        emerging = analyzer._identify_emerging_interests(interests)
        
        assert isinstance(emerging, list)
    
    def test_map_interests_to_career_pathways(self, analyzer):
        """Test interests to career pathways mapping."""
        interests = ['Technology', 'Science', 'Mathematics', 'Art']
        
        pathways = analyzer._map_interests_to_career_pathways(interests)
        
        assert isinstance(pathways, dict)
        assert 'Technology' in pathways
        assert 'Science' in pathways
        assert 'Mathematics' in pathways
    
    def test_cluster_similar_interests(self, analyzer):
        """Test similar interests clustering."""
        interests = ['Technology', 'Science', 'Mathematics', 'Art', 'Music']
        
        clusters = analyzer._cluster_similar_interests(interests)
        
        assert isinstance(clusters, dict)
    
    def test_identify_natural_talents(self, analyzer):
        """Test natural talents identification."""
        analysis_results = {
            'academic': AcademicAnalysis(
                strong_subjects=['Mathematics', 'Physics'],
                weak_subjects=[],
                performance_trends={},
                stream_recommendation='Science',
                competitive_exam_suitability=['JEE Main'],
                academic_trajectory='Upward',
                subject_correlations={},
                overall_performance='Excellent'
            )
        }
        
        talents = analyzer._identify_natural_talents(analysis_results)
        
        assert isinstance(talents, list)
        assert 'Academic Excellence' in talents
        assert 'Mathematical Aptitude' in talents
    
    def test_identify_career_clusters(self, analyzer):
        """Test career clusters identification."""
        analysis_results = {
            'academic': AcademicAnalysis(
                strong_subjects=['Mathematics', 'Physics'],
                weak_subjects=[],
                performance_trends={},
                stream_recommendation='Science',
                competitive_exam_suitability=['JEE Main'],
                academic_trajectory='Upward',
                subject_correlations={},
                overall_performance='Excellent'
            )
        }
        
        clusters = analyzer._identify_career_clusters(analysis_results)
        
        assert isinstance(clusters, list)
        assert 'Engineering and Technology' in clusters
    
    def test_generate_skill_development_recommendations(self, analyzer):
        """Test skill development recommendations generation."""
        analysis_results = {
            'skills': SkillsAssessment(
                technical_skills={},
                soft_skills={},
                learning_agility=0.5,
                problem_solving_approach='Balanced',
                digital_literacy=0.5,
                skill_gaps=['Programming', 'Data Analysis'],
                skill_strengths=[]
            )
        }
        
        recommendations = analyzer._generate_skill_development_recommendations(analysis_results)
        
        assert isinstance(recommendations, list)
        assert len(recommendations) <= 5
    
    def test_generate_academic_pathway_suggestions(self, analyzer):
        """Test academic pathway suggestions generation."""
        analysis_results = {
            'academic': AcademicAnalysis(
                strong_subjects=['Mathematics', 'Physics'],
                weak_subjects=[],
                performance_trends={},
                stream_recommendation='Science',
                competitive_exam_suitability=['JEE Main'],
                academic_trajectory='Upward',
                subject_correlations={},
                overall_performance='Excellent'
            )
        }
        
        suggestions = analyzer._generate_academic_pathway_suggestions(analysis_results)
        
        assert isinstance(suggestions, list)
        assert len(suggestions) > 0
    
    def test_identify_work_environment_preferences(self, analyzer):
        """Test work environment preferences identification."""
        analysis_results = {
            'extracurricular': ExtracurricularAnalysis(
                leadership_experience=[],
                activity_preferences={},
                creative_vs_technical='Technical-oriented',
                social_impact_score=0.5,
                sports_participation=[],
                team_vs_individual='Team-oriented',
                activity_diversity_score=0.5
            )
        }
        
        preferences = analyzer._identify_work_environment_preferences(analysis_results)
        
        assert isinstance(preferences, list)
    
    def test_generate_personality_insights(self, analyzer):
        """Test personality insights generation."""
        analysis_results = {
            'academic': AcademicAnalysis(
                strong_subjects=['Mathematics', 'Physics'],
                weak_subjects=[],
                performance_trends={},
                stream_recommendation='Science',
                competitive_exam_suitability=['JEE Main'],
                academic_trajectory='Upward',
                subject_correlations={},
                overall_performance='Excellent'
            )
        }
        
        insights = analyzer._generate_personality_insights(analysis_results)
        
        assert isinstance(insights, str)
        assert len(insights) > 0
    
    def test_generate_motivational_message(self, analyzer):
        """Test motivational message generation."""
        analysis_results = {
            'academic': AcademicAnalysis(
                strong_subjects=['Mathematics', 'Physics'],
                weak_subjects=[],
                performance_trends={},
                stream_recommendation='Science',
                competitive_exam_suitability=['JEE Main'],
                academic_trajectory='Upward',
                subject_correlations={},
                overall_performance='Excellent'
            )
        }
        
        message = analyzer._generate_motivational_message(analysis_results)
        
        assert isinstance(message, str)
        assert len(message) > 0
    
    def test_generate_next_steps(self, analyzer):
        """Test next steps generation."""
        analysis_results = {
            'academic': AcademicAnalysis(
                strong_subjects=['Mathematics', 'Physics'],
                weak_subjects=[],
                performance_trends={},
                stream_recommendation='Science',
                competitive_exam_suitability=['JEE Main'],
                academic_trajectory='Upward',
                subject_correlations={},
                overall_performance='Excellent'
            )
        }
        
        steps = analyzer._generate_next_steps(analysis_results)
        
        assert isinstance(steps, list)
        assert len(steps) > 0
    
    def test_assess_profile_completeness(self, analyzer, sample_profile_data):
        """Test profile completeness assessment."""
        completeness = analyzer._assess_profile_completeness(sample_profile_data)
        
        assert isinstance(completeness, ProfileCompleteness)
        assert isinstance(completeness.completeness_score, float)
        assert isinstance(completeness.missing_information, list)
        assert isinstance(completeness.profile_improvements, list)
        assert isinstance(completeness.priority_areas, list)
        assert isinstance(completeness.completion_suggestions, list)
        
        assert 0.0 <= completeness.completeness_score <= 1.0
    
    def test_generate_ai_summary(self, analyzer, sample_profile_data):
        """Test AI summary generation."""
        academic_analysis = analyzer.extract_academic_strengths(sample_profile_data['academic_info'])
        analysis_results = {'academic': academic_analysis}
        
        summary = analyzer._generate_ai_summary(analysis_results, sample_profile_data)
        
        assert isinstance(summary, str)
        assert len(summary) > 0
    
    def test_empty_profile_handling(self, analyzer):
        """Test handling of empty profile."""
        empty_profile = {}
        
        analysis = analyzer.analyze_complete_profile(empty_profile)
        
        assert isinstance(analysis, CompleteProfileAnalysis)
        assert isinstance(analysis.academic_analysis, AcademicAnalysis)
        assert isinstance(analysis.extracurricular_analysis, ExtracurricularAnalysis)
        assert isinstance(analysis.skills_assessment, SkillsAssessment)
        assert isinstance(analysis.interest_analysis, InterestAnalysis)
        assert isinstance(analysis.profile_insights, ProfileInsights)
        assert isinstance(analysis.completeness_assessment, ProfileCompleteness)
    
    def test_partial_profile_handling(self, analyzer):
        """Test handling of partial profile."""
        partial_profile = {
            'academic_info': {
                'class_10_marks': {'Mathematics': 85, 'Physics': 80}
            },
            'interests': ['Technology', 'Science']
        }
        
        analysis = analyzer.analyze_complete_profile(partial_profile)
        
        assert isinstance(analysis, CompleteProfileAnalysis)
        assert len(analysis.academic_analysis.strong_subjects) > 0
        assert len(analysis.interest_analysis.primary_interests) > 0

if __name__ == "__main__":
    pytest.main([__file__])
