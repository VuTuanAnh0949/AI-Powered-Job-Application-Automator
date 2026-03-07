# Setup Instructions for AutoApply AI v2.0

## Quick Start with Docker (Recommended)

### 1. Start all services with Docker Compose

```bash
# Create docker-compose.yml for easy setup
docker-compose up -d
```

This will start:
- MongoDB (port 27017)
- Qdrant Vector DB (port 6333)
- Backend API (port 8000)
- Frontend UI (port 3000)

---

## Manual Setup (Development)

### 1. Install & Start MongoDB

**Option A: Docker**
```bash
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

**Option B: Local Installation**
- Download: https://www.mongodb.com/try/download/community
- Install and start MongoDB service
- Default: `mongodb://localhost:27017`

### 2. Install & Start Qdrant

**Option A: Docker**
```bash
docker run -d -p 6333:6333 --name qdrant qdrant/qdrant:latest
```

**Option B: Local Installation**
```bash
# Download from: https://qdrant.tech/documentation/quick-start/
# Or use docker (recommended)
```

### 3. Setup Backend

```bash
# Activate conda environment
conda activate ai-powered-job-application-automator

# Install new dependencies
cd apps/backend
pip install -r requirements.txt

# Create .env from example
copy .env.example .env

# Edit .env and add:
# - MONGODB_URL=mongodb://localhost:27017
# - QDRANT_URL=http://localhost:6333
# - GEMINI_API_KEY=your_api_key
# - Other API keys

# Start backend
start-backend.bat
```

### 4. Setup Frontend

```bash
cd apps/frontend
npm install  # If not done yet
npm run dev
```

---

## Docker Compose Setup (All-in-One)

Create `docker-compose.yml` in project root:

```yaml
version: '3.8'

services:
  mongodb:
    image: mongo:latest
    container_name: autoapply_mongodb
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
    environment:
      MONGO_INITDB_DATABASE: autoapply_ai

  qdrant:
    image: qdrant/qdrant:latest
    container_name: autoapply_qdrant
    ports:
      - "6333:6333"
    volumes:
      - qdrant_data:/qdrant/storage

  backend:
    build:
      context: ./apps/backend
      dockerfile: Dockerfile
    container_name: autoapply_backend
    ports:
      - "8000:8000"
    environment:
      - MONGODB_URL=mongodb://mongodb:27017
      - QDRANT_URL=http://qdrant:6333
    depends_on:
      - mongodb
      - qdrant
    volumes:
      - ./apps/backend:/app
      - ./data:/app/data

  frontend:
    build:
      context: ./apps/frontend
      dockerfile: Dockerfile
    container_name: autoapply_frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
    volumes:
      - ./apps/frontend:/app
      - /app/node_modules

volumes:
  mongodb_data:
  qdrant_data:
```

**Start everything:**
```bash
docker-compose up -d
```

**Stop everything:**
```bash
docker-compose down
```

---

## Verify Installation

### Check MongoDB:
```bash
# PowerShell
Invoke-WebRequest http://localhost:27017

# Or use MongoDB Compass GUI
# Download: https://www.mongodb.com/products/compass
```

### Check Qdrant:
```bash
# PowerShell
Invoke-WebRequest http://localhost:6333

# Or open in browser
http://localhost:6333/dashboard
```

### Check Backend:
```bash
# PowerShell
Invoke-WebRequest http://localhost:8000/health

# Or open in browser
http://localhost:8000/api/docs
```

### Check Frontend:
```bash
# Open in browser
http://localhost:3000
```

---

## Environment Variables

Update `apps/backend/.env`:

```env
# MongoDB
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=autoapply_ai

# Qdrant Vector DB
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=  # Leave empty for local
QDRANT_COLLECTION_NAME=job_embeddings

# AI Providers (at least one required)
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
GROQ_API_KEY=your_groq_api_key_here
DEFAULT_LLM_PROVIDER=gemini

# Job Platforms (optional)
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password
```

---

## Troubleshooting

### MongoDB Connection Failed
```bash
# Check if MongoDB is running
Get-Process mongod

# Or check port
Test-NetConnection localhost -Port 27017
```

### Qdrant Connection Failed
```bash
# Check if Qdrant is running
Test-NetConnection localhost -Port 6333

# Check docker container
docker ps | findstr qdrant
```

### Backend Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Port Already in Use
```bash
# Kill process on port
Get-NetTCPConnection -LocalPort 8000 | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }
```

---

## Next Steps

1. ✅ Start MongoDB & Qdrant
2. ✅ Configure .env files
3. ✅ Start backend & frontend
4. 🔄 Setup user profile
5. 🔄 Start searching for jobs
6. 🔄 Generate tailored resumes

---

## Development Commands

```bash
# Backend
start-backend.bat          # Start backend server
test-backend.bat          # Test backend setup

# Frontend
cd apps/frontend
npm run dev               # Start dev server
npm run build             # Build for production
npm run test              # Run tests

# Database
# MongoDB shell
mongosh                   # Connect to MongoDB

# Reset databases (CAUTION!)
# MongoDB
docker exec -it autoapply_mongodb mongosh --eval "db.dropDatabase()"

# Qdrant
curl -X DELETE http://localhost:6333/collections/job_embeddings
```

---

**Ready to start!** 🚀

Run: `start-all.bat` or `docker-compose up -d`
