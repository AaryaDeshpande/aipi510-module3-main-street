"""Export actual runs referenced by the current model; portable review evidence."""
from datetime import datetime, timezone
import json
from pathlib import Path
from mlflow.tracking import MlflowClient

root = Path(__file__).resolve().parents[1]
metadata = json.loads((root / "artifacts" / "metadata.json").read_text())
client = MlflowClient(tracking_uri=f"sqlite:///{root / 'artifacts' / 'tracking' / 'mlflow.db'}")
ids = [item["run_id"] for item in metadata["candidates"]] + [metadata["final_run_id"]]
runs = []
for run_id in ids:
    run = client.get_run(run_id)
    runs.append({"run_id": run_id, "name": run.info.run_name, "status": run.info.status, "parameters": run.data.params,
        "metrics": run.data.metrics, "artifacts": [item.path for item in client.list_artifacts(run_id)]})
output = root / "reports" / "mlflow_runs.json"
output.parent.mkdir(exist_ok=True)
output.write_text(json.dumps({"exported_utc": datetime.now(timezone.utc).isoformat(), "runs": runs}, indent=2) + "\n")
print(f"Exported {len(runs)} actual runs")
