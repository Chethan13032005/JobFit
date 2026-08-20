from dataclasses import dataclass, field
from typing import List

@dataclass
class Skill:
    """Represents a canonical technical skill from the taxonomy database."""
    name: str
    category: str
    aliases: List[str]
    is_core_technical: bool = True

@dataclass
class ExtractedSkill:
    """Represents a skill extracted from the job description and checked against the resume."""
    skill: Skill
    count_in_jd: int
    count_in_resume: int
    is_matched: bool

@dataclass
class SkillGap:
    """Represents a missing skill prioritized into actionable gap tiers with an explainable reason."""
    skill: Skill
    count_in_jd: int
    priority: str  # "HIGH", "MEDIUM", or "LOW"
    reason: str

@dataclass
class CategoryCoverage:
    """Represents coverage percentage and metrics for a specific skill category."""
    category_name: str
    total_jd_skills: int
    matched_skills: int
    coverage_percentage: float

@dataclass
class AnalysisResult:
    """Complete results of comparing resume text against job description text."""
    total_jd_skills: int
    matched_count: int
    missing_count: int
    keyword_match_score: float
    matched_skills: List[ExtractedSkill] = field(default_factory=list)
    missing_skills: List[SkillGap] = field(default_factory=list)
    category_breakdowns: List[CategoryCoverage] = field(default_factory=list)
    high_priority_gaps: List[SkillGap] = field(default_factory=list)
    medium_priority_gaps: List[SkillGap] = field(default_factory=list)
    low_priority_gaps: List[SkillGap] = field(default_factory=list)
