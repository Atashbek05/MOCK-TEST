# IELTS Mock Test Backend (Day 1)

## Run locally

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Deploy on Render

Use `render.yaml` from repo root. It sets:
- `rootDir: backend`
- correct start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Python version `3.12.3`

## Implemented endpoints

- `GET /health`
- `POST /register`
- `POST /login`
- `GET /me` (Bearer token)
- `GET /dashboard` (Bearer token)
