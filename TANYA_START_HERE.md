# Tanya's independent contribution

Complete the Docker training and serving reproduction on the `tanya/docker-reproduction` branch.

## Tasks

1. Build the Docker image.
2. Train the model into `container-artifacts/` without modifying tracked `artifacts/`.
3. Start the containerized application.
4. Check `/health`, a valid `/predict` request, and an empty-object `/predict` request.
5. Open the local application and verify the 2024 estimate is labeled historical.
6. Compare model and dataset hashes and test MAE against the README.
7. Save actual results in `reports/tanya_docker_review.md`.
8. Commit and push the branch, then open a PR back to `aarya/module3-implementation`.

## Commands

```bash
git fetch origin
git switch -c tanya/docker-reproduction origin/aarya/module3-implementation
docker build -t main-street-review .
mkdir -p container-artifacts
docker run --rm --user "$(id -u):$(id -g)" \
  -v "$PWD/container-artifacts:/output" \
  main-street-review train --data-uri data/panel.csv --output-dir /output
docker run --rm -p 8080:8080 \
  -v "$PWD/container-artifacts:/app/artifacts:ro" \
  main-street-review
```

In a second terminal:

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

The valid request should return HTTP 200. The empty object should return HTTP 422. Use `reports/tanya_review_template.md` as a checklist, but report only actual results.

## Expected model explanation

The model learns next-year establishment change from industry and current/previous counts. Training targets 2021, validation targets 2022, and test targets 2023. The three Ridge settings are selected by validation MAE, and the final model is evaluated once on the 2023 test split. The no-change baseline currently has lower held-out MAE.

## Submission

The Docker reproduction and review are complete. The branch is committed and pushed as `tanya/docker-reproduction`.

Open a PR from `tanya/docker-reproduction` to `aarya/module3-implementation`. If PR #1 has merged, branch from and target updated `main` instead.
