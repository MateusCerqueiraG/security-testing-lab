import pytest
import requests

BASE_URL = "http://127.0.0.1:8000"


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture
def auth():
    """Builds an Authorization header for a given token."""
    return lambda token: {"Authorization": f"Bearer {token}"}


@pytest.fixture
def alice_note(base_url, auth):
    """A note that belongs to Alice — used as the victim resource in attacks."""
    resp = requests.post(
        f"{base_url}/notes",
        json={"text": "segredo da Alice"},
        headers=auth("alice-token"),
        timeout=15,
    )
    assert resp.status_code == 201
    return resp.json()
