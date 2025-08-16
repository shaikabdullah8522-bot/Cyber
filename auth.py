from fastapi import APIRouter, HTTPException, Header
import jwt, datetime
import config

router = APIRouter()

def verify_token(token: str = Header(...)):
    try:
        payload = jwt.decode(token, config.JWT_SECRET, algorithms=["HS256"])
        return payload["sub"]
    except:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

def require_admin(x_api_key: str = Header(...)):
    if x_api_key != config.ADMIN_API_KEY:
        raise HTTPException(status_code=403, detail="Admin key required")
    return True

@router.post("/login")
def login(username: str, password: str, x_api_key: str = Header(...)):
    if x_api_key != config.ADMIN_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid Admin Key")
    if username != "admin" or password != "password123":
        raise HTTPException(status_code=401, detail="Invalid credentials")
    payload = {"sub": username, "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}
    token = jwt.encode(payload, config.JWT_SECRET, algorithm="HS256")
    return {"access_token": token}
