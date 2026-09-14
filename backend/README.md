# Backend

The `backend` package is the Trading Assistant's Backend Component: the executable
application layer that implements the Target's Behaviour and publishes the API through
which external consumers reach it. It follows Hexagonal Architecture with four explicit
parts — **API Interface**, **Logic**, **Model Interface**, and **Database Interface** —
plus a shared **Logic Foundation** every Model Logic unit builds on.

Backend owns application Behaviour only. It never redefines domain meaning (`model`) or
persistence (`database`), and it exposes no importable Python API of its own — its only
public boundary is the running HTTP API, reached through its official executable entry
point.

## Public surface

External consumers reach Backend only over HTTP, through the versioned API — there is no
`from backend import ...` surface to import. Start it with:

```bash
fastapi run
```

- **Every Domain Definition** the Target defines — User, Trading Platform, Instance,
  Currency, Broker, Asset, Account Group, Account, Trailing Group, Trailing Rule,
  Partial Group, Partial Rule, Action Group, Action, Position — is reachable under
  `/{api_version}/<resource>` (for example `/v1/trading-platform`), with:
  - `POST /{resource}` — create
  - `GET /{resource}/{id}` — read by identifier
  - `GET /{resource}` — bounded, cursor-paginated list
  - `GET /{resource}/search` — bounded, cursor-paginated search by declared Model fields
  - `PUT /{resource}/{id}` — partial update
  - `POST /{resource}/{id}/enable` and `.../disable`
  - `DELETE /{resource}/{id}` — delete by identifier
- **`GET /health`** — reports the process is running, independent of dependency state.
- **`GET /ready`** — reports ready only once required configuration and Database are
  confirmed usable.
- **`GET /openapi.json`**, **`/docs`** — the machine-readable API contract, always
  generated from the live route definitions (never hand-maintained, never able to drift).
- **Authentication** — every operation requires a valid API key in the `X-API-Key`
  header, checked against `User.api_key`.

Every response and every documented `...Read` schema excludes credential fields
(`password`, `api_key`) entirely — never even a redacted placeholder appears in a
response body.

## Setup

Requires Python 3.13+ and [uv](https://docs.astral.sh/uv/). `backend` depends on the
sibling `model` and `database` packages by relative path.

```bash
cd backend
uv sync
```

## Installation

Backend is deployed and run as a standalone service, not installed as a library
dependency of another Component.

## Configuration

Backend defines and validates its own Runtime Configuration contract (environment
variables prefixed `BACKEND_`), and depends on Database's own component-root resolution:

| Variable | Required | Default | Purpose |
|---|---|---|---|
| `BACKEND_CORS_ALLOWED_ORIGINS` | **Yes** | — | JSON array of allowlisted CORS origins, e.g. `["https://app.example.com"]`. No permissive default is supplied; a wildcard (`["*"]`) is accepted but is never combined with credentialed access. |
| `BACKEND_HOST` | No | `0.0.0.0` | Bind address. |
| `BACKEND_PORT` | No | `8000` | Bind port. |
| `BACKEND_API_VERSION` | No | `v1` | Published API version path segment. |
| `BACKEND_DATABASE_INSTANCE` | No | `general` | The Database Instance Backend persists through. |
| `BACKEND_REQUEST_TIMEOUT_SECONDS` | No | `5.0` | Finite timeout on every persistence interaction. |
| `BACKEND_MAX_RETRY_ATTEMPTS` | No | `3` | Bound on automatic retry for a safe/idempotent persistence operation. |
| `BACKEND_SHUTDOWN_TIMEOUT_SECONDS` | No | `30.0` | Graceful shutdown boundary. |
| `DATABASE_COMPONENT_ROOT` | **Yes**, for this deployment topology | — | Points Database (a non-editable dependency here) at its actual component root — the sibling `database/` directory — so it finds `database.yaml`, `data/`, and `.secrets/`. See the `database` package's own README. |

A missing required value fails startup immediately (before readiness is ever reported),
not later at first use.

## Use

Storage structure must already be migrated (see the `database` package's own README) and
initial data seeded before Backend can authenticate anyone:

```bash
# One-time setup, from the database/ directory:
uv run alembic upgrade head
uv run python -c "
from database import Database, seed_initial_data
creds = seed_initial_data(Database())
print(creds)  # capture 'admin_api_key' now — it is never recoverable again
"
```

Then run Backend:

```bash
export BACKEND_CORS_ALLOWED_ORIGINS='["https://app.example.com"]'
export DATABASE_COMPONENT_ROOT=../database
fastapi run
```

```bash
# Authenticated requests use the seeded Admin's API key.
curl -H "X-API-Key: $ADMIN_API_KEY" http://localhost:8000/v1/user

curl -X POST -H "X-API-Key: $ADMIN_API_KEY" -H "Content-Type: application/json" \
  -d '{"name": "MetaTrader 5", "code": "metatrader_5"}' \
  http://localhost:8000/v1/trading-platform
```

## Verification

From the `backend` directory, with the development dependencies installed and
`DATABASE_COMPONENT_ROOT` set to the sibling `database/` directory:

```bash
uv run pytest      # unit and integration tests across every Task in this phase:
                    # Model/Database Interfaces, the Logic Foundation, every Model
                    # Logic unit, authentication/authorization, the API contract,
                    # pagination, CORS, error mapping, lifecycle, observability,
                    # the public boundary, and this README
uv run ruff check . && uv run ruff format --check .
uv run pyright
```

## Troubleshooting

- **`401 Unauthorized` on every request** — no valid `X-API-Key` header was sent, or the
  Database Instance has no active User with that `api_key`. Re-run `seed_initial_data`
  only if you did not capture the Admin's key the first time (it is never recoverable
  otherwise); see the `database` package's Troubleshooting section.
- **`503` from `GET /ready`** — required configuration or Database is not yet usable;
  check the deployment logs from startup, which fail fast on a missing required value.
- **`FileNotFoundError` mentioning `database.yaml` inside `site-packages`** — set
  `DATABASE_COMPONENT_ROOT` to the sibling `database/` directory; Database's non-editable
  install here cannot find its own configuration relative to itself.
- **`422` on a request that looks correct** — either the request body does not match the
  Model's declared fields (check `/openapi.json` for the exact `...Create`/`...Update`
  schema) or a list request named a query parameter other than `cursor`/`limit`, which
  this phase does not allowlist.
- **A credential value never appears in a response, even right after creating it** —
  expected: Backend excludes every credential field from every response schema
  entirely, per Backend Principle 11.

## Consequential implementation choices

- **Authentication mechanism**: API-key header (`X-API-Key`), verified through
  Database's `verify_credential` (added to Database's public interface specifically to
  support this — see the `database` README). The Target defines no other identity
  mechanism.
- **Authorization**: the Target defines no differentiated permission model for this
  phase, so any authenticated identity is authorized for every operation Backend
  exposes; the decision is still made explicitly in Logic (`backend.logic.auth.authorize`)
  rather than skipped.
- **Pagination**: cursor-based, ordered by ascending `id` (a stable, monotonic natural
  cursor), rather than a separately maintained cursor token, since Database's own list
  operation has no independent ordering concept to expose.
- **Filtering and sorting**: no Field is allowlisted for either in this phase — the
  Target states no filter or sort requirement — so any query parameter beyond
  `cursor`/`limit` is rejected rather than silently ignored.
- **Request correlation** is implemented as a raw ASGI middleware rather than the
  `@app.middleware("http")` / `BaseHTTPMiddleware` helper: in this environment's
  Starlette, that helper re-raises an exception past a registered exception handler
  before a response is observed, which would have defeated Application Outcome mapping.
