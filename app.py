import streamlit as st
from src.analyzer import ResumeAnalyzer
from src.validator import InputValidationError

# Page configuration
st.set_page_config(
    page_title="JobFit — Resume & Skill Gap Analyzer",
    page_icon="🎯",
    layout="wide"
)

# Custom CSS styling for clean presentation
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .badge-matched {
        background-color: #D1FAE5;
        color: #065F46;
        padding: 0.35rem 0.7rem;
        border-radius: 0.375rem;
        font-weight: 600;
        display: inline-block;
        margin: 0.25rem;
    }
    .badge-missing {
        background-color: #FEE2E2;
        color: #991B1B;
        padding: 0.35rem 0.7rem;
        border-radius: 0.375rem;
        font-weight: 600;
        display: inline-block;
        margin: 0.25rem;
    }
    .high-priority-box {
        border-left: 5px solid #EF4444;
        background-color: #FEF2F2;
        padding: 0.75rem 1rem;
        border-radius: 0.375rem;
        margin-bottom: 0.5rem;
    }
    .medium-priority-box {
        border-left: 5px solid #FFFBEB;
        border-left-color: #F59E0B;
        background-color: #FFFBEB;
        padding: 0.75rem 1rem;
        border-radius: 0.375rem;
        margin-bottom: 0.5rem;
    }
    .low-priority-box {
        border-left: 5px solid #3B82F6;
        background-color: #EFF6FF;
        padding: 0.75rem 1rem;
        border-radius: 0.375rem;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Sample Data Strings
SAMPLE_JD_TEXT = """Job Title: Senior Software Engineer (Python & Cloud)

Responsibilities:
- Design and build high-performance web applications using Python, FastAPI, and Django.
- Write efficient SQL queries and manage PostgreSQL databases.
- Develop clean REST API endpoints for web and mobile frontends.
- Use Docker for containerization and deploy microservices on AWS and Kubernetes.
- Apply strong Data Structures and Algorithms principles to optimize performance.
- Perform code reviews using Git and GitHub, adhering to clean OOP design practices.

Required Technical Skills:
- Python (Python 3.x experience required. Python clean code practices.)
- FastAPI or Django
- PostgreSQL and SQL
- Docker (Docker, Docker Compose, container management)
- AWS and Kubernetes
- REST API design
- Data Structures & Algorithms
- Git and Linux"""

SAMPLE_STRONG_RESUME = """Alex Developer
Email: alex@example.com | GitHub: github.com/alexdev

PROFESSIONAL SUMMARY
Backend Engineer with 3+ years of experience building scalable microservices and web APIs using Python, FastAPI, and PostgreSQL. Experienced with Docker, Git, REST API design, and Data Structures.

TECHNICAL SKILLS
- Programming Languages: Python, SQL
- Frameworks: FastAPI, Django
- Databases: PostgreSQL, Redis
- Core CS: Data Structures, Algorithms, OOP, REST API
- DevOps & Tools: Docker, Git, GitHub, Linux

WORK EXPERIENCE
Software Engineer | TechCorp
- Developed backend microservices using Python and FastAPI.
- Wrote optimized PostgreSQL SQL queries to handle over 1M daily API requests.
- Containerized services with Docker and set up CI/CD pipelines.
- Integrated REST API endpoints with frontend applications."""

SAMPLE_PARTIAL_RESUME = """Sam Frontend
Email: sam@example.com

SUMMARY
Frontend Engineer with experience in JavaScript, React, and CSS. Learning backend technologies.

SKILLS
- Languages: JavaScript, HTML, CSS, Java
- Frameworks: React, Express.js
- Tools: Git, Postman

EXPERIENCE
Frontend Developer
- Built responsive UI components with React and JavaScript.
- Used Git for version control."""

# Initialize Analyzer instance
@st.cache_resource
def get_analyzer():
    return ResumeAnalyzer()

analyzer = get_analyzer()

# Title & Subtitle
st.markdown('<div class="main-title">🎯 JobFit — Resume & Skill Gap Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Compare resume text against job descriptions and get a transparent keyword coverage report with explainable skill gaps.</div>', unsafe_allow_html=True)

# Sidebar controls
with st.sidebar:
    st.header("⚡ Quick Demo Samples")
    st.write("Load sample text directly into inputs:")
    
    col_s1, col_s2 = st.columns(2)
    if col_s1.button("Strong Match Sample"):
        st.session_state["resume_text_area"] = SAMPLE_STRONG_RESUME
        st.session_state["jd_text_area"] = SAMPLE_JD_TEXT
        st.rerun()
        
    if col_s2.button("Partial Match Sample"):
        st.session_state["resume_text_area"] = SAMPLE_PARTIAL_RESUME
        st.session_state["jd_text_area"] = SAMPLE_JD_TEXT
        st.rerun()
        
    st.markdown("---")
    st.markdown("### ℹ️ Analysis Pipeline")
    st.markdown("""
    - **Preprocessing:** Lowercasing, whitespace cleanup, and symbol normalization.
    - **Extraction:** Boundary-aware regex keyword extraction from Job Description.
    - **Matching:** Subset boundary protection (`Java` vs `JavaScript`, `C` vs `C++`).
    - **Coverage Score:** Transparent keyword match percentage.
    - **Prioritized Skill Gaps:**
      - **HIGH:** Mentioned $\\ge 2$ times in JD.
      - **MEDIUM:** Core technical skill mentioned 1 time.
      - **LOW:** Auxiliary/tool skill mentioned 1 time.
    """)

# Input Columns
col_res, col_jd = st.columns(2)

with col_res:
    st.subheader("📄 1. Resume Input")
    res_input_mode = st.radio("Input mode:", ["Paste Text", "Upload .txt File"], key="res_mode")
    
    resume_text = ""
    if res_input_mode == "Paste Text":
        resume_text = st.text_area(
            "Paste Resume Text here:",
            height=250,
            key="resume_text_area"
        )
    else:
        uploaded_res = st.file_uploader("Upload Resume (.txt)", type=["txt"], key="res_file")
        if uploaded_res is not None:
            resume_text = uploaded_res.read().decode("utf-8")

with col_jd:
    st.subheader("📋 2. Job Description Input")
    jd_input_mode = st.radio("Input mode:", ["Paste Text", "Upload .txt File"], key="jd_mode")
    
    jd_text = ""
    if jd_input_mode == "Paste Text":
        jd_text = st.text_area(
            "Paste Job Description Text here:",
            height=250,
            key="jd_text_area"
        )
    else:
        uploaded_jd = st.file_uploader("Upload Job Description (.txt)", type=["txt"], key="jd_file")
        if uploaded_jd is not None:
            jd_text = uploaded_jd.read().decode("utf-8")

st.markdown("---")
analyze_btn = st.button("🚀 Analyze Keyword Alignment", type="primary", use_container_width=True)

if analyze_btn:
    try:
        result = analyzer.analyze(resume_text, jd_text)
        
        if result.total_jd_skills == 0:
            st.warning("⚠️ No recognized technical keywords were found in the provided Job Description. Please check that the Job Description contains relevant technical requirements.")
        else:
            st.markdown("## 📊 Analysis Results")
            
            # Summary Metrics
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Keyword Match Score", f"{result.keyword_match_score}%")
            m2.metric("Matched Skills", result.matched_count)
            m3.metric("Missing Skills", result.missing_count)
            m4.metric("Total JD Keywords", result.total_jd_skills)
            
            # Score progress bar
            st.progress(result.keyword_match_score / 100.0)
            
            st.markdown("---")
            
            # Matched & Missing Skills
            col_match, col_miss = st.columns(2)
            
            with col_match:
                st.subheader(f"✓ Matched Skills ({result.matched_count})")
                if result.matched_skills:
                    for item in result.matched_skills:
                        st.markdown(f'<span class="badge-matched">✓ {item.skill.name} ({item.skill.category})</span>', unsafe_allow_html=True)
                else:
                    st.write("No matching skills found in resume.")
                    
            with col_miss:
                st.subheader(f"✗ Missing Skills ({result.missing_count})")
                if result.missing_skills:
                    for gap in result.missing_skills:
                        st.markdown(f'<span class="badge-missing">✗ {gap.skill.name} ({gap.skill.category})</span>', unsafe_allow_html=True)
                else:
                    st.success("🎉 Excellent coverage! No missing keywords detected.")
                    
            st.markdown("---")
            
            # Category Breakdown
            st.subheader("📁 Category Coverage Breakdown")
            cat_cols = st.columns(len(result.category_breakdowns) if result.category_breakdowns else 1)
            for i, cat in enumerate(result.category_breakdowns):
                with cat_cols[i % len(cat_cols)]:
                    st.markdown(f"**{cat.category_name}**")
                    st.write(f"{cat.matched_skills} / {cat.total_jd_skills} matched ({cat.coverage_percentage}%)")
                    st.progress(cat.coverage_percentage / 100.0)
                    
            st.markdown("---")
            
            # Skill Gap Prioritization
            st.subheader("🎯 Prioritized Skill Gaps & Action Plan")
            st.caption("Missing skills are prioritized using deterministic rules and explicit reasons.")
            
            # High Priority
            if result.high_priority_gaps:
                st.markdown("#### 🔴 High Priority Gaps")
                for gap in result.high_priority_gaps:
                    st.markdown(f"""
                    <div class="high-priority-box">
                        <strong>✗ {gap.skill.name}</strong> <em>({gap.skill.category})</em><br/>
                        <small>💡 <strong>Reason:</strong> {gap.reason}</small>
                    </div>
                    """, unsafe_allow_html=True)
                    
            # Medium Priority
            if result.medium_priority_gaps:
                st.markdown("#### 🟡 Medium Priority Gaps")
                for gap in result.medium_priority_gaps:
                    st.markdown(f"""
                    <div class="medium-priority-box">
                        <strong>✗ {gap.skill.name}</strong> <em>({gap.skill.category})</em><br/>
                        <small>💡 <strong>Reason:</strong> {gap.reason}</small>
                    </div>
                    """, unsafe_allow_html=True)
                    
            # Low Priority
            if result.low_priority_gaps:
                st.markdown("#### 🔵 Low Priority Gaps")
                for gap in result.low_priority_gaps:
                    st.markdown(f"""
                    <div class="low-priority-box">
                        <strong>✗ {gap.skill.name}</strong> <em>({gap.skill.category})</em><br/>
                        <small>💡 <strong>Reason:</strong> {gap.reason}</small>
                    </div>
                    """, unsafe_allow_html=True)
                    
            if not result.missing_skills:
                st.info("No skill gaps to prioritize. Great job!")

    except InputValidationError as e:
        st.error(f"❌ Input Validation Error: {str(e)}")
    except Exception as e:
        st.error(f"❌ An unexpected error occurred: {str(e)}")
