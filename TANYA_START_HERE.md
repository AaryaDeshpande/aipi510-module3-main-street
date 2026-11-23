# Tanya's independent contribution

Account confirmed: **[Tanya-duke](https://github.com/Tanya-duke)**. Her authored [Module 2 PR #3](https://github.com/AaryaDeshpande/aipi510-module2-abbeyroad-sampling/pull/3) verifies this identity. Your Module 3 collaborator invitation has been sent. GitHub currently shows Awaiting Tanya-duke’s response. Accept the invitation before pushing your branch to this repository.

## Your task

Independently reproduce the Docker training and serving workflow, verify predictions and the reported baseline comparison, and contribute your actual execution record plus any correction you discover. Your own branch, commit, and PR establish your contribution. A prepared template is a starting point; it does not claim you completed the work.

Start with Docker Desktop installed and running on your Mac. Allow time for the first image/dependency download. From Terminal:

```bash
git clone --branch aarya/module3-implementation https://github.com/AaryaDeshpande/aipi510-module3-main-street.git
cd aipi510-module3-main-street
git fetch origin
git switch -c tanya/docker-reproduction origin/aarya/module3-implementation
git rev-parse HEAD
docker version
docker build -t main-street-review .
mkdir -p container-artifacts
docker run --rm --user "$(id -u):$(id -g)" \
  -v "$PWD/container-artifacts:/output" \
  main-street-review train --data-uri data/panel.csv --output-dir /output
docker run --rm -p 8080:8080 \
  -v "$PWD/container-artifacts:/app/artifacts:ro" \
  main-street-review
```

The final command keeps the API running. In a second terminal:

```bash
curl --fail --silent --show-error http://localhost:8080/health
curl --fail --silent --show-error \
  -H 'Content-Type: application/json' \
  -d '{"industry":"2382","establishments":100,"previous_establishments":95}' \
  http://localhost:8080/predict
curl --silent --show-error -i \
  -H 'Content-Type: application/json' -d '{}' \
  http://localhost:8080/predict
```

Open http://localhost:8080/ and run a prediction from the map. A valid JSON prediction should succeed; the empty object should return HTTP 422. Compare the health and prediction model hashes with `container-artifacts/metadata.json`. Check its test MAE against the README (model 3.0594, baseline 2.9016) and verify the displayed 2024 estimate is labeled historical. Do not overwrite the tracked `artifacts/` directory with your local rerun.

Stop the running container with Control-C after review. Independently fill `reports/tanya_review_template.md`, then save your completed record as `reports/tanya_docker_review.md`. Include the actual date, tested commit, Docker/OS versions, commands, results, model/data hashes, and what you personally checked. Describe any failure honestly; a real fix is a valuable contribution. Omit credentials, private tokens, and unrelated machine details.

```bash
git add reports/tanya_docker_review.md
# Add any actual source/test fixes you made as well.
git commit -m "Record independent Docker reproduction and model review"
git push -u origin tanya/docker-reproduction
```

Use your own GitHub identity. In GitHub, open a PR with **base `aarya/module3-implementation`**, **compare `tanya/docker-reproduction`**. Aarya reviews it. If PR #1 has already been approved and merged when you start, branch from updated main and target main instead. If you lack write access, you may use a fork and open your PR back to this repository.

## What you should be able to explain

The model learns next-year establishment change from current/previous counts and industry. Training targets 2021, validation targets 2022, and the reserved test targets 2023. Preprocessing is learned on training data. Three Ridge settings are compared on validation data. Four real MLflow runs record that selection and final evaluation. The model is saved and used by `/predict`; the webpage calls that endpoint. The model has higher average absolute test error than the no-change baseline, which remains visible.

## Separate course check

The syllabus says teams of three with different teammates for each project. The working roster is Aarya and Tanya, who also worked together previously. Confirm the current Canvas assignment's online-cohort/team exception or existing instructor approval before submitting. This document does not establish that exception.
