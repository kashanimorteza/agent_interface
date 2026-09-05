"""Secure value generation for initial records marked "Generate securely"."""

from __future__ import annotations

import secrets


def generate_secret(length: int = 32) -> str:
    """Return a URL-safe random string with at least ``length`` characters."""
    return secrets.token_urlsafe(max(length, 32))
