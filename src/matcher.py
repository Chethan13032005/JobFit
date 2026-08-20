from typing import Dict, Tuple, List
from src.models import Skill, ExtractedSkill
from src.preprocessing import normalize_text
from src.extractor import build_alias_regex

def match_skills_against_resume(
    extracted_jd_skills: Dict[str, Tuple[Skill, int]],
    resume_text: str
) -> List[ExtractedSkill]:
    """
    Compares extracted Job Description skills against the resume text.
    Uses boundary-safe phrase regexes to determine presence and frequency in the resume.
    """
    normalized_resume = normalize_text(resume_text)
    matched_results: List[ExtractedSkill] = []
    
    for skill_name, (skill, jd_count) in extracted_jd_skills.items():
        resume_count = 0
        for alias in skill.aliases:
            pattern = build_alias_regex(alias)
            matches = pattern.findall(normalized_resume)
            resume_count += len(matches)
            
        is_matched = resume_count > 0
        extracted_item = ExtractedSkill(
            skill=skill,
            count_in_jd=jd_count,
            count_in_resume=resume_count,
            is_matched=is_matched
        )
        matched_results.append(extracted_item)
        
    return matched_results
