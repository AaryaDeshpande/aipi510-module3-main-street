# Submission audit — November 24, 2026

This audit used the actual fetched repository, GitHub PR/permission and CI APIs/logs, the live browser and HTTP service, and the signed-in Canvas assignment. It did not rely on the prior ChatGPT handoff as proof.

## Findings at the start of the audit

- Default branch was `360dfa0811aa261dfee11e1126db8fc43515ffc5`. It already contained the full implementation, despite README claiming main only had initialization and PR #1 was a draft.
- Aarya PR #1 was merged into main. Tanya PR #2 was authored by `Tanya-duke` and merged into `aarya/module3-implementation`, not main. Tanya had write access. This integration preserves her commits and original local Docker report.
- Main-branch Actions run 45292395651 genuinely passed 61 tests, image build, container training, evaluation/prediction reproduction, and real HTTP/curl checks. The auditor read actual logs, including the 61-test result and all successful comparison checks.
- Public Vercel HTTP checks and a browser prediction worked. Dane County/building-equipment contractors returned 281.2185, displayed as 281.2, against a no-change baseline of 276.
- Data storage was R2 and API hosting was Vercel. Both lay outside the assignment's named provider choices. No instructor exception was established.
- Canvas already showed a submitted attempt with the repository and frontend URLs. The auditor made no Canvas changes. Current displayed deadline was November 24, 11:30am Eastern (10:30am Central). Group membership was not established.

## Work executed during this audit

- Preserved both partners' genuine Git commits and corrected stale current-status documents; retained earlier dated evidence with its original scope and restored prior-source citations.
- Installed the pinned Python environment in an isolated local venv; 61 tests initially passed, then 62 passed after adding the GCS generation/checksum test. `pip check` found no broken requirements.
- Verified the existing Google Cloud project owner and enabled billing. No new billing account was created or linked. Used normal browser sign-in without copying credentials into source or chat.
- Created a private GCS bucket with uniform access and public-access prevention; uploaded and downloaded the cleaned 5,799,225-byte public Census panel, verifying its SHA-256.
- Actually trained from the `gs://` object, logging four new MLflow runs and model/evaluation artifacts. Recorded bucket/object/generation and GCS checksums. All 12 cloud-source reproduction checks passed.
- Built the repository Dockerfile through Cloud Build. The public Cloud Run service passed real HTTP checks. Cloud Run and Vercel routing results are recorded separately in `google_cloud_deployment.json` and public HTTP evidence; verify those outcomes rather than treating prepared code as deployment proof.

## Requirement assessment

See the current table in [REQUIREMENTS.md](../REQUIREMENTS.md). Dataset/task/metric, cleaning, configured chronological pipeline, actual MLflow logging, pinned dependencies, Docker entry points/execution, Flask JSON inference, public interactive frontend, sources, limitations, and one submitted PR per partner have evidence.

The named-provider requirements now have actual execution evidence: GCS ingestion and public Cloud Run inference both succeeded. The deployment record captures the successful Cloud Build image digest and Cloud Run revision. The retained Vercel URL uses the Cloud Run API through explicit rewrite rules; post-deployment evidence is recorded separately.

## Useful scope and limitations

The app helps inspect historical business-location counts, compare Wisconsin counties/categories, and organize interview hypotheses and a research shortlist. It does not accept a ZIP code or cover every location. The model uses industry and two establishment counts; it does not learn a direct measure of county demand, business profitability, purchase price, financing, owner wealth, customer spending or willingness to buy.

The held-out model MAE is 3.0594 versus 2.9016 for persistence, approximately 5.4% worse. This is disclosed; the assignment explicitly excludes accuracy from assessment. A successful ML pipeline is demonstrated, but forecasting improvement and profitable opportunities are not demonstrated. Fewer establishments need not imply unmet demand, and growth can mean more competition. 2024 displayed estimates are historical exercises using 2023 inputs.

The current Census release-status page was checked directly and still identifies 2023 as the latest CBP reference year: <https://www.census.gov/programs-surveys/cbp/data.html>. The dated snapshot is not simply an omitted newer CBP release.

## Remaining personal checks

- Tanya should confirm the pandas-version entry in her original Docker report: it lists 2.3.5 while Docker requirements pin 2.2.3. The auditor preserved the report unchanged and did not invent a correction or claim to witness her original run.
- Both partners should personally review and understand the work. GitHub authorship and automated checks do not establish human understanding.
- Confirm Canvas group membership if group grading applies. The submitted attempt and both URLs were directly visible; no resubmission is necessary merely to retain those same URLs.
- A useful current local-opportunity product would need a separate research and validation phase. No such economic validation is claimed here.

The audit, migration and documentation changes were prepared with Codex assistance. Tanya's work remains attributed to Tanya; no new human execution or review is fabricated.
