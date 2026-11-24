# Main Street Business Explorer

**Aarya Deshpande and Tanya Sharma · Duke AIPI 510**

Explore historical Wisconsin business data and estimate next-year establishment counts with a reproducible machine-learning pipeline.

- **Application:** <https://aipi510-module3-main-street.vercel.app/>
- **Prediction API:** <https://main-street-business-explorer-afbeftfbia-uc.a.run.app/predict> — JSON POST
- **Deployment guide:** [DEPLOYMENT.md](DEPLOYMENT.md)
- **Experiment and verification results:** [reports/](reports/README.md)

The frontend compares county histories, maps establishment counts, payroll and growth, and saves research shortlists with CSV export. Its prediction button sends a request through Vercel to the Flask API on Google Cloud Run.

## Data

The dataset contains **110,488 county–industry–year observations** from U.S. Census **County Business Patterns, 2019–2023**, covering ten four-digit 2017 NAICS service categories. Model training uses national data; the explorer displays Wisconsin's 72 counties. Of 720 possible county/category cells, 637 have published 2023 observations.

Sources: [CBP datasets](https://www.census.gov/programs-surveys/cbp/data/datasets.html), [methodology](https://www.census.gov/programs-surveys/cbp/technical-documentation/methodology.html), [definitions](https://www.census.gov/programs-surveys/cbp/about/glossary.html), [2023 Gazetteer files](https://www.census.gov/geographies/reference-files/time-series/geo/gazetteer-files.2023.html), and [TIGERweb geometry](https://tigerweb.geo.census.gov/). Download URLs, checksums and cleaning details are recorded in [data/SOURCE.json](data/SOURCE.json).

Preprocessing preserves county and industry identifiers as strings, selects consistent industry aggregates, removes invalid and duplicate observations, and joins consecutive years. Missing or suppressed cells remain unknown. Payroll is converted from thousands of dollars to dollars; employment and payroll retain their disclosure/noise flags. Geometry is used for display, not as a model feature.

The cleaned panel is stored in **Google Cloud Storage**. `config.yaml` specifies its URI and SHA-256. The reader pins the GCS object generation and validates the downloaded content. [artifacts/ingestion.json](artifacts/ingestion.json) records the object version, checksums and row count.

The supplementary `/ownership` worksheet uses a separate IRS 2023 Wisconsin Schedule C snapshot with 32 industry groups. Its source workbook is `data/economics_source.xlsx`; regenerate it with `python scripts/prepare_economics.py`. The worksheet provides context and editable arithmetic and is separate from the prediction model.

## Model and evaluation

The supervised regression task is to predict the following year's establishment count from industry, current count and previous-year count. Ridge regression learns relative change, `(next − current) / (current + 1)`, which is converted back into a count estimate. Features include log counts, lagged growth and one-hot industry indicators. Numeric scaling and encoding are fitted on training data only.

| Split | Input years | Target year | Rows |
|---|---|---:|---:|
| Training | 2019–2020 | 2021 | 21,258 |
| Validation | 2020–2021 | 2022 | 21,132 |
| Test | 2021–2022 | 2023 | 21,224 |

Validation MAE selects among alpha values 1, 10 and 100; alpha 1 was selected. The selected model remains fitted on the training split.

| Metric | Ridge model | Persistence baseline |
|---|---:|---:|
| Validation MAE | 3.4101 | 3.6320 |
| Test MAE | **3.0594** | **2.9016** |
| Test RMSE | 8.6409 | 9.0990 |
| Test median absolute error | 1.2709 | 1.0000 |

Persistence predicts no change from the current count. The model's test MAE is **5.4% higher** than persistence, despite lower RMSE, so this experiment does not demonstrate improved average absolute forecasting error. The interface reports both results.

Four MLflow runs record the three validation candidates and final evaluation, including parameters, metrics, dataset/code hashes and model artifacts. The portable export is [reports/mlflow_runs.json](reports/mlflow_runs.json). Saved metadata, split IDs and held-out predictions are in `artifacts/`.

## Local setup

Use Python 3.12. On Windows, activate `.venv\Scripts\activate` instead.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m business_app serve
```

Open <http://localhost:8080>. Serving loads the included model and snapshots. `requirements.txt` provides serving dependencies, `requirements-train.txt` adds training and MLflow, and `requirements-dev.txt` adds tests and workbook tools.

### Train and reproduce

For local training from the bundled snapshot:

```bash
python -m business_app train --data-uri data/panel.csv
python -m business_app verify
python scripts/export_runs.py
```

Training replaces the contents of `artifacts/`. Use `--output-dir artifacts/local-review` to write a separate training result. Without `--data-uri`, training uses the configured GCS source and requires Google application-default credentials; see [Google Cloud setup](infrastructure/GOOGLE_CLOUD.md).

To inspect a locally generated MLflow tracking store:

```bash
python -m mlflow ui --backend-store-uri sqlite:///artifacts/tracking/mlflow.db --host 127.0.0.1 --port 5000
```

Tracking databases and raw downloads are excluded from Git. `python -m business_app prepare` rebuilds the panel from official sources; source changes require updating the configured checksum and regenerating model artifacts.

### Test the API

With the server running:

```bash
curl --fail --silent --show-error \
  -H 'Content-Type: application/json' \
  -d '{"industry":"2382","establishments":100,"previous_establishments":95}' \
  http://localhost:8080/predict

python scripts/http_smoke.py --base-url http://localhost:8080 --output reports/local_http_smoke.json
```

The response includes `prediction`, `baseline`, `target_year`, `as_of_year`, and `model_sha256`. Industry must be one of the ten supported string codes. Both counts must be whole numbers from 3 to 1,000,000. Invalid values return 422; non-JSON returns 415; malformed JSON returns 400; requests over 16 KB return 413.

| Route | Purpose |
|---|---|
| `/` or `/market` | County explorer and prediction interface |
| `/predict` | JSON model inference |
| `/health` | Service readiness and loaded model/data hashes |
| `/metadata` | Model configuration, evaluation and limitations |
| `/api/data` | Wisconsin county/category observations |
| `/api/geo` | County geometry |
| `/ownership` and `/api/economics` | Supplementary worksheet and financial snapshot |

`python scripts/check_http_local.py` starts a temporary Gunicorn server, runs HTTP and curl checks, and stops the process.

## Docker

The image runs as a nonroot user and supports both training and serving. Serving starts Gunicorn on `PORT`, defaulting to 8080.

```bash
docker build -t main-street-explorer .
docker run --rm -p 8080:8080 main-street-explorer
```

For container training with a mounted output directory:

```bash
mkdir -p container-artifacts
docker run --rm --user "$(id -u):$(id -g)" \
  -v "$PWD/container-artifacts:/output" \
  main-street-explorer train --data-uri data/panel.csv --output-dir /output
```

These volume/user commands use Linux/macOS syntax. Model, dataset and geometry checksums are validated before serving.

## Deployment and verification

**GCS → training and MLflow → saved model → Cloud Run API → Vercel frontend**

[DEPLOYMENT.md](DEPLOYMENT.md) describes the architecture and [infrastructure/GOOGLE_CLOUD.md](infrastructure/GOOGLE_CLOUD.md) provides setup and deployment commands. Vercel forwards `/predict`, `/health`, `/metadata` and `/api/*` to Cloud Run through `vercel.json`. The inference container includes its model and display data.

Run the test suite with `python -m pytest -q`. The recorded verification includes **62 passing tests**, **12 reproduction checks**, Docker build/training/serving, and public HTTP checks. [GitHub Actions run 45437248856](https://github.com/AaryaDeshpande/aipi510-module3-main-street/actions/runs/45437248856) records container reproduction and API tests. [reports/README.md](reports/README.md) links the deployment, local Docker and experiment records.

## Limitations and ethics

- CBP counts establishments with paid employees. It excludes nonemployer businesses; one firm can have several establishments.
- Data ends in 2023. Displayed 2024 predictions are historical estimates, not current market forecasts.
- Counts, payroll and employment describe market scale. They do not establish profits, owner wealth, demand or willingness to pay. Interview prompts are research hypotheses.
- Suppressed cells and complete-history requirements can favor established markets. Missing observations are not treated as zero.
- Temporal splits share county/industry entities across years. Performance on unseen places is untested, and pandemic-era patterns may not generalize.
- Source publication lags mean the experiment is not a simulated real-time backtest. A growing category can also mean greater competition.
- The ownership worksheet uses aggregate financial data and user-supplied arithmetic. Its averages do not predict an individual business's outcome.

Shortlists and worksheet inputs are stored in the browser. The dataset contains aggregate statistics rather than named owners or personal net-worth records.

## Project structure and credits

- `business_app/`: cleaning, ingestion, training, evaluation and Flask serving
- `business_app/templates/` and `business_app/static/`: interface
- `data/`: source manifests and frozen datasets
- `artifacts/`: trained model and evaluation outputs
- `scripts/` and `infrastructure/`: deployment and verification tools
- `tests/` and `reports/`: automated checks and recorded results

Aarya's [implementation PR](https://github.com/AaryaDeshpande/aipi510-module3-main-street/pull/1) contains the initial pipeline and application. Tanya's [reproduction PR](https://github.com/AaryaDeshpande/aipi510-module3-main-street/pull/2) contains the local Docker review and related improvements. [PR #3](https://github.com/AaryaDeshpande/aipi510-module3-main-street/pull/3) adds GCS and Cloud Run deployment.

Related prior work: [Week 12 Iris pipeline](https://github.com/AaryaDeshpande/aipi510-week12-ml-pipeline) for pipeline patterns and [Module 1 local-service market screen](https://github.com/AaryaDeshpande/aipi510-module1-local-service-market-screen) for market-research context.
