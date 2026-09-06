# my_database.database_interface

## Purpose and boundaries

The only boundary published to consumers of `my_database`: the `Database` class, which accepts a
Model key, an operation, and that operation's data or criteria. It never exposes the engine,
connection, sessions, ORM classes, migrations, or the database file.

## Public interface

`Database(url: str | None = None)` with `create`, `read`, `list`, `update`, `delete`, `status`, and
`execute_sql`. The parent package re-exports it: `from my_database import Database`. Error types are
the parent's `my_database.errors` classes. Nothing else in this package is a supported operation.

## Dependencies

`my_database.data_logic` (the generic operation pipeline) and `my_database.storage_adapter` (engine
and session factory). Third-party dependencies are managed by the parent.

## Configuration

None of its own; `DATABASE_URL` is read through the parent's settings when no URL is given.

## Usage examples

```python
from my_database import Database

db = Database()
print(db.read("user", 1))          # {'id': 1, 'name': 'Admin', ...} — no credential fields
rows = db.execute_sql("select code from currencies where code = :code", {"code": "USD"})
```

Installation and startup: see [database/README.md](../../../README.md).
