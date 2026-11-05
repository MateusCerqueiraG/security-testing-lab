"""OWASP A01 — Broken Access Control · IDOR (Insecure Direct Object Reference).

Bob tries to read Alice's note by guessing/altering the id in the URL.
"""
import requests


def test_user_cannot_read_another_users_note_by_id(base_url, auth, alice_note):
    resp = requests.get(
        f"{base_url}/notes/{alice_note['id']}",
        headers=auth("bob-token"),
        timeout=15,
    )
    assert resp.status_code == 403, "IDOR: Bob conseguiu ler a nota da Alice pelo id!"


def test_owner_can_read_own_note(base_url, auth, alice_note):
    resp = requests.get(
        f"{base_url}/notes/{alice_note['id']}",
        headers=auth("alice-token"),
        timeout=15,
    )
    assert resp.status_code == 200
    assert resp.json()["owner"] == "alice"
