# my_backend

The application layer for the Trading Assistant. It turns the shared domain Model and the Database public interface into an external HTTP API, enforcing the rules that depend on application context and exposing the result through a documented contract.

## Purpose and boundaries

`my_backend` is one independent package built from four internal layers:

```text
Model package ── Model Interface ──┐
                                   ├── Logic ── API Interface ── External consumers
Database ─────── Database Interface┘
```

- **Model Interface** (`my_backend._model_interface`) — the only route to shared Model definitions.
- **Database Interface** (`my_backend._database_interface`) — the only translation to the public Database interface, including its transaction boundary.
- **Logic** (`my_backend.logic`) — application Behaviour: one unit per shared Model (create/get/list/update/delete/status), built on a shared reusable baseline.
- **API Interface** (`my_backend.api`, `my_backend._app`) — the external HTTP boundary: FastAPI routers, request/response schemas, and the machine-readable API contract.

`my_backend` does not own domain-model meaning (that belongs to `my_model`), physical persistence (that belongs to `my_database`), or presentation.

## Installation and startup

```bash
cd my_backend
uv sync
uv run fastapi dev src/my_backend/_app.py   # interactive local server
```

The package's documented public startup boundary is `create_app()`:

```python
import my_backend

app = my_backend.create_app()
```

Any ASGI server (uvicorn, hypercorn, `fastapi run`) can serve `app`.

## The API

Every one of the 15 domain entities gets the same operations, mounted under its own path prefix (e.g. `/users`, `/brokers`, `/trading-platforms`):

| Method | Path | Operation |
| --- | --- | --- |
| POST | `/{resource}` | create |
| GET | `/{resource}/{id}` | get by identifier |
| GET | `/{resource}` | list (`limit`, `offset` query parameters) |
| PATCH | `/{resource}/{id}` | partial update |
| DELETE | `/{resource}/{id}` | delete |
| POST | `/{resource}/{id}/status?action=enable\|disable` | enable/disable |

Interactive documentation is served at `/docs`; the machine-readable OpenAPI contract is at `/openapi.json`.

## Example: creating and reading a Broker

```python
from fastapi.testclient import TestClient

import my_backend

client = TestClient(my_backend.create_app())

user = client.post(
    "/users", json={"name": "Ada", "username": "ada", "password": "x", "api_key": "y"}
).json()

broker = client.post(
    "/brokers", json={"name": "Example Broker", "user_id": user["id"]}
).json()
client.get(f"/brokers/{broker['id']}")  # 200
client.patch(f"/brokers/{broker['id']}", json={"description": "Updated"})
client.post(f"/brokers/{broker['id']}/status", params={"action": "disable"})
client.delete(f"/brokers/{broker['id']}")  # 204
```

## Partial updates

`PATCH` only changes the fields actually present in the request body — an omitted field is left untouched, while an explicit `null` clears it (where the domain permits `null` for that field):

```python
client.patch(
    f"/currencies/{currency_id}", json={"country": None}
)  # clears country only
```

## Failure handling

| Situation | Response |
| --- | --- |
| Record not found | `404` |
| A uniqueness rule or a reference to a nonexistent record is violated | `409` |
| Request body fails transport-level validation (missing/invalid/unknown field) | `422` |
| `status` requested on a Model that declares no `status` field | `400` |

Error responses never include a credential value, a stack trace, or persistence internals.

## Credential protection

A Model field marked as a credential (e.g. `User.password`, `User.api_key`, `Instance.password`, `Instance.api_key`, `Account.password`) is **write-only**: it appears in the Create and Update request schemas so a caller can supply it, and is completely absent from every Read/response schema and from OpenAPI's response definitions. It is never echoed back, logged, or included in any error payload.

## Non-secret configuration and runtime Bindings

`my_backend` itself declares no environment variables. It calls through to `my_database`, which resolves its own configuration (see `my_database`'s `README.md`, notably `MY_DATABASE_ENCRYPTION_KEY`). No secret value is read or embedded by this package directly.

## Boundary with Model, Database, and Platform

- **Model** (`my_model`) is reached only through Model Interface; Logic never imports `my_model` directly.
- **Database** (`my_database`) is reached only through Database Interface, including its transaction boundary; Logic never imports `my_database` directly and API Interface never reaches persistence directly.
- **Platform** delivers runtime Bindings (should any be required) through the selected Launch; this package does not manage deployment topology.

## Dependencies

- [FastAPI](https://fastapi.tiangolo.com/) (`fastapi[standard]`) — the API framework.
- [Pydantic](https://docs.pydantic.dev/) `2.x` — request/response schema validation.
- `pydantic-settings` — reserved for typed non-secret configuration, not currently required.
- Development-only: `ruff`, `pyright`, `pytest`, `httpx` (test client transport).
