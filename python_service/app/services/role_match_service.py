from __future__ import annotations
from typing import Any, Dict, List, Tuple, Optional

import numpy as np
import pandas as pd
from rapidfuzz import fuzz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.config.settings import Settings
from app.utils.skill_extractor import parse_skill_list, normalize_text
from app.services.resume_score_service import resume_ats_score

_jobs_df: Optional[pd.DataFrame] = None
_vectorizer: Optional[TfidfVectorizer] = None
_job_matrix = None

def _load_jobs() -> pd.DataFrame:
    global _jobs_df, _vectorizer, _job_matrix
    if _jobs_df is not None:
        return _jobs_df
    df = pd.read_csv(Settings.JOBS_CSV_PATH)
    # normalize expected columns
    # required: company, title; optional: skills, description
    # allow common alternatives
    def pick(cands):
        for c in cands:
            if c in df.columns:
                return c
        return None

    c_company = pick(["company","Company","company_name"])
    c_title = pick(["title","job_title","Title"])
    c_skills = pick(["skills","Skills","skill_list","required_skills"])
    c_desc = pick(["description","job_description","Description"])

    if not (c_company and c_title):
        raise ValueError("jobs_and_skills.csv must contain company and title columns (company/title).")

    df["_company"] = df[c_company].astype(str).fillna("")
    df["_title"] = df[c_title].astype(str).fillna("")
    df["_skills"] = df[c_skills].astype(str).fillna("") if c_skills else ""
    df["_desc"] = df[c_desc].astype(str).fillna("") if c_desc else ""
    df["_role_text"] = (df["_title"] + " " + df["_skills"] + " " + df["_desc"]).fillna("")

    _jobs_df = df
    _vectorizer = TfidfVectorizer(stop_words="english", max_features=30000)
    _job_matrix = _vectorizer.fit_transform(df["_role_text"].astype(str))
    return _jobs_df

def _recommend_by_resume(resume_text: str, top_k: int = 50) -> Tuple[List[int], List[float]]:
    df = _load_jobs()
    q = _vectorizer.transform([resume_text or ""])
    sims = cosine_similarity(q, _job_matrix)[0]
    idx = np.argsort(-sims)[:top_k]
    return idx.tolist(), sims[idx].tolist()

def _find_by_company_role(company: str, role: str, top_k: int = 10) -> List[int]:
    df = _load_jobs()
    cn = normalize_text(company)
    rn = normalize_text(role)
    scored = []
    for i, r in df.iterrows():
        c = normalize_text(r["_company"])
        t = normalize_text(r["_title"])
        cs = fuzz.partial_ratio(cn, c) if cn else 0
        ts = fuzz.partial_ratio(rn, t) if rn else 0
        total = 0.55 * ts + 0.45 * cs
        scored.append((total, i))
    scored.sort(reverse=True, key=lambda x: x[0])
    return [i for _, i in scored[:top_k]]

def _find_by_role(role: str, top_k: int = 80) -> List[int]:
    df = _load_jobs()
    rn = normalize_text(role)
    scored = []
    for i, r in df.iterrows():
        t = normalize_text(r["_title"])
        ts = fuzz.partial_ratio(rn, t)
        scored.append((ts, i))
    scored.sort(reverse=True, key=lambda x: x[0])
    return [i for _, i in scored[:top_k]]

def mode_a(company: str, role: str, resume_text: str, placement_prob: float) -> Dict[str, Any]:
    df = _load_jobs()
    ids = _find_by_company_role(company, role, top_k=10)
    best = df.loc[ids].iloc[0]
    role_skills = parse_skill_list(best["_skills"])

    ats = resume_ats_score(resume_text, role_skills)
    fit = ats["score"]  # reuse role-aware score as fit proxy (simple + stable)

    missing = ats.get("missing_skills", [])[:15]
    matched = ats.get("matched_skills", [])[:15]

    suggestions = []
    if missing:
        suggestions.append("Add/learn missing skills: " + ", ".join(missing[:8]) + ".")
    suggestions += [
        "Add 2 quantified projects (numbers: accuracy, latency, revenue, users).",
        "Mirror role keywords in Skills + Projects (ATS alignment).",
        "Include impact metrics for internships and projects."
    ]

    return {
        "mode": "A",
        "placement_probability": round(placement_prob, 2),
        "target": {"company": company, "role": role},
        "role_fit_score": int(fit),
        "resume_ats_score": int(ats["score"]),
        "matched_skills": matched,
        "missing_skills": missing,
        "suggestions": suggestions
    }

def mode_c(role: str, resume_text: str, placement_prob: float) -> Dict[str, Any]:
    df = _load_jobs()
    ids = _find_by_role(role, top_k=80)
    subset = df.loc[ids].copy()

    results = []
    for _, r in subset.iterrows():
        role_skills = parse_skill_list(r["_skills"])
        ats = resume_ats_score(resume_text, role_skills)
        role_fit = ats["score"]
        fit_score = int(round(0.55 * role_fit + 0.25 * ats["score"] + 0.20 * placement_prob))
        results.append({
            "company": r["_company"],
            "role": r["_title"],
            "fit_score": fit_score,
            "role_fit": int(role_fit),
            "ats": int(ats["score"])
        })

    seen, uniq = set(), []
    for x in sorted(results, key=lambda z: z["fit_score"], reverse=True):
        key = (x["company"].lower(), x["role"].lower())
        if key in seen:
            continue
        seen.add(key)
        uniq.append(x)
        if len(uniq) >= 25:
            break

    return {
        "mode": "C",
        "placement_probability": round(placement_prob, 2),
        "target": {"role": role},
        "matches": uniq
    }

def mode_b(resume_text: str, placement_prob: float) -> Dict[str, Any]:
    df = _load_jobs()
    idx, sims = _recommend_by_resume(resume_text, top_k=60)
    subset = df.loc[idx].copy()
    subset["_sim"] = sims

    results = []
    for _, r in subset.iterrows():
        role_skills = parse_skill_list(r["_skills"])
        ats = resume_ats_score(resume_text, role_skills)
        role_fit = ats["score"]
        fit_score = int(round(0.45 * (float(r["_sim"]) * 100) + 0.30 * role_fit + 0.10 * ats["score"] + 0.15 * placement_prob))
        results.append({
            "company": r["_company"],
            "role": r["_title"],
            "fit_score": fit_score,
            "role_fit": int(role_fit),
            "ats": int(ats["score"])
        })

    seen, uniq = set(), []
    for x in sorted(results, key=lambda z: z["fit_score"], reverse=True):
        key = (x["company"].lower(), x["role"].lower())
        if key in seen:
            continue
        seen.add(key)
        uniq.append(x)
        if len(uniq) >= 25:
            break

    return {
        "mode": "B",
        "placement_probability": round(placement_prob, 2),
        "matches": uniq,
        "note": "No company/role provided → showing best role matches from dataset."
    }
