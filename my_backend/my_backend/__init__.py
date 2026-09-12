"""Public interface of the Trading Assistant's Backend package.

Canonical usage::

    import my_backend
    my_backend.app  # the FastAPI application

Consumers reach Backend only through its HTTP API, published at the
application's OpenAPI description (``/openapi.json`` by default); this
Python-level export exists for running or testing the application itself.
"""

from my_backend.app import app

__all__ = ["app"]
