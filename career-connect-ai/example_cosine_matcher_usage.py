#!/usr/bin/env python3
"""
Example usage of Cosine Career Matcher for CareerConnect AI
Demonstrates intelligent career matching using cosine similarity and multi-dimensional analysis.
"""

from core.cosine_matcher import CosineCareerMatcher

def main():
    """Main example function."""
    
    print("CareerConnect AI - Cosine Career Matcher Example")
    print("=" * 60)
    
    # Initialize matcher
    matcher = CosineCareerMatcher()
    
    # Sample student profiles for different scenarios
    profiles = {
        "Tech Enthusiast": {
            'academic_subjects': {
                'Mathematics': 'A+',
                'Physics': 'A',
                'Chemistry': 'B+',
                'Computer Science': 'A+',
                'English': 'B'
            },
            'extracurricular_activities': ['Coding', 'Robotics', 'Math Olympiad'],
            'technical_skills': {
                'Programming': 'Expert',
                'Data Analysis': 'Advanced',
                'Web Development': 'Intermediate',
                'Machine Learning': 'Beginner',
                'Database Management': 'Intermediate'
            },
            'soft_skills': {
                'Communication': 'Advanced',
                'Problem Solving': 'Expert',
                'Leadership': 'Intermediate',
                'Teamwork': 'Advanced',
                'Critical Thinking': 'Expert'
            },
            'riasec_scores': {
                'Realistic': 3.5,
                'Investigative': 4.8,
                'Artistic': 2.1,
                'Social': 3.2,
                'Enterprising': 3.8,
                'Conventional': 4.2
            },
            'interests': ['Technology', 'Science', 'Mathematics', 'Engineering', 'AI'],
            'career_preferences': ['High Salary', 'Career Growth', 'Innovation', 'Creative Freedom'],
            'location_preferences': ['Bangalore', 'Mumbai', 'Delhi', 'Hyderabad'],
            'salary_expectations': '15+ LPA',
            'work_environment_preferences': ['Office', 'Hybrid', 'Remote']
        },
        
        "Medical Aspirant": {
            'academic_subjects': {
                'Biology': 'A+',
                'Chemistry': 'A+',
                'Physics': 'A',
                'Mathematics': 'B+',
                'English': 'A'
            },
            'extracurricular_activities': ['Science Club', 'Volunteering', 'Debate'],
            'technical_skills': {
                'Research': 'Advanced',
                'Data Analysis': 'Intermediate',
                'Communication': 'Expert'
            },
            'soft_skills': {
                'Communication': 'Expert',
                'Problem Solving': 'Advanced',
                'Empathy': 'Expert',
                'Teamwork': 'Advanced',
                'Leadership': 'Intermediate'
            },
            'riasec_scores': {
                'Realistic': 2.8,
                'Investigative': 4.5,
                'Artistic': 2.5,
                'Social': 4.7,
                'Enterprising': 3.2,
                'Conventional': 4.0
            },
            'interests': ['Medicine', 'Science', 'Biology', 'Psychology', 'Social Work'],
            'career_preferences': ['Social Impact', 'Job Security', 'Career Growth'],
            'location_preferences': ['Delhi', 'Mumbai', 'Bangalore', 'Chennai'],
            'salary_expectations': '10-15 LPA',
            'work_environment_preferences': ['Hospital', 'Office']
        },
        
        "Business Leader": {
            'academic_subjects': {
                'Mathematics': 'A',
                'Economics': 'A+',
                'Business Studies': 'A+',
                'English': 'A',
                'Accountancy': 'A'
            },
            'extracurricular_activities': ['Student Council', 'Debate', 'Volunteering'],
            'technical_skills': {
                'Data Analysis': 'Advanced',
                'Project Management': 'Advanced',
                'Communication': 'Expert'
            },
            'soft_skills': {
                'Leadership': 'Expert',
                'Communication': 'Expert',
                'Negotiation': 'Advanced',
                'Decision Making': 'Expert',
                'Teamwork': 'Advanced'
            },
            'riasec_scores': {
                'Realistic': 3.0,
                'Investigative': 3.5,
                'Artistic': 3.2,
                'Social': 4.0,
                'Enterprising': 4.8,
                'Conventional': 4.5
            },
            'interests': ['Business', 'Finance', 'Economics', 'Leadership', 'Politics'],
            'career_preferences': ['Leadership Opportunities', 'High Salary', 'Career Growth', 'Travel'],
            'location_preferences': ['Mumbai', 'Delhi', 'Bangalore', 'Gurgaon'],
            'salary_expectations': '15+ LPA',
            'work_environment_preferences': ['Office', 'Hybrid']
        },
        
        "Creative Artist": {
            'academic_subjects': {
                'Art': 'A+',
                'English': 'A+',
                'Literature': 'A',
                'History': 'A',
                'Mathematics': 'C+'
            },
            'extracurricular_activities': ['Drama', 'Art', 'Music', 'Photography'],
            'technical_skills': {
                'UI/UX Design': 'Advanced',
                'Digital Marketing': 'Intermediate',
                'Photography': 'Expert'
            },
            'soft_skills': {
                'Creativity': 'Expert',
                'Communication': 'Advanced',
                'Presentation Skills': 'Advanced',
                'Adaptability': 'Expert'
            },
            'riasec_scores': {
                'Realistic': 2.5,
                'Investigative': 3.0,
                'Artistic': 4.8,
                'Social': 3.8,
                'Enterprising': 3.5,
                'Conventional': 2.8
            },
            'interests': ['Art', 'Design', 'Music', 'Literature', 'Photography', 'Movies'],
            'career_preferences': ['Creative Freedom', 'Flexible Schedule', 'Social Impact'],
            'location_preferences': ['Mumbai', 'Delhi', 'Bangalore', 'Chennai'],
            'salary_expectations': '6-10 LPA',
            'work_environment_preferences': ['Studio', 'Office', 'Remote']
        }
    }
    
    # Analyze each profile
    for profile_name, profile_data in profiles.items():
        print(f"\n{'='*60}")
        print(f"ANALYZING: {profile_name}")
        print(f"{'='*60}")
        
        # Get comprehensive recommendations
        recommendations = matcher.get_career_recommendations(profile_data)
        
        # Display primary recommendations
        print(f"\n🎯 PRIMARY RECOMMENDATIONS (80%+ match):")
        if recommendations['primary_recommendations']:
            for i, match in enumerate(recommendations['primary_recommendations'], 1):
                print(f"\n{i}. {match.career_name}")
                print(f"   Match: {match.match_percentage:.1f}% ({match.confidence_level})")
                print(f"   Explanation: {match.explanation}")
                print(f"   Salary Range: {match.indian_context.get('salary_range', 'N/A')}")
                print(f"   Growth Prospects: {match.indian_context.get('growth_prospects', 'N/A')}")
                print(f"   Top Colleges: {', '.join(match.indian_context.get('top_colleges', []))}")
                print(f"   Entrance Exams: {', '.join(match.indian_context.get('entrance_exams', []))}")
                print(f"   Skill Gaps: {', '.join(match.skill_gaps[:3])}")
        else:
            print("   No primary recommendations found.")
        
        # Display secondary recommendations
        print(f"\n🔍 SECONDARY RECOMMENDATIONS (60-79% match):")
        if recommendations['secondary_recommendations']:
            for i, match in enumerate(recommendations['secondary_recommendations'], 1):
                print(f"\n{i}. {match.career_name}")
                print(f"   Match: {match.match_percentage:.1f}% ({match.confidence_level})")
                print(f"   Explanation: {match.explanation}")
                print(f"   Salary Range: {match.indian_context.get('salary_range', 'N/A')}")
        else:
            print("   No secondary recommendations found.")
        
        # Display emerging opportunities
        print(f"\n🚀 EMERGING OPPORTUNITIES (40-59% match):")
        if recommendations['emerging_opportunities']:
            for i, match in enumerate(recommendations['emerging_opportunities'], 1):
                print(f"\n{i}. {match.career_name}")
                print(f"   Match: {match.match_percentage:.1f}% ({match.confidence_level})")
                print(f"   Explanation: {match.explanation}")
        else:
            print("   No emerging opportunities found.")
        
        # Display summary
        print(f"\n📊 ANALYSIS SUMMARY:")
        summary = recommendations['summary']
        print(f"   Total Careers Analyzed: {summary['total_careers_analyzed']}")
        if summary['top_match']:
            print(f"   Top Match: {summary['top_match'].career_name} ({summary['top_match'].match_percentage:.1f}%)")
        print(f"   Average Match Score: {summary['average_match_score']:.3f}")
        print(f"   Confidence Distribution: {summary['confidence_distribution']}")
        
        # Display improvement suggestions for top match
        if summary['top_match']:
            print(f"\n💡 IMPROVEMENT SUGGESTIONS FOR {summary['top_match'].career_name}:")
            for i, suggestion in enumerate(summary['top_match'].improvement_suggestions, 1):
                print(f"   {i}. {suggestion}")
    
    # Demonstrate individual methods
    print(f"\n{'='*60}")
    print("INDIVIDUAL METHOD DEMONSTRATIONS")
    print(f"{'='*60}")
    
    # Use the first profile for demonstrations
    sample_profile = profiles["Tech Enthusiast"]
    
    print(f"\n🔧 PROFILE VECTORIZATION:")
    profile_vector = matcher.calculate_profile_vector(sample_profile)
    print(f"   Profile vector dimensions: {len(profile_vector.to_array())}")
    print(f"   Academic subjects vector: {len(profile_vector.academic_subjects)} dimensions")
    print(f"   Technical skills vector: {len(profile_vector.technical_skills)} dimensions")
    print(f"   RIASEC scores vector: {len(profile_vector.riasec_scores)} dimensions")
    
    print(f"\n🎯 CAREER VECTORIZATION:")
    career_vectors = matcher.calculate_career_vectors(matcher.career_database)
    print(f"   Total careers processed: {len(career_vectors)}")
    print(f"   Career vector dimensions: {len(career_vectors[0][1].to_array())}")
    
    print(f"\n📐 COSINE SIMILARITY CALCULATION:")
    similarities = []
    for career_name, career_vector in career_vectors[:5]:  # Show top 5
        similarity = matcher.compute_cosine_similarity(profile_vector, career_vector)
        similarities.append((career_name, similarity))
        print(f"   {career_name}: {similarity:.3f}")
    
    print(f"\n🏆 CAREER RANKING:")
    ranked_matches = matcher.rank_career_matches(similarities)
    for i, (career_name, similarity) in enumerate(ranked_matches, 1):
        print(f"   {i}. {career_name}: {similarity:.3f}")
    
    print(f"\n📝 MATCH EXPLANATIONS:")
    explanations = matcher.generate_match_explanations(ranked_matches[:3])
    for match in explanations:
        print(f"   {match.career_name}: {match.explanation}")
        print(f"     Confidence: {match.confidence_level}")
        print(f"     Skill Gaps: {', '.join(match.skill_gaps[:2])}")
    
    # Demonstrate feature mappings
    print(f"\n🗺️ FEATURE MAPPINGS:")
    mappings = matcher.get_feature_mappings()
    print(f"   Academic Subjects: {len(mappings['academic_subjects'])} categories")
    print(f"   Technical Skills: {len(mappings['technical_skills'])} categories")
    print(f"   Soft Skills: {len(mappings['soft_skills'])} categories")
    print(f"   Interests: {len(mappings['interests'])} categories")
    print(f"   Locations: {len(mappings['locations'])} cities")
    print(f"   Salary Ranges: {len(mappings['salary_ranges'])} ranges")
    
    # Show sample mappings
    print(f"\n   Sample Academic Subjects:")
    for subject, idx in list(mappings['academic_subjects'].items())[:5]:
        print(f"     {subject}: {idx}")
    
    print(f"\n   Sample Technical Skills:")
    for skill, idx in list(mappings['technical_skills'].items())[:5]:
        print(f"     {skill}: {idx}")
    
    print(f"\n   Sample Locations:")
    for location, idx in list(mappings['locations'].items())[:5]:
        print(f"     {location}: {idx}")
    
    # Demonstrate career database
    print(f"\n💼 CAREER DATABASE:")
    careers = matcher.get_career_database()
    print(f"   Total careers: {len(careers)}")
    print(f"   Sample careers:")
    for i, career in enumerate(careers[:5], 1):
        print(f"     {i}. {career['career']}")
        print(f"        Education: {', '.join(career['education_requirements'])}")
        print(f"        Skills: {', '.join(career['essential_skills'])}")
        print(f"        Personality: {', '.join(career['personality_fit'])}")
        print(f"        Salary: {career['salary_range']}")
        print(f"        Demand: {career['job_market_demand']}")
        print(f"        Growth: {career['growth_prospects']}")
        print(f"        Locations: {', '.join(career['location_availability'])}")
        print()
    
    print(f"\n{'='*60}")
    print("EXAMPLE COMPLETE")
    print(f"{'='*60}")
    
    print(f"\nThis example demonstrates:")
    print("• Multi-dimensional profile vectorization")
    print("• Career database vectorization")
    print("• Weighted cosine similarity calculation")
    print("• Dynamic weighting based on student profile")
    print("• Comprehensive career recommendations")
    print("• Indian job market integration")
    print("• Skill gap identification")
    print("• Improvement suggestions")
    print("• Confidence level assessment")
    print("• Feature mapping and career database access")
    
    print(f"\nTo use this matcher in your application:")
    print("1. Initialize: matcher = CosineCareerMatcher()")
    print("2. Create profile: profile_vector = matcher.calculate_profile_vector(student_data)")
    print("3. Get recommendations: recommendations = matcher.get_career_recommendations(student_data)")
    print("4. Access results: primary, secondary, emerging, alternative = recommendations['primary_recommendations'], ...")

if __name__ == "__main__":
    main()
