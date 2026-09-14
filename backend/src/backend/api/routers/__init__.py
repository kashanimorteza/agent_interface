"""Assembles every Model Logic unit's router under the versioned API prefix."""

from __future__ import annotations

import re

from fastapi import APIRouter

from ...logic.registry import LOGIC_REGISTRY
from ..router_factory import build_router


def _path_segment(model_name: str) -> str:
    words = re.findall(r"[A-Z][a-z0-9]*", model_name)
    return "-".join(word.lower() for word in words)


def build_all_routers(*, prefix: str) -> list[APIRouter]:
    return [
        build_router(logic_cls, prefix=f"{prefix}/{_path_segment(logic_cls.model_cls.__name__)}")
        for logic_cls in LOGIC_REGISTRY
    ]
