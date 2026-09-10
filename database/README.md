# my_database

## Purpose and boundaries

The persistence layer for the Trading Assistant. It maps every domain Model
published by `my_model` to storage, guarantees the Model rules that require
stored state (uniqueness, referenced existence), and publishes one generic,
Model-driven interface through which every consumer reads and writes.

Database is formed from three internal layers, in this dependency direction:

`Database Interface` (this package's public surface) → `Data Logic and
Mapping` (generic Model-to-table mapping and operation pipeline) → `Storage
Adapter` (Engine connection and physical persistence).

Only the Database Interface layer — the gateway and the Instance Registry —
is meant to be imported by a consumer. Internal modules are named with a
leading underscore to signal that they are not part of the public interface.

Database owns persistence only: engines, Instances, connections, the ORM
mapping, storage schema, migrations, and the published interface. Logical
Models, fields, relationships, and domain rules remain owned by `my_model`;
Database owns only their persistence mapping and enforcement.

## Public interface

An import surface, exposing:

- `gateway` — a ready-to-use `Database` instance bound to the default
  Instance. `Database(instance_key)` selects another configured Instance.
- `Database.create(model_cls, data)` / `.get(model_cls, id)` /
  `.list(model_cls, where=...)` / `.update(model_cls, id, data)` /
  `.delete(model_cls, id)` — the same generic operation for any Model
  published by `my_model`.
- `Database.set_status(model_cls, id, "enable" | "disable")` — available only
  for a Model that declares a `status` field.
- `Database.execute_sql(model_cls, sql, params)` — a controlled, parameterized
  SQL route for a data operation that the generic operations cannot express.
  It rejects structural (DDL) statements and any statement touching a
  credential field, and validates the targeted table against its Model before
  committing.
- `Database.transaction()` — a context manager yielding a `BoundDatabase` that
  exposes the same operations bound to one connection; its writes commit
  together on success and roll back together on failure.
- `list_instances()` / `default_instance()` — the Instance Registry: every
  configured Instance's key, name, purpose, and Engine, and the default's key.
- `seed_initial_data()` — inserts every initial record declared by a Model,
  skipping records that already exist; safe to call repeatedly.

A read never returns a credential field's stored representation: `password`
and `api_key` come back as the fixed placeholder `"**redacted**"`.

## Dependencies

- Python (this package's declared `requires-python`)
- [SQLAlchemy](https://www.sqlalchemy.org/) for schema definition and queries
- [Alembic](https://alembic.sqlalchemy.org/) for migration history
- [cryptography](https://cryptography.io/) for reversible credential encryption
- [PyYAML](https://pyyaml.org/) for the runtime configuration file
- `my_model`, the shared domain Model package, as a local dependency

## Configuration

- `database.yaml` — this package's own non-secret runtime configuration:
  the supported Engine, the configured Instances, and the default Instance.
- `DATABASE_ENCRYPTION_KEY` (environment variable, optional) — the key used
  to encrypt/decrypt fields whose at-rest mode is `encrypted`. When unset, a
  key is generated on first use and kept in `.secrets/encryption.key`
  (excluded from version control); either way, the key never appears in
  `database.yaml` or any committed file.

## Installation and startup

A local workspace package, added as an editable path dependency by its
consumers. To prepare a fresh environment:

```
uv run alembic upgrade head       # create the schema
uv run python -c "import my_database as db; db.seed_initial_data()"
```

## Usage examples

```python
import my_database as db
from my_model import Broker

broker = db.gateway.create(Broker, {"name": "FxPro", "user_id": 1})
same = db.gateway.get(Broker, broker.id)
active = db.gateway.list(Broker, where={"user_id": 1})
db.gateway.set_status(Broker, broker.id, "disable")
```

```python
with db.gateway.transaction() as tx:
    group = tx.create(AccountGroup, {"user_id": 1, "name": "New Group"})
    tx.create(Account, {"group_id": group.id, ...})
```
