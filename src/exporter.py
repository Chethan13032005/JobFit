"""Report Exporter for JobFit Resume and Skill Gap Analysis."""
import json
import csv
import io
from typing import Dict, Any, List

def format_skill_gap_summary(matched: List[str], missing: List[str]) -> str:
    """Generate bullet points for matched vs missing competencies."""
    lines = ["### Matched Skills:"]
    lines.extend([f"- {s}" for s in matched] if matched else ["- None"])
    lines.append("\n### Missing Skills (Gaps):")
    lines.extend([f"- {s}" for s in missing] if missing else ["- None"])
    return "\n".join(lines)

def generate_markdown_report(result: Dict[str, Any]) -> str:
    """Generate professional Markdown formatted match report."""
    score = result.get('overall_score', 0)
    matched = result.get('matched_skills', [])
    missing = result.get('missing_skills', [])
    
    report = [
        "# JobFit Resume Match Report",
        f"**Overall Compatibility Score:** {score}%",
        f"**Status:** {'Recommended' if score >= 75 else 'Skill Gap Identified'}",
        "---",
        format_skill_gap_summary(matched, missing)
    ]
    return "\n\n".join(report)

def generate_csv_report(result: Dict[str, Any]) -> str:
    """Generate CSV string detailing skill matches and gaps."""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Category", "Skill", "Status"])
    
    for s in result.get('matched_skills', []):
        writer.writerow(["Competency", s, "MATCHED"])
    for s in result.get('missing_skills', []):
        writer.writerow(["Competency", s, "MISSING"])
        
    return output.getvalue()

def export_recommendation_matrix(missing_skills: List[str]) -> List[Dict[str, str]]:
    """Map missing skills to recommended learning resources."""
    catalog = {
        "Docker": "Complete Docker Mastery on Udemy / Official Docs",
        "Kubernetes": "Certified Kubernetes Administrator (CKA) Course",
        "AWS": "AWS Certified Solutions Architect Associate Prep",
        "PyTorch": "Deep Learning with PyTorch: A 60 Minute Blitz",
        "Terraform": "HashiCorp Certified Terraform Associate Guide",
        "RAG": "Building Production RAG Systems with LangChain & Vector DBs"
    }
    return [
        {"skill": s, "recommended_course": catalog.get(s, f"Fundamentals of {s} on Coursera")}
        for s in missing_skills
    ]
