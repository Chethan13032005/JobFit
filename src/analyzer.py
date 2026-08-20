from typing import List, Optional
from src.models import AnalysisResult, ExtractedSkill
from src.validator import validate_text
from src.preprocessing import normalize_text
from src.extractor import TaxonomyLoader, extract_skills_from_jd
from src.matcher import match_skills_against_resume
from src.scoring import calculate_match_score, calculate_category_breakdowns
from src.skill_gap import prioritize_skill_gaps

class ResumeAnalyzer:
    """
    Main orchestrator class for Project #56 — Resume Keyword Analyzer.
    Coordinates input validation, preprocessing, skill extraction, safe regex matching,
    scoring, category breakdowns, and explainable skill gap prioritization.
    """
    
    def __init__(self, taxonomy_path: Optional[str] = None):
        self.taxonomy_loader = TaxonomyLoader(json_path=taxonomy_path)
        self.taxonomy = self.taxonomy_loader.skills

    def analyze(self, resume_text: str, jd_text: str) -> AnalysisResult:
        """
        Executes complete analysis comparing resume text against job description text.
        Raises InputValidationError if inputs are empty or invalid.
        """
        # 1. Validate inputs
        clean_resume = validate_text(resume_text, "Resume text")
        clean_jd = validate_text(jd_text, "Job description text")
        
        # 2. Extract present skills from Job Description with frequency counts
        extracted_jd_skills = extract_skills_from_jd(clean_jd, self.taxonomy)
        
        if not extracted_jd_skills:
            # Handle case where no configured skills are found in the JD gracefully
            return AnalysisResult(
                total_jd_skills=0,
                matched_count=0,
                missing_count=0,
                keyword_match_score=0.0,
                matched_skills=[],
                missing_skills=[],
                category_breakdowns=[],
                high_priority_gaps=[],
                medium_priority_gaps=[],
                low_priority_gaps=[]
            )
            
        # 3. Safely match extracted JD skills against the Resume text
        extracted_skills: List[ExtractedSkill] = match_skills_against_resume(
            extracted_jd_skills=extracted_jd_skills,
            resume_text=clean_resume
        )
        
        # 4. Calculate overall Keyword Match Score
        score, matched_count, total_count = calculate_match_score(extracted_skills)
        missing_count = total_count - matched_count
        
        # 5. Partition matched skills
        matched_items = [item for item in extracted_skills if item.is_matched]
        matched_items.sort(key=lambda x: x.skill.name)
        
        # 6. Calculate category coverage breakdowns
        category_breakdowns = calculate_category_breakdowns(extracted_skills)
        
        # 7. Prioritize missing skills into explainable gap tiers
        all_gaps, high_gaps, medium_gaps, low_gaps = prioritize_skill_gaps(extracted_skills)
        
        return AnalysisResult(
            total_jd_skills=total_count,
            matched_count=matched_count,
            missing_count=missing_count,
            keyword_match_score=score,
            matched_skills=matched_items,
            missing_skills=all_gaps,
            category_breakdowns=category_breakdowns,
            high_priority_gaps=high_gaps,
            medium_priority_gaps=medium_gaps,
            low_priority_gaps=low_gaps
        )
