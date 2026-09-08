"""Starting the layer, where its own settings say.

The settings this layer owns decide where it answers, so bringing it up reads
them rather than repeating them on a command line. A deployment changes the
settings; nothing here changes.
"""

from __future__ import annotations

import uvicorn

from .configuration import Configuration, load


def serve(configuration: Configuration | None = None) -> None:
    """Bring the layer up on the address its settings name."""

    settings = configuration or load()
    uvicorn.run(
        "my_backend.api.app:app",
        host=settings.service.host,
        port=settings.service.port,
        log_level="info",
    )


if __name__ == "__main__":  # pragma: no cover - the entry a person types
    serve()
