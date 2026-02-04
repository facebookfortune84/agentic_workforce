"""
GitHub OAuth & License-Protected Authentication Routes
------------------------------------------------------

Extracted from server.py (v29.2 INDUSTRIAL ULTIMATE).

Provides:
- GitHub OAuth redirect
- GitHub OAuth callback
- GitHub token exchange
"""

import os
import httpx
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse

from src.api.dependencies.security import get_license
from src.auth import gatekeeper
from src.system.config import logger


router = APIRouter(tags=["auth"])


# ==============================================================================
# 1. GITHUB LOGIN (REDIRECT)
# ==============================================================================

@router.get("/github")
async def github_login():
    """
    Redirects the user to GitHub OAuth authorization page.
    """
    client_id = os.getenv("GITHUB_CLIENT_ID")

    if not client_id or client_id == "undefined":
        raise HTTPException(
            status_code=500,
            detail="GITHUB_CLIENT_ID is undefined. Check .env file."
        )

    redirect_uri = os.getenv(
        "GITHUB_REDIRECT_URI",
        "http://localhost:8000/api/v1/auth/github/callback"
    )

    url = (
        f"https://github.com/login/oauth/authorize?"
        f"client_id={client_id}&redirect_uri={redirect_uri}&scope=repo,user"
    )

    logger.info(f"🗝️ [OAUTH]: Redirecting to GitHub: {url}")

    return RedirectResponse(url)


# ==============================================================================
# 2. GITHUB CALLBACK
# ==============================================================================

@router.get("/github/callback")
async def github_callback(code: str):
    """
    Receives GitHub OAuth code and forwards it to the frontend.
    """
    frontend_url = "https://realmforgev2-prod.vercel.app/"
    target_url = f"{frontend_url}?code={code}"

    logger.info(
        f"🗝️ [OAUTH]: Handshake code received. Bridging to Root: {target_url}"
    )

    return RedirectResponse(url=target_url, status_code=302)


# ==============================================================================
# 3. GITHUB TOKEN EXCHANGE
# ==============================================================================

@router.post("/github")
async def github_exchange(
    req: gatekeeper.GithubTokenRequest,
    lic: gatekeeper.License = Depends(get_license)
):
    """
    Exchanges the GitHub OAuth code for an access token.
    """
    logger.info(f"🗝️ [OAUTH]: Token exchange initiated for {lic.user_id}")

    async with httpx.AsyncClient() as client:
        res = await client.post(
            "https://github.com/login/oauth/access_token",
            params={
                "client_id": os.getenv("GITHUB_CLIENT_ID"),
                "client_secret": os.getenv("GITHUB_CLIENT_SECRET"),
                "code": req.code,
            },
            headers={"Accept": "application/json"},
        )

        return res.json()