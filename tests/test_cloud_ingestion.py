"""Isolated security/provenance contract checks; these are not live-cloud evidence."""
import json
from unittest.mock import Mock

import pytest

from business_app.data import SITES_PANEL_URL, load_panel, sha256


CSV = (
    "county_fips,industry,year,establishments,employment,annual_payroll,employment_flag,payroll_flag,county_name,state\n"
    "55025,2382,2023,25,100,5000000,G,G,Dane County,WI\n"
).encode()
DIGEST = sha256(CSV)
HEADERS = {"x-storage-provider": "cloudflare-r2", "x-object-sha256": DIGEST,
    "x-object-key": f"panel-{DIGEST}.csv", "x-object-version": "test-object-version"}


def fake_response(content=CSV, headers=None, status=200):
    response = Mock()
    response.content = content
    response.headers = dict(HEADERS if headers is None else headers)
    response.status_code = status
    return response


def test_verified_r2_endpoint_uses_scoped_auth_and_records_no_token(monkeypatch):
    token = "unit-test-only-token"
    monkeypatch.setenv("SITES_DATA_BEARER", token)
    get = Mock(return_value=fake_response())
    monkeypatch.setattr("business_app.data.requests.get", get)
    frame, evidence = load_panel(SITES_PANEL_URL, DIGEST)
    get.assert_called_once_with(SITES_PANEL_URL, timeout=45,
        headers={"OAI-Sites-Authorization": "Bearer " + token}, allow_redirects=False)
    assert len(frame) == 1
    assert evidence["cloud_ingestion_verified"] is True
    assert evidence["storage_provider"] == "cloudflare-r2"
    assert evidence["object_key"] == f"panel-{DIGEST}.csv"
    assert evidence["object_version"] == "test-object-version"
    assert evidence["source"] == SITES_PANEL_URL and evidence["sha256"] == DIGEST
    assert token not in json.dumps(evidence)
    assert "Authorization" not in json.dumps(evidence)


@pytest.mark.parametrize("uri", [
    "https://example.org/panel.csv",
    SITES_PANEL_URL.replace("aarya-main-street-20261122.ad277", "another-site.ad277"),
    SITES_PANEL_URL.replace("/training-data/panel.csv", "/different-path.csv"),
    SITES_PANEL_URL + "?unapproved=query",
    SITES_PANEL_URL.replace(".site/", ".site.evil.example/"),
    SITES_PANEL_URL.replace("https://", "https://unapproved-user@"),
])
def test_bearer_never_leaves_exact_endpoint_and_other_https_is_not_r2_evidence(monkeypatch, uri):
    monkeypatch.setenv("SITES_DATA_BEARER", "must-not-be-forwarded")
    get = Mock(return_value=fake_response())
    monkeypatch.setattr("business_app.data.requests.get", get)
    _, evidence = load_panel(uri, DIGEST)
    get.assert_called_once_with(uri, timeout=45)
    assert evidence["cloud_ingestion_verified"] is False
    assert "storage_provider" not in evidence
    assert "must-not-be-forwarded" not in json.dumps(evidence)


def test_private_endpoint_without_token_does_not_send_request(monkeypatch):
    monkeypatch.delenv("SITES_DATA_BEARER", raising=False)
    get = Mock()
    monkeypatch.setattr("business_app.data.requests.get", get)
    with pytest.raises(ValueError, match="SITES_DATA_BEARER"):
        load_panel(SITES_PANEL_URL, DIGEST)
    get.assert_not_called()


@pytest.mark.parametrize("status", [301, 302, 307, 308, 401, 403, 500])
def test_authenticated_redirect_or_error_is_rejected_without_leaking_token(monkeypatch, status):
    token = "private-unit-test-token"
    monkeypatch.setenv("SITES_DATA_BEARER", token)
    get = Mock(return_value=fake_response(status=status))
    monkeypatch.setattr("business_app.data.requests.get", get)
    with pytest.raises(ValueError) as error:
        load_panel(SITES_PANEL_URL, DIGEST)
    assert token not in str(error.value)
    assert get.call_args.kwargs["allow_redirects"] is False
    assert get.call_count == 1


@pytest.mark.parametrize("field,value", [
    ("x-storage-provider", "other-storage"),
    ("x-object-sha256", "0" * 64),
    ("x-object-key", "panel-another-hash.csv"),
    ("x-object-version", ""),
    ("x-object-version", "   "),
])
def test_false_or_missing_r2_provenance_is_rejected(monkeypatch, field, value):
    monkeypatch.setenv("SITES_DATA_BEARER", "unit-test-only")
    headers = {**HEADERS, field: value}
    monkeypatch.setattr("business_app.data.requests.get", Mock(return_value=fake_response(headers=headers)))
    with pytest.raises(ValueError):
        load_panel(SITES_PANEL_URL, DIGEST)


def test_matching_object_headers_cannot_override_modified_body(monkeypatch):
    monkeypatch.setenv("SITES_DATA_BEARER", "unit-test-only")
    response = fake_response(content=CSV.replace(b",25,100,", b",99,100,"))
    monkeypatch.setattr("business_app.data.requests.get", Mock(return_value=response))
    with pytest.raises(ValueError, match="SHA-256"):
        load_panel(SITES_PANEL_URL, DIGEST)
