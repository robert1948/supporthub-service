from __future__ import annotations
from typing import Optional
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import json
import time

import httpx

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

    def send_chat(self, channel: Optional[str], message: str) -> None:
        """Send a chat message via Slack Incoming Webhook if configured, else dev-log.

        If SLACK_WEBHOOK_URL is not set, prints to console. Supports optional
        channel override, username and icon emoji from settings.
        Includes simple retry/backoff for transient errors.
        """
        webhook = settings.SLACK_WEBHOOK_URL
        if not webhook:
            print(f"[Chat DEV] Channel: {channel or settings.SLACK_CHANNEL or '#support'} | Message: {message}")
            return

        payload = {
            "text": message,
        }
        if channel or settings.SLACK_CHANNEL:
            payload["channel"] = channel or settings.SLACK_CHANNEL
        if settings.SLACK_USERNAME:
            payload["username"] = settings.SLACK_USERNAME
        if settings.SLACK_ICON_EMOJI:
            payload["icon_emoji"] = settings.SLACK_ICON_EMOJI

        max_attempts = 3
        backoff = 1.0
        for attempt in range(1, max_attempts + 1):
            try:
                resp = httpx.post(webhook, json=payload, timeout=10)
                if resp.status_code in (200, 204):
                    return
                # Slack webhooks may return 5xx on transient issues
                if 500 <= resp.status_code < 600:
                    raise RuntimeError(f"Slack error {resp.status_code}: {resp.text}")
                # For other errors, do not retry
                print(f"[Chat ERROR] Slack webhook responded {resp.status_code}: {resp.text}")
                return
            except Exception as e:
                if attempt == max_attempts:
                    print(f"[Chat ERROR] Failed to send after {attempt} attempts: {e}")
                    return
                time.sleep(backoff)
                backoff *= 2

    def forward_phone_call(self, from_number: str, to_number: Optional[str] = None) -> None:
        # Placeholder: integrate Twilio inbound webhook + call forward
        print(f"[Phone DEV] Forwarding call from {from_number} to {to_number or settings.SUPPORT_FORWARD_NUMBER}")

notifications = NotificationService()
