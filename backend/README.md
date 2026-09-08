# Backend — the application layer of Trading Assistant

`my_backend` is what the application *does*. It takes the domain definitions the
Model layer publishes, keeps the rules that depend on an operation rather than
on values alone, reaches stored data only through the Database layer's published
boundary, and offers all of it as one HTTP contract.

Unlike the two layers beneath it, this one is normally met as a running service
rather than imported. The contract is the thing to depend on.

## Purpose and boundaries

**This layer does:** give every kind of data the project defines its own unit of
behaviour; judge each operation against the state it would produce, including
for a change that states only some fields; group related data operations when
they must hold together; and publish one contract — with a machine-readable
description of itself — through which all the defined data can be entered and
managed.

**This layer does not:** decide what the domain means, or how it is stored.
Fields, connections and rules belong to the Model layer; tables, constraints and
the recorded structural history belong to the Database layer. It owns no
persistence of its own, and it never reaches an engine, a connection or a query.

## Public interface

The contract is HTTP. In-process, this package publishes only how to build the
application and the refusals a caller can meet:

```python
from my_backend import create_app, NotFound, Invalid, Conflict, Unsupported

app = create_app()
```

### The contract

For every kind of data the project defines — users, currencies, trading
platforms, brokers, account groups, accounts, assets, trailing groups and rules,
partial groups and rules, action groups, actions and positions — the same five
operations, under a path named for that kind of data:

| Operation | Request |
|---|---|
| List | `GET /currencies/?limit=&offset=&order_by=` |
| Create | `POST /currencies/` |
| Get | `GET /currencies/{identifier}` |
| Change | `PATCH /currencies/{identifier}` |
| Remove | `DELETE /currencies/{identifier}` |

A change states only the fields it means to change; anything left out is left
alone. Where a kind of data declares an active state, one more operation
enables or disables it, and those two actions are the only ones it accepts:

```
POST /currencies/{identifier}/status     {"action": "enable"}
```

A kind of data that declares no such field does not offer that operation at all.

`GET /health` says whether the layer is answering.

### What comes back

Every shape the contract carries is derived from the shared definition it
belongs to, so a field means here what it means everywhere else. **A credential
never comes back.** A field the definitions mark as a credential may be sent —
that is how a password is set — and is absent from every response, from every
response shape in the description, and from every refusal.

### Refusals

| Refusal | Answer | What it means |
|---|---|---|
| `NotFound` | 404 | The record is not there |
| `Invalid` | 422 | The resulting state breaks a rule |
| `Conflict` | 409 | It cannot stand beside what is stored |
| `Unsupported` | 400 | This kind of data does not offer that |
| `Misconfigured` | 500 | The layer was not given what it needs |

Each answer carries the reason and never the value that was rejected.

### The description of the contract

The contract describes itself, in a machine-readable form produced by the
boundary that defines it: `/openapi.json`, with a readable rendering at `/docs`.
Both can be turned off in this layer's settings.

## Internal, and not yours to depend on

`api` (the boundary, the shapes, the routes), `logic` (the per-definition units
of behaviour) and `data_access` (the single route to stored data) are internal.
Reach the layer through its HTTP contract, or through `create_app`.

## Dependencies

Python 3.14, the shared `my_model` layer, the `my_database` layer, FastAPI
0.141.1 (with its standard extras, including Uvicorn 0.52.4) and PyYAML 6.0.3.

The persistence layer is taken from where it lives rather than as a copy, so it
keeps its own settings and its own stored data.

## Configuration

`backend.yaml`, beside this file, holds the settings this layer owns: where it
answers, whether it describes itself and where, and how much a listing returns.
This layer requires no secret of its own.

Cross-layer bindings live in `application.yaml` at the project root. That is
where it is decided which stored identity the application works with; naming one
the Database layer does not publish stops this layer at startup with that
reason, rather than quietly working somewhere else.

## Installation and startup

```bash
cd backend
uv sync
uv run my-backend
```

That reads `backend.yaml` and serves on the address it names. For development
with reload:

```bash
uv run fastapi dev
```

The Database layer must have its structure applied first — see its own
description — or the first request will be refused.

## Usage

```bash
curl http://127.0.0.1:8000/currencies/

curl -X POST http://127.0.0.1:8000/currencies/ \
  -H 'content-type: application/json' \
  -d '{"name": "Swedish Krona", "code": "SEK", "symbol": "kr", "decimal_digits": 2}'

curl -X PATCH http://127.0.0.1:8000/currencies/9 \
  -H 'content-type: application/json' \
  -d '{"symbol": "SEK"}'

curl -X POST http://127.0.0.1:8000/currencies/9/status \
  -H 'content-type: application/json' \
  -d '{"action": "disable"}'
```

In the same process, without HTTP:

```python
from fastapi.testclient import TestClient
from my_backend import create_app

client = TestClient(create_app())
client.get("/assets/").json()
```
