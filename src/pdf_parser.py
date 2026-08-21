"""PDF Document Parser for Resume and Job Description Extraction."""
import re
from typing import Dict, Any, Optional

def clean_extracted_text(raw_text: str) -> str:
    """Normalize whitespace and remove non-printable characters."""
    if not raw_text:
        return ""
    text = re.sub(r'\s+', ' ', raw_text)
    return text.strip()
