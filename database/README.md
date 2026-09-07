# my_database

The persistence layer of Trading Assistant. It stores and retrieves the shared
Models of `my_model` through one generic interface, owns the storage schema and
its migration history, seeds the declared initial data, and keeps credential
values transformed at rest.

## Purpose and boundaries

`my_database` owns everything about persistence: the Database Instances and
their Engine bindings, the connection, the ORM and the Model-to-table mappings,
the storage schema with its constraints and indexes, the migration history, the
seeding of initial data, credential at-rest storage, and the generic data-access
interface published to consumers.

It is formed from three nested packages, each with its own README:

| Layer | Package | Responsibility |
| --- | --- | --- |
| Database Interface | `my_database.database_interface` | The only boundary consumers use: Model operations, Instance discovery and selection |
| Data Logic and Mapping | `my_database.data_logic` | The generic Model-driven operation pipeline, persistence mapping, credential transformations, seeding |
| Storage Adapter | `my_database.storage_adapter` | The settings boundary, the Engine binding, physical persistence operations |

The dependency direction is Database Interface → Data Logic → Storage Adapter →
Engine. Migration (Alembic, in `migrations/`) is internal tooling that changes
the storage structure through the Storage Adapter; it is not part of the public
interface.

The package does **not** own the Models themselves (`my_model`), application
behaviour or the API (Backend), presentation (Frontend), or the delivery of
runtime configuration and secrets (Platform). Consumers never receive the
Engine, a connection, a table, a mapping, a migration, or a database file.

## Public interface

Import only from the package root:

```python
from my_database import Database, InstanceRegistry, DatabaseError
```

**`InstanceRegistry()`** lists the configured Instances as public identities and
names the default:

- `registry.default` — the key of the default Instance;
- `registry.instances` — a tuple of `InstanceIdentity(key, name, purpose, engine)`;
- `registry.get(key)` — one identity, or `UnknownInstanceError`.

No connection detail, file path, or secret is exposed.

**`Database()`** selects the default Instance; **`Database(instance="<key>")`**
selects a named one. An unknown key, or a default that names no configured
Instance, raises `UnknownInstanceError` before any connection is made.
Construction opens no connection; the Instance's file is created by the first
operation (after the migrations have created the schema — see below).

The operations are generic: pass a Model class or instance exported by
`my_model`; every persistent Model is served by the same pipeline.

| Operation | Returns | Notes |
| --- | --- | --- |
| `create(instance)` | the stored instance with its primary key | credential fields must be supplied; they are transformed at rest |
| `read(Model, key)` | the instance, or `None` | |
| `list(Model, criteria=None, order_by=None, limit=None, offset=None)` | a list of instances | `criteria` is a mapping of field name to value (equality); ordered by primary key unless `order_by` names a Model field |
| `update(instance)` | the stored instance | the instance must carry its primary key; a credential left `None` keeps its stored value, a supplied one is transformed |
| `delete(Model, key)` | `None` | subject to the RESTRICT actions of every relationship that references the record |
| `status(Model, key, action)` | the stored instance | `action` is exactly `"enable"` or `"disable"`; only for a Model with a `status` field |
| `sql(statement, parameters=None)` | a list of plain tuples | values are bound to `:name` placeholders, never interpolated |

Returned instances are validated Model instances whose credential fields are
always `None`; the stored representation never leaves the boundary.

Every failure is raised as `DatabaseError` or one of its subclasses:
`ConfigurationError` (`UnknownInstanceError`, `UnsupportedEngineError`,
`CredentialKeyError`), `OperationError` (unusable arguments), `NotFoundError`,
`ConstraintError` (a uniqueness, relationship, or nullability violation), and
`StatementError` (the Engine could not execute a statement). No driver or ORM
exception escapes.

## Dependencies

- Python 3.14.7 (`requires-python >=3.14,<3.15`)
- [SQLAlchemy](https://www.sqlalchemy.org/) 2.0.52 — ORM and parameterized SQL
- [Alembic](https://alembic.sqlalchemy.org/) 1.19.2 — migration tool
- [cryptography](https://cryptography.io/) 50.0.1 — reversible credential encryption
- `my-model` — the shared Model package, installed as an editable local path dependency (`../model`)
- SQLite through the runtime-provided `sqlite3` module — the only Engine implemented in this version
- [uv](https://docs.astral.sh/uv/) 0.12.10 — environment and build tool

## Configuration

Platform delivers the `database` section of the runtime configuration as
environment variables. The package reads only these; it never reads a
configuration file.

| Variable | Default | Meaning |
| --- | --- | --- |
| `DATABASE__DEFAULT_INSTANCE` | `general` | The key of the default Instance |
| `DATABASE__INSTANCES__<KEY>__ENGINE` | `sqlite` | The Engine bound to Instance `<KEY>` |
| `DATABASE__INSTANCES__<KEY>__FILE` | `database/data/trading_assistant_general.db` for `general` | The database file of a file-backed Instance |
| `DATABASE__CREDENTIAL_ENCRYPTION_KEY_SECRET` | `TRADING_ASSISTANT_CREDENTIAL_ENCRYPTION_KEY` | The **name** of the environment variable holding the credential-encryption key |

The one built-in Instance is `general` — "Trading Assistant General", purpose
"General application data.", Engine SQLite. Setting variables for another
`<KEY>` declares an additional Instance.

A relative file path is resolved against the project root (the directory
containing `.interface/`), whatever the working directory.

The credential-encryption key is read from the variable named by
`DATABASE__CREDENTIAL_ENCRYPTION_KEY_SECRET`. Any non-empty secret is accepted
(a cipher key is derived from it); the URL-safe base64 encoding of 32 random
bytes is a good value:

```
export TRADING_ASSISTANT_CREDENTIAL_ENCRYPTION_KEY=$(python -c "import secrets, base64; print(base64.urlsafe_b64encode(secrets.token_bytes(32)).decode())")
```

The key is required before the first encrypted write — including the seeding
migration, which stores an encrypted Account credential. Never commit its value.

Credential at-rest modes: `User.password` and `User.api_key` are stored as
salted one-way hashes (PBKDF2-HMAC-SHA256); `Account.password` is stored
encrypted (reversible under the key).

## Installation and startup

From this directory:

```
uv sync
```

Create or bring the default Instance up to date (the file and its directory are
created on first use), with the encryption key exported as shown above:

```
uv run alembic upgrade head
```

Other migration commands: `uv run alembic current` reports the applied
revision, `uv run alembic downgrade -1` reverts one revision, and
`uv run alembic -x instance=<key> upgrade head` migrates a named Instance.
The history is linear: `0001_schema` creates the fourteen tables and
`0002_initial_data` seeds the declared initial records idempotently (matched on
each Model's natural key). A credential declared as "generate securely" is
fulfilled with a random value at seed time and reported **once on standard
error**; it is never stored in clear.

A consumer installs the package as an editable local path dependency:

```toml
[project]
dependencies = ["my-database"]

[tool.uv.sources]
my-database = { path = "../database", editable = true }
my-model = { path = "../model", editable = true }
```

The distribution is named `my-database` and the import package `my_database`;
it is internal and never published.

## Usage examples

Discover the Instances and read seeded data:

```python
from my_database import Database, InstanceRegistry
from my_model import Currency

registry = InstanceRegistry()
print("default:", registry.default, [(i.key, i.name, i.engine) for i in registry.instances])

db = Database()                                   # the default Instance
jpy = db.list(Currency, criteria={"code": "JPY"})[0]
assert jpy.decimal_digits == 0
print(jpy.name, jpy.symbol, db.read(Currency, jpy.id).country)
```

Create, update, change status, and delete a record:

```python
from my_database import Database, DatabaseError
from my_model import Currency

db = Database()
coin = db.create(Currency(name="Example Coin", code="EXC", symbol="Ⓔ"))
assert coin.id is not None and coin.status is True

coin.symbol = "E$"
coin = db.update(coin)
disabled = db.status(Currency, coin.id, "disable")
assert disabled.status is False and disabled.symbol == "E$"

db.delete(Currency, coin.id)
assert db.read(Currency, coin.id) is None
try:
    db.delete(Currency, coin.id)
except DatabaseError as error:                     # NotFoundError
    print("second delete rejected:", error)
```

Credentials are accepted on write and never returned:

```python
from my_database import Database
from my_model import User

db = Database()
user = db.create(User(name="Example Operator", username="example", password="s3cret", api_key="k3y"))
assert user.password is None and user.api_key is None     # transformed at rest, never carried back
user.description = "renamed without touching the credentials"
assert db.update(user).description.startswith("renamed")
db.delete(User, user.id)
```

Parameterized SQL for what the typed operations cannot express:

```python
from my_database import Database

db = Database()
rows = db.sql("select code, decimal_digits from currencies where decimal_digits = :digits order by code", {"digits": 2})
print(rows[:3])                                    # plain tuples
```
