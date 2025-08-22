from typing import Dict, Set
from rapidfuzz import fuzz


def compute_ats_score(resume_text: str, jd_text: str, comparison: Dict[str, Set[str]]) -> int:
	"""Compute a simple ATS score 0-100.
	- 60% weight: skill overlap
	- 40% weight: text similarity (fuzzy)
	"""
	jd_skill_count = max(1, len(comparison["matched_skills"]) + len(comparison["missing_skills"]))
	skill_overlap_ratio = len(comparison["matched_skills"]) / jd_skill_count
	text_similarity = fuzz.token_set_ratio(resume_text, jd_text) / 100.0

	score = int(round(60 * skill_overlap_ratio + 40 * text_similarity))
	return max(0, min(100, score))