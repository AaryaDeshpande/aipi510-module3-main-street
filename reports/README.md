# Experiments and verification results

The pipeline logs three validation candidates and one selected-model evaluation in MLflow. Its test MAE is 3.0594 establishments, compared with 2.9016 for persistence. The recorded test suite contains 62 passing tests, and all 12 reproduction checks passed.

| Record | Contents |
|---|---|
| [MLflow runs](mlflow_runs.json) | Parameters, metrics, run IDs and logged artifacts |
| [Reproduction](reproducibility.json) | Split, preprocessing, metric and prediction comparisons |
| [GCS upload](cloud_upload.json) | Dataset URI, bytes, checksum and object generation |
| [Ingestion manifest](../artifacts/ingestion.json) | GCS source and downloaded dataset checksums |
| [Deployment](google_cloud_deployment.json) | Cloud Build ID, image digest, Cloud Run revision and API routing |
| [Cloud Run HTTP](google_cloud_http.json) | Direct API and frontend checks |
| [Frontend HTTP](frontend_http.json) | Public Vercel requests through the API routes |
| [Endpoint and artifact checks](public_http_checks.json) | Predictions, invalid-input handling, matching hashes and recomputed MAE |
| [CI run](ci_run.json) | Completed build, container training, reproduction and HTTP steps |
| [Local Docker reproduction](tanya_docker_review.md) | Tanya's November 23 environment, commands and results |

The [GitHub Actions run](https://github.com/AaryaDeshpande/aipi510-module3-main-street/actions/runs/45437248856) contains the full container logs. Data/model artifacts and evaluation outputs are in `artifacts/`.

The local Docker report predates the GCS deployment. Its pandas entry is 2.3.5, while the dependency files pin 2.2.3; the CI run uses the pinned requirements.

## Rerun checks

```bash
python -m pytest -q
python -m business_app verify
python scripts/export_runs.py
python scripts/check_http_local.py
```

`verify` retrains from the source recorded in the model metadata. The committed model records GCS, so it requires application-default credentials. For an offline reproduction, train from `data/panel.csv` first, as shown in the README.

The CI workflow performs credential-free container training from the bundled panel and compares its splits, metrics and predictions with the committed artifacts. Dates, source commits and hashes identify the execution associated with each record.
