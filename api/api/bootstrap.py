"""Bootstrap: the single runtime entry point of API."""

from pathlib import Path

import uvicorn
import yaml
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.groups import entity

CONFIGURATION = Path(__file__).resolve().parent.parent / "config.yaml"


def create_app() -> FastAPI:
    """Create the API from the runtime Configuration."""
    configuration = yaml.safe_load(CONFIGURATION.read_text())
    app = FastAPI(
        title=configuration["title"],
        description=configuration["description"],
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    key = configuration["key"]
    base = f"/{key}" if key else ""
    for router in entity.routers:
        app.include_router(router, prefix=f"{base}/entity")
    return app


app = create_app()


def main() -> None:
    """Start serving on the configured host and port with the configured workers."""
    configuration = yaml.safe_load(CONFIGURATION.read_text())
    uvicorn.run(
        "api.bootstrap:app",
        host=configuration["host"],
        port=configuration["port"],
        workers=configuration["workers"],
    )


if __name__ == "__main__":
    main()
