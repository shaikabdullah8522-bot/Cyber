from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import time

class RateLimitMiddleware(BaseHTTPMiddleware):
    RATE_LIMIT = 30   # max requests
    WINDOW = 60       # per 60 sec
    requests = {}

    async def dispatch(self, request, call_next):
        ip = request.client.host
        now = time.time()
        window_start = now - self.WINDOW

        self.requests.setdefault(ip, [])
        self.requests[ip] = [t for t in self.requests[ip] if t > window_start]

        if len(self.requests[ip]) >= self.RATE_LIMIT:
            return JSONResponse({"error": "Rate limit exceeded"}, status_code=429)

        self.requests[ip].append(now)
        return await call_next(request)
