# Current implementation audit

Checked November 22, 2026. See `environment_checks.json` for the current source and model hashes. The earlier environment report is retained as `environment_checks_earlier.json`.

## Executed and passed

- Official cleaned CBP panel: 110,488 observations; frozen source/schema/hash checks.
- Real Cloudflare R2 storage upload and retrieval, exact 5,799,225-byte checksum match, and actual stored object version. See `cloud_storage.json` and `../infrastructure/`.
- Model training retrieves that R2 object programmatically. `../artifacts/ingestion.json` records `cloud_ingestion_verified: true` with provider, key, version, source URI, hash, and row count. Credentials are excluded.
- Four actual finished MLflow runs for three validation settings and the selected model. Parameters, metrics, and artifact references are exported in `mlflow_runs.json`.
- Twelve deterministic reproduction checks pass, including splits, training-only preprocessing, evaluation, and repeated predictions.
- All 61 tests pass. Cloud contract/security tests use simulated responses; the separate storage/training reports establish real cloud execution.
- Fresh pinned training and serving environments both pass `pip check`. The serving environment has no MLflow installed. The actual saved pipeline loads, Gunicorn serves HTTP, and real JSON prediction plus curl checks pass.
- Ownership and market frontend workflows were checked in the earlier recorded browser review. A separate Worker coefficient-export review passes 673 prediction parity cases. The review Site is owner-private and uses JavaScript; it is a distinct deployment from the required public Python app.

## Remaining completion gates

1. Run the actual Docker image build, training, and serving checks. The prepared GitHub Actions workflow has to execute after the full source is uploaded. Record its actual URL and results. A CI run establishes execution on its runner; the assignment's local-machine Docker wording still needs the team to execute or verify those commands on its own machine.
2. Deploy the Flask service publicly and verify anonymous frontend, health, metadata, and prediction requests against the final artifact. Vercel is connected; access to the selected workspace awaits the user's consent. No public Flask URL is claimed.
3. Aarya and Tanya review and explain the work, complete their own meaningful contributions, and retain genuine member-authored PR evidence. An AI-assisted implementation branch or draft PR is not evidence of Tanya's contribution or either member's review.
4. Check the current Canvas assignment, team assignment, rubric, deadline, and text-entry instructions once signed-in access is restored. The previously verified deadline is November 24, 2026, 11:30 am Eastern / 10:30 am Central.
5. Fill verified deployment and PR URLs into the final submission text. Aarya performs the final Canvas submission. No submission has been made.

## Model and product limits

Shared numeric functions now live in `business_app/inference.py`; training and serving use the same formulas. Serving uses 25 pinned packages; Docker and training retain the 97-package training environment. Fresh serialization references the inference module, and the trained code hash matches current Python source.

The held-out model MAE is 3.0594 business locations versus 2.9016 for persistence. This result, historical 2024 estimate date, source publication lag, and unknown small cells remain visible. No hyperparameter tuning was done in response to the test result.

The business cases, IRS financial context, ownership routes, and editable scenario arithmetic help formulate a testable business thesis. Actual customer pain, willingness to pay, accessible customers, profitability, acquisition value, and personal wealth outcomes remain unverified.
