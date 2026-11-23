# Module Project 3 continuation handoff

## Latest verified access update

Canvas sign-in succeeded and assignment 363937 was read directly. The deadline is November 24, 2026 at **10:30 am Central / 11:30 am Eastern** (16:30 UTC). The current assignment explicitly excludes predictive accuracy from assessment, requires each member to author a PR, and requires a local Docker build/run. GitHub invitation **345631416** was sent to **Tanya-duke** and is awaiting her response. Older login-blocker notes below describe earlier attempts. See `reports/canvas_access_review.json` for current findings.

Updated 2026-11-22T13:05:29.105448+00:00. Project: **Main Street Business Explorer**, AIPI 510 Module Project 3. Confirmed partners: Aarya Deshpande and Tanya. The earlier App Review Triage/Iris experiment is a different project and its results do not establish completion here.

## Resume here

The public Flask deployment is complete and verified. Use <https://aipi510-module3-main-street.vercel.app/> or <https://aipi510-module3-main-street.vercel.app/market>; API JSON POST endpoint: <https://aipi510-module3-main-street.vercel.app/predict>.

- Repository: <https://github.com/AaryaDeshpande/aipi510-module3-main-street>.
- Implementation: branch `aarya/module3-implementation`, [draft PR #1](https://github.com/AaryaDeshpande/aipi510-module3-main-street/pull/1). Default main still contains initialization; do not merge without Aarya's review/approval.
- Deployed application source: `ba6386433cb2b26fab5228992dd13f0cfa5a9c5b`. This continuation updates documentation and execution evidence; application code, data, and model remain the deployed version.
- Vercel deployment: `dpl_6V8j2jMzxtdypBbYfSi7dT3HNgp7`, READY, Flask, Python 3.12. Build logs show the exact GitHub commit was cloned and built. The stable domain is public; the unique build URL is protected. No access-control change was applied.
- Public execution evidence: `reports/public_http_smoke.json`, `reports/public_deployment.json`, `reports/public_browser_checks.json`.

## Preserved completed work

Official CBP panel: 110,488 rows, 2019–2023; Wisconsin map: 72 counties × 10 categories. Actual R2 storage/ingestion, four real MLflow runs, 61 prior passing tests, 12 reproduction checks, inference-only HTTP checks, and successful hosted Docker build/train/reproduce/serve remain recorded. Do not retrain merely to repeat completed work.

Public signed-out HTTP checks now pass; loaded model/data hashes match the frozen artifacts. The public desktop webpage performed a real prediction and its ownership controls, arithmetic, browser-local thesis workflow, map filters, unknown values, and shortlist download were exercised. The previous private-Site login-gate report is historical and is superseded for public access by the new reports.

## Remaining actual gates

1. Aarya personally reviews the draft implementation; Tanya performs meaningful work in her own identity, opens her own PR, and both partners review and understand the pipeline. Do not invent authorship/review evidence.
2. A teammate builds/trains/serves Docker on their own computer and preserves real commands/results. Hosted CI already passed; it is a separate execution environment.
3. Review on a phone/device, the frontend's unavailable-API state, and a selected suppressed financial record. These have not been executed.
4. Refresh the current Canvas assignment/rubric/deadline when signed in. The attempt in this continuation reached Duke's public login landing page. Previously verified deadline: Tuesday November 24, **10:30 am Central / 11:30 am Eastern**. Personal target: Sunday November 22.
5. Record the final reviewed source commit and complete the remaining checklists. **Aarya submits personally; do not submit through Canvas.**

## Important experiment result

Held-out MAE is 3.0594 locations versus persistence 2.9016. The model's higher average absolute error remains disclosed. Displayed 2024 estimates use observations ending in 2023 and are unverified historical estimates. Financial context and the editable calculator do not predict personal income.

## Instructor-facing continuation review

See [INSTRUCTOR_REVIEW.md](INSTRUCTOR_REVIEW.md) for the ML implementation/evidence map, presentation changes, and remaining source-access/team eligibility checks. Tanya’s confirmed account is `Tanya-duke`; [TANYA_START_HERE.md](TANYA_START_HERE.md) prepares her independent Docker/model-review PR. Invitation was sent to `Tanya-duke` and awaits acceptance. The prepared research-first homepage is local until published.
