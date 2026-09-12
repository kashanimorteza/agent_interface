# my_database

## Purpose and Boundaries

`my_database` is the complete persistence layer for the Trading Assistant. It
turns the logical entities declared by the shared `my_model` package into
stored data, keeps the whole storage structure reproducible from the
repository through an ordered migration history, and publishes one generic
interface through which every consumer reads and writes without ever
touching the engine behind it.

`my_database` owns:

- supported Engine integration, Database Instances, and physical storage;
- the model-to-storage mapping, physical constraints, and indexes;
- the migration history that produced the current schema;
- the generic add/read/list/edit/delete/status data-access interface;
- transactions, credential at-rest protection, and the controlled SQL route.

`my_database` does **not** own:

- domain entity names, fields, relationships, or rules — those belong to
  `my_model`, which `my_database` imports and never redefines;
- HTTP routing or request/response contracts — those belong to Backend;
- runtime startup, connection Bindings between layers, or Access Points —
  those belong to Platform, which delivers what this layer needs through the
  selected Launch;
- application-context or actor-context business rules (for example, "is this
  actor allowed to perform this operation?") — those belong to Backend Logic.

## Internal Layers

```
Database Interface  →  Data Logic and Mapping  →  Storage Adapter  →  Engine
(operations, registry,   (_orm, _credentials,       (_session, _config)
 transactions, sql)       _seed)
```

A consumer only ever imports the Database Interface modules
(`operations`, `registry`, `transactions`, `sql`, `exceptions`, `seed`).
The internal modules (prefixed with `_`) are not a public contract and may
change without notice.

## Installation

```bash
uv sync
```

`my_database` depends on the local `my_model` package (declared as a `uv`
path source) plus SQLAlchemy, Alembic, `cryptography`, and PyYAML. It is an
internal package — never published to a registry — consumed by other layers
through this local dependency mechanism.

## Public Interface

```python
import my_model as m
import my_database as db

record = db.operations.add(m.Broker, name="Example Broker", user_id=1)
```

Every operation is parameterized by an imported `my_model` type — never by a
Model name string — and plain field values or criteria.

| Module | Provides |
| --- | --- |
| `operations` | `add`, `get`, `list`, `update`, `delete`, `set_status` — the one generic pipeline for every persistent Model. |
| `registry` | `list_instances()`, `default_instance()` — discoverable Instance identities. |
| `transactions` | `unit()` — a context manager grouping related operations into one commit or rollback. |
| `sql` | `execute()` — the controlled, parameterized, allow-listed SQL route. |
| `exceptions` | The public failure types every operation raises. |
| `seed` | Inserts every Model-declared initial record, idempotently. |

## Engine, Runtime Configuration, and Migrations

The selected Engine is SQLite; the resolved Instance is `general`
(`Trading Assistant General`), file-backed under `data/` (excluded from
version control, along with the private encryption key under `.secrets/`).
Non-secret runtime settings live in `database.yaml`, packaged alongside the
code.

The storage schema is never changed by application code. Every change is a
recorded Alembic migration under `migrations/versions/`, each covered by an
integrity checksum in `migrations/integrity.json`:

```bash
uv run alembic upgrade head      # apply every pending migration
uv run alembic downgrade -1      # reverse the most recent migration
uv run alembic revision --autogenerate -m "describe the change"
```

`my_database._schema_check.detect_drift(engine)` compares the live database
against the current mapping before normal operation and returns a list of
human-readable differences (empty means no drift).

## The Boundary With Model, Backend, Platform, and Development

- **Model** — `my_database` imports every domain entity from `my_model`'s
  public interface and never maintains a competing definition. A rule
  determinable from one entity's own data (for example, `leverage > 0`) is
  validated by Model; a rule that depends on other stored rows (for example,
  a uniqueness constraint) is enforced here as a storage constraint, because
  Model has no visibility into other persisted records.
- **Backend** — reaches this layer only through the modules above; it never
  imports `_orm`, `_session`, or any other internal module.
- **Platform** — delivers the Bindings this layer needs (when a future
  Engine requires them) through the selected Launch; `my_database` never
  discovers or dials out to a connection on its own outside what Platform
  provides.
- **Development** — this package follows the shared package and
  cross-cutting conventions Development defines; `database.yaml` and
  `.secrets/` follow Database's own layer-local configuration convention
  under Development's rules.

## Credential Protection and Controlled SQL

Every field a Model declares through `credential_fields` is transformed
before storage: `password` fields use a one-way PBKDF2-HMAC-SHA256 hash;
`api_key` fields use authenticated (Fernet) encryption keyed from a private
runtime secret generated on first use. A generic `get`/`list` result always
redacts these fields to a fixed marker; the raw storage representation is
never returned.

The controlled SQL route (`sql.execute`) accepts one parameterized,
data-only `select`/`insert`/`update`/`delete` statement referencing only
tables in an internal allow-list. It rejects multiple statements and any
structural, privilege, or migration keyword, and it applies the same
credential redaction to its results.

## Usage Examples

### Add a record and read it back by identifier

```python
import my_model as m
import my_database as db

broker = db.operations.add(m.Broker, name="Example Broker", user_id=1)
same_broker = db.operations.get(m.Broker, broker.id)
assert same_broker.name == "Example Broker"
```

### List with criteria, ordering, and pagination

```python
first_page = db.operations.list(m.Currency, user_id=1, limit=5, offset=0)
second_page = db.operations.list(m.Currency, user_id=1, limit=5, offset=5)
```

### Update while preserving partial-update semantics

```python
updated = db.operations.update(m.Broker, broker.id, description="Updated")
assert updated.name == "Example Broker"  # omitted field is left unchanged
```

### Delete a record and observe the constraint or not-found result

```python
from my_database.exceptions import ConstraintViolation, NotFound

db.operations.delete(m.Broker, broker.id)
try:
    db.operations.get(m.Broker, broker.id)
except NotFound:
    ...  # the record is gone, as expected

try:
    db.operations.delete(m.Currency, 1)  # still referenced by seeded data
except ConstraintViolation:
    ...  # a referencing record blocks the delete
```

### Enable or disable a Model that declares a status field

```python
platform = db.operations.add(m.TradingPlatform, name="Example Platform", code="example")
disabled = db.operations.set_status(m.TradingPlatform, platform.id, "disable")
assert disabled.status is False
```

### Select an Instance explicitly, or use the configured default

```python
default_id = db.registry.default_instance()
assert default_id.key == "general"

db.operations.list(m.Broker, instance="general")  # explicit
db.operations.list(m.Broker)                      # omitted -> uses the default
```

### Group operations in one transaction and observe commit or rollback

```python
from my_database.exceptions import DatabaseError

with db.transactions.unit() as tx:
    a = db.operations.add(m.AccountGroup, unit=tx, user_id=1, name="Group A")
    b = db.operations.add(m.AccountGroup, unit=tx, user_id=1, name="Group B")
# both committed together here

try:
    with db.transactions.unit() as tx:
        db.operations.add(m.AccountGroup, unit=tx, user_id=1, name="Group C")
        db.operations.add(m.AccountGroup, unit=tx, user_id=1, name="Group C")  # duplicate
except DatabaseError:
    ...  # neither "Group C" row exists; the whole unit rolled back
```

### Handle a validation failure

```python
from my_database.exceptions import ValidationFailed

try:
    db.operations.add(m.Broker, name="", user_id=1)  # blank name violates Model's own rule
except ValidationFailed:
    ...
```

### Use the controlled SQL route with protected output

```python
rows = db.sql.execute(
    "select id, name, password, api_key from users where name = :name",
    {"name": "Admin"},
)
assert rows[0]["password"] == "••••••••"  # credential storage representation withheld
```
