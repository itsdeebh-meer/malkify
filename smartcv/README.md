# SmartCV
Local Flask resume builder with editable profile, skills, education/experience and browser print-to-PDF.
## Setup
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python app.py
```
Visit http://127.0.0.1:5000. Data is not persisted; save your PDF before closing.
Production needs authentication, storage, CSRF protection and a production WSGI server. This version does not claim to use AI.