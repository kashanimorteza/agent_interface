# Database

## Overview

Database is the Trading Assistant's storage library. It keeps every Model Entity in a database and offers one stable gateway for reading and changing that data. A consumer creates the Interface class once, passes Entities, Field references and enumeration members to it, and gets Entities back. Connection details, storage paths and Engine code stay inside Database.

This example needs a prepared database (see [Setup](#setup)). It adds one User and lists every User.

```python
from model import User

from database import database_interface

db = database_interface()
user = db.add(
    User(name="Ada", username="ada", password="example-password", api_key="example-key")
)
print(user.id)
print([stored.username for stored in db.list(User)])
```

## Interface

The package root publishes exactly six groups and nothing else. Each group is named by the prefix `database`, an underscore and its key. A consumer imports a group and reaches every member through it. The Interface follows contract version 3.0.

| Group | Kind | What it holds |
|---|---|---|
| `database_interface` | class, created with no argument | every Entity Operation and the Command Operation |
| `database_setup` | class, created with no argument | the three Setup Operations |
| `database_value` | namespace | the values passed to an Operation |
| `database_instance` | enumeration | the active Instances a call can run on |
| `database_result` | namespace | the Results read back |
| `database_error` | namespace | every error |

```python
from database import (
    database_error,
    database_instance,
    database_interface,
    database_result,
    database_setup,
    database_value,
)
```

### Operation parameters

Every Operation takes exactly the parameters listed here, in this order. Every parameter after `entity`, `id`, `field` and `command` is optional, and `instance` is always last. `entity` is an Entity class imported from Model, except for `add` and `update`, which take an Entity instance. A string is never accepted in place of an Entity, a Field reference, an enumeration member or an Instance; such a call fails with `InvalidInputError` before any storage is touched. When `instance` is omitted the call runs on the configured default Instance.

#### `database_interface`

| Operation | Parameters | Returns |
|---|---|---|
| `add` | `entity`, `instance` | the stored Entity, including generated values |
| `update` | `entity`, `instance` | the stored Entity, or `None` when no record exists |
| `list` | `entity`, `filters`, `combination`, `orders`, `limit`, `instance` | the matching Entities |
| `get_by_id` | `entity`, `id`, `instance` | the Entity, or `None` |
| `delete` | `entity`, `id`, `instance` | the final deleted Entity, or `None` |
| `enable` | `entity`, `id`, `instance` | the final Entity (also when already enabled), or `None` |
| `disable` | `entity`, `id`, `instance` | the final Entity (also when already disabled), or `None` |
| `count` | `entity`, `filters`, `combination`, `instance` | the number of matching records |
| `sum` | `entity`, `field`, `filters`, `combination`, `instance` | the total, or zero when nothing matches |
| `min` | `entity`, `field`, `filters`, `combination`, `instance` | the smallest value, or `None` when nothing matches |
| `max` | `entity`, `field`, `filters`, `combination`, `instance` | the largest value, or `None` when nothing matches |
| `truncate` | `entity`, `instance` | the number of deleted records |
| `execute_command` | `command`, `parameters`, `instance` | a `CommandResult` |

- `add` takes one complete new Entity. Model never lets a caller supply an `id`, so storage assigns it and the returned Entity carries it.
- `update` takes an Entity that was read from Database. Its `id` only locates the record. It replaces every mutable Field and never changes `id` or another immutable Field.
- `list`, `count`, `sum`, `min` and `max` accept `filters` and `combination`. Only `list` accepts `orders` and `limit`. Omitted values come from the configuration: the combination is `AND`, the order is `id` ascending, and the limit is none. A positive `limit` is the maximum number of Entities returned; zero or a negative `limit` means no limit.
- `sum` needs a numeric Field (integer, float or decimal). `min` and `max` need a comparable Field (string, integer, float, decimal, datetime, date or time). `sum`, `min` and `max` ignore null values, and decimals are added and compared exactly.
- `enable` and `disable` set only `is_active`.
- `truncate` removes every record of the Entity and keeps its Table.
- `execute_command` runs any command valid for the Instance's Engine, including a schema change. `parameters` is a mapping for named parameters or a sequence for positional ones.

One example for each Operation:

```python
from decimal import Decimal

from model import Account, Broker, PartialRule, User

from database import database_interface, database_value

db = database_interface()
admin = db.get_by_id(User, 1)  # get_by_id: an Entity, or None
print(admin.username)

alan = db.add(User(name="Alan", username="alan", password="x", api_key="y"))  # add
alan.description = "Analyst"
alan = db.update(alan)  # update: replaces the mutable Fields
print(db.disable(User, alan.id).is_active)  # disable
print(db.enable(User, alan.id).is_active)  # enable

users = db.list(  # list: filters, combination, orders and limit are optional
    User,
    filters=[
        database_value.Filter(
            User.is_active, database_value.FilterOperator.EQUALS, True
        )
    ],
    orders=[database_value.Order(User.name, database_value.OrderDirection.DESCENDING)],
    limit=5,
)
print([user.name for user in users])
print(db.count(User))  # count
print(db.sum(Account, Account.leverage))  # sum: total over the Field
print(db.min(User, User.name), db.max(User, User.name))  # min and max
print(db.sum(Account, Account.balance) == Decimal(0))  # decimals add exactly

broker = db.add(Broker(name="Example", user_id=alan.id))
print(db.delete(Broker, broker.id).name)  # delete: the final deleted Entity
print(db.get_by_id(Broker, broker.id))  # None once it is gone

result = db.execute_command("SELECT COUNT(*) AS total FROM User")  # execute_command
print(result.rows[0]["total"])
print(db.truncate(PartialRule))  # truncate: the number of deleted records
```

#### `database_setup`

| Setup Operation | Parameters | Returns |
|---|---|---|
| `create_tables` | `instance` | a `SetupResult` |
| `insert_initial_data` | `instance` | a `SetupResult` |
| `prepare` | `instance` | a `SetupResult` |

`create_tables` creates the Table of every Model Entity and leaves matching Tables unchanged. `insert_initial_data` inserts every missing Initial Data record. `prepare` runs both, in that order, and stops without inserting when `create_tables` fails. A failure after the Instance is selected is reported as an unsuccessful `SetupResult` whose `message` states the cause.

```python
from database import database_setup

setup = database_setup()
print(setup.create_tables().message)
print(setup.insert_initial_data().message)
print(setup.prepare().success)
```

#### `database_value`

| Member | What it is for |
|---|---|
| `Filter(field, operator, value=None)` | one condition; `field` is an Entity's class attribute such as `User.is_active` |
| `FilterOperator` | how a Filter compares |
| `FilterCombination` | how several Filters combine: `AND` or `OR` |
| `Order(field, direction=ASCENDING)` | one sort |
| `OrderDirection` | `ASCENDING` or `DESCENDING` |

`FilterOperator` members: `EQUALS`, `NOT_EQUALS`, `GREATER_THAN`, `GREATER_OR_EQUAL`, `LESS_THAN`, `LESS_OR_EQUAL`, `IN`, `CONTAINS`, `STARTS_WITH`, `ENDS_WITH`, `IS_NULL`, `IS_NOT_NULL`. Rules: `CONTAINS`, `STARTS_WITH` and `ENDS_WITH` need a string Field and are case-sensitive. The ordering comparisons need a Field that can be ordered (not boolean or uuid). `IN` needs a collection. `IS_NULL` and `IS_NOT_NULL` take no value. A value must have the Field's exact type: an integer for an integer Field, a `Decimal` for a decimal Field, a timezone-aware `datetime` for a datetime Field, and so on.

```python
from model import Asset, User

from database import database_interface, database_value

Filter = database_value.Filter
Operator = database_value.FilterOperator
db = database_interface()

print(db.count(User, [Filter(User.name, Operator.EQUALS, "Admin")]))
print(db.count(User, [Filter(User.name, Operator.NOT_EQUALS, "Admin")]))
print(db.count(Asset, [Filter(Asset.digits, Operator.GREATER_THAN, 2)]))
print(db.count(Asset, [Filter(Asset.digits, Operator.GREATER_OR_EQUAL, 5)]))
print(db.count(Asset, [Filter(Asset.digits, Operator.LESS_THAN, 3)]))
print(db.count(Asset, [Filter(Asset.digits, Operator.LESS_OR_EQUAL, 2)]))
print(db.count(Asset, [Filter(Asset.digits, Operator.IN, [2, 3])]))
print(db.count(Asset, [Filter(Asset.symbol, Operator.CONTAINS, "/")]))
print(db.count(Asset, [Filter(Asset.symbol, Operator.STARTS_WITH, "EUR")]))
print(db.count(Asset, [Filter(Asset.symbol, Operator.ENDS_WITH, "Oil")]))
print(db.count(User, [Filter(User.description, Operator.IS_NULL)]))
print(db.count(User, [Filter(User.description, Operator.IS_NOT_NULL)]))

both = database_value.FilterCombination.AND  # every Filter must hold; the default
either = database_value.FilterCombination.OR  # at least one Filter must hold
conditions = [
    Filter(Asset.digits, Operator.EQUALS, 2),
    Filter(Asset.digits, Operator.EQUALS, 3),
]
print(db.count(Asset, conditions, both), db.count(Asset, conditions, either))
ascending = database_value.Order(Asset.symbol)  # OrderDirection defaults to ASCENDING
descending = database_value.Order(
    Asset.symbol, database_value.OrderDirection.DESCENDING
)
print(
    db.list(Asset, orders=[ascending])[0].symbol,
    db.list(Asset, orders=[descending])[0].symbol,
)
```

#### `database_instance`

The enumeration of active Instances. Each member name is the Instance key in upper case. See [Instances](#instances).

```python
from database import database_instance

print([member.name for member in database_instance])
```

#### `database_result`

`CommandResult` has the fields `rows`, `affected`, `columns`, `success`, `message` and `instance`. `rows` is a tuple of mappings and `columns` a tuple of names for a command that returns rows; `affected` is the changed record count for a command that does not. `SetupResult` has the fields `command`, `instance`, `success`, `affected` and `message`; `affected` is the number of Tables or records the command processed (for `insert_initial_data`, the records inserted plus those already present), and `message` states the cause when `success` is false. Both are immutable.

```python
from database import database_interface, database_setup

command = database_interface().execute_command(
    "SELECT id, name FROM User WHERE id = ?", [1]
)
print(command.columns, command.rows[0]["name"], command.success, command.instance.name)
setup = database_setup().create_tables()
print(setup.command, setup.success, setup.affected, setup.instance.name)
```

#### `database_error`

Every error derives from `DatabaseError`, and the failure kinds are never confused.

| Error | Meaning | Where you meet it |
|---|---|---|
| `DatabaseError` | the base of every error below | catch it to handle any Database failure |
| `ConfigurationError` | the configuration or the selected Instance is invalid | any call, the first time the configuration is used |
| `InactiveInstanceError` | an inactive Instance is selected | any call naming an Instance that is inactive in `config.yaml` |
| `InvalidInputError` | an input, an Entity, a Field reference or a value is invalid | any Operation, before storage is touched |
| `ConnectionFailureError` | the connection to an Instance cannot be opened | any Operation |
| `ExecutionError` | a request fails while it runs: a violated constraint, an invalid native command, a stored row that does not satisfy its Entity, or a value too large for the Instance | any Operation |
| `DeclarationMismatchError` | an existing Table differs from its Entity's Declaration | reported in the `message` of an unsuccessful `SetupResult`; a Setup Operation does not raise it |
| `SetupError` | table creation did not complete | reported in the `message` of an unsuccessful `SetupResult`; a Setup Operation does not raise it |

No error carries a connection value or a credential. One handler for every error, each with what to do next:

```python
from model import User

from database import database_error, database_interface, database_setup


def attempt(call):
    try:
        return call()
    except database_error.InvalidInputError as error:
        print("fix the call:", error)
    except database_error.ConfigurationError as error:
        print("fix config.yaml:", error)
    except database_error.InactiveInstanceError as error:
        print("select an active Instance:", error)
    except database_error.ConnectionFailureError as error:
        print("check the storage directory:", error)
    except database_error.ExecutionError as error:
        print("the request failed:", error)
    except database_error.DeclarationMismatchError as error:
        print("a Table differs from its Entity:", error)
    except database_error.SetupError as error:
        print("setup did not complete:", error)
    except database_error.DatabaseError as error:
        print("any other Database error:", error)


db = database_interface()
attempt(
    lambda: db.get_by_id("User", 1)
)  # InvalidInputError: a string for an Entity class
attempt(
    lambda: db.add(User(name="Admin", username="other", password="x", api_key="y"))
)  # ExecutionError

result = database_setup().create_tables()  # setup problems arrive in the result
if not result.success:
    print(result.message)
```

## Instances

An Instance is one named database connection. `database_instance` has exactly one member for every active configured Instance and none for an inactive one. This project has one active Instance, `SQLITE`, which is the default. The configured `PostgreSQL` Instance is inactive, so it has no member and no Engine implementation.

- Pass `instance=database_instance.SQLITE` to run a call on a specific Instance, or omit it to use the default.
- A file-backed Instance keeps its file inside Database's own storage directory, `db/` at the Component root. The default Instance's file is `db/application.db`. Only Database creates and manages these files, and a location that escapes the directory is refused.
- Connection values (host, port, database, username, password) are read from the configuration by Database and are never part of a call, a member, a Result or an error.
- Changing which Instances are active takes effect through the configuration and the next generation of Database.

```python
from model import User

from database import database_instance, database_interface

db = database_interface()
print(db.count(User), db.count(User, instance=database_instance.SQLITE))
```

## Setup

Database needs Python 3.14 or newer and `uv`.

1. Install the dependencies, from the `database` directory:

   ```text
   uv sync
   ```

2. Prepare the default Instance (creates the Tables and inserts the Initial Data):

   ```text
   uv run python scripts/prepare.py
   ```

3. To use Database from another project in this repository, declare it, and Model, as local path dependencies of that project:

   ```toml
   [project]
   dependencies = ["database"]

   [tool.uv.sources]
   database = { path = "../database", editable = true }
   model = { path = "../model", editable = true }
   ```

Database reads `config.yaml` at the Component root, so it must be used from its repository location (an editable path dependency).

## Use

Everything goes through the Interface. Pass Field references (an Entity's class attribute such as `Account.leverage`) and enumeration members, never strings.

```python
from model import Account, Broker, Currency, PartialRule, User

from database import database_interface, database_value

db = database_interface()
Filter = database_value.Filter
Operator = database_value.FilterOperator

# add and get_by_id
owner = db.add(User(name="Grace", username="grace", password="x", api_key="y"))
print(db.get_by_id(User, owner.id).username)

# update, enable and disable
owner.description = "Trader"
print(db.update(owner).description)
print(db.disable(User, owner.id).is_active, db.enable(User, owner.id).is_active)

# list with a Filter, an Order and a limit
euro = db.list(
    Currency,
    filters=[Filter(Currency.code, Operator.IN, ["EUR", "USD", "GBP"])],
    orders=[
        database_value.Order(Currency.code, database_value.OrderDirection.DESCENDING)
    ],
    limit=2,
)
print([currency.code for currency in euro])

# count, sum, min and max
print(db.count(Currency, [Filter(Currency.decimal_digits, Operator.EQUALS, 2)]))
print(db.sum(Currency, Currency.decimal_digits))
print(db.min(Currency, Currency.code), db.max(Currency, Currency.code))
print(db.max(Account, Account.leverage))

# delete and truncate
broker = db.add(Broker(name="Temporary", user_id=owner.id))
print(db.delete(Broker, broker.id).name)
print(db.truncate(PartialRule))

# a native command with bound parameters
print(
    db.execute_command(
        "SELECT code FROM Currency WHERE decimal_digits = :digits", {"digits": 0}
    ).rows
)
```

## Setup Operations

Setup Operations prepare storage. They are separate from the everyday Operations, so an ordinary call never changes the schema or inserts seed data.

- `create_tables` creates the Table of every Model Entity from its Declaration and nothing else. Re-running it over matching Tables changes nothing. If an existing Table differs from its Entity, the command stops, reports the difference and changes nothing.
- `insert_initial_data` inserts every Initial Data record that is missing, skips a record that is already present and identical, and fails without any change when a record conflicts with a different existing one. It is safe to run again.
- `prepare` runs `create_tables` and then `insert_initial_data`.

Run them by hand from the `database` directory, on the default Instance. Each script prints the result and exits with a failure code when the result is unsuccessful:

```text
uv run python scripts/create_tables.py
uv run python scripts/insert_initial_data.py
uv run python scripts/prepare.py
```

Generation runs `prepare` automatically on the default Instance, so a freshly generated Database is already prepared. Other Instances are prepared only when you select them explicitly, for example `database_setup().prepare(database_instance.SQLITE)`.

## Initial Data

Database inserts these records unchanged, with no omission for security reasons. A value the Target does not make concrete (`Generate securely`) is held as an empty string; Database never generates a value, so fill such values in `config.yaml` yourself before the first `insert_initial_data`. A stored record you change afterwards no longer matches its configured record, so `insert_initial_data` reports a conflict until the two agree again. Records appear in the order Database inserts them.

### User

| `name` | `username` | `password` | `api_key` |
|---|---|---|---|
| `Admin` | `admin` | `""` | `""` |

### TradingPlatform

| `name` | `code` |
|---|---|
| `MetaTrader 5` | `metatrader_5` |
| `Binance` | `binance` |

### Instance

| `name` | `user_id` | `trading_platform_id` | `ip` | `username` | `password` | `api_key` |
|---|---|---|---|---|---|---|
| `MetaTrader` | `1` | `1` | `127.0.0.1` | `test` | `""` | `""` |

### Currency

| `user_id` | `code` | `symbol` | `country` | `decimal_digits` |
|---|---|---|---|---|
| `1` | `USD` | `$` | `United States` | `2` |
| `1` | `EUR` | `€` | `Eurozone` | `2` |
| `1` | `GBP` | `£` | `United Kingdom` | `2` |
| `1` | `JPY` | `¥` | `Japan` | `0` |
| `1` | `CHF` | `CHF` | `Switzerland` | `2` |
| `1` | `CAD` | `C$` | `Canada` | `2` |
| `1` | `AUD` | `A$` | `Australia` | `2` |
| `1` | `NZD` | `NZ$` | `New Zealand` | `2` |

### Broker

| `name` | `user_id` |
|---|---|
| `FxPro` | `1` |

### Asset

| `broker_id` | `symbol` | `category` | `point_size` | `digits` |
|---|---|---|---|---|
| `1` | `EUR/USD` | `Currency` | `0.0001` | `5` |
| `1` | `EUR/GBP` | `Currency` | `0.001` | `5` |
| `1` | `XAU/USD` | `Commodity` | `0.01` | `2` |
| `1` | `USOil` | `Commodity` | `0.01` | `3` |

### AccountGroup

| `user_id` | `name` |
|---|---|
| `1` | `Default` |

### Account

| `name` | `group_id` | `broker_id` | `instance_id` | `base_currency_id` | `username` | `password` | `leverage` | `account_type` |
|---|---|---|---|---|---|---|---|---|
| `Acc-1` | `1` | `1` | `1` | `1` | `test` | `""` | `100` | `CFD` |

### TrailingGroup

| `user_id` | `name` |
|---|---|
| `1` | `Default` |

### PartialGroup

| `user_id` | `name` |
|---|---|
| `1` | `Default` |

### ActionGroup

| `user_id` | `name` |
|---|---|
| `1` | `Default` |

### Action

| `name` | `action_group_id` | `asset_id` | `account_id` | `partial_group_id` | `trailing_group_id` | `risk_by_reward` | `take_profit` | `stop_loss` |
|---|---|---|---|---|---|---|---|---|
| `Default` | `1` | `1` | `1` | `1` | `1` | `1` | `1` | `1` |

## Verify

Run this from the `database` directory after [Setup](#setup). It checks the public import, Instance selection, the query vocabulary, each capability group, the persistent file location and that the Setup Operations are repeatable. It prints `verified` when everything holds, provided the seeded records are unchanged.

```python
from pathlib import Path

from model import User

from database import (
    database_error,
    database_instance,
    database_interface,
    database_result,
    database_setup,
    database_value,
)

assert [member.name for member in database_instance] == ["SQLITE"]
db = database_interface()
setup = database_setup()

# query vocabulary: the closed enumerations
assert [member.name for member in database_value.FilterCombination] == ["AND", "OR"]
assert [member.name for member in database_value.OrderDirection] == [
    "ASCENDING",
    "DESCENDING",
]
assert len(database_value.FilterOperator) == 12

# Instance selection: the default Instance and the SQLITE member agree
assert db.count(User) == db.count(User, instance=database_instance.SQLITE)

# capability groups: read, change, aggregate, native command, Setup, Result, Error
user = db.add(User(name="Verify", username="verify", password="x", api_key="y"))
assert db.get_by_id(User, user.id).username == "verify"
assert db.update(db.get_by_id(User, user.id)).id == user.id
assert (
    db.disable(User, user.id).is_active is False and db.enable(User, user.id).is_active
)
assert db.count(User) == len(db.list(User))
assert db.min(User, User.id) <= db.max(User, User.id) <= db.sum(User, User.id)
assert isinstance(db.execute_command("SELECT 1 AS one"), database_result.CommandResult)
assert (
    db.delete(User, user.id).username == "verify"
    and db.get_by_id(User, user.id) is None
)
try:
    db.get_by_id("User", 1)
except database_error.InvalidInputError:
    pass
else:
    raise AssertionError("a string must be refused")

# persistent file location: the default Instance's file lives in db/
assert Path("db/application.db").is_file()

# repeatable Setup Operations: nothing is created or inserted twice
assert setup.prepare().success and setup.prepare().success
assert setup.create_tables().message.endswith("0 Tables created, 15 already matching")
assert "0 records inserted" in setup.insert_initial_data().message
print("verified")
```

## Troubleshooting

| Symptom | Cause | Remedy |
|---|---|---|
| An Instance is missing from `database_instance`, or loading fails with `the default Instance is not active`, or `InactiveInstanceError` is raised | The Instance is inactive in `config.yaml`: an inactive Instance has no member, and the default Instance must be active | Set `active` to true for the Instance you need and keep the default Instance active. A new member appears at the next generation of Database. |
| `ConfigurationError` mentioning an Engine without an implementation, a missing value or an escaping location | `config.yaml` is incomplete or points outside `db/`, or an active Instance uses an Engine that has no implementation | Fix the named item in `config.yaml`; every Instance needs all its values and an active Instance's Engine needs an implementation. |
| `prepare` or `create_tables` reports an unsuccessful result naming a Table and column | An existing Table differs from its Entity's Declaration | Database never alters a Table. Move or remove the differing Table (or the database file) and run `create_tables` again. |
| Passwords and API keys are empty strings after `prepare` | The Target does not make those Initial Data values concrete, and Database never generates a value | Fill them in `config.yaml` before the first `insert_initial_data`. Changing a seeded record afterwards makes `insert_initial_data` report a conflict until the configured record is changed to match. |
| `insert_initial_data` (or `prepare`) fails with a record that conflicts with an existing record | A stored record was changed and differs from its configured Initial Data on a uniqueness rule, for example a changed password beside the same name | Change the configured record to match the stored one, or restore the stored record. Nothing was changed by the failed command. |
| `InvalidInputError` for an Entity, a Field or an instance | A string, a wrong type or another Entity's Field reference was passed | Pass an Entity class, a Field reference such as `User.name`, an enumeration member or a `database_instance` member. |
| `InvalidInputError` from `update` or `add` | `update` needs an Entity read from Database, and `add` needs a new one | Read the record with `get_by_id` or `list`, change it, then call `update`. |
| `ExecutionError` with `FOREIGN KEY constraint failed` | The change would leave a record pointing at a missing one, for example deleting a User that owns a Broker | Remove or change the dependent records first. |
| `ExecutionError` with `UNIQUE constraint failed` | The record repeats a value that must be unique | Use a different value. |
| `ConnectionFailureError` | The storage directory or file of the Instance cannot be opened | Check that `db/` can be created and written by the current user. |
