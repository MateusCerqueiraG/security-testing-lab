"""OWASP A05 — Security Misconfiguration · baseline security headers."""
import requests


def test_baseline_security_headers_present(base_url):
    resp = requests.get(f"{base_url}/health", timeout=15)
    assert resp.headers.get("X-Content-Type-Options") == "nosniff"
    assert resp.headers.get("X-Frame-Options") == "DENY"
    assert "Content-Security-Policy" in resp.headers
    assert "Referrer-Policy" in resp.headers
