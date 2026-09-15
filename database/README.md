# Database

The `database` package is the complete persistence boundary of the Trading Assistant. It maps every persistent [`model`](../model) Domain Definition to durable SQLite storage and exposes one generic public interface through which every other Component reads and writes persistent data — no private adapter, mapping, connection, or configuration file is ever imported directly.

## Public surface

```python
from database import (
    DatabaseInterface,  # the one generic, Model-driven CRUD + Transaction + controlled-command boundary
    StorageAdapter,  # owns Engine connections per Instance; rarely used directly
    InstanceRegistry,  # discover selectable Instances and the default
    ensure_ready,  # verify Migration integrity, apply pending Migrations, confirm no drift
    upgrade_to_head,  # apply every recorded Migration
    downgrade_to_base,  # reverse every recorded Migration (tested rollback path)
    verify_migration_integrity,
    detect_schema_drift,
    portability_report,  # every persistence decision, classified portable vs Engine-specific
)
```

Every persistent Domain Definition supports **create, read, read-by-identifier (`get_by_id`), list, search, update, delete**, and **activation** (`enable`/`disable`, only where the Domain Definition declares `is_active` — every current Domain Definition does) through `DatabaseInterface`. Related operations group into one atomic unit through `DatabaseInterface.transaction()`. A narrow, allow-listed controlled-command route (`execute_command`) exists for operations standard CRUD cannot express; today it supports only `"count"`, and any other name is rejected outright — nothing structural, privileged, connection-administrative, or Migration-related is or ever will be allow-listed.

## Structure

```text
database/
├── database.yaml             # Database's own non-secret runtime config (Engines, Instances, default)
├── alembic.ini, alembic/      # ordered Migration history (the only way storage structure changes)
├── src/database/
│   ├── __init__.py            # Public Interface
│   ├── adapter.py              # Storage Adapter — Engine connections per Instance
│   ├── mapping.py               # generic Model → SQLAlchemy Table derivation + portability ledger
│   ├── migrations.py             # Migration execution, integrity checksums, drift detection
│   ├── credentials.py             # hash / authenticated-encryption at-rest treatment
│   ├── interface.py                # the generic Database Interface, Transaction, controlled commands
│   ├── seed.py                      # repeatable Target Initial Data importer
│   └── registry.py                   # public Instance Registry
└── tests/                               # adapter, mapping, credentials, migrations, interface, seed
```

## Setup

Requires Python 3.14+ and [`uv`](https://docs.astral.sh/uv/).

```bash
cd database
uv sync
```

Installs SQLAlchemy, Alembic, `cryptography` (for encrypted-at-rest credentials), PyYAML, the local `model` package, and the dev tools (`pytest`, `ruff`, `pyright`).

## Configuration

`database.yaml` (committed, non-secret) declares supported Engines and Instances:

```yaml
engines:
  sqlite:
    driver: "sqlite"
instances:
  general:
    name: "Trading Assistant General"
    purpose: "General application data."
    engine: "sqlite"
    database: "trading_assistant_general"
default_instance: "general"
```

SQLite data files live under `database/data/` (not committed; created automatically, restricted to `0600`).

**Encrypted credentials** (`Instance.password`, `Instance.api_key`, `Account.password`) require an encryption key from the runtime environment — never committed:

```bash
export DATABASE_CREDENTIAL_ENCRYPTION_KEY=$(python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
```

`User.password` and `User.api_key` use a one-way hash and need no key. Any operation that touches an encrypted field without this variable set raises `MissingEncryptionKeyError`.

## Use

```python
from database import DatabaseInterface, StorageAdapter, InstanceRegistry, ensure_ready
from model import User

adapter = StorageAdapter()
ensure_ready(
    adapter.engine_for()
)  # verify integrity, apply Migrations, confirm no drift

print(InstanceRegistry(adapter).list_instances())

db = DatabaseInterface(adapter)
# `id` takes any placeholder value; auto-increment always assigns the real one.
created = db.create(
    User(id=0, name="Admin", username="admin", password="secret", api_key="key")
)
print(
    created.id, created.password
)  # password is now the stored hash, never the plaintext

db.list(User)
db.search(User, {"username": "admin"})
db.update(User, created.id, {"description": "updated"})
db.disable(User, created.id)
db.delete(User, created.id)

with db.transaction() as txn:  # grouped operations commit or roll back together
    db.create(User(id=0, name="A", username="a", password="p", api_key="k"), txn=txn)
    db.create(User(id=0, name="B", username="b", password="p", api_key="k"), txn=txn)

db.execute_command("count", model_cls=User, criteria={"is_active": True})
```

## Migrations

Storage structure changes only through recorded Alembic Migrations — never `create_all()` or ad-hoc DDL.

```bash
uv run alembic upgrade head          # apply every pending Migration
uv run alembic downgrade base        # reverse every Migration (tested rollback path)
uv run alembic revision --autogenerate -m "description"   # after changing model/, generate the next Migration
```

After adding a Migration, refresh its recorded integrity checksum:

```bash
uv run python -c "from database.migrations import write_checksum_manifest; write_checksum_manifest()"
```

`ensure_ready()` (called once at startup) verifies that checksum against every Migration file, applies any pending Migration, then confirms the running structure matches the mapping exactly — raising rather than silently proceeding on either integrity failure or drift.

## Seeding Initial Data

```python
from database import DatabaseInterface, StorageAdapter, ensure_ready
from database.seed import seed_initial_data

adapter = StorageAdapter()
ensure_ready(adapter.engine_for())
seed_initial_data(DatabaseInterface(adapter))
```

Imports every Target-declared Initial Data record (the `Admin` user, both Trading Platforms, the `MetaTrader` Instance, all 8 Currencies, the `FxPro` Broker and its 4 Assets, the default Account/Trailing/Partial/Action Groups, `Acc-1`, and the default Action) in dependency order, inside one Transaction. Safe to run repeatedly: an already-present record (matched by its natural key — e.g. `username` for `User`, `(broker_id, symbol)` for `Asset`) is left untouched, never duplicated. Every `"Generate securely"` credential (`User.password`/`api_key`, `Instance.password`/`api_key`, `Account.password`) is generated fresh only the first time its record is created.

## Verification

```bash
cd database
uv run pytest      # adapter, mapping, credentials, migrations, generic interface, seed — 51 tests
uv run ruff check . && uv run ruff format --check .
uv run pyright
```

## Troubleshooting

- **`InstanceConfigurationError: Database runtime configuration not found`** — `database.yaml` is missing or the Component root could not be resolved; run from within `database/` or check the installed package layout.
- **`UnknownInstanceError`** — an explicit Instance key was requested that is not declared in `database.yaml`.
- **`MissingEncryptionKeyError`** — `DATABASE_CREDENTIAL_ENCRYPTION_KEY` is not set; see Configuration above.
- **`RuntimeError: Schema drift detected`** from `ensure_ready()`** — the running database's structure no longer matches the recorded mapping; inspect with `detect_schema_drift(engine)` before taking any action, and never repair drift with ad-hoc structural commands — record a proper Migration instead.
- **`sqlalchemy.exc.IntegrityError`** on `create`/`update`** — a uniqueness, foreign-key, or not-null constraint was violated; the operation (and its enclosing Transaction, if any) is rolled back automatically.

## Active capabilities

- **Error handling** — every constraint violation, missing record, unknown Instance, and unsupported credential treatment raises a specific, catchable exception; nothing fails silently.
- **Logging / observability** (`database.observability`) — connection failures, Migration failures, constraint violations, Transaction conflicts, and controlled-command / protected-data access are all logged by event type, with only the error's type name recorded — never the exception message, a row value, or a secret.
- **Authentication / Encryption** — every classified credential field is hashed (`User.password`/`api_key`) or authenticated-encrypted (`Instance.password`/`api_key`, `Account.password`) before it reaches storage; a field whose declared treatment is missing or unsupported is rejected outright, never persisted unprotected.

## Portability

Every persistence decision is classified as `portable_contract`, `portable_mapping`, or `engine_specific_extension` (call `portability_report()` for the current list). Today's SQLite-specific extensions — foreign-key enforcement requiring `PRAGMA foreign_keys = ON` per connection, single-writer connection handling, and OS-file-lock-based concurrent-Migration coordination — are isolated inside `database.adapter` and `database.migrations`; nothing outside those two modules depends on them.
