# Main Street Business Explorer

A research workspace for understanding ordinary-business economics, comparing routes to ownership, and writing a testable ownership thesis. A supporting Wisconsin market explorer provides geographic context and the reproducible supervised-learning experiment for AIPI 510 Module Project 3.

Phone review: <https://aarya-main-street-20261122.ad277.chatgpt.site/> (owner-private ChatGPT sign-in). This review uses an exported model on a JavaScript hosting service. It does not complete the required public Flask deployment or the other outstanding course gates.

The homepage uses dated company examples to explain customers, repeat purchases, costs, operating advantages, and entry barriers. These are explanatory cases, not recommended investments or evidence of a particular founder's likely outcome. Its scenario calculator performs editable arithmetic; it does not predict income. The thesis worksheet stores only in the browser and sends no outreach.

The economics context is a separately audited IRS 2023 Wisconsin Schedule C snapshot with 32 selected industry groups. Its source workbook is included at `data/economics_source.xlsx`; regenerate with `python scripts/prepare_economics.py` after installing development dependencies. `config.yaml` pins the JSON snapshot hash. Dollar units, suppressed values, owner-labor treatment, filing-address geography, and aggregate-mean limits are explicit. The financial snapshot is not an input to the CBP prediction model. A state-industry margin model was explored separately and is not claimed as a validated opportunity predictor.

**Current review status, November 22:** actual R2 storage, cloud-ingested training, 61 tests, reproduction, and hosted Docker CI are verified. The 85-file implementation is uploaded on the [review branch](https://github.com/AaryaDeshpande/aipi510-module3-main-street/tree/aarya/module3-implementation); [draft PR #1](https://github.com/AaryaDeshpande/aipi510-module3-main-street/pull/1) contains the authorized AI-assisted work and awaits Aarya’s personal review and approval before merge. Default `main` still contains initialization content, so use the branch or draft PR to review this version. Tanya’s own meaningful PR, both partners’ review, teammate-machine Docker execution, and public Flask deployment remain open. Vercel’s workspace grant is still pending. See [STATUS.md](STATUS.md) and [REQUIREMENTS.md](REQUIREMENTS.md).

## Submission links

- GitHub repository: <https://github.com/AaryaDeshpande/aipi510-module3-main-street>; current implementation: [review branch](https://github.com/AaryaDeshpande/aipi510-module3-main-street/tree/aarya/module3-implementation) and [draft PR #1](https://github.com/AaryaDeshpande/aipi510-module3-main-street/pull/1) (personal review and instructor-access check pending)
- Successful Docker CI: [run 45013764218](https://github.com/AaryaDeshpande/aipi510-module3-main-street/actions/runs/45013764218)
- Live frontend: **PENDING deployment**
- Deployed prediction API: **PENDING deployment**, endpoint `/predict`
- [Canvas assignment](https://canvas.duke.edu/courses/83524/assignments/363937)
- Previously verified due time: **November 24, 2026, 11:30 am Eastern / 10:30 am Central**. Personal target: Sunday November 22. Fresh Canvas access is currently sign-in blocked; the source audit records that limit.

The same Flask service serves the frontend and JSON API. Its public root URL provides the frontend, and the browser calls `/predict` on that host.

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

Current executed checks on November 22: **61 tests passed** (`reports/pytest.txt`), all **12 cloud-source reproduction checks passed** (`reports/reproducibility.json`), and **four actual MLflow runs finished** (`reports/mlflow_runs.json`). Training and inference-only environments both pass `pip check`; the fresh inference-only environment loads the saved model without MLflow and passes real Gunicorn HTTP/curl checks (`reports/serving_only_http.log`). The current evidence summary is `reports/environment_checks.json`; the earlier 40-test run is retained separately in `reports/environment_checks_earlier.json`. Desktop browser flows are recorded in `reports/browser_checks.json` and `reports/ownership_browser_checks.json`. Hosted Docker execution now passes as described below. Final teammate-machine Docker, live public/phone, and public Flask checks remain open.

The latest live-browser attempt stopped at the private Site’s ChatGPT sign-in gate (`reports/final_ui_check.json`). Final live ownership controls, export, calculator, market predictions, and phone layout were not rechecked. The earlier local desktop QA reports remain dated evidence.

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

The cleaned panel is stored in **Cloudflare R2**, with actual storage/download and body/header checks in `reports/cloud_storage.json`. **Cloud-ingested training succeeded**: `artifacts/ingestion.json` records the authenticated HTTPS endpoint, provider, content-addressed object key, version `7e5dfd2f3a14003c7290b88534de41da`, 110,488 rows, the pinned hash, and `cloud_ingestion_verified: true`. `reports/cloud_training.log` contains the successful run.

Cloud retraining requires `SITES_DATA_BEARER` to be set privately in the terminal environment. The token is read only for the exact approved endpoint, redirects are refused, and it is excluded from recorded evidence. Do not paste it into chat, source, or logs. The bundled local snapshot is the credential-free reproduction and CI route. See [DEPLOYMENT.md](DEPLOYMENT.md) for both commands and the final reproduction/export checks. Ordinary HTTPS alone is not claimed as verified cloud storage; the approved endpoint additionally identifies the R2 object and its version.

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

The commands are Linux/macOS examples. Windows users should adapt volume/user syntax to their Docker setup. The hosted Actions run below passed actual container execution. The assignment's local build/run wording still calls for a teammate-machine run and recorded results.

**Hosted Docker CI passed:** [run 45013764218](https://github.com/AaryaDeshpande/aipi510-module3-main-street/actions/runs/45013764218) built the image, trained inside it, reproduced metrics/splits/predictions, served the container-trained model, passed real HTTP/curl checks, and uploaded evidence. The tested commit is `520e0d1b3b52d80173ef2920a663943784aab8a3`. `reports/ci_observation.json` records the successful job, and `reports/ci/` retains downloaded execution evidence. This establishes hosted Ubuntu execution; a teammate-machine Docker run remains separate.

The [workflow](.github/workflows/verify.yml) uses Python 3.12 and pinned development dependencies, runs the full tests and Docker checks, and uploads real evidence. The downloaded artifact `14751147208` was verified against SHA-256 `4a86198b544bb540f7e7bd787ce21ff39260e2ee2f43b25c7efdc8006012624a`; provenance is in `reports/ci/artifact_provenance.json`. It uses the frozen local panel and no cloud credentials. The actual R2-ingested run is documented separately.

The actual training-data service is Cloudflare R2 behind the authenticated review endpoint. The selected public Flask/API route is Vercel; its workspace permission grant is pending after a 403 response. No final public Flask URL is claimed. The packaged inference service needs no training-data token. Earlier GCS/Cloud Run options remain alternatives, and their completion is not claimed. See [DEPLOYMENT.md](DEPLOYMENT.md).

## Files and authorship

`business_app/prepare.py` freezes official data; `data.py` validates ingestion and joins consecutive years; `train.py` handles preprocessing, chronological selection/evaluation, and tracking; `web.py` implements the public contracts. `templates/` and `static/` implement the visual explorer; `tests/`, verification scripts, and `reports/` capture checks as they are executed. The requirement audit, deployment guide, and team checklist document open work.

This original business application was prepared with AI assistance. It reuses engineering patterns/helpers from the separate local Iris review implementation prepared in this conversation: data hashing, a CLI, MLflow tracking, saved-artifact serving, and Docker structure. The business cleaning, regression target, chronological evaluation, geography, and visual research workflow are project-specific additions. No Iris accuracy or test result is evidence for this model.

Earlier learning source: [Aarya's Week 12 Iris pipeline](https://github.com/AaryaDeshpande/aipi510-week12-ml-pipeline), notebook blob SHA `cce4e60e1ecf3a3bc01b94cc2c5d7f94ad5888f6`. Its use of scikit-learn pipelines and separate evaluation motivated the workflow; the present model is a different regression experiment. Cite any further external snippets/templates and record real authorship. The syllabus recommends AI citation and requires citation of reused external code.

Earlier research source: [Aarya's Module 1 national local-service market screen](https://github.com/AaryaDeshpande/aipi510-module1-local-service-market-screen). That project provides prior market-screening research and context. The Module 3 regression target, chronological splits, model training, experiment tracking, and serving pipeline are distinct work; Module 1 results are not evidence for this model.

**Confirmed teammates: Aarya Deshpande and Tanya**, as confirmed by Aarya. The authorized AI-assisted implementation is in [Aarya’s draft PR #1](https://github.com/AaryaDeshpande/aipi510-module3-main-street/pull/1); Aarya’s personal review and merge approval remain pending. Tanya’s GitHub handle, own meaningful PR, and both partners’ review remain pending. The prepared implementation is AI assisted; no completed human contribution is attributed without evidence. See [TEAM_WORKFLOW.md](TEAM_WORKFLOW.md) for the contribution record and [SUBMISSION.md](SUBMISSION.md) for the final review checklist. Both partners should review the work and explain their contributions. Aarya completes the final Canvas submission after review; no automatic submission is planned.
