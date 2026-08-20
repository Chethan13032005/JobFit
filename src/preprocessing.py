import re

def normalize_text(text: str) -> str:
    """
    Normalizes text for robust keyword matching:
    1. Converts text to lowercase.
    2. Normalizes multiple spaces, tabs, and newlines into a single space.
    3. Retains technical characters (+, #, ., /, -) essential for terms like C++, C#, Node.js, CI/CD.
    """
    if not text:
        return ""
    
    # 1. Lowercase
    normalized = text.lower()
    
    # 2. Replace carriage returns/newlines with space
    normalized = re.sub(r'[\r\n\t]+', ' ', normalized)
    
    # 3. Normalize multiple whitespace into single space
    normalized = re.sub(r'\s+', ' ', normalized)
    
    return normalized.strip()

def prepare_text_for_matching(text: str) -> str:
    """
    Prepares text by adding leading/trailing spaces to ensure boundary regex matches safely.
    """
    normalized = normalize_text(text)
    return f" {normalized} "
