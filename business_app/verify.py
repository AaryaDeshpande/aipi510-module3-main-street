"""Independent split/preprocessing checks plus deterministic training rerun."""
from __future__ import annotations
import json
from datetime import datetime, timezone
import joblib
import numpy as np
from .data import ROOT, FEATURES, load_panel, supervised
from .train import build_features, predict_next, train_project, write_json

def verify():
    first = json.loads((ROOT / "artifacts" / "metadata.json").read_text())
    output = ROOT / "artifacts" / "reproduced"
    second = train_project(first["dataset"]["source"], output)
    checks = {"same_" + key: first[key] == second[key] for key in ["alpha", "validation", "test", "baseline_test", "split_counts", "model_beats_baseline"]}
    ids = json.loads((ROOT / "artifacts" / "split_ids.json").read_text())
    checks["same_split_ids"] = ids == json.loads((output / "split_ids.json").read_text())
    checks["same_dataset_hash"] = first["dataset"]["sha256"] == second["dataset"]["sha256"]
    panel, _ = load_panel(first["dataset"]["source"], first["dataset"]["sha256"])
    joined = supervised(panel)
    sets = [set(ids[k]) for k in ["train", "validation", "test"]]
    checks["split_ids_disjoint"] = not (sets[0] & sets[1] or sets[0] & sets[2] or sets[1] & sets[2])
    checks["chronological_labels"] = all(set(joined.loc[joined.row_id.isin(ids[k]), "target_year"]) == {first[field]} for k, field in [
        ("train", "train_target_year"), ("validation", "validation_target_year"), ("test", "test_target_year")])
    model = joblib.load(ROOT / "artifacts" / "model.joblib")
    train = joined.loc[joined.row_id.isin(ids["train"])]
    features = build_features(train[FEATURES])
    expected_mean = features[["log_current", "log_previous", "lag_growth"]].mean().to_numpy()
    checks["scaler_fit_only_on_training"] = bool(np.allclose(model.named_steps["preprocess"].named_transformers_["numeric"].mean_, expected_mean))
    test = joined.loc[joined.row_id.isin(ids["test"])].sort_values(["county_fips", "industry"])
    repeated = joblib.load(output / "model.joblib")
    checks["same_test_predictions"] = bool(np.allclose(predict_next(model, test), predict_next(repeated, test), rtol=0, atol=1e-12))
    result = {"checked_utc": datetime.now(timezone.utc).isoformat(), "passed": all(checks.values()), "checks": checks,
        "scope": "Local/cloud-source training reproduction according to recorded source; container/public checks are separate"}
    write_json(ROOT / "reports" / "reproducibility.json", result)
    if not result["passed"]: raise AssertionError(json.dumps(result))
    return result
