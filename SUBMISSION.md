# Submission review sheet

## Latest verified access update

Canvas sign-in succeeded and assignment 363937 was read directly. The deadline is November 24, 2026 at **10:30 am Central / 11:30 am Eastern** (16:30 UTC). The current assignment explicitly excludes predictive accuracy from assessment, requires each member to author a PR, and requires a local Docker build/run. GitHub invitation **345631416** was sent to **Tanya-duke** and is awaiting her response. Older login-blocker notes below describe earlier attempts. See `reports/canvas_access_review.json` for current findings.

**Draft only.** This file prepares the final review and text entry. It does not record a completed Canvas submission or certify that every assignment requirement has passed.

Assignment: <https://canvas.duke.edu/courses/83524/assignments/363937>.

Previously verified deadline: **November 24, 2026, 11:30 am Eastern / 10:30 am Central**. Personal completion target: Sunday, November 22. Fresh Canvas access is sign-in blocked in the recorded audit; check for updates once access is available.

Confirmed teammates: **Aarya Deshpande and Tanya**. See [TEAM_WORKFLOW.md](TEAM_WORKFLOW.md) for genuine contribution and PR evidence. [Aarya’s authorized AI-assisted draft PR #1](https://github.com/AaryaDeshpande/aipi510-module3-main-street/pull/1) exists and awaits personal review and approval before merge. Tanya’s own meaningful PR remains pending.

## Final links

| Required item | Actual value or current gap |
|---|---|
| GitHub repository | <https://github.com/AaryaDeshpande/aipi510-module3-main-street>; current full implementation: [review branch](https://github.com/AaryaDeshpande/aipi510-module3-main-street/tree/aarya/module3-implementation) / [draft PR #1](https://github.com/AaryaDeshpande/aipi510-module3-main-street/pull/1); default main remains initialization |
| Live Flask frontend | <https://aipi510-module3-main-street.vercel.app/> — signed-out HTTP and desktop interaction verified |
| Deployed prediction API | <https://aipi510-module3-main-street.vercel.app/predict> — real JSON POSTs verified |
| Cloud training-data object and executed ingestion evidence | **Verified R2 storage and actual cloud training** — `reports/cloud_storage.json`, `artifacts/ingestion.json`, `reports/cloud_training.log`; version `7e5dfd2f3a14003c7290b88534de41da` |
| Successful Docker/CI evidence | **SUCCESS** [run 45013764218](https://github.com/AaryaDeshpande/aipi510-module3-main-street/actions/runs/45013764218), commit `520e0d1b3b52d80173ef2920a663943784aab8a3`; actual build/train/reproduction/serve/HTTP/artifact evidence retained in reports/ci/ |
| Teammate-machine Docker evidence | **PENDING local execution**; hosted CI is recorded separately |
| Aarya’s implementation PR | [Draft #1](https://github.com/AaryaDeshpande/aipi510-module3-main-street/pull/1) — authorized AI-assisted implementation; personal review and merge approval pending |
| Tanya's meaningful authored PR | **PENDING** |
| Submitted commit | **PENDING final reviewed commit** |
| Observed Canvas submission confirmation | **Aarya's final action after review**; no automated submission planned |

**Completed checks:** 61 passing tests, 12 passed cloud-source reproduction checks, four actual finished MLflow runs, and real HTTP/curl checks in a fresh inference-only environment. Both training and serving environments pass `pip check`. Hosted Docker CI also passed real build/train/reproduction/serve/HTTP checks; its downloaded artifact hash and provenance are recorded in `reports/ci/artifact_provenance.json`. See `reports/environment_checks.json` and the linked execution reports.

**Public deployment verified:** Vercel Flask build `dpl_6V8j2jMzxtdypBbYfSi7dT3HNgp7` is READY from source commit `ba6386433cb2b26fab5228992dd13f0cfa5a9c5b`. The stable production domain serves the app/API without sign-in. Health reports matching saved model and dataset hashes. Use the stable domain above; the unique build URL is protected. No access-control setting was changed.

Public Flask deployment and signed-out HTTP checks now pass at <https://aipi510-module3-main-street.vercel.app>. Live desktop checks cover ownership controls, calculator with owner labor, thesis save/restore/export/clear, county filters, unknown cells, a real browser prediction, and shortlist CSV download. See `reports/public_http_smoke.json`, `reports/public_deployment.json`, and `reports/public_browser_checks.json`. Phone/device review and a simulated frontend request failure remain unexecuted. The earlier private-Site gate in `reports/final_ui_check.json` is historical evidence.

The earlier owner-private ChatGPT Site is a review/data-retrieval surface. Use the verified public Flask production URL above for instructor access.

## Proposed Canvas text, after the gaps are closed

```text
Main Street Business Explorer — AIPI 510 Module Project 3
Team: Aarya Deshpande and Tanya [record exact submission display name]

GitHub: https://github.com/AaryaDeshpande/aipi510-module3-main-street
Current review branch: https://github.com/AaryaDeshpande/aipi510-module3-main-street/tree/aarya/module3-implementation
Draft implementation PR: https://github.com/AaryaDeshpande/aipi510-module3-main-street/pull/1
Live frontend: https://aipi510-module3-main-street.vercel.app/
Prediction API: https://aipi510-module3-main-street.vercel.app/predict

README contains data provenance, setup and reproduction instructions, the
chronological regression experiment, honest baseline comparison, and links
to verified deployment and team contribution evidence.
```

Replace every bracketed field with observed information before copying this draft. The assignment's requested GitHub and frontend links must be accessible to the instructor, and the deployed API URL must also appear in README.

## Required final evidence

- [ ] Recheck current assignment instructions, rubric, exact deadline, and submission format in Canvas when accessible. Use [REQUIREMENTS.md](REQUIREMENTS.md) and [the audit](reports/assignment_audit.md) as the existing evidence map.
- [ ] Confirm the final repository contains the intended source, frozen datasets, pinned dependencies, configuration, saved model, source citations, and execution reports; exclude credentials and temporary downloads.
- [x] Cleaned data stored in R2 and actual training retrieved the cloud object programmatically. Matching hash, source, 110,488 rows, and object version are recorded.
- [x] Current Python checks passed: 61 tests, 12 cloud-source reproduction checks, four finished MLflow runs, clean training/serving dependency checks, and inference-only real HTTP/curl results. Record the final uploaded commit alongside this source hash. CI artifacts describe only the run that created them.
- [x] [Hosted Docker CI run 45013764218](https://github.com/AaryaDeshpande/aipi510-module3-main-street/actions/runs/45013764218) passed real build/train/reproduction/serve/HTTP checks; downloaded evidence retained.
- [ ] Build the Docker image and execute training/serving on a teammate's machine. Exercise real `/health` and `/predict` requests and retain matching model/data identifiers. The successful hosted run above remains separate evidence.
- [x] Public Flask service is deployed; signed-out HTTP, the frontend's real JSON prediction, API input-error handling, and matching deployed model/data identifiers are verified. Evidence: `reports/public_http_smoke.json`, `reports/public_deployment.json`, `reports/public_browser_checks.json`.
- [x] Desktop public app: dated source labels, calculator including owner labor, all case/route controls, map/filter agreement, unknown values, browser-local thesis workflow, real prediction, and shortlist export were exercised.
- [ ] Complete phone/device review, a selected suppressed financial value check, and frontend behavior when the API is unavailable. These checks are not claimed as executed.
- [ ] Both members have personally reviewed/performed their recorded work and opened meaningful, correctly authored PRs. Record actual URLs and review evidence.
- [ ] README and this sheet contain real final URLs and accurate completion claims. Reconcile all checklists with actual evidence.
- [ ] Aarya reviews the final repository, public service, contribution record, and prepared Canvas entry. Obtain any required explicit authorization for remaining shared-repository or submission actions.
- [ ] Aarya submits through Canvas personally, then records the observed submission result and timestamp here. No automated Canvas submission is planned.

## Plain-language explanation for the instructor

The reproducible ML component predicts next-year county–industry establishment counts using earlier reported counts. Data cleaning, chronological splits, training-only preprocessing, validation selection, MLflow tracking, saved-artifact inference, and real JSON serving form the engineering pipeline. The financial snapshot and ownership worksheet provide a practical research interface alongside that experiment.

The held-out model MAE is **3.0594 locations**, compared with **2.9016** for the no-change baseline. The model therefore has higher average absolute test error. Its displayed **2024** estimates are unverified historical estimates based on observations ending in **2023**. The app cannot establish an individual's wealth, a profitable acquisition, customer demand, or future personal earnings. IRS Schedule C figures are aggregate averages with important owner-labor and sample limitations; scenario outputs depend on the user's assumptions.

## Instructor-facing continuation review

See [INSTRUCTOR_REVIEW.md](INSTRUCTOR_REVIEW.md) for the ML implementation/evidence map, presentation changes, and remaining source-access/team eligibility checks. Tanya’s confirmed account is `Tanya-duke`; [TANYA_START_HERE.md](TANYA_START_HERE.md) prepares her independent Docker/model-review PR. Invitation was sent to `Tanya-duke` and awaits acceptance. The prepared research-first homepage is local until published.
