# my_database.data_logic

## Purpose and boundaries

The generic, Model-driven data logic and mapping of `my_database`: a registry that resolves each
Model key to its table, columns, primary key, credential modes, and status capability, and one
operation pipeline implementing create, read, list, update, delete, and status for every Model. No
Model-specific application Behaviour lives here.

## Public interface

Used by `my_database.database_interface` only:

- `registry.get_model(key)`, `registry.get_model_by_table(name)`, `registry.MODEL_KEYS`,
  `registry.CREDENTIAL_MODES`.
- `operations.create(session, model, data)`, `read`, `list_records`, `update`, `delete`,
  `set_status` — each takes a SQLAlchemy `Session` whose transaction the caller owns, and returns
  plain dicts without credential columns.

## Dependencies

`my_database.storage_adapter` (mapped tables, credential transformations) and `my_database.errors`.

## Configuration

None of its own.

## Usage examples

```python
from my_database.storage_adapter.engine import get_engine, session_factory
from my_database.data_logic import operations

Session = session_factory(get_engine())
with Session() as session, session.begin():
    record = operations.create(session, "trading_platform", {"name": "cTrader", "code": "ctrader"})
```

Installation and startup: see [database/README.md](../../../README.md).
