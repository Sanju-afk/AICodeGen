from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from main import app #fastapi instance
import datetime

def generate_openapi_spec():
    return get_openapi(
        title = app.title,
        version = app.version,
        openapi_version= app.openapi_version,
        description=app.description,
        routes = app.routes,
        tags = app.openapi_tags
    )

#endpoint to retrieve raw spec
@app.get("/openapi.json", include_in_schema=False)
async def get_openapi_spec():
    return generate_openapi_spec()

@app.get("/docs", include_in_schema=False)
async def custom_docs_redirect():
    return JSONResponse({"message" : "Access docs at /redoc or /docs"})

@app.get("/health", tags = ["System"], summary = "Service health check")
async def health_check(): 
    return {"status" : "OK", "timestamp" : datetime.datetime.now()}