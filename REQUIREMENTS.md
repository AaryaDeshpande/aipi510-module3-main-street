# Module Project 3 requirement coverage

Audited November 24, 2026 against the assignment text supplied by Aarya. The authenticated Canvas assignment and submitted attempt were also inspected directly.

| Requirement | Assessment and evidence |
|---|---|
| Public dataset, supervised task, target, metric | Met: official Census CBP, next-year establishment regression, MAE; `data/SOURCE.json`, README |
| Local cleaning and programmatic cloud ingestion | Met with actual GCS upload and GCS-sourced training: `business_app/prepare.py`, `business_app/data.py`, `artifacts/ingestion.json` |
| Named storage provider | **Met: actual private GCS object and cloud-ingested training; `reports/cloud_upload.json`, `artifacts/ingestion.json`.** |
| Configured preprocessing, training, validation, test | Met: `config.yaml`, `business_app/train.py`; learned transforms fit training only; chronological targets 2021/2022/2023 |
| Actual MLflow parameters, metrics, artifacts | Met in recorded execution: four FINISHED runs; `reports/mlflow_runs.json`, training code and CI logs |
| Requirements, structure, training/serving Dockerfile | Met: pinned environment files, `Dockerfile`, CLI entry points |
| Docker build/run and reproducibility | Hosted CI execution verified; Tanya's PR documents local execution. Confirm the pandas-version entry in her report. |
| Flask JSON `/predict`, local curl testing | Met: serving code, actual CI HTTP/curl logs, Tanya's local report |
| Named public API hosting platform | **Met: public Cloud Run service; successful Docker image build/revision and HTTP checks in `reports/google_cloud_deployment.json` and `reports/google_cloud_http.json`.** |
| Public interactive frontend consuming live API | Met: public Vercel frontend; real browser prediction and fresh HTTP checks passed |
| README content and links | Present; this integration replaces stale status statements and restores explicit API/frontend links and prior-source citations |
| Branches and at least one PR per member | Met: Aarya PR #1 and Tanya PR #2; Tanya has write access. This integration retains both authors' commits. |
| Ethical implications and limitations | Met: missingness/selection, reporting lag, competition, historical estimates, no demand/profit/wealth claims |
| Canvas roster, deadline, submission | Submitted attempt and deadline directly observed; group membership remains unverified. No Canvas changes made. |

The assignment excludes model accuracy from assessment. Test MAE 3.0594 versus persistence 2.9016 is disclosed and is not itself a rubric failure.

Read [the audit](reports/submission_audit_20261124.md), [team actions](TEAM_ACTIONS.md), and [Google Cloud migration instructions](infrastructure/GOOGLE_CLOUD.md). Actual GCS/Cloud Run execution is recorded separately from the reusable deployment script.
