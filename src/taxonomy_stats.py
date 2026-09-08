"""Taxonomy Inspector & Skill Count Profiler."""
import json

def get_total_taxonomy_count(skills_path: str = "data/skills.json") -> int:
    with open(skills_path, "r", encoding="utf-8") as f:
        skills = json.load(f)
    return sum(len(items) for items in skills.values())
