# Backend

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Environment variables:

* `OPENAI_API_KEY`
* `NASA_API_KEY`
* `JWT_SECRET`
* `REDIS_URL`
