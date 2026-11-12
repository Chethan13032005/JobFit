"""Boundary-Safe Regex Matching Engine."""
import re
from typing import List, Set

def extract_matched_skills(text: str, skill_catalog: List[str]) -> List[str]:
    matched: Set[str] = set()
    for skill in skill_catalog:
        escaped = re.escape(skill)
        pattern = rf'(?<![a-zA-Z0-9]){escaped}(?![a-zA-Z0-9])'
        if re.search(pattern, text, flags=re.IGNORECASE):
            matched.add(skill)
    return sorted(list(matched))
