"""Logic's runtime configuration contract."""

import math
import os
from collections.abc import Mapping
from dataclasses import dataclass, field

SECRET = "LOGIC_CREDENTIAL_SECRET"
TIMEOUT = "LOGIC_DEPENDENCY_TIMEOUT_SECONDS"
RETRIES = "LOGIC_DEPENDENCY_RETRIES"
MINIMUM_SECRET_LENGTH = 32


class ConfigurationError(ValueError):
    """Raised when a required runtime value is missing or malformed; names values, never contents."""


@dataclass(frozen=True, slots=True)
class Configuration:
    """Every runtime value Logic's Behaviour requires, validated on creation.

    Attributes:
        credential_secret: Secret material protecting encrypted credentials.
        dependency_timeout_seconds: Longest wait, in seconds, for one call to a dependency.
        dependency_retries: Most repeats of a safe or idempotent call after a temporary failure.
    """

    credential_secret: str = field(repr=False)
    dependency_timeout_seconds: float
    dependency_retries: int

    def __post_init__(self) -> None:
        """Refuse a value that is malformed, naming it without revealing it."""
        problems = []
        secret = self.credential_secret
        if not isinstance(secret, str) or len(secret) < MINIMUM_SECRET_LENGTH:
            problems.append(
                f"{SECRET} must be text of at least {MINIMUM_SECRET_LENGTH} characters"
            )
        timeout = self.dependency_timeout_seconds
        if (
            isinstance(timeout, bool)
            or not isinstance(timeout, int | float)
            or not math.isfinite(timeout)
            or timeout <= 0
        ):
            problems.append(f"{TIMEOUT} must be a finite number of seconds above zero")
        retries = self.dependency_retries
        if isinstance(retries, bool) or not isinstance(retries, int) or retries < 0:
            problems.append(f"{RETRIES} must be a whole number of zero or more")
        if problems:
            raise ConfigurationError("; ".join(problems))

    @classmethod
    def from_environment(
        cls, environment: Mapping[str, str] | None = None
    ) -> Configuration:
        """Read and validate the values from the environment.

        Args:
            environment (Mapping, optional): Values to read instead of the process environment.

        Returns:
            (Configuration): The validated configuration.
        """
        source = os.environ if environment is None else environment
        missing = [name for name in (SECRET, TIMEOUT, RETRIES) if not source.get(name)]
        if missing:
            raise ConfigurationError(
                f"missing required runtime values: {', '.join(missing)}"
            )
        try:
            timeout = float(source[TIMEOUT])
        except ValueError:
            timeout = math.nan
        try:
            retries = int(source[RETRIES])
        except ValueError:
            retries = -1
        return cls(source[SECRET], timeout, retries)
