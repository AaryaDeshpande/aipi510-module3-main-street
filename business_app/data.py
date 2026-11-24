"""Validated snapshot ingestion, adapted from the local Iris project."""
from __future__ import annotations
import hashlib
import io
import os
from pathlib import Path
from urllib.parse import urlsplit
import numpy as np
import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
FEATURES = ["industry", "establishments", "previous_establishments"]
SITES_PANEL_URL = "https://aarya-main-street-20261122.ad277.chatgpt.site/training-data/panel.csv"

def sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()

def load_panel(uri: str, expected_hash: str, root: Path = ROOT):
    parts = urlsplit(uri)
    storage_evidence = {}
    cloud_verified = parts.scheme == "gs"
    if parts.scheme == "gs":
        from google.cloud import storage
        blob = storage.Client().bucket(parts.netloc).blob(parts.path.lstrip("/"))
        blob.reload()
        if blob.size is None or blob.size > 30_000_000:
            raise ValueError("Dataset is unavailable or exceeds 30 MB")
        if blob.generation is None:
            raise ValueError("GCS object generation is unavailable")
        content = blob.download_as_bytes(if_generation_match=blob.generation)
        storage_evidence = {"storage_provider": "google-cloud-storage",
            "bucket": parts.netloc, "object_key": parts.path.lstrip("/"),
            "object_generation": str(blob.generation),
            "crc32c": blob.crc32c, "md5_hash": blob.md5_hash}
    elif parts.scheme == "https":
        if uri == SITES_PANEL_URL:
            bearer = os.environ.get("SITES_DATA_BEARER")
            if not bearer:
                raise ValueError("Set SITES_DATA_BEARER for the approved private dataset endpoint")
            # Exact endpoint only. Redirects could otherwise forward this private
            # header to another origin. The token is never added to run evidence.
            response = requests.get(uri, timeout=45,
                headers={"OAI-Sites-Authorization": f"Bearer {bearer}"}, allow_redirects=False)
            if response.status_code != 200:
                raise ValueError(f"Approved dataset endpoint returned HTTP {response.status_code}; redirects are not followed")
        else:
            response = requests.get(uri, timeout=45)
            response.raise_for_status()
        content = response.content
        if uri == SITES_PANEL_URL:
            headers = {key.lower(): value for key, value in response.headers.items()}
            if headers.get("x-storage-provider") != "cloudflare-r2":
                raise ValueError("Approved dataset endpoint did not identify Cloudflare R2 storage")
            if headers.get("x-object-sha256") != expected_hash:
                raise ValueError("R2 object SHA-256 header differs from the pinned snapshot")
            if headers.get("x-object-key") != f"panel-{expected_hash}.csv":
                raise ValueError("R2 object key differs from the expected content-addressed key")
            version = headers.get("x-object-version", "").strip()
            if not version:
                raise ValueError("R2 object version is missing")
            storage_evidence = {"storage_provider": "cloudflare-r2",
                "object_key": headers["x-object-key"], "object_version": version}
            cloud_verified = True
    elif not parts.scheme:
        path = Path(uri)
        content = (path if path.is_absolute() else root / path).read_bytes()
    else:
        raise ValueError("Use a local snapshot, HTTPS, or gs:// object")
    if len(content) > 30_000_000 or sha256(content) != expected_hash:
        raise ValueError("Dataset size or SHA-256 differs from the frozen snapshot")
    frame = pd.read_csv(io.BytesIO(content), dtype={"county_fips": str, "industry": str, "state": str})
    needed = {"county_fips", "industry", "year", "establishments", "employment", "annual_payroll", "county_name", "employment_flag", "payroll_flag"}
    if not needed.issubset(frame.columns):
        raise ValueError("Dataset columns do not match the documented panel schema")
    if frame.duplicated(["county_fips", "industry", "year"]).any():
        raise ValueError("Duplicate county-industry-year observations")
    if frame[["county_fips", "industry", "year", "establishments"]].isna().any().any():
        raise ValueError("Identifiers, dates, and establishment counts cannot be missing")
    if not frame.county_fips.str.fullmatch(r"\d{5}").all() or frame.county_fips.str.endswith("999").any():
        raise ValueError("Invalid or unclassified county identifier")
    if not frame.industry.str.fullmatch(r"\d{4}").all():
        raise ValueError("Use exact four-digit industries")
    counts = frame.establishments.to_numpy(dtype=float)
    if not np.isfinite(counts).all() or (counts < 3).any() or not np.equal(counts, np.floor(counts)).all():
        raise ValueError("Reported establishment counts must be finite integers >= 3")
    for field in ["employment", "annual_payroll"]:
        known = frame[field].dropna().to_numpy(dtype=float)
        if not np.isfinite(known).all() or (known < 0).any():
            raise ValueError("Known employment/payroll values must be finite and nonnegative")
    return frame, {"source": uri, "transport": parts.scheme or "local", "rows": len(frame),
        "sha256": sha256(content), "cloud_ingestion_verified": cloud_verified, **storage_evidence}

def supervised(panel: pd.DataFrame) -> pd.DataFrame:
    """Join consecutive reported years; absent or hidden cells stay absent."""
    keys = ["county_fips", "industry", "year"]
    previous = panel[keys + ["establishments"]].rename(columns={"establishments": "previous_establishments"})
    previous["year"] += 1
    future = panel[keys + ["establishments"]].rename(columns={"establishments": "actual_next"})
    future["year"] -= 1
    rows = panel.merge(previous, on=keys, validate="one_to_one").merge(future, on=keys, validate="one_to_one")
    rows["target_year"] = rows["year"] + 1
    rows["row_id"] = rows.county_fips + ":" + rows.industry + ":" + rows.year.astype(str)
    return rows.sort_values(["year", "county_fips", "industry"]).reset_index(drop=True)
