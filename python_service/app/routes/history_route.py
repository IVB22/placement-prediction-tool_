from flask import Blueprint, request, jsonify
from app.repositories.mongo_repo import get_last_runs

history_bp = Blueprint("history", __name__)

@history_bp.get("/history")
def history():
    limit = int(request.args.get("limit", "10"))
    return jsonify({"items": get_last_runs(limit)})
