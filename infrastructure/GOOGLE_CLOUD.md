# Google Cloud setup

Training uses Google Cloud Storage. The Flask API is built with Cloud Build from the repository Dockerfile and deployed to Cloud Run.

| Setting | Deployed value |
|---|---|
| Project | `linen-flux-439023-g2` |
| Region | `us-central1` |
| Bucket | `linen-flux-439023-g2-aipi510-m3` |
| Service | `main-street-business-explorer` |

## Prerequisites

Use a billing-enabled Google Cloud project with permissions to manage the bucket, Cloud Build, Artifact Registry and Cloud Run. Install the Google Cloud CLI and the Python development dependencies described in the README.

```bash
gcloud auth login
gcloud auth application-default login
```

The CLI uses the first login; the Python GCS client uses application-default credentials. Credentials and local environments are excluded from the image by `.gcloudignore` and `.dockerignore`.

For a new bucket, choose a globally unique name and create it with uniform access:

```bash
gcloud storage buckets create gs://YOUR_BUCKET   --project=YOUR_PROJECT --location=us-central1   --uniform-bucket-level-access --public-access-prevention
```

## Train and deploy

From the repository root with the development environment activated:

```bash
bash scripts/deploy_google_cloud.sh linen-flux-439023-g2 linen-flux-439023-g2-aipi510-m3
```

The script checks prerequisites, uploads or verifies the cleaned panel, trains from its GCS URI, reproduces evaluation, exports MLflow runs, builds the Dockerfile and deploys Cloud Run. It then runs public HTTP checks. For another project, replace both arguments with the project ID and existing bucket name.

The GCS object name includes the dataset SHA-256. Downloads are pinned to an object generation and validated against `config.yaml`. Source details are saved in `artifacts/ingestion.json`; training parameters, metrics and artifact records are exported to `reports/mlflow_runs.json`.

Cloud Run uses port 8080, 512 MiB memory and one CPU, with a zero-instance minimum and one-instance maximum. Standard Google Cloud storage, build and runtime charges apply.

## Verify

The deployed endpoint is <https://main-street-business-explorer-afbeftfbia-uc.a.run.app/predict>. The frontend's API routes forward to this service through `vercel.json`.

```bash
python scripts/http_smoke.py   --base-url https://main-street-business-explorer-afbeftfbia-uc.a.run.app   --output reports/google_cloud_http.json
```

The build ID, image digest and ready revision are recorded in `reports/google_cloud_deployment.json`. See [the results index](../reports/README.md) for experiment, reproduction and HTTP results.

For local training without cloud credentials, use `python -m business_app train --data-uri data/panel.csv`. Add `--output-dir artifacts/local-review` to write a separate result.

Reference: [Cloud Run source deployment](https://docs.cloud.google.com/run/docs/deploying-source-code).
