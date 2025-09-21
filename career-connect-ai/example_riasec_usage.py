#!/usr/bin/env python3
"""
Example usage of RIASEC Analyzer for CareerConnect AI
Demonstrates how to use the analyzer for personality assessment and career matching.
"""

import json
from core.riasec_analyzer import RIASECAnalyzer

def main():
    """Main example function."""
    
    print("CareerConnect AI - RIASEC Personality Assessment Example")
    print("=" * 60)
    
    # Initialize analyzer
    analyzer = RIASECAnalyzer()
    
    # Sample assessment responses (simulating a student's answers)
    sample_responses = {
        # Realistic questions (R1-R6)
        'R1': 4,  # Agree - "You enjoy working with your hands and building things"
        'R2': 3,  # Neutral - "You prefer outdoor activities over indoor work"
        'R3': 5,  # Strongly Agree - "You like working with tools and machinery"
        'R4': 4,  # Agree - "You enjoy physical activities and sports"
        'R5': 4,  # Agree - "You prefer concrete, practical solutions over abstract ideas"
        'R6': 2,  # Disagree - "You like working with animals or plants"
        
        # Investigative questions (I1-I6)
        'I1': 5,  # Strongly Agree - "You enjoy solving complex problems and puzzles"
        'I2': 4,  # Agree - "You like to understand how things work"
        'I3': 4,  # Agree - "You prefer working independently on research projects"
        'I4': 3,  # Neutral - "You enjoy reading scientific articles and journals"
        'I5': 5,  # Strongly Agree - "You like to analyze data and find patterns"
        'I6': 3,  # Neutral - "You prefer theoretical discussions over practical applications"
        
        # Artistic questions (A1-A6)
        'A1': 2,  # Disagree - "You enjoy creating art, music, or writing"
        'A2': 3,  # Neutral - "You like to express yourself through creative means"
        'A3': 2,  # Disagree - "You prefer flexible, unstructured work environments"
        'A4': 3,  # Neutral - "You enjoy designing and creating new things"
        'A5': 2,  # Disagree - "You like to work with colors, shapes, and aesthetics"
        'A6': 3,  # Neutral - "You prefer original, unique approaches over conventional methods"
        
        # Social questions (S1-S6)
        'S1': 3,  # Neutral - "You enjoy helping others and making a difference in their lives"
        'S2': 4,  # Agree - "You like working in teams and collaborating with others"
        'S3': 3,  # Neutral - "You enjoy teaching and explaining things to others"
        'S4': 3,  # Neutral - "You prefer working with people rather than things"
        'S5': 3,  # Neutral - "You like to listen to others and understand their problems"
        'S6': 3,  # Neutral - "You enjoy organizing events and bringing people together"
        
        # Enterprising questions (E1-E6)
        'E1': 4,  # Agree - "You enjoy leading and managing others"
        'E2': 3,  # Neutral - "You like to persuade and influence others"
        'E3': 3,  # Neutral - "You enjoy taking risks and trying new ventures"
        'E4': 3,  # Neutral - "You prefer competitive environments"
        'E5': 4,  # Agree - "You like to make decisions and take responsibility"
        'E6': 3,  # Neutral - "You enjoy networking and building professional relationships"
        
        # Conventional questions (C1-C6)
        'C1': 4,  # Agree - "You enjoy organizing and maintaining systems"
        'C2': 5,  # Strongly Agree - "You like working with numbers and data"
        'C3': 4,  # Agree - "You prefer structured, predictable work environments"
        'C4': 4,  # Agree - "You enjoy following established procedures and protocols"
        'C5': 5,  # Strongly Agree - "You like to work with computers and technology systems"
        'C6': 4   # Agree - "You prefer clear instructions and well-defined tasks"
    }
    
    print("Sample Student Profile:")
    print("- Name: Rajesh Kumar")
    print("- Age: 17")
    print("- Grade: 12th")
    print("- Interests: Technology, Mathematics, Problem Solving")
    print("- Location: Bangalore")
    print()
    
    # Analyze responses
    print("Analyzing RIASEC Assessment Responses...")
    analysis = analyzer.analyze_responses(sample_responses)
    
    # Display results
    print("\n" + "=" * 60)
    print("PERSONALITY ASSESSMENT RESULTS")
    print("=" * 60)
    
    # RIASEC Scores
    print("\nRIASEC Dimension Scores:")
    scores = analysis['riasec_scores']
    for dimension, score in scores.items():
        print(f"  {dimension}: {score:.2f}/5.0")
    
    # Personality Profile
    profile = analysis['personality_profile']
    print(f"\nPrimary Personality Type: {profile.primary_type}")
    print(f"Secondary Personality Type: {profile.secondary_type}")
    print(f"Personality Description: {profile.personality_description}")
    
    print(f"\nStrengths:")
    for strength in profile.strengths:
        print(f"  • {strength}")
    
    print(f"\nWork Environment Preferences:")
    for preference in profile.work_environment_preferences:
        print(f"  • {preference}")
    
    print(f"\nCommunication Style: {profile.communication_style}")
    
    print(f"\nLearning Preferences:")
    for preference in profile.learning_preferences:
        print(f"  • {preference}")
    
    print(f"\nCareer Clusters:")
    for cluster in profile.career_clusters:
        print(f"  • {cluster}")
    
    # Indian Context Insights
    print(f"\nIndian Context Insights:")
    indian_context = profile.indian_context_insights
    print(f"  Primary Type Context: {indian_context['primary_type_context']}")
    print(f"  Secondary Type Context: {indian_context['secondary_type_context']}")
    
    print(f"\nRecommended Entrance Exams:")
    for exam in indian_context['entrance_exam_recommendations']:
        print(f"  • {exam}")
    
    print(f"\nRegional Opportunities:")
    for location in indian_context['regional_opportunities']:
        print(f"  • {location}")
    
    family_expectations = indian_context['family_expectations']
    print(f"\nFamily Expectations Alignment: {family_expectations['alignment']}")
    print(f"Explanation: {family_expectations['explanation']}")
    
    # Career Matches
    print("\n" + "=" * 60)
    print("TOP CAREER RECOMMENDATIONS")
    print("=" * 60)
    
    for i, match in enumerate(analysis['career_matches'][:5], 1):
        print(f"\n{i}. {match.career_name}")
        print(f"   Match Percentage: {match.match_percentage:.1f}%")
        print(f"   Explanation: {match.explanation}")
        print(f"   Description: {match.indian_relevance.get('description', 'N/A')}")
        print(f"   Salary Range: {match.indian_relevance.get('salary_range', 'N/A')}")
        print(f"   Growth Prospects: {match.indian_relevance.get('growth_prospects', 'N/A')}")
        print(f"   Job Market: {match.indian_relevance.get('job_market', 'N/A')}")
        print(f"   Entrance Exams: {', '.join(match.indian_relevance.get('entrance_exams', []))}")
        print(f"   Top Colleges: {', '.join(match.indian_relevance.get('top_colleges', []))}")
    
    # Visualization Data
    print("\n" + "=" * 60)
    print("VISUALIZATION DATA")
    print("=" * 60)
    
    viz_data = analysis['visualization_data']
    
    print("\nRadar Chart Data:")
    print(f"  Labels: {viz_data['radar_chart']['labels']}")
    print(f"  Data: {viz_data['radar_chart']['datasets'][0]['data']}")
    
    print("\nCareer Match Percentages:")
    career_data = viz_data['career_matches']
    for career, percentage in zip(career_data['careers'][:5], career_data['percentages'][:5]):
        print(f"  {career}: {percentage:.1f}%")
    
    print("\nTrait Explanations:")
    trait_explanations = viz_data['trait_explanations']
    for dimension, explanation in trait_explanations.items():
        print(f"  {dimension}: {explanation['level']} ({explanation['score']:.2f})")
        print(f"    {explanation['description']}")
        print(f"    Indian Context: {explanation['indian_context']}")
    
    # Assessment Summary
    print("\n" + "=" * 60)
    print("ASSESSMENT SUMMARY")
    print("=" * 60)
    
    summary = analysis['assessment_summary']
    print(f"Total Questions Answered: {summary['total_questions']}")
    print(f"Primary Type: {summary['primary_type']}")
    print(f"Secondary Type: {summary['secondary_type']}")
    print(f"Top Strengths: {', '.join(summary['top_strengths'])}")
    print(f"Career Clusters: {', '.join(summary['career_clusters'])}")
    print(f"Communication Style: {summary['communication_style']}")
    
    # Individual Dimension Scores
    print("\n" + "=" * 60)
    print("INDIVIDUAL DIMENSION SCORES")
    print("=" * 60)
    
    print("\nIndividual Dimension Scoring:")
    realistic_score = analyzer.score_realistic_dimension(sample_responses)
    investigative_score = analyzer.score_investigative_dimension(sample_responses)
    artistic_score = analyzer.score_artistic_dimension(sample_responses)
    social_score = analyzer.score_social_dimension(sample_responses)
    enterprising_score = analyzer.score_enterprising_dimension(sample_responses)
    conventional_score = analyzer.score_conventional_dimension(sample_responses)
    
    print(f"  Realistic: {realistic_score:.2f}")
    print(f"  Investigative: {investigative_score:.2f}")
    print(f"  Artistic: {artistic_score:.2f}")
    print(f"  Social: {social_score:.2f}")
    print(f"  Enterprising: {enterprising_score:.2f}")
    print(f"  Conventional: {conventional_score:.2f}")
    
    # Assessment Questions
    print("\n" + "=" * 60)
    print("ASSESSMENT QUESTIONS")
    print("=" * 60)
    
    questions = analyzer.get_assessment_questions()
    print(f"\nTotal Questions: {len(questions)}")
    print("\nSample Questions:")
    
    # Show a few sample questions from each dimension
    dimensions_shown = set()
    for question in questions:
        if question['dimension'] not in dimensions_shown and len(dimensions_shown) < 3:
            dimensions_shown.add(question['dimension'])
            print(f"\n{question['dimension']} Dimension:")
            print(f"  {question['id']}: {question['question']}")
            print(f"  Indian Context: {question['indian_context']}")
    
    # Career Database
    print("\n" + "=" * 60)
    print("CAREER DATABASE")
    print("=" * 60)
    
    careers = analyzer.get_career_database()
    print(f"\nTotal Careers in Database: {len(careers)}")
    print("\nSample Careers:")
    
    for i, career in enumerate(careers[:3]):
        print(f"\n{i+1}. {career['career']}")
        print(f"   RIASEC Codes: {', '.join(career['riasec_codes'])}")
        print(f"   Description: {career['description']}")
        print(f"   Salary Range: {career['indian_context']['salary_range']}")
        print(f"   Growth Prospects: {career['indian_context']['growth_prospects']}")
    
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)
    
    print("\nThis example demonstrates:")
    print("• Complete RIASEC personality assessment")
    print("• Career matching with Indian context")
    print("• Visualization data generation")
    print("• Individual dimension scoring")
    print("• Assessment question management")
    print("• Career database integration")
    
    print("\nTo use this analyzer in your application:")
    print("1. Initialize: analyzer = RIASECAnalyzer()")
    print("2. Get questions: questions = analyzer.get_assessment_questions()")
    print("3. Analyze responses: analysis = analyzer.analyze_responses(responses)")
    print("4. Access results: scores, profile, career_matches, visualization_data")

if __name__ == "__main__":
    main()
