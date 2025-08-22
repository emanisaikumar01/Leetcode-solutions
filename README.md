## DPR – AI Resume Analyzer

A cloud-native platform to analyze resumes against job descriptions, returning ATS score, skill gaps, course recommendations, and actionable suggestions.

### Features
- Upload resume (.pdf/.docx) with strict validation
- Paste job description
- AI-lite analysis: skill extraction, matching, ATS score, recommendations
- Results UI with score meter, missing skills, suggestions
- "Analyse Another Resume" flow without page reload

### Tech Stack
- Backend: FastAPI (Python)
- Frontend: React + Vite + Tailwind + Recharts
- Packaging: Docker + docker-compose

### Quickstart (Docker)
```bash
cd /workspace
docker compose up --build -d
# Frontend: http://localhost:5173
# Backend:  http://localhost:8000/api/health
```

### Local Dev (Backend)
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Local Dev (Frontend)
```bash
cd frontend
npm install
npm run dev
# Vite dev server at http://localhost:5173
```

### API
- POST `/api/analyze`
  - form-data: `file` (.pdf/.docx), `job_description` (string)
  - returns: `{ ats_score, matched_skills[], missing_skills[], extra_skills[], course_recommendations[], suggestions[] }`

### Notes on Scalability
- Stateless backend with simple in-memory TTL cache (plug Redis later)
- Split services for NLP, scoring in production
- Add API Gateway, CDN, and observability (Prometheus/Grafana) as next steps

### Security & Validation
- Only `.pdf`/`.docx` files accepted
- Size limit (frontend) and content sanity checks
- Graceful error messages surfaced in UI

### License
MIT