"""Past-year training, later-year selection, untouched final-year evaluation."""
from __future__ import annotations
import hashlib
import json
import platform
from datetime import datetime, timezone
from pathlib import Path
import joblib
import mlflow
import numpy as np
import pandas as pd
import sklearn
import yaml
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, median_absolute_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, StandardScaler
from .data import ROOT, FEATURES, load_panel, sha256, supervised
from .inference import build_features, predict_next

def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n")

def make_model(alpha):
    return Pipeline([
        ("features", FunctionTransformer(build_features, validate=False)),
        ("preprocess", ColumnTransformer([
            ("numeric", StandardScaler(), ["log_current", "log_previous", "lag_growth"]),
            ("industry", OneHotEncoder(handle_unknown="ignore", sparse_output=False), ["industry"]),
        ])),
        ("regression", Ridge(alpha=float(alpha))),
    ])

def score(actual, predicted):
    actual, predicted = np.asarray(actual, dtype=float), np.asarray(predicted, dtype=float)
    return {"mae": float(mean_absolute_error(actual, predicted)), "median_ae": float(median_absolute_error(actual, predicted)),
        "rmse": float(np.sqrt(mean_squared_error(actual, predicted))),
        "wape": float(np.abs(actual - predicted).sum() / actual.sum())}

def train_project(data_uri=None, output_dir=None, config_path=ROOT / "config.yaml"):
    config = yaml.safe_load(Path(config_path).read_text())
    source = data_uri or config["dataset"]["uri"]
    config["dataset"]["uri"] = source
    panel, ingestion = load_panel(source, config["dataset"]["sha256"])
    joined = supervised(panel)
    split_cfg = config.get("split", {"train_target_year": 2021, "validation_target_year": 2022, "test_target_year": 2023})
    years = [int(split_cfg[k]) for k in ["train_target_year", "validation_target_year", "test_target_year"]]
    if not years[0] < years[1] < years[2]:
        raise ValueError("Training, validation, and test target years must strictly increase")
    parts = [joined.loc[joined.target_year.eq(year)].copy() for year in years]
    if min(map(len, parts)) < 100:
        raise ValueError("Too few complete observations in a temporal split")
    train, validation, test = parts
    output = Path(output_dir or ROOT / config.get("output_dir", "artifacts")).resolve()
    output.mkdir(parents=True, exist_ok=True)
    tracking = output / "tracking"
    tracking.mkdir(exist_ok=True)
    mlflow.set_tracking_uri(f"sqlite:///{tracking / 'mlflow.db'}")
    name = config.get("tracking", {}).get("experiment", "aipi510-main-street-business")
    experiment = mlflow.get_experiment_by_name(name)
    experiment_id = experiment.experiment_id if experiment else mlflow.create_experiment(name, artifact_location=(tracking / "runs").as_uri())
    mlflow.set_experiment(experiment_id=experiment_id)
    manifest = {key: data.row_id.tolist() for key, data in zip(["train", "validation", "test"], parts)}
    write_json(output / "split_ids.json", manifest)
    write_json(output / "ingestion.json", ingestion)
    write_json(output / "resolved_config.json", config)
    digest = hashlib.sha256()
    for path in sorted((ROOT / "business_app").rglob("*.py")):
        digest.update(path.name.encode()); digest.update(path.read_bytes())
    fixed = {"dataset_sha256": ingestion["sha256"], "code_sha256": digest.hexdigest(), "train_target_year": years[0],
        "validation_target_year": years[1], "test_target_year": years[2], "train_rows": len(train), "validation_rows": len(validation),
        "test_rows": len(test), "target": "next-year establishment relative change", "seed": int(config.get("model", {}).get("seed", 42))}
    targets = (train.actual_next - train.establishments) / (train.establishments + 1)
    candidates, models = [], {}
    for alpha in config.get("model", {}).get("alphas", [1, 10, 100]):
        model = make_model(alpha).fit(train[FEATURES], targets)
        metrics = score(validation.actual_next, predict_next(model, validation))
        with mlflow.start_run(run_name=f"validation-ridge-alpha-{alpha}") as run:
            mlflow.log_params({**fixed, "alpha": alpha, "stage": "validation"})
            mlflow.log_metrics({"validation_" + k: v for k, v in metrics.items()})
            mlflow.log_artifact(str(output / "split_ids.json"))
            candidates.append({"alpha": float(alpha), "validation": metrics, "run_id": run.info.run_id})
        models[float(alpha)] = model
    best = min(candidates, key=lambda row: (row["validation"]["mae"], -row["alpha"]))
    model = models[best["alpha"]]
    predictions = predict_next(model, test)
    metrics = score(test.actual_next, predictions)
    baseline = score(test.actual_next, test.establishments)
    wi_mask = test.county_fips.str.startswith("55")
    wi_test = score(test.loc[wi_mask, "actual_next"], predictions[wi_mask.to_numpy()])
    wi_baseline = score(test.loc[wi_mask, "actual_next"], test.loc[wi_mask, "establishments"])
    validation_baseline = score(validation.actual_next, validation.establishments)
    predictions_frame = test[["row_id", "county_fips", "industry", "year", "target_year", "establishments", "actual_next"]].copy()
    predictions_frame["prediction"] = predictions
    predictions_frame["baseline"] = test.establishments.to_numpy()
    predictions_frame.to_csv(output / "test_predictions.csv", index=False)
    joblib.dump(model, output / "model.joblib")
    metadata = {**fixed, "created_utc": datetime.now(timezone.utc).isoformat(), "dataset": ingestion,
        "selected_model": "Ridge regression of relative establishment change", "alpha": best["alpha"],
        "selection_rule": "Lowest validation MAE; ties select stronger regularization", "features": FEATURES,
        "split_counts": {k: len(v) for k, v in zip(["train", "validation", "test"], parts)},
        "validation": best["validation"], "baseline_validation": validation_baseline, "test": metrics, "baseline_test": baseline,
        "model_beats_baseline": metrics["mae"] < baseline["mae"], "validation_beats_baseline": best["validation"]["mae"] < validation_baseline["mae"],
        "wisconsin_test": wi_test, "wisconsin_baseline_test": wi_baseline, "wisconsin_test_rows": int(wi_mask.sum()),
        "test_skill_vs_persistence": 1 - metrics["mae"] / baseline["mae"], "forecast_year": int(panel.year.max()) + 1,
        "as_of_year": int(panel.year.max()), "scope": "National complete county-industry triples in ten selected service industries; Wisconsin explorer",
        "candidates": candidates, "model_sha256": sha256((output / "model.joblib").read_bytes()),
        "versions": {"python": platform.python_version(), "scikit-learn": sklearn.__version__, "numpy": np.__version__, "pandas": pd.__version__},
        "limitations": ["Historical data ending in 2023; displayed 2024 estimates are unverified historical estimates, not a 2026 nowcast",
            "Temporal checks separate reference years; source publication lags mean this is not a real-time forecast backtest",
            "Establishments are business locations, not distinct firms, profits, owner wealth, or proven customer demand",
            "Unpublished small cells remain unknown; complete-case modeling excludes incomplete histories and can favor established markets",
            "Employment and payroll include disclosure/noise flags and are excluded from model features",
            "Annual temporal splits share county-industry entities across years, appropriate to forecasting existing markets; performance on unseen places is untested",
            "Pandemic/recovery-era behavior may not generalize; establishment growth can also mean greater competition"],
    }
    with mlflow.start_run(run_name="selected-ridge-final-test") as run:
        metadata["final_run_id"] = run.info.run_id
        mlflow.log_params({**fixed, "alpha": best["alpha"], "stage": "test"})
        mlflow.log_metrics({"test_" + k: v for k, v in metrics.items()})
        mlflow.log_metrics({"baseline_test_" + k: v for k, v in baseline.items()})
        write_json(output / "metadata.json", metadata)
        for name in ["metadata.json", "model.joblib", "ingestion.json", "resolved_config.json", "split_ids.json", "test_predictions.csv"]:
            mlflow.log_artifact(str(output / name))
    return metadata
