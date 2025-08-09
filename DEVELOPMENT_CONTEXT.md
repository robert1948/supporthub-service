# Development Context — SupportHub Service

Updated: 2025-08-09

## Links
- Repo: https://github.com/robert1948/supporthub-service
- Local API: http://localhost:8000
- OpenAPI Docs: http://localhost:8000/docs
- Reference App (provided): https://cc-support-a3485ff0fa5f.herokuapp.com/
- Reference Chat (context): https://chatgpt.com/c/68849685-cc94-832b-8867-fc5da0d6cfca

## Current Status
- FastAPI service scaffolded with 24/7 support intent (chat, email, phone).
- Endpoints:
  - Health: GET / and GET /health (reports app version and DB status)
  - Support intake: POST /v1/support/request (channel=email|chat|phone)
  - Tickets: GET/POST /v1/tickets, GET/PATCH /v1/tickets/{id}
  - Messages: GET/POST /v1/messages, GET /v1/messages/{id}
- Notifications service:
  - Email via SMTP (prints to console in dev when SMTP is not configured)
  - Chat via Slack Incoming Webhook when SLACK_WEBHOOK_URL is set; dev-logs otherwise
  - Phone placeholders (integration points for Twilio)
- Config and Security:
  - CORS middleware (configurable origins, headers, methods)
  - Optional API key guard (header: X-API-Key) via env var API_KEY
  - App metadata (APP_NAME, APP_VERSION) via settings
  - DATABASE_URL normalization (postgres -> postgresql for SQLAlchemy)
  - .env.example added; real .env files are ignored by Git
- Containerization:
  - Dockerfile with curl for healthcheck
  - docker-compose with env wiring (SMTP, CORS, API key, Redis, Postgres)
- Database & Migrations:
  - SQLAlchemy 2.x Base/engine/session configured
  - ORM models: Ticket, Message
  - Alembic scaffolding with initial migration
  - /health checks DB connectivity
- CI/CD & Deployment:
  - GitHub Actions: PR CI (ruff lint, smoke test, pytest)
  - Docker image build/push to GHCR on tags only (concurrency guarded)
  - Heroku Procfile (gunicorn with uvicorn workers)
  - Release phase runs Alembic migrations (upgrade head) then health check
  - Heroku web dyno scaled and app serving 200 on GET /

## How to Run (Dev)
1) Copy envs and edit as needed:
   cp .env.example .env
2) Start services (API + Postgres + Redis):
   docker compose up --build
3) Apply DB migrations (first run and after model changes):
   - Inside compose: docker compose run --rm web alembic upgrade head
   - Or locally: DATABASE_URL=postgresql://... alembic upgrade head
4) Visit docs: http://localhost:8000/docs

## Configuration (key envs)
- APP_NAME / APP_VERSION: app metadata
- DATABASE_URL: e.g. postgresql://user:pass@db:5432/app ("postgres://" will be normalized)
- CORS_ORIGINS: comma-separated origins (use explicit domains in prod)
- API_KEY: optional; when set, require header X-API-Key on requests
- SMTP_*: SMTP_HOST/PORT/USER/PASSWORD/FROM
- SUPPORT_TEAM_EMAIL: default support email
- REDIS_URL: redis://redis:6379/0 (placeholder for bg tasks later)
- SLACK_*: SLACK_WEBHOOK_URL, SLACK_CHANNEL, SLACK_USERNAME, SLACK_ICON_EMOJI
- SUPPORT_FORWARD_NUMBER: for phone integrations

## Recently Completed
- Fixed dependencies for EmailStr (email-validator) and httpx for tests
- Normalized DATABASE_URL for SQLAlchemy
- Added SQLAlchemy Base/session and models (Ticket, Message)
- Added Alembic and initial migration; health endpoint reports DB status
- Heroku release phase runs migrations before health check; app healthy
- CI on PRs; Docker images published on tags to GHCR
- Replaced in-memory Tickets/Messages with DB-backed CRUD, schemas, pagination/filtering
- Fixed Alembic env import path; added created_at migration; migrations applied
- Added integration tests for CRUD; passing via docker compose
- CI updated to include mypy type checking and coverage gating (80% threshold)
- Added GitHub Actions integration-tests workflow (Postgres/Redis services; Alembic migrate; live API tests)
- Slack Incoming Webhook support added to notifications with retry/backoff

## Next Steps (Roadmap)
- CI/CD:
  - Versioning and release process (tag v0.1.0 after DB CRUD lands)
- Email:
  - Add retries/timeouts for SMTP; structured error handling
  - Optional: pluggable provider with SendGrid integration (env toggle)
- Chat:
  - Document Slack setup in README and add minimal unit test for payload shape
- Phone:
  - Add Twilio webhooks for inbound calls and status callbacks
  - Implement call forwarding to SUPPORT_FORWARD_NUMBER and persist call logs
- Jobs:
  - Introduce background queue (RQ or Celery) with Redis for notifications
  - Add retries and DLQ pattern for failed jobs
- Security:
  - Rate limiting (fastapi-limiter with Redis)
  - Structured logging + request ID middleware; security headers hardening
- Observability:
  - Prometheus metrics (prometheus-fastapi-instrumentator)
  - Tracing (OpenTelemetry) and Sentry error tracking (SENTRY_DSN)
- Ops:
  - On-call escalation integration (PagerDuty/Opsgenie) and runbooks

## Phased Rollout Plan
- Phase 0: Stabilize v0.1.x
  - Goals: Keep CI green (ruff, mypy, coverage>=80), integration-tests workflow stable, Heroku release migrations OK.
  - Success: /health 200 in prod; CRUD endpoints functional; no failing CI on main.
- Phase 1: Chat notifications (Slack) GA → v0.2.0
  - Tasks: Document SLACK_* setup; minimal unit test for payload shape; validate retries/backoff; enable via env in staging then prod.
  - Success: Support requests post to Slack reliably when SLACK_WEBHOOK_URL is set.
- Phase 2: Email hardening → v0.3.0
  - Tasks: Add SMTP timeouts/retries; structured error handling; pluggable email provider; optional SendGrid; feature flag.
  - Success: Robust delivery with graceful fallbacks and clear logs.
- Phase 3: Background jobs → v0.4.0
  - Tasks: Introduce RQ/Celery with Redis; move notifications off request path; retries + DLQ; worker health.
  - Success: Async notifications with DLQ visibility.
- Phase 4: Security → v0.5.0
  - Tasks: Enforce API key in prod; rate limiting (fastapi-limiter); security headers; request ID logging.
  - Success: Abuse protected; traceable requests.
- Phase 5: Observability → v0.6.0
  - Tasks: Prometheus metrics; OpenTelemetry tracing; Sentry errors; dashboards.
  - Success: Metrics and traces available with alerts.
- Phase 6: Phone (Twilio) → v0.7.0
  - Tasks: Inbound webhooks; call forwarding; persist call logs (models/migrations).
  - Success: Test call flows end-to-end.
- Phase 7: Ops → v0.8.0
  - Tasks: PagerDuty/Opsgenie integration; runbooks; escalation tests.
  - Success: Test incident routes to on-call.
