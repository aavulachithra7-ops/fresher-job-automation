import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Sample job database (local)
SAMPLE_JOBS = [
    {
        "id": 1,
        "company": "Flipkart",
        "role": "Python Developer",
        "location": "Bangalore",
        "description": "Python backend developer with experience in FastAPI, REST APIs, and database design. Work on e-commerce platform",
        "skills_required": ["Python", "FastAPI", "PostgreSQL", "Docker", "REST API"],
        "salary_range": "4-6 LPA",
        "experience_required": "0-2 years",
        "application_url": "https://flipkart.com/careers",
        "posted_date": "2026-05-01"
    },
    {
        "id": 2,
        "company": "Unacademy",
        "role": "AI/ML Engineer",
        "location": "Bangalore",
        "description": "Build AI models for personalized learning. Work with LLMs, NLP, and recommendation systems. Freshers welcome.",
        "skills_required": ["Python", "Machine Learning", "TensorFlow", "NLP", "PyTorch"],
        "salary_range": "5-8 LPA",
        "experience_required": "Fresher",
        "application_url": "https://unacademy.com/careers",
        "posted_date": "2026-05-03"
    },
    {
        "id": 3,
        "company": "Razorpay",
        "role": "Backend Engineer",
        "location": "Bangalore",
        "description": "Build scalable payment processing backend. Python/Go experience. APIs, microservices, system design.",
        "skills_required": ["Python", "API Design", "Microservices", "MongoDB", "Redis"],
        "salary_range": "6-9 LPA",
        "experience_required": "0-1 years",
        "application_url": "https://razorpay.com/careers",
        "posted_date": "2026-05-02"
    },
    {
        "id": 4,
        "company": "Byju's",
        "role": "Full Stack Developer",
        "location": "Bangalore",
        "description": "Full stack development using Python backend and React frontend. Build educational platforms.",
        "skills_required": ["Python", "React", "Django", "PostgreSQL", "JavaScript"],
        "salary_range": "4-7 LPA",
        "experience_required": "Fresher",
        "application_url": "https://byjus.com/careers",
        "posted_date": "2026-04-28"
    },
    {
        "id": 5,
        "company": "Infosys",
        "role": "Python Automation Engineer",
        "location": "Bangalore",
        "description": "Automation testing and scripting with Python. Selenium, pytest, CI/CD pipelines.",
        "skills_required": ["Python", "Selenium", "pytest", "Automation", "GitHub Actions"],
        "salary_range": "3-5 LPA",
        "experience_required": "Fresher",
        "application_url": "https://infosys.com/careers",
        "posted_date": "2026-05-04"
    },
    {
        "id": 6,
        "company": "Freshworks",
        "role": "GenAI Engineer",
        "location": "Bangalore",
        "description": "Work on generative AI features. LLMs, prompt engineering, fine-tuning. Build AI-powered customer support tools.",
        "skills_required": ["Python", "GenAI", "LangChain", "OpenAI", "Prompt Engineering"],
        "salary_range": "6-10 LPA",
        "experience_required": "0-2 years",
        "application_url": "https://freshworks.com/careers",
        "posted_date": "2026-05-05"
    },
    {
        "id": 7,
        "company": "Atlassian",
        "role": "Backend Developer",
        "location": "Bangalore",
        "description": "Work on Jira backend. REST APIs, scalability, database optimization. Junior friendly.",
        "skills_required": ["Python", "Java", "REST API", "PostgreSQL", "Docker"],
        "salary_range": "8-12 LPA",
        "experience_required": "0-2 years",
        "application_url": "https://atlassian.com/careers",
        "posted_date": "2026-05-01"
    },
    {
        "id": 8,
        "company": "Paytm",
        "role": "Python Developer (FinTech)",
        "location": "Bangalore",
        "description": "Python development for fintech platform. APIs, payments, fraud detection systems.",
        "skills_required": ["Python", "FastAPI", "APIs", "PostgreSQL", "Kafka"],
        "salary_range": "5-8 LPA",
        "experience_required": "0-2 years",
        "application_url": "https://paytm.com/careers",
        "posted_date": "2026-04-30"
    },
    {
        "id": 9,
        "company": "Jio Platforms",
        "role": "AI Engineer",
        "location": "Bangalore",
        "description": "Machine learning models for telecom. Computer vision, NLP, recommendation systems.",
        "skills_required": ["Python", "ML", "TensorFlow", "Computer Vision", "Deep Learning"],
        "salary_range": "6-9 LPA",
        "experience_required": "Fresher",
        "application_url": "https://jio.com/careers",
        "posted_date": "2026-05-06"
    },
    {
        "id": 10,
        "company": "Dream11",
        "role": "Full Stack Developer",
        "location": "Bangalore",
        "description": "Full stack development for gaming platform. Python backend, React frontend, real-time updates.",
        "skills_required": ["Python", "React", "FastAPI", "WebSockets", "PostgreSQL"],
        "salary_range": "5-9 LPA",
        "experience_required": "0-2 years",
        "application_url": "https://dream11.com/careers",
        "posted_date": "2026-05-02"
    }
]


def match_jobs(resume_data: dict, domain: str, location: str = "Bangalore") -> list:
    """
    Match jobs based on resume and domain preference
    """
    
    # Get jobs from database
    jobs = get_jobs(location)
    
    # Filter by domain
    domain_jobs = filter_by_domain(jobs, domain)
    
    if not domain_jobs:
        return []
    
    # Calculate match scores
    matched_jobs = []
    for job in domain_jobs:
        match_score = calculate_match_score(
            resume_data,
            job,
            domain
        )
        
        if match_score > 40:  # Only include jobs with >40% match
            job_with_score = job.copy()
            job_with_score["match_percentage"] = match_score
            job_with_score["missing_skills"] = get_missing_skills(
                resume_data["skills"],
                job["skills_required"]
            )
            matched_jobs.append(job_with_score)
    
    # Sort by match score (descending)
    matched_jobs = sorted(
        matched_jobs,
        key=lambda x: x["match_percentage"],
        reverse=True
    )
    
    return matched_jobs


def get_jobs(location: str) -> list:
    """
    Get jobs from local database or file
    """
    jobs_file = "app/jobs_database.json"
    
    if os.path.exists(jobs_file):
        with open(jobs_file, "r") as f:
            content = f.read().strip()
            if content:
                try:
                    jobs = json.loads(content)
                except:
                    jobs = SAMPLE_JOBS
            else:
                jobs = SAMPLE_JOBS
    else:
        jobs = SAMPLE_JOBS
        # Save to file
        os.makedirs("app", exist_ok=True)
        with open(jobs_file, "w") as f:
            json.dump(SAMPLE_JOBS, f, indent=2)
    
    return jobs


def filter_by_domain(jobs: list, domain: str) -> list:
    """
    Filter jobs based on domain
    """
    domain_lower = domain.lower()
    
    domain_keywords = {
        "python": ["python", "fastapi", "django", "flask"],
        "ai": ["ai", "ml", "machine learning", "nlp", "deep learning"],
        "genai": ["genai", "llm", "gpt", "prompt engineering"],
        "backend": ["backend", "api", "microservices", "server"],
        "fullstack": ["full stack", "fullstack", "frontend", "backend"],
        "automation": ["automation", "selenium", "ci/cd", "testing"]
    }
    
    keywords = domain_keywords.get(domain_lower, [domain_lower])
    
    filtered = []
    for job in jobs:
        job_text = (job["role"] + " " + job["description"]).lower()
        if any(kw in job_text for kw in keywords):
            filtered.append(job)
    
    return filtered


def calculate_match_score(resume_data: dict, job: dict, domain: str) -> int:
    """
    Calculate match score between resume and job (0-100)
    """
    score = 0
    
    # Skill matching (60 points max)
    resume_skills = set([s.lower() for s in resume_data["skills"]])
    job_skills = set([s.lower() for s in job["skills_required"]])
    
    if job_skills:
        skill_overlap = len(resume_skills & job_skills)
        skill_score = (skill_overlap / len(job_skills)) * 60
        score += skill_score
    
    # Domain match (25 points)
    domain_lower = domain.lower()
    job_title = job["role"].lower()
    job_desc = job["description"].lower()
    
    if domain_lower in job_title or domain_lower in job_desc:
        score += 25
    elif any(kw in job_title or kw in job_desc for kw in ["develop", "engineer"]):
        score += 15
    
    # Experience match (15 points)
    if "fresher" in job["experience_required"].lower():
        score += 15
    elif resume_data["experience_years"] == 0:
        score += 10
    
    return min(100, int(score))


def get_missing_skills(resume_skills: list, job_skills: list) -> list:
    """
    Get missing skills for a job
    """
    resume_skills_lower = set([s.lower() for s in resume_skills])
    job_skills_lower = set([s.lower() for s in job_skills])
    
    missing = list(job_skills_lower - resume_skills_lower)
    return missing[:5]  # Top 5 missing skills
