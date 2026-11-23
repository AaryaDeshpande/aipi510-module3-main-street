# Understand the project in two minutes

Open the [live website](https://aipi510-module3-main-street.vercel.app/). Choose a business category and Wisconsin county, inspect its history, then click **Run estimate for this selection**.

The assignment asks for a complete machine-learning system: real data stored in the cloud, reproducible training, recorded experiments, a deployed prediction API, and an interactive website. The quality of the model's accuracy is explicitly not graded.

Our question is: **can earlier counts of business locations help estimate next year's count?** Official Census data covers 2019–2023. A Ridge regression model learns from earlier years, a separate year selects its setting, and a reserved year checks the result. The website sends your selected counts to the deployed Python model and displays its answer. The displayed 2024 estimate is a historical exercise, not current 2026 information.

- **ML training** is the Python process that learns the model's numerical settings from historical examples. It already ran and saved the model.
- **MLflow** records training settings, results, and model artifacts. Four real runs are retained.
- **API** means a URL accepting a structured request and returning a prediction. The website calls `/predict`.
- **Docker** packages Python, dependencies, and the commands into a repeatable environment. Its build, training, and serving have passed in GitHub Actions; a teammate still needs to run it locally for the assignment wording.
- **Pull request (PR)** is a proposed change on a separate GitHub branch for teammates to review. Every member needs their own actual contribution/PR.

The held-out model error averages **3.06 locations**, versus **2.90** for simply using the previous count. The model's weaker result is reported honestly. The engineering workflow is the main assignment objective.

Verified: cloud ingestion, preprocessing, chronological splits, training, MLflow, saved-model API, public website, 61 tests, 12 reproduction checks, Docker CI, and real public prediction requests. The optional `/ownership` worksheet provides business-research context; it is separate from the ML model.

## Remaining team steps

1. **Aarya:** read [START_HERE.md](START_HERE.md), use the [live app](https://aipi510-module3-main-street.vercel.app/), and personally review [draft PR #1](https://github.com/AaryaDeshpande/aipi510-module3-main-street/pull/1). Correct anything you cannot explain. Mark it ready and merge only after the team review is complete. The implementation is on `aarya/module3-implementation`; `main` still has initialization content.
2. **Tanya (`Tanya-duke`):** accept the collaborator invitation, independently run the local Docker training/API workflow, record the actual results and any corrections, and open your own PR. [TANYA_START_HERE.md](TANYA_START_HERE.md) has exact commands and branch instructions. Aarya reviews her PR. No completed Tanya contribution is claimed.
3. **Team:** confirm the Canvas Project Groups roster and any existing online-cohort/team exception. The assignment says partner; the syllabus has different general team wording. Current group membership was not established.
4. **Course platform interpretation:** actual storage is Cloudflare R2 and the Flask API/frontend run on Vercel. Canvas explicitly allows Vercel for the frontend but names GCS/S3/Firebase/cloud PostgreSQL for storage and Google/AWS/Azure for the API. Functional cloud operation is verified; acceptance of these substitutions is unverified. The GCP console was unavailable in this environment, so no listed-provider migration is claimed.
5. **Aarya:** after the contributions, reviews, and course checks, submit the repository and frontend links personally using [SUBMISSION.md](SUBMISSION.md). Due **November 24, 2026, 10:30 am Central / 11:30 am Eastern**. No Canvas submission has been made.
