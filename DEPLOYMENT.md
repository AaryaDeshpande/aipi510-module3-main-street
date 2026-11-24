# Deployment and reproduction

The canonical cleaned dataset is on **Google Cloud Storage** and the public containerized model API is on **Google Cloud Run**. The submitted frontend URL remains <https://aipi510-module3-main-street.vercel.app/>; explicit API rewrites in `vercel.json` forward requests to Cloud Run.

See [infrastructure/GOOGLE_CLOUD.md](infrastructure/GOOGLE_CLOUD.md) for authentication, existing-project/bucket prerequisites, and the reusable training/reproduction/deployment script. The actual executed component commands and result are recorded in `reports/cloud_upload.json`, `artifacts/ingestion.json`, `reports/gcs_training_20261124.log`, `reports/gcs_reproduction_20261124.log`, `reports/google_cloud_deployment.json`, and `reports/google_cloud_http.json`.

[README.md](README.md) contains Python setup, local training, Docker build/train/serve, real curl requests, and endpoint contracts. For credential-free training use `--data-uri data/panel.csv`; ordinary configured training uses GCS and authorized local application-default credentials. Packaged model serving requires no cloud data credential.

Cloud Build actually built the Dockerfile and Cloud Run successfully deployed the recorded image digest/revision. This is distinct from local Docker execution: Tanya's original report records her pre-migration local run, and GitHub Actions runs actual container training and HTTP reproduction.

Earlier R2/private-Site and Vercel-inference reports are retained as historical evidence. They describe the previous deployment, not the current required-provider architecture. Source/data/model hashes and dates should be used to match an execution to its artifacts.

No billing account was created or linked, and no Canvas change was made during this migration. The existing submitted attempt was read directly. Personal review, Canvas group membership if applicable, and Tanya's original report version entry remain human checks.
