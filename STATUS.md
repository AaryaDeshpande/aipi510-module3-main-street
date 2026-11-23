# Requirement evidence and remaining work

## Latest verified access update

Canvas sign-in succeeded and assignment 363937 was read directly. The deadline is November 24, 2026 at **10:30 am Central / 11:30 am Eastern** (16:30 UTC). The current assignment explicitly excludes predictive accuracy from assessment, requires each member to author a PR, and requires a local Docker build/run. GitHub invitation **345631416** was sent to **Tanya-duke** and is awaiting her response. Older login-blocker notes below describe earlier attempts. See `reports/canvas_access_review.json` for current findings.

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
| Public Flask service | Stable production origin https://aipi510-module3-main-street.vercel.app; successful Vercel Flask build from `ba6386433cb2b26fab5228992dd13f0cfa5a9c5b`; reports/public_deployment.json |
| Public HTTP and desktop interaction | Signed-out smoke checks, matching model/data hashes, 72 counties, three prediction payloads, input errors, and live browser flows pass; reports/public_http_smoke.json and reports/public_browser_checks.json; phone behavior remains untested |
| Repository and review | Implementation uploaded to [review branch](https://github.com/AaryaDeshpande/aipi510-module3-main-street/tree/aarya/module3-implementation); [draft PR #1](https://github.com/AaryaDeshpande/aipi510-module3-main-street/pull/1) awaits Aarya’s personal review/approval before merge; default main remains initialization |
| Hosted Docker CI | [Run 45013764218](https://github.com/AaryaDeshpande/aipi510-module3-main-street/actions/runs/45013764218) SUCCESS: real build, train, reproduction, container serving, HTTP/curl and evidence artifact; source commit `520e0d1b3b52d80173ef2920a663943784aab8a3`; reports/ci_observation.json and retained reports/ci/ |

The earlier environment report is retained as `reports/environment_checks_earlier.json`; it describes the earlier 40-test, local-source run. Current claims use the newer report. No further training is needed merely to repeat completed checks; rerun relevant checks after a substantive source/model change.

## Finish these remaining steps

1. **Review the existing draft PR and finish team contributions.** Aarya personally reviews the authorized AI-assisted draft PR #1 before any approved merge. Tanya independently executes meaningful work, records it in her own PR, and both partners review and understand the pipeline.
2. **Run Docker on a teammate's computer.** Build, train, serve, and send real JSON requests using DEPLOYMENT.md. Save the outputs. Hosted Ubuntu Docker CI already passed; retain that result and add the teammate-machine evidence.
3. **Finish device and failure-state review.** Public Flask deployment, signed-out access, model/data hashes, input errors, and the desktop browser's real API request now pass. Review the app on an actual phone and check the visible frontend response to an unavailable API. Final reviewed commit remains pending team review.
4. **Recheck current Canvas instructions when signed in.** The fresh assignment navigation again led to Duke's public Canvas login landing page; no current rubric/deadline update was verified.
5. **Aarya completes Canvas submission.** Recheck the current assignment/rubric/deadline when signed in, review the final links/evidence, submit personally, and record the observed confirmation and timestamp. No automated Canvas submission is planned.

Public Flask deployment and signed-out HTTP checks now pass at <https://aipi510-module3-main-street.vercel.app>. Live desktop checks cover ownership controls, calculator with owner labor, thesis save/restore/export/clear, county filters, unknown cells, a real browser prediction, and shortlist CSV download. See `reports/public_http_smoke.json`, `reports/public_deployment.json`, and `reports/public_browser_checks.json`. Phone/device review and a simulated frontend request failure remain unexecuted. The earlier private-Site gate in `reports/final_ui_check.json` is historical evidence.

## Practical meaning and limits

The ownership homepage explains repeat purchases, costs, entry routes, financial context, scenario arithmetic, and one falsifiable thesis. The supporting county view organizes dated market observations. Neither establishes a proven winning business, an individual's wealth, current customer demand, willingness to pay, or future personal earnings. The ML component's 2024 estimates are unverified historical estimates based on data ending in 2023; its held-out MAE is higher than the baseline.

The earlier phone-review Site uses an exported model and owner-private access. The public Python Flask/API service is now independently verified at the stable Vercel production domain. The R2 cloud-data and Python training requirements retain their executed evidence.

## Instructor-facing continuation review

See [INSTRUCTOR_REVIEW.md](INSTRUCTOR_REVIEW.md) for the ML implementation/evidence map, presentation changes, and remaining source-access/team eligibility checks. Tanya’s confirmed account is `Tanya-duke`; [TANYA_START_HERE.md](TANYA_START_HERE.md) prepares her independent Docker/model-review PR. Invitation was sent to `Tanya-duke` and awaits acceptance. The prepared research-first homepage is local until published.
