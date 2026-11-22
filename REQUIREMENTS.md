# Module Project 3 acceptance checklist

This checklist maps the previously verified Canvas requirements to concrete evidence for the business explorer. It does not certify completion or assign invented rubric points. See [the source audit](reports/assignment_audit.md) for source freshness and unresolved items.

Assignment: <https://canvas.duke.edu/courses/83524/assignments/363937>

**Previously verified deadline:** November 24, 2026, 11:30 am Eastern / 10:30 am Central. Personal target: Sunday November 22. Worth 200 points / 20% of the course.

## Data and modeling

- [x] **Public supervised dataset.** Cite official source URLs, reference years, variable definitions, and applicable use terms. Define the regression target and units clearly.
- [x] **Local cleaning.** Save reproducible cleaning code, a frozen cleaned dataset, source provenance, row counts, exclusion decisions, and a content hash. Handle aggregate county codes, suppressed/flagged values, missing records, and industry-code changes explicitly.
- [x] **Actual cloud data storage.** Cloudflare R2 object stored and retrieved; provider/key/hash/version headers and response body verified. Evidence: `reports/cloud_storage.json`; object version `7e5dfd2f3a14003c7290b88534de41da`.
- [x] **Programmatic cloud ingestion.** Successful training retrieved the actual authenticated HTTPS R2 object, verified content/schema, and recorded 110,488 rows with `cloud_ingestion_verified: true` in `artifacts/ingestion.json`; successful output in `reports/cloud_training.log`. The cloud-source rerun passed all 12 reproduction checks; four actual finished MLflow runs are exported in `reports/mlflow_runs.json`.
- [x] **Configuration.** Provide `config.yaml` for data source/version, splits, model settings, tracking, and outputs. Preserve the effective configuration used for each final run.
- [x] **Training/validation/test split.** Keep three separate sets. For a next-year forecast, use chronological split periods and features available before each prediction target. Record row/time identifiers and leakage checks.
- [x] **Preprocessing and features.** Fit learned transformations only on training data. Explain any lagged counts, growth measures, categorical encodings, and missing-data policy.
- [x] **Simple model and genuine evaluation.** Fit the selected regressor, choose settings on validation data, and report reserved-test metrics in clear units. Compare with a meaningful baseline, such as carrying the previous count forward. Report negative or weak results honestly.
- [x] **MLflow or W&B.** Execute and retain real experiment runs, parameters, metrics, model, and evaluation artifacts. A prepared logging script alone is insufficient evidence of execution.

## Reproducibility and serving

- [x] **Pinned environment.** Provide pinned `requirements.txt` or equivalent. Verify installation and execution in a clean environment; retain versions and exit results.
- [x] **Dockerfile.** Include reproducible training and serving entry points and document their commands.
- [ ] **Actual container checks.** Build the image and run training and serving on a teammate's machine, then verify real JSON requests. The prepared Actions workflow can add hosted Ubuntu Docker evidence after a real run; it must be identified separately from the local-machine requirement.
- [x] **Flask/FastAPI JSON API.** Provide `/predict` with documented field names, types, units, outputs, and input-error behavior. Load the intended saved model/preprocessing artifact.
- [ ] **Public cloud API.** Vercel is connected; a workspace 403 requires the pending team permission grant. After authorized deployment, verify the real HTTPS URL and model/version against final artifacts. Local serving-only checks already pass; public deployment is still open.
- [ ] **Public frontend calling the API.** Use a real HTTP JSON request to the deployed endpoint. Verify the request succeeds from the public page on desktop and phone; show useful errors. A shared host for frontend and API is acceptable when the browser genuinely calls `/predict`.

## Documentation, authorship, and submission

- [x] **README overview and sources.** Explain the actual business question, dataset, source/reference years, preparation, target, features, model, evaluation, baseline, cloud services, and limitations.
- [x] **README reproducibility.** Give exact setup, training, test, container, and deployment instructions that match the final code.
- [ ] **README links.** Include the actual live frontend URL and deployed API URL. Confirm the GitHub repository is accessible to the instructor. Remove placeholders before submission.
- [x] **Honest use and limitations.** Clearly distinguish observed business statistics, historical model estimates, screening hypotheses, and any manually supplied information. Do not label estimated establishment counts as wealth, revenue, profit, or customer demand.
- [x] **Code-source attribution.** Cite copied/reused code or templates and explain material changes. The syllabus states uncited copying can receive zero and expects originality.
- [x] **AI acknowledgment.** Recommended by the syllabus, with no points deducted for omitting it. A concise README disclosure can identify AI assistance. An interface banner is not required by the syllabus.
- [x] **Confirmed group and implementation branch.** Aarya confirms Aarya Deshpande and Tanya as partners. The implementation branch is `aarya/module3-implementation` in the actual Module 3 repository. Individual member branch/PR evidence remains open in `TEAM_WORKFLOW.md`.
- [ ] **Each actual member's authored PR.** Retain a meaningful real PR for every actual member. Record names, work, and actual URLs; do not fabricate authorship or contributions.
- [ ] **Final audit.** Match the final deployed artifact, source/config/data version, public HTTP evidence, and README. Check for any current Canvas instruction/rubric update when access is available.
- [ ] **Canvas text entry.** Prepare the actual GitHub URL and live frontend URL for Aarya to submit. The README must also contain the deployed API URL. No automated submission is planned.
- [ ] **Review and authorization.** The user reviews the final work. No shared-repository modification or Canvas submission occurs without the user's explicit authorization under the original task constraints.
- [ ] **Submission verification.** After Aarya submits, record the observed Canvas result and timestamp. A prepared draft or a working public demo does not establish submission.

## Useful project-specific checks

These strengthen the result; they are not a newly invented scored rubric:

- Repeated training preserves splits, selected settings, and predictions/metrics under the documented environment.
- Cloud-ingested data matches the frozen cleaned data hash.
- Baseline and model use the same held-out rows.
- Future-year labels and their derivatives never enter training features.
- County maps, table rows, selected filters, and displayed units match the same underlying records.
- Suppression or missing values are not silently treated as meaningful zeros.
- Public `/predict` results match the saved local artifact on known requests, and invalid requests return clear errors.
- The interface displays data vintage and distinguishes historical backtests from forecasts for an unobserved year.
