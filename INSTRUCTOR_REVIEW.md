# Instructor-facing review and requirement evidence

## Latest verified access update

Canvas sign-in succeeded and assignment 363937 was read directly. The deadline is November 24, 2026 at **10:30 am Central / 11:30 am Eastern** (16:30 UTC). The current assignment explicitly excludes predictive accuracy from assessment, requires each member to author a PR, and requires a local Docker build/run. GitHub invitation **345631416** was sent to **Tanya-duke** and is awaiting her response. Older login-blocker notes below describe earlier attempts. See `reports/canvas_access_review.json` for current findings.

Review scope: actual source/artifacts, previously executed cloud and Docker reports, new local serving review, and public HTTP/browser evidence. The current Canvas assignment has now been read directly after successful sign-in. The latest findings below supersede earlier login failures.

## Presentation

The prepared application now opens the county-data and ML research view at `/`, with `/market` as an alias. The introduction states the research question, pipeline, split years/sizes, selected model, and baseline comparison. The supplementary business-economics worksheet remains at `/ownership`. This presentation change is prepared locally and requires publication before it appears on the current live service.

The project uses aggregate published business statistics; it contains no individual wealth ranking or promise of financial returns. Sources, dates, missing values, model limitations, and AI assistance are documented. The freshly retrieved syllabus permits generative AI use and requires attribution for reused code. Human understanding and actual contribution evidence remain necessary.

## Where the ML happens

| Step | Actual implementation/evidence |
|---|---|
| Source and cleaning | `business_app/prepare.py`; `data/SOURCE.json`; frozen panel of 110,488 observations, 2019–2023 |
| Cloud storage and ingestion | R2 object and matching bytes/version recorded in `reports/cloud_storage.json`, `artifacts/ingestion.json`, `reports/cloud_training.log` |
| Supervised target | Predict next-year establishment change from industry and current/previous establishment counts |
| Learned preprocessing | `business_app/train.py`: feature creation, training-fitted StandardScaler and OneHotEncoder |
| Training | Ridge regression `.fit()` on 21,258 rows targeting 2021 |
| Model selection | Alpha 1, 10, 100 compared on 21,132 validation rows targeting 2022; selected alpha 1.0 |
| Reserved test | 21,224 rows targeting 2023; model MAE 3.0594, no-change MAE 2.9016 |
| Experiment tracking | Four actual finished MLflow runs in `reports/mlflow_runs.json` |
| Saved-model serving | `artifacts/model.joblib`; `business_app/web.py` loads it and `/predict` calls `predict_next` |
| Public UI and API | Signed-out stable production domain, real browser prediction, hashes, and invalid-input behavior verified in `reports/public_*.json` for the deployed version recorded there |
| Container | Hosted Docker build/train/reproduction/serving passed in Actions run 45013764218; a teammate-machine run remains pending |

The negative MAE comparison is a valid reported experiment result. The current assignment explicitly says predictive accuracy is not assessed. No accuracy threshold or full-credit guarantee is claimed.

## Requirement status

| Requirement checked against current Canvas page | Current assessment |
|---|---|
| Public supervised dataset; local cleaning | Implemented, sources and tests recorded |
| Cleaned data in cloud; programmatic retrieval | Actual R2-ingested training evidence recorded |
| config.yaml; features; train/validation/test; fitted model; evaluation | Implemented with chronological splits and reserved-test evaluation |
| MLflow/W&B runs | Four actual MLflow runs recorded |
| Pinned dependencies | Pinned serving/training/dev files; clean environments tested |
| Dockerfile and local execution | Hosted Docker CI passed; actual teammate-computer run still pending |
| Flask/FastAPI JSON /predict deployed publicly | Verified publicly for the recorded deployed source |
| Public frontend calls deployed API | Real public browser prediction passed |
| README setup, results, ethics, source, deployment links | Present; latest presentation/team changes await publishing |
| Each member authors a PR | Aarya's draft PR #1 exists; Tanya's Module 3 PR remains pending |
| GitHub and frontend links submitted on Canvas | Prepared only; Aarya submits after review |
| Correct team composition | UNRESOLVED: syllabus says three/new teammates; current roster is Aarya and Tanya, also prior partners. Check assignment exception or existing approval |
| Current assignment/deadline | Directly read; 200 points, unlimited attempts, due Nov 24 16:30 UTC. No separately scored rubric was observed on the assignment page |

## Tanya setup and invitation

Confirmed account: `Tanya-duke`, verified against her authored Module 2 PR #3. `TANYA_START_HERE.md` provides a bounded independent reproduction task, branch/base instructions, and a clearly uncompleted report template. No work is attributed to Tanya until she performs it and opens her PR. Invitation 345631416 was sent and the access page shows Awaiting Tanya-duke’s response. Active accepted access is not claimed.

## Minimum remaining human actions

1. Confirm AIPI Project Groups membership and any team exception: the assignment refers to a partner and group-based submission, while the current global Groups list shows only MENG groups for this account. The syllabus still specifies three/new teammates; the assignment does not explicitly settle that discrepancy.
2. Tanya accepts the GitHub invitation.
3. Publish the prepared commit(s) to the existing draft PR, verify the updated deployment, then Aarya reviews it.
4. Tanya independently runs Docker/reviews the model, records actual evidence, and authors her PR; partners review/merge through the approved workflow.
5. Quick phone/device check, final link/commit check, and Aarya's personal Canvas submission.

Fresh syllabus source: https://docs.google.com/document/d/1y0gghRpzgDZEh8-y4mgQo5R2JyfKUnmOnta6tOKp4oM/edit (modified November 15, freshly read this session). The actual Canvas assignment is https://canvas.duke.edu/courses/83524/assignments/363937 .

## Cloud-provider wording

The current assignment names GCS, AWS S3, Firebase, and cloud PostgreSQL for storage; it names Cloud Run/Functions, AWS Lambda/API Gateway, and Azure Functions for the API. Vercel is explicitly listed for frontend hosting. This implementation uses R2 cloud storage and a Vercel-hosted Flask API. Their executed functional evidence is real, but acceptance of these substitutions is not explicitly stated on the assignment page. Confirm they are allowed or use a named storage/API deployment platform before claiming literal compliance with every platform choice. No paid cloud migration was attempted.
