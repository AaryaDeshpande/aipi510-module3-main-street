"""Evidence-focused checks for dated observations, fair evaluation, and real inference."""
from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import pytest
import yaml

from business_app.data import FEATURES, ROOT, load_panel, sha256, supervised
from business_app.prepare import INDUSTRIES, magnitude
from business_app.train import train_project
from business_app.web import create_app


@pytest.fixture(scope="session")
def snapshot():
    config = yaml.safe_load((ROOT / "config.yaml").read_text())
    return load_panel(str(ROOT / "data" / "panel.csv"), config["dataset"]["sha256"])


@pytest.fixture(scope="session")
def trained(tmp_path_factory):
    output = tmp_path_factory.mktemp("business-model")
    metadata = train_project(data_uri=str(ROOT / "data" / "panel.csv"), output_dir=output)
    return output, metadata


@pytest.fixture(scope="session")
def client(trained):
    app = create_app(trained[0])
    app.config.update(TESTING=True)
    return app.test_client()


def test_snapshot_matches_published_provenance_and_has_unique_valid_keys(snapshot):
    panel, evidence = snapshot
    provenance = json.loads((ROOT / "data" / "SOURCE.json").read_text())
    assert evidence["sha256"] == provenance["sha256"] == sha256((ROOT / "data" / "panel.csv").read_bytes())
    assert evidence["rows"] == provenance["rows"] == len(panel)
    assert evidence["transport"] == "local" and evidence["cloud_ingestion_verified"] is False
    assert set(panel.year) == set(range(2019, 2024))
    assert set(panel.industry) == set(INDUSTRIES)
    assert panel.county_fips.str.fullmatch(r"\d{5}").all()
    assert not panel.county_fips.str.endswith(("000", "999")).any()
    assert not panel.duplicated(["county_fips", "industry", "year"]).any()
    assert (panel.establishments >= 3).all()
    assert all(code.isdigit() and len(code) == 4 for code in panel.industry)


def test_missing_small_cells_stay_absent_instead_of_becoming_zero(snapshot):
    panel, _ = snapshot
    latest_wi = panel.loc[panel.state.eq("WI") & panel.year.eq(2023)]
    assert len(latest_wi) == 637
    assert len(latest_wi) < 72 * len(INDUSTRIES)
    assert not latest_wi.establishments.eq(0).any()
    # Choose a genuinely absent cell from the complete county/industry grid.
    known = set(zip(latest_wi.county_fips, latest_wi.industry))
    counties = {f["properties"]["GEOID"] for f in json.loads((ROOT / "data" / "wi_counties.geojson").read_text())["features"]}
    assert any((county, industry) not in known for county in counties for industry in INDUSTRIES)


def test_changed_snapshot_is_rejected_before_training(tmp_path):
    path = tmp_path / "changed.csv"
    original = (ROOT / "data" / "panel.csv").read_bytes()
    path.write_bytes(original + b"\n")
    with pytest.raises(ValueError, match="SHA-256"):
        load_panel(str(path), sha256(original))


@pytest.mark.parametrize("change", ["duplicate", "county", "industry", "negative", "fractional", "infinite"])
def test_bad_frozen_data_cannot_enter_training(snapshot, tmp_path, change):
    panel, _ = snapshot
    data = panel.iloc[:10].copy()
    if change == "duplicate":
        data = pd.concat([data, data.iloc[[0]]], ignore_index=True)
    elif change == "county":
        data.loc[data.index[0], "county_fips"] = "55999"
    elif change == "industry":
        data.loc[data.index[0], "industry"] = "2382//"
    elif change == "negative":
        data.loc[data.index[0], "establishments"] = -1
    elif change == "fractional":
        data["establishments"] = data.establishments.astype(float)
        data.loc[data.index[0], "establishments"] = 3.5
    else:
        data["establishments"] = data.establishments.astype(float)
        data.loc[data.index[0], "establishments"] = np.inf
    content = data.to_csv(index=False).encode()
    path = tmp_path / "invalid.csv"
    path.write_bytes(content)
    with pytest.raises(ValueError):
        load_panel(str(path), sha256(content))


def test_magnitude_units_and_withheld_values_are_preserved():
    assert magnitude("1234", "G", 1000) == 1_234_000
    assert magnitude("0", "H") == 0
    assert magnitude("17", "J") == 17
    for flag in ["S", "D", "N", ""]:
        assert magnitude("0", flag) is None
    assert magnitude("-1", "G") is None
    assert magnitude("invalid", "G") is None


def test_consecutive_year_features_and_labels_match_independent_source_lookup(snapshot):
    panel, _ = snapshot
    rows = supervised(panel)
    lookup = {(row.county_fips, row.industry, int(row.year)): int(row.establishments) for row in panel.itertuples()}
    assert set(rows.target_year) == {2021, 2022, 2023}
    assert rows.row_id.is_unique
    for row in rows.itertuples():
        assert row.target_year == row.year + 1
        assert row.previous_establishments == lookup[row.county_fips, row.industry, row.year - 1]
        assert row.establishments == lookup[row.county_fips, row.industry, row.year]
        assert row.actual_next == lookup[row.county_fips, row.industry, row.year + 1]
    expected_ids = {
        f"{county}:{industry}:{year}"
        for county, industry, year in lookup
        if (county, industry, year - 1) in lookup and (county, industry, year + 1) in lookup
    }
    assert set(rows.row_id) == expected_ids


def test_temporal_splits_and_scaling_use_training_observations_only(snapshot, trained):
    output, metadata = trained
    panel, _ = snapshot
    all_rows = supervised(panel).set_index("row_id")
    splits = json.loads((output / "split_ids.json").read_text())
    for name, year in [("train", 2021), ("validation", 2022), ("test", 2023)]:
        part = all_rows.loc[splits[name]]
        assert set(part.target_year) == {year}
        assert set(part.year) == {year - 1}
        assert len(part) == metadata["split_counts"][name]
    assert not set(splits["train"]) & set(splits["validation"])
    assert not set(splits["train"]) & set(splits["test"])
    assert not set(splits["validation"]) & set(splits["test"])
    train = all_rows.loc[splits["train"]]
    independent_numeric = np.column_stack([
        np.log1p(train.establishments),
        np.log1p(train.previous_establishments),
        np.clip((train.establishments - train.previous_establishments) / (train.previous_establishments + 1), -1, 2),
    ])
    model = joblib.load(output / "model.joblib")
    scaler = model.named_steps["preprocess"].named_transformers_["numeric"]
    np.testing.assert_allclose(scaler.mean_, independent_numeric.mean(axis=0), rtol=1e-12, atol=1e-12)
    assert scaler.n_samples_seen_ == len(train)


def test_test_metrics_and_persistence_baseline_match_saved_predictions(trained):
    output, metadata = trained
    data = pd.read_csv(output / "test_predictions.csv")
    assert set(data.target_year) == {2023}
    np.testing.assert_array_equal(data.baseline, data.establishments)
    actual = data.actual_next.to_numpy()
    for prediction, key in [(data.prediction.to_numpy(), "test"), (data.baseline.to_numpy(), "baseline_test")]:
        error = np.abs(actual - prediction)
        assert metadata[key]["mae"] == pytest.approx(error.mean())
        assert metadata[key]["wape"] == pytest.approx(error.sum() / actual.sum())
    assert metadata["model_beats_baseline"] == (metadata["test"]["mae"] < metadata["baseline_test"]["mae"])


@pytest.mark.parametrize("industry,current,previous", [("2382", 240, 230), ("5412", 80, 82), ("8121", 15, 12)])
def test_json_predictions_use_actual_saved_supervised_model(client, trained, industry, current, previous):
    supplied = dict(industry=industry, establishments=current, previous_establishments=previous)
    response = client.post("/predict", json=supplied)
    assert response.status_code == 200
    model = joblib.load(trained[0] / "model.joblib")
    relative_change = float(model.predict(pd.DataFrame([supplied], columns=FEATURES))[0])
    expected = max(0, current + (current + 1) * relative_change)
    assert response.json["prediction"] == pytest.approx(expected)
    assert response.json["baseline"] == current
    assert response.json["target_year"] == 2024 and response.json["as_of_year"] == 2023
    assert response.json["model_sha256"] == trained[1]["model_sha256"]
    assert "historical" in response.json["notice"].lower()


VALID = {"industry": "2382", "establishments": 25, "previous_establishments": 24}


@pytest.mark.parametrize("invalid", [
    None, [], {}, {"industry": "2382"}, {**VALID, "extra": 1},
    {**VALID, "industry": "9999"}, {**VALID, "industry": 2382}, {**VALID, "industry": "2382//"},
    {**VALID, "establishments": True}, {**VALID, "previous_establishments": False},
    {**VALID, "establishments": -1}, {**VALID, "establishments": 0}, {**VALID, "establishments": 2},
    {**VALID, "establishments": 3.5}, {**VALID, "establishments": "25"},
    {**VALID, "establishments": 1_000_001}, {**VALID, "establishments": float("nan")},
    {**VALID, "previous_establishments": float("inf")},
])
def test_invalid_prediction_requests_are_rejected(client, invalid):
    response = client.post("/predict", data=json.dumps(invalid), content_type="application/json")
    assert response.status_code == 422
    assert "error" in response.json


def test_bad_request_transport_and_oversized_body_are_rejected(client):
    assert client.post("/predict", data="no-json").status_code == 415
    assert client.post("/predict", data="{broken", content_type="application/json").status_code == 400
    assert client.post("/predict", data="x" * 20000, content_type="application/json").status_code == 413


def test_explorer_grid_preserves_unknowns_and_exact_source_observations(client, snapshot, trained):
    response = client.get("/api/data")
    assert response.status_code == 200
    def invalid_constant(value):
        raise AssertionError(f"Nonstandard JSON constant: {value}")
    data = json.loads(response.data, parse_constant=invalid_constant)
    assert len(data["rows"]) == 720 and len(data["counties"]) == 72
    assert len({(row["county_fips"], row["industry"]) for row in data["rows"]}) == 720
    assert sum(row["establishments"] is not None for row in data["rows"]) == 637
    assert sum(row["establishments"] is None for row in data["rows"]) == 83
    panel, evidence = snapshot
    lookup = {(row.county_fips, row.industry, int(row.year)): row for row in panel.loc[panel.state.eq("WI")].itertuples()}
    for row in data["rows"]:
        actual = lookup.get((row["county_fips"], row["industry"], 2023))
        assert row["establishments"] == (int(actual.establishments) if actual else None)
        if actual is None:
            assert row["employment"] is None and row["annual_payroll"] is None
            assert row["employment_flag"] is None and row["payroll_flag"] is None
        else:
            assert row["annual_payroll"] == actual.annual_payroll
            assert row["employment"] == actual.employment
            assert row["employment_flag"] in {"G", "H", "J"}
            assert row["payroll_flag"] in {"G", "H", "J"}
        for point in row["history"]:
            past = lookup.get((row["county_fips"], row["industry"], point["year"]))
            assert point["establishments"] == (int(past.establishments) if past else None)
    assert data["dataset_sha256"] == evidence["sha256"] == trained[1]["dataset"]["sha256"]
    assert data["model"]["model_sha256"] == trained[1]["model_sha256"]
    assert data["latest_year"] == 2023


def test_geometry_health_and_metadata_identify_real_frozen_artifacts(client, trained):
    geometry = client.get("/api/geo").json
    assert geometry["type"] == "FeatureCollection"
    assert len(geometry["features"]) == 72
    identifiers = [feature["properties"]["GEOID"] for feature in geometry["features"]]
    assert len(set(identifiers)) == 72 and all(code.startswith("55") for code in identifiers)
    assert not any(code.endswith(("000", "999")) for code in identifiers)
    assert all(feature["geometry"]["type"] in {"Polygon", "MultiPolygon"} for feature in geometry["features"])
    health = client.get("/health").json
    assert health["status"] == "ready"
    assert health["model_sha256"] == trained[1]["model_sha256"]
    assert health["dataset_sha256"] == trained[1]["dataset"]["sha256"]
    meta = client.get("/metadata").json
    assert meta["model"]["test"] == trained[1]["test"]
    assert client.get("/").status_code == 200


def test_corrupted_or_mismatched_saved_model_cannot_start_service(trained, tmp_path):
    (tmp_path / "metadata.json").write_bytes((trained[0] / "metadata.json").read_bytes())
    (tmp_path / "model.joblib").write_bytes(b"wrong-model")
    with pytest.raises(ValueError, match="checksum"):
        create_app(tmp_path)
