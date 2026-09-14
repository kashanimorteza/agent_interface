# database

The persistence boundary for the Trading Assistant Target. `database` maps every persistent `model` Domain Definition to storage, owns the Storage Adapter and Instance Registry, and publishes one generic, Model-driven Database Interface. Consumers (Backend) never see SQL, a session, or a connection.

## Public Interface

```python
from database import (
    NotFoundError,
    UnknownModelError,
    create,
    default_instance,  # Instance Registry
    delete,
    get_by_id,
    list_,
    list_instances,
    seed_initial_data,  # Target's declared Initial Data
    set_active,  # generic, Model-driven
    transaction,  # Transaction boundary
    update,
)
```

Every one of the 15 persistent Domain Definitions (`model.User`, `model.Account`, `model.Position`, …) works through these same generic calls — there is no per-Model function.

```python
from model import Currency
from database import create, get_by_id, transaction

with transaction() as tx:
    row = create(Currency(user_id=1, code="USD"), session=tx)
    same = get_by_id(Currency, row.id, session=tx)
```

Calling a generic operation without `session=` opens and commits its own one-operation Transaction. Passing `session=tx` (from an open `transaction()` block) groups multiple operations into one atomic commit-or-rollback unit.

## Setup

```bash
cd database
uv sync
export DATABASE_ENCRYPTION_KEY="$(python3 -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())')"
uv run alembic upgrade head
uv run python -c "from database import seed_initial_data; print(seed_initial_data())"
```

**`DATABASE_ENCRYPTION_KEY` must stay the same for the life of the database.** It is the Fernet key protecting every reversible ("encrypted") credential field (`Instance.password`, `Instance.api_key`, `Account.password`). Losing it makes that data permanently unreadable; it is never committed to the repository or written to any Interface record — supply it as a real runtime secret.

`seed_initial_data()` prints the plaintext of every credential it generated (the initial Admin user's password and API key, the seed Instance's technical credentials, the seed Account's password) so an operator can record them once. Nothing after that call can recover them — `password`-mode credentials are one-way hashed, and re-running `seed_initial_data()` is a no-op once the records already exist.

## Architecture

- **`foundation.py`** — the shared storage-mapping base (`StorageBase`), the `UTCDateTime` column type (every stored instant is timezone-aware, normalized to UTC), and the credential at-rest mechanism: `protect_credential` / `reveal_credential` / `verify_credential`, driven by the `credential_storage` metadata each Domain Definition in `model` declares on its own credential fields (`hash` → PBKDF2-HMAC-SHA256, one-way; `encrypted` → Fernet, reversible).
- **`mapping/`** — one SQLAlchemy ORM class per persistent Domain Definition, grouped the same way as `model`'s own modules (`identity`, `reference`, `accounts`, `risk`, `actions`). Each class registers itself against its Pydantic Model type in `mapping.MAPPINGS`, which is what lets the Database Interface stay generic instead of one implementation per Model.
- **`convert.py`** — the generic Pydantic ⇄ ORM conversion every operation shares, including automatic credential protection on write and reveal-or-mask on read.
- **`adapter.py`** — the Storage Adapter: resolves `database.yaml`, builds the SQLite engine (enabling `PRAGMA foreign_keys=ON`, since SQLite does not enforce foreign keys by default), and the Instance Registry (`list_instances`, `default_instance`) — no connection or secret is ever returned from it.
- **`interface.py`** — the generic `create` / `get_by_id` / `list_` / `update` / `delete` / `set_active` operations and the `transaction()` context manager.
- **`seed.py`** — seeds the Target's declared Initial Data in dependency order, idempotently.
- **`migrations/`** — Alembic. `migrations/env.py` resolves its engine and target metadata from this package (`database.adapter.get_engine`, `database.foundation.StorageBase.metadata`), not from `alembic.ini`.

The Database Interface's optional capability-restricted command route (for operations no standard call can express) is not implemented — nothing in the current Target needs it.

## Running a migration

```bash
uv run alembic revision --autogenerate -m "message"
uv run alembic upgrade head
```

**Known step:** if a new or changed column uses a custom type (currently only `UTCDateTime`, used by `Position.date`), Alembic's autogenerate does not add the import it needs. Add `import database.foundation` to the generated revision file before applying it — the generator will otherwise fail with a `NameError` naming the missing module.

## Verification

```bash
uv run pytest       # 25 tests, run against an isolated in-memory SQLite database per test
uv run ruff check .
uv run ruff format --check .
uv run pyright
uv run alembic check   # confirms the applied migration history matches the current mapping exactly
```

## Scope exclusions

Per the Target's Development section, this Component has no HTTPS/TLS, authentication/authorization, logging, or custom error-handling machinery. Constraint and referential violations surface as SQLAlchemy's own `IntegrityError`; a missing row from `update`/`delete` raises this package's `NotFoundError`.
