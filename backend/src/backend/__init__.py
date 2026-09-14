"""Trading Assistant Backend.

Backend's only public boundary is its running API (reached over HTTP) and its official
executable entry point (`backend.main:app`, started via the `fastapi` CLI). This package
exposes no importable application programming surface of its own: every internal part
(Logic, Model Interface, Database Interface, Runtime Configuration) remains private.
"""

from __future__ import annotations

__version__ = "0.1.0"
