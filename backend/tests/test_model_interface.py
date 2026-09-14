"""Tests for the Model Interface (task P3-G1-T1)."""

from __future__ import annotations

import model

from backend import model_interface


def test_every_domain_definition_resolved_through_model_interface() -> None:
    for name in model_interface.__all__:
        if name == "ModelBase":
            continue
        backend_type = getattr(model_interface, name)
        model_type = getattr(model, name)
        assert backend_type is model_type


def test_domain_definitions_tuple_matches_the_public_names() -> None:
    names = {cls.__name__ for cls in model_interface.DOMAIN_DEFINITIONS}
    assert names == set(model_interface.__all__) - {"ModelBase"}
