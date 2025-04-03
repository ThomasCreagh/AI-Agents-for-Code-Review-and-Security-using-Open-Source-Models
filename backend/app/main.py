import os
import logging
from fastapi import FastAPI, Depends, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

from app.api.main import api_router
from app.core.config import settings

app = FastAPI(
    title="Security Code Analyzer",
    description="API for analyzing code for security vulnerabilities",
    version="0.1.0",
)


@app.on_event("startup")
async def validate_environment():
    use_anthropic = os.getenv("USE_ANTHROPIC", "false").lower() == "true"
    if use_anthropic and not os.getenv("ANTHROPIC_API_KEY"):
        logging.error(
            "USE_ANTHROPIC is set to true but ANTHROPIC_API_KEY is not provided")
        raise ValueError(
            "Invalid API configuration: ANTHROPIC_API_KEY missing")

# Configure CORS
origins = ["*"]
if isinstance(settings.BACKEND_CORS_ORIGINS, list):
    origins = [str(origin) for origin in settings.BACKEND_CORS_ORIGINS]
elif settings.BACKEND_CORS_ORIGINS == "*":
    origins = ["*"]
else:
    origins = [settings.BACKEND_CORS_ORIGINS]

app.add_middleware(
    CORSMiddleware,
<<<<<<< HEAD
    allow_origins=["http://api.keysentinel.xyz",
                   "http://keysentinel.xyz",
                   "https://keysentinel.xyz",
                   "http://localhost:3000"],
=======
    allow_origins=["*"],
>>>>>>> origin/merge-ai-folder-fix
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": str(exc)},
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
