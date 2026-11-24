"""Saved-model JSON inference and a dated, source-grounded local market explorer."""
from __future__ import annotations
import json
import math
from pathlib import Path
import joblib
import pandas as pd
import yaml
from flask import Flask, jsonify, render_template, request
from werkzeug.exceptions import BadRequest, RequestEntityTooLarge
from .data import ROOT, FEATURES, load_panel, sha256
from .inference import predict_next

HYPOTHESES = {
 "2382": "Investigate missed inquiries, estimate follow-up, and scheduling handoffs with building-equipment contractors.",
 "2383": "Investigate how finishing contractors turn photos and scope notes into estimates and follow-up tasks.",
 "5412": "Investigate document collection, client status updates, and repetitive reminders with accounting firms.",
 "5413": "Investigate finding project documents and tracking client requests with engineering/design firms.",
 "5415": "Investigate repetitive client support, knowledge retrieval, and incident-routing work with IT service firms.",
 "5617": "Investigate quote follow-up and recurring job scheduling with cleaning/grounds service businesses.",
 "6212": "Investigate referral correspondence and administrative handoffs with dental offices; begin without patient data.",
 "6213": "Investigate appointment-request and administrative handoffs with health-practitioner offices; begin without patient data.",
 "8111": "Investigate estimate approval, appointment inquiries, and service-status updates with repair shops.",
 "8121": "Investigate booking inquiries, missed calls, and appointment follow-up with personal-care businesses.",
}

def number(value):
    return None if pd.isna(value) else float(value)

def create_app(artifact_dir: Path | None = None):
    folder = Path(artifact_dir or ROOT / "artifacts")
    metadata = json.loads((folder / "metadata.json").read_text())
    if sha256((folder / "model.joblib").read_bytes()) != metadata["model_sha256"]:
        raise ValueError("Saved model checksum does not match metadata")
    # joblib can execute code: only the team's own controlled training artifact is loaded.
    model = joblib.load(folder / "model.joblib")
    config = yaml.safe_load((ROOT / "config.yaml").read_text())
    economics_bytes = (ROOT / config["economics"]["uri"]).read_bytes()
    if sha256(economics_bytes) != config["economics"]["sha256"]:
        raise ValueError("Economics snapshot checksum does not match configuration")
    economics = json.loads(economics_bytes)
    panel, evidence = load_panel(str(ROOT / "data" / "panel.csv"), config["dataset"]["sha256"])
    if evidence["sha256"] != metadata["dataset"]["sha256"]:
        raise ValueError("Model and explorer dataset versions differ")
    geometry = json.loads((ROOT / "data" / "wi_counties.geojson").read_text())
    provenance = json.loads((ROOT / "data" / "SOURCE.json").read_text())
    if sha256((ROOT / "data" / "wi_counties.geojson").read_bytes()) != provenance["geometry"]["sha256"]:
        raise ValueError("Geometry checksum does not match source manifest")
    industries = json.loads((ROOT / "data" / "industries.json").read_text())
    counties = sorted([{"fips": str(f.get("id") or f["properties"]["GEOID"]), "name": f["properties"]["NAME"]} for f in geometry["features"]], key=lambda row: row["name"])
    wi = panel.loc[panel.county_fips.str.startswith("55")].copy()
    records = {(row.county_fips, row.industry, int(row.year)): row for row in wi.itertuples()}
    test = pd.read_csv(folder / "test_predictions.csv", dtype={"county_fips": str, "industry": str})
    test_records = {(row.county_fips, row.industry): row for row in test.itertuples()}
    latest = int(wi.year.max())
    rows = []
    for county in counties:
        for industry in industries:
            current = records.get((county["fips"], industry, latest))
            previous = records.get((county["fips"], industry, latest - 1))
            backtest = test_records.get((county["fips"], industry))
            rows.append({"county_fips": county["fips"], "county_name": county["name"], "industry": industry,
                "establishments": int(current.establishments) if current else None,
                "previous_establishments": int(previous.establishments) if previous else None,
                "growth_pct": 100 * (current.establishments / previous.establishments - 1) if current and previous else None,
                "employment": number(current.employment) if current else None,
                "annual_payroll": number(current.annual_payroll) if current else None,
                "employment_flag": str(current.employment_flag) if current else None,
                "payroll_flag": str(current.payroll_flag) if current else None,
                "history": [{"year": year, "establishments": int(r.establishments) if (r := records.get((county["fips"], industry, year))) else None} for year in range(2019, latest + 1)],
                "backtest": {"target_year": int(backtest.target_year), "actual": int(backtest.actual_next), "prediction": float(backtest.prediction), "baseline": int(backtest.baseline)} if backtest else None})
    public_model = {key: metadata[key] for key in ["test", "baseline_test", "validation", "baseline_validation", "selected_model", "alpha", "model_beats_baseline", "validation_beats_baseline", "test_skill_vs_persistence", "forecast_year", "as_of_year", "train_target_year", "validation_target_year", "test_target_year", "split_counts", "model_sha256", "scope"]}
    sources = [{"name": "Census County Business Patterns: downloadable data", "url": "https://www.census.gov/programs-surveys/cbp/data/datasets.html"},
        {"name": "Census methodology and disclosure rules", "url": "https://www.census.gov/programs-surveys/cbp/technical-documentation/methodology.html"},
        {"name": "Current release status (latest reference year 2023)", "url": "https://www.census.gov/programs-surveys/cbp/data.html"},
        {"name": "Census TIGERweb county map geometry", "url": "https://tigerweb.geo.census.gov/"}]
    payload = {"latest_year": latest, "industries": [{"code": code, "name": name, "workflow_hypothesis": HYPOTHESES[code]} for code, name in industries.items()],
        "counties": counties, "rows": rows, "model": public_model, "sources": sources, "limitations": metadata["limitations"],
        "dataset_sha256": evidence["sha256"], "missing_data_note": "Unpublished cells are unknown. Since 2017, cells below three establishments are excluded by Census; absence can also reflect other reporting/geography issues.",
        "questions": ["Describe the last time this workflow caused a delay or lost inquiry.", "How frequently does it happen, and who handles it today?", "What time or money does it cost, and what have you already tried?", "Who approves spending, and what would a paid pilot need to prove?"]}
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = 16384

    @app.after_request
    def headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Cache-Control"] = "no-store"
        return response

    @app.errorhandler(RequestEntityTooLarge)
    def too_large(_):
        return jsonify(error="Request exceeds 16 KB"), 413

    @app.get("/")
    def index(): return render_template("index.html")

    @app.get("/ownership")
    def ownership(): return render_template("home.html")

    @app.get("/market")
    def market(): return render_template("index.html")

    @app.get("/api/economics")
    def financial_context(): return jsonify(economics)

    @app.get("/api/data")
    def data(): return jsonify(payload)

    @app.get("/api/geo")
    def geo(): return jsonify(geometry)

    @app.get("/health")
    def health(): return jsonify(status="ready", model_sha256=metadata["model_sha256"], dataset_sha256=evidence["sha256"])

    @app.get("/metadata")
    def info(): return jsonify(model=public_model, limitations=metadata["limitations"], versions=metadata["versions"])

    @app.post("/predict")
    def predict():
        if not request.is_json:
            return jsonify(error="Send application/json"), 415
        try: supplied = request.get_json()
        except BadRequest: return jsonify(error="Malformed JSON"), 400
        if not isinstance(supplied, dict) or set(supplied) != set(FEATURES):
            return jsonify(error="Include exactly industry, establishments, and previous_establishments", fields=FEATURES), 422
        if not isinstance(supplied["industry"], str) or supplied["industry"] not in industries:
            return jsonify(error="Industry must be one of the ten documented four-digit codes"), 422
        for key in FEATURES[1:]:
            value = supplied[key]
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not 3 <= value <= 1_000_000 or not float(value).is_integer():
                return jsonify(error=f"{key} must be a reported whole count between 3 and 1,000,000"), 422
        frame = pd.DataFrame([supplied], columns=FEATURES)
        result = float(predict_next(model, frame)[0])
        return jsonify(prediction=result, baseline=float(supplied["establishments"]), target_year=metadata["forecast_year"], as_of_year=latest,
            model_sha256=metadata["model_sha256"], model_beats_baseline=metadata["model_beats_baseline"],
            notice="Unverified historical 2024 estimate using the 2023 feature definition. Review held-out 2023 error and persistence baseline; this is not a current market-demand forecast.")
    return app
