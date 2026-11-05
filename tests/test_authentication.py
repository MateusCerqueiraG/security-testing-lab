"""OWASP A07 — Identification & Authentication Failures."""
import requests


def test_protected_route_rejects_missing_token(base_url):
    resp = requests.get(f"{base_url}/notes", timeout=15)
    assert resp.status_code == 401


def test_protected_route_rejects_invalid_token(base_url, auth):
    resp = requests.get(f"{base_url}/notes", headers=auth("token-invalido"), timeout=15)
    assert resp.status_code == 401
