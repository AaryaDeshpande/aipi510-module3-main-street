#!/usr/bin/env bash
# Existing billing-enabled project and private bucket required. No billing setup.
set -euo pipefail
if [ "$#" -ne 2 ]; then
  echo 'Usage: bash scripts/deploy_google_cloud.sh PROJECT_ID EXISTING_BUCKET' >&2
  exit 2
fi
GCP_PROJECT_ID="$1"
GCS_BUCKET_NAME="$2"
GCP_REGION="us-central1"
GCP_SERVICE="main-street-business-explorer"
export GOOGLE_CLOUD_PROJECT="$GCP_PROJECT_ID"
if [ "$(gcloud billing projects describe "$GCP_PROJECT_ID" --format='value(billingEnabled)')" != 'True' ]; then
  echo 'An existing billing-enabled project is required.' >&2
  exit 1
fi
gcloud storage buckets describe "gs://$GCS_BUCKET_NAME" --project="$GCP_PROJECT_ID" >/dev/null
GCS_OBJECT_NAME="$(python -c 'import yaml; c=yaml.safe_load(open("config.yaml")); print("aipi510-module3/panel-"+c["dataset"]["sha256"]+".csv")')"
export GCS_BUCKET_NAME GCS_OBJECT_NAME
python - <<'PY'
import os
from google.cloud import storage
from business_app.cloud import upload_data
from business_app.data import ROOT, sha256
blob = storage.Client().bucket(os.environ['GCS_BUCKET_NAME']).blob(os.environ['GCS_OBJECT_NAME'])
if blob.exists():
    blob.reload()
    actual = blob.download_as_bytes(if_generation_match=blob.generation)
    if sha256(actual) != sha256((ROOT / 'data/panel.csv').read_bytes()):
        raise SystemExit('Existing object does not match the frozen dataset; refusing overwrite')
else:
    upload_data(os.environ['GCS_BUCKET_NAME'], os.environ['GCS_OBJECT_NAME'])
PY
python -m business_app train --data-uri "gs://$GCS_BUCKET_NAME/$GCS_OBJECT_NAME"
python -m business_app verify
python scripts/export_runs.py
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com --project="$GCP_PROJECT_ID" --quiet
gcloud run deploy "$GCP_SERVICE" --source . --project="$GCP_PROJECT_ID" \
  --region="$GCP_REGION" --allow-unauthenticated --port=8080 \
  --memory=512Mi --cpu=1 --min-instances=0 --max-instances=1 --quiet
GCP_SERVICE_URL="$(gcloud run services describe "$GCP_SERVICE" --project="$GCP_PROJECT_ID" --region="$GCP_REGION" --format='value(status.url)')"
python scripts/http_smoke.py --base-url "$GCP_SERVICE_URL" --output reports/google_cloud_http.json
echo "Verified service: $GCP_SERVICE_URL"
