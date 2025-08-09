from fastapi import FastAPI
from app.routes import tickets, messages
from app.routes import support

app = FastAPI(title="SupportHub Service", description="24/7 Support — chat, email, or phone.")

app.include_router(tickets.router, prefix="/v1/tickets", tags=["Tickets"])
app.include_router(messages.router, prefix="/v1/messages", tags=["Messages"])
app.include_router(support.router, prefix="/v1/support", tags=["Support"])

@app.get("/")
def root():
    return {"message": "SupportHub API running"}
