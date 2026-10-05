"""Bootstrap: the single runtime entry point of API."""

from pathlib import Path
from urllib.parse import urlparse

import uvicorn
import yaml
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.groups import entity

CONFIGURATION = Path(__file__).resolve().parent.parent / "config.yaml"


def configuration() -> dict:
    """The runtime Configuration, the only source of every runtime value."""
    return yaml.safe_load(CONFIGURATION.read_text())


def create_app() -> FastAPI:
    """Create the API from the runtime Configuration."""
    values = configuration()
    key = values["key"]
    base = f"/{key}" if key else ""
    app = FastAPI(
        title=values["title"],
        description=values["description"],
        docs_url=urlparse(values["documentation"]["swagger"]).path,
        redoc_url=urlparse(values["documentation"]["redoc"]).path,
        openapi_url=f"{base}/openapi.json",
        swagger_ui_oauth2_redirect_url=None,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    for router in entity.routers:
        app.include_router(router, prefix=f"{base}/entity")
    return app


app = create_app()


def main() -> None:
    """Start serving on the configured host and port with the configured workers."""
    values = configuration()
    uvicorn.run(
        "api.bootstrap:app",
        host=values["host"],
        port=values["port"],
        workers=values["workers"],
    )


if __name__ == "__main__":
    main()
