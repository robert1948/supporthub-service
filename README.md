# SupportHub Service

A minimal FastAPI-based backend prepared to support 24/7 assistance via chat, email, or phone.

## Quick Start (Docker Compose)

- Dev server: http://localhost:8000
- OpenAPI Docs: http://localhost:8000/docs

```bash
docker compose up --build
```

## Heroku

- Ensure a Procfile exists (web dyno):
  `web: gunicorn -k uvicorn.workers.UvicornWorker app.main:app --log-level info --workers ${WEB_CONCURRENCY:-2} --bind 0.0.0.0:${PORT}`
- Set config vars (e.g., CORS_ORIGINS, API_KEY, SMTP_*).
- Scale dynos:
  ```bash
  heroku ps:scale web=1
  ```

## API

- POST `/v1/support/request`
  - body:
    ```json
    {
      "name": "Jane Doe",
      "email": "jane@example.com",
      "channel": "email|chat|phone",
      "subject": "Need help",
      "message": "Describe your issue",
      "phone_from": "+1555123456" // required if channel=phone
    }
    ```
  - returns: `{"status": "accepted"}`

## Configuration

Environment variables:

- SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, SMTP_FROM_EMAIL
- SUPPORT_TEAM_EMAIL
- REDIS_URL
- SUPPORT_FORWARD_NUMBER
- CORS_ORIGINS, API_KEY

When SMTP is not configured, emails are printed to console (dev friendly).

## Production

- Build image from `Dockerfile` and run behind a reverse proxy.
- Set env vars and secrets for SMTP, chat webhooks, and telephony provider.

## CI/CD Strategy

- Heroku Auto Deploy from GitHub on main (single source of deploy).
- GitHub Actions CI runs on pull requests only.
- Docker image builds happen on version tags (v*). Use Releases to publish images.

### Tagging a release

```bash
git tag v0.1.0
git push origin v0.1.0
```

This triggers the Docker workflow to build and push:
- ghcr.io/<owner>/<repo>:v0.1.0
- ghcr.io/<owner>/<repo>:latest
- ghcr.io/<owner>/<repo>:<commit-sha>
