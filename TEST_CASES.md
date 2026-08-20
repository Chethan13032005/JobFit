# Test Cases Specification & Execution Log

**Project:** JobFit — Resume & Skill Gap Analyzer  
**Framework:** Pytest 9.1.1  

---

## Overview

This document details the test matrix and execution results for the 14 automated unit tests implemented in `tests/test_jobfit.py`.

---

## Summary Results

- **Total Test Cases:** 14
- **Passed:** 14
- **Failed:** 0
- **Pass Rate:** 100%

---

## Core Test Cases

### 1. Strong Match (`test_strong_match`)
- **Input:** Resume contains Python, FastAPI, PostgreSQL, Docker, and REST API. Job Description requires all 5 skills.
- **Expected Result:** 100.0% Keyword Match Score, 5 matched skills, 0 missing skills.
- **Status:** PASSED

### 2. Partial Match (`test_partial_match`)
- **Input:** Resume contains Python and SQL. Job Description requires Python, Java, SQL, Docker, Kubernetes, and AWS.
- **Expected Result:** 33.3% Keyword Match Score (2 matched, 4 missing).
- **Status:** PASSED

### 3. No Match (`test_zero_match`)
- **Input:** Resume with non-technical content. Job Description requires Python, Django, PostgreSQL, and Docker.
- **Expected Result:** 0.0% Keyword Match Score (0 matched, 4 missing). No crash.
- **Status:** PASSED

### 4. Empty Input Validation (`test_empty_input_validation`)
- **Input:** Empty or whitespace-only text strings.
- **Expected Result:** Raises `InputValidationError` without crashing the application.
- **Status:** PASSED

### 5. Invalid File Reading (`test_invalid_file_reading`)
- **Input:** Non-existent file path or non-txt extension file.
- **Expected Result:** Raises `InputValidationError` explaining unsupported or missing file.
- **Status:** PASSED

### 6. Case & Phrase Variation Normalization (`test_case_and_phrase_variations`)
- **Input:** `PYTHON`, `Machine Learning`, `REST API` in JD matched against lowercased variants in resume.
- **Expected Result:** Correct matching regardless of case differences.
- **Status:** PASSED

### 7. Word Boundary — Java vs JavaScript (`test_word_boundary_java_vs_javascript`)
- **Input:** Job Description requires `Java`. Resume contains only `JavaScript`.
- **Expected Result:** `Java` is marked as missing. `Java` is not falsely matched inside `JavaScript`.
- **Status:** PASSED

### 8. Word Boundary — C vs C++ (`test_word_boundary_c_vs_cpp`)
- **Input:** Job Description requires `C`. Resume contains only `C++`.
- **Expected Result:** `C` is marked as missing. `C` is not falsely matched inside `C++`.
- **Status:** PASSED

### 9. Skill Gap Prioritization & Explanations (`test_skill_gap_prioritization_and_reasons`)
- **Input:** `Docker` mentioned 3 times in JD; `Python` (core technical) mentioned 1 time; `Jira` (auxiliary tool) mentioned 1 time.
- **Expected Result:** `Docker` -> High Priority; `Python` -> Medium Priority; `Jira` -> Low Priority.
- **Status:** PASSED

### 10. Alias Deduplication (`test_duplicate_aliases_count_unique_canonical_skill`)
- **Input:** Job Description contains `Python`, `Py`, `Python 3`.
- **Expected Result:** Counted as 1 unique canonical skill with aggregate mention frequency.
- **Status:** PASSED

### 11. Special Symbols (`test_special_symbols_csharp_dotnet_cicd`)
- **Input:** `C#`, `Node.js`, `CI/CD`, `React.js`.
- **Expected Result:** Correct matching for terms with symbols without regex syntax errors.
- **Status:** PASSED

### 12. No Recognized Skills in Job Description (`test_no_recognized_skills_in_jd`)
- **Input:** Job Description containing non-technical prose.
- **Expected Result:** Returns 0 detected skills and 0.0% score cleanly.
- **Status:** PASSED

### 13. Large Resume Text (`test_large_resume_text`)
- **Input:** 500-paragraph multi-page resume text.
- **Expected Result:** Fast processing under 0.1s with accurate skill extraction.
- **Status:** PASSED

### 14. Category Coverage Math (`test_category_breakdown_percentages`)
- **Input:** Job Description with 2 Programming Languages and 2 Tools. Resume matches 1 Language and 0 Tools.
- **Expected Result:** Languages category = 50.0%; Tools category = 0.0%.
- **Status:** PASSED

---

## Execution Command

```bash
python -m pytest tests/ -v
```
