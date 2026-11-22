# Team handoff and final review

**Confirmed Module 3 teammates: Aarya Deshpande and Tanya**, as confirmed by Aarya. [Authorized AI-assisted draft PR #1](https://github.com/AaryaDeshpande/aipi510-module3-main-street/pull/1) exists; Aarya’s personal review and approval before merge are pending. Tanya’s GitHub handle and own meaningful PR remain pending. See [TEAM_WORKFLOW.md](TEAM_WORKFLOW.md) for the authoritative contribution record and [SUBMISSION.md](SUBMISSION.md) for the final review sheet. The syllabus's general group-size wording and assignment's partner wording remain documented in the source audit; no additional teammate has been assumed.

## Suggested work packages

Aarya and Tanya can agree on these work packages. Each member reviews and authors their actual changes and PR. These suggestions do not represent completed human contributions.

| Work package | Concrete deliverable | Owner |
|---|---|---|
| Data and evaluation | Review official source/provenance, chronological joins, missingness, baseline and negative MAE result; execute reproduction and author relevant PR | Actual member, pending agreement |
| Cloud and containers | Prove upload/retrieval, build and run training/serving image, deploy to approved target, retain HTTP/model-hash evidence; author relevant PR | Actual member with approved access, pending agreement |
| Visual workflow and documentation | Verify map/filter consistency, phone use, shortlist/CSV, API call/errors, sources, final links and requirement coverage; author relevant PR | Actual member, pending agreement |

## Completion order for Sunday November 22

1. Use the confirmed Aarya/Tanya roster and [project repository](https://github.com/AaryaDeshpande/aipi510-module3-main-street); review the completed implementation branch/draft PR and agree who will run Docker locally. Cloud storage and cloud-ingested training are already verified.
2. Review the prepared app and explain the data/model. Resolve incorrect assumptions before deployment.
3. Preserve completed R2 cloud-ingestion/training evidence, 12 passed reproduction checks, 61 passing tests, four finished MLflow runs, and inference-only HTTP results. Run Docker training/serving on a teammate's machine; hosted [Docker CI already passed](https://github.com/AaryaDeshpande/aipi510-module3-main-street/actions/runs/45013764218) and is recorded separately.
4. Publish the approved service and test it through the actual public page on desktop and phone.
5. Complete each real member's meaningful PR, final README links, and evidence checklist.
6. Aarya reviews the final repository/demo/Canvas entry and submits personally once the required evidence is in place. No automated Canvas submission is planned.

Aim for a working verified public link by the afternoon to leave time for account/build issues. The previously verified Canvas deadline is Tuesday November 24, 10:30 am Central / 11:30 am Eastern; Sunday remains the personal completion target. Fresh Canvas access is currently blocked by sign-in, so check for any final instruction update when access is available.

## Actual contributions and PRs

Fill with observed work only:

| Member | Work personally reviewed/performed | Authored PR URL |
|---|---|---|
| Aarya Deshpande | Authorized AI-assisted implementation uploaded; personal review/understanding and merge approval pending | [Draft PR #1](https://github.com/AaryaDeshpande/aipi510-module3-main-street/pull/1) |
| Tanya | Pending personal review/execution and team agreement; GitHub handle still to record | Pending |

The current implementation was prepared with AI assistance. The README describes this and the reused learning/engineering sources. Every actual author should be able to explain their contribution and the complete pipeline.

## Explain the project in plain language

1. **Freeze reliable history.** Download official Census business data, keep ten consistent service-industry categories, preserve missing information, and save a versioned cleaned panel. Put that panel in cloud storage and verify the downloaded bytes when training.
2. **Separate learning from checking.** Use 2019/2020 counts to learn predictions for 2021; choose a Ridge setting using the 2022 target; reserve the 2023 target for the final test. Fit learned preprocessing only on training rows.
3. **Save and serve the recipe.** Record real experiments in MLflow, pin dependencies, save the preprocessing/model together, run it in Docker, and expose a JSON prediction API. The public webpage sends the selected measurements to that API.
4. **Use the evidence carefully.** The map/history/comparisons organize market research. The forecasting experiment has worse held-out MAE than the simple no-change baseline. Its 2024 estimate is historical and unverified. Owner needs, budget, and partner fit require real conversations.

## The result everyone should understand

The selected model's held-out MAE is **3.0594 business locations**, compared with **2.9016** for carrying the previous count forward, a **5.4% deterioration** in the primary metric. Its RMSE is lower (8.6409 versus 9.0990). These outcomes are retained honestly. We did not tune on the test set or refit on validation/test rows to improve the reported result.

Training covers complete national histories in ten industries; the interface displays Wisconsin's 72 counties. The snapshot ends in 2023. A business location count, employment estimate, and payroll figure each measure a different aspect of market scale. None establishes profits, a named owner's wealth, or confirmed demand for a new product. G/H/J noise flags and unavailable cells must remain visible in the interpretation.

## Final evidence gates

- [x] Actual teammates confirmed by Aarya: Aarya Deshpande and Tanya.
- [ ] Both members have meaningful, correctly authored PRs with recorded URLs.
- [x] Cleaned data stored in R2; actual cloud training retrieves it and records matching hash, version, and 110,488 rows.
- [x] Current checks: 61 tests, 12 cloud-source reproduction checks, four finished MLflow runs, and real inference-only Gunicorn HTTP/curl checks.
- [ ] Final code/model passes the executed tests and repeated-run checks; reports describe their exact scope.
- [x] Hosted Docker build/train/reproduction/serve/HTTP checks pass in [run 45013764218](https://github.com/AaryaDeshpande/aipi510-module3-main-street/actions/runs/45013764218); evidence retained in reports/ci/.
- [ ] Teammate-machine Docker build/train/serve/HTTP results recorded for the local requirement.
- [ ] Public frontend and API are reachable to the instructor; frontend makes a real successful prediction request.
- [ ] Final live desktop/phone checks completed. Earlier local desktop QA is retained; the latest private Site attempt stopped at sign-in (`reports/final_ui_check.json`).
- [ ] Model/baseline outcome and historical 2024 status are presented accurately.
- [ ] README has real GitHub, frontend, and API links plus setup/train/test/deploy instructions and sources.
- [ ] Final requirements reviewed against the published assignment, with unresolved items disclosed.
- [ ] Aarya reviews the final repository, public demo, and Canvas entry.
- [ ] Any shared-repository changes, publication, or submission receive the required explicit approval.
- [ ] Aarya submits personally and records the observed Canvas confirmation and timestamp.
