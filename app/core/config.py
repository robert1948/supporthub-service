import os

class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "SupportHub Service")

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

settings = Settings()
