"""Secure Notes API — the target under test.

Implements the access-control defenses that the security suite probes:
ownership checks (anti-IDOR/BOLA), role checks (anti privilege-escalation),
authentication on every protected route, and baseline security headers.
Self-contained on purpose — security testing runs against our own instance.
"""
from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Secure Notes API")

# Pre-seeded tokens (demo only): two regular users and one admin.
TOKENS = {
    "alice-token": {"user": "alice", "role": "user"},
    "bob-token": {"user": "bob", "role": "user"},
    "admin-token": {"user": "admin", "role": "admin"},
}

NOTES: dict[int, dict] = {}
_seq = {"n": 0}


class NoteIn(BaseModel):
    text: str


def current_user(authorization: str = Header(default="")):
    token = authorization.removeprefix("Bearer ").strip()
    user = TOKENS.get(token)
    if not user:
        raise HTTPException(status_code=401, detail="autenticação necessária")
    return user


@app.middleware("http")
async def security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Content-Security-Policy"] = "default-src 'none'"
    return response


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/notes", status_code=201)
def create_note(note: NoteIn, user=Depends(current_user)):
    _seq["n"] += 1
    note_id = _seq["n"]
    NOTES[note_id] = {"id": note_id, "owner": user["user"], "text": note.text}
    return NOTES[note_id]


@app.get("/notes")
def list_notes(user=Depends(current_user)):
    # Returns ONLY the caller's own notes (prevents BOLA / mass exposure).
    return [n for n in NOTES.values() if n["owner"] == user["user"]]


@app.get("/notes/{note_id}")
def get_note(note_id: int, user=Depends(current_user)):
    note = NOTES.get(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="não encontrado")
    if note["owner"] != user["user"]:
        # Ownership check — prevents IDOR (reading someone else's note by id).
        raise HTTPException(status_code=403, detail="acesso negado")
    return note


@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int, user=Depends(current_user)):
    note = NOTES.get(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="não encontrado")
    if note["owner"] != user["user"]:
        raise HTTPException(status_code=403, detail="acesso negado")
    del NOTES[note_id]


@app.get("/admin/users")
def admin_users(user=Depends(current_user)):
    # Role check — prevents vertical privilege escalation.
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="acesso restrito a administradores")
    return sorted({v["user"] for v in TOKENS.values()})
