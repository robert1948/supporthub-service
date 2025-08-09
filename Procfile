release: python scripts/release_check.py
web: gunicorn -k uvicorn.workers.UvicornWorker app.main:app --log-level info --workers ${WEB_CONCURRENCY:-2} --bind 0.0.0.0:${PORT}
