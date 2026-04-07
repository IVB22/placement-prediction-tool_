from flask import Blueprint, request, jsonify

from app.services.placement_service import placement_probability
from app.services.role_match_service import mode_a, mode_b, mode_c
from app.repositories.mongo_repo import save_run

match_bp = Blueprint("match", __name__)

@match_bp.post("/match-json")
def match_json():
    data = request.get_json(force=True) or {}
    profile = data.get("profile", {}) or {}
    resume_text = data.get("resume_text", "") or ""
    company = (data.get("company") or "").strip()
    role = (data.get("role") or "").strip()

    placement_prob = placement_probability(profile)

    if company and role:
        response = mode_a(company, role, resume_text, placement_prob)
    elif (not company) and role:
        response = mode_c(role, resume_text, placement_prob)
    else:
        response = mode_b(resume_text, placement_prob)

    # Persist full history: request + response (includes resume_text)
    save_run({"profile": profile, "resume_text": resume_text, "company": company, "role": role}, response)

    return jsonify(response)
