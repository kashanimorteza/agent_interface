# Database

## Purpose and boundaries

The project's persistence layer for the Trading Assistant. It maps every persistent domain Model (from the `my_model` package) to physical storage, keeps the storage schema reproducible through migration history, seeds declared initial data, and publishes one generic interface through which every consumer reads and writes.

Database owns persistence mapping, storage schema, migrations, connections, and the generic data-access interface. It never owns domain meaning (that stays in Model), application behaviour, the HTTP API, or Frontend.

Internally it is three layers, in this dependency direction: **Database Interface** (the only published boundary) → **Data Logic and Mapping** (generic Model-to-table mapping, credential at-rest transformation) → **Storage Adapter** (owns the connection to the selected Engine). Migration is separate internal tooling that records the ordered, reversible history of the schema.

## Public interface

An import surface. Consumers install this package and import from its top-level namespace:

- `create(model_cls, **values)`, `get(model_cls, id)`, `list(model_cls, **filters)`, `update(model_cls, id, **values)`, `delete(model_cls, id)` — the generic, Model-driven data operations. Every one accepts a real Model type from `my_model`, never an untyped name string.
- `status(model_cls, id, action)` — `action` is `"enable"` or `"disable"`; rejected when `model_cls` declares no `status` field.
- `transaction(instance=None)` — a context manager yielding a connection to pass as `conn=...` to the operations above, so their changes commit or roll back together. A standalone call without `conn=` is its own atomic unit.
- `execute_sql(sql, params=None, instance=None, conn=None)` — the controlled SQL route for what the generic operations cannot express. Rejects structural (DDL) statements and any statement not naming exactly one mapped table; a write must use `RETURNING` so its resulting row can be re-validated against its Model before the caller sees it. Never returns a credential field's stored representation.
- `list_instances()`, `default_instance()` — the Instance Registry: selectable identities (key, name, purpose) only, never a connection or secret.
- `seed_initial_data(instance=None)` — seeds every Model's declared initial data; repeatable without duplication.
- `RejectedOperationError`, `UnsupportedOperationError` — raised when an operation cannot be performed under Database's protections or does not apply to the given Model.

No caller ever receives a connection object, an ORM mapping, a migration internal, or a credential's stored representation.

## Dependencies

The `my_model` package (installed as a local, editable dependency — Model and Database evolve in the same repository and are never independently published). SQLAlchemy for the ORM/Core mapping and Storage Adapter, Alembic for migrations, `cryptography` for reversible credential encryption, PyYAML to read this package's own runtime configuration.

## Configuration

Non-secret runtime configuration — the Engine and Instance catalogue and the default Instance — lives in [`database.yaml`](database.yaml) at this package's root; it is safe to commit and contains no secret values.

Secrets are never committed. The one secret this package currently owns is the encryption key for the `encrypted` credential at-rest mode: it is read from the `TRADING_ASSISTANT_DATABASE_ENCRYPTION_KEY` environment variable when set; otherwise a key is generated once and kept under `.secrets/` (git-ignored) for local development. The configured SQLite Instance needs no connection credentials — its storage is a local file under `data/` (also git-ignored, per the selected Engine's `committed: false` storage setting).

## Installation and startup

Managed as an isolated `uv` project with a local editable dependency on `../model`. From this directory:

```bash
uv sync
uv run alembic upgrade head     # creates/updates the physical schema
```

Migration commands:

```bash
uv run alembic upgrade head     # apply every migration up to the latest
uv run alembic downgrade -1     # reverse the most recently applied migration
uv run alembic revision --autogenerate -m "description"   # record a new schema change
```

## Usage examples

```python
import my_database as db
import my_model as m

user = db.create(m.User, name="Admin", username="admin", password="...", api_key="...")
db.get(m.User, user["id"])          # -> dict without password/api_key
db.list(m.User, status=True)
db.status(m.User, user["id"], "disable")

# Related writes committed or rolled back together:
with db.transaction() as conn:
    group = db.create(m.AccountGroup, user_id=user["id"], name="Default", conn=conn)
    db.create(m.Account, group_id=group["id"], ..., conn=conn)

# One-time setup:
db.seed_initial_data()
```
