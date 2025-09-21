#!/usr/bin/env python3
"""
Example usage of Gemini Client for CareerConnect AI
Demonstrates how to use the client for various career counseling tasks.
"""

import asyncio
import json
import os
from core.gemini_client import GeminiClient, create_gemini_client

async def main():
    """Main example function."""
    
    # Check if API key is available
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        print("Please set GEMINI_API_KEY environment variable")
        print("Example: export GEMINI_API_KEY='your-api-key-here'")
        return
    
    # Initialize client
    print("Initializing Gemini Client...")
    client = create_gemini_client(api_key=api_key)
    
    try:
        # Test 1: Basic response generation
        print("\n=== Test 1: Basic Response Generation ===")
        response = await client.generate_response(
            prompt="Hello! I'm a career counselor AI. How can I help you today?",
            temperature=0.7,
            max_tokens=200
        )
        print(f"Response: {response.content}")
        print(f"Tokens used: {response.usage.get('totalTokenCount', 'N/A')}")
        print(f"Correlation ID: {response.correlation_id}")
        
        # Test 2: Student Profile Analysis
        print("\n=== Test 2: Student Profile Analysis ===")
        student_profile = {
            "name": "Arjun Sharma",
            "age": 17,
            "grade": "12th",
            "interests": ["Technology", "Mathematics", "Problem Solving"],
            "skills": ["Python", "Basic Web Development", "Logical Thinking"],
            "learning_style": "Visual",
            "location": "Bangalore",
            "career_goals": ["Software Engineer", "Data Scientist"],
            "family_background": "Middle class, parents are teachers",
            "academic_performance": "Above average",
            "extracurricular": ["Debate club", "Math olympiad"]
        }
        
        analysis_response = await client.analyze_student_profile(student_profile)
        print(f"Profile Analysis:\n{analysis_response.content}")
        
        # Test 3: RIASEC Career Recommendations
        print("\n=== Test 3: RIASEC Career Recommendations ===")
        riasec_scores = {
            "Realistic": 75,
            "Investigative": 90,
            "Artistic": 60,
            "Social": 70,
            "Enterprising": 80,
            "Conventional": 65
        }
        interests = ["Technology", "Mathematics", "Problem Solving", "Innovation"]
        
        career_response = await client.generate_career_recommendations(riasec_scores, interests)
        print(f"Career Recommendations:\n{career_response.content}")
        
        # Test 4: Learning Path Generation
        print("\n=== Test 4: Learning Path Generation ===")
        learning_path_response = await client.create_learning_path(
            career_choice="Software Engineer",
            current_skills=["Python", "Basic HTML", "Logical Thinking"],
            education_level="12th",
            learning_style="Visual",
            time_available="12 months",
            budget="moderate"
        )
        print(f"Learning Path:\n{learning_path_response.content}")
        
        # Test 5: Chat Conversation
        print("\n=== Test 5: Chat Conversation ===")
        conversation_history = [
            {"role": "user", "content": "Hi, I'm confused about my career choice"},
            {"role": "assistant", "content": "Hello! I'd be happy to help you with career guidance. Can you tell me about your interests and current academic situation?"}
        ]
        
        chat_response = await client.chat_response(
            message="I'm interested in technology but my parents want me to become a doctor. What should I do?",
            conversation_history=conversation_history,
            student_context=student_profile
        )
        print(f"Chat Response:\n{chat_response.content}")
        
        # Test 6: Demonstrate caching (if Redis is available)
        print("\n=== Test 6: Caching Demonstration ===")
        print("Making the same request twice to demonstrate caching...")
        
        start_time = asyncio.get_event_loop().time()
        response1 = await client.generate_response("What is artificial intelligence?")
        time1 = asyncio.get_event_loop().time() - start_time
        
        start_time = asyncio.get_event_loop().time()
        response2 = await client.generate_response("What is artificial intelligence?")
        time2 = asyncio.get_event_loop().time() - start_time
        
        print(f"First request time: {time1:.2f} seconds")
        print(f"Second request time: {time2:.2f} seconds")
        print(f"Response 1 cached: {response1.cached}")
        print(f"Response 2 cached: {response2.cached}")
        
        # Test 7: Error Handling
        print("\n=== Test 7: Error Handling ===")
        try:
            # This should work fine
            await client.generate_response("Test prompt", max_tokens=10)
            print("✓ Normal request successful")
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
        
        # Test 8: Invalid RIASEC scores
        try:
            invalid_scores = {"Invalid": 100}
            await client.generate_career_recommendations(invalid_scores, ["test"])
            print("✗ Should have raised ValueError")
        except ValueError as e:
            print(f"✓ Correctly caught invalid RIASEC scores: {e}")
        
        print("\n=== All Tests Completed Successfully! ===")
        
    except Exception as e:
        print(f"Error during testing: {e}")
        print("Make sure your GEMINI_API_KEY is valid and you have internet connectivity")

def demonstrate_synchronous_usage():
    """Demonstrate how to use the client in synchronous code."""
    print("\n=== Synchronous Usage Example ===")
    
    async def async_wrapper():
        client = create_gemini_client()
        response = await client.generate_response("Hello from sync code!")
        return response.content
    
    # Run async function in sync context
    result = asyncio.run(async_wrapper())
    print(f"Synchronous result: {result}")

if __name__ == "__main__":
    print("CareerConnect AI - Gemini Client Example")
    print("======================================")
    
    # Run async main function
    asyncio.run(main())
    
    # Demonstrate synchronous usage
    demonstrate_synchronous_usage()
    
    print("\nExample completed!")
    print("\nTo run this example:")
    print("1. Set your GEMINI_API_KEY environment variable")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Run: python example_gemini_usage.py")
