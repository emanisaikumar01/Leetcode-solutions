from typing import List, Dict, Set
from urllib.parse import quote_plus


def recommend_courses(missing_skills: Set[str]) -> List[Dict[str, str]]:
	courses: List[Dict[str, str]] = []
	for skill in sorted(missing_skills):
		query = quote_plus(skill + " course")
		courses.append({
			"skill": skill,
			"coursera": f"https://www.coursera.org/search?query={query}",
			"udemy": f"https://www.udemy.com/courses/search/?q={query}",
			"nptel": f"https://nptel.ac.in/courses?search={query}",
		})
	return courses


def suggest_improvements(resume_text, comparison: Dict[str, Set[str]]) -> List[str]:
	suggestions: List[str] = []
	if len(comparison["missing_skills"]) > 0:
		suggestions.append("Add concrete projects or experience that demonstrate missing key skills.")
	if len(comparison["matched_skills"]) < 5:
		suggestions.append("Highlight core competencies in a dedicated 'Skills' section for better ATS parsing.")
	if len(resume_text) < 1500:
		suggestions.append("Expand work experience with measurable impact, metrics, and relevant keywords.")
	if "education" not in resume_text.lower():
		suggestions.append("Include an Education section with degree, institution, and graduation year.")
	return suggestions