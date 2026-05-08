from fastapi import FastAPI, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import json
from datetime import datetime
from app.resume_parser import parse_resume, calculate_ats_score
from app.job_matcher import match_jobs

app = FastAPI(title="Fresher Job Matcher")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
if not os.path.exists("static"):
    os.makedirs("static")
if not os.path.exists("templates"):
    os.makedirs("templates")


@app.get("/", response_class=HTMLResponse)
async def home():
    """Serve the main form page"""
    with open("templates/index.html", "r") as f:
        return f.read()


@app.post("/api/match-jobs")
async def match_jobs_endpoint(
    username: str = Form(...),
    resume: str = Form(...),
    domain: str = Form(...)
):
    """
    Process user input and match jobs
    
    Args:
        username: User's name
        resume: Resume content (text)
        domain: Preferred domain (Python, AI, Backend, Full Stack, GenAI)
    
    Returns:
        JSON with matched jobs and ATS analysis
    """
    
    if not username or not resume or not domain:
        return JSONResponse(
            {"error": "All fields are required"},
            status_code=400
        )
    
    if len(resume.strip()) < 50:
        return JSONResponse(
            {"error": "Resume must be at least 50 characters"},
            status_code=400
        )
    
    # Parse resume
    resume_data = parse_resume(resume)
    ats_score = calculate_ats_score(resume_data)
    
    # Match jobs
    matched_jobs = match_jobs(resume_data, domain, location="Bangalore")
    
    # Prepare response
    response = {
        "username": username,
        "domain": domain,
        "location": "Bangalore",
        "timestamp": datetime.now().isoformat(),
        "resume_analysis": {
            "ats_score": ats_score,
            "skills_found": resume_data["skills"],
            "projects_count": len(resume_data["projects"]),
            "experience_years": resume_data["experience_years"]
        },
        "matched_jobs": matched_jobs,
        "total_matches": len(matched_jobs)
    }
    
    # Save to history
    save_search_history(username, response)
    
    return response


@app.get("/api/history/{username}")
async def get_history(username: str):
    """
    Get search history for a user
    """
    history_file = f"data/history_{username}.json"
    
    if not os.path.exists(history_file):
        return {"history": []}
    
    with open(history_file, "r") as f:
        history = json.load(f)
    
    return {"history": history}


def save_search_history(username: str, data: dict):
    """
    Save search results to history file
    """
    os.makedirs("data", exist_ok=True)
    
    history_file = f"data/history_{username}.json"
    history = []
    
    if os.path.exists(history_file):
        with open(history_file, "r") as f:
            history = json.load(f)
    
    history.append(data)
    
    with open(history_file, "w") as f:
        json.dump(history, f, indent=2)


if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("🚀 Fresher Job Matcher - Starting")
    print("="*60)
    print("📂 Open browser: http://localhost:8000")
    print("="*60 + "\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
