# my_database.storage_adapter

## Purpose and boundaries

The engine-specific persistence of `my_database`: the SQLite connection with foreign keys enforced,
the SQLAlchemy declarative mapping of the 13 resolved tables, credential at-rest transformations
(scrypt hashing, Fernet encryption), the idempotent seed functions, and the Alembic migration
environment at the parent root (`database/alembic/`). Nothing here is reached by consumers of the
parent package.

## Public interface

Used by `my_database.data_logic` and the migration environment:

- `engine.create_database_engine(url)`, `engine.get_engine()`, `engine.reset_engine()`,
  `engine.session_factory(engine)`.
- `base.Base`, `base.NAMING_CONVENTION`, `base.decimal_type()`; `tables` — one mapped class per
  Model, each declaring `__model_key__`.
- `credentials.hash_credential`, `verify_hashed_credential`, `encrypt_credential`,
  `decrypt_credential`, `transform_for_storage`.
- `seed.seed(connection)`, `seed.unseed(connection)`, `seed.INITIAL_DATA`, `seed.NATURAL_KEYS`.

## Dependencies

SQLAlchemy, cryptography, and the parent's `settings` and `errors` modules.

## Configuration

`DATABASE_URL` and `CREDENTIAL_ENCRYPTION_KEY`, read through the parent's settings (process
environment first, then `database/.env`). No values are stored in this package.

## Usage examples

```python
from my_database.storage_adapter.engine import get_engine
from my_database.storage_adapter.seed import seed

with get_engine().begin() as connection:
    inserted = seed(connection)   # {'users': 1, 'currencies': 8, ...} or zeros when already seeded
```

Schema changes are made only through Alembic revisions; see the parent README for the commands.
Installation and startup: see [database/README.md](../../../README.md).
