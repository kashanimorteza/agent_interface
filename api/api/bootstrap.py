"""The API Bootstrap: reads the runtime Configuration, creates the API, and starts serving."""

from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import uvicorn
import yaml
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# The API Component: the directory that holds the runtime Configuration and the project file.
COMPONENT_ROOT = Path(__file__).resolve().parents[1]
CONFIGURATION_FILE = COMPONENT_ROOT / "config.yaml"


def load_configuration() -> dict[str, Any]:
    """Read the runtime Configuration, the only source of every runtime value."""
    with CONFIGURATION_FILE.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def create_app() -> FastAPI:
    """Create the one API from the runtime Configuration."""
    configuration = load_configuration()
    prefix = urlparse(configuration["url"]).path.rstrip("/")
    swagger = urlparse(configuration["documentation"]["swagger"]).path
    application = FastAPI(
        title=configuration["title"],
        description=configuration["description"],
        docs_url=swagger,
        redoc_url=urlparse(configuration["documentation"]["redoc"]).path,
        openapi_url=f"{prefix}/openapi.json",
        swagger_ui_oauth2_redirect_url=f"{swagger}/oauth2-redirect",
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return application


app = create_app()


def main() -> None:
    """Start serving at the configured address with the configured number of workers."""
    configuration = load_configuration()
    uvicorn.run(
        "api.bootstrap:app",
        host=configuration["host"],
        port=configuration["port"],
        workers=configuration["workers"],
    )


if __name__ == "__main__":
    main()
