# Training-data storage reference

`r2-worker.mjs` preserves the exact bounded upload and stored-object read handlers used by the owner-private review Site. The host provisions a real Cloudflare R2 bucket and supplies the logical `BUCKET` binding. Its platform service-access boundary protects the routes. It checks the pinned cleaned CSV SHA-256, creates an immutable content-addressed object, and streams the stored object on reads.

Observed upload, object version, byte count, checksum, and download evidence are in `reports/cloud_storage.json`; the model training reader records the actual cloud source in `artifacts/ingestion.json`. This reference excludes the separate review UI. It is not a standalone authentication system or a public upload service.

Training uses the private endpoint documented in `business_app/data.py`. Obtain service access through the supported owner account workflow and set `SITES_DATA_BEARER` only in the process environment. Never commit or paste a token into the repository. Other reviewers can reproduce the exact frozen data locally with `--data-uri data/panel.csv`.
