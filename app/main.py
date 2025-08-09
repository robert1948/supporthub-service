from fastapi import FastAPI
from app.routes import tickets, messages

app = FastAPI(title="SupportHub Service")

app.include_router(tickets.router, prefix="/v1/tickets", tags=["Tickets"])
app.include_router(messages.router, prefix="/v1/messages", tags=["Messages"])

@app.get("/")
def root():
    return {"message": "SupportHub API running"}
