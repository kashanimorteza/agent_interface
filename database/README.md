# Database

## Overview

Database is the storage library of the Trading Assistant. It stores and retrieves the Entities that the Model
publishes, behind one public Interface. A consumer never touches a connection, a driver, a file path, or the
configuration: it creates a `Database`, passes Entities, Field references, and enumeration members, and gets
Entities and results back.

```python
from database.interface import Database
from model.interface import Currency

database = Database()
stored = database.add(Currency(user_id=1, code="SEK", symbol="kr", country="Sweden"))
print(stored.id, [currency.code for currency in database.list(Currency)])
database.delete(Currency, stored.id)
```

The example adds one Currency and lists every Currency; the last line removes the Currency again so the example
can be run repeatedly.

## Interface

`database.interface` is the only entry point. It publishes exactly five groups and nothing else:

| Group | Members |
|---|---|
| **Database** | `Database` |
| **Setup** | `Setup` |
| **Value** | `Filter`, `FilterOperator`, `FilterCombination`, `Order`, `OrderDirection`, `DatabaseInstance` |
| **Result** | `CommandResult`, `SetupResult` |
| **Error** | `DatabaseError`, `ConfigurationError`, `InactiveInstanceError`, `InvalidInputError`, `DeclarationMismatchError`, `ConnectionFailureError`, `ExecutionError`, `LifecycleError` |

Every Operation passes Entities, Fields, Instances, operators, combinations, and directions as imported values and
never as strings. Every Operation takes exactly the parameters listed here, in this order. Every parameter after
`entity`, `id`, `field`, and `command` is optional, and `instance` is always last.

### Common rules

- **Entity.** `entity` is the Entity itself, imported from `model.interface`: a new Entity instance for `add` and
  `update`, and the Entity class for every other Operation. A name such as `"User"` is refused with
  `InvalidInputError`.
- **Field reference.** A Field is named by the Entity's class attribute, such as `User.name`. A string is refused.
- **Instance.** `instance` is an optional `DatabaseInstance` member. Without it the call runs on the default
  Instance.
- **A missing record** is never an error: Operations that look a record up return `None`.
- **Atomic.** Every changing Operation either completes or changes nothing.

### Database

Create it once with `Database()`. It holds the Entity Operations and the Command Operation.

#### `add(entity, instance=None)`

Stores one complete new Entity (its `id` still pending) and returns the stored Entity, including the generated
`id`.

```python
from database.interface import Database
from model.interface import Broker

database = Database()
stored = database.add(Broker(name="Example Broker", user_id=1))
print(stored.id, stored.name, stored.is_active)
database.delete(Broker, stored.id)
```

#### `update(entity, instance=None)`

Takes one complete Entity whose `id` locates the stored record, replaces every mutable Field, and never changes the
`id`. Returns the stored Entity, or `None` when no record has that `id`.

```python
from database.interface import Database
from model.interface import Broker

database = Database()
stored = database.add(Broker(name="Example Broker", user_id=1))
stored.description = "Updated through the Interface"
print(database.update(stored).description)
database.delete(Broker, stored.id)
```

#### `list(entity, filters=None, combination=None, orders=None, limit=None, instance=None)`

Returns a list of the matching Entities.

- `filters` is a list of `Filter` values; without it every record matches.
- `combination` is `FilterCombination.AND` (the default: every Filter must hold) or `FilterCombination.OR`.
- `orders` is a list of `Order` values applied in the order given; without it the records are ordered by `id`
  ascending. Supplied Orders replace the default.
- `limit` is the maximum number of Entities returned; `None`, zero, or a negative number means no limit.

```python
from database.interface import Database, Filter, FilterOperator, Order, OrderDirection
from model.interface import Currency

database = Database()
rich = database.list(
    Currency,
    filters=[Filter(Currency.decimal_digits, FilterOperator.EQUALS, 2)],
    orders=[Order(Currency.code, OrderDirection.DESCENDING)],
    limit=3,
)
print([currency.code for currency in rich])
```

#### `get_by_id(entity, id, instance=None)`

Returns the Entity with that `id`, or `None`.

```python
from database.interface import Database
from model.interface import Currency

database = Database()
first = database.list(Currency, limit=1)[0]
print(database.get_by_id(Currency, first.id).code, database.get_by_id(Currency, 0))
```

#### `delete(entity, id, instance=None)`

Removes the record and returns the Entity as it was when deleted, or `None` when no record has that `id`.

```python
from database.interface import Database
from model.interface import Broker

database = Database()
stored = database.add(Broker(name="Example Broker", user_id=1))
print(database.delete(Broker, stored.id).name, database.delete(Broker, stored.id))
```

#### `enable(entity, id, instance=None)` and `disable(entity, id, instance=None)`

Set only `is_active`, to `True` and `False`. Both return the final Entity, also when the record was already in that
state, or `None` when no record has that `id`.

```python
from database.interface import Database
from model.interface import Broker

database = Database()
stored = database.add(Broker(name="Example Broker", user_id=1))
print(database.disable(Broker, stored.id).is_active, database.enable(Broker, stored.id).is_active)
database.delete(Broker, stored.id)
```

#### `count(entity, filters=None, combination=None, instance=None)`

Returns how many records match; `filters` and `combination` work as in `list`.

```python
from database.interface import Database, Filter, FilterOperator
from model.interface import Currency

database = Database()
print(
    database.count(Currency),
    database.count(Currency, [Filter(Currency.code, FilterOperator.STARTS_WITH, "E")]),
)
```

#### `sum(entity, field, filters=None, combination=None, instance=None)`

Returns the total of one numeric Field (`integer`, `float`, or `decimal`) over the matching records. Null values are
ignored. When nothing matches the result is zero (`0`, `0.0`, or `Decimal("0")`, following the Field).

```python
from database.interface import Database
from model.interface import Currency

database = Database()
print(database.sum(Currency, Currency.decimal_digits))
```

#### `min(entity, field, filters=None, combination=None, instance=None)` and `max(...)`

Return the smallest and the largest non-null value of one comparable Field (every Type except `boolean`) over the
matching records, or `None` when nothing matches. Decimals compare as numbers and datetimes as instants.

```python
from database.interface import Database
from model.interface import Currency

database = Database()
print(database.min(Currency, Currency.code), database.max(Currency, Currency.decimal_digits))
```

#### `truncate(entity, instance=None)`

Removes every record of the Entity and keeps its Table. Returns the number of records removed.

```python
from database.interface import Database
from model.interface import Position

database = Database()
print(database.truncate(Position))
```

#### `execute_command(command, parameters=None, instance=None)`

Runs a native command in the query language of the Instance's Engine and returns a `CommandResult`. `parameters` is
a mapping whose names are bound to the `:name` markers of the command. A command may change the schema; use
`Setup.create_tables` as the standard way to prepare the Tables.

```python
from database.interface import Database

database = Database()
result = database.execute_command(
    "SELECT code FROM Currency WHERE decimal_digits = :digits", {"digits": 0}
)
print([row["code"] for row in result.rows], result.columns, result.success)
```

### Setup

Create it with `Setup()`. It holds the Setup Operations, which prepare the storage of an Instance. Each takes only
`instance=None` and returns a `SetupResult`. See [Setup Operations](#setup-operations) for when to run them.

#### `create_tables(instance=None)`

Creates the Table of every Model Entity and nothing else. Tables that already match their Entity are left
unchanged. A Table that differs from its Entity stops the Setup Operation with `DeclarationMismatchError` before
anything is created.

```python
from database.interface import Setup

print(Setup().create_tables().message)
```

#### `insert_initial_data(instance=None)`

Inserts every missing record of the configured Initial Data, skips a record that is already present and identical,
and fails with `ExecutionError`, changing nothing, when a stored record conflicts with a configured one.

```python
from database.interface import Setup

print(Setup().insert_initial_data().message)
```

#### `prepare(instance=None)`

Runs `create_tables` and then `insert_initial_data`. It stops without inserting when `create_tables` fails.

```python
from database.interface import Setup

print(Setup().prepare().message)
```

### Value

#### `FilterOperator`

The operators of a `Filter`. Each member's value equals its name.

| Member | Meaning | Value |
|---|---|---|
| `EQUALS` | the Field equals the value | one value |
| `NOT_EQUALS` | the Field differs from the value (records whose Field is null do not match; use `IS_NULL`) | one value |
| `GREATER_THAN` | the Field is greater | one value |
| `GREATER_OR_EQUAL` | the Field is greater or equal | one value |
| `LESS_THAN` | the Field is smaller | one value |
| `LESS_OR_EQUAL` | the Field is smaller or equal | one value |
| `IN` | the Field equals one of the values | a list of values |
| `CONTAINS` | the text Field contains the text | text |
| `STARTS_WITH` | the text Field starts with the text | text |
| `ENDS_WITH` | the text Field ends with the text | text |
| `IS_NULL` | the Field is null | none |
| `IS_NOT_NULL` | the Field is not null | none |

`CONTAINS`, `STARTS_WITH`, and `ENDS_WITH` need a text Field and treat `%` and `_` in the text literally. The four
ordering comparisons are refused for a `boolean` Field. A value must suit the Field's Type: an integer is accepted
for a `decimal` or `float` Field, a `datetime` must carry a timezone, and nothing else is converted.

#### `Filter(field, operator, value=None)`

An immutable condition. `field` is a Field reference such as `Currency.code`, `operator` is a `FilterOperator`
member, and `value` is omitted for `IS_NULL` and `IS_NOT_NULL` and required for every other operator.

```python
from database.interface import Filter, FilterOperator
from model.interface import Currency

condition = Filter(Currency.code, FilterOperator.IN, ["USD", "EUR"])
print(condition.operator.name, condition.value)
```

#### `FilterCombination`

How several Filters combine: `AND` (all must hold, the default) or `OR` (at least one must hold).

```python
from database.interface import Database, Filter, FilterCombination, FilterOperator
from model.interface import Currency

database = Database()
either = [
    Filter(Currency.code, FilterOperator.EQUALS, "USD"),
    Filter(Currency.code, FilterOperator.EQUALS, "JPY"),
]
print(database.count(Currency, either, FilterCombination.OR))
```

#### `Order(field, direction=OrderDirection.ASCENDING)` and `OrderDirection`

An immutable ordering. `OrderDirection` has the members `ASCENDING` and `DESCENDING`. Orders given to `list` apply in
the order given.

```python
from database.interface import Order, OrderDirection
from model.interface import Currency

print(
    Order(Currency.code).direction.name,
    Order(Currency.code, OrderDirection.DESCENDING).direction.name,
)
```

#### `DatabaseInstance`

The Instances you can select. It has one member for every active Instance and carries no connection values. The
member `SQLITE` selects the default Instance; omitting `instance` selects the same one.

```python
from database.interface import Database, DatabaseInstance
from model.interface import Currency

database = Database()
print(
    [member.name for member in DatabaseInstance],
    database.count(Currency, instance=DatabaseInstance.SQLITE),
)
```

### Result

#### `CommandResult`

The immutable result of `execute_command`, with the fields `rows`, `affected`, `columns`, `success`, `message`, and
`instance`.

| Field | Meaning |
|---|---|
| `rows` | a tuple of read-only row mappings, or `None` when the command returns no rows |
| `affected` | the number of rows the command changed, or `None` when unknown or when rows were returned |
| `columns` | a tuple of the column names in order, or `None` |
| `success` | `True` (a failing command raises `ExecutionError` instead) |
| `message` | a public message |
| `instance` | the `DatabaseInstance` used |

#### `SetupResult`

The immutable result of a Setup Operation, with the fields `command`, `instance`, `success`, `affected`, and
`message`: the Setup Operation's name, the `DatabaseInstance` used, `True`, the number of Tables or records
processed, and a public message that says how many were created or inserted.

```python
from database.interface import Setup

result = Setup().prepare()
print(result.command, result.instance.name, result.success, result.affected)
```

### Error

Every failure is an error derived from `DatabaseError`, so one `except DatabaseError` catches them all. No error
carries a connection value or a credential.

| Error | Raised when |
|---|---|
| `DatabaseError` | the base of all the errors below |
| `ConfigurationError` | the configuration is invalid or an Instance is not configured |
| `InactiveInstanceError` | an inactive Instance is selected |
| `InvalidInputError` | an argument or Field reference is invalid, or a string is passed where an imported value is required |
| `DeclarationMismatchError` | an existing Table differs from the Declaration of its Entity |
| `ConnectionFailureError` | the storage of the Instance cannot be reached |
| `ExecutionError` | a request reached the storage and failed there, or a stored row does not satisfy its Entity |
| `LifecycleError` | preparation stopped part way and left an incomplete state |

```python
from database.interface import Database, DatabaseError, InvalidInputError

try:
    Database().count("Currency")
except InvalidInputError as error:
    print(type(error).__name__, isinstance(error, DatabaseError))
```

## Instances

An Instance is one named database connection and storage identity. The Database ships with two declared Instances:

- **`SQLITE`** is active and is the default. It is file-backed.
- **`PostgreSQL`** is declared but inactive. An inactive Instance has no `DatabaseInstance` member and cannot be
  selected.

`DatabaseInstance` has exactly one member for every active Instance, and every Operation and Setup Operation takes
an optional member. Omit it to use the default Instance. Connection values never appear in a member, a result, or an
error.

```python
from database.interface import Database, DatabaseInstance
from model.interface import Currency

database = Database()
print(database.count(Currency) == database.count(Currency, instance=DatabaseInstance.SQLITE))
```

The Database owns its storage. A file-backed Instance keeps its database file in the `db` directory next to
`pyproject.toml`, creates that directory on first use, and never resolves the file from the working directory, an
installed package, a virtual environment, or the consumer. The file is runtime data and is ignored by version
control.

## Setup

Requirements: Python 3.14 or newer and [uv](https://docs.astral.sh/uv/). The Model must sit beside the Database in
the same repository, because the Database depends on it as a local project dependency.

```sh
cd database
uv sync
```

`uv sync` creates the isolated environment in `.venv` from `pyproject.toml` and `uv.lock` and installs the Model from
its sibling directory. Run Python in that environment with `uv run python`. Then prepare the default Instance, as
described under [Setup Operations](#setup-operations).

## Use

Everything goes through `database.interface` and the Model's Entities. Entities, Field references, and enumeration
members are always imported values, never strings.

```python
from database.interface import (
    Database,
    DatabaseError,
    DatabaseInstance,
    Filter,
    FilterCombination,
    FilterOperator,
    Order,
    OrderDirection,
)
from model.interface import Asset, Broker, Currency

database = Database()

# Add, read, change, and remove a record.
broker = database.add(Broker(name="Use Example", user_id=1))
broker.description = "changed"
database.update(broker)
print(database.get_by_id(Broker, broker.id).description)
database.disable(Broker, broker.id)
print(database.count(Broker, [Filter(Broker.is_active, FilterOperator.EQUALS, False)]))
database.delete(Broker, broker.id)

# Narrow, combine, order, and limit what is read.
cheap = database.list(
    Asset,
    filters=[
        Filter(Asset.category, FilterOperator.EQUALS, "Commodity"),
        Filter(Asset.symbol, FilterOperator.ENDS_WITH, "Oil"),
    ],
    combination=FilterCombination.OR,
    orders=[Order(Asset.digits, OrderDirection.DESCENDING)],
    limit=2,
    instance=DatabaseInstance.SQLITE,
)
print([asset.symbol for asset in cheap])

# Read aggregates and handle a failure through the base error.
print(
    database.max(Currency, Currency.decimal_digits), database.sum(Currency, Currency.decimal_digits)
)
try:
    database.get_by_id(Currency, "1")
except DatabaseError as error:
    print(type(error).__name__)
```

## Setup Operations

The Setup Operations prepare the storage of an Instance. They are separate from the Operations, so an everyday call
never changes the schema or seeds data. Each returns a `SetupResult`, and each is safe to repeat.

| Setup Operation | Effect |
|---|---|
| `create_tables` | Creates the Table of every Model Entity. Matching Tables are left unchanged. |
| `insert_initial_data` | Inserts every missing Initial Data record and skips records that are already present. |
| `prepare` | Runs `create_tables` and then `insert_initial_data`. |

Run them from Python through `Setup`, or by hand with the three entry points, which run the same Setup Operation on
the default Instance and print its result:

```sh
uv run python scripts/create_tables.py
uv run python scripts/insert_initial_data.py
uv run python scripts/prepare.py
```

An entry point exits with status 1 and prints the failure when the Setup Operation fails. Generation runs `prepare`
the same way on the default Instance, and a failure fails the generation.

## Initial Data

`insert_initial_data` inserts the records below, which the Target defines. The Database inserts every value
unchanged and never omits a record because of what a Field means. A value the Target leaves to be generated securely
(`password` and `api_key` of the User and the Instance, and `password` of the Account) is stored as empty text;
fill it later. Records are inserted in this order, so every record exists before the records that refer to it.

Every record lists all of its Fields except `id`, which storage generates. `Trailing Rule`, `Partial Rule`, and
`Position` have no Initial Data.

#### User

| name | username | password | api_key | is_active | description |
|---|---|---|---|---|---|
| `Admin` | `admin` | `""` | `""` | `true` | `null` |

#### TradingPlatform

| name | code | is_active | description |
|---|---|---|---|
| `MetaTrader 5` | `metatrader_5` | `true` | `null` |
| `Binance` | `binance` | `true` | `null` |

#### Instance

| user_id | trading_platform_id | name | ip | username | password | api_key | is_active | description |
|---|---|---|---|---|---|---|---|---|
| `1` | `1` | `MetaTrader` | `127.0.0.1` | `test` | `""` | `""` | `true` | `null` |

#### Currency

| user_id | code | symbol | country | decimal_digits | is_active | description |
|---|---|---|---|---|---|---|
| `1` | `USD` | `$` | `United States` | `2` | `true` | `null` |
| `1` | `EUR` | `€` | `Eurozone` | `2` | `true` | `null` |
| `1` | `GBP` | `£` | `United Kingdom` | `2` | `true` | `null` |
| `1` | `JPY` | `¥` | `Japan` | `0` | `true` | `null` |
| `1` | `CHF` | `CHF` | `Switzerland` | `2` | `true` | `null` |
| `1` | `CAD` | `C$` | `Canada` | `2` | `true` | `null` |
| `1` | `AUD` | `A$` | `Australia` | `2` | `true` | `null` |
| `1` | `NZD` | `NZ$` | `New Zealand` | `2` | `true` | `null` |

#### Broker

| name | user_id | is_active | description |
|---|---|---|---|
| `FxPro` | `1` | `true` | `null` |

#### Asset

| broker_id | symbol | category | point_size | digits | is_active | description |
|---|---|---|---|---|---|---|
| `1` | `EUR/USD` | `Currency` | `0.0001` | `5` | `true` | `null` |
| `1` | `EUR/GBP` | `Currency` | `0.001` | `5` | `true` | `null` |
| `1` | `XAU/USD` | `Commodity` | `0.01` | `2` | `true` | `null` |
| `1` | `USOil` | `Commodity` | `0.01` | `3` | `true` | `null` |

#### AccountGroup

| user_id | name | is_active | description |
|---|---|---|---|
| `1` | `Default` | `true` | `null` |

#### Account

| name | group_id | broker_id | instance_id | base_currency_id | username | password | leverage | balance | account_type | is_active | description |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `Acc-1` | `1` | `1` | `1` | `1` | `test` | `""` | `100` | `0` | `CFD` | `true` | `null` |

#### TrailingGroup

| user_id | name | is_active | description |
|---|---|---|---|
| `1` | `Default` | `true` | `null` |

#### PartialGroup

| user_id | name | is_active | description |
|---|---|---|---|
| `1` | `Default` | `true` | `null` |

#### ActionGroup

| user_id | name | is_active | description |
|---|---|---|---|
| `1` | `Default` | `true` | `null` |

#### Action

| name | action_group_id | asset_id | account_id | partial_group_id | trailing_group_id | risk_by_reward | take_profit | stop_loss | is_active | description |
|---|---|---|---|---|---|---|---|---|---|---|
| `Default` | `1` | `1` | `1` | `1` | `1` | `1` | `1` | `1` | `true` | `null` |

## Verify

Run this script with `uv run python` from the `database` directory. It checks the public import, Instance
selection, the query vocabulary, each capability group, the persistent file location, and that the Setup Operations
are repeatable. It prints `all checks passed` when every check holds. It adds one Broker and removes it again, and it
runs the default Instance's preparation, which changes nothing when the Instance is already prepared.

```python
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import database as package
from database import interface
from database.interface import (
    CommandResult,
    Database,
    DatabaseError,
    DatabaseInstance,
    Filter,
    FilterCombination,
    FilterOperator,
    InvalidInputError,
    Order,
    OrderDirection,
    Setup,
    SetupResult,
)
from model.interface import Broker, Currency, entities

EXPECTED = {
    "Database",
    "Setup",
    "Filter",
    "FilterOperator",
    "FilterCombination",
    "Order",
    "OrderDirection",
    "DatabaseInstance",
    "CommandResult",
    "SetupResult",
    "DatabaseError",
    "ConfigurationError",
    "InactiveInstanceError",
    "InvalidInputError",
    "DeclarationMismatchError",
    "ConnectionFailureError",
    "ExecutionError",
    "LifecycleError",
}

# Public import: exactly the declared names, and loading has no side effect.
assert {name for name in vars(interface) if not name.startswith("_")} == EXPECTED
PROBE = """
import sys
events = []
def hook(event, args):
    if event in ("socket.connect", "subprocess.Popen", "os.system", "sqlite3.connect"):
        events.append(event)
    if event == "open" and any(mode in str(args[1]) for mode in "wax+"):
        events.append(event)
    if event == "os.mkdir":
        events.append(event)
sys.addaudithook(hook)
import database.interface
assert not events, events
"""
subprocess.run([sys.executable, "-B", "-c", PROBE], check=True)

# Instance selection: one member per active Instance; the default and the member agree.
database = Database()
assert [member.name for member in DatabaseInstance] == ["SQLITE"]
assert all(member.value == member.name for member in DatabaseInstance)
assert database.count(Currency) == database.count(Currency, instance=DatabaseInstance.SQLITE)

# Query vocabulary: closed member sets whose values equal their names.
assert [m.name for m in FilterOperator] == [
    "EQUALS",
    "NOT_EQUALS",
    "GREATER_THAN",
    "GREATER_OR_EQUAL",
    "LESS_THAN",
    "LESS_OR_EQUAL",
    "IN",
    "CONTAINS",
    "STARTS_WITH",
    "ENDS_WITH",
    "IS_NULL",
    "IS_NOT_NULL",
]
assert [m.name for m in FilterCombination] == ["AND", "OR"]
assert [m.name for m in OrderDirection] == ["ASCENDING", "DESCENDING"]
for enumeration in (FilterOperator, FilterCombination, OrderDirection):
    assert all(member.value == member.name for member in enumeration)
assert Order(Currency.code).direction is OrderDirection.ASCENDING

# Capability groups: Entity Operations, the Command Operation, and the Setup Operations.
broker = database.add(Broker(name="Verify Example", user_id=1))
assert database.get_by_id(Broker, broker.id).name == "Verify Example"
assert database.get_by_id(Broker, 0) is None
assert database.disable(Broker, broker.id).is_active is False
assert database.enable(Broker, broker.id).is_active is True
assert broker.id in [
    b.id
    for b in database.list(Broker, [Filter(Broker.name, FilterOperator.EQUALS, "Verify Example")])
]
assert (
    database.delete(Broker, broker.id).id == broker.id
    and database.delete(Broker, broker.id) is None
)
assert database.sum(Currency, Currency.decimal_digits) >= 0
assert database.min(Currency, Currency.code) <= database.max(Currency, Currency.code)
result = database.execute_command("SELECT COUNT(*) AS n FROM Currency")
assert isinstance(result, CommandResult) and result.rows[0]["n"] == database.count(Currency)

# Strings are refused where imported values are required, and every failure is a DatabaseError.
for call in (
    lambda: database.count("Currency"),
    lambda: database.sum(Currency, "decimal_digits"),
    lambda: database.count(Currency, instance="SQLITE"),
    lambda: database.count(Currency, [Filter(Currency.code, "EQUALS", "USD")]),
):
    try:
        call()
    except InvalidInputError as error:
        assert isinstance(error, DatabaseError)
    else:
        raise AssertionError("a string was accepted")

# Persistent file location: inside the Database's own storage, whatever the working directory.
storage = Path(package.__file__).resolve().parents[1] / "db" / "application.db"
assert storage.is_file()
previous = Path.cwd()
os.chdir(tempfile.gettempdir())
try:
    assert Database().count(Currency) == database.count(Currency)
finally:
    os.chdir(previous)

# Repeatable Setup Operations: a second run creates and inserts nothing and changes no record.
before = [currency.to_json() for currency in database.list(Currency)]
for run in (Setup().prepare(), Setup().prepare()):
    assert isinstance(run, SetupResult) and run.success and run.command == "prepare"
assert "Created 0 Tables" in run.message and "Inserted 0 records" in run.message
assert [currency.to_json() for currency in database.list(Currency)] == before
assert len(entities) == 15

print("all checks passed")
```

## Troubleshooting

- **`InvalidInputError` on a call that looks right.** An Entity, Field, Instance, operator, combination, or direction
  was passed as a string, or a Field reference belongs to a different Entity. Pass the imported value, such as
  `Currency` and `Currency.code`. Values must also suit the Field's Type: text for an integer is refused, and a
  `datetime` needs a timezone.
- **`InvalidInputError` on `add` or `update`.** `add` takes a new Entity whose `id` is still pending, and `update`
  takes an Entity that has an `id`. Pass the Entity returned by an earlier call to `update`, not to `add`.
- **`ConfigurationError` when importing `database.interface`.** The configuration is invalid or does not match the
  code. Active Instances must match the members of `DatabaseInstance` and each needs an Engine unit, so changing which
  Instances are active takes effect only after the Database is regenerated. The message names the setting, never its
  value.
- **`InactiveInstanceError` or no member for an Instance.** Only active Instances have a `DatabaseInstance` member. An
  inactive Instance cannot be selected.
- **`DeclarationMismatchError` from `create_tables` or `prepare`.** An existing Table differs from its Entity, for
  example after the Model changed. The Database never alters an existing Table and creates nothing when it finds a
  difference. Remove the old database file from the `db` directory (or move the data yourself) and run `prepare`
  again.
- **`ExecutionError` from `insert_initial_data`.** A stored record has the same unique values as a configured record
  but differs from it. Nothing was inserted. Change or remove the stored record, or run `prepare` on a fresh Instance.
- **Empty `password` or `api_key` after preparation.** The Target leaves these Initial Data values to be generated
  securely, so the Database stores them as empty text. Set them with `update`.
- **`ExecutionError` naming an Entity and Field names.** A stored row does not satisfy its Entity's contract, so it is
  reported and not repaired. Correct the data.
- **`ConnectionFailureError`.** The storage cannot be reached: for the file-backed Instance, the `db` directory
  cannot be created or the database file cannot be opened.
- **`ModuleNotFoundError: No module named 'database'` or `'model'`.** Run Python inside the Database's environment,
  from the `database` directory, with `uv run python`.
