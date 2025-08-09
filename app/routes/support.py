from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel, EmailStr, Field
from app.services.notifications import notifications

router = APIRouter()

class SupportRequest(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    channel: str = Field("email", pattern=r"^(email|chat|phone)$")
    subject: str = Field(..., min_length=3, max_length=200)
    message: str = Field(..., min_length=3, max_length=5000)
    phone_from: str | None = None

@router.post("/request", status_code=202)
def create_support_request(data: SupportRequest, bg: BackgroundTasks):
    """
    Accepts a support request and dispatches notifications via:
    - email: send an email to the support team
    - chat: post to a chat channel (placeholder)
    - phone: forward a call (placeholder)
    """
    summary = f"Support request from {data.name} <{data.email}>\n\n{data.message}"

    if data.channel == "email":
        bg.add_task(
            notifications.send_email,
            to="support@example.com",
            subject=f"[Support] {data.subject}",
            body=summary,
        )
    elif data.channel == "chat":
        bg.add_task(notifications.send_chat, channel="#support", message=summary)
    elif data.channel == "phone":
        if not data.phone_from:
            raise HTTPException(status_code=400, detail="phone_from required when channel=phone")
        bg.add_task(notifications.forward_phone_call, from_number=data.phone_from)
    else:
        raise HTTPException(status_code=400, detail="Invalid channel")

    return {"status": "accepted"}
