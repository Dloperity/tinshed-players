# Tinshed Players — Crew Rostering System

A show scheduling and volunteer crew rostering web application for The Tinshed Players, a community theatre company. Built for ISYS3001 Managing Software Development (A2/A3).

## Stack

- Python 3.12 + Flask 3 + Flask-SQLAlchemy + SQLite
- Bootstrap 5 (CDN), Jinja2 templates
- pytest for automated tests
- GitHub Actions for CI, Render for optional deployment

## Run from a clean checkout

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows (PowerShell)
source .venv/bin/activate       # macOS / Linux
pip install -r requirements.txt
python run.py
Open http://127.0.0.1:5000

The SQLite database (tinshed.db) is created automatically on first start.

Run the tests
bash
pytest -v
Project structure
text
app/
  __init__.py        # create_app() factory, blueprint registration
  models.py          # shared data model (single source of truth)
  volunteers/        # volunteer management module
  productions/       # productions, performances, crew calls
  assignments/       # roster assignments + one-role-per-performance rule
  templates/         # Jinja2 templates
tests/               # pytest suite
Features
Volunteer directory with add, edit, deactivate, search, and status filter.

Productions and performances with crew calls.

Assignments enforcing the one-role-per-performance rule.

Configuration
Copy .env.example to .env for local overrides (illustrative values only).

Variable	Default	Purpose
SECRET_KEY	dev	Flask session signing
DATABASE_URL	sqlite:///tinshed.db	SQLAlchemy database URI
CI / deployment
CI: .github/workflows/ci.yml runs pytest on every push / pull request.

Deploy: render.yaml deploys the app on Render's free tier (gunicorn run:app).

A2