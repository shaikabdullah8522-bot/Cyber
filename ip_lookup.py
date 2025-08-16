from fastapi import APIRouter, Depends
from auth import verify_token, require_admin

router = APIRouter()

@router.get("/ping")
def ping(user=Depends(verify_token)):
    return {"status": "ok"}
