#!/usr/bin/env python3
"""
Example usage of Career Discovery Service for CareerConnect AI
Demonstrates comprehensive career exploration and discovery specifically designed for Indian students.
"""

from services.career_discovery import CareerDiscoveryService

def main():
    """Main example function."""
    
    print("CareerConnect AI - Career Discovery Service Example")
    print("=" * 60)
    
    # Initialize service
    service = CareerDiscoveryService()
    
    # Sample student profiles for different scenarios
    profiles = {
        "Tech-Enthusiast Student": {
            'academic_info': {
                'stream': 'Science',
                'class_10_marks': {'Mathematics': 95, 'Physics': 92, 'Chemistry': 90, 'English': 85},
                'class_12_marks': {'Mathematics': 98, 'Physics': 95, 'Chemistry': 92, 'English': 88}
            },
            'skill_assessments': {
                'technical_skills': {
                    'Programming': 5,
                    'Data Analysis': 4,
                    'Web Development': 3,
                    'Machine Learning': 2,
                    'Problem Solving': 5
                },
                'soft_skills': {
                    'Communication': 4,
                    'Leadership': 3,
                    'Teamwork': 4,
                    'Critical Thinking': 5
                }
            },
            'interests': [
                'Technology', 'Programming', 'Data Science', 'Artificial Intelligence', 
                'Software Development', 'Machine Learning', 'Web Development'
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
                'work_environment': 'tech_company',
                'career_growth': 'fast'
            }
        },
        
        "Healthcare-Focused Student": {
            'academic_info': {
                'stream': 'Science',
                'class_10_marks': {'Biology': 95, 'Chemistry': 92, 'Physics': 88, 'English': 90},
                'class_12_marks': {'Biology': 98, 'Chemistry': 95, 'Physics': 90, 'English': 92}
            },
            'skill_assessments': {
                'technical_skills': {
                    'Medical Knowledge': 4,
                    'Research': 3,
                    'Data Analysis': 2
                },
                'soft_skills': {
                    'Communication': 5,
                    'Empathy': 5,
                    'Problem Solving': 4,
                    'Leadership': 3,
                    'Teamwork': 4
                }
            },
            'interests': [
                'Medicine', 'Biology', 'Healthcare', 'Medical Research', 
                'Public Health', 'Psychology', 'Human Anatomy'
            ],
            'riasec_scores': {
                'Realistic': 2.8,
                'Investigative': 4.5,
                'Artistic': 2.5,
                'Social': 4.8,
                'Enterprising': 3.2,
                'Conventional': 3.5
            },
            'preferences': {
                'salary_expectation': 'medium',
                'work_location': 'Delhi',
                'work_environment': 'hospital',
                'career_growth': 'stable'
            }
        },
        
        "Business-Oriented Student": {
            'academic_info': {
                'stream': 'Commerce',
                'class_10_marks': {'Mathematics': 88, 'Economics': 92, 'Business Studies': 90, 'English': 87},
                'class_12_marks': {'Mathematics': 90, 'Economics': 95, 'Business Studies': 92, 'English': 89}
            },
            'skill_assessments': {
                'technical_skills': {
                    'Data Analysis': 4,
                    'Financial Analysis': 4,
                    'Project Management': 3,
                    'Digital Marketing': 2
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
                'Business', 'Finance', 'Economics', 'Management', 
                'Entrepreneurship', 'Marketing', 'Leadership'
            ],
            'riasec_scores': {
                'Realistic': 3.0,
                'Investigative': 3.5,
                'Artistic': 2.8,
                'Social': 4.0,
                'Enterprising': 4.8,
                'Conventional': 4.5
            },
            'preferences': {
                'salary_expectation': 'very_high',
                'work_location': 'Mumbai',
                'work_environment': 'corporate',
                'career_growth': 'fast'
            }
        }
    }
    
    # Demonstrate career discovery for each profile
    for profile_name, profile_data in profiles.items():
        print(f"\n{'='*60}")
        print(f"CAREER DISCOVERY FOR: {profile_name}")
        print(f"{'='*60}")
        
        # Discover careers by profile
        discovery_result = service.discover_careers_by_profile(profile_data)
        
        # Display Primary Matches
        print(f"\n🎯 PRIMARY CAREER MATCHES:")
        for i, match in enumerate(discovery_result.primary_matches[:5], 1):
            career = service.get_career_details(match.career_id)
            print(f"  {i}. {career.title}")
            print(f"     Match Score: {match.match_score:.2f}")
            print(f"     Match Reasons: {', '.join(match.match_reasons)}")
            if match.skill_gaps:
                print(f"     Skill Gaps: {', '.join(match.skill_gaps)}")
            print(f"     Industry: {career.industry}")
            print(f"     Salary Range: ₹{career.salary_ranges['entry']['min']:,} - ₹{career.salary_ranges['entry']['max']:,}")
            print()
        
        # Display Alternative Careers
        print(f"\n🔄 ALTERNATIVE CAREER PATHS:")
        for i, match in enumerate(discovery_result.alternative_careers[:3], 1):
            career = service.get_career_details(match.career_id)
            print(f"  {i}. {career.title}")
            print(f"     Similarity Score: {match.match_score:.2f}")
            print(f"     Reasons: {', '.join(match.match_reasons)}")
            print()
        
        # Display Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        for i, recommendation in enumerate(discovery_result.recommendations, 1):
            print(f"  {i}. {recommendation}")
        
        # Display Discovery Timestamp
        print(f"\n⏰ Discovery Completed: {discovery_result.discovery_timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Demonstrate individual methods
    print(f"\n{'='*60}")
    print("INDIVIDUAL METHOD DEMONSTRATIONS")
    print(f"{'='*60}")
    
    # Use the first profile for demonstrations
    sample_profile = profiles["Tech-Enthusiast Student"]
    
    print(f"\n🔍 KEYWORD-BASED CAREER SEARCH:")
    search_terms = ['software', 'programming', 'data']
    keyword_matches = service.search_careers_by_keywords(search_terms)
    print(f"  Search Terms: {', '.join(search_terms)}")
    print(f"  Found {len(keyword_matches)} matches:")
    for i, match in enumerate(keyword_matches[:3], 1):
        career = service.get_career_details(match.career_id)
        print(f"    {i}. {career.title} (Score: {match.match_score:.2f})")
        print(f"       Reasons: {', '.join(match.match_reasons)}")
    
    print(f"\n🔗 SIMILAR CAREERS:")
    similar_careers = service.find_similar_careers('software_engineer')
    print(f"  Similar to Software Engineer:")
    for i, match in enumerate(similar_careers[:3], 1):
        career = service.get_career_details(match.career_id)
        print(f"    {i}. {career.title} (Similarity: {match.match_score:.2f})")
        print(f"       Reasons: {', '.join(match.match_reasons)}")
    
    print(f"\n📈 TRENDING CAREERS:")
    trending_careers = service.get_trending_careers()
    print(f"  Currently trending careers:")
    for i, career in enumerate(trending_careers[:3], 1):
        print(f"    {i}. {career.title}")
        print(f"       Growth Rate: {career.indian_context.get('growth_rate', 0):.1%}")
        print(f"       Market Demand: {career.indian_context.get('market_demand', 'stable')}")
        print(f"       Future Outlook: {career.indian_context.get('future_outlook', 'positive')}")
    
    print(f"\n📊 CAREER GROWTH ANALYSIS:")
    growth_analysis = service.analyze_career_growth('software_engineer')
    print(f"  Software Engineer Growth Analysis:")
    print(f"    Growth Rate: {growth_analysis.get('growth_rate', 0):.1%}")
    print(f"    Market Demand: {growth_analysis.get('market_demand', 'stable')}")
    print(f"    Future Outlook: {growth_analysis.get('future_outlook', 'positive')}")
    print(f"    Trending: {growth_analysis.get('trending', False)}")
    print(f"    Top Companies: {', '.join(growth_analysis.get('top_companies', [])[:3])}")
    print(f"    Growth Cities: {', '.join(growth_analysis.get('growth_cities', [])[:3])}")
    
    print(f"\n📋 CAREER DETAILS:")
    career_details = service.get_career_details('data_scientist')
    if career_details:
        print(f"  {career_details.title}")
        print(f"    Description: {career_details.description}")
        print(f"    Required Education: {', '.join(career_details.required_education)}")
        print(f"    Essential Skills: {', '.join(career_details.essential_skills)}")
        print(f"    Industry: {career_details.industry}")
        print(f"    Salary Ranges:")
        for level, salary_range in career_details.salary_ranges.items():
            print(f"      {level.title()}: ₹{salary_range['min']:,} - ₹{salary_range['max']:,}")
        print(f"    Indian Context:")
        print(f"      Trending: {career_details.indian_context.get('trending', False)}")
        print(f"      Growth Rate: {career_details.indian_context.get('growth_rate', 0):.1%}")
        print(f"      Market Demand: {career_details.indian_context.get('market_demand', 'stable')}")
        print(f"      Top Companies: {', '.join(career_details.indian_context.get('top_companies', [])[:3])}")
    
    # Demonstrate helper methods
    print(f"\n🛠️ HELPER METHODS DEMONSTRATION:")
    
    # Test skill matching
    required_skills = ['Programming', 'Problem Solving', 'Data Structures']
    user_skills = {'Programming': 4, 'Problem Solving': 3, 'Communication': 2}
    skill_match = service._calculate_skill_match(required_skills, user_skills)
    print(f"  Skill Match Score: {skill_match:.2f}")
    
    # Test interest matching
    industry = 'Technology'
    interests = ['Technology', 'Programming', 'Data Science', 'Art']
    interest_match = service._calculate_interest_match(industry, interests)
    print(f"  Interest Match Score: {interest_match:.2f}")
    
    # Test education matching
    required_education = ['Bachelor in Computer Science', 'Bachelor in Engineering']
    academic_info = {'stream': 'Science'}
    education_match = service._calculate_education_match(required_education, academic_info)
    print(f"  Education Match Score: {education_match:.2f}")
    
    # Test personality matching
    career = service.career_database['software_engineer']
    riasec_scores = {
        'Realistic': 3.5,
        'Investigative': 4.8,
        'Artistic': 2.1,
        'Social': 3.2,
        'Enterprising': 3.8,
        'Conventional': 4.2
    }
    personality_match = service._calculate_personality_match(career, riasec_scores)
    print(f"  Personality Match Score: {personality_match:.2f}")
    
    # Test skill gap identification
    skill_gaps = service._identify_skill_gaps(required_skills, user_skills)
    print(f"  Skill Gaps: {', '.join(skill_gaps)}")
    
    # Test keyword matching
    career = service.career_database['software_engineer']
    search_terms = ['software', 'programming', 'technology']
    keyword_score = service._calculate_keyword_match_score(career, search_terms)
    print(f"  Keyword Match Score: {keyword_score:.2f}")
    
    # Test career similarity
    career1 = service.career_database['software_engineer']
    career2 = service.career_database['data_scientist']
    similarity = service._calculate_career_similarity(career1, career2)
    print(f"  Career Similarity Score: {similarity:.2f}")
    
    print(f"\n{'='*60}")
    print("EXAMPLE COMPLETE")
    print(f"{'='*60}")
    
    print(f"\nThis example demonstrates:")
    print("• Profile-based career discovery")
    print("• Keyword-based career search")
    print("• Detailed career information retrieval")
    print("• Similar career recommendations")
    print("• Trending career analysis")
    print("• Career growth prospects analysis")
    print("• Multi-factor career matching (skills, interests, education, personality)")
    print("• Indian job market integration")
    print("• Skill gap identification")
    print("• Alternative career path discovery")
    print("• Comprehensive career insights generation")
    
    print(f"\nTo use this service in your application:")
    print("1. Initialize: service = CareerDiscoveryService()")
    print("2. Discover: result = service.discover_careers_by_profile(student_profile)")
    print("3. Search: matches = service.search_careers_by_keywords(['software', 'programming'])")
    print("4. Get details: career = service.get_career_details('software_engineer')")
    print("5. Find similar: similar = service.find_similar_careers('software_engineer')")
    print("6. Get trending: trending = service.get_trending_careers()")
    print("7. Analyze growth: growth = service.analyze_career_growth('software_engineer')")

if __name__ == "__main__":
    main()
