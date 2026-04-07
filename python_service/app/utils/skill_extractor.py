import re
from typing import List, Set

_CURATED = [
    "python","java","javascript","typescript","react","node","flask","django","fastapi",
    "sql","mysql","postgresql","mongodb","redis","docker","kubernetes","aws","azure","gcp",
    "git","linux","pandas","numpy","scikit-learn","machine learning","deep learning",
    "data analysis","power bi","tableau","excel","dsa","system design","rest api","graphql",
    "html","css","tailwind","nextjs","express"
]

def normalize_text(s: str) -> str:
    s = (s or "").lower()
    s = re.sub(r"[^a-z0-9+\s#.-]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def extract_resume_skills(resume_text: str) -> List[str]:
    t = normalize_text(resume_text)
    found: Set[str] = set()
    for kw in _CURATED:
        if normalize_text(kw) in t:
            found.add(kw)
    return sorted(found)

def parse_skill_list(skill_str: str) -> List[str]:
    s = (skill_str or "").replace("|", ",")
    parts = [p.strip().lower() for p in s.split(",")]
    parts = [p for p in parts if p and len(p) <= 80]
    return sorted(set(parts))
