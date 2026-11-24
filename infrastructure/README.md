# Infrastructure

The active deployment uses Google Cloud Storage for the training dataset, Cloud Build for container builds, Cloud Run for inference and Vercel for the frontend.

- [Google Cloud setup](GOOGLE_CLOUD.md)
- [Deployment overview](../DEPLOYMENT.md)
- [Deployment script](../scripts/deploy_google_cloud.sh)
- [Frontend routing](../vercel.json)

`r2-worker.mjs` is an earlier storage adapter retained for compatibility. The current pipeline uses the GCS source in `config.yaml`.
