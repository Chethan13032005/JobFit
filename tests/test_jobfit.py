import os
import pytest
from src.analyzer import ResumeAnalyzer
from src.validator import InputValidationError
from src.file_handler import read_txt_file

@pytest.fixture
def analyzer():
    """Provides a fresh instance of ResumeAnalyzer."""
    return ResumeAnalyzer()

def test_strong_match(analyzer):
    """Test Case 1: Strong Match - Resume contains most JD skills."""
    jd_text = "Looking for a Python developer with FastAPI, PostgreSQL, Docker, and REST API experience."
    resume_text = "Software Engineer skilled in Python, FastAPI, PostgreSQL, Docker, REST API, Git, and Linux."
    
    result = analyzer.analyze(resume_text, jd_text)
    
    assert result.keyword_match_score == 100.0
    assert result.matched_count == 5
    assert result.missing_count == 0
    assert len(result.missing_skills) == 0

def test_partial_match(analyzer):
    """Test Case 2: Partial Match - Resume contains some JD skills."""
    jd_text = "Required: Python, Java, SQL, Docker, Kubernetes, AWS."
    resume_text = "Developer with experience in Python, SQL, and Git."
    
    result = analyzer.analyze(resume_text, jd_text)
    
    assert result.matched_count == 2  # Python, SQL
    assert result.missing_count == 4  # Java, Docker, Kubernetes, AWS
    assert result.keyword_match_score == round((2 / 6) * 100.0, 1)
    
    matched_names = [item.skill.name for item in result.matched_skills]
    assert "Python" in matched_names
    assert "SQL" in matched_names

def test_zero_match(analyzer):
    """Test Case 3: No Match - Resume has none of the JD skills."""
    jd_text = "Looking for Python, Django, PostgreSQL, Docker."
    resume_text = "Cook and manager with extensive customer service experience."
    
    result = analyzer.analyze(resume_text, jd_text)
    
    assert result.keyword_match_score == 0.0
    assert result.matched_count == 0
    assert result.missing_count == 4

def test_empty_input_validation(analyzer):
    """Test Case 4: Empty Input - Empty or whitespace inputs raise validation errors."""
    with pytest.raises(InputValidationError):
        analyzer.analyze("", "Python developer required")
        
    with pytest.raises(InputValidationError):
        analyzer.analyze("Python developer resume", "   ")

def test_invalid_file_reading():
    """Test Case 5: Invalid file reading raises InputValidationError."""
    with pytest.raises(InputValidationError):
        read_txt_file("non_existent_file.txt")
        
    with pytest.raises(InputValidationError):
        read_txt_file(__file__)  # .py file instead of .txt

def test_case_and_phrase_variations(analyzer):
    """Test Case 6: Case & Phrase Variations - Matching handles uppercase/lowercase and multi-word terms."""
    jd_text = "We require PYTHON, Machine Learning, and REST API."
    resume_text = "Built machine learning pipelines using python and rest api."
    
    result = analyzer.analyze(resume_text, jd_text)
    
    assert result.matched_count == 3
    assert result.keyword_match_score == 100.0

def test_word_boundary_java_vs_javascript(analyzer):
    """Test Case 7: Boundary Protection - Java must NOT match when resume only contains JavaScript."""
    jd_text = "Required: Java developer."
    resume_text = "Experienced JavaScript developer working with React and Node.js."
    
    result = analyzer.analyze(resume_text, jd_text)
    
    assert result.matched_count == 0
    assert result.missing_count == 1
    assert result.missing_skills[0].skill.name == "Java"

def test_word_boundary_c_vs_cpp(analyzer):
    """Test Case 8: Boundary Protection - C must NOT match when resume only contains C++."""
    jd_text = "Required: C programming language expert."
    resume_text = "Proficient in C++ and Python."
    
    result = analyzer.analyze(resume_text, jd_text)
    
    assert result.matched_count == 0
    assert result.missing_count == 1
    assert result.missing_skills[0].skill.name == "C"

def test_skill_gap_prioritization_and_reasons(analyzer):
    """Test Case 9: Skill Gap Prioritization - High (2+ mentions), Medium (Core), Low (Auxiliary)."""
    jd_text = "Docker is required. Docker containerization skills. We also need Python and Jira."
    resume_text = "Software developer with no cloud or devops skills."
    
    result = analyzer.analyze(resume_text, jd_text)
    
    high_names = [g.skill.name for g in result.high_priority_gaps]
    medium_names = [g.skill.name for g in result.medium_priority_gaps]
    low_names = [g.skill.name for g in result.low_priority_gaps]
    
    assert "Docker" in high_names
    assert "Python" in medium_names
    assert "Jira" in low_names
    
    docker_gap = next(g for g in result.high_priority_gaps if g.skill.name == "Docker")
    assert f"Mentioned {docker_gap.count_in_jd} times" in docker_gap.reason
    assert docker_gap.count_in_jd >= 2

def test_duplicate_aliases_count_unique_canonical_skill(analyzer):
    """Test Case 10: Deduplication - Multiple aliases for same skill count as 1 unique skill."""
    jd_text = "Seeking a Python, Py, Python 3 developer."
    resume_text = "Python developer."
    
    result = analyzer.analyze(resume_text, jd_text)
    
    assert result.total_jd_skills == 1
    assert result.matched_skills[0].skill.name == "Python"
    assert result.matched_skills[0].count_in_jd >= 2

def test_special_symbols_csharp_dotnet_cicd(analyzer):
    """Test Case 11: Special Characters - C#, Node.js, CI/CD, React.js match cleanly."""
    jd_text = "Required: C#, Node.js, CI/CD, and React.js."
    resume_text = "Skilled in C#, Node.js, CI/CD, React.js."
    
    result = analyzer.analyze(resume_text, jd_text)
    
    assert result.keyword_match_score == 100.0
    assert result.matched_count == 4

def test_no_recognized_skills_in_jd(analyzer):
    """Test Case 12: Prose JD without taxonomy skills handles gracefully without crash."""
    jd_text = "We are seeking an enthusiastic team player with strong communication skills."
    resume_text = "Hardworking individual with strong work ethic."
    
    result = analyzer.analyze(resume_text, jd_text)
    
    assert result.total_jd_skills == 0
    assert result.matched_count == 0
    assert result.keyword_match_score == 0.0

def test_large_resume_text(analyzer):
    """Test Case 13: Large Text Handling - Performs quickly on long multi-page resumes."""
    jd_text = "Python, SQL, Docker, AWS, React, Data Structures."
    long_resume = "Experienced software engineer. " + ("Python developer. SQL database expert. " * 500)
    
    result = analyzer.analyze(long_resume, jd_text)
    
    assert result.matched_count == 2
    assert "Python" in [s.skill.name for s in result.matched_skills]

def test_category_breakdown_percentages(analyzer):
    """Test Case 14: Category Math - Computes per-category coverage percentage accurately."""
    jd_text = "Required: Python, Java, Docker, AWS."  # 2 Languages, 2 Tools & Cloud
    resume_text = "Python expert."                     # 1 Language matched (50%), 0 Tools (0%)
    
    result = analyzer.analyze(resume_text, jd_text)
    
    lang_cat = next(c for c in result.category_breakdowns if c.category_name == "Programming Languages")
    tool_cat = next(c for c in result.category_breakdowns if c.category_name == "Tools & Cloud")
    
    assert lang_cat.total_jd_skills == 2
    assert lang_cat.matched_skills == 1
    assert lang_cat.coverage_percentage == 50.0
    
    assert tool_cat.total_jd_skills == 2
    assert tool_cat.matched_skills == 0
    assert tool_cat.coverage_percentage == 0.0


def test_clean_pdf_artifacts():
    from src.pdf_parser import clean_pdf_artifacts
    dirty = "Page 1 of 5 Resume John Doe Confidential Software Engineer"
    cleaned = clean_pdf_artifacts(dirty)
    assert "Page 1 of 5" not in cleaned
    assert "Confidential" not in cleaned
    assert "John Doe" in cleaned