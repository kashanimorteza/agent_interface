# backend

## Purpose and Boundaries

`backend` executes application Behaviour for the Trading Assistant and
publishes the external HTTP API through which the Frontend (and any other
consumer) reaches every domain entity. It turns the shared `my_model`
definitions and the `my_database` persistence layer into what the
application actually does.

`backend` owns:

- application Behaviour and the rules that depend on operation context;
- the route from that Behaviour to persistence;
- the external API contract, including its machine-readable description.

`backend` does **not** own domain-model meaning (`my_model`), physical
persistence (`my_database`), user-interface presentation, or how it is
started and connected at runtime (Platform).

## Internal Layers

```
API  →  Logic  →  Data Access  →  Database Interface
```

- **API** (`backend.api`) decodes HTTP requests, invokes Logic, and
  serializes results. It owns no Behaviour and never calls Data Access or
  Database directly.
- **Logic** (`backend.logic`) implements what the application does: one
  separately defined unit per domain Model, built on a shared baseline.
- **Data Access** (`backend.data_access`) is the *only* module that imports
  `my_database`. Every other module reaches persistence exclusively through
  it.

## Installation and Startup

```bash
uv sync
fastapi dev            # development server with reload
fastapi run            # production server
```

Before first use, `my_database`'s migration history must be applied and, for
a fresh environment, seeded — see `my_database`'s own documentation. Backend
has no runtime configuration or secrets of its own; it consumes whatever
Instance `my_database` resolves as its default.

## The Public API

Every domain Model is reachable at its own resource path with the standard
operations:

| Method | Path | Operation |
| --- | --- | --- |
| `POST` | `/{resource}` | create |
| `GET` | `/{resource}/{id}` | get |
| `GET` | `/{resource}` | list (`limit`, `offset`) |
| `PATCH` | `/{resource}/{id}` | update (partial) |
| `DELETE` | `/{resource}/{id}` | delete |
| `POST` | `/{resource}/{id}/status` | enable or disable |

The full machine-readable description (OpenAPI) is published at
`/openapi.json`, and interactive documentation at `/docs`.

### Example: create, read, update, delete

```python
import httpx

client = httpx.Client(base_url="http://localhost:8000")

created = client.post("/brokers", json={"name": "Example Broker", "user_id": 1})
broker = created.json()  # {"id": 1, "name": "Example Broker", "user_id": 1, "status": True, "description": None}

fetched = client.get(f"/brokers/{broker['id']}").json()
updated = client.patch(f"/brokers/{broker['id']}", json={"description": "Updated"}).json()
client.delete(f"/brokers/{broker['id']}")  # 204 No Content
```

### Example: a Credential field is write-only

```python
created = client.post(
    "/users",
    json={"name": "Ada", "username": "ada", "password": "change-me", "api_key": "change-me"},
)
body = created.json()
assert "password" not in body
assert "api_key" not in body
```

A Credential field is accepted on create or update but never appears in a
response body or in a response schema in the published OpenAPI description.

### Example: enable or disable a record

```python
platform = client.post("/trading-platforms", json={"name": "Example", "code": "example"}).json()
client.post(f"/trading-platforms/{platform['id']}/status", json={"action": "disable"})
```

### Example: failure handling

| Situation | HTTP status |
| --- | --- |
| Record does not exist | `404` |
| Payload violates the Model's own rules | `422` |
| A uniqueness or referenced-record constraint is violated | `409` |
| An operation is unavailable for this Model (for example, status on a Model without one) | `405` |

```python
response = client.get("/brokers/999999")
assert response.status_code == 404

response = client.post("/brokers", json={"name": "", "user_id": 1})
assert response.status_code == 422
```

## Application Behaviour and Model Logic

Every domain Model has its own Logic unit under `backend.logic` (for
example, `backend.logic.broker.BrokerLogic`), reachable through
`backend.logic.REGISTRY[model_type]`. Every unit currently relies on the
shared `ModelLogic` baseline (create/get/list/update/delete/status); a Model
that later needs behaviour beyond CRUD gets it added to its own unit without
touching any other Model's Logic.

```python
import my_model as m
from backend.logic import REGISTRY

broker_logic = REGISTRY[m.Broker]
broker = broker_logic.create(name="Example Broker", user_id=1)
```

A partial update's validation considers the resulting complete domain
state — updating a field to a value that would leave the record invalid is
rejected even though other fields were not touched.

## Reaching Database Only Through Data Access

`backend.data_access` is the sole translation point to `my_database`. It
forwards `create`, `get`, `list_records`, `update`, `delete`, and
`set_status` for any Model type, and exposes `transaction()` to group
related calls into one commit-or-rollback unit:

```python
from backend import data_access
import my_model as m

with data_access.transaction() as tx:
    a = data_access.create(m.AccountGroup, unit=tx, user_id=1, name="Group A")
    b = data_access.create(m.AccountGroup, unit=tx, user_id=1, name="Group B")
# both committed together; an exception before the block exits rolls both back
```

No other Backend module imports `my_database`.

## Runtime Bindings

Backend currently requires no cross-layer runtime Binding beyond the
Database Instance `my_database` resolves on its own; Platform will deliver
any future Binding (for example, a different selected Instance) through the
selected Launch without Backend discovering it independently.
