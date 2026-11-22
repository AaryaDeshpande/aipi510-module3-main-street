# Team workflow and genuine contribution record

Aarya confirms the Module 3 teammates are **Aarya Deshpande and Tanya**. Tanya's GitHub handle and exact display name for submission still need recording. No additional teammate has been assumed. The syllabus's general group-size wording and the assignment's partner wording are recorded in the source audit; the working roster here follows Aarya's confirmation.

Repository: <https://github.com/AaryaDeshpande/aipi510-module3-main-street>. The initial source/data/assets/tests upload is committed on `aarya/module3-implementation`; final documentation/artifact/workflow upload and instructor access still need checking. The AI-assisted implementation PR will be opened as a draft for Aarya's review before any approved merge.

## Contributions to record

The implementation was prepared with AI assistance. The rows below distinguish suggested review work from completed human contributions. Each person should author their own meaningful changes in their own GitHub identity, open their own PR, and explain what they changed and checked. Existing local files are not proof of either person's authorship.

| Member | Suggested bounded responsibility, pending agreement | Personally completed work and evidence | Authored PR |
|---|---|---|---|
| Aarya Deshpande | Review the business question, ownership homepage, prior-project attribution, and final data/model limitations; make and explain substantive improvements | Pending recorded personal review and actual changes | Pending |
| Tanya | Independently build Docker, train and serve inside it, run real HTTP/curl checks, and review data dates/limitations; record commands, machine, date, results, and any necessary fix in her own branch/PR | Pending her actual execution, review, and authored changes | Pending |

Cloud/container responsibilities depend on who has the approved account and working runtime. Record the real operator and execution evidence when those checks finish. These proposed responsibilities do not prevent either member from taking the other work package by agreement.

A concrete meaningful Tanya PR can add her independently executed local Docker evidence and correct any issue discovered. Include machine/runtime, date, exact commands, exit results, model/data hashes, HTTP outputs, and the data-date/limitation review. This would establish the local Docker gate when she actually performs it. No such execution or authorship is claimed yet.

## Finish in this order

1. Both members run or inspect the app and read the assignment audit, README, and model limitations. Explain why the county counts, IRS financial context, and calculator measure different things.
2. Agree on bounded changes that each person will actually perform. Create separate branches, such as `aarya/ownership-review` and `tanya/reproducibility-review`; use the branch owner’s own identity.
3. Complete each change, run the relevant checks, and open a meaningful PR. Include the concrete change, source references where applicable, and actual validation output. Record the URL above only after the PR exists.
4. Review the other person's PR and resolve issues. Preserve actual authorship and review history. Merge only within the team's authorized repository workflow.
5. Preserve the completed R2 cloud-ingestion evidence, 61 passing tests, 12 passed cloud-source reproduction checks, four finished MLflow runs, and serving-only HTTP checks. Execute the remaining Docker training/serving and public frontend/API checks. Label a hosted Actions run as CI evidence, and record a teammate-machine Docker run for the assignment's local execution wording.
6. Fill the real deployed URLs into README and SUBMISSION.md, check instructor access, and complete the final requirement audit. Aarya reviews the final result and submits through Canvas personally. No automated submission is planned.

The personal target is Sunday, November 22, 2026. The earlier verified Canvas deadline is November 24, 11:30 am Eastern / 10:30 am Central; fresh Canvas instructions still need checking when sign-in access permits.

## What both members should be able to explain

- **Data:** official CBP county–industry observations from 2019–2023. The panel is frozen and hash checked. Unpublished cells remain unknown. Establishments count business locations.
- **Learning:** earlier years train the preprocessing and Ridge model; the following year selects the setting; a later held-out year measures performance. Future labels do not enter features.
- **Result:** held-out model MAE is 3.0594 locations, while the no-change baseline is 2.9016. The selected model has higher average absolute error. Its displayed 2024 estimates are historical, unverified estimates.
- **Engineering:** configuration identifies the data and settings; MLflow logs actual runs; the saved pipeline is loaded for JSON requests. The container must be built and its training and serving entry points executed before claiming that requirement is complete.
- **Practical use:** cases and financial context explain repeat purchases, costs, ownership routes, and assumptions to investigate. The scenario is editable arithmetic. Customer access, demand, willingness to pay, personal fit, and investment outcomes remain unverified.

## Attribution

The [Module 1 local-service market screen](https://github.com/AaryaDeshpande/aipi510-module1-local-service-market-screen) is prior national market-screening research. The [Week 12 Iris pipeline](https://github.com/AaryaDeshpande/aipi510-week12-ml-pipeline) is an earlier learning source for engineering patterns. The current business regression experiment and its results must be evaluated independently. README documents AI assistance and the reused patterns. Cite any further code or templates actually reused.

Do not enter invented contribution summaries, PRs, test results, deployment URLs, or submission confirmations. Record executed checks with their run URL or report path and the exact commit they tested.
