# MediBook
Flask + SQLite appointment request demo with required-field validation and local request list.
## Run
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python app.py
```
Visit http://127.0.0.1:5000. Database is created automatically.
This is not a real medical service. Do not enter sensitive patient/health data. Requests remain local and no provider is notified. Production needs verified providers, authentication, access controls, encryption, privacy/legal review, audit logs and secure hosting.