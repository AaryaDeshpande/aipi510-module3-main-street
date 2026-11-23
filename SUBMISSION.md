# Final submission sheet

Due **November 24, 2026, 10:30 am Central / 11:30 am Eastern**. Canvas was read while signed in; see `reports/canvas_access_review.json`. No submission has been made.

## Links

- Repository: https://github.com/AaryaDeshpande/aipi510-module3-main-street
- Current implementation: https://github.com/AaryaDeshpande/aipi510-module3-main-street/tree/aarya/module3-implementation
- Frontend: https://aipi510-module3-main-street.vercel.app/
- JSON prediction API: https://aipi510-module3-main-street.vercel.app/predict (POST)
- Aarya's draft PR: https://github.com/AaryaDeshpande/aipi510-module3-main-street/pull/1
- Tanya's PR: pending her actual contribution
- Docker validation: https://github.com/AaryaDeshpande/aipi510-module3-main-street/actions/runs/45284798476

The default `main` branch still contains initialization. Complete team review and merge the reviewed implementation before submitting the repository root link. Check that README and the project files then appear on `main`.

## Prepared submission text

```text
Main Street Business Explorer — AIPI 510 Module Project 3
Team: Aarya Deshpande and Tanya Sharma
GitHub: https://github.com/AaryaDeshpande/aipi510-module3-main-street
Live frontend: https://aipi510-module3-main-street.vercel.app/
Live API: https://aipi510-module3-main-street.vercel.app/predict (JSON POST)

A reproducible Census CBP pipeline predicts next-year establishment counts using Ridge regression, logs MLflow experiments, and serves the saved model through Flask. The frontend displays historical Wisconsin data and requests model predictions. README documents sources, evaluation, training, Docker, deployment, and limitations.
```

Confirm the team name and Canvas group, fill the actual contribution/PR record, and resolve or explicitly disclose the provider caveat in REQUIREMENTS.md before using this text. Do not claim instructor approval or completed member work without evidence.

## Remaining team steps

1. **Aarya:** read [START_HERE.md](START_HERE.md), use the [live app](https://aipi510-module3-main-street.vercel.app/), and personally review [draft PR #1](https://github.com/AaryaDeshpande/aipi510-module3-main-street/pull/1). Correct anything you cannot explain. Mark it ready and merge only after the team review is complete. The implementation is on `aarya/module3-implementation`; `main` still has initialization content.
2. **Tanya (`Tanya-duke`):** accept the collaborator invitation, independently run the local Docker training/API workflow, record the actual results and any corrections, and open your own PR. [TANYA_START_HERE.md](TANYA_START_HERE.md) has exact commands and branch instructions. Aarya reviews her PR. No completed Tanya contribution is claimed.
3. **Team:** confirm the Canvas Project Groups roster and any existing online-cohort/team exception. The assignment says partner; the syllabus has different general team wording. Current group membership was not established.
4. **Course platform interpretation:** actual storage is Cloudflare R2 and the Flask API/frontend run on Vercel. Canvas explicitly allows Vercel for the frontend but names GCS/S3/Firebase/cloud PostgreSQL for storage and Google/AWS/Azure for the API. Functional cloud operation is verified; acceptance of these substitutions is unverified. The GCP console was unavailable in this environment, so no listed-provider migration is claimed.
5. **Aarya:** after the contributions, reviews, and course checks, submit the repository and frontend links personally using [SUBMISSION.md](SUBMISSION.md). Due **November 24, 2026, 10:30 am Central / 11:30 am Eastern**. No Canvas submission has been made.


After submitting, save the observed Canvas confirmation and timestamp. A working website alone does not establish submission.
