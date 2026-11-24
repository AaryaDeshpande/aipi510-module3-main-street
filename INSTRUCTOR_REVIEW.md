# ML implementation and evidence map

| Component | Evidence |
|---|---|
| Dataset and cleaning | `business_app/prepare.py`, `data/SOURCE.json` |
| Training and model | `business_app/train.py`, `config.yaml`, `artifacts/metadata.json` |
| Experiment tracking | `reports/mlflow_runs.json` |
| Evaluation | MAE `3.0594` versus persistence `2.9016` |
| Docker | Docker CI and `reports/tanya_docker_review.md` |
| Serving | Flask `/predict`, `reports/public_http_smoke.json` |
| Frontend | Live Vercel application |
| Reproduction | `reports/reproducibility.json`, 61 tests |

Open checks: Tanya PR submission, Aarya review, provider interpretation, and final submission.
