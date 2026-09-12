"""The Backend application entry point."""

from __future__ import annotations

from fastapi import FastAPI

from .api import build_all_routers

app = FastAPI(
    title="Trading Assistant Backend",
    description="Standard operations for every domain Model, backed by the shared Database.",
    version="0.1.0",
)

for router in build_all_routers():
    app.include_router(router)
