# DeniAI Studio
Flask app that calls Gemini from the server; the API key is not exposed to browser JavaScript.
## Setup
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```
Copy `.env.example` to `.env`, add your key, run `python app.py`, then open http://127.0.0.1:5000.
Never commit `.env`. Quotas/model availability depend on your Google AI account. Add authentication, request limits and production hosting before public launch.