from typing import List, Tuple, Dict
from src.models import ExtractedSkill, CategoryCoverage

def calculate_match_score(
    extracted_skills: List[ExtractedSkill]
) -> Tuple[float, int, int]:
    """
    Calculates overall Keyword Match Score percentage and returns (score, matched_count, total_count).
    Formula: (Matched JD Skills / Total JD Skills) * 100
    """
    total_jd_skills = len(extracted_skills)
    if total_jd_skills == 0:
        return 0.0, 0, 0
        
    matched_count = sum(1 for item in extracted_skills if item.is_matched)
    score = round((matched_count / total_jd_skills) * 100.0, 1)
    
    return score, matched_count, total_jd_skills


def calculate_category_breakdowns(
    extracted_skills: List[ExtractedSkill]
) -> List[CategoryCoverage]:
    """
    Computes per-category keyword coverage percentages.
    """
    categories: Dict[str, Dict[str, int]] = {}
    
    for item in extracted_skills:
        cat_name = item.skill.category
        if cat_name not in categories:
            categories[cat_name] = {"total": 0, "matched": 0}
            
        categories[cat_name]["total"] += 1
        if item.is_matched:
            categories[cat_name]["matched"] += 1
            
    breakdowns: List[CategoryCoverage] = []
    for cat_name, metrics in categories.items():
        total = metrics["total"]
        matched = metrics["matched"]
        percentage = round((matched / total) * 100.0, 1) if total > 0 else 0.0
        
        breakdowns.append(
            CategoryCoverage(
                category_name=cat_name,
                total_jd_skills=total,
                matched_skills=matched,
                coverage_percentage=percentage
            )
        )
        
    # Sort categories alphabetically
    breakdowns.sort(key=lambda x: x.category_name)
    return breakdowns
