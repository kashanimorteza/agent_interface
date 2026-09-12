# my_backend

Application Behaviour and the public HTTP API for the Trading Assistant Target, built on the
shared `my_model` logical Model package and the `my_database` persistence package.

## Purpose and boundaries

`my_backend` implements what the application does and publishes the API through which external
consumers reach that Behaviour. It owns no domain-model meaning (that belongs to `my_model`), no
physical persistence (that belongs to `my_database`), and no presentation (that belongs to
Frontend).

## The four internal layers

```
API Interface  ->  Logic  ->  Model Interface   (shared domain meaning)
                          ->  Database Interface (persistence)
```

- **Model Interface** (`my_backend._model_interface`) is Logic's only route to shared Model types
  and Credential markers.
- **Database Interface** (`my_backend._database_interface`) is Logic's only route to persistence;
  it translates a requested operation or related-operation group into the public `my_database`
  interface and its transaction boundary.
- **Logic** (`my_backend.logic`) implements application Behaviour: one distinct Model Logic unit
  per shared Model, offering create, get, list, update, delete, and status wherever its Model
  supports them.
- **API Interface** (`my_backend.api`, `my_backend.app`) is Logic's only external boundary: an
  HTTP API built with FastAPI that validates transport shape, invokes Logic, and maps outcomes to
  distinguishable HTTP responses.

No layer bypasses the layer responsible for the next boundary.

## Installation and startup

```bash
cd my_backend
uv sync
uv run fastapi dev my_backend/app.py   # development server with reload
uv run fastapi run my_backend/app.py   # production server
```

`my_backend` requires an already-migrated database; run `uv run alembic upgrade head` inside
`my_database/` first.

## The public API Interface and its published description

Every operation is reached over HTTP. The application publishes a machine-readable OpenAPI
description at `/openapi.json` (and interactive documentation at `/docs`), always kept consistent
with the implemented routes because it is generated directly from them.

Every Model gets its own resource collection, for example `/users`, `/instances`,
`/trailing-rules`. Each supports:

| Method | Path | Operation |
| --- | --- | --- |
| POST | `/<resource>` | create |
| GET | `/<resource>/{id}` | get |
| GET | `/<resource>` | list |
| PATCH | `/<resource>/{id}` | update (partial) |
| DELETE | `/<resource>/{id}` | delete |
| POST | `/<resource>/{id}/status` | status (`{"action": "enable"|"disable"}`) |

## Organization of Model Logic and Target Behaviour

Every shared Model has its own Model Logic unit under `my_backend/logic/`, sharing a common base
(`my_backend.logic._base.ModelLogic`) for the standard operations while remaining free to extend
or override any of them. For example, `my_backend.logic.instance` extends the base to enforce the
Target's own declared rule that the selected Trading Platform determines which of an Instance's
connection fields are required — a rule that depends on the referenced Trading Platform's own
data, so neither the Model package nor the Database package enforces it themselves.

## Configuration and runtime Bindings

`my_backend` declares no configuration or secrets of its own; it reaches persistence entirely
through `my_database`'s own runtime configuration and Instance Registry. No Database internal
(engine, connection, ORM object, or schema) is ever exposed through this package's interface.

## Credential protection

A field Model Interface marks as a Credential is accepted only as write-only input on the create
and update operations that need it, and is excluded from every response and every published
response schema — read from Model Interface's own Credential markers, never inferred from a field
name. Database owns how the value is protected at rest; Backend never redefines that.

## Usage examples

Start a test client against the application:

```python
from fastapi.testclient import TestClient
from my_backend import app

client = TestClient(app)
```

Create a record, observing the Credential fields are write-only input, absent from the response:

```python
response = client.post(
    "/users", json={"name": "Admin", "username": "admin", "password": "secret", "api_key": "key"}
)
assert response.status_code == 201
user = response.json()
assert "password" not in user
assert "api_key" not in user
```

Get one record by its identifier, and observe the not-found outcome for a missing one:

```python
fetched = client.get(f"/users/{user['id']}")
assert fetched.status_code == 200

missing = client.get("/users/999999")
assert missing.status_code == 404
```

List records:

```python
listed = client.get("/users")
assert listed.status_code == 200
assert len(listed.json()) == 1
```

Update a record, preserving partial-update semantics:

```python
updated = client.patch(f"/users/{user['id']}", json={"description": "a note"})
assert updated.status_code == 200
body = updated.json()
assert body["name"] == "Admin"  # omitted from the patch: unchanged
assert body["description"] == "a note"  # supplied in the patch: replaced
```

Enable or disable a Model that declares a `status` field:

```python
disabled = client.post(f"/users/{user['id']}/status", json={"action": "disable"})
assert disabled.status_code == 200
assert disabled.json()["status"] is False
```

Delete a record and observe the not-found result afterward:

```python
deleted = client.delete(f"/users/{user['id']}")
assert deleted.status_code == 204
assert client.get(f"/users/{user['id']}").status_code == 404
```

Handle a validation failure and a uniqueness conflict:

```python
invalid = client.post("/currencies", json={"user_id": 1, "code": "US"})  # code must be 3 characters
assert invalid.status_code == 422

second_user = client.post(
    "/users", json={"name": "Admin", "username": "admin2", "password": "x", "api_key": "y"}
)
another = client.post(
    "/users", json={"name": "Admin", "username": "admin3", "password": "x", "api_key": "y"}
)
assert second_user.status_code == 201
assert another.status_code == 409
```

Handle the Target-declared platform-required-field failure:

```python
platform = client.post(
    "/trading-platforms", json={"name": "MetaTrader 5", "code": "metatrader_5"}
).json()
bad_instance = client.post(
    "/instances",
    json={
        "user_id": user["id"],
        "name": "MT",
        "trading_platform_id": platform["id"],
        "ip": "127.0.0.1",
        "username": "trader",
        # password omitted: MetaTrader 5 requires it
    },
)
assert bad_instance.status_code == 422
```
