# Submission review sheet

**Draft only.** This file prepares the final review and text entry. It does not record a completed Canvas submission or certify that every assignment requirement has passed.

Assignment: <https://canvas.duke.edu/courses/83524/assignments/363937>.

Previously verified deadline: **November 24, 2026, 11:30 am Eastern / 10:30 am Central**. Personal completion target: Sunday, November 22. Fresh Canvas access is sign-in blocked in the recorded audit; check for updates once access is available.

Confirmed teammates: **Aarya Deshpande and Tanya**. See [TEAM_WORKFLOW.md](TEAM_WORKFLOW.md) for genuine contribution and PR evidence. The actual partner PRs remain pending.

## Final links

| Required item | Actual value or current gap |
|---|---|
| GitHub repository | <https://github.com/AaryaDeshpande/aipi510-module3-main-street> — initial source upload committed on `aarya/module3-implementation`; final docs/artifacts/workflow and instructor-access check pending |
| Live Flask frontend | **PENDING public deployment and verification** |
| Deployed prediction API | **PENDING public deployment and verification**; route `/predict` |
| Cloud training-data object and executed ingestion evidence | **Verified R2 storage and actual cloud training** — `reports/cloud_storage.json`, `artifacts/ingestion.json`, `reports/cloud_training.log`; version `7e5dfd2f3a14003c7290b88534de41da` |
| Successful Docker/CI evidence | **PENDING actual execution and Actions run URL** |
| Aarya's meaningful authored PR | **PENDING** |
| Tanya's meaningful authored PR | **PENDING** |
| Submitted commit | **PENDING final reviewed commit** |
| Observed Canvas submission confirmation | **Aarya's final action after review**; no automated submission planned |

**Completed checks:** 61 passing tests, 12 passed cloud-source reproduction checks, four actual finished MLflow runs, and real HTTP/curl checks in a fresh inference-only environment. Both training and serving environments pass `pip check`. See `reports/environment_checks.json` and the linked execution reports.

**Public deployment blocker:** Vercel is connected, but its team/workspace permission grant remains pending after a 403 response. The final frontend/API URLs will be recorded only after deployment and real public checks.

The owner-private phone review at <https://aarya-main-street-20261122.ad277.chatgpt.site/> is a review surface. The required final service still needs a public, instructor-accessible Flask frontend/API with verified real HTTP requests.

## Proposed Canvas text, after the gaps are closed

```text
Main Street Business Explorer — AIPI 510 Module Project 3
Team: Aarya Deshpande and Tanya [record exact submission display name]

GitHub: https://github.com/AaryaDeshpande/aipi510-module3-main-street
Live frontend: [insert verified public URL]
Prediction API: [insert verified public URL]/predict

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
- [ ] Build the Docker image and execute training/serving on a teammate's machine. Exercise real `/health` and `/predict` requests and retain matching model/data identifiers. Label any successful hosted Actions run as CI evidence separately.
- [ ] Deploy the approved Flask service publicly. Test the frontend's real JSON call to its API and input-error handling; verify the deployed model matches the final artifact.
- [ ] Open the public app on desktop and phone. Check source dates, financial suppression, calculator labels, case/route controls, map/filter agreement, unknown values, and browser-local thesis/export behavior. Record any unexecuted checks explicitly.
- [ ] Both members have personally reviewed/performed their recorded work and opened meaningful, correctly authored PRs. Record actual URLs and review evidence.
- [ ] README and this sheet contain real final URLs and accurate completion claims. Reconcile all checklists with actual evidence.
- [ ] Aarya reviews the final repository, public service, contribution record, and prepared Canvas entry. Obtain any required explicit authorization for remaining shared-repository or submission actions.
- [ ] Aarya submits through Canvas personally, then records the observed submission result and timestamp here. No automated Canvas submission is planned.

## Plain-language explanation for the instructor

The reproducible ML component predicts next-year county–industry establishment counts using earlier reported counts. Data cleaning, chronological splits, training-only preprocessing, validation selection, MLflow tracking, saved-artifact inference, and real JSON serving form the engineering pipeline. The financial snapshot and ownership worksheet provide a practical research interface alongside that experiment.

The held-out model MAE is **3.0594 locations**, compared with **2.9016** for the no-change baseline. The model therefore has higher average absolute test error. Its displayed **2024** estimates are unverified historical estimates based on observations ending in **2023**. The app cannot establish an individual's wealth, a profitable acquisition, customer demand, or future personal earnings. IRS Schedule C figures are aggregate averages with important owner-labor and sample limitations; scenario outputs depend on the user's assumptions.
