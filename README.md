# Fresher Job Matcher - Bangalore

## 🚀 Overview
A simple localhost-based job matching system for college freshers in Bangalore.

**Single Feature**: Match your resume with Bangalore job openings

### Input Fields
1. **Your Name** - Username
2. **Your Resume** - Paste resume content
3. **Preferred Domain** - Python, AI, GenAI, Backend, Full Stack, Automation
4. **Location** - Auto-set to Bangalore

### Output
- Resume ATS Score (0-100)
- Skills detected from resume
- Matched job opportunities
- Match percentage for each job
- Missing skills for each role
- Direct apply links

---

## ⚡ Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/aavulachithra7-ops/fresher-job-automation.git
cd fresher-job-automation
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Application
```bash
python main.py
```

### 5. Open Browser
```
http://localhost:8000
```

---

## 📁 Project Structure
```
fresher-job-automation/
├── main.py                    # FastAPI app (entry point)
├── requirements.txt           # Dependencies
├── README.md                  # This file
├── app/
│   ├── __init__.py
│   ├── resume_parser.py       # Resume parsing & ATS scoring
│   ├── job_matcher.py         # Job matching logic
│   └── jobs_database.json     # Local job database
├── templates/
│   └── index.html             # Web form & results UI
└── static/
    └── style.css              # Beautiful styling
```

---

## 🎯 How It Works

1. **User enters**:
   - Name
   - Resume content
   - Domain preference
   - Location (auto: Bangalore)

2. **System processes**:
   - Parses resume for skills, projects, experience
   - Calculates ATS score (0-100)
   - Filters jobs by domain
   - Matches resume against job requirements

3. **Displays**:
   - Resume analysis card
   - List of matched jobs
   - Match percentage for each job
   - Missing skills
   - Apply buttons with career page links

---

## 🏢 Pre-loaded Jobs
10 Bangalore-based job opportunities from:
- Flipkart
- Unacademy
- Razorpay
- Byju's
- Infosys
- Freshworks
- Atlassian
- Paytm
- Jio Platforms
- Dream11

---

## 🔧 Tech Stack
- **Backend**: FastAPI + Uvicorn
- **Frontend**: HTML5 + CSS3
- **Data Processing**: Pandas, scikit-learn
- **Database**: JSON (local)

---

## 📊 ATS Score Calculation
- **Skills** (40 points): Based on skill count
- **Projects** (30 points): Based on project mentions
- **Experience** (20 points): Fresher bonus included
- **Education** (10 points): Degree detection

**Total**: 0-100 score

---

## ✨ Features
✅ Beautiful purple gradient UI
✅ Responsive design (mobile-friendly)
✅ Real-time form validation
✅ Loading spinner
✅ Error handling
✅ Skill matching algorithm
✅ Resume analysis
✅ Direct apply links

---

## 📝 Sample Resume
```
Name: Aarav Kulkarni

Education:
B.Tech in Computer Science, IIT Bangalore (2026)

Skills:
Python, FastAPI, Django, React, PostgreSQL, Docker, Git, AWS
Machine Learning, TensorFlow, NLP, Pandas, Scikit-learn

Experience:
2 years freelance full-stack development

Projects:
1. AI Chatbot using LangChain and OpenAI
2. E-commerce platform with FastAPI and React
3. Data analysis dashboard with Pandas
4. Web scraper using Selenium
```

---

**Built with ❤️ for freshers in Bangalore**
