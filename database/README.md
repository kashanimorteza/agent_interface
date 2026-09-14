# Database

The `database` package is the Trading Assistant's Database Component: the complete
persistence boundary for the domain Model defines. It maps every Domain Definition to
durable SQLite storage, preserves storage-level guarantees (uniqueness, relationships,
credential protection), and exposes one generic public interface through which consumers
use persistent data without depending on private persistence details.

Database owns persistence only. It never redefines domain meaning (that's `model`),
application behavior, presentation, or workflow orchestration.

## Public surface

```python
from database import (
    ConnectionFailure,
    ConstraintViolation,
    ControlledCommandRejected,
    Database,
    DatabaseError,
    InstanceInfo,
    InstanceRegistry,
    MigrationFailure,
    Transaction,
    TransactionConflict,
    UnknownDatabaseInstance,
    seed_initial_data,
)
```

- **`Database`** — the generic, Model-driven Database Interface: `create`, `get`,
  `list`, `update`, `delete`, and `activate` for any persisted Domain Definition from
  `model`, identified by its type or instance, never by an untyped name string.
- **`Database.transaction()`** — the explicit Transaction boundary: a context manager
  under which grouped operations on one Database Instance commit together or roll back
  together. A standalone call (no `txn=` passed) forms its own atomic unit automatically.
- **`Database.execute_command(name, **params)`** — the capability-restricted controlled
  command route for the few data operations the generic interface cannot express. Only
  pre-registered, parameterized commands are reachable; there is no path from caller
  input to a structural change, a privilege change, connection administration, or a
  Migration operation.
- **`Database.instances`** (`InstanceRegistry`) — discover every configured Database
  Instance's identity, name, and purpose, and the default, without ever receiving a
  connection or a secret value.
- **`seed_initial_data(db)`** — seeds every Target-declared initial record in dependency
  order; safe to call more than once.
- **Exceptions** — `ConnectionFailure`, `MigrationFailure`, `ConstraintViolation`,
  `TransactionConflict`, `ControlledCommandRejected`, `UnknownDatabaseInstance`, all
  subclasses of `DatabaseError`.

Every operation reads a credential-marked field (as `model` declares it) back as the
literal string `"***protected***"`, never a usable representation — hashed or encrypted.

## Setup

Requires Python 3.13+ and [uv](https://docs.astral.sh/uv/). `database` depends on the
sibling `model` package by relative path.

```bash
cd database
uv sync
```

## Installation (as a dependency)

```toml
[project]
dependencies = ["database"]

[tool.uv.sources]
database = { path = "../database" }
```

## Configuration

Non-secret runtime configuration — the configured Engine profiles, Database Instances,
and the default selection — lives in `database.yaml` at the component root:

```yaml
engines:
  sqlite:
    driver: sqlite3
    url_scheme: sqlite
instances:
  general:
    name: "Trading Assistant General"
    purpose: "General application data."
    engine: sqlite
    database: trading_assistant_general
default_instance: general
```

The SQLite file itself lives under `data/` (ignored by version control) and is created
with owner-only (`0o600`) permissions.

Credential protection uses a per-Database-Instance key, resolved in this order:

1. The environment variable `TRADING_ASSISTANT_<INSTANCE>_DATABASE_ENCRYPTION_KEY`
   (for example `TRADING_ASSISTANT_GENERAL_DATABASE_ENCRYPTION_KEY`).
2. A key file Database generates and persists under `.secrets/<instance>.key`
   (also ignored by version control, created with owner-only permissions) the first
   time it is needed.

No secret value is ever recorded in `database.yaml`, an Interface record, or this file.

## Use

Storage structure comes only from Migrations — nothing is created automatically at
import or connect time:

```bash
uv run alembic upgrade head
```

```python
import model
from database import Database

db = Database()  # uses the default Database Instance ("general")

# The generic interface: one pipeline for every Domain Definition.
user = db.create(model.User(name="Ada", username="ada", password="pw", api_key="key"))
fetched = db.get(model.User, user.id)
assert fetched.password == "***protected***"  # never a usable credential representation

# Explicit Transaction boundary: grouped operations commit or roll back together.
with db.transaction() as txn:
    platform = db.create(model.TradingPlatform(name="MetaTrader 5", code="metatrader_5"), txn=txn)
    db.create(model.TradingPlatform(name="Binance", code="binance"), txn=txn)

# Instance Registry: discover Database Instances without a connection or secret.
for info in db.instances.list_instances():
    print(info.key, info.name, info.is_default)

# Controlled command route: a pre-registered, parameterized command only.
db.execute_command("count_positions_by_execution", user_id=user.id)

# Seed every Target-declared initial record (repeatable; skips what already exists).
from database import seed_initial_data

seed_initial_data(db)
```

## Verification

From the `database` directory, with the development dependencies installed:

```bash
uv run alembic upgrade head    # only needed once per fresh data/ directory
uv run pytest      # 59 checks: adapter, registry, every mapping, migrations, interface,
                    # transactions, controlled commands, seeding, credentials, the public
                    # boundary, and this README
uv run ruff check . && uv run ruff format --check .
uv run pyright
```

## Troubleshooting

- **`MigrationFailure: The running Database structure has drifted...`** — the live
  SQLite file's structure no longer matches the recorded Migration history (for example,
  a column was added by hand). Restore it from a Migration-managed state; Database never
  repairs drift automatically.
- **`ConstraintViolation`** — a create, update, or delete would violate a declared
  uniqueness or relationship constraint; inspect the raised exception's message for which
  Domain Definition and constraint were involved.
- **`ControlledCommandRejected: Unknown controlled command`** — the controlled command
  route only ever executes a small, pre-registered set of parameterized commands; it
  never accepts free-form SQL, so a new operation must be added to the route's
  registration, not passed as text.
- **`ConnectionFailure`** — the configured Database Instance's storage location could
  not be opened; check that its `data/` directory is writable and that no other process
  has replaced the database file with something unusable.
- **A previously seeded credential appears unchanged after re-running `seed_initial_data`**
  — expected: seeding is idempotent and skips a record whose natural key already exists.

## Consequential implementation choices

- **Least privilege** for the file-backed SQLite Engine is realized as owner-only
  (`0o600`) file permissions on the database file and every generated secret-key file,
  since SQLite has no server-side role system to restrict.
- **Schema drift detection** compares a SHA-256 checksum of the mapped SQLAlchemy
  metadata against the same checksum computed by reflecting the live database, run
  automatically before a `Database` starts serving operations.
- **`cryptography`** is used as a compatible supporting dependency (beyond the primary
  SQLAlchemy/Alembic selection) to provide authenticated, reversible protection for
  credentials whose resolved at-rest mode is `encrypted`.
