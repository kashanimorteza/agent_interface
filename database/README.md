# Database

## Overview

Database persists the public Entities of the Model library and gives every consumer one stable data-access gateway. A consumer imports the `database` package, picks a `DatabaseInstance` (or accepts the default) and calls an Entity Operation, the Database-wide Operation, or a Lifecycle Command. Database validates the request, resolves the Instance, routes the work to that Instance's own implementation, and returns the result in one published form. A consumer never touches configuration, connection details, storage files or drivers.

- **Consumes Model through its public boundary only.** Entity classes and their Declarations come from `model`; Database derives tables, columns, keys, Relations, Uniqueness Constraints and Indexes from those Declarations and never changes Model.
- **Stores values as they are.** Database does not hash, encrypt, mask or otherwise interpret a Field because of its meaning (for example a password); the value you supply is the value stored and returned.
- **Instances.** The default set is a file-backed Instance (SQLite, default) and a server-based Instance (PostgreSQL). Each has its own implementation.

Layout of the Database Component:

```text
database/
├── src/database/
│   ├── interface.py        the only public boundary
│   ├── core/               validation, defaults, routing, configuration, lifecycle coordination
│   └── engine/             one complete implementation file per active Instance (owns its storage mechanics)
├── db/                     Database-owned persistent data files (no source)
├── config.yaml             generated runtime configuration (sole runtime source)
├── pyproject.toml, uv.lock
└── README.md
```

## Interface

Everything a consumer uses is published by `database` (the `database.interface` entrypoint re-exported by the package). Nothing else is public.

```python
from database import (
    CommandResult,
    Database,
    DatabaseInstance,
    Filter,
    FilterCombination,
    FilterOperator,
    LifecycleResult,
    Order,
    OrderDirection,
)
```

`Database` holds every capability as a static method, in three groups: **Entity Operations**, the **Database-wide Operation**, and **Lifecycle Commands**. Every capability accepts an optional `instance` (a `DatabaseInstance`) as its last parameter and uses the default Instance when it is omitted.

Entities are the public classes of the Model library (`from model import User, Currency, ...`). Operations that create or change a record receive an Entity **instance**; every other Operation receives the Entity **class**. An Entity is never selected by a name string.

The examples in this section run one after another against a prepared Instance (see [Lifecycle](#lifecycle)). Placeholder values such as `example-password` are not real credentials.

```python
from decimal import Decimal

from database import (
    Database, DatabaseInstance, Filter, FilterCombination, FilterOperator,
    Order, OrderDirection,
)
from model import Broker, Currency, PartialGroup, PartialRule, User

Database.create_tables()  # prepare the default Instance (see Lifecycle)
```

### Entity Operations

| Operation | Receives | Returns |
|---|---|---|
| `add(entity, instance=None)` | a complete new Entity instance (no `id`) | the stored Entity with its generated values |
| `update(entity, instance=None)` | a complete Entity instance carrying its `id` | the stored Entity, or `None` when no record has that `id` |
| `list(entity, filters=None, combination=None, orders=None, limit=None, instance=None)` | an Entity class | a list of matching Entities |
| `delete(entity, id, instance=None)` | an Entity class and an `id` | the last stored (now deleted) Entity, or `None` |
| `enable(entity, id, instance=None)` | an Entity class and an `id` | the final Entity, or `None` |
| `disable(entity, id, instance=None)` | an Entity class and an `id` | the final Entity, or `None` |
| `get_by_id(entity, id, instance=None)` | an Entity class and an `id` | the Entity, or `None` |
| `count(entity, filters=None, combination=None, instance=None)` | an Entity class | the number of matching records |
| `sum(entity, field, filters=None, combination=None, instance=None)` | an Entity class and a numeric Field name | the total, ignoring `null`; zero of the Field's type when nothing contributes |
| `min(entity, field, filters=None, combination=None, instance=None)` | an Entity class and a Field name | the minimum, ignoring `null`, or `None` |
| `max(entity, field, filters=None, combination=None, instance=None)` | an Entity class and a Field name | the maximum, ignoring `null`, or `None` |
| `truncate(entity, instance=None)` | an Entity class | the number of records deleted (the table is kept) |

**Add and GetById.** `add` stores a new record and returns the stored Entity, including the generated `id`. The object you passed is not modified.

```python
ada = Database.add(User(name="Ada", username="ada", password="example-password", api_key="example-key"))
assert ada.id is not None
assert Database.get_by_id(User, ada.id) == ada
assert Database.get_by_id(User, 424242) is None       # a missing record is None, not an error
```

**Update.** The Entity's `id` only locates the record; every other mutable Field is replaced (including back to `None`). A missing record returns `None`.

```python
ada.description = "Administrator"
updated = Database.update(ada)
assert updated is not None and updated.description == "Administrator"
```

**Enable and Disable.** Each changes only `is_active` and returns the final Entity, also when it already had that value.

```python
assert Database.disable(User, ada.id).is_active is False
assert Database.enable(User, ada.id).is_active is True
```

**List, Count.** Filters are combined by `combination` (default `AND`), sorted by `orders` (default `id` ascending) and capped by `limit` (default unlimited).

```python
broker = Database.add(Broker(name="ExampleBroker", user_id=ada.id))
for code, digits in (("USD", 2), ("JPY", 0), ("EUR", 2)):
    Database.add(Currency(user_id=ada.id, code=code, decimal_digits=digits))

two_digit = Database.list(
    Currency,
    filters=[Filter("decimal_digits", FilterOperator.EQUALS, 2)],
    orders=[Order("code", OrderDirection.DESCENDING)],
    limit=10,
)
assert [c.code for c in two_digit] == ["USD", "EUR"]

either = Database.count(
    Currency,
    filters=[Filter("code", FilterOperator.EQUALS, "JPY"), Filter("code", FilterOperator.EQUALS, "EUR")],
    combination=FilterCombination.OR,
)
assert either == 2
```

**Sum, Min, Max.** `null` values are ignored. An empty `sum` is a zero of the Field's own type (`0`, `0.0`, or `Decimal(0)`); an empty `min` or `max` is `None`.

```python
assert Database.sum(Currency, "decimal_digits") == 4
assert Database.min(Currency, "code") == "EUR" and Database.max(Currency, "code") == "USD"
assert Database.max(Currency, "code", filters=[Filter("code", FilterOperator.EQUALS, "nope")]) is None
```

**Delete and Truncate.** A record another record refers to cannot be deleted (no cascade is performed); that is an execution failure and nothing changes.

```python
jpy = Database.list(Currency, [Filter("code", FilterOperator.EQUALS, "JPY")])[0]
assert Database.delete(Currency, jpy.id) == jpy
assert Database.delete(Currency, jpy.id) is None
group = Database.add(PartialGroup(user_id=ada.id, name="ExampleGroup"))
Database.add(PartialRule(name="ExampleRule", partial_group_id=group.id,
                         profit_percentage=Decimal("10"), close_percentage=Decimal("50")))
assert Database.truncate(PartialRule) == 1
assert Database.count(PartialRule) == 0
```

**Every change is atomic.** An Operation that fails leaves no partial change, and separate calls never share a hidden transaction.

### Database-wide Operation

`execute_command(command, parameters=None, instance=None)` runs any valid SQL command the selected Instance supports, with named bound parameters (`:name`), and returns a `CommandResult`. It is not restricted: it may change the schema. Use `create_tables` for the standard schema preparation.

```python
result = Database.execute_command("select id, code from currencies where code = :code", {"code": "USD"})
assert result.success and result.columns == ["id", "code"] and result.rows[0]["code"] == "USD"

changed = Database.execute_command("update currencies set symbol = :s where code = :c", {"s": "$", "c": "USD"})
assert changed.affected == 1 and changed.rows is None
```

A command the Instance rejects raises an execution failure (see [Errors](#errors)); it does not return a result.

### Lifecycle Commands

`create_tables(instance=None)` and `insert_initial_data(instance=None)` prepare an Instance and return a `LifecycleResult`. They are documented in full under [Lifecycle](#lifecycle) below.

### Query vocabulary

Public requests use these closed sets; a plain string is never accepted where a member is required. Each is a `StrEnum`; `FilterOperator["EQUALS"]` resolves a member from its canonical name.

| `FilterOperator` | Meaning |
|---|---|
| `EQUALS`, `NOT_EQUALS` | equal / not equal to the value |
| `GREATER_THAN`, `GREATER_OR_EQUAL`, `LESS_THAN`, `LESS_OR_EQUAL` | ordered comparison with the value |
| `IN` | equal to any member of a collection of values |
| `CONTAINS`, `STARTS_WITH`, `ENDS_WITH` | exact, case-sensitive text match on a textual Field (`%` and `_` match literally) |
| `IS_NULL`, `IS_NOT_NULL` | the Field is / is not `null`; these take no value |

| `FilterCombination` | Meaning |
|---|---|
| `AND` | every Filter must match (default) |
| `OR` | at least one Filter must match |

| `OrderDirection` | Meaning |
|---|---|
| `ASCENDING` | smallest first (default); `null` counts as the smallest value, so it comes first |
| `DESCENDING` | largest first; `null` comes last |

### Query values

`Filter(field, operator, value)` and `Order(field, direction=OrderDirection.ASCENDING)` are immutable. A Filter's `value` must be omitted for `IS_NULL` and `IS_NOT_NULL`, must be a collection for `IN`, and must be compatible with the Field: an integer for an integer Field, `int` or `float` for a float Field, `Decimal` or `int` for a decimal Field, text for a text Field, a boolean for a boolean Field, and a time zone aware `datetime` for a datetime Field. Textual operators need a textual Field. Every named Field is validated against the Entity before any Instance is used.

```python
Filter("code", FilterOperator.IN, ["USD", "EUR"])   # a collection
Filter("symbol", FilterOperator.IS_NULL)            # no value
Order("code")                                       # ascending
```

### DatabaseInstance

`DatabaseInstance` has exactly one member for each active Instance and no others; a member carries no connection detail. See [Instances](#instances).

### Defaults

| Part | Default when omitted |
|---|---|
| `instance` | the configured default Instance |
| `combination` | `AND` (configured) |
| `orders` (List only) | `Order("id", ASCENDING)` |
| an `Order` without a direction | `ASCENDING` |
| `limit` (List only) | unlimited (`-1`); `0` and every negative value also mean unlimited; a positive value is the maximum count |

Supplied `orders` replace the default order and apply in the order given. Only `list` accepts `orders` and `limit`; the aggregate Operations do not.

### Results

`CommandResult` (from `execute_command`):

| Part | Meaning |
|---|---|
| `rows` | returned rows as dictionaries, or `None` |
| `affected` | affected row count, or `None` for a row-returning command |
| `columns` | ordered column names, or `None` |
| `success` | whether the command executed |
| `message` | a public message |
| `instance` | the `DatabaseInstance` used |

`LifecycleResult` (from a Lifecycle Command):

| Part | Meaning |
|---|---|
| `command` | `"create_tables"` or `"insert_initial_data"` |
| `instance` | the `DatabaseInstance` used |
| `success` | whether the command completed |
| `affected` | tables aligned or records inserted, or `None` |
| `message` | a public message |

### Errors

Every failure is a distinct class and carries a stable `meaning` string. The classes are not published names; catch them by the built-in type below or by `meaning`. No failure contains a credential or a value you supplied.

| Meaning (`error.meaning`) | Built-in base | Raised when |
|---|---|---|
| `invalid_configuration` | `ValueError` | the configuration, or the selected Instance, is invalid |
| `inactive_instance` | `LookupError` | the selected Instance is not active |
| `invalid_input` | `ValueError` | a request, Field, or Initial Data record is invalid |
| `declaration_incompatibility` | `TypeError` | stored structure and a Declaration differ in a way that cannot be aligned safely |
| `connection_failure` | `ConnectionError` | the Instance cannot be reached |
| `execution_failure` | `RuntimeError` | the Instance rejected the request (constraint, Relation, unsupported value, invalid SQL) |
| `incomplete_lifecycle` | `RuntimeError` | a Lifecycle Command could not complete (for example missing tables) |

```python
try:
    Database.delete(User, ada.id)          # ada owns a broker: a Relation refuses this
except RuntimeError as error:
    assert error.meaning == "execution_failure"
    assert Database.get_by_id(User, ada.id) is not None   # nothing changed
```

A missing record is never a failure: `get_by_id`, `update`, `delete`, `enable` and `disable` return `None`.

## Instances

An Instance is one named database connection with its own storage. `DatabaseInstance` has one member for each **active** Instance and none for an inactive one:

| Member | Instance | Kind | Default |
|---|---|---|---|
| `DatabaseInstance.SQLITE` | SQLite | file-backed | yes |
| `DatabaseInstance.POSTGRESQL` | PostgreSQL | server-based | no |

Select an Instance per call; omit it to use the default Instance.

```python
from database import Database, DatabaseInstance
from model import User

Database.list(User)                                       # the default Instance
Database.list(User, instance=DatabaseInstance.SQLITE)     # explicitly
Database.list(User, instance=DatabaseInstance.POSTGRESQL) # server-based (prepare it with create_tables first)
```

Selecting anything that is not a `DatabaseInstance` member raises `invalid_configuration`; selecting a member whose Instance is not active raises `inactive_instance`.

Connection values (host, port, database, user, password) live only in the generated configuration (`config.yaml` at the Database Component root) and are never repeated in a request, a member, an error, or this document. Active membership is decided by that configuration: when it changes, Database is regenerated so the members and Instance implementations match again, and a mismatch is refused when the configuration loads.

### Storage

- **File-backed Instance.** Its data file lives in the Database-owned `db` directory of the Database Component (`db/application.db` by default). The location is resolved from the Component itself, so it does not depend on the working directory, on a virtual environment, or on the consuming Component; Database must run from an editable installation of its Component (see [Setup](#setup)). A configured location that would leave `db` (an absolute path or `..`) is refused before any connection is made. Only Database creates and manages files there.
- **Server-based Instance.** Its data lives on the configured server; Database connects with the configured host, port, database, user and password (5 second connect timeout). An unreachable server or a missing required connection value raises `connection_failure`, without revealing the password.
- **Values.** Integers are 64-bit; an integer outside that range, or text containing a NUL character, is refused (`invalid_input`) on every Instance. Text is compared and ordered byte by byte on every Instance: matching is case-sensitive and ordering does not depend on a server's locale (the server-based Instance creates text columns with byte-order collation; a table created earlier keeps its own). Datetimes must be time zone aware and are stored and returned as UTC instants (equal instants compare equal). Decimals support up to 12 decimal places and 26 integer digits; a decimal beyond that is refused (`execution_failure`), never rounded. The file-backed Instance stores decimals as doubles, so it accepts only decimals that a double reproduces exactly (about 15 significant digits) and refuses the rest; the server-based Instance stores them exactly. Decimal `sum` is exact on both.



## Setup

Requirements: Python 3.14 or newer and [uv](https://docs.astral.sh/uv/). Database uses the Model library from the sibling `model` directory.

```text
cd database
uv sync                      # installs the pinned dependencies and Database itself (editable)
uv run database-prepare      # prepares the default Instance: create tables, then insert Initial Data
```

To use Database from another Component, declare it (and Model) as **editable path dependencies**, for example `uv add --editable ../database ../model`. Database resolves its configuration and its `db` storage directory from its own Component location, so it must run from an editable installation of that Component; an installed copy without them cannot find its configuration and fails with `invalid_configuration` on first use.

The server-based Instance needs a reachable server and the connection values in `config.yaml`; the file-backed Instance needs nothing else.

Quality checks used for this Component (run from the Component directory):

```text
uv run ruff format --check src
uv run ruff check src
uv run pyright
```

## Use

A typical workflow: prepare the Instance once, then add, query and change records through `Database`; select another Instance only when you need it.

```python
from database import Database, DatabaseInstance, Filter, FilterOperator, Order
from model import User

Database.create_tables()                                    # once per Instance; safe to repeat
user = Database.add(User(name="Grace", username="grace", password="example-password", api_key="example-key"))
matches = Database.list(User, [Filter("username", FilterOperator.STARTS_WITH, "gr")], orders=[Order("name")])
assert matches == [user]
Database.disable(User, user.id)
assert Database.count(User, [Filter("is_active", FilterOperator.EQUALS, False)]) == 1
```

## Lifecycle

Two Lifecycle Commands prepare an Instance. Both accept an optional `DatabaseInstance` (default: the default Instance), return a `LifecycleResult`, and can be run from code or by hand.

### CreateTables

`Database.create_tables(instance=None)` creates every table the current public Entity Declarations require (Fields, Primary Keys, Relations, Uniqueness Constraints, Indexes) or safely aligns existing ones. It is safe to repeat.

```python
from database import Database, DatabaseInstance

result = Database.create_tables(DatabaseInstance.SQLITE)
assert result.success and result.command == "create_tables" and result.affected == 15
assert Database.create_tables(DatabaseInstance.SQLITE).success      # repeat: nothing changes
```

- Missing tables, missing indexes, and missing columns that are nullable or have a default are added. Data is never touched.
- Anything else that differs (an extra column, a missing not-null column without a default, a changed constraint, a wrong type) is destructive or incompatible: **nothing** is applied and the command raises `declaration_incompatibility`.
- Tables that Database does not own are ignored.
- The whole alignment is one transaction on both Instances, so a failure leaves no half-prepared schema.

### InsertInitialData

`Database.insert_initial_data(instance=None)` inserts the shared **Initial Data** that is missing. Initial Data is one collection in the configuration, shared by every Instance, keyed by the public Entity class name:

```yaml
initial_data:
  - entity: Currency
    records:
      - {user_id: 1, code: "USD", symbol: "$", country: "United States", decimal_digits: 2}
```

- Each record is validated through its public Entity, so an unknown Field, a wrong type, a missing required Field, or a supplied generated `id` is refused (`invalid_input`, naming Fields only) before anything is inserted.
- A missing record is inserted; an identical record that is already present is skipped, so the command is safe to repeat.
- A record that matches an existing record on a Uniqueness Constraint but differs in any value is a **conflict**: the command fails (`execution_failure`) and the existing record is not overwritten. Existing records are never updated or deleted.
- The whole insertion is atomic: if any record fails, none is inserted.
- With no Initial Data declared it succeeds with `affected == 0`; otherwise the Instance's tables must exist, else it raises `incomplete_lifecycle`.

The shared collection currently declares no records.

### Manual use

Each command has an entry point that calls the same public command and returns the same result; it adds no logic of its own. Run them from the Database Component with the project environment:

```text
uv run database-create-tables
uv run database-insert-initial-data
uv run database-create-tables --instance postgresql
uv run database-prepare
```

Each prints one line per command (`<command> on <instance>: ok - <message>`) and exits `0`; on failure it prints `<meaning>: <message>` to standard error and exits `1`.

### After generation

When enabled in the configuration, generation prepares the default Instance by running `create_tables` and then `insert_initial_data`, in that order (`database-prepare` repeats exactly that sequence). If `create_tables` fails, `insert_initial_data` does not run and preparation fails with a message naming the Instance and the command. Other Instances are prepared only when you select them explicitly.

## Verify

Run this script from the Database Component (it needs a prepared default Instance: `uv run database-prepare`). It checks public import, Instance selection, the query vocabulary, each capability group, the persistent file location and the repeatable Lifecycle Commands, and it removes everything it adds. It prints `verified` when every check holds.

```python
from pathlib import Path

import database
from database import (
    CommandResult, Database, DatabaseInstance, Filter, FilterCombination,
    FilterOperator, LifecycleResult, Order, OrderDirection,
)
from model import Broker, User

# 1. Public import: exactly the published symbols.
assert set(database.__all__) == {
    "CommandResult", "Database", "DatabaseInstance", "Filter", "FilterCombination",
    "FilterOperator", "LifecycleResult", "Order", "OrderDirection",
}

# 2. Instance selection: members exist for the active Instances; the default works when omitted.
assert DatabaseInstance.SQLITE in DatabaseInstance
assert Database.count(User) == Database.count(User, instance=DatabaseInstance.SQLITE)

# 3. Query vocabulary: typed members resolve from canonical names; free strings are refused.
assert FilterOperator["IN"] is FilterOperator.IN and OrderDirection["DESCENDING"] and FilterCombination["OR"]
try:
    Filter("id", "EQUALS", 1)
    raise AssertionError("a string operator must be refused")
except ValueError as error:
    assert error.meaning == "invalid_input"

# 4. Each capability group.
assert Database.create_tables().success and Database.create_tables().success          # Lifecycle, repeatable
user = Database.add(User(name="verify-user", username="verify-user", password="example-password", api_key="example-key"))
try:
    assert Database.get_by_id(User, user.id) == user                                     # Entity Operations
    assert Database.list(User, [Filter("username", FilterOperator.EQUALS, "verify-user")]) == [user]
    assert Database.disable(User, user.id).is_active is False and Database.enable(User, user.id).is_active
    assert Database.count(User, [Filter("id", FilterOperator.EQUALS, user.id)]) == 1
    result = Database.execute_command("select id from users where id = :id", {"id": user.id})   # Database-wide
    assert isinstance(result, CommandResult) and result.rows == [{"id": user.id}]
    assert isinstance(Database.insert_initial_data(), LifecycleResult)                   # Lifecycle, repeatable
    assert Database.insert_initial_data().affected == 0
finally:
    Database.delete(User, user.id)
assert Database.get_by_id(User, user.id) is None

# 5. Persistent file location: the data file is inside the Database Component's db directory.
component = Path(database.__file__).resolve().parents[2]
assert (component / "db" / "application.db").is_file()
print("verified")
```

## Troubleshooting

| Symptom (`error.meaning`) | Cause | Fix |
|---|---|---|
| `invalid_configuration`: "The runtime configuration cannot be read" | Database is not running from an editable installation of its Component | Install it as an editable path dependency (see Setup) |
| `invalid_configuration`: "An active Instance has no DatabaseInstance member" or "Engine files do not match the active Instances" | the configuration's active Instances changed without regenerating Database | Regenerate Database so members and Instance implementations match the configuration |
| `invalid_configuration`: names a configuration part | `config.yaml` is invalid | Correct the named part; the message never includes a value |
| `inactive_instance` | the selected Instance is not active | Select an active Instance, or activate it and regenerate |
| `connection_failure` | the server-based Instance is unreachable or a required connection value is missing | Start the server, or correct host, port, database, user or password in `config.yaml` |
| `incomplete_lifecycle`: "Tables are missing" | Initial Data is declared but the Instance has no tables | Run `create_tables` for that Instance first |
| `declaration_incompatibility` | the stored tables differ from the Declarations in a way that cannot be applied safely (extra column, changed constraint, missing not-null column without default) | Resolve the difference in the database (nothing was changed), then run `create_tables` again |
| `execution_failure`: "violates a Relation or a Uniqueness Constraint" | a duplicate, a missing related record, or deleting a record that others refer to | Fix the data; the failed request changed nothing |
| `execution_failure`: "cannot hold the value exactly" / "exceeds the supported precision" | a decimal the Instance cannot store without altering it | Use a value with at most 12 decimals (and, on the file-backed Instance, about 15 significant digits) |
| `invalid_input` | the request or a Field is invalid (a string used as an Entity, an unknown Field, an incompatible value, a naive datetime, an integer beyond 64 bits, text containing NUL) | Correct the request; the message names the problem, never your value |
| a data file appears or is missing elsewhere than `db/` | Database is not run from its own Component | Use an editable installation; the location is fixed to the Component's `db` directory |
