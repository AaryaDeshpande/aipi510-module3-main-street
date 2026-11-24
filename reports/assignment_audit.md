> Historical pre-migration audit, preserved unchanged below. For the November 24 GCS/Cloud Run deployment and current requirement assessment, read [submission_audit_20261124.md](submission_audit_20261124.md) and [../REQUIREMENTS.md](../REQUIREMENTS.md).

# Module Project 3 requirements audit

## Verified requirements

- Public dataset: U.S. Census County Business Patterns, 2019–2023.
- Target: next-year establishment count for selected county–industry observations.
- Data cleaning and integrity checks: `business_app/prepare.py` and `data/SOURCE.json`.
- Chronological splits: training 2021, validation 2022, held-out test 2023.
- Ridge model with training-only preprocessing and validation-based alpha selection.
- MLflow parameter, metric, artifact, and reproducibility records.
- Pinned requirements and Docker training/serving entry points.
- Flask `/predict` endpoint and public frontend/API deployment.
- README and deployment documentation.
- Ethics and limitations, including the model's higher held-out MAE than persistence.

## Current evidence

- Test MAE: `3.0594`.
- No-change baseline MAE: `2.9016`.
- Local Docker review: `reports/tanya_docker_review.md`.
- Status summary: `STATUS.md`.
- Public HTTP evidence: `reports/final_public_http_smoke.json`.
- Browser evidence: `reports/final_browser_checks.json` or `reports/public_browser_checks.json`.

## Open course checks

- Confirm whether R2 and Vercel are accepted substitutes for the provider examples named in the assignment.
- Complete the final repository review and Canvas submission.

This report records only project evidence relevant to the assignment checklist.
