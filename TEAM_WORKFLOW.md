# Team workflow and genuine contribution record

Aarya confirms the Module 3 teammates are **Aarya Deshpande and Tanya**. Tanya's GitHub handle and exact display name for submission still need recording. No additional teammate has been assumed. The syllabus's general group-size wording and the assignment's partner wording are recorded in the source audit; the working roster here follows Aarya's confirmation.

Repository: <https://github.com/AaryaDeshpande/aipi510-module3-main-street>. The 85-file implementation is uploaded on the [review branch](https://github.com/AaryaDeshpande/aipi510-module3-main-street/tree/aarya/module3-implementation); use that branch or [draft PR #1](https://github.com/AaryaDeshpande/aipi510-module3-main-street/pull/1) while default main remains initialization. The draft is authorized AI-assisted work awaiting Aarya’s personal review and approval before merge.

## Contributions to record

The implementation was prepared with AI assistance. The rows below distinguish suggested review work from completed human contributions. Each person should author their own meaningful changes in their own GitHub identity, open their own PR, and explain what they changed and checked. Existing local files are not proof of either person's authorship.

| Member | Suggested bounded responsibility, pending agreement | Personally completed work and evidence | Authored PR |
|---|---|---|---|
| Aarya Deshpande | Review the business question, ownership homepage, attribution, pipeline and limitations; explain and approve any final changes | Authorized AI-assisted implementation uploaded; personal review and merge approval pending | [Draft PR #1](https://github.com/AaryaDeshpande/aipi510-module3-main-street/pull/1) |
| Tanya | Independently build Docker, train and serve inside it, run real HTTP/curl checks, and review data dates/limitations; record commands, machine, date, results, and any necessary fix in her own branch/PR | Pending her actual execution, review, and authored changes | Pending |

Cloud/container responsibilities depend on who has the approved account and working runtime. Record the real operator and execution evidence when those checks finish. These proposed responsibilities do not prevent either member from taking the other work package by agreement.

A concrete meaningful Tanya PR can add her independently executed local Docker evidence and correct any issue discovered. Include machine/runtime, date, exact commands, exit results, model/data hashes, HTTP outputs, and the data-date/limitation review. This would establish the local Docker gate when she actually performs it. No such execution or authorship is claimed yet.

## Tanya: start from the actual implementation

Default `main` currently has initialization content. Until Aarya approves and merges draft PR #1, Tanya should branch from the existing implementation branch so she gets the code, data, and Dockerfile:

```bash
git clone --branch aarya/module3-implementation https://github.com/AaryaDeshpande/aipi510-module3-main-street.git
cd aipi510-module3-main-street
git fetch origin
git switch -c tanya/independent-review origin/aarya/module3-implementation
```

For an existing checkout, start with `git fetch origin` and the `git switch` command. Tanya then independently follows DEPLOYMENT.md, records her actual machine/date/commands/results and any fixes, commits her work with her own identity, and pushes her branch if she has write access. Open her PR with **base `aarya/module3-implementation`** and **head `tanya/independent-review`**. Review that PR before merging it; its changes will then be included in the still-open implementation PR.

If Tanya has no repository write access, she can use her own GitHub fork: fetch the implementation branch from this upstream repository, branch from it, push to her fork, and open a PR back to upstream with base `aarya/module3-implementation` and her fork/branch as the head. Use her actual account; no handle is assumed here. No invitation or message has been sent to her.

If Aarya first approves and merges PR #1, Tanya can instead fetch the updated `main`, branch from `origin/main`, and target `main` in her PR. Check which state exists before starting. Neither creating a branch nor copying these commands establishes that Tanya has run Docker or authored a contribution.

## Finish in this order

1. Both members run or inspect the app and read the assignment audit, README, and model limitations. Explain why the county counts, IRS financial context, and calculator measure different things.
2. Agree on bounded changes that each person will actually perform. Tanya follows the implementation-branch instructions above; each branch owner uses their own identity. Aarya reviews the existing draft implementation PR before approving any merge.
3. Complete each change, run the relevant checks, and open a meaningful PR. Include the concrete change, source references where applicable, and actual validation output. Record the URL above only after the PR exists.
4. Review the other person's PR and resolve issues. Preserve actual authorship and review history. Merge only within the team's authorized repository workflow.
5. Preserve the completed R2 cloud-ingestion evidence, 61 passing tests, 12 passed cloud-source reproduction checks, four finished MLflow runs, and serving-only HTTP checks. [Hosted Docker CI](https://github.com/AaryaDeshpande/aipi510-module3-main-street/actions/runs/45013764218) has now passed build/train/reproduction/serve/HTTP checks. Preserve its evidence in `reports/ci/`, then record a teammate-machine Docker run for the local execution wording and complete the final public frontend/API checks.
6. Fill the real deployed URLs into README and SUBMISSION.md, check instructor access, and complete the final requirement audit. Aarya reviews the final result and submits through Canvas personally. No automated submission is planned.

The personal target is Sunday, November 22, 2026. The earlier verified Canvas deadline is November 24, 11:30 am Eastern / 10:30 am Central; fresh Canvas instructions still need checking when sign-in access permits.

## What both members should be able to explain

- **Data:** official CBP county–industry observations from 2019–2023. The panel is frozen and hash checked. Unpublished cells remain unknown. Establishments count business locations.
- **Learning:** earlier years train the preprocessing and Ridge model; the following year selects the setting; a later held-out year measures performance. Future labels do not enter features.
- **Result:** held-out model MAE is 3.0594 locations, while the no-change baseline is 2.9016. The selected model has higher average absolute error. Its displayed 2024 estimates are historical, unverified estimates.
- **Engineering:** configuration identifies the data and settings; MLflow logs actual runs; the saved pipeline is loaded for JSON requests. The container must be built and its training and serving entry points executed before claiming that requirement is complete.
- **Practical use:** cases and financial context explain repeat purchases, costs, ownership routes, and assumptions to investigate. The scenario is editable arithmetic. Customer access, demand, willingness to pay, personal fit, and investment outcomes remain unverified.

**Hosted Docker CI passed:** [run 45013764218](https://github.com/AaryaDeshpande/aipi510-module3-main-street/actions/runs/45013764218) built the image, trained inside it, reproduced metrics/splits/predictions, served the container-trained model, passed real HTTP/curl checks, and uploaded evidence. The tested commit is `520e0d1b3b52d80173ef2920a663943784aab8a3`. `reports/ci_observation.json` records the successful job, and `reports/ci/` retains downloaded execution evidence. This establishes hosted Ubuntu execution; a teammate-machine Docker run remains separate.

The latest live-browser attempt stopped at the private Site’s ChatGPT sign-in gate (`reports/final_ui_check.json`). Final live ownership controls, export, calculator, market predictions, and phone layout were not rechecked. The earlier local desktop QA reports remain dated evidence.

## Attribution

The [Module 1 local-service market screen](https://github.com/AaryaDeshpande/aipi510-module1-local-service-market-screen) is prior national market-screening research. The [Week 12 Iris pipeline](https://github.com/AaryaDeshpande/aipi510-week12-ml-pipeline) is an earlier learning source for engineering patterns. The current business regression experiment and its results must be evaluated independently. README documents AI assistance and the reused patterns. Cite any further code or templates actually reused.

Do not enter invented contribution summaries, PRs, test results, deployment URLs, or submission confirmations. Record executed checks with their run URL or report path and the exact commit they tested.
