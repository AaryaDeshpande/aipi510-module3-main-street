# Verified project status

Updated November 23, 2026. [Live app](https://aipi510-module3-main-street.vercel.app/) · [implementation branch](https://github.com/AaryaDeshpande/aipi510-module3-main-street/tree/aarya/module3-implementation) · [draft PR #1](https://github.com/AaryaDeshpande/aipi510-module3-main-street/pull/1).

| Requirement area | Recorded evidence |
|---|---|
| Official data and cleaning | 110,488 Census county–industry–year rows, 2019–2023; `data/SOURCE.json` and `business_app/prepare.py` |
| Cloud storage and programmatic ingestion | Actual R2 object retrieval, version/hash verification; `reports/cloud_storage.json`, `artifacts/ingestion.json`, `reports/cloud_training.log` |
| Reproducible ML | Configuration, train-only preprocessing, chronological 2021/2022/2023 targets, validation-selected Ridge; `config.yaml`, `business_app/train.py` |
| Experiment tracking | Four finished MLflow runs with parameters, metrics and artifacts; `reports/mlflow_runs.json` |
| Evaluation | Test MAE 3.0594, persistence 2.9016; the model's higher error is disclosed |
| Checks | 61 tests and 12 cloud-source reproduction checks passed; `reports/pytest.txt`, `reports/reproducibility.json` |
| Docker | [Run 45284798476](https://github.com/AaryaDeshpande/aipi510-module3-main-street/actions/runs/45284798476) passed actual image build, training, evaluation reproduction, serving, HTTP requests and artifact upload |
| Public deployment | READY `dpl_AkkQfyWPFsSXYMBsffBJPYH2ncQD`, application source `f4e78dbdb72bf78c4f49586b89a317eb72b5d0f6` |
| Public API | `reports/final_public_http_smoke.json`: health, frontend, model hash/catalog, 72 county geometries, three JSON predictions, invalid-input rejection all pass |
| Public UI | New ML homepage and real browser prediction verified: Dane building-equipment estimate 281.2, persistence 276; `reports/final_release_review.json` |
| Canvas read | Signed-in assignment read; 200 points, accuracy excluded, local Docker and member PRs required; `reports/canvas_access_review.json` |
| Collaboration | Aarya draft PR exists; invitation to Tanya-duke sent and last observed awaiting acceptance |

Earlier reports retain their original dates and scope. They do not override this status. The new homepage is published; earlier private-Site and deployment-pending notes are historical.

## Remaining team steps

1. **Aarya:** read [START_HERE.md](START_HERE.md), use the [live app](https://aipi510-module3-main-street.vercel.app/), and personally review [draft PR #1](https://github.com/AaryaDeshpande/aipi510-module3-main-street/pull/1). Correct anything you cannot explain. Mark it ready and merge only after the team review is complete. The implementation is on `aarya/module3-implementation`; `main` still has initialization content.
2. **Tanya (`Tanya-duke`):** accept the collaborator invitation, independently run the local Docker training/API workflow, record the actual results and any corrections, and open your own PR. [TANYA_START_HERE.md](TANYA_START_HERE.md) has exact commands and branch instructions. Aarya reviews her PR. No completed Tanya contribution is claimed.
3. **Team:** confirm the Canvas Project Groups roster and any existing online-cohort/team exception. The assignment says partner; the syllabus has different general team wording. Current group membership was not established.
4. **Course platform interpretation:** actual storage is Cloudflare R2 and the Flask API/frontend run on Vercel. Canvas explicitly allows Vercel for the frontend but names GCS/S3/Firebase/cloud PostgreSQL for storage and Google/AWS/Azure for the API. Functional cloud operation is verified; acceptance of these substitutions is unverified. The GCP console was unavailable in this environment, so no listed-provider migration is claimed.
5. **Aarya:** after the contributions, reviews, and course checks, submit the repository and frontend links personally using [SUBMISSION.md](SUBMISSION.md). Due **November 24, 2026, 10:30 am Central / 11:30 am Eastern**. No Canvas submission has been made.


Optional QA still unrecorded: actual phone layout and simulated frontend API outage. Public invalid-input API checks already pass.
