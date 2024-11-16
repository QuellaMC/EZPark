# app/api/utils/rate_limiter.py

from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from collections import defaultdict
from time import time

class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int, window_seconds: int):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time()
        window_start = current_time - self.window_seconds
        # Remove outdated requests
        self.requests[client_ip] = [timestamp for timestamp in self.requests[client_ip] if timestamp > window_start]
        
        if len(self.requests[client_ip]) >= self.max_requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests. Please try again later."
            )
        
        self.requests[client_ip].append(current_time)
        response = await call_next(request)
        return response
