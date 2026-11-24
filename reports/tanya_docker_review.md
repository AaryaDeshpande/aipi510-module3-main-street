# Independent Docker and model review

**Reviewer/GitHub identity:** Tanya-duke

**Actual date:** 2026-11-23

**Tested source commit (`git rev-parse HEAD`):** `1b710ae3cbd35258c98a8173dcb956f07b809eb7`

**Working branch:** `tanya/docker-reproduction`

**OS:** macOS 15.7.9

**Docker versions:** Docker Desktop 4.100.1; Docker client 29.9.3; Docker engine 29.9.3

## Exact commands executed

```bash
git fetch origin
git switch -c tanya/docker-reproduction origin/aarya/module3-implementation
docker build -t main-street-review .
mkdir -p container-artifacts
docker run --rm --user "$(id -u):$(id -g)" -v "$PWD/container-artifacts:/output" main-street-review train --data-uri data/panel.csv --output-dir /output
docker run --rm -p 8080:8080 -v "$PWD/container-artifacts:/app/artifacts:ro" main-street-review
curl --fail --silent --show-error http://localhost:8080/health
curl --fail --silent --show-error -H 'Content-Type: application/json' -d '{"industry":"2382","establishments":100,"previous_establishments":95}' http://localhost:8080/predict
curl --silent --show-error -i -H 'Content-Type: application/json' -d '{}' http://localhost:8080/predict
```

## Docker build

- Exit status: success
- Image: `main-street-review:latest`
- Build completed in approximately 135 seconds

## Container training

- Exit status: success
- Source: local `data/panel.csv`
- Dataset SHA-256: `ddef9fbb3835bb981395cc1c77b904d27e899f8f4c75ac97028be31bb5206682`
- Model SHA-256: `7b764d79ca4e014e4ded87d9fc603611f93a167289eeafed136ab21aa7174251`
- Code SHA-256: `8d91922b07a024258b970c4fefc6776d0b002edb4d86f1dd2ddbb02a30024c47`
- Alpha: `1.0`
- Train/validation/test rows: `21258 / 21132 / 21224`
- Python/scikit-learn/NumPy/Pandas: `3.12.16 / 1.8.0 / 2.3.5 / 2.3.5`

Artifacts were written only to `container-artifacts/`; tracked `artifacts/` was not modified.

## HTTP checks

### `/health`

HTTP 200:

```json
{"dataset_sha256":"ddef9fbb3835bb981395cc1c77b904d27e899f8f4c75ac97028be31bb5206682","model_sha256":"7b764d79ca4e014e4ded87d9fc603611f93a167289eeafed136ab21aa7174251","status":"ready"}
```

### Valid `/predict`

Request: `{"industry":"2382","establishments":100,"previous_establishments":95}`

HTTP 200:

```json
{"as_of_year":2023,"baseline":100.0,"model_beats_baseline":false,"model_sha256":"7b764d79ca4e014e4ded87d9fc603611f93a167289eeafed136ab21aa7174251","notice":"Unverified historical 2024 estimate using the 2023 feature definition. Review held-out 2023 error and persistence baseline; this is not a current market-demand forecast.","prediction":102.00787374502853,"target_year":2024}
```

### Empty `/predict`

HTTP 422:

```json
{"error":"Include exactly industry, establishments, and previous_establishments","fields":["industry","establishments","previous_establishments"]}
```

The model hash agreed across `container-artifacts/metadata.json`, `/health`, and `/predict`. The independently generated model hash differs from the tracked cloud artifact; dataset and numeric metrics agree.

## Baseline comparison

| Measure | Model | No-change baseline |
|---|---:|---:|
| Validation MAE | 3.4101333990532026 | 3.631979935642627 |
| Held-out test MAE | 3.0593603978699386 | 2.9015736901620808 |
| Held-out test RMSE | 8.640868334839439 | 9.098978809669601 |
| Held-out test median AE | 1.270866854321266 | 1.0000 |

The model's held-out MAE is approximately 5.4% worse than persistence. The rounded README values match.

## Findings

- Training targets 2021, validation targets 2022, and test targets 2023.
- Ridge alpha `1.0` was selected on validation MAE.
- The application loaded successfully and a browser map prediction was executed for Dane County and Building equipment contractors.
- No application source or test defect was found; no source fix was required.

## Browser check

The application loaded successfully at `http://localhost:8080/`. Dane County and Building equipment contractors were selected, and **Run estimate for this selection** was executed in the browser.

- 2024 model estimate: `281.2` business locations
- 2024 no-change estimate: `276` business locations
- 2024 estimate label: unverified historical estimate using the 2023 feature definition
- The page explicitly notes that this is not a 2026 current market-demand forecast

## Tests

The complete pytest suite ran successfully in the Docker environment: **61 tests passed** with 2 dependency warnings.
