"""Builds and returns every Model's API router."""

from __future__ import annotations

import my_model as m
from fastapi import APIRouter

from ..logic import REGISTRY
from ._router_factory import build_router

#: Backend's own external resource naming for each Model, independent of any
#: internal Database naming it happens to resemble.
_RESOURCES: dict[type[m.BaseModel], tuple[str, str]] = {
    m.User: ("users", "User"),
    m.TradingPlatform: ("trading-platforms", "Trading Platform"),
    m.Instance: ("instances", "Instance"),
    m.Currency: ("currencies", "Currency"),
    m.Broker: ("brokers", "Broker"),
    m.Asset: ("assets", "Asset"),
    m.AccountGroup: ("account-groups", "Account Group"),
    m.Account: ("accounts", "Account"),
    m.TrailingGroup: ("trailing-groups", "Trailing Group"),
    m.TrailingRule: ("trailing-rules", "Trailing Rule"),
    m.PartialGroup: ("partial-groups", "Partial Group"),
    m.PartialRule: ("partial-rules", "Partial Rule"),
    m.ActionGroup: ("action-groups", "Action Group"),
    m.Action: ("actions", "Action"),
    m.Position: ("positions", "Position"),
}


def build_all_routers() -> list[APIRouter]:
    return [
        build_router(model_type, REGISTRY[model_type], resource, tag)
        for model_type, (resource, tag) in _RESOURCES.items()
    ]
