from fastapi import FastAPI

from app.api.main import api_router
from fastapi.routing import APIRoute
from app.core.config import settings

def custom_generate_unique_id(route: APIRoute) -> str:  # Generates unique ID for API instantiation
    return f"{route.tags[0]}-{route.name}"

app = FastAPI(
    title=settings.PROJECT_NAME,                        # Uses config.py
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,)
app.include_router(api_router, prefix=settings.API_V1_STR)
