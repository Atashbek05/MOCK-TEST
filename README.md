# IELTS Mock Test Backend (Day 1)

## Run locally

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Implemented endpoints

- `GET /health`
- `POST /register`
- `POST /login`
- `GET /me` (Bearer token)
- `GET /dashboard` (Bearer token)
