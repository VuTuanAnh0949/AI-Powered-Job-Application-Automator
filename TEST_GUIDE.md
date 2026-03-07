# Hướng Dẫn Test Hệ Thống AutoApply AI

## 1️⃣ Tạo User Profile

**API**: `POST /api/v1/profile`

Vào http://localhost:8000/docs, tìm endpoint **POST /api/v1/profile**, click "Try it out" và nhập:

```json
{
  "email": "test@example.com",
  "full_name": "Nguyen Van A",
  "phone": "+84912345678",
  "location": "Ho Chi Minh City, Vietnam",
  "linkedin_url": "https://linkedin.com/in/nguyenvana",
  "github_url": "https://github.com/nguyenvana",
  "portfolio_url": "https://portfolio.com",
  "summary": "Experienced Software Engineer with 5 years in full-stack development. Specialized in Python, React, and cloud technologies.",
  "target_roles": ["Software Engineer", "Full Stack Developer", "Backend Developer"],
  "target_locations": ["Ho Chi Minh City", "Remote"],
  "years_of_experience": 5
}
```

Click **Execute** → Lưu lại response.

---

## 2️⃣ Thêm Experience (Kinh nghiệm làm việc)

**API**: `POST /api/v1/profile/experience`

```json
{
  "user_email": "test@example.com",
  "company": "Tech Company ABC",
  "position": "Senior Software Engineer",
  "start_date": "2020-01-01",
  "end_date": "2024-12-31",
  "is_current": false,
  "description": "Led development of microservices architecture using Python FastAPI and React. Managed team of 5 developers. Improved system performance by 40%.",
  "achievements": [
    "Reduced API response time by 60%",
    "Implemented CI/CD pipeline reducing deployment time from 2 hours to 15 minutes",
    "Mentored 3 junior developers"
  ],
  "technologies": ["Python", "FastAPI", "React", "Docker", "AWS", "PostgreSQL"]
}
```

---

## 3️⃣ Thêm Education (Học vấn)

**API**: `POST /api/v1/profile/education`

```json
{
  "user_email": "test@example.com",
  "institution": "University of Technology",
  "degree": "Bachelor of Computer Science",
  "field_of_study": "Computer Science",
  "start_date": "2015-09-01",
  "end_date": "2019-06-30",
  "gpa": "3.8",
  "achievements": [
    "Dean's List all semesters",
    "First prize in Hackathon 2018"
  ]
}
```

---

## 4️⃣ Search Jobs (Tìm việc)

**API**: `POST /api/v1/jobs/search`

```json
{
  "keywords": "Python Developer",
  "location": "Ho Chi Minh",
  "job_type": "full-time",
  "experience_level": "mid-level",
  "remote": false,
  "platforms": ["linkedin"]
}
```

---

## 5️⃣ Generate Resume (Tạo CV tự động)

**API**: `POST /api/v1/documents/resume/generate`

```json
{
  "user_email": "test@example.com",
  "job_id": "job-123",
  "template": "professional",
  "highlight_skills": ["Python", "FastAPI", "React", "Docker"]
}
```

---

## 6️⃣ Generate Cover Letter (Tạo thư xin việc)

**API**: `POST /api/v1/documents/cover-letter/generate`

```json
{
  "user_email": "test@example.com",
  "job_id": "job-123",
  "company_name": "Google",
  "position": "Senior Python Developer",
  "tone": "professional"
}
```

---

## 7️⃣ Track Application (Theo dõi đơn ứng tuyển)

**API**: `POST /api/v1/applications`

```json
{
  "user_email": "test@example.com",
  "job_id": "job-123",
  "resume_id": "resume-456",
  "cover_letter_id": "cover-letter-789",
  "status": "submitted",
  "notes": "Applied via LinkedIn"
}
```

---

## 8️⃣ ATS Score Analysis (Phân tích điểm ATS)

**API**: `POST /api/v1/jobs/{job_id}/analyze`

```json
{
  "user_email": "test@example.com"
}
```

Kết quả sẽ cho biết:
- **Overall Score**: Điểm tổng (0-100)
- **Keyword Match**: Khớp từ khóa
- **Semantic Similarity**: Độ tương đồng ngữ nghĩa
- **Experience Match**: Khớp kinh nghiệm
- **Skills Match**: Khớp kỹ năng
- **Recommendations**: Gợi ý cải thiện

---

## 🎯 Test Full Flow

1. **Tạo profile** → `/api/v1/profile`
2. **Thêm experience** → `/api/v1/profile/experience`
3. **Thêm education** → `/api/v1/profile/education`
4. **Search jobs** → `/api/v1/jobs/search`
5. **Generate resume** cho job cụ thể → `/api/v1/documents/resume/generate`
6. **Generate cover letter** → `/api/v1/documents/cover-letter/generate`
7. **Submit application** → `/api/v1/applications`
8. **Track progress** → `GET /api/v1/applications`

---

## 🔍 Kiểm tra Database

### MongoDB
```bash
# Connect to MongoDB
docker exec -it mongodb mongosh

# Switch to database
use autoapply_ai

# View collections
show collections

# View user profiles
db.UserProfile.find().pretty()

# View applications
db.Application.find().pretty()
```

### Qdrant (Vector DB)
Open browser: http://localhost:6333/dashboard

---

## 🎨 Frontend Features

Mở http://localhost:3000 và test:

1. **Dashboard**: Xem thống kê applications
2. **Job Search**: Tìm kiếm việc làm với AI filtering
3. **Profile**: Quản lý thông tin cá nhân
4. **Applications**: Theo dõi các đơn đã nộp
5. **Documents**: Xem resume và cover letter đã tạo

---

## ❗ Lưu ý

- **Gemini API Key** đã được cấu hình trong `.env`
- **Job scrapers** hiện tại là stub (chưa scrape thật)
- Vector search hoạt động với embedding model `all-MiniLM-L6-v2`
- MongoDB và Qdrant đang chạy trong Docker

---

## 🚀 Quick Test Script

Save as `test_api.py`:

```python
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

# 1. Create profile
profile_data = {
    "email": "test@example.com",
    "full_name": "Test User",
    "summary": "Python Developer with 5 years experience",
    "target_roles": ["Python Developer"],
    "years_of_experience": 5
}

response = requests.post(f"{BASE_URL}/profile", json=profile_data)
print("Profile created:", response.json())

# 2. Generate resume
resume_data = {
    "user_email": "test@example.com",
    "template": "professional"
}

response = requests.post(f"{BASE_URL}/documents/resume/generate", json=resume_data)
print("Resume generated:", response.json())
```

Run: `python test_api.py`
