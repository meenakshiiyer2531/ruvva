"""
Simple API smoke test to verify key endpoints are reachable and return expected schema.
Run: python -m tests.api_smoke_test
"""
import os
import sys
import time
import json
import requests
from datetime import datetime

BASE_URL = os.environ.get("BASE_URL", "http://localhost:5000")
SESSION = requests.Session()

def print_result(name, ok, resp=None):
    status = "OK" if ok else "FAIL"
    print(f"[{status}] {name}")
    if resp is not None:
        try:
            payload = resp.json()
        except Exception:
            payload = resp.text
        print(f"    -> status={resp.status_code}")
        print(f"    -> body={json.dumps(payload, indent=2) if isinstance(payload, dict) else payload}")


def get_token(student_id=1):
    url = f"{BASE_URL}/api/v1/auth/dev-token"
    resp = SESSION.post(url, json={"student_id": student_id, "expires_in": 3600})
    ok = resp.status_code == 200 and resp.json().get("success")
    print_result("auth/dev-token", ok, resp)
    token = resp.json().get("data", {}).get("access_token") if ok else None
    if token:
        SESSION.headers.update({"Authorization": f"Bearer {token}"})
    return ok


def test_profile(student_id=1):
    # Create
    resp = SESSION.post(f"{BASE_URL}/api/v1/profile/create", json={
        "name": "Test User",
        "email": "test@example.com",
        "age": 22,
        "education_level": "bachelor",
        "skills": ["Python", "JavaScript"],
        "interests": ["Data Science"],
        "career_goals": ["Data Scientist"]
    })
    print_result("profile/create", resp.status_code in (200,201), resp)

    # Get
    resp = SESSION.get(f"{BASE_URL}/api/v1/profile/{student_id}")
    print_result("profile/{id}", resp.status_code == 200, resp)

    # Update
    resp = SESSION.put(f"{BASE_URL}/api/v1/profile/update", json={
        "skills": ["Python", "SQL", "Pandas"]
    })
    print_result("profile/update", resp.status_code == 200, resp)

    # Insights
    resp = SESSION.get(f"{BASE_URL}/api/v1/profile/{student_id}/insights")
    print_result("profile/{id}/insights", resp.status_code == 200, resp)

    # Analyze
    resp = SESSION.post(f"{BASE_URL}/api/v1/profile/analyze", json={"analysis_type": "comprehensive"})
    print_result("profile/analyze", resp.status_code == 200, resp)


def test_assessment(student_id=1):
    # RIASEC questions
    resp = SESSION.get(f"{BASE_URL}/api/v1/assessment/riasec/questions")
    print_result("assessment/riasec/questions", resp.status_code == 200, resp)

    # RIASEC submit (minimal mock)
    resp = SESSION.post(f"{BASE_URL}/api/v1/assessment/riasec/submit", json={
        "responses": {"q1": 4, "q2": 3, "q3": 5}
    })
    print_result("assessment/riasec/submit", resp.status_code in (200,201), resp)

    # RIASEC results
    resp = SESSION.get(f"{BASE_URL}/api/v1/assessment/riasec/results/{student_id}")
    print_result("assessment/riasec/results/{id}", resp.status_code == 200, resp)

    # Skills evaluate
    resp = SESSION.post(f"{BASE_URL}/api/v1/assessment/skills/evaluate", json={
        "assessment_type": "self_evaluation",
        "skills": {"Python": 5, "Communication": 4}
    })
    print_result("assessment/skills/evaluate", resp.status_code in (200,201), resp)

    # History
    resp = SESSION.get(f"{BASE_URL}/api/v1/assessment/history/{student_id}")
    print_result("assessment/history/{id}", resp.status_code == 200, resp)


def test_careers():
    # Discover
    resp = SESSION.post(f"{BASE_URL}/api/v1/careers/discover", json={"filters": {"category": "Technology"}, "limit": 5})
    print_result("careers/discover", resp.status_code == 200, resp)

    # Search
    resp = SESSION.get(f"{BASE_URL}/api/v1/careers/search", params={"q": "engineer", "limit": 5})
    print_result("careers/search", resp.status_code == 200, resp)

    # Details
    resp = SESSION.get(f"{BASE_URL}/api/v1/careers/1/details")
    print_result("careers/{id}/details", resp.status_code == 200, resp)

    # Similar
    resp = SESSION.get(f"{BASE_URL}/api/v1/careers/1/similar")
    print_result("careers/{id}/similar", resp.status_code == 200, resp)

    # Trending
    resp = SESSION.get(f"{BASE_URL}/api/v1/careers/trending")
    print_result("careers/trending", resp.status_code == 200, resp)

    # Compare
    resp = SESSION.post(f"{BASE_URL}/api/v1/careers/compare", json={"career_ids": [1,2]})
    print_result("careers/compare", resp.status_code == 200, resp)


def test_chat(student_id=1):
    # Create session
    resp = SESSION.post(f"{BASE_URL}/api/v1/chat/session", json={})
    print_result("chat/session", resp.status_code in (200,201), resp)
    session_id = resp.json().get("data", {}).get("session_id")

    # Send message
    resp = SESSION.post(f"{BASE_URL}/api/v1/chat/message", json={"session_id": session_id, "message": "Hello"})
    print_result("chat/message", resp.status_code == 200, resp)

    # Quick replies
    resp = SESSION.get(f"{BASE_URL}/api/v1/chat/quick-replies")
    print_result("chat/quick-replies", resp.status_code == 200, resp)

    # History by student
    resp = SESSION.get(f"{BASE_URL}/api/v1/chat/history/{student_id}")
    print_result("chat/history/{id}", resp.status_code == 200, resp)

    # End session
    resp = SESSION.post(f"{BASE_URL}/api/v1/chat/session/{session_id}/end", json={"feedback": {"rating": 5}})
    print_result("chat/session/{id}/end", resp.status_code == 200, resp)

    # Sentiment
    resp = SESSION.get(f"{BASE_URL}/api/v1/chat/session/{session_id}/sentiment")
    print_result("chat/session/{id}/sentiment", resp.status_code == 200, resp)

    # Summary
    resp = SESSION.get(f"{BASE_URL}/api/v1/chat/session/{session_id}/summary")
    print_result("chat/session/{id}/summary", resp.status_code == 200, resp)

    # Feedback
    resp = SESSION.post(f"{BASE_URL}/api/v1/chat/feedback", json={"session_id": session_id, "feedback_type": "helpful", "rating": 5})
    print_result("chat/feedback", resp.status_code in (200,201), resp)

    # Reset context
    resp = SESSION.post(f"{BASE_URL}/api/v1/chat/context/reset", json={})
    print_result("chat/context/reset", resp.status_code == 200, resp)


def test_learning(student_id=1):
    # Generate path
    resp = SESSION.post(f"{BASE_URL}/api/v1/learning/path/generate", json={"career_id": 1})
    print_result("learning/path/generate", resp.status_code == 200, resp)

    # Resources
    resp = SESSION.get(f"{BASE_URL}/api/v1/learning/resources/1")
    print_result("learning/resources/{id}", resp.status_code == 200, resp)

    # Progress update
    resp = SESSION.post(f"{BASE_URL}/api/v1/learning/progress/update", json={"learning_path_id": 1001, "progress_data": {"completed": 1}})
    print_result("learning/progress/update", resp.status_code == 200, resp)

    # Progress get
    resp = SESSION.get(f"{BASE_URL}/api/v1/learning/progress/{student_id}")
    print_result("learning/progress/{id}", resp.status_code == 200, resp)

    # Milestones
    resp = SESSION.get(f"{BASE_URL}/api/v1/learning/milestones")
    print_result("learning/milestones", resp.status_code == 200, resp)

    # Recommendations
    resp = SESSION.get(f"{BASE_URL}/api/v1/learning/recommendations")
    print_result("learning/recommendations", resp.status_code == 200, resp)


def main():
    print(f"Starting API smoke tests against {BASE_URL} at {datetime.utcnow().isoformat()}Z")
    if not get_token(student_id=int(os.environ.get("STUDENT_ID", 1))):
        print("Failed to acquire dev token; aborting.")
        sys.exit(1)

    student_id = int(os.environ.get("STUDENT_ID", 1))
    test_profile(student_id)
    test_assessment(student_id)
    test_careers()
    test_chat(student_id)
    test_learning(student_id)
    print("Done.")

if __name__ == "__main__":
    main()
