"""Run the Backend HTTP server with host and port from runtime configuration: ``python -m trading_backend``."""

import uvicorn

from trading_backend.settings import get_settings


def main() -> None:
    settings = get_settings()
    uvicorn.run("trading_backend.main:app", host=settings.host, port=settings.port)


if __name__ == "__main__":
    main()
