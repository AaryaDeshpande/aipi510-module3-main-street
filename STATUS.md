# Requirement evidence and remaining work

Updated November 22, 2026 UTC. Personal completion target: Sunday November 22, Central Time. Previously verified Canvas deadline: Tuesday November 24, **10:30 am Central / 11:30 am Eastern**. Current Canvas instructions still require a signed-in refresh; [the dated audit](reports/assignment_audit.md) records the source limits.

## Completed and recorded

| Area | Actual evidence |
|---|---|
| Confirmed partners | Aarya Deshpande and Tanya, confirmed by Aarya; genuine contribution/PR record in TEAM_WORKFLOW.md |
| Official CBP data | 110,488 national county–industry–year rows, 2019–2023; source/hash/cleaning evidence in data/SOURCE.json |
| Financial context | 32 selected IRS 2023 Wisconsin Schedule C groups audited against included workbook; financial units, suppression, owner-labor and average limitations explicit |
| Supervised experiment | Chronological 2021/2022/2023 target-year splits; training-only learned preprocessing; validation-selected Ridge model |
| Honest evaluation | National held-out MAE 3.0594 vs no-change 2.9016; Wisconsin 2.2174 vs 1.9951 across 617 complete histories; model's higher average absolute error disclosed |
| Actual cloud storage | Cloudflare R2 object, successful retrieval, matching body/hash/provider/key/version checks; reports/cloud_storage.json |
| Actual cloud training | artifacts/ingestion.json records the HTTPS R2 source, version 7e5dfd2f3a14003c7290b88534de41da, 110,488 rows, pinned hash, and cloud_ingestion_verified=true; successful reports/cloud_training.log |
| Actual experiment tracking | Four FINISHED MLflow runs; parameters, metrics, and artifact export in reports/mlflow_runs.json |
| Reproduction | All 12 cloud-source reproduction and leakage checks pass; reports/reproducibility.json |
| Environments and tests | 61 tests passed; training and separate inference-only environments pass pip check; reports/pytest.txt and reports/environment_checks.json |
| Real serving-only HTTP | Fresh inference environment without MLflow loads the saved model; Gunicorn, HTTP requests, JSON predictions, curl, and errors checked; reports/serving_only_http.log, http_smoke.json and curl_prediction.json |
| Desktop interaction | Map/filter/history/unknown/shortlist checks and revised ownership case/route/scenario/thesis controls recorded in reports/browser_checks.json and reports/ownership_browser_checks.json |
| Repository and review | Actual repo: https://github.com/AaryaDeshpande/aipi510-module3-main-street; initial source upload is committed on aarya/module3-implementation; final docs/artifacts/workflow upload pending; owner-private phone review remains available |

The earlier environment report is retained as `reports/environment_checks_earlier.json`; it describes the earlier 40-test, local-source run. Current claims use the newer report. No further training is needed merely to repeat completed checks; rerun relevant checks after a substantive source/model change.

## Finish these remaining steps

1. **Finish publishing and review the code.** Complete the implementation upload and genuine authored PR. Tanya reviews the project, makes her own meaningful change, and opens her own PR. Both partners review and understand the full pipeline. Record actual contribution and PR URLs.
2. **Run Docker on a teammate's computer.** Build, train, serve, and send real JSON requests using DEPLOYMENT.md. Save the outputs. The prepared Actions workflow can add hosted Ubuntu Docker evidence after it runs; identify that as CI rather than a teammate-machine run.
3. **Finish public Flask deployment.** Vercel is connected, but the workspace's 403 permission response needs its pending team grant. Once granted, deploy the reviewed Python service and record its real frontend and `/predict` URLs.
4. **Check the real public service.** Verify signed-out instructor access, model/data hashes, the browser's real API request, errors, and phone/desktop behavior. Fill the URLs and final commit into README and SUBMISSION.md.
5. **Aarya completes Canvas submission.** Recheck the current assignment/rubric/deadline when signed in, review the final links/evidence, submit personally, and record the observed confirmation and timestamp. No automated Canvas submission is planned.

## Practical meaning and limits

The ownership homepage explains repeat purchases, costs, entry routes, financial context, scenario arithmetic, and one falsifiable thesis. The supporting county view organizes dated market observations. Neither establishes a proven winning business, an individual's wealth, current customer demand, willingness to pay, or future personal earnings. The ML component's 2024 estimates are unverified historical estimates based on data ending in 2023; its held-out MAE is higher than the baseline.

The phone-review Site uses an exported model and owner-private access. The required final public Python Flask/API service remains a separate open gate. The actual R2 cloud-data and Python training requirements already have executed evidence.
