"""Bootstrap: the single runtime entry point of the API."""

from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import uvicorn
import yaml
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import problems
from api.groups import GROUPS

CONFIGURATION = Path(__file__).resolve().parents[1] / "config.yaml"


def load_configuration() -> dict[str, Any]:
    return yaml.safe_load(CONFIGURATION.read_text())


class DocumentedAPI(FastAPI):
    """The API, whose documentation holds one section per Group over its Adapters' sections."""

    def openapi(self) -> dict[str, Any]:
        schema = super().openapi()
        schema["x-tagGroups"] = [
            {"name": group.NAME, "tags": [router.tags[0] for router in group.ADAPTERS.values()]}
            for group in GROUPS
        ]
        return schema


def create_api() -> FastAPI:
    configuration = load_configuration()
    documentation = configuration["documentation"]
    base_path = urlparse(configuration["url"]).path.rstrip("/")
    sections = [router.tags[0] for group in GROUPS for router in group.ADAPTERS.values()]
    api = DocumentedAPI(
        title=configuration["title"],
        description=configuration["description"],
        docs_url=urlparse(documentation["swagger"]).path,
        redoc_url=urlparse(documentation["redoc"]).path,
        openapi_url=f"{base_path}/openapi.json",
        openapi_tags=[{"name": section} for section in sections],
        swagger_ui_oauth2_redirect_url=None,
    )
    api.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    problems.register(api)
    key = configuration["key"]
    prefix = f"/{key}" if key else ""
    for group in GROUPS:
        for adapter, router in group.ADAPTERS.items():
            api.include_router(router, prefix=f"{prefix}/{group.SEGMENT}/{adapter}")
    return api


app = create_api()


def main() -> None:
    configuration = load_configuration()
    uvicorn.run(
        "api.bootstrap:app",
        host=configuration["host"],
        port=configuration["port"],
        workers=configuration["workers"],
    )


if __name__ == "__main__":
    main()
