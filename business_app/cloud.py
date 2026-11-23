"""Explicit, creation-only upload to an existing approved Google Cloud bucket."""
import json
from pathlib import Path
from google.cloud import storage
from .data import ROOT, sha256
from .train import write_json

def upload_data(bucket_name: str, object_name: str):
    content = (ROOT / "data" / "panel.csv").read_bytes()
    blob = storage.Client().bucket(bucket_name).blob(object_name)
    blob.upload_from_string(content, content_type="text/csv", if_generation_match=0)
    downloaded = blob.download_as_bytes()
    if sha256(downloaded) != sha256(content):
        raise ValueError("Uploaded object checksum verification failed")
    blob.reload()
    result = {"uri": f"gs://{bucket_name}/{object_name}", "sha256": sha256(content), "bytes": len(content), "generation": str(blob.generation), "verified": True}
    write_json(ROOT / "reports" / "cloud_upload.json", result)
    return result
