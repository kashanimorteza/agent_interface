# my_backend

The application layer of the Trading Assistant. It lets a user enter and manage every defined Model, and publishes those operations as the HTTP API every external consumer depends on.

## Purpose and boundaries

`my_backend` owns **what the application does and how it is reached**:

- **Logic**: one Logic unit per shared Model, each providing create, get, list, update, and delete through a common baseline, validating input against the shared Model before persistence is reached;
- **Data Access**: the single translation point through which Logic reaches the Database gateway on the Instance bound in the runtime configuration;
- **API**: the HTTP boundary that decodes requests, invokes Logic, serializes results, maps logical outcomes to responses, and publishes its machine-readable description.

The dependency direction is fixed: **API → Logic → Data Access → Database interface**. Every Backend representation of a Model is derived from the shared definition in `my_model`; nothing here redefines a Model.

It does **not** own domain meaning (`my_model`), physical persistence (`my_database`), the user interface, or cross-layer composition. No cross-cutting capability (authentication, logging, error handling, testing) is enabled for this project, so the API is unauthenticated.

## Public interface

The external interface is the HTTP API the server publishes. In-process, `my_backend` exposes:

| Symbol | Purpose |
|---|---|
| `create_app` | Builds the API application from the Backend section of the runtime configuration; accepts optional resolved settings. |
| `resolve_settings` | Reads the Backend section of the runtime configuration into `BackendSettings`. |
| `BackendSettings` | The resolved section: `host`, `port`, `api_documentation`, and the bound `database_instance`. |
| `ConfigurationError` | The Backend section is missing or invalid. |

### HTTP API

Every shared Model is a resource named by the plural kebab case of the Model name, and every resource offers the same five operations:

| Operation | Method and path | Success |
|---|---|---|
| Create | `POST /{resource}` with the Model's fields in the body | `201` with the record |
| List | `GET /{resource}` | `200` with every record |
| Get | `GET /{resource}/{id}` | `200` with the record |
| Update | `PATCH /{resource}/{id}` with only the fields to change | `200` with the record |
| Delete | `DELETE /{resource}/{id}` | `204` |

Resources: `users`, `currencies`, `trading-platforms`, `brokers`, `account-groups`, `accounts`, `assets`, `trailing-groups`, `trailing-rules`, `partial-groups`, `partial-rules`, `action-groups`, `actions`, `positions`.

Input and output shapes derive from the shared Models. The identifier is assigned by storage and is never an input. A **credential field** (the User's `password` and `api_key`, the Account's `password`) is accepted as input and never returned: it is absent from every response, response schema, and error body. On update, an omitted credential leaves the stored credential unchanged.

Logical outcomes map to distinct responses:

| Outcome | Status | Body |
|---|---|---|
| The request shape or content violates the shared Model | `422` | `detail`: a list naming each failing field (`loc`), its message, and its type; never the offending input |
| The record does not exist | `404` | `detail`: a message naming the Model and identifier |
| The record conflicts with an existing one on a unique field | `409` | `detail`: a message naming the Model |

### API description

While the server runs, the API publishes its machine-readable description in OpenAPI format at `/openapi.json` and the interactive documentation built from it at `/docs`. Both are controlled by the `api_documentation` setting.

## Dependencies

- Python 3.14 or later.
- `my-model` and `my-database`, consumed only through their public interfaces (local path dependencies).
- `fastapi` with its standard extras, which supply the HTTP server, and `pyyaml` to read the runtime configuration.

The package is consumed by the Frontend layer through the HTTP API.

## Configuration

The package reads its section of the centralized public runtime configuration, `application.yaml` at the project root. The project root is found by walking up from the current directory, or taken from `TRADING_ASSISTANT_ROOT`. The Backend needs no secret of its own; the Database layer resolves its secrets itself.

The `backend` section:

| Setting | Meaning | Example |
|---|---|---|
| `settings.host` | The address the server listens on. | `127.0.0.1` |
| `settings.port` | The port the server listens on. | `8000` |
| `settings.api_documentation` | Whether the description and documentation are published. | `true` |
| `bindings.model` | The Model package consumed and how. | `package: my_model`, `interface: import` |
| `bindings.database` | The Database package consumed, how, and which Instance every operation uses. Omit `instance` to use the Database's default. | `package: my_database`, `interface: gateway`, `instance: general` |

## Installation

The package is internal and is not published. Install it together with the packages it depends on into the consuming environment:

```bash
uv pip install path/to/model path/to/database path/to/backend
```

Inside the package directory, `uv sync` creates the package's own isolated environment with every dependency, including the Model and Database packages, resolved.

### Starting the server

The storage structure must exist and, normally, the initial data must be applied (see the Database package). Then, from the package directory:

```bash
uv run python -m my_backend serve
```

The server listens on the configured host and port until stopped with an interrupt. `fastapi dev` from the same directory starts a reloading development server on the framework's default port instead.

## Usage

Set `BACKEND_URL` to where the server listens (default `http://127.0.0.1:8000`).

Enter and manage a currency:

```python
import os
import httpx

base = os.environ.get("BACKEND_URL", "http://127.0.0.1:8000")
with httpx.Client(base_url=base) as api:
    created = api.post("/currencies", json={"name": "Example Dollar", "code": "EXD", "symbol": "E$"})
    assert created.status_code == 201
    record = created.json()
    assert record["decimal_digits"] == 2  # default applied

    assert api.get(f"/currencies/{record['id']}").json() == record
    assert any(c["id"] == record["id"] for c in api.get("/currencies").json())

    updated = api.patch(f"/currencies/{record['id']}", json={"name": "Example Dollar (renamed)"})
    assert updated.status_code == 200 and updated.json()["code"] == "EXD"

    assert api.delete(f"/currencies/{record['id']}").status_code == 204
    assert api.get(f"/currencies/{record['id']}").status_code == 404
```

Credentials are write-only:

```python
import os
import httpx

base = os.environ.get("BACKEND_URL", "http://127.0.0.1:8000")
with httpx.Client(base_url=base) as api:
    created = api.post("/users", json={
        "name": "Example", "username": "example", "password": "s3cret", "api_key": "k3y",
    })
    assert created.status_code == 201
    user = created.json()
    assert "password" not in user and "api_key" not in user

    renamed = api.patch(f"/users/{user['id']}", json={"name": "Example (renamed)"})
    assert renamed.status_code == 200  # the password is unchanged

    assert api.delete(f"/users/{user['id']}").status_code == 204
```

Distinguish outcomes:

```python
import os
import httpx

base = os.environ.get("BACKEND_URL", "http://127.0.0.1:8000")
with httpx.Client(base_url=base) as api:
    invalid = api.post("/currencies", json={"name": "Bad", "code": "ABCD"})
    assert invalid.status_code == 422
    assert any("code" in error["loc"] for error in invalid.json()["detail"])

    assert api.get("/currencies/999999").status_code == 404

    description = api.get("/openapi.json").json()
    assert "/currencies/{key}" in description["paths"]
```
