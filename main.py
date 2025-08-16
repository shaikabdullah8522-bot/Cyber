from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth import router as auth_router
from routers import ai, whois, ip_lookup, scan, hash_tools, terminal
from middleware.rate_limit import RateLimitMiddleware

app = FastAPI()
app.add_middleware(RateLimitMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth")
app.include_router(ai.router, prefix="/ai")
app.include_router(whois.router, prefix="/tools")
app.include_router(ip_lookup.router, prefix="/tools")
app.include_router(scan.router, prefix="/tools")
app.include_router(hash_tools.router, prefix="/tools")
app.include_router(terminal.router, prefix="/tools")
