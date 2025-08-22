from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Dict, Any
import hashlib

from .services.parser import extract_text_from_resume, validate_file_type
from .services.skills import extract_skills, compare_skills
from .services.scoring import compute_ats_score
from .services.recommendations import recommend_courses, suggest_improvements
from .utils.cache import result_cache

app = FastAPI(title="DPR – AI Resume Analyzer", version="0.1.0")

app.add_middleware(	CORSMiddleware,	allow_origins=["*"],	allow_credentials=True,	allow_methods=["*"],	allow_headers=["*"]
)


@app.get("/api/health")
async def health() -> Dict[str, str]:
	return {"status": "ok"}


@app.post("/api/analyze")
async def analyze_resume(
	file: UploadFile = File(..., description="Resume file (.pdf or .docx)"),
	job_description: str = Form(..., description="Job description text"),
) -> JSONResponse:
	if not validate_file_type(file):
		raise HTTPException(status_code=400, detail="Only .pdf and .docx resume files are allowed.")

	# Read bytes for caching and parsing
	file_bytes: bytes = await file.read()
	if len(file_bytes) == 0:
		raise HTTPException(status_code=422, detail="Uploaded file is empty or corrupted.")

	cache_key = hashlib.sha256(file_bytes + job_description.encode("utf-8")).hexdigest()
	cached = result_cache.get(cache_key)
	if cached is not None:
		return JSONResponse(content=cached)

	try:
		resume_text = extract_text_from_resume(file.filename, file.content_type, file_bytes)
	except ValueError as parse_err:
		raise HTTPException(status_code=422, detail=str(parse_err))
	except Exception:
		raise HTTPException(status_code=500, detail="Failed to parse resume. Please try another file.")

	if len(resume_text.split()) < 50:
		raise HTTPException(status_code=422, detail="The uploaded file does not appear to be a valid resume.")

	resume_skills = extract_skills(resume_text)
	jd_skills = extract_skills(job_description)
	comparison = compare_skills(resume_skills, jd_skills)
	score = compute_ats_score(resume_text, job_description, comparison)
	courses = recommend_courses(comparison["missing_skills"]) 
	suggestions = suggest_improvements(resume_text, comparison)

	result: Dict[str, Any] = {
		"ats_score": score,
		"matched_skills": sorted(list(comparison["matched_skills"])),
		"missing_skills": sorted(list(comparison["missing_skills"])),
		"extra_skills": sorted(list(comparison["extra_skills"])),
		"course_recommendations": courses,
		"suggestions": suggestions,
	}

	result_cache.set(cache_key, result)
	return JSONResponse(content=result)