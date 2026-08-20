from typing import List, Tuple
from src.models import ExtractedSkill, SkillGap

def prioritize_skill_gaps(
    extracted_skills: List[ExtractedSkill]
) -> Tuple[List[SkillGap], List[SkillGap], List[SkillGap], List[SkillGap]]:
    """
    Identifies missing skills and classifies them into transparent, explainable priority tiers:
    - HIGH: Mentioned 2+ times in the Job Description.
    - MEDIUM: Core technical skill mentioned once.
    - LOW: Auxiliary/tool skill mentioned once.
    
    Returns (all_gaps, high_gaps, medium_gaps, low_gaps).
    """
    missing_items = [item for item in extracted_skills if not item.is_matched]
    
    all_gaps: List[SkillGap] = []
    high_gaps: List[SkillGap] = []
    medium_gaps: List[SkillGap] = []
    low_gaps: List[SkillGap] = []
    
    for item in missing_items:
        count = item.count_in_jd
        category = item.skill.category
        
        if count >= 2:
            priority = "HIGH"
            reason = f"Mentioned {count} times in the job description (frequently emphasized requirement)."
        elif item.skill.is_core_technical:
            priority = "MEDIUM"
            reason = f"Core technical skill in '{category}' (mentioned 1 time in job description)."
        else:
            priority = "LOW"
            reason = f"Auxiliary/tool skill in '{category}' (mentioned 1 time in job description)."
            
        gap_entry = SkillGap(
            skill=item.skill,
            count_in_jd=count,
            priority=priority,
            reason=reason
        )
        
        all_gaps.append(gap_entry)
        if priority == "HIGH":
            high_gaps.append(gap_entry)
        elif priority == "MEDIUM":
            medium_gaps.append(gap_entry)
        else:
            low_gaps.append(gap_entry)
            
    # Sort gaps within each bucket by JD frequency descending
    high_gaps.sort(key=lambda x: x.count_in_jd, reverse=True)
    medium_gaps.sort(key=lambda x: x.skill.name)
    low_gaps.sort(key=lambda x: x.skill.name)
    
    return all_gaps, high_gaps, medium_gaps, low_gaps
