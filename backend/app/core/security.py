from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader

from app.core.config import settings


api_key_header = APIKeyHeader(name="Authorization", auto_error=True)


def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != settings.NEXT_PUBLIC_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key
