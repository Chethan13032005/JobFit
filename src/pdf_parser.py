"""PDF Document Parser for Resume and Job Description Extraction."""
import re
from typing import Dict, Any, Optional

def clean_extracted_text(raw_text: str) -> str:
    """Normalize whitespace and remove non-printable characters."""
    if not raw_text:
        return ""
    text = re.sub(r'\s+', ' ', raw_text)
    return text.strip()

def extract_text_from_pdf(file_path: str) -> str:
    """Extract clean text content from PDF file."""
    try:
        import pypdf
        reader = pypdf.PdfReader(file_path)
        pages_text = [page.extract_text() or "" for page in reader.pages]
        return clean_extracted_text(" ".join(pages_text))
    except ImportError:
        with open(file_path, "rb") as f:
            content = f.read().decode("latin-1", errors="ignore")
            return clean_extracted_text(content)

def clean_pdf_artifacts(text: str) -> str:
    """Strip common header, footer, page number patterns."""
    text = re.sub(r'Page \d+ of \d+', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\b(Confidential|Resume|Curriculum Vitae)\b', '', text, flags=re.IGNORECASE)
    return clean_extracted_text(text)

def extract_pdf_metadata(file_path: str) -> Dict[str, Any]:
    """Extract author, title, creation date metadata."""
    try:
        import pypdf
        reader = pypdf.PdfReader(file_path)
        meta = reader.metadata or {}
        return {
            "author": meta.get("/Author", ""),
            "creator": meta.get("/Creator", ""),
            "pages": len(reader.pages)
        }
    except Exception:
        return {"author": "", "creator": "", "pages": 1}
