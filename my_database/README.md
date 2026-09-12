# my_database

The persistence layer for the Trading Assistant Target, built on the shared `my_model` logical
Model package.

## Responsibilities and boundaries

`my_database` turns the `my_model` domain entities into stored data, keeps the whole storage
structure reproducible from the repository, and publishes one generic interface through which
every consumer reads and writes without ever meeting the engine behind it.

It does **not** decide domain names, fields, relationships, or domain rules — those belong to
`my_model`. It does not implement application behaviour, an HTTP API, or presentation — those
belong to Backend and Frontend. It owns only the persistence mapping and enforcement of what
`my_model` declares.

## The three internal layers

```
Database Interface  ->  Data Logic and Mapping  ->  Storage Adapter  ->  Engine
```

- **Database Interface** (`my_database.operations`, `my_database.transactions`,
  `my_database.sql`, `my_database.instances`) is the only boundary published to consumers.
- **Data Logic and Mapping** (internal `_pipeline`, `_mapping`, `_credentials`, `_orm`) implements
  the generic operation pipeline and resolves the physical mapping of every Model.
- **Storage Adapter** (internal `_session`, `_config`) owns the connection to the selected Engine.

Consumers never import an internal module (any module whose name starts with `_`); the public
submodules above are the entire contract.

## Installation

```bash
cd my_database
uv sync
uv run alembic upgrade head
```

`my_database` depends on `my_model` as a local path dependency; no external network install is
required beyond ordinary Python packages.

## Public interface and usage pattern

The canonical way to use the package is a module-qualified import:

```text
import my_database

my_database.operations.add(record)  # record: any my_model instance you already have
```

Every public operation is also re-exported from the package root as a convenience (for example,
`my_database.add`), but this never replaces the module-qualified interface as the canonical usage
pattern.

## Engine, runtime configuration, and Instances

The selected Engine is SQLite, mapped through SQLAlchemy. Non-secret runtime configuration
(Engine catalogue, Instance catalogue, default Instance) lives in the package's own
`database.yaml`. The public Instance Registry exposes selectable identities and the default
without ever exposing a connection or a secret value:

```python
import my_database

identities = my_database.instance_registry.list()
default = my_database.instance_registry.default
```

An omitted `instance` argument on any operation uses the configured default; an explicit unknown
Instance is rejected rather than silently redirected:

```python
try:
    my_database.instance_registry.resolve("does-not-exist")
except my_database.errors.UnknownInstanceError:
    ...
```

## Migrations

The storage schema never changes without a recorded Alembic migration:

```bash
uv run alembic upgrade head      # apply every recorded migration
uv run alembic downgrade -1      # reverse the most recent one
uv run alembic check             # detect drift between the mappings and the applied schema
```

Application code never creates or alters tables directly; only Migration does.

## Transactions

Related operations can be grouped in one atomic unit that commits together or rolls back
together; a standalone operation outside a group forms its own atomic unit. See the transaction
example below.

## Credential protection

`my_database` never decides which fields are credentials or how they must be protected: it reads
that decision from each field's own Model-declared metadata (`credential` and `storage_at_rest`).
A `hash`-designated field is transformed with an approved one-way scheme and a read never
recovers it — a read returns the fixed marker `"<redacted>"`. An `encrypted`-designated field is
reversible: a read decrypts it back to its original value. An explicit Model declaration always
takes precedence over any of Database's own generic field-name defaults (for example, `my_model`
declares `User.api_key` as `hash`, even though Database's own generic default for a field named
`api_key` is `encrypted`; the explicit Model declaration wins).

## Controlled SQL

For a data operation the generic pipeline cannot express, a capability-restricted, parameterized,
allow-listed controlled-SQL route is available. It rejects structural changes, privilege changes,
and migration operations before execution, and applies the same credential protection to its
results as the generic operations. See the example below.

## Boundary with other Components

- **Model** owns domain names, fields, relationships, rules, and initial-data declarations;
  `my_database` only maps and enforces them.
- **Backend** is the only application-layer consumer of this package's public interface.
- **Platform** delivers any Binding this layer needs through the selected Launch.
- **Development** owns the shared package and runtime-configuration conventions this package
  follows (its `database.yaml` and its `.secrets/` directory).

## Usage examples

Add a record from an imported Model type:

```python
import my_model
import my_database

user = my_database.add(
    my_model.User(id=0, name="Admin", username="admin", password="secret", api_key="key")
)
print(user.id)  # the storage structure assigned the real identity; the placeholder id=0 is discarded
```

Read one record by its typed identifier:

```python
fetched = my_database.read(my_model.User, user.id)
assert fetched.password == "<redacted>"  # a hash-designated credential never comes back
```

List records with deterministic ordering and pagination:

```python
page = my_database.list_records(my_model.User, limit=10, offset=0, order_by="id")
```

Update a record while preserving Model validation and partial-update semantics:

```python
updated = my_database.edit(my_model.User, user.id, {"description": "a note"})
assert updated.name == user.name  # omitted from the patch: unchanged
assert updated.description == "a note"  # supplied in the patch: replaced
```

Delete a record and observe the not-found result on a second read:

```python
my_database.delete(my_model.User, user.id)
try:
    my_database.read(my_model.User, user.id)
except my_database.errors.NotFoundError:
    print("deleted")
```

Enable or disable a Model that declares a `status` field:

```python
user2 = my_database.add(
    my_model.User(id=0, name="Second", username="second", password="x", api_key="y")
)
disabled = my_database.set_status(my_model.User, user2.id, "disable")
assert disabled.status is False
```

Select an Instance explicitly, and use the configured default when selection is omitted:

```python
default_key = my_database.instance_registry.default.key
same = my_database.read(my_model.User, user2.id, instance=default_key)
assert same.id == user2.id
```

Group related operations in one transaction and observe commit or rollback:

```python
try:
    with my_database.transaction() as session:
        broker = my_database.add(
            my_model.Broker(id=0, name="FxPro", user_id=user2.id), session=session
        )
        # A reference to a nonexistent Broker rolls the whole group back.
        my_database.add(
            my_model.Asset(id=0, broker_id=999999, symbol="EUR/USD", category="Currency"),
            session=session,
        )
except my_database.errors.ConstraintViolationError:
    print("transaction rolled back; the Broker above was not persisted either")
```

Handle a validation error, a not-found result, and a constraint failure:

```python
from pydantic import ValidationError

try:
    my_database.add(my_model.Currency(id=0, user_id=user2.id, code="US"))  # code must be 3 chars
except ValidationError:
    print("validation failed before any write was attempted")

try:
    my_database.read(my_model.User, 999999)
except my_database.errors.NotFoundError:
    print("not found")

my_database.add(my_model.User(id=0, name="Unique", username="u1", password="x", api_key="y"))
try:
    my_database.add(my_model.User(id=0, name="Unique", username="u2", password="x", api_key="y"))
except my_database.errors.ConstraintViolationError:
    print("uniqueness rule enforced")
```

Execute a parameterized controlled SQL command and observe protected results:

```python
rows = my_database.execute_controlled_sql(
    "SELECT id, name, password FROM users WHERE id = :id", {"id": user2.id}, table="users"
)
assert rows[0]["password"] == "<redacted>"

try:
    my_database.execute_controlled_sql("ALTER TABLE users ADD COLUMN hacked TEXT", {}, table="users")
except my_database.errors.ControlledSQLRejectedError:
    print("structural change rejected before execution")
```

Seed every Model-declared initial record (used once to bootstrap a fresh database):

```python
inserted = my_database.seed_initial_data()
print(inserted)  # {"User": 1, "TradingPlatform": 2, ...}
```
