import importlib.util
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load_app(folder, name):
    path = ROOT / folder / "app.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def test_smartcv_form_and_preview():
    module = load_app("smartcv", "smartcv_test")
    client = module.app.test_client()
    assert client.get("/").status_code == 200
    response = client.post("/", data={"name":"Test User","headline":"Developer","email":"test@example.com","summary":"Summary","skills":"Python","experience":"BSCS"})
    assert response.status_code == 200
    assert b"Test User" in response.data

def test_linkify_shortens_and_redirects(tmp_path):
    module = load_app("linkify", "linkify_test")
    module.DB = str(tmp_path / "links.sqlite")
    with __import__("sqlite3").connect(module.DB) as db:
        db.execute("CREATE TABLE links(code TEXT PRIMARY KEY,url TEXT NOT NULL,clicks INTEGER DEFAULT 0)")
    client = module.app.test_client()
    response = client.post("/", data={"url":"https://example.com/docs"})
    assert response.status_code == 200
    import re
    match = re.search(rb"href='/([A-Za-z0-9]{7})'", response.data)
    assert match, response.data
    code = match.group(1).decode()
    redirected = client.get("/" + code)
    assert redirected.status_code == 302
    assert redirected.headers["Location"] == "https://example.com/docs"

def test_medibook_saves_demo_request(tmp_path):
    module = load_app("medibook", "medibook_test")
    module.DB = str(tmp_path / "appointments.sqlite")
    with __import__("sqlite3").connect(module.DB) as db:
        db.execute("CREATE TABLE appointments(id INTEGER PRIMARY KEY,patient TEXT,email TEXT,provider TEXT,day TEXT,note TEXT)")
    client = module.app.test_client()
    response = client.post("/", data={"patient":"Test Patient","email":"test@example.com","provider":"General Consultation","day":"2030-01-01","note":"Routine visit"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Saved locally" in response.data
    assert b"Test Patient" in response.data

def test_deniai_requires_api_key_gracefully(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    module = load_app("deniai-studio", "deniai_test")
    client = module.app.test_client()
    assert client.get("/").status_code == 200
    response = client.post("/api/generate", json={"prompt":"Hello"})
    assert response.status_code == 503
    assert response.get_json()["error"]
