from typing import Optional
from io import BytesIO

from pdfminer.high_level import extract_text as pdf_extract_text
from docx import Document

ALLOWED_CONTENT_TYPES = {
	"application/pdf": ".pdf",
	"application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
}


def validate_file_type(upload_file) -> bool:
	content_type = getattr(upload_file, "content_type", None)
	filename = getattr(upload_file, "filename", "")
	if content_type in ALLOWED_CONTENT_TYPES:
		return True
	# Fallback to extension check
	return filename.lower().endswith(('.pdf', '.docx'))


def extract_text_from_resume(filename: str, content_type: Optional[str], file_bytes: bytes) -> str:
	if content_type == "application/pdf" or filename.lower().endswith(".pdf"):
		return _extract_text_from_pdf(file_bytes)
	if content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document" or filename.lower().endswith(".docx"):
		return _extract_text_from_docx(file_bytes)
	raise ValueError("Unsupported file type. Only PDF and DOCX are supported.")


def _extract_text_from_pdf(file_bytes: bytes) -> str:
	try:
		bio = BytesIO(file_bytes)
		text = pdf_extract_text(bio)
		return text or ""
	except Exception as e:
		raise ValueError(f"Could not read PDF: {e}")


def _extract_text_from_docx(file_bytes: bytes) -> str:
	try:
		bio = BytesIO(file_bytes)
		doc = Document(bio)
		parts = [p.text for p in doc.paragraphs if p.text]
		return "\n".join(parts)
	except Exception as e:
		raise ValueError(f"Could not read DOCX: {e}")