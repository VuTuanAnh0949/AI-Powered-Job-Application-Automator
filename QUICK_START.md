# 🚀 Quick Start Guide

## Cách 1: Dùng Batch Files (Khuyên dùng cho Windows)

### Start Backend + Frontend cùng lúc:

```bash
start-all.bat
```

### Hoặc start riêng từng service:

**Terminal 1 - Backend:**

```bash
start-backend.bat
```

**Terminal 2 - Frontend:**

```bash
start-frontend.bat
```

---

## Cách 2: Manual (Nếu batch files không hoạt động)

### Terminal 1 - Backend:

```bash
# 1. Activate conda environment
conda activate ai-powered-job-application-automator

# 2. Navigate to backend
cd apps\backend

# 3. Start server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Terminal 2 - Frontend:

```bash
# 1. Navigate to frontend
cd apps\frontend

# 2. Start dev server
npm run dev
```

---

## 🌐 URLs sau khi khởi động

✅ **Backend API**: http://localhost:8000  
✅ **API Documentation**: http://localhost:8000/api/docs  
✅ **Frontend UI**: http://localhost:5173

---

## ⚙️ Cấu hình (Lần đầu)

### 1. Tạo file `.env` cho Backend:

```bash
cd apps\backend
copy .env.example .env
```

### 2. Edit `.env` và điền API keys:

```env
# AI Provider
GEMINI_API_KEY=your_gemini_api_key_here

# LinkedIn (optional)
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password
```

### 3. Khởi động lại backend để load env variables

---

## 🛠️ Troubleshooting

### Lỗi: "conda: command not found"

👉 Cài đặt Anaconda hoặc Miniconda: https://docs.conda.io/en/latest/miniconda.html

### Lỗi: "Environment does not exist"

👉 Tạo environment:

```bash
conda create -n ai-powered-job-application-automator python=3.10
conda activate ai-powered-job-application-automator
cd apps\backend
pip install -r requirements.txt
```

### Lỗi: "Port 8000 already in use"

👉 Kill process đang dùng port:

```bash
# PowerShell
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process

# Hoặc đổi port trong command:
python -m uvicorn app.main:app --reload --port 8001
```

### Lỗi: "npm: command not found"

👉 Cài đặt Node.js: https://nodejs.org/

### Frontend không kết nối được Backend

👉 Kiểm tra trong `apps/frontend/vite.config.ts`:

```ts
server: {
  proxy: {
    '/api': 'http://localhost:8000'  // ✅ Đúng port backend
  }
}
```

---

## 📝 Development Commands

### Backend:

```bash
# Run tests
pytest

# Format code
black app/

# Type check
mypy app/

# Database migrations
alembic upgrade head
```

### Frontend:

```bash
# Lint
npm run lint

# Type check
npm run type-check

# Build for production
npm run build

# Preview production build
npm run preview
```

---

## 🐳 Docker (Production)

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## 📚 Thêm Documentation

- [Full Setup Guide](HUONG_DAN_V2.md)
- [Architecture Overview](MONOREPO_STRUCTURE.md)
- [Migration Guide](MIGRATION_GUIDE.md)
- [API Documentation](http://localhost:8000/api/docs) (sau khi start backend)

---

**Hỗ trợ**: Mở issue trên GitHub nếu gặp vấn đề
