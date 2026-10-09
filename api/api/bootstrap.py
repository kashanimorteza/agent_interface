"""Bootstrap: the single composition and execution point of the API."""

from pathlib import Path
from typing import Any

import uvicorn
import yaml
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.groups.entity import (
    account,
    account_group,
    action,
    action_group,
    asset,
    broker,
    currency,
    instance,
    partial_group,
    partial_rule,
    position,
    trading_platform,
    trailing_group,
    trailing_rule,
    user,
)
from api.problems import register_problems

CONFIGURATION = Path(__file__).resolve().parent.parent / "config.yaml"

GROUPS: dict[str, list[APIRouter]] = {
    "Entity": [
        user.router,
        trading_platform.router,
        instance.router,
        currency.router,
        broker.router,
        asset.router,
        account_group.router,
        account.router,
        trailing_group.router,
        trailing_rule.router,
        partial_group.router,
        partial_rule.router,
        action_group.router,
        action.router,
        position.router,
    ],
}

configuration = yaml.safe_load(CONFIGURATION.read_text())
prefix = f"/{configuration['key']}" if configuration["key"] else ""


class Api(FastAPI):
    """The one API, whose published schema groups the Adapter sections by Group."""

    def openapi(self) -> dict[str, Any]:
        schema = super().openapi()
        schema["x-tagGroups"] = [
            {"name": group, "tags": [tag for router in routers for tag in router.tags]}
            for group, routers in GROUPS.items()
        ]
        return schema


app = Api(
    title=configuration["title"],
    description=configuration["description"],
    docs_url=f"{prefix}/docs",
    redoc_url=f"{prefix}/redoc",
    openapi_url=f"{prefix}/openapi.json",
    swagger_ui_oauth2_redirect_url=None,
    openapi_tags=[
        {"name": tag}
        for routers in GROUPS.values()
        for router in routers
        for tag in router.tags
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
register_problems(app)

for group, routers in GROUPS.items():
    for router in routers:
        app.include_router(router, prefix=f"{prefix}/{group.lower()}")


def main() -> None:
    uvicorn.run(
        "api.bootstrap:app",
        host=configuration["host"],
        port=configuration["port"],
        workers=configuration["workers"],
    )


if __name__ == "__main__":
    main()
