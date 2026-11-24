# Deployment

The application uses three services:

| Service | Role |
|---|---|
| Google Cloud Storage | Versioned cleaned Census panel used for training |
| Google Cloud Run | Dockerized Flask model API |
| Vercel | Frontend hosting and API routing |

The frontend is available at <https://aipi510-module3-main-street.vercel.app/>. Its same-origin API requests are forwarded to <https://main-street-business-explorer-afbeftfbia-uc.a.run.app> by the rewrites in `vercel.json`.

## Google Cloud

Follow [infrastructure/GOOGLE_CLOUD.md](infrastructure/GOOGLE_CLOUD.md) to configure credentials, train from GCS, reproduce evaluation, build the Docker image and deploy Cloud Run.

The deployment script is `scripts/deploy_google_cloud.sh`. The service uses port 8080, 512 MiB memory, one CPU, a minimum of zero instances and a maximum of one. It loads the packaged model and snapshots at startup.

## Frontend

Deploy this repository to the existing Vercel project `aipi510-module3-main-street`, using the Flask framework. The Cloud Run destination is configured in `vercel.json`; update those rewrites if the API URL changes. The public frontend and direct API URLs are linked in the README.

## Validation

```bash
python scripts/http_smoke.py --base-url https://main-street-business-explorer-afbeftfbia-uc.a.run.app --output reports/google_cloud_http.json
python scripts/http_smoke.py --base-url https://aipi510-module3-main-street.vercel.app --output reports/frontend_http.json
```

These checks cover readiness, the frontend, county data/geometry, model hashes, predictions and invalid-input responses. Deployment image/revision details are in [reports/google_cloud_deployment.json](reports/google_cloud_deployment.json); the complete results index is [reports/README.md](reports/README.md).
