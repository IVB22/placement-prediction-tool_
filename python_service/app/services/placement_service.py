from __future__ import annotations
import os
from typing import Any, Dict, Optional

import numpy as np
import pandas as pd
import joblib

from app.config.settings import Settings

_model: Optional[Any] = None

def load_model() -> Optional[Any]:
    global _model
    if _model is not None:
        return _model
    if os.path.exists(Settings.PLACEMENT_MODEL_PATH):
        _model = joblib.load(Settings.PLACEMENT_MODEL_PATH)
    return _model

def placement_probability(profile: Dict[str, Any]) -> float:
    # If model exists, use it. Otherwise, a reasonable heuristic.
    model = load_model()
    if model is None:
        # heuristic using key percentages if present
        vals = []
        for k in ["ssc_p","hsc_p","degree_p","etest_p","mba_p"]:
            try:
                vals.append(float(profile.get(k, 0)))
            except Exception:
                pass
        base = float(np.mean(vals)) if vals else 50.0
        # workex small bump
        if str(profile.get("workex", "No")).lower() == "yes":
            base += 3
        return float(np.clip(base, 0, 100))

    # Expect model trained on the campus dataset columns (same names).
    model_cols = model.named_steps["preprocess"].feature_names_in_
    row = {}
    for c in model_cols:
        row[c] = profile.get(c, profile.get(c.lower(), None))
        if row[c] is None:
            # defaults
            row[c] = "No" if c.lower() == "workex" else 0
    X = pd.DataFrame([row])
    proba = model.predict_proba(X)[0][1] * 100
    return float(np.clip(proba, 0, 100))
