# Database

Database persists the public Entity data of Model and provides one stable data-access gateway. A consumer imports the groups Database publishes, chooses a DatabaseInstance or accepts the default, and calls an Entity Operation, a Command Operation, or a Setup Operation. Database keeps configuration, Core, Engine units, connection values, and storage paths behind that boundary.

Database enumerates every Entity through the Entity Collection that Model publishes and stores values exactly as it receives them; it never interprets what a value means.

## Overview

Interface contract version: `3.0`.

The default Instance is prepared (Tables created, Initial Data inserted) when the Component is generated. Create the Interface class once, then call Operations on it. One add and one list:

```python
from model import User

from database import database_interface

db = database_interface()
user = db.add(User(name="Ada", username="ada", password="placeholder", api_key="placeholder"))
print(user.id, user.name)
print([item.name for item in db.list(User)])
```

```text
2 Ada
['Admin', 'Ada']
```

## Interface

Database publishes exactly six groups from the package root and nothing else. Each is named by the prefix `database`, an underscore, and its key. A consumer imports a group and reaches every member through it:

| Group | Key | What it is |
| --- | --- | --- |
| `database_interface` | Interface | the class created once, with no argument, that holds every Entity Operation and the Command Operation |
| `database_setup` | Setup | the class created with no argument that holds the three Setup Operations |
| `database_value` | Value | what a consumer passes to an Operation: the query vocabulary |
| `database_instance` | Instance | the enumeration of the active Instances |
| `database_result` | Result | what a consumer reads back |
| `database_error` | Error | every error a consumer can catch |

Entities, Fields, Instances, and query vocabulary are always passed as imported values, never as strings. An Entity is passed as the class or instance imported from Model, a Field as the Entity's class attribute for it (`User.is_active`), and an Instance as a member of `database_instance`.

Every Operation takes exactly the parameters listed, by those names and in that order; every parameter after `entity`, `id`, `field`, and `command` is optional, and `instance` is always last. Omitting `instance` runs the call on the default Instance.

### database_interface

| Operation | Parameters | Returns |
| --- | --- | --- |
| `add` | `entity`, `instance` | the stored Entity, including generated values |
| `update` | `entity`, `instance` | the stored Entity, or `None` when no record exists |
| `list` | `entity`, `filters`, `combination`, `orders`, `limit`, `instance` | the matching Entity instances |
| `get_by_id` | `entity`, `id`, `instance` | the Entity, or `None` when no record exists |
| `delete` | `entity`, `id`, `instance` | the final deleted Entity, or `None` when no record exists |
| `enable` | `entity`, `id`, `instance` | the final Entity (also when already enabled), or `None` |
| `disable` | `entity`, `id`, `instance` | the final Entity (also when already disabled), or `None` |
| `count` | `entity`, `filters`, `combination`, `instance` | the matching count |
| `sum` | `entity`, `field`, `filters`, `combination`, `instance` | the total of a numeric Field, ignoring nulls, or zero when nothing matches |
| `min` | `entity`, `field`, `filters`, `combination`, `instance` | the smallest non-null value, or `None` when nothing matches |
| `max` | `entity`, `field`, `filters`, `combination`, `instance` | the largest non-null value, or `None` when nothing matches |
| `truncate` | `entity`, `instance` | the number of records removed; the Table stays |
| `execute_command` | `command`, `parameters`, `instance` | a `CommandResult` |

Defaults: an omitted `combination` is `AND`, omitted `orders` order by `id` ascending, and an omitted `limit` is no limit. A positive `limit` is the maximum number returned; zero or a negative `limit` means no limit. Aggregates (`count`, `sum`, `min`, `max`) accept filters and a combination but no orders.

`add` takes a new Entity without an `id`; the id is assigned by storage and returned on the stored Entity.

`add` — store one complete new Entity:

```python
from model import Broker

from database import database_interface

broker = database_interface().add(Broker(name="Example Broker", user_id=1))
print(broker.id, broker.name, broker.is_active)
```

```text
2 Example Broker True
```

`update` — replace every mutable Field of an existing record; `id` only locates it and never changes:

```python
from model import Broker

from database import database_interface

db = database_interface()
broker = db.get_by_id(Broker, 2)
broker.description = "Updated through update"
stored = db.update(broker)
print(stored.id, stored.description)
```

```text
2 Updated through update
```

`list` — filters, a combination, orders, and a limit. Filters and orders are built from Field references and enumeration members of `database_value`:

```python
from model import Currency

from database import database_interface, database_value

db = database_interface()
rows = db.list(
    Currency,
    filters=[database_value.Filter(Currency.decimal_digits, database_value.FilterOperator.EQUALS, 2)],
    combination=database_value.FilterCombination.AND,
    orders=[database_value.Order(Currency.code, database_value.OrderDirection.DESCENDING)],
    limit=3,
)
print([item.code for item in rows])
```

```text
['USD', 'NZD', 'GBP']
```

`get_by_id` — one record by its id, or `None` (a missing record is not an error):

```python
from model import User

from database import database_interface

db = database_interface()
print(db.get_by_id(User, 1).username)
print(db.get_by_id(User, 999))
```

```text
admin
None
```

`delete` — remove one record and return it as it was:

```python
from model import Broker

from database import database_interface

db = database_interface()
gone = db.delete(Broker, 2)
print(gone.name)
print(db.get_by_id(Broker, 2))
```

```text
Example Broker
None
```

`enable` and `disable` — set only `is_active` and return the final Entity:

```python
from model import Currency

from database import database_interface

db = database_interface()
print(db.disable(Currency, 1).is_active)
print(db.disable(Currency, 1).is_active)
print(db.enable(Currency, 1).is_active)
```

```text
False
False
True
```

`count`, `sum`, `min`, and `max` — aggregates over optional filters. `sum` needs a numeric Field; null values are ignored:

```python
from model import Asset, Currency

from database import database_interface, database_value

db = database_interface()
print(db.count(Currency))
print(db.count(Currency, [database_value.Filter(Currency.decimal_digits, database_value.FilterOperator.EQUALS, 0)]))
print(db.sum(Currency, Currency.decimal_digits))
print(db.min(Asset, Asset.point_size), db.max(Asset, Asset.point_size))
```

```text
8
1
14
0.0001 0.01
```

`truncate` — remove every record of one Entity and keep its Table:

```python
from decimal import Decimal

from model import TrailingRule

from database import database_interface

db = database_interface()
db.add(TrailingRule(name="rule-1", trailing_group_id=1, trigger_percentage=Decimal("50")))
db.add(TrailingRule(name="rule-2", trailing_group_id=1, trigger_percentage=Decimal("75")))
print(db.truncate(TrailingRule))
print(db.count(TrailingRule))
```

```text
2
0
```

`execute_command` — run a native command with bound parameters and read a `CommandResult`. `create_tables` remains the standard way to prepare schema:

```python
from database import database_interface

result = database_interface().execute_command("SELECT code FROM Currency WHERE decimal_digits = ? ORDER BY id", (0,))
print(result.rows, result.columns, result.affected, result.success)
```

```text
({'code': 'JPY'},) ('code',) None True
```

### database_setup

The three Setup Operations, each taking only the optional `instance` and returning a `SetupResult`: `create_tables`, `insert_initial_data`, and `prepare`. They are described in [Setup Operations](#setup-operations).

### database_value

The values a consumer passes to `list`, `count`, `sum`, `min`, and `max`:

- `Filter(field, operator, value)` — an immutable condition. `field` is a Field reference; `operator` is a `FilterOperator` member; `value` is compatible with the Field, absent for `IS_NULL` and `IS_NOT_NULL`, and a collection for `IN`.
- `Order(field, direction)` — an immutable ordering; `direction` is an `OrderDirection` member and defaults to `ASCENDING`.
- `FilterOperator` — `EQUALS`, `NOT_EQUALS`, `GREATER_THAN`, `GREATER_OR_EQUAL`, `LESS_THAN`, `LESS_OR_EQUAL`, `IN`, `CONTAINS`, `STARTS_WITH`, `ENDS_WITH`, `IS_NULL`, `IS_NOT_NULL`. The text operators need a textual Field.
- `FilterCombination` — `AND`, `OR`.
- `OrderDirection` — `ASCENDING`, `DESCENDING`.

Each member's value equals its name. A string given in place of a member or a Field reference is refused.

```python
from database import database_value

print([member.name for member in database_value.FilterOperator])
print([member.name for member in database_value.FilterCombination], [member.name for member in database_value.OrderDirection])
```

```text
['EQUALS', 'NOT_EQUALS', 'GREATER_THAN', 'GREATER_OR_EQUAL', 'LESS_THAN', 'LESS_OR_EQUAL', 'IN', 'CONTAINS', 'STARTS_WITH', 'ENDS_WITH', 'IS_NULL', 'IS_NOT_NULL']
['AND', 'OR'] ['ASCENDING', 'DESCENDING']
```

### database_instance

The enumeration of the active Instances: one member per active configured Instance and none for an inactive one. Each member name is the Instance key in upper case.

```python
from database import database_instance

print([member.name for member in database_instance])
```

```text
['SQLITE']
```

### database_result

- `CommandResult` — `rows` (row mappings, or `None`), `affected` (affected row count, or `None`), `columns` (ordered column names, or `None`), `success`, `message`, and `instance` (the DatabaseInstance used).
- `SetupResult` — `command` (the Setup Operation name), `instance`, `success`, `affected` (the processed Table or record count), and `message`.

Both are immutable.

```python
from database import database_instance, database_setup

result = database_setup().create_tables(database_instance.SQLITE)
print(result.command, result.instance.name, result.success, result.affected)
print(result.message)
```

```text
create_tables SQLITE True 0
0 Tables created, 15 already present
```

### database_error

Every error derives from `DatabaseError`, so a consumer can catch one kind or all of them. No error carries a connection value or credential.

| Error | Raised when |
| --- | --- |
| `ConfigurationError` | the Configuration or an Instance is invalid |
| `InactiveInstanceError` | an inactive Instance is selected |
| `InvalidInputError` | an input or a Field is invalid, such as a string where an imported value is required |
| `DeclarationMismatchError` | an existing Table differs from its Entity, or a stored row breaks its Entity contract |
| `ConnectionFailureError` | the storage of an Instance cannot be reached |
| `ExecutionError` | an Engine cannot execute a request, such as a violated constraint |
| `SetupError` | a Setup Operation did not complete |

```python
from model import Currency, User

from database import database_error, database_interface, database_value

v = database_value
try:
    database_interface().count(User, [v.Filter(Currency.code, v.FilterOperator.EQUALS, "USD")])
except database_error.DatabaseError as error:
    print(type(error).__name__, "-", error)
```

```text
InvalidInputError - The Field must be a Field reference of User
```

## Instances

An Instance is one named database connection and storage identity. The Configuration defines two:

| Key | Engine | Active | Role |
| --- | --- | --- | --- |
| `sqlite` | SQLite | yes | the default Instance; its database file lives in the Database-owned storage directory |
| `postgresql` | PostgreSQL | no | defined but inactive, so it has no `database_instance` member and no Engine unit |

Every Operation and Setup Operation accepts an optional member of `database_instance`. When none is given, the call runs on the default Instance. Connection values and credentials stay in the Configuration; they never appear in `database_instance`, in a request, in a result, or in an error.

The database file of a file-backed Instance is `db/` plus the Instance's database value, inside this Component. It is created and managed only by Database; it cannot be moved outside that directory by a path in the Configuration.

```python
from model import User

from database import database_instance, database_interface

db = database_interface()
print(db.count(User) == db.count(User, instance=database_instance.SQLITE))
```

```text
True
```

## Setup

1. Install [uv](https://docs.astral.sh/uv/).
2. From this directory, run `uv sync`. It creates the isolated environment and installs the dependencies recorded in `uv.lock`, including the Model Component from its local path. Python 3.14 or newer is required.
3. Keep the Component in place: the Configuration (`config.yaml`) and the storage directory (`db/`) are read from this directory, so a consumer inside this repository declares an editable local path dependency on it.
4. Prepare the default Instance with `uv run python scripts/prepare.py` (see [Setup Operations](#setup-operations)). Generation does this automatically.
5. To check the source, run `uv run ruff format --check database scripts`, `uv run ruff check database scripts`, and `uv run ty check database scripts`.

## Use

Use Database only through the six groups. Fields are always Field references and every query value is an enumeration member:

```python
from model import Asset, Currency

from database import database_interface, database_value

db = database_interface()
v = database_value
cheap = db.list(
    Asset,
    filters=[
        v.Filter(Asset.category, v.FilterOperator.EQUALS, "Commodity"),
        v.Filter(Asset.symbol, v.FilterOperator.STARTS_WITH, "XAU"),
    ],
    combination=v.FilterCombination.AND,
)
print([item.symbol for item in cheap])
either = db.list(
    Currency,
    filters=[
        v.Filter(Currency.code, v.FilterOperator.IN, ["USD", "JPY"]),
        v.Filter(Currency.symbol, v.FilterOperator.EQUALS, "CHF"),
    ],
    combination=v.FilterCombination.OR,
    orders=[v.Order(Currency.code, v.OrderDirection.ASCENDING)],
)
print([item.code for item in either])
```

```text
['XAU/USD']
['CHF', 'JPY', 'USD']
```

Every returned Entity is built through its own construction, so it is validated like any other Entity of Model. A row that breaks its Entity contract raises `DeclarationMismatchError`; it is never repaired.

## Setup Operations

Preparing storage is a separate act from using it. The Setup Operations are called through `database_setup`, or by hand through the three scripts in `scripts/`; both run the same Operation on the default Instance and report the same `SetupResult`:

| Operation | Script | What it does |
| --- | --- | --- |
| `create_tables` | `scripts/create_tables.py` | creates every Table from the Entities of the Model Entity Collection and their Declarations; matching Tables are left unchanged; a Table that differs from its Entity stops the command and nothing is created |
| `insert_initial_data` | `scripts/insert_initial_data.py` | inserts every missing Initial Data record, skips a record already present, and fails, leaving nothing partial, on a record that conflicts with stored data |
| `prepare` | `scripts/prepare.py` | runs `create_tables` and then `insert_initial_data`, and stops without inserting when `create_tables` fails |

Run a script from this directory:

```text
uv run python scripts/prepare.py
```

```text
prepare: 0 Tables created, 15 already present; 0 of 23 Initial Data records inserted
```

Each Setup Operation can be repeated safely. Generation runs `prepare` automatically on the default Instance (after-generation preparation is enabled); a failure identifies the Instance and the command. Other Instances are prepared only when you select them.

```python
from database import database_instance, database_setup

setup = database_setup()
print(setup.create_tables(database_instance.SQLITE).message)
print(setup.insert_initial_data().message)
print(setup.prepare().message)
```

```text
0 Tables created, 15 already present
0 of 23 Initial Data records inserted
0 Tables created, 15 already present; 0 of 23 Initial Data records inserted
```

## Initial Data

Initial Data is part of the Database Configuration: one shared collection holding every Target-defined Initial Data record. `insert_initial_data` validates each record through its public Entity contract and inserts the values unchanged; no value is omitted, postponed, or blocked because of a sensitivity marker, a credential Field, or an at-rest instruction, and Database never hashes, encrypts, or masks. Records are matched to Entities by the Entity's export name.

A Target value that is not concrete (for example `Generate securely`) is copied as an empty string and no value is generated; fill such values in `config.yaml` later. Records are listed in insertion order:

### User

| `name` | `username` | `password` | `api_key` |
| --- | --- | --- | --- |
| Admin | admin | (empty) | (empty) |

### TradingPlatform

| `name` | `code` |
| --- | --- |
| MetaTrader 5 | metatrader_5 |
| Binance | binance |

### Instance

| `name` | `user_id` | `trading_platform_id` | `ip` | `username` | `password` | `api_key` |
| --- | --- | --- | --- | --- | --- | --- |
| MetaTrader | 1 | 1 | 127.0.0.1 | test | (empty) | (empty) |

### Currency

| `user_id` | `code` | `symbol` | `country` | `decimal_digits` |
| --- | --- | --- | --- | --- |
| 1 | USD | $ | United States | 2 |
| 1 | EUR | € | Eurozone | 2 |
| 1 | GBP | £ | United Kingdom | 2 |
| 1 | JPY | ¥ | Japan | 0 |
| 1 | CHF | CHF | Switzerland | 2 |
| 1 | CAD | C$ | Canada | 2 |
| 1 | AUD | A$ | Australia | 2 |
| 1 | NZD | NZ$ | New Zealand | 2 |

### Broker

| `name` | `user_id` |
| --- | --- |
| FxPro | 1 |

### Asset

| `broker_id` | `symbol` | `category` | `point_size` | `digits` |
| --- | --- | --- | --- | --- |
| 1 | EUR/USD | Currency | 0.0001 | 5 |
| 1 | EUR/GBP | Currency | 0.001 | 5 |
| 1 | XAU/USD | Commodity | 0.01 | 2 |
| 1 | USOil | Commodity | 0.01 | 3 |

### AccountGroup

| `user_id` | `name` |
| --- | --- |
| 1 | Default |

### Account

| `name` | `group_id` | `broker_id` | `instance_id` | `base_currency_id` | `username` | `password` | `leverage` | `account_type` |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Acc-1 | 1 | 1 | 1 | 1 | test | (empty) | 100 | CFD |

### TrailingGroup

| `user_id` | `name` |
| --- | --- |
| 1 | Default |

### PartialGroup

| `user_id` | `name` |
| --- | --- |
| 1 | Default |

### ActionGroup

| `user_id` | `name` |
| --- | --- |
| 1 | Default |

### Action

| `name` | `action_group_id` | `asset_id` | `account_id` | `partial_group_id` | `trailing_group_id` | `risk_by_reward` | `take_profit` | `stop_loss` |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Default | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |

## Verify

The following script, run from this directory on a prepared default Instance, verifies public import, Instance selection, the query vocabulary, each capability group, the persistent file location, and repeatable Setup Operations.

```python
from pathlib import Path

import database
from model import Currency, User

from database import (
    database_error,
    database_instance,
    database_interface,
    database_result,
    database_setup,
    database_value,
)

assert sorted(database.__all__) == [
    "database_error", "database_instance", "database_interface",
    "database_result", "database_setup", "database_value",
], "public import: exactly six groups"

assert [m.name for m in database_instance] == ["SQLITE"], "Instance selection: only active Instances"
db, setup = database_interface(), database_setup()
assert db.count(User) == db.count(User, instance=database_instance.SQLITE), "default Instance"

v = database_value
assert [m.name for m in v.FilterOperator] == [
    "EQUALS", "NOT_EQUALS", "GREATER_THAN", "GREATER_OR_EQUAL", "LESS_THAN", "LESS_OR_EQUAL",
    "IN", "CONTAINS", "STARTS_WITH", "ENDS_WITH", "IS_NULL", "IS_NOT_NULL",
], "query vocabulary: operators"
assert [m.name for m in v.FilterCombination] == ["AND", "OR"]
assert [m.name for m in v.OrderDirection] == ["ASCENDING", "DESCENDING"]

# capability groups
added = db.add(User(name="verify", username="verify", password="placeholder", api_key="placeholder"))
assert db.get_by_id(User, added.id).username == "verify"
assert db.disable(User, added.id).is_active is False and db.enable(User, added.id).is_active is True
assert [c.code for c in db.list(Currency, [v.Filter(Currency.code, v.FilterOperator.IN, ["EUR", "USD"])],
        orders=[v.Order(Currency.code, v.OrderDirection.ASCENDING)])] == ["EUR", "USD"]
assert db.count(Currency) == 8 and db.sum(Currency, Currency.decimal_digits) == 14
assert db.delete(User, added.id).id == added.id and db.get_by_id(User, added.id) is None
assert isinstance(db.execute_command("SELECT 1 AS one"), database_result.CommandResult)

# anything but an imported value is refused
for call in (
    lambda: db.count(User, [v.Filter(Currency.code, v.FilterOperator.EQUALS, "USD")]),
    lambda: db.list(Currency, combination=v.FilterOperator.EQUALS),
    lambda: db.list(Currency, orders=[Currency.code]),
):
    try:
        call()
    except database_error.InvalidInputError:
        pass
    else:
        raise AssertionError("a value that is not imported was accepted")

# persistent file location and repeatable Setup Operations
assert Path("db/application.db").is_file(), "the database file lives in the storage directory"
assert setup.prepare().affected == 0 and setup.prepare().affected == 0, "repeatable"
print("verified")
```

```text
verified
```

## Troubleshooting

- **`InvalidInputError`** — an input was not an imported value or did not match its Field: an Entity, Field, or Instance given as a string; a Field of another Entity; a text operator on a non-textual Field; a value that does not match the Field's Type; or an `id` of the wrong Type. The message names what was refused.
- **`InactiveInstanceError`** — an inactive Instance was selected. Only active Instances are members of `database_instance`; set `active: true` in `config.yaml` and generate again to add one, which also adds the Engine unit it needs.
- **`DeclarationMismatchError` from `create_tables`** — an existing Table differs from its Entity. Database never alters an existing Table and never resolves the difference by judgment: change the Entity, or remove the Table (for a development database, delete the file in `db/` and run `prepare`). Database owns no data migration.
- **Empty values in Initial Data** — a Target value that is not concrete is copied as an empty string and inserted as is. Fill it in `config.yaml`; `insert_initial_data` inserts missing records only, so existing rows keep their stored values.
- **`ExecutionError` from `insert_initial_data`** — an Initial Data record conflicts with stored data (for example it repeats a unique value). Nothing is inserted. Fix the record or the stored row.
- **`ConfigurationError` when importing `database`** — the Configuration is missing or invalid, or the package is not installed from this directory. Keep `config.yaml` beside the package and install it as an editable local path dependency.
- **`ConnectionFailureError`** — the storage directory or database file cannot be created or opened.
- **`SetupError` from `prepare`** — table creation failed, so no Initial Data was inserted. The error names the Instance and chains the cause.
- **A missing record** — `get_by_id`, `update`, `delete`, `enable`, and `disable` return `None` for an unknown id; this is not an error.
