from fastapi import Depends, FastAPI

from app.dependencies import verify_api_key
from app.routes import router

app = FastAPI(title="Trading Assistant", docs_url="/docs", redoc_url=None)
app.include_router(router, dependencies=[Depends(verify_api_key)])
