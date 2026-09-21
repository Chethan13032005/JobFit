"""Weighted Domain Scoring for Precise Technical Job Matching."""
from typing import Dict, List, Any

CATEGORY_WEIGHTS = {
    'languages': 0.25,
    'frameworks': 0.20,
    'cloud_aws': 0.15,
    'devops_containers': 0.15,
    'devops_orchestration': 0.15,
    'ai_rag_vectors': 0.10
}

def calculate_weighted_match(matched_by_cat: Dict[str, List[str]], required_by_cat: Dict[str, List[str]]) -> Dict[str, Any]:
    category_scores = {}
    total_weighted = 0.0
    total_weight_applied = 0.0

    for cat, req_skills in required_by_cat.items():
        if not req_skills:
            continue
        weight = CATEGORY_WEIGHTS.get(cat, 0.10)
        matched_count = len(matched_by_cat.get(cat, []))
        cat_ratio = min(1.0, matched_count / len(req_skills))
        category_scores[cat] = round(cat_ratio * 100, 1)
        total_weighted += cat_ratio * weight
        total_weight_applied += weight

    overall = round((total_weighted / total_weight_applied) * 100, 1) if total_weight_applied > 0 else 0
    return {
        'overall_weighted_score': overall,
        'breakdown': category_scores
    }
