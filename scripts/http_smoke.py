"""Exercise a real running local, container, or public HTTP service."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import requests

parser = argparse.ArgumentParser()
parser.add_argument("--base-url", required=True)
parser.add_argument("--output", type=Path, default=Path("reports/http_smoke.json"))
args = parser.parse_args()
base = args.base_url.rstrip("/")
checks = []
health = requests.get(base + "/health", timeout=30)
health.raise_for_status()
assert health.json()["status"] == "ready"
checks.append("health")
response = requests.get(base + "/", timeout=30)
response.raise_for_status()
assert "Main Street" in response.text
checks.append("frontend_served")
data = requests.get(base + "/api/data", timeout=30)
data.raise_for_status()
catalog = data.json()
assert len(catalog["counties"]) == 72 and len(catalog["rows"]) == 720
assert data.json()["model"]["model_sha256"] == health.json()["model_sha256"]
checks.append("real_catalog_and_model_hash")
geometry = requests.get(base + "/api/geo", timeout=30)
geometry.raise_for_status()
assert len(geometry.json()["features"]) == 72
checks.append("72_county_geometries")
for industry in ["2382", "5412", "8121"]:
    prediction = requests.post(base + "/predict", json={"industry": industry, "establishments": 100, "previous_establishments": 95}, timeout=30)
    prediction.raise_for_status()
    result = prediction.json()
    assert result["prediction"] >= 0 and result["target_year"] == 2024 and result["model_sha256"] == health.json()["model_sha256"]
checks.append("three_real_json_predictions")
for bad in [{}, {"industry": "2382", "establishments": True, "previous_establishments": 95}]:
    assert requests.post(base + "/predict", json=bad, timeout=30).status_code == 422
assert requests.post(base + "/predict", data="no-json", timeout=30).status_code == 415
checks.append("invalid_inputs_rejected")
output = {"checked_utc": datetime.now(timezone.utc).isoformat(), "base_url": base, "passed": True, "checks": checks, "model_sha256": health.json()["model_sha256"]}
args.output.parent.mkdir(parents=True, exist_ok=True)
args.output.write_text(json.dumps(output, indent=2) + "\n")
print(json.dumps(output, indent=2))
