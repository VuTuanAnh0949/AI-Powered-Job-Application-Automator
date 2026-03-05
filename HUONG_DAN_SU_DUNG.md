# 📖 HƯỚNG DẪN SỬ DỤNG - AI JOB APPLICATION AUTOMATOR

## 🎯 TỔNG QUAN CHỨC NĂNG

Project này là **hệ thống tự động hóa tìm việc và ứng tuyển với AI**, bao gồm:

### ✨ Các Chức Năng Chính

1. **🔍 Tìm Kiếm Việc Làm (Job Search)**
   - Tìm việc trên LinkedIn, Indeed, Glassdoor
   - Tự động lọc theo kỹ năng, vị trí, từ khóa
   - Lưu danh sách công việc

2. **📝 Tạo CV & Cover Letter với AI**
   - Tự động tạo CV phù hợp với từng công việc
   - Tạo cover letter được cá nhân hóa
   - Hỗ trợ Gemini 2.5-flash & Groq Llama 3.3

3. **🎯 Phân Tích & Chấm Điểm Resume (ATS Scoring)**
   - Đánh giá độ phù hợp CV với job description
   - Phân tích từ khóa, kỹ năng, kinh nghiệm
   - Đề xuất cải thiện CV

4. **🚀 Tự Động Nộp Đơn (Auto-Apply)**
   - Tự động điền form ứng tuyển
   - Hỗ trợ LinkedIn, Indeed (beta)
   - Browser automation với Playwright/Selenium

5. **📊 Theo Dõi Đơn Ứng Tuyển (Application Tracking)**
   - Database lưu trữ tất cả đơn đã nộp
   - Theo dõi trạng thái (Applied, Interview, Rejected, Offer)
   - Quản lý follow-up dates

---

## 🖥️ GIAO DIỆN

### **❌ Hiện tại: KHÔNG có giao diện đồ họa**

- Project chủ yếu chạy qua **Command Line (CLI)**
- Có **Streamlit UI cơ bản** nhưng chưa hoàn thiện
- Tất cả chức năng đều dùng terminal

### **✅ Sẽ có trong tương lai (nếu cần):**

- Web UI với Streamlit
- Desktop GUI
- Dashboard theo dõi ứng tuyển

---

## 📁 DATABASE - XEM Ở ĐÂU?

### **📍 Vị trí:**

```
job_application_automation/data/job_applications.db
```

### **🔍 Cách xem Database:**

#### **Option 1: DB Browser for SQLite (Recommended)**

```bash
# Download: https://sqlitebrowser.org/
# Mở file: job_applications.db
```

#### **Option 2: Python script**

```python
import sqlite3
conn = sqlite3.connect('job_application_automation/data/job_applications.db')
cursor = conn.cursor()

# Xem tất cả applications
cursor.execute("SELECT * FROM job_applications")
for row in cursor.fetchall():
    print(row)
```

#### **Option 3: CLI trong project**

```bash
python -m job_application_automation.src.manage_db --list
```

### **🗂️ Database Schema:**

- `job_applications` - Lưu các đơn đã nộp
  - id, job_title, company, status, applied_date, resume_path, cover_letter_path
- `job_listings` - Lưu danh sách công việc tìm được
- `resume_versions` - Lưu các phiên bản CV đã tạo

---

## 🚀 CÁCH CHẠY CÁC CHỨC NĂNG

### **1. Tạo Resume & Cover Letter với AI**

#### **📌 Script 1: generate_ai_docs.py (Recommended)**

```bash
# Cơ bản - dùng defaults
python generate_ai_docs.py --company "VNG Corporation" --job "Senior AI Engineer"

# Với job description
python generate_ai_docs.py --company "Google" --job "ML Engineer" --description "Build ML models..."

# Interactive mode (nhập tay từng thông tin)
python generate_ai_docs.py -i

# Xem help
python generate_ai_docs.py --help
```

**Output:**

- File `.docx` trong `job_application_automation/data/generated_cover_letters/`
- Format: `YYYYMMDD_HHMMSS_CompanyName_resume.docx`

#### **📌 Script 2: generate_documents.py (Giống y hệt)**

```bash
python generate_documents.py --company "Microsoft" --job "Software Engineer"
```

#### **📌 Script 3: generate_with_groq.py (Chỉ dùng Groq)**

```bash
python generate_with_groq.py
```

**⚙️ Chọn AI Provider:**

- Mở `.env` file
- Thay đổi `LLAMA_API_PROVIDER=gemini` hoặc `groq`

---

### **2. Tìm Kiếm Việc Làm**

```bash
# CLI chính
cd job_application_automation
python src/cli.py search --keywords "python,ai,machine learning" --location "Remote"

# Với LinkedIn
python src/cli.py search --keywords "data scientist" --linkedin

# Với browser automation (mở trình duyệt thật)
python src/cli.py search --keywords "python" --browser --site linkedin
```

**Output:**

- `job_listings.json` - Danh sách công việc
- `linkedin_job_listings.json` - Từ LinkedIn
- `combined_job_listings.json` - Tổng hợp

---

### **3. Chấm Điểm Resume (ATS Scoring)**

```bash
# Analyze resume vs job description
python -m job_application_automation.src.ats_cli \
  --resume "path/to/your_resume.pdf" \
  --job-desc "path/to/job_description.txt" \
  --analyze

# Với optimize (tự động cải thiện nếu điểm thấp)
python -m job_application_automation.src.ats_cli \
  --resume "resume.pdf" \
  --job-desc "job.txt" \
  --optimize \
  --target-score 0.75
```

**Output:**

- Score: 0-100
- Report trong `data/ats_reports/`
- Optimized resume nếu dùng `--optimize`

---

### **4. Tự Động Nộp Đơn (Smart Apply)**

```bash
cd job_application_automation
python src/smart_apply.py \
  --resume "path/to/resume.pdf" \
  --job-url "https://linkedin.com/jobs/view/12345" \
  --auto-apply
```

**⚠️ Lưu ý:**

- Cần LinkedIn cookies (login trước)
- Browser automation có thể bị block bởi CAPTCHA
- Khuyến nghị: Manual apply sau khi generate documents

---

### **5. Theo Dõi Ứng Tuyển**

```bash
# List tất cả applications
python -m job_application_automation.src.manage_db --list

# Add application manually
python -m job_application_automation.src.manage_db --add \
  --job-title "AI Engineer" \
  --company "Google" \
  --status "Applied"

# Update status
python -m job_application_automation.src.manage_db --update-status \
  --id 1 \
  --status "Interview"

# Xem statistics
python -m job_application_automation.src.manage_db --stats
```

---

### **6. Streamlit UI (Beta)**

```bash
cd job_application_automation/src/interfaces
streamlit run ui_app.py
```

**Truy cập:** http://localhost:8501

**Chức năng UI:**

- Search jobs
- Generate documents
- View applications
- (Chưa đầy đủ như CLI)

---

## 📊 LUỒNG HOẠT ĐỘNG TỔNG THỂ

```
┌─────────────────────────────────────────────────────────────┐
│                    1. TÌM VIỆC                             │
│  python src/cli.py search --keywords "python" --location "Remote" │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
        ┌─────────────────────┐
        │  job_listings.json  │
        │  (100+ jobs)        │
        └─────────┬───────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│              2. CHỌN JOB & PHÂN TÍCH                       │
│  - Đọc job description                                      │
│  - Chấm điểm resume hiện tại                               │
│  python ats_cli.py --analyze                               │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
        ┌─────────────────────┐
        │  ATS Score: 75/100  │
        │  (Pass threshold)   │
        └─────────┬───────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│           3. TẠO CV & COVER LETTER                         │
│  python generate_ai_docs.py --company "Google" --job "AI Engineer" │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
        ┌─────────────────────────────────┐
        │  ✅ resume.docx                │
        │  ✅ cover_letter.docx          │
        │  (Personalized with AI)        │
        └─────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│              4. NỘP ĐƠN (Manual/Auto)                      │
│  - Manual: Upload files to job portal                      │
│  - Auto: python smart_apply.py --auto-apply               │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
        ┌─────────────────────────────────┐
        │  Save to Database               │
        │  job_applications.db            │
        └─────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│              5. THEO DÕI & FOLLOW-UP                       │
│  python manage_db.py --list                                │
│  Update status: Applied → Interview → Offer               │
└─────────────────────────────────────────────────────────────┘
```

---

## ⚙️ CẤU HÌNH (Configuration)

### **File: job_application_automation/.env**

```env
# AI Provider (chọn 1)
LLAMA_API_PROVIDER=gemini  # hoặc groq

# API Keys
GEMINI_API_KEY=AIzaSy...
GROQ_API_KEY=gsk_...

# LinkedIn (optional)
LINKEDIN_CLIENT_ID=your_id
LINKEDIN_CLIENT_SECRET=your_secret

# Browser Automation
BROWSER_TYPE=chromium
BROWSER_HEADLESS=true

# Auto-Apply Settings
MAX_DAILY_APPLICATIONS=50
AUTO_APPLY_ENABLED=False  # Bật/tắt auto-apply
```

---

## 📦 CẤU TRÚC THƯ MỤC

```
job_application_automation/
├── data/                          # ✅ DỮ LIỆU
│   ├── job_applications.db       # 📊 DATABASE chính
│   ├── candidate_profile.json    # 👤 Profile của bạn
│   ├── job_listings.json         # 📋 Danh sách việc làm
│   ├── generated_cover_letters/  # 📝 CV & Cover letter được tạo
│   ├── ats_reports/              # 📈 Báo cáo ATS scores
│   └── logs/                     # 📜 Log files
│
├── src/                           # ✅ SOURCE CODE
│   ├── cli.py                    # 🖥️ CLI chính
│   ├── main.py                   # 🚀 Main orchestrator
│   ├── smart_apply.py            # 🤖 Auto-apply logic
│   ├── ats_cli.py                # 📊 ATS scoring CLI
│   ├── resume_optimizer.py       # ✨ Resume analyzer
│   ├── application_tracker.py    # 📋 Track applications
│   │
│   ├── job_sources/              # 🔍 Job search integrations
│   │   ├── linkedin_integration.py
│   │   ├── indeed_integration.py
│   │   └── glassdoor_integration.py
│   │
│   ├── interfaces/               # 🖼️ UI (Streamlit)
│   │   └── ui_app.py
│   │
│   └── utils/                    # 🛠️ Utilities
│       ├── browser_automation.py
│       └── web_scraping.py
│
├── config/                        # ⚙️ Configuration
│   ├── config.yaml
│   └── gemini_config.py
│
└── scripts/                       # 📜 Utility scripts
    ├── generate_ai_docs.py       # ✅ Tạo documents
    ├── generate_with_groq.py     # ✅ Groq-only generator
    └── test_system.py            # ✅ Test setup
```

---

## 🎓 WORKFLOW KHUYẾN NGHỊ

### **Use Case 1: Nộp 1 công việc cụ thể**

```bash
# Bước 1: Tạo documents
python generate_ai_docs.py --company "Google" --job "ML Engineer"

# Bước 2: Manual upload
# - Mở job posting
# - Upload resume.docx và cover_letter.docx
# - Submit application

# Bước 3: Lưu vào database
python -m job_application_automation.src.manage_db --add \
  --job-title "ML Engineer" \
  --company "Google" \
  --status "Applied"
```

### **Use Case 2: Tìm kiếm hàng loạt**

```bash
# Bước 1: Search jobs
python src/cli.py search --keywords "python,ai" --location "Remote"

# Bước 2: Review job_listings.json
cat job_application_automation/data/job_listings.json

# Bước 3: Generate documents cho từng job
python generate_ai_docs.py --company "Company1" --job "Title1"
python generate_ai_docs.py --company "Company2" --job "Title2"
# ... (có thể viết script loop)

# Bước 4: Batch apply (manual hoặc auto)
```

### **Use Case 3: Optimize resume hiện tại**

```bash
# Check ATS score
python -m job_application_automation.src.ats_cli \
  --resume "my_resume.pdf" \
  --job-desc "target_job.txt" \
  --analyze

# Nếu score < 70, optimize
python -m job_application_automation.src.ats_cli \
  --resume "my_resume.pdf" \
  --job-desc "target_job.txt" \
  --optimize \
  --target-score 0.80
```

---

## 🆘 TROUBLESHOOTING

### **Lỗi API Key**

```bash
# Check API key trong .env
cat job_application_automation/.env | grep API_KEY

# Test API
python check_gemini_models.py  # Check Gemini models
python test_quick.py           # Test both Gemini & Groq
```

### **Database locked**

```bash
# Đóng tất cả processes đang access DB
# Hoặc delete lock file
rm job_application_automation/data/job_applications.db-journal
```

### **Import errors**

```bash
# Re-install dependencies
pip install -r requirements.txt
```

### **Browser automation fails**

```bash
# Install browsers
playwright install chromium

# Test manually
python -c "from playwright.sync_api import sync_playwright; sync_playwright().start()"
```

---

## 📞 HỖ TRỢ

- **Documentation:** [docs/](docs/)
- **API Reference:** [docs/API.md](docs/API.md)
- **Integration Guide:** [docs/INTEGRATION_PLAN.md](docs/INTEGRATION_PLAN.md)
- **Tools List:** [docs/TOOLS.md](docs/TOOLS.md)

---

## 🎯 TÓM TẮT NHANH

| Chức năng       | Command                                              | Output                |
| --------------- | ---------------------------------------------------- | --------------------- |
| **Tạo CV & CL** | `python generate_ai_docs.py --company "X" --job "Y"` | `.docx` files         |
| **Tìm việc**    | `python src/cli.py search --keywords "python"`       | `job_listings.json`   |
| **ATS Score**   | `python ats_cli.py --resume X.pdf --job-desc Y.txt`  | Score + report        |
| **Xem DB**      | SQLite Browser hoặc `python manage_db.py --list`     | Applications list     |
| **Auto-apply**  | `python smart_apply.py --job-url URL --auto-apply`   | Submitted application |

---

**✨ Happy job hunting! 🚀**
