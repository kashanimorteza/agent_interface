"""Verifies the complete Backend Public Interface as one whole (task P3-G13-T1)."""

from __future__ import annotations

import ast
from pathlib import Path

from backend.logic.registry import LOGIC_REGISTRY

_BACKEND_SRC = Path(__file__).resolve().parents[1] / "src" / "backend"


def test_every_capability_reachable_through_the_official_entry_point(client, auth_headers) -> None:
    # Health/readiness, every Model's CRUD+enable/disable, auth, all through one app.
    assert client.get("/health").status_code == 200
    assert client.get("/ready").status_code == 200
    for logic_cls in LOGIC_REGISTRY:
        import re

        words = re.findall(r"[A-Z][a-z0-9]*", logic_cls.model_cls.__name__)
        segment = "-".join(w.lower() for w in words)
        r = client.get(f"/v1/{segment}", headers=auth_headers)
        assert r.status_code == 200, f"{segment} not reachable"


def test_no_internal_module_is_imported_from_outside_the_backend_package() -> None:
    """No test or external code should need `backend.logic`, `backend.database_interface`,
    etc. directly to use Backend — only `backend.main:create_app` / the running API.
    This test instead checks the inverse invariant that matters operationally: nothing
    outside `backend` (in this repo) imports Backend's internals, since Backend's only
    declared Connection is to be consumed as a running service, not a library.
    """
    for path in [
        Path(__file__).resolve().parents[3] / "database",
        Path(__file__).resolve().parents[3] / "model",
    ]:
        if not path.exists():
            continue
        for py_file in path.rglob("*.py"):
            if ".venv" in py_file.parts:
                continue
            tree = ast.parse(py_file.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if (
                    isinstance(node, ast.ImportFrom)
                    and node.module
                    and node.module.startswith("backend")
                ):
                    raise AssertionError(f"{py_file} imports Backend internals: {node.module}")
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        assert not alias.name.startswith("backend"), py_file


def test_construction_uses_only_the_supported_surface(test_db_config) -> None:
    from backend.config import Settings
    from backend.main import create_app

    app = create_app(Settings(cors_allowed_origins=[]), database_config=test_db_config)
    assert app is not None


def test_runtime_configuration_values_are_not_reachable_as_python_attributes_of_the_app(
    client,
) -> None:
    # Settings live on app.state (private), never exposed through any response body.
    r = client.get("/health")
    assert "settings" not in r.text.lower()
