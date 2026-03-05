# ✅ SETUP HOÀN TẤT - HƯỚNG DẪN CHẠY

## 🎉 Tất cả lỗi đã được fix!

### ✅ Đã hoàn thành:

- ✅ Backend dependencies installed
- ✅ Frontend dependencies installed
- ✅ Environment files created (.env)
- ✅ Data directories created
- ✅ Logging configuration fixed
- ✅ Email validator installed

---

## 🚀 Cách Chạy Project

### Option 1: Chạy Từng Service (Recommended cho Dev)

#### Terminal 1 - Backend:

```powershell
cd apps\backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

✅ Backend: http://localhost:8000
📚 API Docs: http://localhost:8000/api/docs

#### Terminal 2 - Frontend:

```powershell
cd apps\frontend
npm run dev
```

✅ Frontend: http://localhost:3000

---

### Option 2: Makefile Commands (Quick)

```powershell
# Backend only
make dev-backend

# Frontend only
make dev-frontend

# Both with Docker
make dev
```

---

## 🔧 Cấu Hình API Keys (Quan Trọng!)

Edit file `apps\backend\.env` với API keys của bạn:

```env
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Optional
OPENAI_API_KEY=
GROQ_API_KEY=

# LinkedIn (for job search)
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password
```

---

## 📊 Kiểm Tra Status

### Backend Health Check:

```powershell
curl http://localhost:8000/health
```

Expected response:

```json
{
  "status": "healthy",
  "version": "2.0.0",
  "environment": "development"
}
```

### Frontend:

Mở browser: http://localhost:3000

---

## 🎯 Các Trang Có Sẵn

Frontend includes:

- 🏠 Dashboard - `/`
- 🔍 Job Search - `/jobs`
- 📝 Applications - `/applications`
- 📄 Documents - `/documents`
- 👤 Profile - `/profile`

---

## 📚 API Endpoints

Backend provides:

### Jobs

- `POST /api/v1/jobs/search` - Search jobs
- `GET /api/v1/jobs/{id}` - Get job details
- `POST /api/v1/jobs/{id}/analyze` - Analyze match

### Applications

- `GET /api/v1/applications` - List applications
- `POST /api/v1/applications` - Create application
- `PATCH /api/v1/applications/{id}/status` - Update status

### Documents

- `POST /api/v1/documents/resume/generate` - Generate resume
- `POST /api/v1/documents/cover-letter/generate` - Generate cover letter

### Profile

- `GET /api/v1/profile` - Get profile
- `POST /api/v1/profile` - Update profile

Full docs: http://localhost:8000/api/docs

---

## 🐛 Nếu Gặp Lỗi

### Port già bị chiếm:

```powershell
# Change port in command
uvicorn app.main:app --reload --port 8001

# Or kill process
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Module not found:

```powershell
cd apps\backend
pip install -r requirements.txt
```

### Frontend errors:

```powershell
cd apps\frontend
rm -rf node_modules package-lock.json
npm install
```

---

## 📖 Documentation

- [HUONG_DAN_V2.md](../HUONG_DAN_V2.md) - Full Vietnamese guide
- [MONOREPO_STRUCTURE.md](../MONOREPO_STRUCTURE.md) - Architecture
- [MIGRATION_GUIDE.md](../MIGRATION_GUIDE.md) - Migration plan

---

## 🎊 Happy Coding!

Project is ready to use. Start developing! 🚀

**Next Steps:**

1. Edit `.env` with your API keys
2. Start backend: `uvicorn app.main:app --reload`
3. Start frontend: `npm run dev`
4. Open http://localhost:3000
5. Start job hunting! 💼
