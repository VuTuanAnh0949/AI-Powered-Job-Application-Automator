# AutoApply AI: Smart Job Application Assistant ✨

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/react-18.3-blue.svg" alt="React Version">
  <img src="https://img.shields.io/badge/AI-Gemini%20%7C%20Groq-purple.svg" alt="AI Powered">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/version-2.0.0-brightgreen.svg" alt="Version">
</p>

<p align="center">
  <strong>Developed by:</strong> Vu Tuan Anh<br>
  📧 vutuananh0949@gmail.com | 🔗 <a href="https://github.com/VuTuanAnh0949">GitHub: VuTuanAnh0949</a>
</p>

---

**AutoApply AI is an intelligent system designed to streamline your job search. It automates finding relevant job postings, crafting personalized resumes and cover letters using AI (Gemini & Groq), and assists with application submissions, helping you land your dream job faster.**

## 🆕 Version 2.0 - Monorepo Architecture

AutoApply AI v2.0 has been completely restructured with modern architecture:

- 🏗️ **Monorepo Structure** - Organized `apps/` and `packages/`
- 🚀 **FastAPI Backend** - Clean architecture REST API
- 💎 **React Frontend** - Modern TypeScript UI with Vite
- 🐳 **Docker Ready** - Full containerization support
- 📦 **Shared Packages** - Reusable code across services

**📚 Quick Links:**
- [Hướng dẫn chi tiết (Vietnamese)](HUONG_DAN_V2.md)
- [Monorepo Structure](MONOREPO_STRUCTURE.md)
- [Backend Docs](apps/backend/README.md)
- [Frontend Docs](apps/frontend/README.md)

---

## 🌟 Features

- 🔍 **Multi-source Job Search**: Search for jobs across LinkedIn, Indeed, Glassdoor, and other platforms.
- 🧠 **Intelligent Job Filtering**: Filter jobs based on your skills, experience, location, and custom keywords.
- ✍️ **AI-Powered Document Generation**: Create tailored resumes and cover letters for each job application using advanced AI models (e.g., Llama 4 Maverick, Llama 3).
- 🚀 **Automated Application Submission**: Assists with or fully automates submitting applications through supported platforms like LinkedIn.
- 📊 **Job Match Scoring**: Calculates compatibility scores between your profile and job requirements to prioritize applications.
- 📈 **Application Tracking**: Keep track of all your job applications, their statuses, and follow-up actions in one place.
- 📄 **Resume Optimization**: Analyzes your existing resume against job descriptions and suggests improvements.

---

## 🎬 Demo / Screenshots

_(Placeholder: Consider adding a GIF or screenshots showcasing AutoApply AI in action. For example, a screen recording of the job search, resume generation, or application submission process.)_

```
[-------------------------------------]
|                                     |
|              |
|                                     |
[-------------------------------------]
```

---

## 📚 Table of Contents

- [AutoApply AI: Smart Job Application Assistant ✨](#autoapply-ai-smart-job-application-assistant-)
- [🌟 Features](#-features)
- [🎬 Demo / Screenshots](#-demo--screenshots)
- [🛠️ Technology Stack](#️-technology-stack)
- [📁 Project Structure](#-project-structure)
- [🚀 Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [💡 Usage](#-usage)
- [🎨 Customization](#-customization)
  - [Resume and Cover Letter Templates](#resume-and-cover-letter-templates)
- [🤝 Contributing](#-contributing)
- [🛡️ Safety and Ethics](#️-safety-and-ethics)
- [📜 License](#-license)
- [🙏 Acknowledgments](#-acknowledgments)

---

## 🛠️ Technology Stack

- **Core Engine**: Python 3.10+
- **AI Models**:
  - Google Gemini 2.5-flash (via `google-genai`)
  - Groq Llama 3.3-70B-versatile
- **Browser Automation**: Playwright, Selenium for web interactions
- **Web Scraping**: Crawl4AI for intelligent data extraction from job listings
- **Document Processing**: `python-docx` for MS Word documents
- **Database**: SQLite with SQLAlchemy ORM
- **Database Migrations**: Alembic
- **Configuration Management**: Pydantic, `.env` files, YAML
- **Dependencies**: See `requirements.txt`

---

## 📁 Project Structure

```
job_application_automation/
├── .env.example                # Example environment variables
├── README.md                   # This file
├── requirements.txt            # Python dependencies for this application
├── alembic.ini                 # Alembic migration configuration
├── config/                     # Configuration settings
│   ├── __init__.py
│   ├── browser_config.py       # Browser automation settings
│   ├── llama_config.py         # LLM settings
│   └── ... (other config files)
├── data/                       # Data storage (logs, generated docs, DB, etc.)
│   ├── candidate_profile.json  # Example candidate profile
│   ├── job_applications.db     # SQLite database for tracking
│   └── generated_cover_letters/
├── src/                        # Source code
│   ├── __init__.py
│   ├── main.py                 # Main application entry point
│   ├── smart_apply.py          # Core application logic script
│   ├── browser_automation.py   # Browser interaction logic
│   ├── web_scraping.py         # Job scraping utilities
│   ├── linkedin_integration.py # LinkedIn specific functions
│   ├── resume_cover_letter_generator.py # AI document generation
│   ├── resume_optimizer.py     # Resume analysis and improvement
│   ├── application_tracker.py  # Tracks job applications
│   ├── database.py             # Database models and session management
│   └── ... (other modules)
├── templates/                  # Document templates (resume, cover letter)
│   ├── resume_template.docx
│   └── cover_letter_template.docx
├── tests/                      # Test cases
└── ... (other project files)
```

---

## 🚀 Getting Started

### Prerequisites

**Python 3.10 or higher** (3.11-3.12 recommended)

- Pip (Python package installer)
- Git (for cloning the repository)
- **AI API Keys** (at least one):
  - **Gemini API Key** (recommended): Get from [Google AI Studio](https://aistudio.google.com/app/apikey)
  - **Groq API Key** (alternative): Get from [Groq Console](https://console.groq.com/keys)
- (Optional) LinkedIn account for direct integration featurestalled.
- (Optional) LinkedIn account for features involving direct LinkedIn interaction.

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/VuTuanAnh0949/ai-powered-job-application-automator.git
    cd ai-powered-job-application-automator
    ```

2.  **Create and activate a virtual environment (recommended):**

    ```bash
    # Using conda (recommended)
    conda create -n job-automation python=3.10
    conda activate job-automation

    # Or using venv
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r job_application_automation/requirements.txt

        # Install Playwright browsers (for browser automation)
        playwright install chromium
        ```

    and edit the `.env` file:
    `bash
    cd job_application_automation
    # Edit .env file with your API keys
    `

        **Required configurations:**
        ```env
        # --- AI Provider Configuration ---
        LLAMA_USE_API=True
        LLAMA_API_PROVIDER=gemini  # Options: "gemini" or "groq"

        # Gemini Configuration (Recommended)
        GEMINI_API_KEY=AIzaSy...your_key_here
        LLAMA_API_MODEL=models/gemini-2.5-flash

        # OR Groq Configuration (Alternative)
        # GROQ_API_KEY=gsk_...your_key_here
        # LLAMA_API_MODEL=llama-3.3-70b-versatile

        # --- Database Configuration ---
        DATABASE_URL=sqlite:///data/job_applications.db

        # --- Application Settings ---
        MAX_DAILY_APPLICATIONS=50
        AUTO_APPLY_ENABLED=False  # Set to True for automatic application
        HEADLESS_MODE=True
        DEBUG_MODE=False
        ```

        **Get API Keys:**
        - **Gemini**: Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
        - **Groq**: Visit [Groq Console](https://console.groq.com/keys)INKEDIN_PASSWORD="your_linkedin_password"

        # --- Other configurations ---
        # Review config/ files for more settings like browser paths, etc.
        ```

    Initialize the database:
    `bash
    cd job_application_automation
    python src/init_db.py
    `
    This creates the SQLite database at `data/job_applications.db`
    ```    This command should be run from the`job_application_automation`directory where`alembic.ini`is located. This will create/update the`job_applications.db`file in the`job_application_automation/data/` directory.

4.  **Candidate Profile:**
    Create or update your candidate profile in `data/candidate_profile.json`. This file is used to personalize resumes and cover letters. An example structure might be:
    ```json
    {
      "full_name": "Your Name",
      "email": "your.email@example.com",
      "phone": "123-456-7890",
      "linkedin_url": "https://linkedin.com/in/yourprofile",
      "github_url": "https://github.com/yourusername",
      "portfolio_url": "https://yourportfolio.com",
      "summary": "A brief professional summary...",
      "skills": ["Python", "AI", "Web Scraping", "Project Management"],
      "experience": [
        {
          "title": "Software Engineer",
          "company": "Tech Corp",
          "dates": "Jan 2020 - Present",
          "description": "Developed amazing things..."
        }
      ],
      "education": [
        {
          "degree": "B.S. in Computer Science",
          "university": "State University",
          "year": "2019"
        }
      ]
    }
    ```

---

### **Quick Start: Generate Resume & Cover Letter**

The most common use case - generate AI-powered documents:

```bash
# From project root
python generate_ai_docs.py --company "Google" --job "AI Engineer"

# With job description
python generate_ai_docs.py --company "VNG" --job "Senior Developer" --description "Build scalable systems..."

# Interactive mode
python generate_ai_docs.py -i
```

Generated documents will be saved in `job_application_automation/data/generated_cover_letters/`

### **Advanced Usage**

**1. Search for Jobs:**

````bash
cd jCandidate Profile

Edit your profile in `job_application_automation/data/candidate_profile.json`:

```json
{
  "full_name": "Your Name",
  "email": "your.email@example.com",
  "phone": "+1234567890",
  "summary": "Experienced AI Engineer...",
  "skills": ["Python", "TensorFlow", "AWS", "Docker"],
  "experience": [
    {
      "title": "AI Engineer",
      "company": "Tech Corp",
      "duration": "2020-Present",
      "description": "Built ML models..."
    }
  ],welcome! Whether it's bug reports, feature requests, or code improvements:

1.  Fork the repository
2.  Create a feature branch: `git checkout -b feature/amazing-feature`
3.  Commit your changes: `git commit -m 'Add amazing feature'`
4.  Push to the branch: `git push origin feature/amazing-feature`
5.  Open a Pull Request

Please ensure your code follows the existing style and includes appropriate documentation
python -m src.manage_db --add --job-title "AI Engineer" --company "Google" --status "Applied"

# Update status
python -m src.manage_db --update-status --id 1 --status "Interview"
````

**4. View Database:**
Use [DB Browser for SQLite](https://sqlitebrowser.org/) to open `job_application_automation/data/job_applications.db`

For detailed usage, see [HUONG_DAN_SU_DUNG.md](HUONG_DAN_SU_DUNG.md) (Vietnamese guide) - Review and approve generated documents. - Track application status.
_(Refer to the script's help messages or internal documentation for specific commands: `python src/smart_apply.py --help`)_

---

## 🎨 Customization



## 🤝 Contribleverages powerful open-source tools:

- **AI Models**: Google Gemini, Meta Llama (via Groq)
- **Browser Automation**: Playwright, Selenium
- **Web Scraping**: Crawl4AI
- **Document Processing**: python-docx
- **Database**: SQLAlchemy, Alembic
- The Python community and all open-source contributors

---

## 📞 Contact

**Developed by:** Vu Tuan Anh  
📧 **Email:** vutuananh0949@gmail.com  
🔗 **GitHub:** [@VuTuanAnh0949](https://github.com/VuTuanAnh0949)

---

\*Built with ❤️ using AI to help job seekers land their dream jobs fasterude new tests. 5. **Push your branch** to your fork:
`bash
    git push origin feature/your-amazing-feature
    ` 6. **Open a Pull Request** against the `main` (or `develop`) branch of the original repository. Please provide a detailed description of your changes.

---

## 🛡️ Safety and Ethics

AutoApply AI is a powerful tool. Please use it responsibly and ethically:

1.  **Review AI-Generated Content**: **Always** carefully review resumes, cover letters, and any application answers generated by the AI before submission. Ensure accuracy, authenticity, and that it truly represents you.
2.  **Respect Rate Limits**: Be mindful of the frequency of job searches and application submissions to avoid overloading job portals or APIs. Configure delays if necessary.
3.  **Honest Representation**: Do not use this tool to misrepresent your skills, experience, or qualifications. The AI is an assistant, not a replacement for your genuine abilities.
4.  **Adhere to Terms of Service**: Respect the terms of service of any job boards (LinkedIn, Indeed, etc.) or platforms interacted with by this tool. Automation may be against the ToS of some platforms.
5.  **Privacy**: Be cautious about the personal information you provide (credentials, profile data) and how it's handled by the system and any third-party APIs. Store sensitive data securely.

---

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file in the repository for full details.
_(If no LICENSE file exists, consider adding one. MIT is a common choice for open-source projects.)_

---

## 🙏 Acknowledgments

This project stands on the shoulders of giants and leverages many fantastic open-source tools and communities:

- [browser-use](https://github.com/browser-use/browser-use) for robust browser automation.
- [Crawl4AI](https://github.com/crawl4ai/crawl4ai) for intelligent web scraping.
- LLM Providers & Libraries (e.g., [Llama CPP](https://github.com/ggerganov/llama.cpp) for local models, Hugging Face, OpenAI, Groq, OpenRouter).
- [python-docx-template (docxtpl)](https://github.com/elapouya/python-docx-template) for Word document template rendering.
- The Python community and the developers of numerous other libraries used.

---

_This README was enhanced with the help of Trae AI, your agentic AI coding assistant._

```


```
