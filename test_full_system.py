#!/usr/bin/env python3
"""
AutoApply AI - Full System Test Script
Tự động test tất cả chức năng của hệ thống
"""

import requests
import json
from datetime import datetime
import time

BASE_URL = "http://localhost:8000/api/v1"
TEST_EMAIL = "test@autoapply.ai"

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_api(method, endpoint, data=None, description=""):
    """Helper function to test API endpoints"""
    url = f"{BASE_URL}{endpoint}"
    print(f"\n🔹 {description}")
    print(f"   {method} {endpoint}")
    
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
            print(f"   Request: {json.dumps(data, indent=2)[:200]}...")
        elif method == "PATCH":
            response = requests.patch(url, json=data)
        
        if response.status_code in [200, 201]:
            print(f"   ✅ SUCCESS - Status: {response.status_code}")
            result = response.json()
            print(f"   Response: {json.dumps(result, indent=2)[:300]}...")
            return result
        else:
            print(f"   ❌ FAILED - Status: {response.status_code}")
            print(f"   Error: {response.text[:200]}")
            return None
    except Exception as e:
        print(f"   ❌ ERROR: {str(e)}")
        return None

def main():
    print("\n" + "🚀"*30)
    print("AutoApply AI - Full System Test")
    print("🚀"*30)
    
    # Test 1: Health Check
    print_section("1️⃣  HEALTH CHECK")
    health_response = requests.get("http://localhost:8000/health")
    if health_response.status_code == 200:
        print(f"   ✅ Backend is healthy: {health_response.json()}")
    else:
        print(f"   ❌ Backend not healthy")
        return
    
    # Test 2: Create User Profile
    print_section("2️⃣  CREATE USER PROFILE")
    profile_data = {
        "email": TEST_EMAIL,
        "full_name": "Nguyễn Văn Test",
        "phone": "+84912345678",
        "location": "Ho Chi Minh City, Vietnam",
        "linkedin_url": "https://linkedin.com/in/test",
        "github_url": "https://github.com/test",
        "summary": "Experienced Software Engineer with 5+ years in full-stack development. Specialized in Python, FastAPI, React, and cloud technologies. Strong problem-solving skills and team leadership experience.",
        "target_roles": ["Software Engineer", "Full Stack Developer", "Backend Developer"],
        "target_locations": ["Ho Chi Minh City", "Hanoi", "Remote"],
        "years_of_experience": 5
    }
    profile = test_api("POST", "/profile", profile_data, "Tạo profile người dùng mới")
    
    if not profile:
        print("\n❌ Không thể tạo profile. Dừng test.")
        return
    
    time.sleep(1)
    
    # Test 3: Add Experience
    print_section("3️⃣  ADD WORK EXPERIENCE")
    experience_data = {
        "user_email": TEST_EMAIL,
        "company": "Tech Innovations Vietnam",
        "position": "Senior Software Engineer",
        "start_date": "2020-01-01",
        "end_date": "2024-12-31",
        "is_current": False,
        "description": "Led development of microservices architecture using Python FastAPI and React. Managed a team of 5 developers. Improved system performance by 40% through optimization and caching strategies.",
        "achievements": [
            "Reduced API response time by 60% through database query optimization",
            "Implemented CI/CD pipeline reducing deployment time from 2 hours to 15 minutes",
            "Mentored 3 junior developers to mid-level positions",
            "Architected and deployed 5 microservices handling 1M+ requests per day"
        ],
        "technologies": ["Python", "FastAPI", "React", "Docker", "Kubernetes", "AWS", "PostgreSQL", "Redis", "RabbitMQ"]
    }
    test_api("POST", "/profile/experience", experience_data, "Thêm kinh nghiệm làm việc")
    
    time.sleep(1)
    
    # Test 4: Add Education
    print_section("4️⃣  ADD EDUCATION")
    education_data = {
        "user_email": TEST_EMAIL,
        "institution": "University of Technology Ho Chi Minh City",
        "degree": "Bachelor of Computer Science",
        "field_of_study": "Computer Science",
        "start_date": "2015-09-01",
        "end_date": "2019-06-30",
        "gpa": "3.8",
        "achievements": [
            "Dean's List all 8 semesters",
            "First prize in National Hackathon 2018",
            "Published research paper on Machine Learning"
        ]
    }
    test_api("POST", "/profile/education", education_data, "Thêm học vấn")
    
    time.sleep(1)
    
    # Test 5: Get Profile
    print_section("5️⃣  GET USER PROFILE")
    test_api("GET", f"/profile/{TEST_EMAIL}", description="Lấy thông tin profile đầy đủ")
    
    time.sleep(1)
    
    # Test 6: Search Jobs
    print_section("6️⃣  SEARCH JOBS")
    search_data = {
        "keywords": "Python Developer",
        "location": "Ho Chi Minh",
        "job_type": "full-time",
        "experience_level": "mid-level",
        "remote": False,
        "platforms": ["linkedin", "indeed"]
    }
    jobs = test_api("POST", "/jobs/search", search_data, "Tìm kiếm công việc")
    
    # Create a sample job for testing
    sample_job = {
        "id": "test-job-001",
        "title": "Senior Python Developer",
        "company": "Amazing Tech Company",
        "location": "Ho Chi Minh City",
        "description": "We are looking for a Senior Python Developer with experience in FastAPI, microservices, Docker, and cloud technologies. You will lead the backend team and architect scalable solutions.",
        "requirements": [
            "5+ years of Python development experience",
            "Strong experience with FastAPI or Django",
            "Experience with Docker and Kubernetes",
            "Cloud platform experience (AWS/GCP/Azure)",
            "Team leadership experience"
        ],
        "required_skills": ["Python", "FastAPI", "Docker", "AWS", "PostgreSQL", "Redis"],
        "salary_range": "$80,000 - $120,000",
        "job_type": "full-time",
        "remote": False
    }
    
    time.sleep(1)
    
    # Test 7: Generate Resume
    print_section("7️⃣  GENERATE AI-POWERED RESUME")
    resume_data = {
        "user_email": TEST_EMAIL,
        "job_title": sample_job["title"],
        "company_name": sample_job["company"],
        "job_description": sample_job["description"],
        "template": "professional",
        "highlight_skills": ["Python", "FastAPI", "Docker", "AWS"]
    }
    resume = test_api("POST", "/documents/resume/generate", resume_data, "Tạo resume tự động với AI")
    
    time.sleep(2)
    
    # Test 8: Generate Cover Letter
    print_section("8️⃣  GENERATE AI-POWERED COVER LETTER")
    cover_letter_data = {
        "user_email": TEST_EMAIL,
        "job_title": sample_job["title"],
        "company_name": sample_job["company"],
        "job_description": sample_job["description"],
        "tone": "professional"
    }
    cover_letter = test_api("POST", "/documents/cover-letter/generate", cover_letter_data, "Tạo cover letter tự động với AI")
    
    time.sleep(2)
    
    # Test 9: Create Application
    print_section("9️⃣  CREATE JOB APPLICATION")
    application_data = {
        "user_email": TEST_EMAIL,
        "job_id": sample_job["id"],
        "company": sample_job["company"],
        "position": sample_job["title"],
        "status": "pending",
        "resume_id": resume.get("id") if resume else None,
        "cover_letter_id": cover_letter.get("id") if cover_letter else None,
        "notes": "Applied through AutoApply AI system"
    }
    application = test_api("POST", "/applications", application_data, "Tạo application tracking")
    
    time.sleep(1)
    
    # Test 10: Get All Applications
    print_section("🔟  GET ALL APPLICATIONS")
    test_api("GET", f"/applications?user_email={TEST_EMAIL}", description="Lấy danh sách tất cả applications")
    
    time.sleep(1)
    
    # Test 11: Get Application Statistics
    print_section("1️⃣1️⃣  APPLICATION STATISTICS")
    test_api("GET", f"/applications/stats/{TEST_EMAIL}", description="Thống kê applications")
    
    time.sleep(1)
    
    # Test 12: Get All Documents
    print_section("1️⃣2️⃣  GET ALL GENERATED DOCUMENTS")
    test_api("GET", f"/documents?user_email={TEST_EMAIL}", description="Lấy tất cả documents đã tạo")
    
    # Summary
    print_section("✅ TEST COMPLETED")
    print("""
    🎉 Tất cả các test đã hoàn thành!
    
    📊 Những gì đã test:
    ✓ Backend Health Check
    ✓ User Profile Management (Create, Get)
    ✓ Work Experience Management
    ✓ Education Management  
    ✓ Job Search
    ✓ AI Resume Generation
    ✓ AI Cover Letter Generation
    ✓ Application Tracking
    ✓ Statistics & Analytics
    
    🌐 Truy cập:
    - Backend API: http://localhost:8000
    - API Docs: http://localhost:8000/docs
    - Frontend UI: http://localhost:3000
    
    📝 Kiểm tra database:
    - MongoDB: docker exec -it mongodb mongosh
    - Qdrant: http://localhost:6333/dashboard
    """)

if __name__ == "__main__":
    print("\n⏳ Starting test in 2 seconds...")
    print("   Make sure backend is running at http://localhost:8000")
    time.sleep(2)
    main()
