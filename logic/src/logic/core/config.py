"""Logic's private reading of its reserved configuration and required values."""

import base64
import binascii
import os
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

import yaml

from logic.core.errors import ConfigurationError

DEFAULT_CONFIGURATION = Path(__file__).parents[1] / "config.yaml"


def _is_fernet_key(value: str) -> bool:
    try:
        return len(base64.urlsafe_b64decode(value)) == 32
    except binascii.Error, ValueError:
        return False


_CHECKS = {"fernet_key": _is_fernet_key}


@dataclass(frozen=True, slots=True)
class RequiredValue:
    """One value Logic requires from its environment.

    Attributes:
        name: Name Logic uses for the value.
        environment: Environment variable that supplies it.
        purpose: What the value is needed for.
        check: Optional named format check applied before use.
    """

    name: str
    environment: str
    purpose: str
    check: str | None = None


def load_contract(path: Path = DEFAULT_CONFIGURATION) -> dict[str, RequiredValue]:
    """Read the required-value contract from the configuration.

    Args:
        path (Path): Configuration file to read.

    Returns:
        (dict[str, RequiredValue]): Declared required values by name; empty while none is declared.
    """
    document = yaml.safe_load(path.read_text()) or {}
    contract = {
        name: RequiredValue(name=name, **spec)
        for name, spec in (document.get("required_values") or {}).items()
    }
    for value in contract.values():
        if value.check is not None and value.check not in _CHECKS:
            raise ConfigurationError(
                f"Required value '{value.name}' declares an unknown check '{value.check}'"
            )
    return contract


def require(
    name: str,
    contract: Mapping[str, RequiredValue] | None = None,
    environ: Mapping[str, str] | None = None,
) -> str:
    """Return a required value after validating it, never disclosing it in an error.

    Args:
        name (str): Declared name of the value.
        contract (Mapping[str, RequiredValue], optional): Contract to use instead of the configuration.
        environ (Mapping[str, str], optional): Environment to read instead of the process environment.

    Returns:
        (str): The validated value.
    """
    declared = load_contract() if contract is None else contract
    if name not in declared:
        raise ConfigurationError(f"'{name}' is not declared in the Logic configuration")
    required = declared[name]
    value = (
        (os.environ if environ is None else environ)
        .get(required.environment, "")
        .strip()
    )
    if not value:
        raise ConfigurationError(
            f"Required value '{name}' is missing; set {required.environment}"
        )
    if required.check is not None and not _CHECKS[required.check](value):
        raise ConfigurationError(
            f"Required value '{name}' in {required.environment} is invalid ({required.check})"
        )
    return value
