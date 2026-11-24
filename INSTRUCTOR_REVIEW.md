# Implementation and evidence map

Start with [README.md](README.md) for purpose, data, evaluation, setup, deployment, and limitations. [REQUIREMENTS.md](REQUIREMENTS.md) records the executed correction of both provider gaps.

| Evidence | Location |
|---|---|
| Official data and cleaning | `data/SOURCE.json`, `business_app/prepare.py` |
| Configured supervised pipeline | `config.yaml`, `business_app/data.py`, `business_app/train.py` |
| Actual MLflow run export | `reports/mlflow_runs.json` |
| Saved model, split IDs, test predictions | `artifacts/` |
| Main-branch Docker build/train/reproduction/HTTP | [CI run 45292395651](https://github.com/AaryaDeshpande/aipi510-module3-main-street/actions/runs/45292395651) |
| Tanya's local execution report | `reports/tanya_docker_review.md`, PR #2 |
| Fresh public HTTP and artifact checks | `reports/submission_http_audit_20261124.json` |
| Full current assessment | `reports/submission_audit_20261124.md` |

The app's historical research view is public at <https://aipi510-module3-main-street.vercel.app/>. The model's test MAE is worse than persistence and this is disclosed. The project does not establish current demand, business profits, or owner wealth.
