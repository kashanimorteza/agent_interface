from __future__ import annotations

import pytest

from my_database._base import get_runtime_config
from my_database._config import UnknownInstanceError


def test_default_instance_resolves():
    config = get_runtime_config()
    resolved = config.resolve(None)
    assert resolved.key == config.default_instance == "general"


def test_explicit_known_instance_resolves():
    config = get_runtime_config()
    resolved = config.resolve("general")
    assert resolved.key == "general"


def test_unknown_instance_is_rejected_not_redirected():
    config = get_runtime_config()
    with pytest.raises(UnknownInstanceError):
        config.resolve("does-not-exist")
