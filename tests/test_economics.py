"""Independently verify the economics context and its financial definitions."""
import hashlib
import json
import openpyxl
import pytest
from business_app.data import ROOT

def test_financial_snapshot_matches_original_workbook():
    data = json.loads((ROOT / "data/economics.json").read_text())
    workbook = ROOT / "data/economics_source.xlsx"
    assert hashlib.sha256(workbook.read_bytes()).hexdigest() == data["source"]["sha256"]
    original = openpyxl.load_workbook(workbook, read_only=True, data_only=True)
    raw = {str(row[0]): row for row in original.active.values if str(row[2]) == "55000"}
    assert data["year"] == 2023 and len(data["records"]) == 32
    missing_profit = 0
    for record in data["records"]:
        row = raw[str(record["industry"])]
        assert record["filings"] == (row[4] if isinstance(row[4], (int, float)) else None)
        assert record["receipts"] == (row[5] if isinstance(row[5], (int, float)) else None)
        if isinstance(row[11], (int, float)):
            assert record["net_profit"] == row[11]
            assert record["profit_per_filing"] == pytest.approx(row[11] / row[4])
            assert record["margin_pct"] == pytest.approx(100 * row[11] / row[5])
        else:
            missing_profit += 1
            assert record["net_profit"] is None and record["profit_per_filing"] is None and record["margin_pct"] is None
    assert missing_profit == 1

def test_financial_ratio_is_context_with_explicit_owner_labor_limits():
    data = json.loads((ROOT / "data/economics.json").read_text())
    text = " ".join(data["limitations"]).lower()
    assert "owner labor" in text and "median" in text and "tax-filing address" in text
    assert data["source"]["units"].startswith("Dollars, not thousands")
