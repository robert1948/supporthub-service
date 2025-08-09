from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list_messages():
    return [{"id": 1, "content": "Example Message"}]
