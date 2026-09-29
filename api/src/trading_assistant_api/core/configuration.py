"""API's runtime configuration contract and its validation.

API owns the contract below and validates every value before it begins serving. It never owns
the values or their delivery: Platform's runtime bindings supply them through the environment,
and no value is stored in source, configuration, messages, or outcomes.

Required runtime values:
    API_HOST: Address the running API listens on.
    API_PORT: Port the running API listens on, an integer from 1 to 65535.
    API_TRANSPORT: Transport of the running API; only `HTTP` is supported.
    API_SHUTDOWN_TIMEOUT_SECONDS: Seconds a graceful shutdown waits for requests in progress,
        a positive integer.
    API_CORS_ALLOWED_ORIGINS: Comma-separated origins granted cross-origin access; present
        but empty grants none.

Optional runtime values:
    API_HEALTH_PATH: Location of the health signal, `/health` when omitted.
    API_READINESS_PATH: Location of the readiness signal, `/ready` when omitted.
    Neither signal can be disabled: a value that is not a usable location is refused.
"""

import os
import re
from collections.abc import Mapping
from dataclasses import dataclass
from urllib.parse import urlsplit

HOST = "API_HOST"
PORT = "API_PORT"
TRANSPORT = "API_TRANSPORT"
SHUTDOWN_TIMEOUT_SECONDS = "API_SHUTDOWN_TIMEOUT_SECONDS"
CORS_ALLOWED_ORIGINS = "API_CORS_ALLOWED_ORIGINS"

HEALTH_PATH = "API_HEALTH_PATH"
READINESS_PATH = "API_READINESS_PATH"

TRANSPORTS = ("HTTP",)
DEFAULT_HEALTH_PATH = "/health"
DEFAULT_READINESS_PATH = "/ready"
RESERVED_PATHS = ("/docs", "/redoc", "/openapi.json")
LOCATION = re.compile(r"/[A-Za-z0-9._~-]+(/[A-Za-z0-9._~-]+)*")


@dataclass(frozen=True)
class Settings:
    """Validated runtime values of the running API.

    Attributes:
        host (str): Address to listen on.
        port (int): Port to listen on.
        transport (str): Transport of the running API.
        shutdown_timeout_seconds (int): Wait allowed for a graceful shutdown.
        cors_allowed_origins (tuple[str, ...]): Origins granted cross-origin access.
        health_path (str): Location of the health signal.
        readiness_path (str): Location of the readiness signal.
    """

    host: str
    port: int
    transport: str
    shutdown_timeout_seconds: int
    cors_allowed_origins: tuple[str, ...]
    health_path: str
    readiness_path: str


def _integer(name: str, value: str, minimum: int, maximum: int | None = None) -> int:
    """Return a runtime value as an integer within its bounds.

    Args:
        name (str): Name of the runtime value, used in the refusal message.
        value (str): Supplied text.
        minimum (int): Smallest accepted number.
        maximum (int, optional): Largest accepted number.

    Returns:
        (int): The validated number.

    Raises:
        ValueError: When the text is not an integer within the bounds; the message names the
            value and never contains it.
    """
    try:
        number = int(value)
    except ValueError:
        number = None
    if number is None or number < minimum or (maximum is not None and number > maximum):
        bound = (
            f"at least {minimum}" if maximum is None else f"from {minimum} to {maximum}"
        )
        raise ValueError(
            f"Required runtime value {name} is invalid: expected an integer {bound}"
        )
    return number


def _origin(value: str) -> str:
    """Return an origin unchanged when it is a scheme, host, and optional port only.

    Args:
        value (str): Supplied origin.

    Returns:
        (str): The validated origin.

    Raises:
        ValueError: When the origin is malformed; the message names the value and never
            contains the origin.
    """
    parts = urlsplit(value)
    if (
        parts.scheme not in ("http", "https")
        or not parts.hostname
        or value != f"{parts.scheme}://{parts.netloc}"
    ):
        raise ValueError(
            f"Required runtime value {CORS_ALLOWED_ORIGINS} is invalid: "
            "expected comma-separated origins such as https://example.com"
        )
    return value


def _location(environ: Mapping[str, str], name: str, default: str) -> str:
    """Return the location of a lifecycle signal.

    Args:
        environ (Mapping[str, str]): Runtime values.
        name (str): Name of the runtime value, used in the refusal message.
        default (str): Location used when the value is omitted.

    Returns:
        (str): The validated location.

    Raises:
        ValueError: When the value is present but is not a usable location, which includes any
            attempt to switch the signal off; the message names the value and never contains it.
    """
    value = environ.get(name, default)
    if not LOCATION.fullmatch(value) or value in RESERVED_PATHS:
        raise ValueError(
            f"Runtime value {name} is invalid: expected a location such as {default}; "
            "the signal cannot be disabled"
        )
    return value


def load_settings(environ: Mapping[str, str] | None = None) -> Settings:
    """Validate every required runtime value and return them.

    Args:
        environ (Mapping[str, str], optional): Runtime values; the process environment when
            omitted.

    Returns:
        (Settings): The validated runtime values.

    Raises:
        ValueError: When a runtime value is missing or invalid; the message names the value
            and never contains it.
    """
    environ = os.environ if environ is None else environ
    for name in (HOST, PORT, TRANSPORT, SHUTDOWN_TIMEOUT_SECONDS, CORS_ALLOWED_ORIGINS):
        if name not in environ or (
            name != CORS_ALLOWED_ORIGINS and not environ[name].strip()
        ):
            raise ValueError(f"Required runtime value {name} is missing")
    if environ[TRANSPORT] not in TRANSPORTS:
        raise ValueError(
            f"Required runtime value {TRANSPORT} is invalid: expected one of {', '.join(TRANSPORTS)}"
        )
    health_path = _location(environ, HEALTH_PATH, DEFAULT_HEALTH_PATH)
    readiness_path = _location(environ, READINESS_PATH, DEFAULT_READINESS_PATH)
    if health_path == readiness_path:
        raise ValueError(
            f"Runtime values {HEALTH_PATH} and {READINESS_PATH} are invalid: "
            "the two signals need distinct locations"
        )
    origins = tuple(
        o.strip() for o in environ[CORS_ALLOWED_ORIGINS].split(",") if o.strip()
    )
    return Settings(
        host=environ[HOST].strip(),
        port=_integer(PORT, environ[PORT], 1, 65535),
        transport=environ[TRANSPORT],
        shutdown_timeout_seconds=_integer(
            SHUTDOWN_TIMEOUT_SECONDS, environ[SHUTDOWN_TIMEOUT_SECONDS], 1
        ),
        cors_allowed_origins=tuple(_origin(o) for o in origins),
        health_path=health_path,
        readiness_path=readiness_path,
    )
