# Understand the project in two minutes

Open the [live app](https://aipi510-module3-main-street.vercel.app/), choose a Wisconsin county and category, inspect reported history, and run an estimate.

The model learns from 2019/2020 counts to predict 2021, selects regularization on 2022, and evaluates on 2023. The displayed 2024 estimates are historical exercises. Test MAE is 3.0594 versus 2.9016 for simply carrying the count forward. Accuracy is excluded from the assignment's assessment.

Docker packages Python, dependencies, source, data and model into a repeatable environment. The same image can run training or start the Flask prediction server. GitHub CI actually built and ran it; Tanya's PR records her local run.

**The original provider gaps have been corrected with actual GCS training and a public Cloud Run deployment.** See [REQUIREMENTS.md](REQUIREMENTS.md) and [TEAM_ACTIONS.md](TEAM_ACTIONS.md). Both partner-authored PRs exist. Canvas receipt was observed directly; group membership still requires personal confirmation.
