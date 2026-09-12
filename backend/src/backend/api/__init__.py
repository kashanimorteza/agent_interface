"""The external API boundary: decodes requests, invokes Logic, serializes results."""

from __future__ import annotations

from .routes import build_all_routers

__all__ = ["build_all_routers"]
