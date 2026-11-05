"""OWASP A01 — Broken Access Control · Vertical privilege escalation."""
import requests


def test_regular_user_cannot_reach_admin(base_url, auth):
    resp = requests.get(f"{base_url}/admin/users", headers=auth("alice-token"), timeout=15)
    assert resp.status_code == 403, "Escalonamento: usuário comum acessou área de admin!"


def test_admin_can_reach_admin(base_url, auth):
    resp = requests.get(f"{base_url}/admin/users", headers=auth("admin-token"), timeout=15)
    assert resp.status_code == 200
