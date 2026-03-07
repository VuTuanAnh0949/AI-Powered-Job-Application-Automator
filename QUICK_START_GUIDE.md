# 🚀 Quick Start Guide - AutoApply AI

## Chạy Hệ Thống Trong 5 Phút

### Bước 1: Start Backend (30 giây)

```powershell
# Mở terminal và chạy:
conda activate ai-powered-job-application-automator
cd apps\backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

✅ Thấy "Application startup complete" = Success!

### Bước 2: Test Backend (1 phút)

Mở browser: **http://localhost:8000/api/docs**

Test endpoint **GET /health** → Nhấn "Try it out" → "Execute"

**Expected:** `{"status": "healthy", "version": "2.0.0"}`

### Bước 3: Tạo Profile (2 phút)

Trong Swagger UI, tìm **POST /api/v1/profile**:

1. Click "Try it out"
2. Paste JSON này:

```json
{
  "email": "me@example.com",
  "full_name": "Your Name",
  "phone": "+84912345678",
  "location": "Ho Chi Minh City",
  "summary": "Software Engineer với 3 năm kinh nghiệm Python, React, và Cloud",
  "skills": ["Python", "JavaScript", "React", "FastAPI", "Docker"],
  "target_roles": ["Software Engineer", "Full Stack Developer"],
  "target_locations": ["Ho Chi Minh City", "Remote"],
  "years_of_experience": 3
}
```

3. Click "Execute"
4. Lưu lại `id` trong response

### Bước 4: Thêm Education (1 phút)

Tìm **POST /api/v1/profile/education**:

```json
{
  "user_email": "me@example.com",
  "institution": "University of Technology",
  "degree": "Bachelor of Computer Science",
  "field_of_study": "Computer Science",
  "start_date": "2018-09-01",
  "end_date": "2022-06-30",
  "gpa": "3.6",
  "achievements": ["Dean's List 2020-2022"]
}
```

### Bước 5: Tạo Application (30 giây)

Tìm **POST /api/v1/applications**:

```json
{
  "user_email": "me@example.com",
  "job_id": "demo-job-001",
  "company": "Tech Company XYZ",
  "position": "Senior Python Developer",
  "status": "submitted",
  "notes": "Applied via LinkedIn on 2024-03-07"
}
```

### Bước 6: Xem Applications (30 giây)

**GET /api/v1/applications**

Params:
- `user_email`: me@example.com

**Expected:** Danh sách applications với stats!

---

## 🎉 Done! Bạn Đã Có 1 Application Được Track

### Tính Năng Có Thể Test Ngay:

#### 📊 View Statistics
```
GET /api/v1/applications/stats/me@example.com
```

Returns:
- Total applications
- Status breakdown (submitted, interview, offered, etc.)
- Interview rate
- Offer rate

#### 🔍 Search Jobs (Mock)
```
POST /api/v1/jobs/search
{
  "keywords": "Python Developer",
  "location": "Ho Chi Minh"
}
```

#### 📄 View Documents  
```
GET /api/v1/documents?user_email=me@example.com
```

#### 👤 Get Full Profile
```
GET /api/v1/profile/me@example.com
```

---

## 🌐 Truy Cập Frontend (Optional)

```powershell
cd apps\frontend
npm run dev
```

Mở: **http://localhost:3000**

---

## 🗄️ Xem Data Trong MongoDB

```bash
docker exec -it mongodb mongosh
use autoapply_ai
db.users.find().pretty()
db.applications.find().pretty()
```

---

## ✨ Next: Thử AI Features

### Generate Resume (Requires API Key)

1. Get Gemini API key: https://ai.google.dev/ (Free)
2. Add to `apps/backend/.env`:
   ```
   GEMINI_API_KEY="your_key_here"
   ```
3. Restart backend
4. Test endpoint:

```json
POST /api/v1/documents/resume/generate
{
  "user_email": "me@example.com",
  "job_title": "Python Developer",
  "company_name": "Google",
  "job_description": "We're looking for...",
  "template": "professional"
}
```

---

## 🐛 Troubleshooting

### Backend không start?
```powershell
# Check conda environment
conda env list

# Reinstall dependencies
pip install -r apps/backend/requirements.txt
```

### MongoDB không connect?
```powershell
# Check Docker containers
docker ps

# Start if not running
docker start mongodb
docker start qdrant
```

### API key error?
- Get free key từ https://ai.google.dev/
- Check file `.env` trong `apps/backend/`
- Restart backend sau khi thêm key

---

## 📞 Help

- **API Documentation:** http://localhost:8000/api/docs
- **System Status:** `SYSTEM_STATUS.md`
- **Full Test:** `python test_full_system.py`

---

**Estimated Time: 5-10 minutes**  
**Difficulty: Easy** ⭐

Happy job hunting! 🎯
