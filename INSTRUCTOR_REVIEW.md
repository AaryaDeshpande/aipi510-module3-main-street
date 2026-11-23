# ML implementation and evidence map

The submitted application centers on the supervised ML research question. The homepage presents the data-to-API pipeline, chronological splits, held-out evaluation and limitations. `/ownership` is a supplementary worksheet; its arithmetic and financial context are not ML predictions.

| Component | Implementation | Evidence |
|---|---|---|
| Source/cleaning | `business_app/prepare.py`, frozen Census panel | `data/SOURCE.json` |
| Cloud ingestion | `business_app/data.py`, authenticated R2 retrieval | `artifacts/ingestion.json`, `reports/cloud_storage.json` |
| Feature learning/training | `business_app/train.py`, `config.yaml` | effective config, splits, model metadata |
| Experiment logging | MLflow parameters/metrics/model artifacts | `reports/mlflow_runs.json` (four finished runs) |
| Evaluation/reproduction | reserved 2023 targets; persistence baseline | MAE 3.0594 vs 2.9016; 12 reproduction checks |
| Container | Dockerfile and CLI training/serving | [Current Docker CI](https://github.com/AaryaDeshpande/aipi510-module3-main-street/actions/runs/45284798476) |
| Serving | saved preprocessing/model; Flask JSON `/predict` | public smoke checks and matching artifact hashes |
| Frontend | public interactive county explorer | live browser prediction and experiment summary |
| Ethics | source dates, unavailable cells, representation limits, weak result | README and on-page method/limitations |

The model's weaker held-out MAE is visible; Canvas explicitly states accuracy is not assessed. This project does not establish current demand, profits or owner wealth. Predictions for 2024 use historical features ending in 2023 and are unverified estimates.

61 tests, 12 reproduction checks, four MLflow runs, cloud ingestion, Docker CI, public HTTP and new homepage browser prediction have executed successfully. A local teammate Docker run and genuine member contributions remain for the team.

Open course interpretation checks: actual providers R2/Vercel differ from the named storage/API examples, and the Canvas group/roster exception has not been established. REQUIREMENTS.md does not certify those items. AI assistance and prior learning sources remain acknowledged in README.
