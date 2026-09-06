# Trading Assistant — Backend Component

The Backend executes application Behaviour and publishes the HTTP API of Trading Assistant. It is a
FastAPI application with three layers:

- **API** (`trading_backend.api`, `trading_backend.main`) — the external HTTP boundary: request
  validation, Pydantic schemas derived from the shared Model specification, error mapping, and the
  OpenAPI description.
- **Logic** (`trading_backend.logic`) — one Logic unit per shared Model with the standard operations
  create, get, list, update, and delete, validated against the shared specification.
- **Data Access** (`trading_backend.data_access`) — the only layer that talks to the Database, through
  the `Database` interface of the `trading_database` package.

The Backend never opens the database file, tables, ORM, or migrations directly.

## Installation

```bash
uv sync
```

This installs FastAPI, uvicorn, and the Database package from `../database` as an editable path
dependency. The Database must already be built (`uv run alembic upgrade head` in `database/`).

## Runtime configuration

Variables come from the process environment or an untracked `.env` in this directory (see
`.env.example`). Process environment variables take precedence.

| Variable | Default | Meaning |
| --- | --- | --- |
| `BACKEND_HOST` | `127.0.0.1` | Bind address of the HTTP server. |
| `BACKEND_PORT` | `8000` | Port of the HTTP server. |
| `BACKEND_CORS_ORIGINS` | `http://127.0.0.1:3000,http://localhost:3000` | Comma-separated browser origins allowed to call the API (the Frontend). |

`DATABASE_URL` and `CREDENTIAL_ENCRYPTION_KEY` are read by the Database package from `database/.env`
(or the process environment) and are not configured here.

## Running

Development server with reload:

```bash
uv run fastapi dev src/trading_backend/main.py
```

Server with host and port from the settings above:

```bash
uv run python -m trading_backend
```

Interactive documentation: `http://127.0.0.1:8000/docs`. Machine-readable description:
`http://127.0.0.1:8000/openapi.json` — this is the contract the Frontend generates its types from.

## Resources

Every shared Model is exposed under `/api/<resource>` with the same five operations:

| Operation | Method and path | Status codes |
| --- | --- | --- |
| create | `POST /api/<resource>` | 201, 409 (constraint), 422 (invalid body) |
| list | `GET /api/<resource>?limit=&offset=&order_by=` | 200, 422 (invalid ordering) |
| get | `GET /api/<resource>/{id}` | 200, 404 |
| update | `PATCH /api/<resource>/{id}` (partial body) | 200, 404, 409, 422 |
| delete | `DELETE /api/<resource>/{id}` | 204, 404, 409 (referenced) |

| Model | Resource |
| --- | --- |
| user | `/api/users` |
| currency | `/api/currencies` |
| trading_platform | `/api/trading-platforms` |
| broker | `/api/brokers` |
| account | `/api/accounts` |
| asset | `/api/assets` |
| trailing_group | `/api/trailing-groups` |
| trailing_rule | `/api/trailing-rules` |
| partial_group | `/api/partial-groups` |
| partial_rule | `/api/partial-rules` |
| action_group | `/api/action-groups` |
| action | `/api/actions` |
| position | `/api/positions` |

`order_by` is a comma-separated list of field names; prefix a name with `-` for descending order.
`limit` is 1–500 (default 100) and `offset` is 0 or more.

Credential fields — `user.password`, `user.api_key`, `account.password` — are **write-only**: they are
accepted in create and update bodies, stored by the Database in their resolved at-rest form, and never
returned in responses, response schemas, or error payloads. Validation errors report only the location,
message, and type of each problem, never the submitted values.

Every error response has the shape `{"detail": ...}`.
