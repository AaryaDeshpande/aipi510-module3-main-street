# Main Street Business Explorer

A reproducible supervised-learning project for AIPI 510 Module Project 3: predict next-year county–industry establishment counts from earlier observations, evaluate against persistence, and serve the saved model through a public Flask API and Wisconsin data explorer. A supplementary worksheet explores business economics.

`/` opens the deployed ML research view; `/market` provides the same explorer and `/ownership` preserves the supplementary worksheet.

Live Flask application: <https://aipi510-module3-main-street.vercel.app/> — publicly accessible without signing in. Open <https://aipi510-module3-main-street.vercel.app/market> for the county explorer and real JSON prediction client. The earlier owner-private ChatGPT Site is retained only as a review surface and cloud-data retrieval service.

The supplementary ownership worksheet uses dated company examples to explain customers, repeat purchases, costs, operating advantages, and entry barriers. These are explanatory cases, not recommended investments or evidence of a particular founder's likely outcome. Its scenario calculator performs editable arithmetic; it does not predict income. The thesis worksheet stores only in the browser and sends no outreach.

The economics context is a separately audited IRS 2023 Wisconsin Schedule C snapshot with 32 selected industry groups. Its source workbook is included at `data/economics_source.xlsx`; regenerate with `python scripts/prepare_economics.py` after installing development dependencies. `config.yaml` pins the JSON snapshot hash. Dollar units, suppressed values, owner-labor treatment, filing-address geography, and aggregate-mean limits are explicit. The financial snapshot is not an input to the CBP prediction model. A state-industry margin model was explored separately and is not claimed as a validated opportunity predictor.

**Audit, November 24, 2026:** the cleaned data has been uploaded to **Google Cloud Storage**, the pipeline has actually trained from that GCS object, and the Docker API is publicly deployed on **Google Cloud Run**. All **62 tests**, **12 cloud-source reproduction checks**, four new MLflow runs, and public Cloud Run HTTP checks passed. The submitted Vercel frontend URL is retained; its API routes forward to Cloud Run. Both partner-authored PRs exist, and this integration includes Tanya's original commits. Canvas already showed the submitted repository/frontend links; this audit made no Canvas changes. See [REQUIREMENTS.md](REQUIREMENTS.md) and the [audit](reports/submission_audit_20261124.md).

## Submission links

- GitHub repository: <https://github.com/AaryaDeshpande/aipi510-module3-main-street>
- Implementation branch: <https://github.com/AaryaDeshpande/aipi510-module3-main-street/tree/aarya/module3-implementation>
- Aarya implementation PR (merged): <https://github.com/AaryaDeshpande/aipi510-module3-main-street/pull/1>
- Tanya contribution PR (merged into implementation branch): <https://github.com/AaryaDeshpande/aipi510-module3-main-street/pull/2>
- Live frontend: <https://aipi510-module3-main-street.vercel.app/>
- Canonical Cloud Run API: <https://main-street-business-explorer-afbeftfbia-uc.a.run.app/predict> (JSON POST; example below)
- Same-origin frontend API proxy: <https://aipi510-module3-main-street.vercel.app/predict>
- [Actual Google Cloud build/revision evidence](reports/google_cloud_deployment.json)
- Current-main Docker CI: <https://github.com/AaryaDeshpande/aipi510-module3-main-street/actions/runs/45292395651>
- Tanya's [local Docker report](reports/tanya_docker_review.md)
- [Canvas assignment](https://canvas.duke.edu/courses/83524/assignments/363937); last recorded deadline: November 24, 2026, 10:30 am Central / 11:30 am Eastern. Confirm current Canvas state personally.

Vercel serves the submitted frontend URL. The browser calls same-origin `/predict`, and Vercel forwards that request to the public Cloud Run API through explicit rewrites. The Cloud Run service also serves the custom Flask interface directly.

## What you can do with it

Choose one of ten service categories and a county. A Census-based county map shows reported establishment counts, annual payroll, or year-over-year growth. Inspect the 2019–2023 history, compare the same category across counties or different categories in one county, and save selections to a browser-local research shortlist with CSV export.

Each category includes an explicitly unverified workflow hypothesis and interview questions about frequency, cost, existing workarounds, buyer authority, and what a paid pilot would need to prove. These help organize research. The tool does not establish customer demand or willingness to pay, and a large or growing category can also have substantial competition. Shortlists stay in the current browser; there is no shared lead database or automatic outreach.

## Official data and cleaning

The frozen panel contains **110,488 county–industry–year rows** from official U.S. Census **County Business Patterns (CBP), 2019–2023**, using ten exact four-digit **2017 NAICS** industry aggregates. Training uses complete national histories; the visual explorer focuses on Wisconsin. The latest Wisconsin view has 72 counties × 10 categories = 720 possible cells, with **637 published 2023 observations**. Unavailable cells remain unknown.

Sources: [CBP datasets](https://www.census.gov/programs-surveys/cbp/data/datasets.html), [methodology](https://www.census.gov/programs-surveys/cbp/technical-documentation/methodology.html), [definitions](https://www.census.gov/programs-surveys/cbp/about/glossary.html), [2023 Gazetteer files](https://www.census.gov/geographies/reference-files/time-series/geo/gazetteer-files.2023.html), and [Census TIGERweb](https://tigerweb.geo.census.gov/). `data/SOURCE.json` contains the exact download URLs, source hashes, cleaning counts, geometry provenance, and limitations. Wisconsin polygons are genuine, simplified Census geometry; they are display data and are excluded from the model.

Cleaning preserves FIPS and industry codes as strings, excludes statewide/unknown-county rows, keeps only the chosen industry aggregate levels, rejects duplicates/invalid counts, and joins matching county/industry identifiers across consecutive years. It converts payroll from thousands of dollars to dollars. Published employment/payroll values retain their G/H/J disclosure-noise flags; unknown magnitudes stay null. Missing cells are not filled with zero or reconstructed by subtraction.

CBP covers establishments with paid employees. Establishments are business locations, and one company can have several. Nonemployer businesses are outside this source. Payroll measures wages paid to employees. It is not revenue, profit, or owner net worth. Dates, reporting limitations, and missingness remain visible in the interface.

## Prediction task and honest evaluation

The model estimates the following year's establishment count from industry, current count, and previous-year count. It learns relative change `(next − current) / (current + 1)` using Ridge regression. Its pipeline creates log-count and lag-growth features, standardizes numeric features, and one-hot encodes industry. Learned preprocessing is fitted only on training rows.

| Split | Input counts | Target year | Complete rows |
|---|---|---:|---:|
| Training | 2019 and 2020 | 2021 | 21,258 |
| Validation | 2020 and 2021 | 2022 | 21,132 |
| Held-out test | 2021 and 2022 | 2023 | 21,224 |

Validation MAE selects among Ridge alpha values 1, 10, and 100; ties choose stronger regularization. Alpha 1 was selected. The model stays fitted on the training split and is not refitted on validation or test rows. Existing county–industry entities can appear in successive periods, appropriate for forecasting their later counts; generalization to unseen places has not been established.

| Count-space measure | Model | No-change baseline |
|---|---:|---:|
| Validation MAE | 3.4101 | 3.6320 |
| Held-out test MAE | **3.0594** | **2.9016** |
| Held-out test RMSE | 8.6409 | 9.0990 |
| Held-out test median absolute error | 1.2709 | 1.0000 |

The baseline carries the input count forward unchanged. The model's held-out MAE is **5.4% worse** than this baseline, despite its lower RMSE. Therefore the experiment does not demonstrate improved average absolute forecasting error. This negative result is retained in the app and metadata. The observed Census map, histories, and shortlist remain useful for organizing research independently of forecasting performance.

The API's **2024 estimates use 2023 and 2022 counts**. They are unverified historical estimates. They are not a 2026 nowcast. Complete-case selection, unpublished small cells, geographic changes, and pandemic/recovery-era dynamics limit interpretation. `artifacts/metadata.json`, `split_ids.json`, and `test_predictions.csv` preserve the exact run evidence.

Splits separate reference years. Because Census publishes these observations after the reference year, this experiment is not a simulated real-time forecasting backtest. The Wisconsin-only held-out subset has 617 complete histories: model MAE 2.2174 and persistence MAE 1.9951. Those local errors are also visible in the interface.

The November 24 audit independently confirmed 17 public-HTTP and recorded-artifact checks, including three real predictions, invalid-input handling, deployed model/data hashes, and recomputed MAE. A browser prediction displayed 281.2 versus a no-change baseline of 276 for Dane County/building-equipment contractors. Evidence: `reports/submission_http_audit_20261124.json`. The auditor reran 62 Python tests and cloud-source training on this Mac, and built Docker through Cloud Build; Docker itself was not run locally on this Mac. Tanya's PR records local Docker execution; her report lists pandas 2.3.5, while the Docker requirements pin 2.2.3. Tanya should confirm that entry from her original output. Her original evidence has been preserved unchanged. Earlier dated reports remain historical evidence, not a current status checklist.

## Run locally

Use Python 3.12 from the project directory. On Windows, activate `.venv\Scripts\activate` instead.

`requirements.txt` installs the inference-only environment for serving existing artifacts. `requirements-train.txt` adds the training and MLflow dependencies. `requirements-dev.txt` includes training dependencies, pytest, and the IRS workbook tools. The full development setup below can train, test, and serve.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m business_app train --data-uri data/panel.csv
python -m pytest -q
python -m business_app verify
python scripts/export_runs.py
python -m business_app serve
```

The quickstart intentionally trains from the bundled local snapshot and records that local source. It requires no cloud token and replaces artifacts in the configured output directory; preserve final cloud-run evidence before rerunning. Cloud retraining uses the private endpoint and environment variable described below.

Open <http://localhost:8080>. In another activated terminal:

```bash
python scripts/http_smoke.py --base-url http://localhost:8080 --output reports/local_http_smoke.json
curl --fail --silent --show-error \
  -H 'Content-Type: application/json' \
  -d '{"industry":"2382","establishments":100,"previous_establishments":95}' \
  http://localhost:8080/predict
```

For an isolated local HTTP check that starts and stops its own serving process, run `python scripts/check_http_local.py` (requires curl). It writes actual request evidence to `reports/`.

The API accepts exactly those three fields. Industry is one of the ten documented string codes; counts must be whole published counts from 3 through 1,000,000. For the frozen model, interpret them as 2023 and 2022 counts. The response includes `prediction`, the no-change `baseline`, `target_year`, `as_of_year`, model hash, and evaluation notice. Predictions can be fractional estimates. Invalid fields/values return HTTP 422, non-JSON returns 415, malformed JSON returns 400, and requests over 16 KB return 413.

Other routes: `/market` opens the supporting map and actual prediction client; `/api/economics` serves the audited IRS snapshot; `/health` identifies the loaded hashes, `/metadata` gives model information, `/api/data` provides the frozen Wisconsin market records, and `/api/geo` serves the county geometry.

Routine training uses the included 5.8 MB `data/panel.csv` snapshot. `python -m business_app prepare` deliberately rebuilds it from the official sources and freezes source hashes. It can download roughly 60 MB of archives plus geography; raw caches are excluded from Git/Docker. After any deliberate source change, review provenance, update the configured dataset hash to the reviewed snapshot if needed, and rerun the full checks.

## Cloud ingestion and experiment tracking

The cleaned panel is stored in **Google Cloud Storage** in private bucket `linen-flux-439023-g2-aipi510-m3`. Actual upload/download SHA-256 verification is in `reports/cloud_upload.json`. **GCS-sourced training succeeded**: `artifacts/ingestion.json` records the `gs://` URI, bucket, object generation, checksums, 110,488 rows, and verified source. `config.yaml` now defaults to that GCS object. The loader pins the object generation during download and checks its SHA-256.

Run `gcloud auth application-default login` through Google's normal browser flow for authorized cloud retraining, then `python -m business_app train`. For credential-free reproduction, explicitly use `--data-uri data/panel.csv`. The packaged inference service needs no training-data credential. See [infrastructure/GOOGLE_CLOUD.md](infrastructure/GOOGLE_CLOUD.md) and the deployment script. Earlier R2 reports preserve the previous provider's historical execution; R2 is no longer the canonical training source.

Real MLflow runs record the three validation candidates and the final selected-model evaluation, including data/code hashes, split periods/counts, alpha, metrics, and saved model/evaluation artifacts. Inspect a locally regenerated tracking store:

```bash
python -m mlflow ui --backend-store-uri sqlite:///artifacts/tracking/mlflow.db --host 127.0.0.1 --port 5000
python scripts/export_runs.py
```

The export in `reports/mlflow_runs.json`, when generated, is portable. MLflow's historical artifact paths are machine-specific. After moving the project, run training to create a tracking store at the new path. Tracking databases and raw downloads are excluded from Git and the image.

## Containers and deployment

The Docker image runs as a nonroot user and exposes one CLI with `train` and `serve` entry points. `serve` starts Gunicorn on `PORT` and loads the saved model, panel, and map snapshot. Model, panel, and geometry hashes are checked before serving. Load only this team's own controlled joblib artifact, since joblib files can execute code.

```bash
docker build -t main-street-explorer .
docker run --rm -p 8080:8080 main-street-explorer
```

In another terminal, run the HTTP smoke command above against the container. Check the training entry point separately, explicitly using the included snapshot and writing outputs to a mounted host directory:

```bash
mkdir -p container-artifacts
docker run --rm --user "$(id -u):$(id -g)" \
  -v "$PWD/container-artifacts:/output" \
  main-street-explorer train --data-uri data/panel.csv --output-dir /output
```

The commands are Linux/macOS examples. Windows users should adapt volume/user syntax to their Docker setup. Docker build, training, serving, and HTTP results are in `reports/tanya_docker_review.md`.

**Hosted Docker CI passed:** [run 45284798476](https://github.com/AaryaDeshpande/aipi510-module3-main-street/actions/runs/45284798476) built the image, trained inside it, reproduced metrics/splits/predictions, served the container-trained model, passed real HTTP/curl checks, and uploaded evidence. Local Docker reproduction is recorded in `reports/tanya_docker_review.md`.

The [workflow](.github/workflows/verify.yml) uses Python 3.12 and pinned development dependencies, runs the full tests and Docker checks, and uploads real evidence. The downloaded artifact `14751147208` was verified against SHA-256 `4a86198b544bb540f7e7bd787ce21ff39260e2ee2f43b25c7efdc8006012624a`; provenance is in `reports/ci/artifact_provenance.json`. It uses the frozen local panel and no cloud credentials. The actual GCS-ingested run is documented separately; older R2 evidence is historical.

The public model API runs on **Google Cloud Run** at <https://main-street-business-explorer-afbeftfbia-uc.a.run.app/predict>. Cloud Build used the repository Dockerfile; the build ID, immutable image digest, ready revision, and real HTTP results are recorded in `reports/google_cloud_deployment.json` and `reports/google_cloud_http.json`. The API scales to zero with a maximum of one instance under the existing billing-enabled project. The Vercel frontend remains at <https://aipi510-module3-main-street.vercel.app/> and proxies `/predict`, `/health`, `/metadata`, and `/api/*` to Cloud Run using `vercel.json`. Direct Cloud Run also serves the custom Flask UI. See [infrastructure/GOOGLE_CLOUD.md](infrastructure/GOOGLE_CLOUD.md).

## Files and authorship

`business_app/prepare.py` freezes official data; `data.py` validates ingestion and joins consecutive years; `train.py` handles preprocessing, chronological selection/evaluation, and tracking; `web.py` implements the public contracts. `templates/` and `static/` implement the visual explorer; `tests/`, verification scripts, and `reports/` capture checks as they are executed. The requirement audit, deployment guide, and team checklist document open work.

This original business application was prepared with AI assistance. It reuses engineering patterns/helpers from the separate local Iris review implementation prepared in earlier work: data hashing, a CLI, MLflow tracking, saved-artifact serving, and Docker structure. The business cleaning, regression target, chronological evaluation, geography, and visual research workflow are project-specific additions. No Iris accuracy or test result is evidence for this model.

Earlier learning source: [Aarya's Week 12 Iris pipeline](https://github.com/AaryaDeshpande/aipi510-week12-ml-pipeline), notebook blob SHA `cce4e60e1ecf3a3bc01b94cc2c5d7f94ad5888f6`. Its use of scikit-learn pipelines and separate evaluation motivated the workflow; the present model is a different regression experiment. Cite any further external snippets/templates and record real authorship. The syllabus recommends AI citation and requires citation of reused external code.

Earlier research source: [Aarya's Module 1 national local-service market screen](https://github.com/AaryaDeshpande/aipi510-module1-local-service-market-screen). That project provides prior market-screening research and context. The Module 3 regression target, chronological splits, model training, experiment tracking, and serving pipeline are distinct work; Module 1 results are not evidence for this model.

**Team:** Aarya Deshpande and Tanya Sharma (`Tanya-duke`). Status and instructions are in [TEAM_WORKFLOW.md](TEAM_WORKFLOW.md) and [TANYA_START_HERE.md](TANYA_START_HERE.md).
