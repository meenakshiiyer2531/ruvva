#!/usr/bin/env python3
"""
Example usage of Student Profile Analyzer for CareerConnect AI
Demonstrates comprehensive student profile processing and analysis specifically designed for Indian students.
"""

from services.profile_analyzer import StudentProfileAnalyzer

def main():
    """Main example function."""
    
    print("CareerConnect AI - Student Profile Analyzer Example")
    print("=" * 60)
    
    # Initialize analyzer
    analyzer = StudentProfileAnalyzer()
    
    # Sample student profiles for different scenarios
    profiles = {
        "High Achiever": {
            'academic_info': {
                'class_10_marks': {
                    'Mathematics': 95,
                    'Physics': 92,
                    'Chemistry': 90,
                    'Biology': 88,
                    'English': 85,
                    'Hindi': 82
                },
                'class_12_marks': {
                    'Mathematics': 98,
                    'Physics': 95,
                    'Chemistry': 92,
                    'Biology': 90,
                    'English': 88,
                    'Hindi': 85
                },
                'stream': 'Science',
                'competitive_exams': ['JEE Main', 'JEE Advanced', 'NEET']
            },
            'extracurricular_activities': [
                {'name': 'Science Club', 'role': 'President', 'duration': '3 years'},
                {'name': 'Math Olympiad', 'role': 'Team Captain', 'duration': '2 years'},
                {'name': 'Robotics', 'role': 'Lead Programmer', 'duration': '2 years'},
                {'name': 'Volunteering', 'role': 'Coordinator', 'duration': '4 years'},
                {'name': 'Debate', 'role': 'Captain', 'duration': '3 years'}
            ],
            'skill_assessments': {
                'technical_skills': {
                    'Programming': 5,
                    'Data Analysis': 4,
                    'Web Development': 3,
                    'Machine Learning': 2,
                    'Database Management': 3
                },
                'soft_skills': {
                    'Communication': 5,
                    'Leadership': 5,
                    'Problem Solving': 4,
                    'Teamwork': 4,
                    'Critical Thinking': 5,
                    'Time Management': 4
                }
            },
            'interests': [
                'Technology', 'Science', 'Mathematics', 'Engineering', 
                'Artificial Intelligence', 'Data Science', 'Robotics'
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
                'Become a software engineer at a top tech company',
                'Work in AI/ML research',
                'Start my own tech startup'
            ]
        },
        
        "Well-Rounded Student": {
            'academic_info': {
                'class_10_marks': {
                    'Mathematics': 85,
                    'Physics': 82,
                    'Chemistry': 80,
                    'Biology': 88,
                    'English': 90,
                    'Hindi': 85
                },
                'class_12_marks': {
                    'Mathematics': 87,
                    'Physics': 85,
                    'Chemistry': 83,
                    'Biology': 90,
                    'English': 92,
                    'Hindi': 88
                },
                'stream': 'Science',
                'competitive_exams': ['NEET', 'AIIMS']
            },
            'extracurricular_activities': [
                {'name': 'Drama', 'role': 'Lead Actor', 'duration': '3 years'},
                {'name': 'Music', 'role': 'Singer', 'duration': '4 years'},
                {'name': 'Volunteering', 'role': 'Member', 'duration': '3 years'},
                {'name': 'Photography', 'role': 'Photographer', 'duration': '2 years'},
                {'name': 'Student Council', 'role': 'Secretary', 'duration': '2 years'}
            ],
            'skill_assessments': {
                'technical_skills': {
                    'Programming': 2,
                    'Data Analysis': 1,
                    'Web Development': 1,
                    'Photography': 4
                },
                'soft_skills': {
                    'Communication': 5,
                    'Leadership': 4,
                    'Problem Solving': 3,
                    'Teamwork': 5,
                    'Creativity': 5,
                    'Presentation Skills': 4
                }
            },
            'interests': [
                'Medicine', 'Biology', 'Psychology', 'Art', 'Music', 
                'Photography', 'Social Work', 'Education'
            ],
            'riasec_scores': {
                'Realistic': 2.8,
                'Investigative': 3.5,
                'Artistic': 4.7,
                'Social': 4.5,
                'Enterprising': 3.2,
                'Conventional': 3.8
            },
            'career_goals': [
                'Become a doctor',
                'Work in healthcare',
                'Combine medicine with social work'
            ]
        },
        
        "Business-Oriented Student": {
            'academic_info': {
                'class_10_marks': {
                    'Mathematics': 88,
                    'Economics': 92,
                    'Business Studies': 90,
                    'Accountancy': 85,
                    'English': 87,
                    'Hindi': 80
                },
                'class_12_marks': {
                    'Mathematics': 90,
                    'Economics': 95,
                    'Business Studies': 92,
                    'Accountancy': 88,
                    'English': 89,
                    'Hindi': 82
                },
                'stream': 'Commerce',
                'competitive_exams': ['CAT', 'XAT', 'GMAT']
            },
            'extracurricular_activities': [
                {'name': 'Student Council', 'role': 'President', 'duration': '2 years'},
                {'name': 'Debate', 'role': 'Captain', 'duration': '3 years'},
                {'name': 'Volunteering', 'role': 'Coordinator', 'duration': '2 years'},
                {'name': 'Business Club', 'role': 'Founder', 'duration': '1 year'}
            ],
            'skill_assessments': {
                'technical_skills': {
                    'Data Analysis': 4,
                    'Project Management': 4,
                    'Digital Marketing': 3,
                    'Financial Analysis': 4
                },
                'soft_skills': {
                    'Leadership': 5,
                    'Communication': 5,
                    'Negotiation': 4,
                    'Decision Making': 4,
                    'Teamwork': 4,
                    'Public Speaking': 5
                }
            },
            'interests': [
                'Business', 'Finance', 'Economics', 'Leadership', 
                'Entrepreneurship', 'Marketing', 'Management'
            ],
            'riasec_scores': {
                'Realistic': 3.0,
                'Investigative': 3.5,
                'Artistic': 2.8,
                'Social': 4.0,
                'Enterprising': 4.8,
                'Conventional': 4.5
            },
            'career_goals': [
                'Become a management consultant',
                'Start my own business',
                'Work in investment banking'
            ]
        },
        
        "Creative Student": {
            'academic_info': {
                'class_10_marks': {
                    'English': 95,
                    'Literature': 92,
                    'History': 88,
                    'Art': 98,
                    'Mathematics': 75,
                    'Science': 70
                },
                'class_12_marks': {
                    'English': 97,
                    'Literature': 94,
                    'History': 90,
                    'Art': 99,
                    'Mathematics': 78,
                    'Science': 72
                },
                'stream': 'Arts',
                'competitive_exams': ['CLAT', 'UPSC']
            },
            'extracurricular_activities': [
                {'name': 'Drama', 'role': 'Director', 'duration': '4 years'},
                {'name': 'Art', 'role': 'Artist', 'duration': '5 years'},
                {'name': 'Music', 'role': 'Composer', 'duration': '3 years'},
                {'name': 'Journalism', 'role': 'Editor', 'duration': '2 years'},
                {'name': 'Photography', 'role': 'Photographer', 'duration': '3 years'}
            ],
            'skill_assessments': {
                'technical_skills': {
                    'UI/UX Design': 4,
                    'Digital Marketing': 3,
                    'Photography': 5,
                    'Video Editing': 3
                },
                'soft_skills': {
                    'Creativity': 5,
                    'Communication': 4,
                    'Presentation Skills': 4,
                    'Adaptability': 4,
                    'Emotional Intelligence': 4
                }
            },
            'interests': [
                'Art', 'Design', 'Music', 'Literature', 'Photography', 
                'Movies', 'Writing', 'Creative Arts'
            ],
            'riasec_scores': {
                'Realistic': 2.5,
                'Investigative': 3.0,
                'Artistic': 4.8,
                'Social': 3.8,
                'Enterprising': 3.5,
                'Conventional': 2.8
            },
            'career_goals': [
                'Become a graphic designer',
                'Work in advertising',
                'Start my own creative agency'
            ]
        }
    }
    
    # Analyze each profile
    for profile_name, profile_data in profiles.items():
        print(f"\n{'='*60}")
        print(f"ANALYZING: {profile_name}")
        print(f"{'='*60}")
        
        # Perform comprehensive analysis
        analysis = analyzer.analyze_complete_profile(profile_data)
        
        # Display Academic Analysis
        print(f"\n📚 ACADEMIC ANALYSIS:")
        academic = analysis.academic_analysis
        print(f"  Strong Subjects: {', '.join(academic.strong_subjects)}")
        print(f"  Weak Subjects: {', '.join(academic.weak_subjects)}")
        print(f"  Stream Recommendation: {academic.stream_recommendation}")
        print(f"  Overall Performance: {academic.overall_performance}")
        print(f"  Competitive Exam Suitability: {', '.join(academic.competitive_exam_suitability)}")
        print(f"  Academic Trajectory: {academic.academic_trajectory}")
        
        # Display Extracurricular Analysis
        print(f"\n🎯 EXTRACURRICULAR ANALYSIS:")
        extracurricular = analysis.extracurricular_analysis
        print(f"  Leadership Experience: {', '.join(extracurricular.leadership_experience)}")
        print(f"  Creative vs Technical: {extracurricular.creative_vs_technical}")
        print(f"  Social Impact Score: {extracurricular.social_impact_score:.2f}")
        print(f"  Sports Participation: {', '.join(extracurricular.sports_participation)}")
        print(f"  Team vs Individual: {extracurricular.team_vs_individual}")
        print(f"  Activity Diversity Score: {extracurricular.activity_diversity_score:.2f}")
        
        # Display Skills Assessment
        print(f"\n🔧 SKILLS ASSESSMENT:")
        skills = analysis.skills_assessment
        print(f"  Learning Agility: {skills.learning_agility:.2f}")
        print(f"  Problem Solving Approach: {skills.problem_solving_approach}")
        print(f"  Digital Literacy: {skills.digital_literacy:.2f}")
        print(f"  Skill Strengths: {', '.join(skills.skill_strengths)}")
        print(f"  Skill Gaps: {', '.join(skills.skill_gaps)}")
        
        # Display Interest Analysis
        print(f"\n💡 INTEREST ANALYSIS:")
        interests = analysis.interest_analysis
        print(f"  Primary Interests: {', '.join(interests.primary_interests)}")
        print(f"  Emerging Interests: {', '.join(interests.emerging_interests)}")
        print(f"  Interest Clusters: {list(interests.interest_clusters.keys())}")
        print(f"  Career Pathway Mapping:")
        for interest, pathways in interests.career_pathway_mapping.items():
            print(f"    {interest}: {', '.join(pathways)}")
        
        # Display Profile Insights
        print(f"\n🌟 PROFILE INSIGHTS:")
        insights = analysis.profile_insights
        print(f"  Natural Talents: {', '.join(insights.natural_talents)}")
        print(f"  Career Clusters: {', '.join(insights.career_clusters)}")
        print(f"  Skill Development Recommendations:")
        for i, rec in enumerate(insights.skill_development_recommendations, 1):
            print(f"    {i}. {rec}")
        print(f"  Academic Pathway Suggestions:")
        for i, suggestion in enumerate(insights.academic_pathway_suggestions, 1):
            print(f"    {i}. {suggestion}")
        print(f"  Work Environment Preferences: {', '.join(insights.work_environment_preferences)}")
        print(f"  Personality Insights: {insights.personality_insights}")
        print(f"  Motivational Message: {insights.motivational_message}")
        print(f"  Next Steps:")
        for i, step in enumerate(insights.next_steps, 1):
            print(f"    {i}. {step}")
        
        # Display Profile Completeness
        print(f"\n📊 PROFILE COMPLETENESS:")
        completeness = analysis.completeness_assessment
        print(f"  Completeness Score: {completeness.completeness_score:.2f}")
        print(f"  Missing Information: {', '.join(completeness.missing_information)}")
        print(f"  Priority Areas: {', '.join(completeness.priority_areas)}")
        print(f"  Completion Suggestions:")
        for i, suggestion in enumerate(completeness.completion_suggestions, 1):
            print(f"    {i}. {suggestion}")
        
        # Display AI Summary
        print(f"\n🤖 AI-GENERATED SUMMARY:")
        print(f"  {analysis.ai_generated_summary}")
        
        # Display Analysis Timestamp
        print(f"\n⏰ Analysis Completed: {analysis.analysis_timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Demonstrate individual methods
    print(f"\n{'='*60}")
    print("INDIVIDUAL METHOD DEMONSTRATIONS")
    print(f"{'='*60}")
    
    # Use the first profile for demonstrations
    sample_profile = profiles["High Achiever"]
    
    print(f"\n🔍 ACADEMIC STRENGTHS EXTRACTION:")
    academic_analysis = analyzer.extract_academic_strengths(sample_profile['academic_info'])
    print(f"  Strong Subjects: {', '.join(academic_analysis.strong_subjects)}")
    print(f"  Stream Recommendation: {academic_analysis.stream_recommendation}")
    print(f"  Competitive Exams: {', '.join(academic_analysis.competitive_exam_suitability)}")
    
    print(f"\n🎯 EXTRACURRICULAR PATTERNS ANALYSIS:")
    extracurricular_analysis = analyzer.analyze_extracurricular_patterns(sample_profile['extracurricular_activities'])
    print(f"  Leadership Experience: {', '.join(extracurricular_analysis.leadership_experience)}")
    print(f"  Activity Preferences: {extracurricular_analysis.activity_preferences}")
    print(f"  Creative vs Technical: {extracurricular_analysis.creative_vs_technical}")
    
    print(f"\n🔧 SKILLS LEVELS ASSESSMENT:")
    skills_assessment = analyzer.assess_skill_levels(sample_profile['skill_assessments'])
    print(f"  Learning Agility: {skills_assessment.learning_agility:.2f}")
    print(f"  Problem Solving Approach: {skills_assessment.problem_solving_approach}")
    print(f"  Digital Literacy: {skills_assessment.digital_literacy:.2f}")
    
    print(f"\n💡 INTEREST CLUSTERS IDENTIFICATION:")
    interest_analysis = analyzer.identify_interest_clusters(sample_profile['interests'])
    print(f"  Primary Interests: {', '.join(interest_analysis.primary_interests)}")
    print(f"  Interest Intensity: {interest_analysis.interest_intensity}")
    print(f"  Interest Clusters: {interest_analysis.interest_clusters}")
    
    print(f"\n🌟 PROFILE INSIGHTS GENERATION:")
    analysis_results = {
        'academic': academic_analysis,
        'extracurricular': extracurricular_analysis,
        'skills': skills_assessment,
        'interests': interest_analysis
    }
    profile_insights = analyzer.generate_profile_insights(analysis_results)
    print(f"  Natural Talents: {', '.join(profile_insights.natural_talents)}")
    print(f"  Career Clusters: {', '.join(profile_insights.career_clusters)}")
    print(f"  Next Steps: {', '.join(profile_insights.next_steps)}")
    
    # Demonstrate helper methods
    print(f"\n🛠️ HELPER METHODS DEMONSTRATION:")
    
    # Test strong subjects identification
    class_10_marks = sample_profile['academic_info']['class_10_marks']
    class_12_marks = sample_profile['academic_info']['class_12_marks']
    strong_subjects = analyzer._identify_strong_subjects(class_10_marks, class_12_marks)
    print(f"  Strong Subjects Identified: {', '.join(strong_subjects)}")
    
    # Test weak subjects identification
    weak_subjects = analyzer._identify_weak_subjects(class_10_marks, class_12_marks)
    print(f"  Weak Subjects Identified: {', '.join(weak_subjects)}")
    
    # Test performance trends analysis
    performance_trends = analyzer._analyze_performance_trends(class_10_marks, class_12_marks)
    print(f"  Performance Trends: {performance_trends}")
    
    # Test stream recommendation
    stream_recommendation = analyzer._recommend_stream(strong_subjects, weak_subjects, sample_profile['academic_info'])
    print(f"  Stream Recommendation: {stream_recommendation}")
    
    # Test competitive exam suitability
    competitive_exams = analyzer._assess_competitive_exam_suitability(strong_subjects, sample_profile['academic_info'])
    print(f"  Competitive Exam Suitability: {', '.join(competitive_exams)}")
    
    # Test academic trajectory prediction
    academic_trajectory = analyzer._predict_academic_trajectory(strong_subjects, performance_trends)
    print(f"  Academic Trajectory: {academic_trajectory}")
    
    # Test overall performance assessment
    overall_performance = analyzer._assess_overall_performance(class_10_marks, class_12_marks)
    print(f"  Overall Performance: {overall_performance}")
    
    print(f"\n{'='*60}")
    print("EXAMPLE COMPLETE")
    print(f"{'='*60}")
    
    print(f"\nThis example demonstrates:")
    print("• Comprehensive academic performance analysis")
    print("• Extracurricular pattern recognition")
    print("• Skills assessment and gap identification")
    print("• Interest cluster analysis and career mapping")
    print("• Natural talent identification")
    print("• Career cluster recommendations")
    print("• Skill development recommendations")
    print("• Academic pathway suggestions")
    print("• Work environment preferences")
    print("• Personality insights generation")
    print("• Motivational message creation")
    print("• Next steps recommendations")
    print("• Profile completeness assessment")
    print("• AI-powered summary generation")
    
    print(f"\nTo use this analyzer in your application:")
    print("1. Initialize: analyzer = StudentProfileAnalyzer()")
    print("2. Analyze: analysis = analyzer.analyze_complete_profile(profile_data)")
    print("3. Access results: academic = analysis.academic_analysis, insights = analysis.profile_insights")
    print("4. Use insights: talents = insights.natural_talents, clusters = insights.career_clusters")

if __name__ == "__main__":
    main()
