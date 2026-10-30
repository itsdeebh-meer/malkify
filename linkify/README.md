# Linkify
Flask + SQLite URL shortener with random codes, redirects and click counts.
## Run
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python app.py
```
Visit http://127.0.0.1:5000. Database is created automatically. Use HTTPS, abuse detection, rate limits and a production WSGI server before public deployment.