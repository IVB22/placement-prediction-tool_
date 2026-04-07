from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple
from app.utils.skill_extractor import extract_resume_skills, normalize_text

def resume_ats_score(resume_text: str, target_skills: Optional[List[str]] = None) -> Dict[str, Any]:
    resume_text = resume_text or ""
    evidence_words = ["project", "internship", "built", "developed", "deployed", "impact", "achieved"]
    t = normalize_text(resume_text)
    evidence_bonus = sum(1 for w in evidence_words if w in t) * 2

    if target_skills:
        role_sk = set([normalize_text(x) for x in target_skills if x])
        res_sk = set([normalize_text(x) for x in extract_resume_skills(resume_text)])
        matched = sorted([s for s in role_sk if s in res_sk])
        missing = sorted([s for s in role_sk if s not in res_sk])
        raw = (len(matched) / max(1, len(role_sk))) * 100
        fit = int(round(min(100, 15 + raw * 0.85)))
        score = int(min(100, fit + evidence_bonus))
        return {"score": score, "matched_skills": matched[:25], "missing_skills": missing[:25]}

    skills = extract_resume_skills(resume_text)
    score = int(min(100, 25 + len(skills) * 6 + evidence_bonus))
    return {"score": score, "skills": skills[:25]}
