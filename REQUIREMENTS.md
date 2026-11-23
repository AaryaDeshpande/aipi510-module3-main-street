# Module Project 3 requirement coverage

Checked against the signed-in [Canvas assignment](https://canvas.duke.edu/courses/83524/assignments/363937). Due November 24, 2026, **10:30 am Central / 11:30 am Eastern**; 200 points. Canvas explicitly excludes accuracy from assessment. This map records evidence rather than predicting a grade.

| Requirement | Status | Evidence |
|---|---|---|
| Public dataset, supervised target and metric | Complete | Census CBP; next-year establishment count; MAE; README and `data/SOURCE.json` |
| Cleaning and programmatic cloud ingestion | Executed; provider caveat below | `prepare.py`, `data.py`, actual R2 retrieval and `artifacts/ingestion.json` |
| Preprocessing, features, train/validation/test | Complete | Chronological targets 2021/2022/2023, training-only learned transformations |
| Simple model controlled by config.yaml | Complete | Ridge alpha selected on validation; effective configuration retained |
| MLflow/W&B parameters, metrics, artifacts | Complete | Four finished MLflow runs and saved model/evaluation |
| requirements.txt and Dockerfile | Complete | Pinned dependencies; training and serving entry points |
| Build/run Docker locally | Team action pending | [Hosted Docker CI passed](https://github.com/AaryaDeshpande/aipi510-module3-main-street/actions/runs/45284798476); Tanya's independent computer run is prepared separately |
| Flask /predict JSON endpoint | Complete | Saved model/preprocessing loaded; real success and input-error checks |
| Public cloud API | Executed; provider caveat below | [Production service](https://aipi510-module3-main-street.vercel.app/); public HTTP checks pass |
| Interactive public frontend consumes live API | Complete | Homepage prediction verified in browser; 281.2 model vs 276 persistence |
| README training, local API, cloud deployment and links | Complete | README and DEPLOYMENT.md |
| Structure, branches, history, each member PR | Partly complete | Implementation branch and Aarya draft PR; Tanya's genuine PR and team review remain |
| Ethics and limitations | Complete documentation | Historical data, missing cells, population limits, weaker-than-baseline result, no demand/profit claims |
| Final repository/demo submission | Pending Aarya | SUBMISSION.md contains the links; no submission made |

## Course checks still open

- **Providers:** R2 cloud storage and Vercel Flask API are operational. Canvas names other storage/API providers; Vercel is explicitly listed for the frontend. Instructor acceptance of the substitutions has not been established. Prepared GCS support is not an executed GCS deployment.
- **Roster:** working partners are Aarya and Tanya. Confirm the Canvas Project Groups membership and applicable team exception; the syllabus's general wording differs from the assignment's partner wording.
- **Contributions:** Aarya personally reviews PR #1. Tanya accepts the invite, performs meaningful work and authors her own PR. Her proposed local Docker reproduction covers another remaining requirement when actually performed.

Phone review and simulated frontend outage are optional QA, not additional quoted assignment requirements. See STATUS.md for the latest evidence and TEAM_ACTIONS.md for the human steps.
