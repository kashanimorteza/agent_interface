# Trading Assistant — Database Component

The Database Component owns the complete persistence layer of Trading Assistant: the SQLite engine,
the storage schema and its Alembic migration history, the initial data, credential at-rest
transformations, and the one generic **Database Interface** every consumer uses.

Consumers never open `app.db`, tables, the ORM mapping, or migrations directly. They import the
package and use the `Database` class.

## Installation as a consumer

The package is `trading-assistant-database` (import name `trading_database`). From a consumer
project (for example the Backend), install it as an editable local path dependency:

```bash
uv add --editable <path to database/>
```

## Runtime configuration

Configuration comes from the process environment or an untracked `.env` file in this directory
(see `.env.example`). Process environment variables take precedence.

| Variable | Meaning |
| --- | --- |
| `DATABASE_URL` | SQLAlchemy connection URL. Empty means the default: the sqlite URL of `database/app.db`. |
| `CREDENTIAL_ENCRYPTION_KEY` | Fernet key used for the reversible encryption of encrypted credential columns (`accounts.password`). Required before the first encrypted write, including the initial-data migration. |

Generate a key:

```bash
uv run python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())'
```

Losing the key makes every encrypted credential unrecoverable. Never commit `.env` or `app.db`.

## Building and migrating the Database

Run from this directory:

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

## The Database Interface

```python
from trading_database import Database

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
