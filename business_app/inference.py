"""Shared feature recipe and saved-model inference, with no training dependencies.

Keeping these functions in a small runtime module lets joblib reload the saved
pipeline without importing MLflow or a training database on the web service.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .data import FEATURES


def build_features(frame):
    result = pd.DataFrame(index=frame.index)
    result["industry"] = frame["industry"].astype(str)
    result["log_current"] = np.log1p(frame["establishments"])
    result["log_previous"] = np.log1p(frame["previous_establishments"])
    result["lag_growth"] = ((frame.establishments - frame.previous_establishments) / (frame.previous_establishments + 1)).clip(-1, 2)
    return result


def predict_next(model, frame):
    current = np.asarray(frame["establishments"], dtype=float)
    relative_change = model.predict(frame[FEATURES])
    return np.maximum(0, current + (current + 1) * relative_change)
