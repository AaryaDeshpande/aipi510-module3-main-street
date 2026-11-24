# Cloud data, containers, and public deployment

Status updated November 23, 2026. This guide distinguishes recorded results from checks still awaiting execution. Use [STATUS.md](STATUS.md) for the current handoff and [SUBMISSION.md](SUBMISSION.md) for the final links.

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

Build and run the image from the project directory:

```bash
docker build -t main-street-explorer .
mkdir -p container-artifacts
docker run --rm --user "$(id -u):$(id -g)" -v "$PWD/container-artifacts:/output" main-street-explorer train --data-uri data/panel.csv --output-dir /output
docker run --rm -p 8080:8080 -v "$PWD/container-artifacts:/app/artifacts:ro" main-street-explorer
```

Hosted CI and local Docker evidence are retained in `reports/ci/` and `reports/tanya_docker_review.md`. Do not overwrite tracked `artifacts/` during local training.

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

**Hosted Docker CI passed:** [run 45284798476](https://github.com/AaryaDeshpande/aipi510-module3-main-street/actions/runs/45284798476) built the image, trained inside it, reproduced metrics/splits/predictions, served the container-trained model, passed real HTTP/curl checks, and uploaded evidence. Local Docker evidence is in `reports/tanya_docker_review.md`.

The downloaded artifact `14751147208` has verified SHA-256 `4a86198b544bb540f7e7bd787ce21ff39260e2ee2f43b25c7efdc8006012624a`; its provenance and retained reports are in `reports/ci/`. The workflow uses the local frozen snapshot, does not deploy, and needs no cloud tokens.

## 3. Deploy the actual Flask service

The current selected route is **Vercel's Flask/Python hosting**. The app exports a Flask instance from `app.py`, uses the inference-only `requirements.txt`, and includes deployment configuration in `vercel.json`. The serving-only environment has loaded the model and passed real Gunicorn HTTP/curl checks with no MLflow requirement; see [reports/serving_only_http.log](reports/serving_only_http.log) and [reports/deployment-runtime-check.json](reports/deployment-runtime-check.json). This establishes local serving readiness.

**Deployment completed.** Vercel built the actual Flask project from review branch commit `f4e78dbdb72bf78c4f49586b89a317eb72b5d0f6` and reports deployment `dpl_AkkQfyWPFsSXYMBsffBJPYH2ncQD` as READY. Build logs confirm GitHub cloning, Python 3.12, pinned dependency installation, completed build, and deployed outputs. Stable public origin: <https://aipi510-module3-main-street.vercel.app/>. The unique build URL requires Vercel authentication; signed-out access to the stable production origin works. No login-protection change was applied. See `reports/final_release_review.json` for the current deployment; `reports/public_deployment.json` retains the previous deployment evidence.

The runtime package includes the saved model, cleaned panel, financial snapshot, and geometry. It excludes training logs, raw downloads, the IRS source workbook, and private credentials. Static files are mirrored under `public/static` for this host; the recorded local check verifies those copies match the application sources. Inference requires no training-data token. Training should run before packaging the service.

The same Flask service supplies the frontend at <https://aipi510-module3-main-street.vercel.app/> and JSON POST API at <https://aipi510-module3-main-street.vercel.app/predict>. Both are recorded in README and SUBMISSION.md with executed public checks.

## 4. Verify public access and frontend requests

The following smoke command was executed successfully against the stable production domain:

```bash
python scripts/http_smoke.py --base-url https://aipi510-module3-main-street.vercel.app --output reports/public_http_smoke.json
curl --fail --silent --show-error https://aipi510-module3-main-street.vercel.app/health
curl --fail --silent --show-error \
  -H 'Content-Type: application/json' \
  -d '{"industry":"2382","establishments":100,"previous_establishments":95}' \
  https://aipi510-module3-main-street.vercel.app/predict
```

Compare the returned model and dataset hashes with the final artifacts. Check signed-out instructor access, then use the actual public webpage on desktop and phone. Observe a successful prediction request initiated by `/market` and useful handling of a failed request. Check ownership case/route controls, IRS year and unknown values, calculator assumptions and owner-labor value, thesis save/export/clear, map filters, histories, and shortlist CSV.

The source years and model limitation must remain visible: observations end in 2023, displayed 2024 estimates are unverified historical estimates, and model test MAE is higher than the no-change baseline. Only record public checks after executing them against the deployed origin.

Public Flask deployment and signed-out HTTP checks now pass at <https://aipi510-module3-main-street.vercel.app>. Live desktop checks cover ownership controls, calculator with owner labor, thesis save/restore/export/clear, county filters, unknown cells, a real browser prediction, and shortlist CSV download. See `reports/public_http_smoke.json`, `reports/public_deployment.json`, and `reports/public_browser_checks.json`. Phone/device review and a simulated frontend request failure remain unexecuted.

# Deployment and verification

## Public deployment

- Frontend/API: <https://aipi510-module3-main-street.vercel.app/>
- Cloud storage: Cloudflare R2
- Public evidence: `reports/public_http_smoke.json`
- Docker evidence: `reports/tanya_docker_review.md`

## Docker reproduction

Build and run the image from the project directory:

```bash
docker build -t main-street-explorer .
mkdir -p container-artifacts
docker run --rm --user "$(id -u):$(id -g)" -v "$PWD/container-artifacts:/output" main-street-explorer train --data-uri data/panel.csv --output-dir /output
docker run --rm -p 8080:8080 -v "$PWD/container-artifacts:/app/artifacts:ro" main-street-explorer
```

Keep temporary container artifacts outside the tracked `artifacts/` directory.

## Remaining actions

- Confirm provider interpretation.
- Tanya commits and opens a PR for the completed Docker review.
- Aarya completes team review and final Canvas submission.
