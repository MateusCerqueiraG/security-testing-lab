"""OWASP A01 — Broken Object Level Authorization (BOLA).

A user must never see or modify resources that belong to another user.
"""
import requests


def test_listing_returns_only_own_resources(base_url, auth, alice_note):
    resp = requests.get(f"{base_url}/notes", headers=auth("bob-token"), timeout=15)
    assert resp.status_code == 200
    ids = [note["id"] for note in resp.json()]
    assert alice_note["id"] not in ids, "BOLA: a listagem de Bob expõe recurso da Alice!"


def test_user_cannot_delete_another_users_note(base_url, auth, alice_note):
    resp = requests.delete(
        f"{base_url}/notes/{alice_note['id']}",
        headers=auth("bob-token"),
        timeout=15,
    )
    assert resp.status_code == 403, "BOLA: Bob conseguiu apagar a nota da Alice!"
