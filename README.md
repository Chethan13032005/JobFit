# JobFit — Resume & Skill Gap Analyzer

> Enhanced implementation of **Learn Depth Track 1 — Project #56 Resume Keyword Analyzer**

---

## 📌 Problem Statement

Job seekers often struggle to determine how well their resume aligns with technical job descriptions. Manual keyword evaluation is time-consuming and can overlook important technical requirements or tool dependencies.

---

## 🎯 Objective

**JobFit** is a zero-cost Python application that compares resume content with the technical skills found in a job description. It provides a transparent keyword coverage report, categorizes detected skills, and prioritizes missing skills into actionable gap tiers with clear explanations.

---

## ✨ Features

- **Dual Input Modes:** Paste text directly or upload `.txt` files for both Resume and Job Description.
- **One-Click Demo Samples:** Pre-fill sample inputs to quickly test application features.
- **Clean Text Preprocessing:** Lowercasing, whitespace cleanup, and symbol normalization (`C++`, `C#`, `Node.js`, `REST API`).
- **Boundary-Aware Phrase Matching:** Prevents false subset matches (e.g., `Java` is not matched inside `JavaScript`, and `C` is not matched inside `C++`).
- **Transparent Match Score:** Calculates a clear keyword coverage percentage.
- **Category-Wise Coverage:** Groups skills into Programming Languages, Frameworks & Libraries, Databases, Core CS Concepts, and Tools & Cloud.
- **Explainable Skill Gap Prioritization:**
  - **High Priority:** Mentioned 2+ times in the Job Description.
  - **Medium Priority:** Core technical skill mentioned 1 time.
  - **Low Priority:** Auxiliary or tool skill mentioned 1 time.
- **Input Validation & Exception Handling:** Prevents crashes when processing empty or invalid inputs.

---

## 🛠️ Technologies Used

- Python 3.x
- Streamlit
- Pytest
- Python standard library (`re`, `json`, `os`, `dataclasses`, `typing`)

---

## ⚙️ Installation

1. Clone or download the repository and navigate to the project directory:
   ```bash
   cd jobfit-resume-skill-analyzer
   ```

2. Create and activate a virtual environment (optional):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 How to Run

Launch the Streamlit interface:
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🧪 How to Run Tests

Run the automated test suite:
```bash
python -m pytest tests/ -v
```

---

## 📁 Project Structure

```text
jobfit-resume-skill-analyzer/
│
├── app.py
├── requirements.txt
├── README.md
├── PROJECT_REPORT.pdf
├── TEST_CASES.md
├── .gitignore
│
├── src/
│   ├── __init__.py
│   ├── models.py
│   ├── validator.py
│   ├── file_handler.py
│   ├── preprocessing.py
│   ├── extractor.py
│   ├── matcher.py
│   ├── scoring.py
│   ├── skill_gap.py
│   └── analyzer.py
│
├── data/
│   └── skills.json
│
├── tests/
│   └── test_jobfit.py
│
└── screenshots/
    ├── 01_main_input_screen.png
    ├── 02_inputs_entered.png
    ├── 03_analysis_overview.png
    └── 04_category_and_skill_gaps.png

```

---

## 🔍 How It Works

1. **Input & Validation:** Ingests raw text or `.txt` files and checks for non-empty content.
2. **Text Normalization:** Cleans whitespace and normalizes Casing while preserving programming symbols.
3. **Keyword Extraction:** Matches job description text against canonical terms in `data/skills.json` using word-boundary regular expressions.
4. **Keyword Matching:** Compares extracted skills against the resume using boundary-aware matching rules.
5. **Scoring & Prioritization:** Computes overall coverage percentage, category metrics, and classifies missing skills into priority tiers with human-readable reasons.
6. **Results Presentation:** Displays summary metrics, category progress bars, and prioritized gap boxes in the Streamlit UI.

---

## 📊 Matching Algorithm & Formula

```text
Keyword Match Score (%) = (Matched JD Skills / Total Extracted JD Skills) × 100
```

> **Note:** This score represents keyword coverage and is not an official ATS score, recruitment probability, or hiring prediction.

---

## 🧪 Testing Results

14 automated tests pass successfully:
- Strong Match (>75% score)
- Partial Match
- Zero Match
- Empty and Whitespace Input Validation
- Missing or Unreadable File Validation
- Case and Multi-Word Phrase Normalization
- Boundary Protection: `Java` vs `JavaScript`
- Boundary Protection: `C` vs `C++`
- Skill Gap Prioritization & Explanations
- Alias Deduplication
- Special Characters (`C#`, `Node.js`, `CI/CD`, `React.js`)
- Unrecognized Job Description Skills
- Large Multi-Page Resume Handling
- Category Coverage Percentage Calculations

---

## 📸 Screenshots

| Screenshot | Description |
|------------|-------------|
| `01_main_input_screen.png` | JobFit input interface showing the application entry point and input fields. |
| `02_inputs_entered.png` | Resume and job description populated with sample data before analysis. |
| `03_analysis_overview.png` | Keyword matching results including the score, matched skills, missing skills, and total detected job-description skills. |
| `04_category_and_skill_gaps.png` | Category-wise coverage together with prioritized skill gaps and their explanations. |

---

## ⚠️ Limitations

- **Predefined Taxonomy Scope:** Relies on canonical skills configured in `data/skills.json`.
- **Keyword Coverage Focus:** Measures explicit keyword presence rather than semantic similarity or deep NLP understanding.
- **File Format Support:** Supports plain text and `.txt` files.

---

## 🔮 Future Improvements

- PDF and DOCX text extraction support.
- User-customizable taxonomy editor in the UI.
- Export analysis reports as Markdown or CSV.
