"""Freeze selected official CBP county data, keeping unpublished cells unknown.

Only this deliberate preparation command uses the network. Training and serving
use the frozen panel. Cached archives are excluded from the review package.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
YEARS = tuple(range(2019, 2024))
INDUSTRIES = {
    "2382": "Building equipment contractors",
    "2383": "Building finishing contractors",
    "5412": "Accounting, tax preparation, bookkeeping, and payroll services",
    "5413": "Architectural, engineering, and related services",
    "5415": "Computer systems design and related services",
    "5617": "Services to buildings and dwellings",
    "6212": "Offices of dentists",
    "6213": "Offices of other health practitioners",
    "8111": "Automotive repair and maintenance",
    "8121": "Personal care services",
}
FIELDS = ["county_fips", "industry", "year", "establishments", "employment",
          "annual_payroll", "employment_flag", "payroll_flag", "county_name", "state"]
GAZETTEER = "https://www2.census.gov/geo/docs/maps-data/data/gazetteer/2023_Gazetteer/2023_Gaz_counties_national.zip"
GEOMETRY = ("https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/State_County/MapServer/1/query"
            "?where=STATE%3D%2755%27&outFields=GEOID%2CNAME%2CSTATE%2CCOUNTY&outSR=4326"
            "&geometryPrecision=4&maxAllowableOffset=0.005&f=geojson")


def digest(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def fetch(url: str, cached: Path, expected_sha: str | None = None) -> bytes:
    """Use an existing source snapshot or download once, with a 30 MB ceiling."""
    if cached.exists():
        content = cached.read_bytes()
    else:
        request = Request(url, headers={"User-Agent": "AIPI510-educational-data-project/1.0"})
        with urlopen(request, timeout=60) as response:
            content = response.read(30_000_001)
        if len(content) > 30_000_000:
            raise ValueError("Source archive exceeds preparation size limit")
        cached.parent.mkdir(parents=True, exist_ok=True)
        cached.write_bytes(content)
    if expected_sha and digest(content) != expected_sha:
        raise ValueError(f"Source snapshot SHA-256 changed: {url}")
    return content


def magnitude(value: str, flag: str, multiplier: int = 1) -> int | None:
    """G/H/J preserve published noisy values; withheld/unknown values stay null."""
    if flag not in {"G", "H", "J"}:
        return None
    try:
        number = int(value)
    except (ValueError, TypeError):
        return None
    return number * multiplier if number >= 0 else None


def prepare(root: Path = ROOT) -> dict:
    root = Path(root)
    data = root / "data"
    data.mkdir(parents=True, exist_ok=True)
    cache = data / "raw"
    cache.mkdir(exist_ok=True)
    existing = json.loads((data / "SOURCE.json").read_text()) if (data / "SOURCE.json").exists() else {}
    prior_hashes = {str(source["year"]): source["sha256"] for source in existing.get("sources", []) if "year" in source}
    gazetteer = fetch(GAZETTEER, cache / "gazetteer2023.zip", existing.get("gazetteer", {}).get("sha256"))
    names = {}
    state_names = {}
    with ZipFile(io.BytesIO(gazetteer)) as archive:
        with archive.open(archive.namelist()[0]) as source:
            for row in csv.DictReader(io.TextIOWrapper(source, encoding="utf-8-sig"), delimiter="\t"):
                record = {key.strip(): value.strip() for key, value in row.items()}
                names[record["GEOID"]] = record["NAME"]
                state_names[record["GEOID"][:2]] = record["USPS"]
    rows = []
    sources = []
    missing_names = Counter()
    seen = set()
    for year in YEARS:
        url = f"https://www2.census.gov/programs-surveys/cbp/datasets/{year}/cbp{year % 100:02d}co.zip"
        content = fetch(url, cache / f"cbp{year}co.zip", prior_hashes.get(str(year)))
        counts = Counter()
        flag_counts = Counter()
        with ZipFile(io.BytesIO(content)) as archive:
            member = archive.namelist()[0]
            with archive.open(member) as source:
                for raw in csv.DictReader(io.TextIOWrapper(source, encoding="utf-8-sig")):
                    counts["raw_rows"] += 1
                    industry = raw["naics"].rstrip("/-")
                    if industry not in INDUSTRIES:
                        counts["outside_selected_industries"] += 1
                        continue
                    if raw["fipscty"] in {"000", "999"}:
                        counts["statewide_or_unknown_county"] += 1
                        continue
                    county = raw["fipstate"] + raw["fipscty"]
                    if len(county) != 5 or not county.isdigit() or raw["fipstate"] not in state_names:
                        counts["invalid_county_or_state"] += 1
                        continue
                    try:
                        establishments = int(raw["est"])
                    except ValueError:
                        counts["invalid_establishment_count"] += 1
                        continue
                    if establishments < 3:
                        raise ValueError("Unexpected published cell below disclosure threshold; review source")
                    key = (county, industry, year)
                    if key in seen:
                        raise ValueError(f"Duplicate county/industry/year: {key}")
                    seen.add(key)
                    name = names.get(county, f"County FIPS {county}")
                    if county not in names:
                        missing_names[county] += 1
                    employment = magnitude(raw["emp"], raw["emp_nf"])
                    payroll = magnitude(raw["ap"], raw["ap_nf"], 1000)
                    counts["unpublished_employment"] += employment is None
                    counts["unpublished_payroll"] += payroll is None
                    flag_counts["employment_" + raw["emp_nf"]] += 1
                    flag_counts["payroll_" + raw["ap_nf"]] += 1
                    rows.append(dict(zip(FIELDS, [county, industry, year, establishments,
                        employment, payroll, raw["emp_nf"], raw["ap_nf"], name,
                        state_names[raw["fipstate"]]])))
                    counts["retained_rows"] += 1
                    if raw["fipstate"] == "55":
                        counts["wisconsin_rows"] += 1
        sources.append({"year": year, "url": url, "archive_member": member,
                        "bytes": len(content), "sha256": digest(content),
                        "counts": dict(counts), "flags": dict(flag_counts)})
    rows.sort(key=lambda row: (row["year"], row["county_fips"], row["industry"]))
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    content = buffer.getvalue().encode("utf-8")
    (data / "panel.csv").write_bytes(content)
    geometry_content = fetch(GEOMETRY, cache / "wi_counties.geojson", existing.get("geometry", {}).get("raw_sha256"))
    geometry = json.loads(geometry_content)
    if len(geometry.get("features", [])) != 72:
        raise ValueError("Expected 72 Wisconsin county geometries")
    identifiers = {feature["properties"]["GEOID"] for feature in geometry["features"]}
    if len(identifiers) != 72 or not all(code.startswith("55") for code in identifiers):
        raise ValueError("Invalid or repeated Wisconsin geometry IDs")
    for feature in geometry["features"]:
        feature["id"] = feature["properties"]["GEOID"]
    (data / "wi_counties.geojson").write_text(json.dumps(geometry, separators=(",", ":")) + "\n")
    (data / "industries.json").write_text(json.dumps(INDUSTRIES, indent=2) + "\n")
    manifest = {
        "prepared_utc": datetime.now(timezone.utc).isoformat(),
        "dataset": "U.S. Census County Business Patterns selected county/2017-NAICS industries",
        "years": list(YEARS), "industries": INDUSTRIES, "rows": len(rows),
        "sha256": digest(content), "bytes": len(content), "columns": FIELDS,
        "sources": sources, "gazetteer": {"url": GAZETTEER, "sha256": digest(gazetteer)},
        "geometry": {"url": GEOMETRY, "raw_sha256": digest(geometry_content),
                     "sha256": digest((data / "wi_counties.geojson").read_bytes()),
                     "counties": 72, "purpose": "Simplified display geometry only; no model input",
                     "note": "TIGERweb current boundaries captured at preparation; Wisconsin has same county identities as business panel"},
        "missing_county_names": dict(missing_names),
        "cleaning": [
            "Keep exactly the ten 4-digit industry aggregate rows; never sum overlapping child industries",
            "Preserve 5-character county FIPS and industry codes as strings",
            "Exclude county 000/999 statewide and unknown-county rows",
            "Reject duplicates, malformed identifiers, and invalid published establishment counts",
            "Retain missing county-industry-year cells as unknown; never fill zero. Cells below three establishments are unpublished",
            "Convert annual payroll from source thousands of dollars to dollars; retain employment/payroll noise flags",
            "Treat withheld or unknown magnitude values as null; do not infer them by subtracting broader totals",
        ],
        "limitations": [
            "Counts represent employer establishment locations, not distinct firms, owners, revenue, profit, or unmet demand",
            "Self-employed and other nonemployer businesses are outside CBP coverage",
            "2019–2023 use the same 2017 NAICS classification, but geography and disclosure changes can affect comparison",
            "Older county IDs absent from the 2023 Gazetteer keep an explicit FIPS label; model joins require matching year-specific IDs",
            "COVID-period dynamics and disclosure-related missingness limit forecast generalization",
            "Payroll and employment values are noisy published estimates; payroll is not business revenue",
        ],
        "references": [
            "https://www.census.gov/programs-surveys/cbp/technical-documentation/methodology.html",
            "https://www.census.gov/programs-surveys/cbp/about/glossary.html",
            "https://www.census.gov/newsroom/press-releases/2025/2023-county-business-patterns.html",
            "https://www.census.gov/data/datasets/2017/econ/cbp/2017-cbp.html",
            "https://www.census.gov/geographies/reference-files/time-series/geo/gazetteer-files.2023.html",
        ],
    }
    (data / "SOURCE.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


if __name__ == "__main__":
    result = prepare()
    print(json.dumps({key: result[key] for key in ["rows", "sha256", "years", "missing_county_names"]}, indent=2))
