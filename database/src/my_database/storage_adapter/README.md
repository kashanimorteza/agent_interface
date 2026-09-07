# my_database.storage_adapter

The Storage Adapter layer of `my_database`. Shared setup is described in the
parent [database/README.md](../../../README.md).

## Purpose and boundaries

Owns the settings boundary, the binding of each Instance to its Engine, and the
physical persistence operations. It is the only place in the package that
touches the driver: every Engine failure is translated into a Database error
here. It knows nothing about Models or credential modes.

## Public interface

Available to Data Logic, the Database Interface layer, and the migration
tooling only; consumers of `my_database` never import it.

- `load_settings(environ=None)` → `Settings(default, instances, credential_key_secret)` with `InstanceSettings(key, name, purpose, engine, file)`;
- `credential_key(environ=None)` — the credential-encryption secret, or `CredentialKeyError`;
- `project_root()` / `resolve_path(value)` — resolution of relative file paths against the project root;
- `make_engine(instance_settings)` — a SQLAlchemy Engine (SQLite: foreign keys enforced, `check_same_thread` off, data directory created on first connection);
- `Storage(engine)` — `insert`, `select_one`, `select_many`, `update`, `delete`, `execute`, each in its own transaction.

## Dependencies

SQLAlchemy and the runtime-provided `sqlite3` driver. Managed by the parent
project.

## Configuration

The `DATABASE__*` variables documented in the parent README are read here and
nowhere else.

## Usage examples

```python
from my_database.storage_adapter import load_settings

settings = load_settings()
print(settings.default, [(i.key, i.engine) for i in settings.instances.values()], settings.credential_key_secret)
```
