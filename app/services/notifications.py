from __future__ import annotations
from typing import Optional
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

from app.core.config import settings

class NotificationService:
    """Simple notification service supporting email now and placeholders for chat/phone."""

    def send_email(self, to: str, subject: str, body: str, *, from_email: Optional[str] = None) -> None:
        host = settings.SMTP_HOST
        user = settings.SMTP_USER
        pwd = settings.SMTP_PASSWORD
        port = settings.SMTP_PORT
        if not host or not user or not pwd:
            # In dev, just log to console to avoid failures when SMTP isn't configured
            print(f"[Email DEV] To: {to} | Subject: {subject}\n{body}")
            return

        msg = MIMEText(body, _charset="utf-8")
        msg["Subject"] = subject
        msg["From"] = formataddr((settings.APP_NAME, from_email or settings.SMTP_FROM_EMAIL))
        msg["To"] = to
        with smtplib.SMTP(host, port) as server:
            server.starttls()
            server.login(user, pwd)
            server.send_message(msg)

    def send_chat(self, channel: str, message: str) -> None:
        # Placeholder: integrate Slack/Discord/MS Teams webhook here
        print(f"[Chat DEV] Channel: {channel} | Message: {message}")

    def forward_phone_call(self, from_number: str, to_number: Optional[str] = None) -> None:
        # Placeholder: integrate Twilio inbound webhook + call forward
        print(f"[Phone DEV] Forwarding call from {from_number} to {to_number or settings.SUPPORT_FORWARD_NUMBER}")

notifications = NotificationService()
