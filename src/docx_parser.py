"""DOCX Document Parser for Microsoft Word Resumes."""
import re
from typing import List, Dict, Any

def clean_docx_text(raw: str) -> str:
    """Normalize paragraph spaces and line breaks."""
    if not raw:
        return ""
    return re.sub(r'\s+', ' ', raw).strip()
