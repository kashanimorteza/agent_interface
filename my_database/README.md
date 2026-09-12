# my_database

The independent persistence layer for the Trading Assistant. It turns the logical Models defined in `my_model` into stored data and publishes one generic interface through which every consumer reads and writes, without ever meeting the engine behind it.

## Responsibilities and boundaries

`my_database` owns Engine integration, Database Instances, physical storage, migrations, model-to-storage mappings, and the generic data-access interface it publishes. It does **not** own domain meaning (that belongs to `my_model`), application behavior, the HTTP API, or Frontend concerns.

## The three internal layers

```text
Database Interface  →  Data Logic and Mapping  →  Storage Adapter  →  Engine
```

- **Database Interface** (`my_database.interface`) — the only boundary published to consumers: generic Model-driven operations plus the Instance Registry.
- **Data Logic and Mapping** (internal: `_orm`, `_mapping`, `_convert`) — persistence mapping of every domain entity, credential transformation, and uniqueness/reference enforcement.
- **Storage Adapter** (internal: `_base`, `_config`) — the Engine connection, session management, and layer-local runtime configuration.

Consumers only ever import `my_database.interface` and `my_database.registry`. Everything else (`_base`, `_config`, `_orm`, `_mapping`, `_convert`, `_credentials`) is internal.

## Installation

```bash
cd my_database
uv sync
uv run alembic upgrade head   # create the schema
```

## The public Database Interface

Every operation accepts an imported Model type or instance from `my_model` — never a string name.

```python
import my_database
from my_model.broker import Broker
from my_model.user import User

# A Broker belongs to a User, so one must exist first.
owner = my_database.interface.add(User(name="Ada", username="ada", password="x", api_key="y"))

# Add / create
created = my_database.interface.add(Broker(name="Example Broker", user_id=owner.id))

# Read by identifier
found = my_database.interface.get(Broker, created.id)

# List, with typed criteria, ordering, and pagination
brokers = my_database.interface.list_(Broker, user_id=owner.id, order_by="id", limit=10, offset=0)

# Edit / update — only supplied fields change (partial update)
updated = my_database.interface.update(Broker, created.id, description="Updated")

# Delete
was_deleted = my_database.interface.delete(Broker, created.id)

# Enable / disable — only for a Model declaring a `status` field
my_database.interface.set_status(Broker, created.id, "disable")
```

### Instance selection

Every operation accepts an optional `instance=` keyword naming an Instance from the Registry; omitting it uses the configured default.

```python
from my_database import registry

registry.list_instances()     # -> (InstanceIdentity(key='general', name=..., purpose=...),)
registry.default_instance()   # -> the Instance used when `instance=` is omitted

my_database.interface.get(Broker, 1, instance="general")
```

Selecting an unknown Instance raises `my_database._config.UnknownInstanceError`; it is never silently redirected to the default.

### Transactions

Group related operations into one committed or rolled-back unit with `interface.transaction()`, passing the returned handle as `within=` to every operation that should join it.

```python
from my_model.user import User

with my_database.interface.transaction() as txn:
    user = my_database.interface.add(User(name="Ada", username="ada", password="x", api_key="y"), within=txn)
    my_database.interface.add(Broker(name="FxPro", user_id=user.id), within=txn)
# both commit together; if either raises, neither is persisted
```

### Handling results

```python
from my_database import interface

interface.get(Broker, 999)  # -> None (not found; no exception)

try:
    interface.update(Broker, 999, description="x")
except interface.NotFoundError:
    ...

interface.add(Broker(name="Existing Broker", user_id=owner.id))
try:
    interface.add(Broker(name="Existing Broker", user_id=owner.id))  # duplicate (name, user_id)
except interface.ConstraintViolationError:
    ...  # a uniqueness rule or a reference to a non-existent record failed

try:
    interface.set_status(SomeModelWithoutStatus, 1, "enable")
except interface.UnsupportedOperationError:
    ...
```

## Credential protection

A field the owning Model marks as a credential (`password`, `api_key` on several entities) is transformed before it is ever written to storage, using the mode the Model itself declared:

- **hash** (one-way — `User.password`, `User.api_key`): stored as a salted PBKDF2-HMAC-SHA256 digest. A read never returns the original value or the digest — it returns the fixed marker `"<redacted>"`.
- **encrypted** (reversible — `Instance.password`, `Instance.api_key`, `Account.password`): stored using Fernet authenticated encryption. A read decrypts and returns the original value, because this mode exists precisely for credentials the application must recover (e.g. to open a live connection).

The storage representation itself — the hash or the ciphertext — is never returned to a consumer, logged, or otherwise exposed.

## Secrets

No secret value lives in a committed file. The Fernet key used for "encrypted" mode credentials is resolved from the `MY_DATABASE_ENCRYPTION_KEY` environment variable; every shared or production environment must set it. When it is absent (local development only), a key is generated once and cached at the gitignored `my_database/.secrets/encryption.key`.

## Engine, Instances, and migrations

The selected Engine is SQLite (file-backed, foreign keys enforced). Non-secret runtime configuration — the Engine and Instance catalogue and the default selection — lives in the committed `database.yaml` next to this package. The database file itself lives under the gitignored `my_database/data/`.

Migrations use Alembic and are the only way the storage schema changes:

```bash
uv run alembic upgrade head      # apply every recorded migration
uv run alembic downgrade base    # reverse them all
uv run alembic revision --autogenerate -m "description"   # record a new schema change
```

## Initial data

Every entity that declares `INITIAL_DATA` in `my_model` is seeded through the public interface, in dependency order, by:

```python
from my_database import seed

seed.seed_all()   # returns the number of records inserted; safe to call again (no duplicates)
```

A field the Target marks "generate securely" (e.g. a seeded user's password) is resolved to a real generated value at seeding time — `my_model` never carries a fabricated placeholder for it.

## Boundary with Model, Backend, and Platform

- **Model** (`my_model`) is the only source of domain meaning, fields, relationships, and validation rules. `my_database` imports Model types from `my_model`'s public namespace only; it never redefines or privately copies them.
- **Backend** reaches persistence only through `my_database.interface` and `my_database.registry` — never through an internal module, a connection, or an ORM object.
- **Platform** delivers connection-relevant Bindings (should a future Instance require them) through the selected Launch; `my_database` never publishes a raw connection.

## Configuration

- `database.yaml` (committed): Engine catalogue, Instance catalogue, default Instance. No secrets.
- `MY_DATABASE_ENCRYPTION_KEY` (environment, required outside local development): the credential-encryption key.
- `my_database/data/` (gitignored): SQLite database files.
- `my_database/.secrets/` (gitignored): local development encryption key, generated automatically when the environment variable is absent.
