from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx
import os

app = FastAPI(title="Gateway Service")

# Environment variables or hardcoded defaults for demo
COMMENT_SERVICE_URL = os.getenv("COMMENT_SERVICE_URL", "http://comment-service:8000")
MEMBER_SERVICE_URL = os.getenv("MEMBER_SERVICE_URL", "http://member-service:8000")

async def proxy_request(request: Request, target_url: str):
    """Generic proxy handler using httpx"""
    method = request.method
    headers = dict(request.headers)
    body = await request.body()

    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=method,
            url=target_url,
            headers=headers,
            content=body
        )
    return JSONResponse(status_code=response.status_code, content=response.json())

# Comments routes
@app.api_route("/comments", methods=["GET", "POST", "DELETE"])
async def handle_comments(request: Request):
    target_url = f"{COMMENT_SERVICE_URL}/comments"
    return await proxy_request(request, target_url)

# Members routes
@app.api_route("/members", methods=["GET", "POST", "DELETE"])
async def handle_members(request: Request):
    target_url = f"{MEMBER_SERVICE_URL}/members"
    return await proxy_request(request, target_url)
