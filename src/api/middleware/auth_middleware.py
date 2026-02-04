"""
REALM FORGE: AUTH MIDDLEWARE v1.0
PURPOSE: Sovereign Gatekeeper integration for FastAPI.
PATH: F:/agentic_workforce/src/api/middleware/auth_middleware.py
"""

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from src.auth.gatekeeper import validate_key

class SovereignAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Paths that don't need a key (Health, Auth, etc.)
        whitelist = ["/health", "/api/v1/auth", "/static", "/docs", "/redoc", "/openapi.json"]
        
        if any(request.url.path.startswith(p) for p in whitelist):
            return await call_next(request)

        # Extract API Key from Header
        api_key = request.headers.get("X-API-KEY") or request.query_params.get("api_key")
        
        if not api_key:
            raise HTTPException(status_code=401, detail="X-API-KEY header missing.")

        license_data = await validate_key(api_key)
        if not license_data:
            raise HTTPException(status_code=403, detail="Invalid or Expired Sovereign License.")

        # Attach license to request state for use in routes
        request.state.license = license_data
        
        return await call_next(request)