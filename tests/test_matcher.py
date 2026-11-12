"""Unit tests for boundary safe matcher."""
from src.matcher import extract_matched_skills

def test_c_plus_plus_matching():
    skills = ["C", "C++", "C#", "Java", "JavaScript"]
    text = "Experienced in C++ and JavaScript programming."
    matched = extract_matched_skills(text, skills)
    assert "C++" in matched
    assert "JavaScript" in matched
    assert "Java" not in matched
    assert "C" not in matched
