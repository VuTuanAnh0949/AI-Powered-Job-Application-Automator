# ==============================================
# Quick Database Setup Guide
# ==============================================

## Option 1: Sử dụng script tự động (RECOMMENDED) ✅

```bash
# Chạy script setup
setup-databases.bat
```

Script sẽ tự động:
- ✅ Check Docker có cài chưa
- ✅ Tạo và start MongoDB container
- ✅ Tạo và start Qdrant container  
- ✅ Show status của databases

---

## Option 2: Cài đặt thủ công 🛠️

### Bước 1: Cài Docker Desktop (nếu chưa có)

**Download:** https://www.docker.com/products/docker-desktop

**Kiểm tra:**
```bash
docker --version
# Output: Docker version 24.x.x
```

### Bước 2: Start MongoDB

```bash
# Tạo và chạy MongoDB container
docker run -d -p 27017:27017 --name mongodb mongo:latest

# Kiểm tra đang chạy
docker ps | findstr mongodb
```

**Test MongoDB:**
```bash
# Mở MongoDB shell
docker exec -it mongodb mongosh

# Trong mongosh:
show dbs
use autoapply_ai
db.test.insertOne({message: "Hello MongoDB"})
db.test.find()
exit
```

### Bước 3: Start Qdrant Vector DB

```bash
# Tạo và chạy Qdrant container
docker run -d -p 6333:6333 -p 6334:6334 --name qdrant qdrant/qdrant:latest

# Kiểm tra đang chạy
docker ps | findstr qdrant
```

**Test Qdrant:**
```bash
# Test health endpoint
curl http://localhost:6333/health

# Output: {"title":"qdrant - vector search engine","version":"1.x.x"}
```

### Bước 4: Cấu hình .env

```bash
cd apps\backend
copy .env.example .env
```

**Mở file `.env` và đảm bảo có:**
```env
# MongoDB
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=autoapply_ai

# Qdrant Vector DB
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=
QDRANT_COLLECTION_NAME=job_embeddings

# AI Provider (chọn 1 trong 3)
GEMINI_API_KEY=your_gemini_key_here      # https://ai.google.dev/
OPENAI_API_KEY=your_openai_key_here      # https://platform.openai.com/
GROQ_API_KEY=your_groq_key_here          # https://console.groq.com/
DEFAULT_LLM_PROVIDER=gemini
```

### Bước 5: Chạy Backend

```bash
# Test backend imports
python -c "from app.db import mongodb, vector_db; print('OK')"

# Nếu OK, chạy server
start-backend.bat
```

---

## Option 3: Không dùng Docker (Local Installation) 🖥️

### MongoDB (Local)

**Windows:**
1. Download MongoDB Community: https://www.mongodb.com/try/download/community
2. Cài đặt với MongoDB Compass
3. Start MongoDB service
4. URL: `mongodb://localhost:27017`

### Qdrant (Local)

```bash
# Cài qua pip
pip install qdrant-client[fastembed]

# Hoặc chạy binary
# Download từ: https://github.com/qdrant/qdrant/releases
```

---

## Các lệnh Docker hữu ích 🔧

### Quản lý containers

```bash
# Xem containers đang chạy
docker ps

# Xem tất cả containers (kể cả stopped)
docker ps -a

# Start databases
docker start mongodb qdrant

# Stop databases
docker stop mongodb qdrant

# Restart databases
docker restart mongodb qdrant

# Remove containers (cẩn thận: mất data!)
docker rm -f mongodb qdrant
```

### Xem logs

```bash
# MongoDB logs
docker logs mongodb

# Qdrant logs
docker logs qdrant

# Follow logs (real-time)
docker logs -f mongodb
```

### Backup & Restore

```bash
# Backup MongoDB
docker exec mongodb mongodump --out=/tmp/backup
docker cp mongodb:/tmp/backup ./mongodb-backup

# Restore MongoDB
docker cp ./mongodb-backup mongodb:/tmp/backup
docker exec mongodb mongorestore /tmp/backup
```

---

## Troubleshooting 🐛

### MongoDB không start được

```bash
# Check if port 27017 is used
netstat -ano | findstr :27017

# If port is used, kill process or use different port
docker run -d -p 27018:27017 --name mongodb mongo:latest

# Update .env:
# MONGODB_URL=mongodb://localhost:27018
```

### Qdrant không start được

```bash
# Check port 6333
netstat -ano | findstr :6333

# Use different port
docker run -d -p 6334:6333 --name qdrant qdrant/qdrant:latest

# Update .env:
# QDRANT_URL=http://localhost:6334
```

### Backend không connect được

```bash
# Test MongoDB connection
python -c "from pymongo import MongoClient; print(MongoClient('mongodb://localhost:27017').server_info())"

# Test Qdrant connection
curl http://localhost:6333/health
```

---

## Verify Setup ✅

Sau khi setup xong, test bằng script:

```bash
# Run test
test-backend.bat
```

Hoặc thủ công:

```bash
# Activate conda env
conda activate ai-powered-job-application-automator

# Test imports
python -c "from app.db.mongodb import database; from app.db.vector_db import vector_db; print('✅ Imports OK')"

# Start backend
cd apps\backend
python -m uvicorn app.main:app --reload

# Mở browser: http://localhost:8000/docs
# Test endpoint: GET /health
```

---

## Quick Reference 📌

| Service  | Port | URL | Purpose |
|----------|------|-----|---------|
| MongoDB  | 27017 | mongodb://localhost:27017 | Primary database |
| Qdrant   | 6333 | http://localhost:6333 | Vector search |
| Backend  | 8000 | http://localhost:8000 | FastAPI server |
| Frontend | 3000 | http://localhost:3000 | React app |

---

**Xong rồi! Giờ chạy `setup-databases.bat` để bắt đầu! 🚀**
