# my_database — Database Component of Trading Assistant

## Purpose and boundaries

`my_database` owns the complete persistence layer of Trading Assistant: the SQLite engine, the
storage schema and its Alembic migration history, the initial data, credential at-rest
transformations, and the one generic **Database Interface** every consumer uses. It is organized as
three nested packages, each with its own README:

- `my_database.database_interface` — the `Database` class (the only public boundary).
- `my_database.data_logic` — the Model registry and the generic operation pipeline.
- `my_database.storage_adapter` — engine, mapped tables, credential transformations, seeding.

Consumers never open `app.db`, tables, the ORM mapping, or migrations directly.

## Public interface

```python
from my_database import Database

db = Database()                      # uses DATABASE_URL / the default app.db
db.create("asset", {"name": "GBPUSD", "symbol": "GBP/USD", "category": "Currency"})
db.read("asset", 1)                  # dict, or None when absent
db.list("currency", filters={"status": True}, order_by=["-id"], limit=10, offset=0)
db.update("asset", 1, {"digits": 4})
db.status("asset", 1, "disable")     # or "enable"
db.delete("asset", 1)                # RESTRICT foreign keys raise ConstraintViolationError
db.execute_sql("select code from currencies where code = :code", {"code": "USD"})
```

Model keys are the keys of `.interface/config/model.yaml` (`user`, `currency`, `trading_platform`,
`broker`, `account`, `asset`, `trailing_group`, `trailing_rule`, `partial_group`, `partial_rule`,
`action_group`, `action`, `position`). Credential fields (`user.password`, `user.api_key`,
`account.password`) are accepted on create and update, transformed on write, and never returned.

Errors are subclasses of `DatabaseError`: `UnknownModelError`, `UnknownFieldError`,
`RecordNotFoundError`, `ConstraintViolationError`, `InvalidActionError`,
`UnsupportedOperationError`, `CredentialKeyMissingError`, `UnsupportedCredentialModeError`.
Internal modules (engine, sessions, mapped tables, settings) are not supported public operations.

## Dependencies

SQLAlchemy 2.0.52, Alembic 1.19.2, cryptography 50.0.1 (pinned in `pyproject.toml`); SQLite is
provided by the Python runtime.

## Configuration

Configuration comes from the process environment or an untracked `.env` file in this directory
(see `.env.example`). Process environment variables take precedence.

| Variable | Meaning |
| --- | --- |
| `DATABASE_URL` | SQLAlchemy connection URL. Empty means the default: the sqlite URL of `database/app.db`. |
| `CREDENTIAL_ENCRYPTION_KEY` | Fernet key for the reversible encryption of encrypted credential columns (`accounts.password`). Required before the first encrypted write, including the initial-data migration. |

Generate a key:

```bash
uv run python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())'
```

Losing the key makes every encrypted credential unrecoverable. Never commit `.env` or `app.db`.

## Installation and startup

The distribution is `my-database` (import name `my_database`). From a consumer project (the
Backend) install it as an editable local path dependency:

```bash
uv add --editable <path to database/>
```

Build and migrate from this directory:

```bash
uv sync                          # create the environment with the pinned dependencies
uv run alembic upgrade head      # create the storage schema and seed the initial data
uv run alembic downgrade -1      # undo the latest revision
uv run alembic current           # show the current revision
```

The history has two revisions: `0001_storage_schema` (13 tables) and `0002_initial_data`
(21 initial records, matched by natural key so re-seeding never duplicates).

During the **first** `upgrade head` the seeding prints three lines of the form

```
GENERATED CREDENTIAL users.Admin.password: <value>
GENERATED CREDENTIAL users.Admin.api_key: <value>
GENERATED CREDENTIAL accounts.Acc-1.password: <value>
```

These values are shown exactly once and are stored only as a one-way hash (users) or encrypted
(accounts). Record them somewhere safe if you need them.

## Usage examples

```python
from my_database import Database, ConstraintViolationError

db = Database()
platform = db.create("trading_platform", {"name": "cTrader", "code": "ctrader"})
print(db.list("trading_platform", order_by=["name"]))
try:
    db.delete("currency", 1)
except ConstraintViolationError:
    print("USD is referenced by an account and cannot be deleted")
```
