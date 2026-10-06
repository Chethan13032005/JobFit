"""HTML Standalone Report Generator for Hiring Managers."""
from typing import Dict, Any

def render_html_report(result: Dict[str, Any], candidate_name: str = "Candidate") -> str:
    score = result.get('overall_score', 0)
    badge_color = "#2ECC71" if score >= 75 else "#E67E22"
    matched_items = "".join([f"<li class='match'>{s}</li>" for s in result.get('matched_skills', [])])
    missing_items = "".join([f"<li class='gap'>{s}</li>" for s in result.get('missing_skills', [])])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>JobFit Evaluation - {candidate_name}</title>
<style>
  body {{ font-family: sans-serif; margin: 40px; background: #FAFAFA; color: #333; }}
  .card {{ background: white; padding: 30px; border-radius: 8px; max-width: 600px; margin: auto; }}
  .score-badge {{ display: inline-block; padding: 8px 16px; background: {badge_color}; color: white; border-radius: 20px; }}
  .match {{ color: #27AE60; }}
  .gap {{ color: #C0392B; }}
</style>
</head>
<body>
  <div class="card">
    <h2>JobFit Resume Evaluation</h2>
    <p>Candidate: <strong>{candidate_name}</strong></p>
    <div class="score-badge">{score}% Match</div>
    <h3>Verified Skills</h3>
    <ul>{matched_items or '<li>None</li>'}</ul>
    <h3>Targeted Skill Gaps</h3>
    <ul>{missing_items or '<li>None</li>'}</ul>
  </div>
</body>
</html>"""
