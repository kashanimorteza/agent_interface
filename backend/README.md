# my_backend

## Purpose and boundaries

The application Backend for the Trading Assistant. It exposes every resolved
domain Model's standard operations through one HTTP API, backed by a
dedicated Logic unit per Model and a single generic Data Access translation
to the Database package.

Backend is formed from three internal layers, in this dependency direction:

`API` (this package's public surface) → `Logic` (per-Model application
behaviour) → `Data Access` (the only boundary that reaches Database).

Only the API layer — the running application — is meant to be imported or
reached by a consumer. Internal modules are named with a leading underscore
to signal that they are not part of the public interface.

Backend owns application behaviour, the route from behaviour to persistence,
and the external API contract. It does not own domain-model meaning
(`my_model`), physical persistence (`my_database`), or user-interface
presentation.

## Public interface

An import surface, exposing:

- `app` — the runnable API application. A process brings the Target online
  by serving this application through an ASGI server.

Every resolved Model gets its own resource under the API, offering the
operations that Model supports:

- `POST /<resource>` — create
- `GET /<resource>` — list
- `GET /<resource>/{id}` — get
- `PATCH /<resource>/{id}` — partial update
- `DELETE /<resource>/{id}` — delete
- `POST /<resource>/{id}/status?action=enable|disable` — only for a Model
  declaring a `status` field

A machine-readable description of every operation and data shape is
published at `/openapi.json` (interactive docs at `/docs`). A credential
field a Model declares (such as a password or API key) is accepted only in a
create or update request body; it never appears in a response or in the
published description's response schemas.

## Dependencies

- Python (this package's declared `requires-python`)
- [FastAPI](https://fastapi.tiangolo.com/) for the API layer and its OpenAPI documentation
- `my_model`, the shared domain Model package, as a local dependency
- `my_database`, the persistence package, as a local dependency (reached only through Data Access)

## Configuration

None of its own. Backend has no settings or secrets; it consumes whatever
Database Instance `my_database` resolves as its default.

## Installation and startup

A local workspace package, added as an editable path dependency by whatever
process launches it. To run it directly during development:

```
uv run fastapi dev src/my_backend/_api.py
```

## Usage examples

```python
from my_backend import app
# Serve `app` with any ASGI server (e.g. uvicorn) to bring the API online.
```

```
POST /brokers            {"name": "FxPro", "user_id": 1}
GET  /brokers
GET  /brokers/1
PATCH /brokers/1         {"description": "updated"}
POST /brokers/1/status?action=disable
DELETE /brokers/1
```
