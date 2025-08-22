from typing import List, Set, Dict
from rapidfuzz import fuzz
import re

# Curated minimal skill database (extend as needed)
SKILL_DB = [
	"python", "java", "javascript", "typescript", "go", "c++", "c#", "sql", "nosql",
	"react", "reactjs", "react native", "next.js", "node.js", "express", "fastapi", "django", "flask",
	"docker", "kubernetes", "aws", "gcp", "azure", "terraform", "ansible",
	"spacy", "bert", "nlp", "transformers", "ml", "machine learning", "deep learning",
	"pandas", "numpy", "scikit-learn", "pytorch", "tensorflow",
	"redis", "kafka", "rabbitmq",
	"git", "github", "ci/cd", "linux",
]

NORMALIZATION_MAP = {
	"js": "javascript",
	"ts": "typescript",
	"tf": "tensorflow",
}


def normalize_token(token: str) -> str:
	n = token.strip().lower()
	return NORMALIZATION_MAP.get(n, n)


def tokenize(text: str) -> List[str]:
	# Basic tokenization; keep words and plus/hash/dot
	return re.findall(r"[a-zA-Z][a-zA-Z0-9+.#-]{1,}", text.lower())


def extract_skills(text: str, threshold: int = 90) -> Set[str]:
	"""Extract skills by fuzzy matching tokens and n-grams against SKILL_DB."""
	tokens = tokenize(text)
	candidates: Set[str] = set(tokens)
	# also look at bi-grams
	for i in range(len(tokens) - 1):
		candidates.add(tokens[i] + " " + tokens[i + 1])

	found: Set[str] = set()
	for cand in candidates:
		cand_norm = normalize_token(cand)
		for skill in SKILL_DB:
			if cand_norm == skill:
				found.add(skill)
				continue
			sim = fuzz.partial_ratio(cand_norm, skill)
			if sim >= threshold:
				found.add(skill)
	return found


def compare_skills(resume_skills: Set[str], jd_skills: Set[str]) -> Dict[str, Set[str]]:
	matched = resume_skills.intersection(jd_skills)
	missing = jd_skills.difference(resume_skills)
	extra = resume_skills.difference(jd_skills)
	return {
		"matched_skills": matched,
		"missing_skills": missing,
		"extra_skills": extra,
	}