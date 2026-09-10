from __future__ import annotations

from dataclasses import dataclass

from ._engine import CONFIG


@dataclass(frozen=True)
class InstanceIdentity:
    key: str
    name: str
    purpose: str
    engine: str


def list_instances() -> list[InstanceIdentity]:
    return [
        InstanceIdentity(key=key, name=cfg["name"], purpose=cfg["purpose"], engine=cfg["engine"])
        for key, cfg in CONFIG["instances"].items()
    ]


def default_instance() -> str:
    return CONFIG["default_instance"]
