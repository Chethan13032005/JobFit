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
