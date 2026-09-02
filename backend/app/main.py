from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.security import APIKeyHeader

from app.config import API_KEY
from app.routers import router

app = FastAPI(title="Trading Assistant", docs_url="/docs", redoc_url=None)

API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(api_key: str | None = Security(API_KEY_HEADER)) -> str:
    if api_key is None or api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Missing or invalid API key")
    return api_key


app.include_router(router, dependencies=[Depends(verify_api_key)])
