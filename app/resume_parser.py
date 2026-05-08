import re
from collections import Counter

# Define skill keywords
PYTHON_SKILLS = [
    "python", "django", "flask", "fastapi", "async", "pandas", "numpy",
    "scikit-learn", "tensorflow", "pytorch", "automation", "requests"
]

AI_SKILLS = [
    "ai", "machine learning", "ml", "deep learning", "nlp", "genai",
    "llm", "prompt engineering", "langchain", "openai", "gemini",
    "transformers", "bert", "gpt", "computer vision", "cv"
]

BACKEND_SKILLS = [
    "backend", "api", "rest", "graphql", "database", "sql", "nosql",
    "mongodb", "postgres", "mysql", "redis", "elasticsearch", "rabbitmq",
    "microservices", "docker", "kubernetes"
]

FRONTEND_SKILLS = [
    "frontend", "react", "vue", "angular", "javascript", "typescript",
    "html", "css", "responsive design"
]

FULLSTACK_SKILLS = PYTHON_SKILLS + BACKEND_SKILLS + FRONTEND_SKILLS

GENAI_SKILLS = [
    "genai", "generative ai", "llm", "prompt engineering", "langchain",
    "openai", "claude", "gemini", "fine-tuning", "rag", "vector database"
]

AUTOMATION_SKILLS = [
    "automation", "selenium", "playwright", "ci/cd", "github actions",
    "jenkins", "testing", "pytest", "automation framework"
]

ALL_SKILLS = {
    "python": PYTHON_SKILLS,
    "ai": AI_SKILLS,
    "backend": BACKEND_SKILLS,
    "frontend": FRONTEND_SKILLS,
    "fullstack": FULLSTACK_SKILLS,
    "genai": GENAI_SKILLS,
    "automation": AUTOMATION_SKILLS
}


def parse_resume(resume_text: str) -> dict:
    """
    Parse resume and extract key information
    """
    resume_lower = resume_text.lower()
    
    # Extract skills
    skills_found = set()
    for skill_list in ALL_SKILLS.values():
        for skill in skill_list:
            if skill in resume_lower:
                skills_found.add(skill)
    
    # Extract projects (assume "project" mentions)
    projects = re.findall(
        r'project[s]?:?\s*([^\n]+)|built\s*([^\n]+)|developed\s*([^\n]+)',
        resume_lower
    )
    projects = [p[0] or p[1] or p[2] for p in projects if any(p)]
    
    # Extract experience (look for years)
    experience_match = re.search(r'(\d+)\s*\+?\s*years?', resume_lower)
    experience_years = int(experience_match.group(1)) if experience_match else 0
    
    # Extract education
    education = []
    if re.search(r'b\.?(tech|sc|e)', resume_lower):
        education.append("Bachelor's")
    if re.search(r'm\.?(tech|sc)', resume_lower):
        education.append("Master's")
    
    return {
        "skills": list(skills_found),
        "projects": projects[:5],  # Top 5 projects
        "experience_years": experience_years,
        "education": education,
        "text": resume_text
    }


def calculate_ats_score(resume_data: dict) -> int:
    """
    Calculate ATS score based on resume data (0-100)
    """
    score = 0
    
    # Skills (40 points)
    skills_count = len(resume_data["skills"])
    if skills_count > 0:
        score += min(40, skills_count * 5)
    
    # Projects (30 points)
    projects_count = len(resume_data["projects"])
    if projects_count > 0:
        score += min(30, projects_count * 10)
    
    # Experience (20 points)
    if resume_data["experience_years"] > 0:
        score += min(20, resume_data["experience_years"] * 5)
    else:
        score += 10  # Fresher bonus
    
    # Education (10 points)
    if resume_data["education"]:
        score += 10
    
    return min(100, score)
