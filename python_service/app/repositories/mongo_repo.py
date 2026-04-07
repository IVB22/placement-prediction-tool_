from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from app.config.settings import Settings

_client: Optional[MongoClient] = None

def _get_client() -> MongoClient:
    global _client
    if _client is None:
        _client = MongoClient(Settings.MONGO_URI)
    return _client

def _get_db() -> Database:
    return _get_client()[Settings.MONGO_DB]

def runs_collection() -> Collection:
    return _get_db()[Settings.MONGO_COLLECTION_RUNS]

def save_run(request_obj: Dict[str, Any], response_obj: Dict[str, Any]) -> str:
    doc = {
        "createdAt": datetime.now(timezone.utc),
        "request": request_obj,
        "response": response_obj,
    }
    res = runs_collection().insert_one(doc)
    return str(res.inserted_id)

def get_last_runs(limit: int = 10) -> List[Dict[str, Any]]:
    cur = runs_collection().find().sort("createdAt", -1).limit(int(limit))
    out = []
    for d in cur:
        d["_id"] = str(d.get("_id"))
        # datetime to iso
        if "createdAt" in d and hasattr(d["createdAt"], "isoformat"):
            d["createdAt"] = d["createdAt"].isoformat()
        out.append(d)
    return out
