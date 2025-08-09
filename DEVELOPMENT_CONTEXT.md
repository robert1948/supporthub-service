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
  - Health: GET /
  - Support intake: POST /v1/support/request (channel=email|chat|phone)
  - Tickets: GET/POST /v1/tickets, GET/PATCH /v1/tickets/{id}
  - Messages: GET/POST /v1/messages, GET /v1/messages/{id}
- Notifications service:
  - Email via SMTP (prints to console in dev when SMTP is not configured)
  - Chat + Phone placeholders (integration points for Slack/Twilio, etc.)
- Config and Security:
  - CORS middleware (configurable origins, headers, methods)
  - Optional API key guard (header: X-API-Key) via env var API_KEY
  - .env.example added; real .env files are ignored by Git
- Containerization:
  - Dockerfile with curl for healthcheck
  - docker-compose with env wiring (SMTP, CORS, API key, Redis)
- Repo hygiene: .gitignore and .dockerignore added

## How to Run (Dev)
1) Copy envs and edit as needed:
   cp .env.example .env
2) Start services:
   docker compose up --build
3) Visit docs: http://localhost:8000/docs

## Configuration (key envs)
- CORS_ORIGINS: comma-separated origins (use explicit domains in prod)
- API_KEY: optional; when set, require header X-API-Key on requests
- SMTP_*: SMTP_HOST/PORT/USER/PASSWORD/FROM
- SUPPORT_TEAM_EMAIL: default support email
- REDIS_URL: redis://redis:6379/0 (placeholder for bg tasks later)
- SUPPORT_FORWARD_NUMBER: for phone integrations

## Next Steps (Roadmap)
- Email: select provider (SMTP or SendGrid) and enable retries
- Chat: integrate Slack/MS Teams (webhook or app), secrets management
- Phone: Twilio voice webhooks for inbound + call forwarding, call logs
- Persistence: SQLAlchemy models + Alembic migrations for tickets/messages/requests
- Jobs: background queue (RQ or Celery) with Redis, retries, DLQ
- Security: rate limiting, structured logging, request ID, security headers
- Observability: metrics (Prometheus), tracing, Sentry, uptime checks
- CI/CD: GitHub Actions (tests, lint, build, image push), deploy pipeline
- Ops: on-call escalation (PagerDuty/Opsgenie), rotation and runbooks
