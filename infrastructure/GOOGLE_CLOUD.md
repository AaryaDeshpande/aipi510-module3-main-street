# Google Cloud deployment

The assignment names GCS storage and Cloud Run API hosting. This migration uses the existing project `linen-flux-439023-g2`, region `us-central1`, and private bucket `linen-flux-439023-g2-aipi510-m3`. The owner and existing billing were verified before deployment; no billing account was created or linked.

## Authentication and setup

Use the normal browser sign-in flows yourself when required. Never paste passwords, OAuth codes, tokens, or service-account keys into source or chat.

```bash
gcloud auth login
gcloud auth application-default login
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

The first account needs access to the existing project. The second sign-in supplies Python client-library credentials for GCS. The deployed API loads the packaged model and does not need a dataset token or an ADC file in its image. `.gcloudignore` and `.dockerignore` exclude credentials, local environments, and tracking databases.

The private bucket was created with uniform bucket-level access and public-access prevention:

```bash
gcloud storage buckets create gs://linen-flux-439023-g2-aipi510-m3 \
  --project=linen-flux-439023-g2 --location=us-central1 \
  --uniform-bucket-level-access --public-access-prevention
```

## Train, reproduce, and deploy

From an activated environment in the repository root:

```bash
bash scripts/deploy_google_cloud.sh linen-flux-439023-g2 linen-flux-439023-g2-aipi510-m3
```

The script verifies existing billing, uploads or verifies a content-addressed cleaned dataset, trains from `gs://`, reruns reproduction, exports real MLflow runs, enables the deployment APIs, builds the Dockerfile with Cloud Build, deploys Cloud Run, and checks public HTTP. It never overwrites a different dataset object or creates/links billing. The equivalent component commands were executed during this migration; consult `reports/google_cloud_deployment.json` and the HTTP evidence for the actual result.

GCS downloads pin the recorded object generation and verify the configured SHA-256. `artifacts/ingestion.json` records bucket, object, generation, GCS checksums, source URI, and row count. The selected model and run IDs are in `artifacts/metadata.json`; portable experiment evidence is in `reports/mlflow_runs.json`.

The service scales to zero and has a maximum of one instance. Storage, image storage, builds, and requests can incur usage charges under the existing account. No claim of a guaranteed zero bill is made.

## Public endpoints and validation

The canonical public Cloud Run endpoint and revision are recorded in `reports/google_cloud_deployment.json`. The existing submitted Vercel URL is retained, with API routes forwarded to that Cloud Run service. Confirm the deployed route configuration and real predictions; a prepared rewrite alone is not execution evidence.

For credential-free local reproduction, override the configured cloud source explicitly:

```bash
python -m business_app train --data-uri data/panel.csv --output-dir artifacts/local-review
docker build -t main-street-explorer .
docker run --rm -p 8080:8080 main-street-explorer
```

Training to a separate output preserves the committed cloud-trained artifacts. Use README's Docker training command for a mounted output directory. Tanya's original local Docker report predates this migration; subsequent cloud/CI checks are recorded separately.

Official reference: [Cloud Run source deployment](https://docs.cloud.google.com/run/docs/deploying-source-code). When a Dockerfile exists, source deployment builds that Dockerfile through Cloud Build.
