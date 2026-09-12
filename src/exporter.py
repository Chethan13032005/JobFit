"""Report Exporter for JobFit Resume and Skill Gap Analysis."""
import json
import csv
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
