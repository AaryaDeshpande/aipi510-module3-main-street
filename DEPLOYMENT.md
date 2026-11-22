# Cloud data, containers, and public deployment

Status updated November 22, 2026. This guide distinguishes recorded results from checks still awaiting execution. Use [STATUS.md](STATUS.md) for the current handoff and [SUBMISSION.md](SUBMISSION.md) for the final links.

## 1. Completed cloud storage and model training

The frozen cleaned panel is stored in **Cloudflare R2**. [reports/cloud_storage.json](reports/cloud_storage.json) records successful storage/retrieval responses, **5,799,225 bytes**, verified provider/key/hash/version headers, and a body SHA-256 of `ddef9fbb3835bb981395cc1c77b904d27e899f8f4c75ac97028be31bb5206682`. The actual object version is `7e5dfd2f3a14003c7290b88534de41da`; its key includes the content hash.

The approved authenticated retrieval endpoint is:

```text
https://aarya-main-street-20261122.ad277.chatgpt.site/training-data/panel.csv
```

The endpoint retrieves the R2 object through the review service. Ingestion checks the storage-provider, object-key, content-hash, and nonempty object-version headers and independently hashes the body. The private bearer is read from `SITES_DATA_BEARER`, sent only to this exact endpoint, and omitted from saved run evidence. Redirects are refused. Keep the token out of source, command history, logs, screenshots, and submitted evidence. No token needs to be pasted into a chat or README.

**Actual cloud-ingested training succeeded.** [artifacts/ingestion.json](artifacts/ingestion.json) records the HTTPS source, `storage_provider: cloudflare-r2`, object key/version, matching SHA-256, **110,488 rows**, and `cloud_ingestion_verified: true`. [reports/cloud_training.log](reports/cloud_training.log) contains the successful training output. The cloud-source reproduction passed all 12 checks in `reports/reproducibility.json`; `reports/mlflow_runs.json` exports four actual finished runs. Current training and serving environment evidence is in `reports/environment_checks.json`.

For an authorized cloud rerun, privately set `SITES_DATA_BEARER` in the terminal environment, then use:

```bash
python -m business_app train \
  --data-uri https://aarya-main-street-20261122.ad277.chatgpt.site/training-data/panel.csv
python -m business_app verify
python scripts/export_runs.py
```

The private data endpoint requires that environment variable. Instructors and CI can reproduce the same frozen bytes without credentials using the bundled local snapshot:

```bash
python -m business_app train --data-uri data/panel.csv
python -m business_app verify
```

A local rerun records its actual local source and replaces the artifacts in the selected output directory. Preserve the final cloud-run evidence before running that quickstart. Use `--output-dir` for an exploratory training run if the final artifacts should be retained.

The GCS `upload-data` helper is an alternative implementation retained in the source. Google Cloud Storage and Cloud Run were earlier options; no completed Google Cloud deployment is claimed.

## 2. Build and execute Docker locally

The assignment explicitly asks for actual local Docker execution. A prepared Dockerfile is one part of that requirement. A GitHub Actions run executes containers on a hosted Ubuntu runner; record it as CI evidence and retain a teammate-machine run for the local requirement.

From the reviewed project directory on a machine with Docker running:

```bash
docker build -t main-street-explorer .
mkdir -p container-artifacts
docker run --rm --user "$(id -u):$(id -g)" \
  -v "$PWD/container-artifacts:/output" \
  main-street-explorer train --data-uri data/panel.csv --output-dir /output
docker run --rm -p 8080:8080 \
  -v "$PWD/container-artifacts:/app/artifacts:ro" \
  main-street-explorer
```

These are Linux/macOS volume and user examples. Adapt them to the teammate's Windows Docker setup if needed. The last command serves the artifacts just trained in the container. In another activated terminal:

```bash
python scripts/http_smoke.py --base-url http://127.0.0.1:8080 --output reports/docker_http_smoke.json
curl --fail --silent --show-error http://127.0.0.1:8080/health
curl --fail --silent --show-error \
  -H 'Content-Type: application/json' \
  -d '{"industry":"2382","establishments":100,"previous_establishments":95}' \
  http://127.0.0.1:8080/predict
```

Retain build/train/serve logs, machine/runtime details, exit results, HTTP results, and model/data hashes. Local-snapshot container training tests container execution; the cloud-ingested run in step 1 provides its own evidence. Keep temporary container outputs outside the tracked final artifacts. Stop the serving container after checking it, and rebuild after a final code/model change.

The prepared [Actions workflow](.github/workflows/verify.yml) builds, trains, compares splits/metrics/predictions, serves the new model, performs real HTTP tests, and uploads evidence. Its successful run URL and actual artifact must exist before it is marked passed. It does not deploy or require cloud tokens.

## 3. Deploy the actual Flask service

The current selected route is **Vercel's Flask/Python hosting**. The app exports a Flask instance from `app.py`, uses the inference-only `requirements.txt`, and includes deployment configuration in `vercel.json`. The serving-only environment has loaded the model and passed real Gunicorn HTTP/curl checks with no MLflow requirement; see [reports/serving_only_http.log](reports/serving_only_http.log) and [reports/deployment-runtime-check.json](reports/deployment-runtime-check.json). This establishes local serving readiness.

Vercel is connected, but the current workspace request returns **403 pending the team's permission grant**. The user-facing grant link is short-lived; it is not a deployment URL and is not stored here. After the existing permission grant is completed, deploy the reviewed branch through the connected account and record the actual returned public URL. The [official Vercel Flask guide](https://vercel.com/docs/frameworks/backend/flask) describes the supported Flask entrypoint and dependency configuration.

The runtime package includes the saved model, cleaned panel, financial snapshot, and geometry. It excludes training logs, raw downloads, the IRS source workbook, and private credentials. Static files are mirrored under `public/static` for this host; the recorded local check verifies those copies match the application sources. Inference requires no training-data token. Training should run before packaging the service.

The same public Flask service supplies the frontend and JSON API. Its root is the frontend URL; its `/predict` route is the API URL. Add both actual URLs to README and SUBMISSION.md after verification.

## 4. Verify public access and frontend requests

Use the actual returned HTTPS origin in place of the placeholder below:

```bash
python scripts/http_smoke.py --base-url ACTUAL_HTTPS_SERVICE_URL --output reports/public_http_smoke.json
curl --fail --silent --show-error ACTUAL_HTTPS_SERVICE_URL/health
curl --fail --silent --show-error \
  -H 'Content-Type: application/json' \
  -d '{"industry":"2382","establishments":100,"previous_establishments":95}' \
  ACTUAL_HTTPS_SERVICE_URL/predict
```

Compare the returned model and dataset hashes with the final artifacts. Check signed-out instructor access, then use the actual public webpage on desktop and phone. Observe a successful prediction request initiated by `/market` and useful handling of a failed request. Check ownership case/route controls, IRS year and unknown values, calculator assumptions and owner-labor value, thesis save/export/clear, map filters, histories, and shortlist CSV.

The source years and model limitation must remain visible: observations end in 2023, displayed 2024 estimates are unverified historical estimates, and model test MAE is higher than the no-change baseline. Only record public checks after executing them against the deployed origin.

## 5. Finish team review and submission

Aarya and Tanya are the confirmed partners. Publish the reviewed source through the approved repository workflow, preserve each person's actual authored work, and record meaningful PR URLs in [TEAM_WORKFLOW.md](TEAM_WORKFLOW.md). Both people review the pipeline and limitations.

Complete [REQUIREMENTS.md](REQUIREMENTS.md), fill the real frontend/API links into README, and prepare the Canvas text in [SUBMISSION.md](SUBMISSION.md). Aarya reviews the final repository and public service, then completes the Canvas submission personally. No automated submission is planned. Record the observed Canvas result and timestamp afterward.
