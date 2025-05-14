from fastapi import FastAPI
from fastapi.responses import JSONResponse
import motor.motor_asyncio
from routes import router
from core.config import settings
from fastapi.openapi.utils import get_openapi
from core.security import oauth2_scheme

app = FastAPI(title=settings.app_name, version=settings.version)
app.include_router(router, prefix="/api")


@app.get("/health")
async def health_check():
    try:
        client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongodb_uri, serverSelectionTimeoutMS=2000)
        await client.server_info()
        db_status = "OK"
    except Exception:
        db_status = "Unavailable"
    return JSONResponse({

        "status": "healthy",
        "database": db_status,
        "limits": {"basic_daily_limit": settings.basic_daily_limit,
                   "premium_daily_limit": settings.premium_daily_limit},
        "config": {"app_name": settings.app_name, "version": settings.version}
    })


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(title=settings.app_name, version=settings.version, description="JWT auth enabled",
                         routes=app.routes)
    schema["components"]["securitySchemes"] = {
        "BearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}}
    for path, methods in schema.get("paths", {}).items():
        if path in ["/api/login", "/health"]:
            continue
        for op in methods.values():
            op["security"] = [{"BearerAuth": []}]
    app.openapi_schema = schema
    return schema


app.openapi = custom_openapi