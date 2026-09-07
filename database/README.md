# my_database

The persistence layer of the Trading Assistant. It turns the shared Models of `my_model` into reproducible storage, keeps the whole storage structure defined as code, and publishes one generic interface through which every consumer reads and writes without ever meeting the engine behind it.

## Purpose and boundaries

`my_database` owns **how the project's data is stored**:

- the Engine profiles it implements, the Instances it offers, and which one is the default;
- the connections behind those identities;
- the storage design derived from the shared Models: one table per Model, one column per field, one foreign key per relationship;
- the guarantee of the Model rules that depend on stored data, enforced when changes commit;
- the at-rest transformation of credential fields;
- the ordered, reversible migration history that creates the structure;
- the seeding of every Model's declared initial data;
- the generic Model operations, the transaction boundary, and the controlled command route it publishes.

It is formed from three internal layers with a fixed dependency direction: **Database Interface → Data Logic and Mapping → Storage Adapter → Engine**. Only the Database Interface is public.

It does **not** own the logical Models (they are `my_model`'s), application behaviour, the HTTP API, the user interface, or deployment secrets. What a Model's own data determines is checked by the validation `my_model` publishes, never by a second copy kept here. Migration is internal tooling: it is a command, not part of the public interface.

## Public interface

Import everything from `my_database`. The adapter, mapping, connection, migration, and configuration implementation are internal and not part of the interface.

| Symbol | Purpose |
|---|---|
| `Database` | The gateway. Construct with no arguments to use the layer's own configuration. Every operation takes an optional `instance`, given as a key or as an identity from the registry. |
| `Transaction` | One unit of related operations on a single Instance, obtained from `Database.transaction()`. Offers the same operations as the gateway, plus `cancel()`, `instance`, and `outcome`. |
| `TransactionCancelled` | Raised by `cancel()` inside a unit and absorbed by the boundary. |
| `InstanceRegistry` | Discovery of Instance identities, available as `Database.instances`. Iterable; `len()` gives the number of Instances; `.default` is the default; `.get(key)` one identity. |
| `Instance` | One registry entry: `key`, `name`, `purpose`, `engine`, `database`, `is_default`. Carries no connection, storage location, or secret. |
| `SeedReport` | Result of `Database.seed()`: `inserted` and `skipped` counts per Model and the `generated` secrets. |
| `GeneratedSecret` | One secret produced during seeding: `model`, `record`, `field`, `value`. Shown once; only its at-rest form is stored. |
| `CREDENTIAL_MASK` | What a consumer receives in place of a stored credential. Passing it back in an update leaves the credential unchanged. |
| `generate_encryption_key` | Produces a new key for the reversible at-rest mode. |
| `DatabaseError` | Base of every error below. |
| `ConfigurationError` | The layer configuration, or a secret it names, is missing or invalid. |
| `UnknownInstance` | The selected Instance was never declared. It is never answered with the default. |
| `ConnectionUnavailable` | The selected Instance could not be reached. No other Instance is used instead. |
| `InvalidOperation` | The operation is not valid for the given Model or arguments. |
| `InvalidData` | The data does not satisfy the Model's own declarations. `fields` names each refused field. |
| `NotFound` | No record matches the identifier. |
| `ConstraintViolation` | The change would break a rule this layer guarantees over stored data. |
| `UnsupportedRequirement` | A required rule cannot be enforced on the selected Engine. |

`Database` operations, each generic over every Model of `my_model`:

| Operation | Behaviour |
|---|---|
| `create(value)` or `create(Model, data)` | Stores a new record from a Model instance, or from a Model and its data. Data is checked by the shared Model validation first. A value still awaiting generation is refused. |
| `read(Model, key)` | Returns the record with the identifier, or raises `NotFound`. |
| `list(Model, criteria=None)` | Returns every record matching the equality criteria, in identifier order. Credential fields cannot be criteria. |
| `update(Model, key, changes)` | Changes only the supplied fields. An omitted field stays as it is; an explicit null is accepted only where the field permits it. |
| `delete(Model, key)` | Removes the record, or raises `NotFound`. |
| `status(Model, key, action)` | `enable` or `disable` a record of a Model that declares a `status` field. Any other action, or a Model without `status`, raises `InvalidOperation`. |
| `execute(statement, parameters=None, engine=None)` | Runs one parameterized data command and returns its rows. Values are bound, never interpolated. A command that would change the storage structure is refused. Name `engine` when the command is written for one Engine; it carries no promise of portability. |
| `transaction(instance=None)` | A context manager yielding a `Transaction`. |
| `verify_credential(Model, key, field, given)` | Whether `given` matches the stored credential, in any at-rest mode. |
| `recover_credential(Model, key, field)` | The original value of a credential stored in a recoverable mode. A hashed credential raises `InvalidOperation`. |
| `seed()` | Applies every Model's declared initial data as one unit and returns a `SeedReport`. Repeatable: existing records are skipped. |
| `close()` | Releases the engine connections. |

Model identity is always a Model type or instance from `my_model`; a bare name string raises `InvalidOperation`. Returned values are Model instances whose credential fields hold `CREDENTIAL_MASK`.

### The transaction boundary

Related operations are grouped so their changes commit together or not at all:

- the block completes normally, so every change in it commits together;
- the block raises, so every change in it is undone and the error propagates;
- `cancel()` ends the unit with nothing kept and no error escaping.

No operation inside a unit is durable before the unit completes, a write outside any unit is atomic on its own, and a unit belongs to exactly one Instance. After the block, `outcome` reads `committed` or `rolled back`. The connection is never handed over.

### Storage design

- Table names are the plural snake case of the Model name (`Currency` → `currencies`, `TradingPlatform` → `trading_platforms`); columns keep the field names. Each table's comment records its source Model and each column's comment its source field.
- Logical types map to engine-independent column types: integer, string with the declared size, boolean, decimal as numeric with precision 28 and scale 10, float, and datetime.
- Every relationship is a foreign key on its carrying field referencing the target's identifier, indexed as `ix_<table>_<column>`, with `RESTRICT` on delete and update. **Its optionality is the optionality the Model resolves for that field**; this layer applies no nullability default of its own.
- Rules that depend on stored data become guarantees enforced at commit: each unique field property, each composite uniqueness rule (for example `uq_brokers_user_id_name`), and the existence of every referenced record. Each records the declaration it implements.
- The at-rest mode of a credential field is the Model's explicit rule, otherwise the default for its name (`password` and `api_key` hash), otherwise plaintext. Here the User's password and API key are hashed and the Account's password is encrypted.

## Dependencies

- Python 3.14 or later.
- `my-model`, the shared Model package, consumed only through its public import interface (a local path dependency).
- `sqlalchemy` for the engine-independent storage design and operations, `alembic` for the migration history, `cryptography` for the reversible at-rest mode, and `pyyaml` to read the layer configuration.

The package is consumed by the Backend layer through its Data Access layer.

## Configuration

This layer owns which Engines it supports, which Instances it offers, and which one is the default, so those live in **this package's own configuration file, `database.yaml`, beside the package** and are validated before any data operation. It is located from the package itself, not from the working directory.

The `settings` section:

| Setting | Meaning | Example |
|---|---|---|
| `engines.<name>` | An Engine profile this layer implements an adapter for, with the settings its connections need. | `SQLite` |
| `instances.<key>.name` | The Instance's human-readable name. | `Trading Assistant General` |
| `instances.<key>.purpose` | What the Instance is for. | `General application data.` |
| `instances.<key>.engine` | Must name a declared Engine profile. | `SQLite` |
| `instances.<key>.database` | The database identity; the storage file name for a file-backed Engine. | `trading_assistant_general` |
| `instances.<key>.host`, `.port` | Server location; `engine_default` selects the Engine's port. Ignored by a file-backed Engine. | `localhost`, `engine_default` |
| `instances.<key>.username_secret`, `.password_secret` | Names of the runtime secrets holding connection credentials. | `TRADING_ASSISTANT_GENERAL_DATABASE_USERNAME` |
| `default_instance` | Must name a declared Instance. Used when a consumer selects none. | `general` |
| `credentials.encryption_key_secret` | Name of the runtime secret holding the key for the reversible at-rest mode. | `TRADING_ASSISTANT_DATABASE_ENCRYPTION_KEY` |

Cross-layer bindings live in `application.yaml` at the project root, under the `database` section; this layer binds to `my_model` through its import interface. Secrets are named in `.env.example` at the project root and supplied through `.env` or the process environment:

| Secret | Purpose |
|---|---|
| `TRADING_ASSISTANT_DATABASE_ENCRYPTION_KEY` | Key for the reversible at-rest mode. Generate one with `uv run python -m my_database generate-key`. |
| `TRADING_ASSISTANT_GENERAL_DATABASE_USERNAME` | Connection username of the `general` Instance (server Engines only). |
| `TRADING_ASSISTANT_GENERAL_DATABASE_PASSWORD` | Connection password of the `general` Instance (server Engines only). |

A file-backed Instance keeps its storage under `data/` inside this package, resolved from the package rather than the working directory, and never committed.

## Installation

The package is internal and is not published. Install it together with the Model package into the consuming environment, as an editable local dependency: this layer keeps its configuration beside its code, so it is consumed from its own tree rather than copied out of it.

```bash
uv pip install --editable path/to/model --editable path/to/database
```

Inside the package directory, `uv sync` creates the package's own isolated environment with every dependency, including the Model package, resolved.

### Creating the storage structure

The structure is created only by the migration history, run from the package directory:

```bash
uv run alembic upgrade head
```

`uv run alembic downgrade -1` reverses the latest migration. Pass `-x instance=<key>` to act on a declared Instance other than the default. Application code never creates or alters storage objects.

### Applying the initial data

```bash
uv run python -m my_database seed
```

The command inserts every declared initial record that is not already present and prints, once, any secret it generated (the Admin user's password and API key, the Acc-1 account's password). Those values are stored only in their at-rest form and cannot be printed again.

There is no service to start: `my_database` is an importable library plus the two commands above.

## Usage

Perform Model operations through the gateway:

```python
from my_model import Currency
from my_database import Database, NotFound

db = Database()
created = db.create(Currency, {"name": "Example Dollar", "code": "EXD", "symbol": "E$"})
assert created.id is not None and created.decimal_digits == 2

assert db.read(Currency, created.id) == created
assert [c.id for c in db.list(Currency, {"code": "EXD"})] == [created.id]

renamed = db.update(Currency, created.id, {"name": "Example Dollar (renamed)"})
assert renamed.code == "EXD"  # an omitted field stays as it was

assert db.status(Currency, created.id, "disable").status is False

db.delete(Currency, created.id)
try:
    db.read(Currency, created.id)
except NotFound:
    pass
else:
    raise AssertionError("expected NotFound")
db.close()
```

Group related operations so they succeed or fail together:

```python
from my_model import Currency
from my_database import Database, ConstraintViolation

db = Database()
with db.transaction() as unit:
    unit.create(Currency, {"name": "Unit One", "code": "UN1"})
    unit.create(Currency, {"name": "Unit Two", "code": "UN2"})
assert unit.outcome == "committed"

try:
    with db.transaction() as failing:
        failing.create(Currency, {"name": "Unit Three", "code": "UN3"})
        failing.create(Currency, {"name": "Clash", "code": "UN1"})  # already taken
except ConstraintViolation:
    pass
assert failing.outcome == "rolled back"
assert db.list(Currency, {"code": "UN3"}) == []   # neither change was kept

for code in ("UN1", "UN2"):
    db.delete(Currency, db.list(Currency, {"code": code})[0].id)
db.close()
```

Discover Instances and run a controlled command:

```python
from my_database import Database, InvalidOperation

db = Database()
registry = db.instances
assert registry.default.key == "general" and len(registry) >= 1

rows = db.execute(
    "SELECT count(*) AS n FROM currencies WHERE code = :code",
    {"code": "USD"},
    instance=registry.default,
)
assert rows[0]["n"] in (0, 1)

try:
    db.execute("DROP TABLE currencies")
except InvalidOperation:
    pass
else:
    raise AssertionError("a structural change must be refused")
db.close()
```

Work with credentials without ever seeing their stored form:

```python
from my_model import User
from my_database import Database, CREDENTIAL_MASK

db = Database()
user = db.create(User, {"name": "Example", "username": "example", "password": "s3cret", "api_key": "k3y"})
assert user.password == CREDENTIAL_MASK
assert db.verify_credential(User, user.id, "password", "s3cret")
assert not db.verify_credential(User, user.id, "password", "other")
db.delete(User, user.id)
db.close()
```
