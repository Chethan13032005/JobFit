"""DOCX Document Parser for Microsoft Word Resumes."""
import re
from typing import List, Dict, Any

def clean_docx_text(raw: str) -> str:
    """Normalize paragraph spaces and line breaks."""
    if not raw:
        return ""
    return re.sub(r'\s+', ' ', raw).strip()

def extract_text_from_docx(file_path: str) -> str:
    """Extract paragraph text from .docx file."""
    try:
        import docx
        doc = docx.Document(file_path)
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        return clean_docx_text(" ".join(paragraphs))
    except ImportError:
        with open(file_path, "rb") as f:
            content = f.read().decode("utf-8", errors="ignore")
            chunks = re.findall(r'<w:t[^>]*>(.*?)</w:t>', content)
            return clean_docx_text(" ".join(chunks) if chunks else content)

def extract_tables_from_docx(file_path: str) -> List[List[str]]:
    """Extract tabular grid cells from docx document."""
    try:
        import docx
        doc = docx.Document(file_path)
        tables_data = []
        for table in doc.tables:
            for row in table.rows:
                row_cells = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                if row_cells:
                    tables_data.append(row_cells)
        return tables_data
    except Exception:
        return []
