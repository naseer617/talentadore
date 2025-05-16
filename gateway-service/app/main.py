from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
import httpx
import os
from typing import Dict, Any

app = FastAPI(
    title="Gateway Service",
    description="API Gateway for Talentadore services",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Environment variables or hardcoded defaults for demo
COMMENT_SERVICE_URL = os.getenv("COMMENT_SERVICE_URL", "http://comment-service:8000")
MEMBER_SERVICE_URL = os.getenv("MEMBER_SERVICE_URL", "http://member-service:8000")

async def proxy_request(request: Request, target_url: str):
    """Generic proxy handler using httpx"""
    method = request.method
    headers = dict(request.headers)
    headers.pop("host", None)
    body = await request.body()

    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=method,
            url=target_url,
            headers=headers,
            content=body
        )
    return JSONResponse(status_code=response.status_code, content=response.json())

async def get_service_schema(service_url: str) -> Dict[str, Any]:
    """Get OpenAPI schema from a service"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{service_url}/openapi.json")
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Failed to fetch schema from {service_url}")
        return response.json()

def custom_openapi():
    """Generate custom OpenAPI schema"""
    if not app.openapi_schema:
        # Get base schema
        openapi_schema = get_openapi(
            title=app.title,
            version="1.0.0",
            description=app.description,
            routes=app.routes,
        )

        # Initialize components if not present
        if "components" not in openapi_schema:
            openapi_schema["components"] = {"schemas": {}}

        # Add paths for each service
        for service_name, service_url in [
            ("comments", COMMENT_SERVICE_URL),
            ("members", MEMBER_SERVICE_URL)
        ]:
            try:
                # Fetch schema from service
                service_schema = httpx.run_sync(get_service_schema, service_url)

                # Add paths
                for path, path_item in service_schema.get("paths", {}).items():
                    # Update operation IDs to avoid conflicts
                    for operation in path_item.values():
                        if "operationId" in operation:
                            operation["operationId"] = f"{service_name}_{operation['operationId']}"

                    # Add path to schema
                    openapi_schema["paths"][path] = path_item

                # Add components (schemas, etc.)
                if "components" in service_schema:
                    for component_type, components in service_schema["components"].items():
                        if component_type not in openapi_schema["components"]:
                            openapi_schema["components"][component_type] = {}
                        openapi_schema["components"][component_type].update(components)

            except Exception as e:
                print(f"Warning: Failed to fetch schema from {service_name} service: {e}")

        app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Comments routes
@app.api_route("/comments", methods=["GET", "POST", "DELETE"], include_in_schema=True)
async def handle_comments(request: Request):
    target_url = f"{COMMENT_SERVICE_URL}/comments"
    return await proxy_request(request, target_url)

@app.api_route("/comments/{comment_id}", methods=["GET", "DELETE"], include_in_schema=True)
async def handle_comment(request: Request, comment_id: int):
    target_url = f"{COMMENT_SERVICE_URL}/comments/{comment_id}"
    return await proxy_request(request, target_url)

# Members routes
@app.api_route("/members", methods=["GET", "POST", "DELETE"], include_in_schema=True)
async def handle_members(request: Request):
    target_url = f"{MEMBER_SERVICE_URL}/members"
    return await proxy_request(request, target_url)

@app.api_route("/members/{member_id}", methods=["GET", "DELETE"], include_in_schema=True)
async def handle_member(request: Request, member_id: int):
    target_url = f"{MEMBER_SERVICE_URL}/members/{member_id}"
    return await proxy_request(request, target_url)
