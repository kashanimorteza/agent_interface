"""Broker: a broker the system can work with through a trading platform."""

from __future__ import annotations

from .base import Model, Relationship, UniqueTogether, field
from .trading_platform import TradingPlatform
from .user import User


class Broker(Model):
    """Defines a broker that the system can work with through its selected
    trading platform. Multiple brokers can be added so the system is not
    limited to a specific broker and can operate with any configured
    broker."""

    id: int | None = field("integer", primary_key=True, auto_increment=True)
    # The name is unique per user through the rule below, not on its own.
    name: str = field("string", purpose="The broker's display name.")
    user_id: int = field("integer", purpose="Identifies the user who owns the broker configuration.")
    trading_platform_id: int = field(
        "integer", purpose="Identifies the trading platform used by the broker."
    )
    status: bool = field("boolean", default=True, purpose="Indicates whether the broker is active.")
    description: str | None = field("string", nullable=True, purpose="Describes the broker.")

    relationships = (
        Relationship(field="user_id", target=User, kind="belongs_to"),
        Relationship(field="trading_platform_id", target=TradingPlatform, kind="belongs_to"),
    )

    rules = (UniqueTogether(fields=("user_id", "name")),)

    initial_data = ({"name": "FxPro", "user_id": 1, "trading_platform_id": 1},)
