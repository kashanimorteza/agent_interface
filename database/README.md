# my_database

The persistence layer of the Trading Assistant. It turns the shared Models of `my_model` into reproducible storage, keeps the whole storage structure defined as code, and publishes one generic interface through which every consumer reads and writes without ever meeting the engine behind it.

## Purpose and boundaries

`my_database` owns **how the project's data is stored**:

- the Instances (selectable database identities) and their connections to the resolved engine;
- the storage design derived from the shared Models: one table per Model, one column per field, one foreign key per relationship, one constraint per rule;
- the at-rest transformation of credential fields (`hash`, `encrypted`, or `plaintext`);
- the ordered, reversible migration history that creates the structure;
- the seeding of every Model's declared initial data;
- the generic Model operations and the controlled command execution it publishes.

It is formed from three internal layers with a fixed dependency direction: **Database Interface → Data Logic and Mapping → Storage Adapter → Engine**. Only the Database Interface is public.

It does **not** own the logical Models (they are `my_model`'s), application behaviour, the HTTP API, the user interface, or deployment secrets. Migration tooling is internal: it is a command, not part of the public interface.

## Public interface

Import everything from `my_database`. The adapter, mapping, connection, migration, and configuration implementation are internal and not part of the interface.

| Symbol | Purpose |
|---|---|
| `Database` | The gateway. Construct with no arguments to resolve settings from the centralized runtime configuration. Every operation takes an optional `instance` key; the default Instance is used when none is given. |
| `InstanceRegistry` | Discovery of Instance identities, available as `Database.instances`. Iterable; `len()` gives the number of Instances; `.default` is the default Instance; `.get(key)` one Instance. |
| `Instance` | One registry entry: `key`, `name`, `purpose`, `engine`, `database`, `is_default`. Carries no connection and no secret. |
| `SeedReport` | Result of `Database.seed()`: `inserted` and `skipped` counts per Model and the `generated` secrets. |
| `GeneratedSecret` | One secret generated during seeding: `model`, `record`, `field`, `value`. Shown once; only its at-rest form is stored. |
| `CREDENTIAL_MASK` | The value returned in place of any stored credential. Passing it back in an update leaves the credential unchanged. |
| `generate_encryption_key` | Produces a new key for the `encrypted` at-rest mode. |
| `DatabaseError` | Base of every error below. |
| `ConfigurationError` | The runtime configuration or a required secret is missing or invalid. |
| `UnknownInstance` | The selected Instance key is not defined. |
| `InvalidOperation` | The operation is not valid for the given Model or arguments. |
| `NotFound` | No record matches the identifier. |
| `ConstraintViolation` | The operation would violate a mapped storage constraint. |

`Database` operations, each generic over every Model of `my_model`:

| Operation | Behaviour |
|---|---|
| `create(value)` | Stores a new record from a Model instance and returns it with its identifier. |
| `read(Model, key)` | Returns the record with the identifier, or raises `NotFound`. |
| `list(Model, criteria=None)` | Returns every record matching the equality criteria, in identifier order. Credential fields cannot be criteria. |
| `update(Model, key, changes)` | Changes only the supplied fields and returns the result. The identifier cannot be changed. |
| `delete(Model, key)` | Removes the record, or raises `NotFound`. |
| `status(Model, key, action)` | `enable` or `disable` a record of a Model that declares a `status` field. Any other action, or a Model without `status`, raises `InvalidOperation`. |
| `execute(statement, parameters=None)` | Runs one command with bound parameters and returns its rows as mappings. Values are never interpolated, and no connection is returned. |
| `verify_credential(Model, key, field, given)` | Whether `given` matches the stored credential, in any at-rest mode. |
| `recover_credential(Model, key, field)` | The original value of a credential stored in a recoverable mode (`encrypted`, `plaintext`). A hashed credential raises `InvalidOperation`. |
| `seed()` | Applies every Model's declared initial data and returns a `SeedReport`. Repeatable: existing records are skipped. |
| `close()` | Releases the engine connections. |

Model identity is always a Model type or instance from `my_model`; a bare name string raises `InvalidOperation`. Returned values are Model instances whose credential fields hold `CREDENTIAL_MASK`.

### Storage design

- Table names are the plural snake case of the Model name (`Currency` → `currencies`, `TradingPlatform` → `trading_platforms`); columns keep the field names. Each table's comment records its source Model and each column's comment its source field.
- Logical types map to engine-independent column types: integer, string (with the declared size), boolean, decimal as numeric with precision 28 and scale 10, float, and datetime.
- Every relationship is a foreign key on its carrying field referencing the target's primary key, indexed as `ix_<table>_<column>`, with `RESTRICT` on delete and update.
- A composite uniqueness rule becomes a unique constraint named `uq_<table>_<fields>`; for example `uq_brokers_user_id_name`.
- The at-rest mode of a credential field is the Model's explicit rule, otherwise the default for its name (`password` and `api_key` hash), otherwise plaintext. In this project the User's password and API key are hashed and the Account's password is encrypted.

## Dependencies

- Python 3.14 or later.
- `my-model`, the shared Model package, consumed only through its public import interface (a local path dependency).
- `sqlalchemy` for the engine-independent storage design and operations, `alembic` for the migration history, `cryptography` for the encrypted at-rest mode, and `pyyaml` to read the runtime configuration.

The supported engines are SQLite (the selected default), PostgreSQL, and MySQL. A server engine additionally needs its driver installed.

The package is consumed by the Backend layer through its Data Access layer.

## Configuration

The package reads its section of the centralized public runtime configuration, `application.yaml` at the project root, and resolves the secrets that section names from the runtime environment: the process environment first, then the project's `.env` file. The project root is found by walking up from the current directory, or taken from `TRADING_ASSISTANT_ROOT`.

The `database` section:

| Setting | Meaning | Example |
|---|---|---|
| `settings.default_instance` | The Instance used when a consumer selects none. | `general` |
| `settings.storage_directory` | Where a file-based Instance keeps its storage file, relative to the project root. Never committed. | `data` |
| `settings.encryption_key_secret` | Name of the runtime secret holding the key for the encrypted at-rest mode. | `TRADING_ASSISTANT_DATABASE_ENCRYPTION_KEY` |
| `settings.instances.<key>.name` | The Instance's human-readable name. | `Trading Assistant General` |
| `settings.instances.<key>.purpose` | What the Instance is for. | `General application data.` |
| `settings.instances.<key>.engine` | `SQLite`, `PostgreSQL`, or `MySQL`. | `SQLite` |
| `settings.instances.<key>.database` | The database name; the storage file name for SQLite. | `trading_assistant_general` |
| `settings.instances.<key>.host`, `.port` | Server location; `engine_default` selects the engine's port. Ignored by SQLite. | `localhost`, `engine_default` |
| `settings.instances.<key>.username_secret`, `.password_secret` | Names of the runtime secrets holding connection credentials. Ignored by SQLite. | `TRADING_ASSISTANT_GENERAL_DATABASE_USERNAME` |
| `bindings.model` | The Model package the layer consumes and how. | `package: my_model`, `interface: import` |

Secrets, named in `.env.example` at the project root and supplied through `.env` or the environment:

| Secret | Purpose |
|---|---|
| `TRADING_ASSISTANT_DATABASE_ENCRYPTION_KEY` | Key for the encrypted at-rest mode. Generate one with `uv run python -m my_database generate-key`. |
| `TRADING_ASSISTANT_GENERAL_DATABASE_USERNAME` | Connection username of the `general` Instance (server engines only). |
| `TRADING_ASSISTANT_GENERAL_DATABASE_PASSWORD` | Connection password of the `general` Instance (server engines only). |

The migration tooling selects its Instance with `TRADING_ASSISTANT_DATABASE_INSTANCE` and uses the default Instance when it is unset.

## Installation

The package is internal and is not published. Install it together with the Model package into the consuming environment:

```bash
uv pip install path/to/model path/to/database
```

Inside the package directory, `uv sync` creates the package's own isolated environment with every dependency, including the Model package, resolved.

### Creating the storage structure

The structure is created only by the migration history, run from the package directory:

```bash
uv run alembic upgrade head
```

`uv run alembic downgrade -1` reverses the latest migration. Application code never creates or alters storage objects.

### Applying the initial data

```bash
uv run python -m my_database seed
```

The command inserts every declared initial record that does not already exist and prints, once, any secret it generated (the Admin user's password and API key, the Acc-1 account's password). Those values are stored only in their at-rest form and cannot be printed again.

There is no service to start: `my_database` is an importable library plus the two commands above.

## Usage

Perform Model operations through the gateway:

```python
from decimal import Decimal
from my_model import Currency
from my_database import Database, NotFound

db = Database()
created = db.create(Currency(name="Example Dollar", code="EXD", symbol="E$"))
assert created.id is not None and created.decimal_digits == 2

same = db.read(Currency, created.id)
assert same == created

listed = db.list(Currency, {"code": "EXD"})
assert [c.id for c in listed] == [created.id]

renamed = db.update(Currency, created.id, {"name": "Example Dollar (renamed)"})
assert renamed.code == "EXD"

disabled = db.status(Currency, created.id, "disable")
assert disabled.status is False

db.delete(Currency, created.id)
try:
    db.read(Currency, created.id)
except NotFound:
    pass
else:
    raise AssertionError("expected NotFound")
db.close()
```

Discover Instances and run a controlled command:

```python
from my_database import Database

db = Database()
registry = db.instances
assert registry.default.key == "general" and len(registry) >= 1
rows = db.execute("SELECT count(*) AS n FROM currencies WHERE code = :code", {"code": "USD"})
assert rows[0]["n"] in (0, 1)
db.close()
```

Work with credentials without ever seeing their stored form:

```python
from my_model import User
from my_database import Database, CREDENTIAL_MASK

db = Database()
user = db.create(User(name="Example", username="example", password="s3cret", api_key="k3y"))
assert user.password == CREDENTIAL_MASK
assert db.verify_credential(User, user.id, "password", "s3cret")
assert not db.verify_credential(User, user.id, "password", "other")
db.delete(User, user.id)
db.close()
```
