import json
import os
import re
from typing import List, Dict, Tuple
from src.models import Skill
from src.preprocessing import normalize_text

class TaxonomyLoader:
    """Loads and manages the technical skill taxonomy from skills.json."""
    
    def __init__(self, json_path: str = None):
        if json_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            json_path = os.path.join(base_dir, "data", "skills.json")
        
        self.json_path = json_path
        self.skills: List[Skill] = []
        self.load_taxonomy()

    def load_taxonomy(self):
        """Reads skills.json and instantiates Skill dataclass objects."""
        if not os.path.exists(self.json_path):
            raise FileNotFoundError(f"Skills taxonomy file not found at: {self.json_path}")
            
        with open(self.json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        categories = data.get("categories", {})
        for cat_name, cat_info in categories.items():
            is_core = cat_info.get("is_core_technical", True)
            skill_list = cat_info.get("skills", [])
            for item in skill_list:
                skill = Skill(
                    name=item["name"],
                    category=cat_name,
                    aliases=item.get("aliases", [item["name"].lower()]),
                    is_core_technical=is_core
                )
                self.skills.append(skill)


def build_alias_regex(alias: str) -> re.Pattern:
    """
    Builds a boundary-safe regular expression pattern for a skill alias.
    Ensures safe matching for special characters like C++, C#, .NET, and prevents false sub-word matches.
    """
    escaped_alias = re.escape(alias.lower())
    
    # Handle specific language boundary edge cases
    if alias.lower() == "c":
        # 'c' must be surrounded by boundaries and NOT followed by + or #
        pattern_str = r'\bc\b(?![+#])'
    elif alias.lower() in ["c++", "cpp"]:
        pattern_str = r'(?:\bc\+\+|\bcpp\b)'
    elif alias.lower() in ["c#", "csharp"]:
        pattern_str = r'(?:\bc\#|\bcsharp\b)'
    elif alias.lower() in ["js", "ts", "py"]:
        # Short extension aliases must NOT be preceded by dot (e.g. node.js, react.js)
        pattern_str = rf'(?<![.\w])\b{escaped_alias}\b'
    else:
        # Standard word boundary pattern
        pattern_str = rf'\b{escaped_alias}\b'
        
    return re.compile(pattern_str, re.IGNORECASE)


def extract_skills_from_jd(jd_text: str, taxonomy: List[Skill]) -> Dict[str, Tuple[Skill, int]]:
    """
    Extracts all taxonomy skills present in the job description along with their frequency of occurrence.
    Returns dict mapping skill canonical name -> (Skill object, mention_count).
    """
    normalized_jd = normalize_text(jd_text)
    extracted: Dict[str, Tuple[Skill, int]] = {}
    
    for skill in taxonomy:
        total_mentions = 0
        for alias in skill.aliases:
            pattern = build_alias_regex(alias)
            matches = pattern.findall(normalized_jd)
            total_mentions += len(matches)
            
        if total_mentions > 0:
            extracted[skill.name] = (skill, total_mentions)
            
    return extracted
