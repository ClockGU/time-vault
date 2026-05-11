from hashlib import sha256

from fastapi import Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN

from .settings import Settings, get_settings

api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)


def required_api_key(
    settings: Settings = Depends(get_settings), api_key: str = Security(api_key_header)
):
    if api_key == settings.API_KEY:
        return api_key_header
    raise HTTPException(
        status_code=HTTP_403_FORBIDDEN, detail="No valid API KEY provided."
    )


def required_hashed_api_key(
    settings: Settings = Depends(get_settings), api_key: str = Security(api_key_header)
):
    hash = bytes(settings.ADMIN_KEYWORD, "utf-8") + bytes(settings.API_KEY, "utf-8")
    hashed_key = sha256(hash).hexdigest()
    if api_key == hashed_key:
        return api_key_header
    raise HTTPException(
        status_code=HTTP_403_FORBIDDEN, detail="No valid API KEY provided."
    )
