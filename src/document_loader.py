"""Universal Document Loader for Resumes and Job Descriptions."""
import os
from src.pdf_parser import extract_text_from_pdf
from src.docx_parser import extract_text_from_docx

class UniversalDocumentLoader:
    SUPPORTED_EXTENSIONS = {'.pdf', '.docx', '.txt'}

    @classmethod
    def load_document_text(cls, file_path: str) -> str:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Resume document not found at: {file_path}")
        _, ext = os.path.splitext(file_path.lower())
        if ext == '.pdf':
            return extract_text_from_pdf(file_path)
        elif ext == '.docx':
            return extract_text_from_docx(file_path)
        elif ext == '.txt':
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read().strip()
        else:
            raise ValueError(f"Unsupported format '{ext}'.")
