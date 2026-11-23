# Module Project 3 requirements audit

Audit date: November 21, 2026 (Central). Scope: read-only course-source review. No shared repository, cloud resource, message, or submission was changed.

## Evidence and access

| Source | Evidence obtained | Limit |
|---|---|---|
| [Canvas assignment 363937](https://canvas.duke.edu/courses/83524/assignments/363937) | The prior signed-in review in this conversation captured the assignment checklist, submission format, and exact due time. | A fresh attempt during this audit redirected to Duke sign-in. No credentials were requested or entered, so the assignment text and deadline were not refreshed in this audit. |
| [Official syllabus](https://docs.google.com/document/d/1y0gghRpzgDZEh8-y4mgQo5R2JyfKUnmOnta6tOKp4oM/edit) | Fresh full text retrieved through the connected Drive account. File modified November 15, 2026. Confirms grading, team expectations, originality/code-source policy, and AI policy. | The syllabus supplies the project date but not its exact submission time. |
| [Week 13 announcement](https://canvas.duke.edu/courses/83524/announcements/359531) | Fresh full plain-text copy read from its November 16 Canvas notification email in the course email account. It links assignment 363937 and says the project is due next week. | It does not specify the exact time, team roster, or detailed rubric. |
| Recent course email searches | Searches for the assignment ID, Module Project 3, Module 3, Data/ML Engineering, and AIPI 510 found no newer project-specific deadline or requirement update. | Search results are not proof that an announcement, Discord conversation, or extension does not exist elsewhere. |

The Week 13 email clearly distinguishes the vector-database activity, optional SQL Holmes investigation, and Module Project 3. The Week 12 code puzzle is also a separate synchronous activity in the syllabus.

## Due time and grading

- **Previously verified assignment deadline:** November 24, 2026 at 16:30 UTC, which is **11:30 am Eastern / 10:30 am Central**.
- Personal target: finish on Sunday November 22.
- The syllabus assigns **200 points / 20% of the 1,000-point course** to Module Project 3.
- The syllabus's Tuesday 2:30 pm deadline refers to online synchronous activities. It should not replace the assignment-specific time.
- No separate scored rubric was observed in the earlier assignment/gradebook review. This audit could not refresh Canvas to establish whether that has changed. The published assignment checklist is the available acceptance checklist; no invented point allocation should be added.

## Assignment checklist retained from the prior signed-in review

1. Use a public dataset for supervised classification or regression.
2. Clean the data locally; place the cleaned data in cloud storage or a cloud database; retrieve it programmatically in the pipeline.
3. Include `config.yaml`, preprocessing/feature handling, separate training/validation/test sets, a simple fitted model, and evaluation.
4. Use MLflow or Weights & Biases to record experiments, parameters, metrics, and model/artifacts.
5. Pin the software environment with `requirements.txt` or an equivalent environment file.
6. Provide a Dockerfile with training and serving entry points; actually build and run it locally.
7. Provide a Flask or FastAPI JSON `/predict` endpoint and deploy it publicly on a cloud service. Cloud Run/Functions, AWS Lambda/API Gateway, and Azure Functions are named examples.
8. Provide a public frontend that calls the deployed API. A custom frontend/framework/platform is allowed. An interface that displays static results alone does not demonstrate this requirement.
9. Document the project, dataset/source, model/evaluation, cloud services, setup/train/test/deploy procedure, and ethics/limitations in the README. Include both the frontend URL and deployed API URL.
10. Use branches, with each actual group member authoring at least one pull request.
11. Submit the GitHub repository URL and live frontend URL in the Canvas text entry.

The prior review recorded that predictive accuracy is not the grading focus. Evaluation must nevertheless be genuine, reproducible, and honestly reported. The new business dataset needs its own results; Iris results and tests cannot establish its performance or completion.

## Team and attribution requirements

The fresh syllabus says module projects are completed in teams of three, with new team members for every project, and are expected to require approximately 40 hours. The previously reviewed assignment also used partner language. At the November 21 course-source audit, the actual Module 3 roster had not yet been established. On November 22, Aarya confirmed **Aarya Deshpande and Tanya** as partners; see `TEAM_WORKFLOW.md`. Genuine authored PRs and human contributions still require observed evidence.

The syllabus permits online code snippets when their source is cited. Its stated consequence for copying code without citation is a grade of zero. It also expects originality and says that copying or slightly altering someone else's work can result in a poor grade. Record reused code or templates, source URLs, and material modifications in the README. A project-specific data pipeline, evaluation, and interface should be understandable to its actual authors.

## AI policy: freshly verified

The syllabus explicitly assumes students will use generative AI for assignments. It recommends citing AI resources and states that points will not be deducted for omitting an AI citation. It recommends attempting work first and checking AI outputs carefully.

This supports AI-assisted implementation for this assignment. A concise README acknowledgment is appropriate and transparent. The syllabus does not require an AI banner in the product interface. Actual team review, understanding, execution, citations, and truthful authorship still matter.

## Business-explorer review considerations

The regression target should be a measurable published quantity such as next-year establishment count. Historical county/industry data can support screening and backtesting. It does not establish an individual owner's wealth, current unmet demand, willingness to buy an AI service, or the user's probability of earning a particular amount.

For this forecasting project, chronological train/validation/test separation, consistent industry definitions across years, matching county identifiers, and explicit exclusion of future-year inputs are important implementation choices. The assignment requires the three splits; the chronological design follows from this particular target.

## Completion gaps recorded at audit, with November 22 updates

- Fresh assignment/rubric access, if a final current-page check is needed.
- Aarya’s authorized AI-assisted [draft PR #1](https://github.com/AaryaDeshpande/aipi510-module3-main-street/pull/1) now exists; personal review/approval before merge, Tanya’s own meaningful PR, and both partners’ review remain open.
- Cloud storage and ingestion were open at this audit; the November 22 R2 storage, actual cloud training, 12-check reproduction, and four finished MLflow runs now provide execution evidence. See current `STATUS.md` and `reports/environment_checks.json`.
- Actual hosted Ubuntu Docker build/train/reproduction/serve/HTTP execution now passes in [run 45013764218](https://github.com/AaryaDeshpande/aipi510-module3-main-street/actions/runs/45013764218). Retain a separate teammate-machine run for the assignment’s local execution wording.
- Public API/frontend deployment, signed-out access, and a real frontend-to-API prediction.
- Final README links and evidence matching the final source/model.
- User review and explicit authorization for any shared-repository changes, publication, or submission that remain outside existing authorization.

Passing local checks alone should be reported as local progress. Submission completion must be verified independently after the user authorizes the submission action.

## Continuation update, November 22

The public Flask/API deployment and signed-out desktop checks now pass at <https://aipi510-module3-main-street.vercel.app/>. Exact deployed source and execution evidence are in `reports/public_deployment.json`, `reports/public_http_smoke.json`, and `reports/public_browser_checks.json`. Phone/device and unavailable-API checks remain open. A fresh navigation to the assignment reached Duke's public Canvas login landing page, so current assignment text/rubric/deadline were not refreshed. The earlier audit and its source limits remain historical evidence.

## Latest signed-in review

## Latest verified access update

Canvas sign-in succeeded and assignment 363937 was read directly. The deadline is November 24, 2026 at **10:30 am Central / 11:30 am Eastern** (16:30 UTC). The current assignment explicitly excludes predictive accuracy from assessment, requires each member to author a PR, and requires a local Docker build/run. GitHub invitation **345631416** was sent to **Tanya-duke** and is awaiting her response. Older login-blocker notes below describe earlier attempts. See `reports/canvas_access_review.json` for current findings.

The current assignment text was read directly. The global Groups list showed MENG 570 groups and no AIPI Project Groups entry; no group enrollment was changed. Cloud provider substitutions (R2 storage and Vercel Flask API) remain a platform-choice interpretation to confirm against the named lists. Full details: `reports/canvas_access_review.json` and `INSTRUCTOR_REVIEW.md`.
