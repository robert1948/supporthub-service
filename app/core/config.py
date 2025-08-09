import os

class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "SupportHub Service")
    APP_VERSION: str = os.getenv("APP_VERSION", os.getenv("GIT_SHA", "dev"))

    # Database
    DATABASE_URL: str | None = os.getenv("DATABASE_URL")

    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://redis:6379/0")

    # Email (SMTP)
    SMTP_HOST: str | None = os.getenv("SMTP_HOST")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: str | None = os.getenv("SMTP_USER")
    SMTP_PASSWORD: str | None = os.getenv("SMTP_PASSWORD")
    SMTP_FROM_EMAIL: str = os.getenv("SMTP_FROM_EMAIL", "no-reply@supporthub.local")
    SUPPORT_TEAM_EMAIL: str = os.getenv("SUPPORT_TEAM_EMAIL", "support@example.com")

    # Phone
    SUPPORT_FORWARD_NUMBER: str | None = os.getenv("SUPPORT_FORWARD_NUMBER")

    # CORS
    _origins_raw = os.getenv("CORS_ORIGINS", "*")
    if _origins_raw.strip() in ("", "*"):
        CORS_ORIGINS: list[str] = ["*"]
    else:
        CORS_ORIGINS: list[str] = [o.strip() for o in _origins_raw.split(",") if o.strip()]
    CORS_ALLOW_CREDENTIALS: bool = os.getenv("CORS_ALLOW_CREDENTIALS", "false").lower() == "true"
    CORS_ALLOW_METHODS: list[str] = [m.strip() for m in os.getenv(
        "CORS_ALLOW_METHODS", "GET,POST,PUT,PATCH,DELETE,OPTIONS"
    ).split(",")]
    CORS_ALLOW_HEADERS: list[str] = [h.strip() for h in os.getenv("CORS_ALLOW_HEADERS", "*").split(",")]

    # API security (optional)
    API_KEY: str | None = os.getenv("API_KEY")

settings = Settings()
