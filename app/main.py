from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from app.routes import tickets, messages
from app.routes import support
from app.core.config import settings

app = FastAPI(title="SupportHub Service", description="24/7 Support — chat, email, or phone.")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# Optional API key security dependency
async def api_key_guard(x_api_key: str | None = Header(default=None, alias="X-API-Key")):
    if settings.API_KEY and x_api_key != settings.API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

# Routers
app.include_router(tickets.router, prefix="/v1/tickets", tags=["Tickets"], dependencies=[Depends(api_key_guard)])
app.include_router(messages.router, prefix="/v1/messages", tags=["Messages"], dependencies=[Depends(api_key_guard)])
app.include_router(support.router, prefix="/v1/support", tags=["Support"], dependencies=[Depends(api_key_guard)])

@app.get("/")
def root():
    return {"message": "SupportHub API running"}
