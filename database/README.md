# Database

Database is the persistence layer of the Trading Assistant. It stores every Model Entity and gives consumers one data-access gateway: select an Instance (or accept the default), call an Operation, and get Entities back. Consumers use only `database.interface`; configuration, Core, Engine units, connection details, and storage paths are never part of the public surface.

## Overview

```python
from database.interface import Database
from model.interface import Broker

db = Database()
added = db.add(Broker(name="Example Broker", user_id=1))
print([broker.name for broker in db.list(Broker)])
db.delete(Broker, added.id)  # tidy up: Broker names are unique per user
```

Output:

```text
['FxPro', 'Example Broker']
```

## Interface

`database.interface` publishes exactly the 17 names below and nothing else. Loading it opens no connection and creates no file. Entities, Fields, Instances, operators, combinations, and directions are always passed as imported values, never as strings; a string is refused with `InvalidInputError` before any storage is touched.

The examples in this README continue one Python session on a prepared Instance (see [Setup](#setup)). Every one of them starts from these imports and this gateway:

```python
from database.interface import (
    Database,
    DatabaseInstance,
    Filter,
    FilterCombination,
    FilterOperator,
    Order,
    OrderDirection,
)
from model.interface import Asset, Broker, Currency, User

db = Database()
```

### Database

The gateway. A consumer creates one `Database()` with no arguments and calls every Operation and Lifecycle Command on it. Creating it opens no connection. Every call takes an optional last parameter, `instance`, a `DatabaseInstance` member.

```python
print(db.count(User))
```

```text
1
```

### DatabaseInstance

The enumeration of the active configured Instances. It has one member per active Instance and none for an inactive one, and its members carry no connection values. Today it holds `SQLITE`. Omitting `instance` runs a call on the configured default Instance, which is `SQLITE`.

```python
print([member.name for member in DatabaseInstance])
print(db.count(User, instance=DatabaseInstance.SQLITE))
```

```text
['SQLITE']
1
```

### Filter and FilterOperator

A `Filter(field, operator, value)` is an immutable condition. `field` is a Field reference of the Entity being queried, written as the Entity's class attribute (`Currency.code`). `operator` is a `FilterOperator` member. `value` is a value of the Field's Type; it is omitted for the two null tests and is a list, tuple, or set of such values for `IN`. A Field of another Entity, a string in place of a Field, or a value of the wrong Type is refused as invalid input.

| Member | Selects the records whose Field |
|---|---|
| `EQUALS` | equals the value |
| `NOT_EQUALS` | does not equal the value |
| `GREATER_THAN` | is greater than the value |
| `GREATER_OR_EQUAL` | is greater than or equal to the value |
| `LESS_THAN` | is less than the value |
| `LESS_OR_EQUAL` | is less than or equal to the value |
| `IN` | equals one of the values |
| `CONTAINS` | contains the text (textual Fields only) |
| `STARTS_WITH` | starts with the text (textual Fields only) |
| `ENDS_WITH` | ends with the text (textual Fields only) |
| `IS_NULL` | holds null (no value) |
| `IS_NOT_NULL` | does not hold null (no value) |

A stored null never satisfies a comparison, `IN`, or a text operator; use `IS_NULL` and `IS_NOT_NULL` for nulls. The text operators are case-sensitive on every Engine. Decimal Fields are compared by value (`1.5` equals `1.50`), not by their stored text.

```python
usd_and_eur = Filter(Currency.code, FilterOperator.IN, ["USD", "EUR"])
print([currency.code for currency in db.list(Currency, [usd_and_eur], orders=[Order(Currency.code)])])
```

```text
['EUR', 'USD']
```

### FilterCombination

How several Filters combine. `AND` (the default) selects records that satisfy every Filter; `OR` selects records that satisfy at least one.

```python
either = [
    Filter(Currency.code, FilterOperator.EQUALS, "JPY"),
    Filter(Currency.code, FilterOperator.EQUALS, "CHF"),
]
print([currency.code for currency in db.list(Currency, either, FilterCombination.OR, [Order(Currency.code)])])
```

```text
['CHF', 'JPY']
```

### Order and OrderDirection

An `Order(field, direction)` is an immutable ordering on one Field. `direction` is `ASCENDING` (the default) or `DESCENDING`. When no Order is supplied a list is ordered by `id` ascending; supplied Orders replace that default and apply in the sequence given.

```python
newest_first = [Order(Currency.code, OrderDirection.DESCENDING)]
print([currency.code for currency in db.list(Currency, orders=newest_first, limit=3)])
```

```text
['USD', 'NZD', 'JPY']
```

### CommandResult

What `execute_command` returns. Members, in order: `rows` (a tuple of row mappings, or `None`), `affected` (the affected row count, or `None`), `columns` (a tuple of column names, or `None`), `success`, `message`, and `instance` (the `DatabaseInstance` used). A command that fails is reported with `success` false and a message that never contains a credential.

```python
result = db.execute_command("select code from Currency where decimal_digits = ?", (0,))
print(result.rows, result.columns, result.affected, result.success, result.instance)
```

```text
({'code': 'JPY'},) ('code',) None True DatabaseInstance.SQLITE
```

### LifecycleResult

What a Lifecycle Command returns. Members, in order: `command`, `instance`, `success`, `affected` (the number of Tables or records processed), and `message`. A Lifecycle Command that fails raises one of the errors below instead of returning `success` false.

```python
print(db.create_tables())
```

```text
LifecycleResult(command='create_tables', instance=<DatabaseInstance.SQLITE: 'SQLITE'>, success=True, affected=15, message='15 Table(s) are ready.')
```

### Errors

`DatabaseError` is the base of every Database failure, so catching it catches all of them. One derived error exists for each failure kind, and each one's message names the Entity, Instance, or command involved and never a credential or a stored value.

| Error | Raised when |
|---|---|
| `ConfigurationError` | the configuration, an Initial Data record, or the selected Instance is invalid |
| `InactiveInstanceError` | an Instance that is not active is selected |
| `InvalidInputError` | an input or Field reference is invalid, such as a Field of another Entity or a string where an imported value is required |
| `DeclarationMismatchError` | an existing Table, or a stored row, does not match its Entity |
| `ConnectionFailureError` | the connection to an Instance cannot be made |
| `ExecutionError` | storage cannot execute the request, for example a uniqueness or foreign-key violation |
| `LifecycleError` | a Lifecycle Command did not complete, for example conflicting Initial Data |

```python
from database.interface import (
    ConfigurationError,
    ConnectionFailureError,
    DatabaseError,
    DeclarationMismatchError,
    ExecutionError,
    InactiveInstanceError,
    InvalidInputError,
    LifecycleError,
)

try:
    db.list(Currency, [Filter(Broker.name, FilterOperator.EQUALS, "FxPro")])  # a Field of another Entity
except InvalidInputError as error:
    print("invalid input:", error)

try:
    db.add(User(name="Admin", username="another", password="", api_key=""))  # the name is taken
except ExecutionError as error:
    print("execution:", error)

try:
    db.prepare()
except ConfigurationError:
    ...  # the configuration or the selected Instance is invalid
except InactiveInstanceError:
    ...  # the Instance is not active
except DeclarationMismatchError:
    ...  # an existing Table differs from its Entity
except ConnectionFailureError:
    ...  # the Instance cannot be reached
except LifecycleError:
    ...  # the command did not complete
except DatabaseError:
    ...  # any other Database failure
```

```text
invalid input: A Field reference of Currency is required, such as Currency.id.
execution: Add failed on Instance 'SQLite': UNIQUE constraint failed: User.name.
```

### Entity Operations

Every Entity Operation takes the Entity itself, never its name: an Entity instance for `add` and `update`, an Entity class for the others. A missing record is never an error; it is reported as `None`. Every changing Operation completes in full or leaves no change.

#### add

Stores one complete new Entity and returns the stored Entity, including generated values such as `id`.

| Parameter | Meaning |
|---|---|
| `entity` | a new Entity instance; its `id` is left unset |
| `instance` | optional `DatabaseInstance` |

```python
broker = db.add(Broker(name="Doc Broker", user_id=1))
print(broker.name, broker.is_active)
```

```text
Doc Broker True
```

#### update

Replaces every mutable Field of the stored record that the Entity's `id` locates; `id` and other immutable Fields never change. Returns the stored Entity, or `None` when no record exists.

| Parameter | Meaning |
|---|---|
| `entity` | a complete Entity instance whose `id` locates the record |
| `instance` | optional `DatabaseInstance` |

```python
broker.description = "Changed by the example"
print(db.update(broker).description)
```

```text
Changed by the example
```

#### get_by_id

Returns the Entity with the given `id`, or `None`.

| Parameter | Meaning |
|---|---|
| `entity` | an Entity class |
| `id` | the record's identity |
| `instance` | optional `DatabaseInstance` |

```python
print(db.get_by_id(Broker, broker.id).name, db.get_by_id(Broker, 999999))
```

```text
Doc Broker None
```

#### list

Returns the Entities that match.

| Parameter | Meaning |
|---|---|
| `entity` | an Entity class |
| `filters` | optional list of `Filter`; omitted selects every record |
| `combination` | optional `FilterCombination`; omitted is `AND` |
| `orders` | optional list of `Order`; omitted is `id` ascending |
| `limit` | optional maximum count; zero, a negative value, or omitted means no limit |
| `instance` | optional `DatabaseInstance` |

```python
cheap = [Filter(Asset.digits, FilterOperator.LESS_THAN, 5)]
print([asset.symbol for asset in db.list(Asset, cheap, orders=[Order(Asset.symbol)], limit=2)])
```

```text
['USOil', 'XAU/USD']
```

#### enable and disable

Set only `is_active` to true (`enable`) or false (`disable`) and return the final Entity, including when the record was already in that state, or `None` when no record exists.

| Parameter | Meaning |
|---|---|
| `entity` | an Entity class that has an `is_active` Field |
| `id` | the record's identity |
| `instance` | optional `DatabaseInstance` |

```python
print(db.disable(Broker, broker.id).is_active, db.enable(Broker, broker.id).is_active)
```

```text
False True
```

#### delete

Deletes the record with the given `id` and returns it as it was, or `None`.

| Parameter | Meaning |
|---|---|
| `entity` | an Entity class |
| `id` | the record's identity |
| `instance` | optional `DatabaseInstance` |

```python
print(db.delete(Broker, broker.id).name, db.delete(Broker, broker.id))
```

```text
Doc Broker None
```

#### count

Returns how many records match.

| Parameter | Meaning |
|---|---|
| `entity` | an Entity class |
| `filters` | optional list of `Filter` |
| `combination` | optional `FilterCombination` |
| `instance` | optional `DatabaseInstance` |

```python
print(db.count(Currency), db.count(Currency, [Filter(Currency.decimal_digits, FilterOperator.EQUALS, 2)]))
```

```text
8 7
```

#### sum, min, and max

`sum` returns the total of a numeric Field (integer, float, or decimal), `min` the smallest and `max` the largest value of a comparable Field. Null values are ignored. With no matching value `sum` returns zero of the Field's Type and `min` and `max` return `None`. Decimal results are exact. None of the three accepts an `Order`.

| Parameter | Meaning |
|---|---|
| `entity` | an Entity class |
| `field` | a Field reference of that Entity, such as `Currency.decimal_digits` |
| `filters` | optional list of `Filter` |
| `combination` | optional `FilterCombination` |
| `instance` | optional `DatabaseInstance` |

```python
print(db.sum(Currency, Currency.decimal_digits), db.min(Currency, Currency.code), db.max(Asset, Asset.digits))
```

```text
14 AUD 5
```

#### truncate

Removes every record of one Entity, keeps its Table, and returns the deleted count. It is refused with `ExecutionError` while other records reference the Entity's records.

| Parameter | Meaning |
|---|---|
| `entity` | an Entity class |
| `instance` | optional `DatabaseInstance` |

```python
from decimal import Decimal

from model.interface import TrailingRule

db.add(TrailingRule(name="Doc Rule", trailing_group_id=1, trigger_percentage=Decimal("50")))
print(db.truncate(TrailingRule))  # removes every TrailingRule record
```

```text
1
```

### Database-wide Operation

#### execute_command

Runs a native command in the selected Instance's query language, with bound parameters, and returns a `CommandResult`. Any command the Engine supports is accepted, including a schema change; `create_tables` remains the standard way to prepare storage. SQLite takes positional parameters as a tuple or list and named parameters as a mapping.

| Parameter | Meaning |
|---|---|
| `command` | the native command text |
| `parameters` | optional tuple, list, or mapping of bound values |
| `instance` | optional `DatabaseInstance` |

```python
result = db.execute_command("select name from User where username = :username", {"username": "admin"})
print(result.rows)
```

```text
({'name': 'Admin'},)
```

### Lifecycle Commands

The three Lifecycle Commands prepare an Instance and are separate from the Operations. Each also exists as a manual entry point (see [Lifecycle](#lifecycle)). Each takes only the optional `instance` and returns a `LifecycleResult`.

| Command | What it does |
|---|---|
| `create_tables` | creates the Table of every Model Entity from its Declaration; Tables that already match are left unchanged; a difference with an existing Table stops the command before anything is changed |
| `insert_initial_data` | inserts every Initial Data record that is missing, skips a record that is already present in identical form, and fails on a conflicting one |
| `prepare` | runs `create_tables` and then `insert_initial_data`; it stops without running `insert_initial_data` when `create_tables` fails |

```python
print(db.insert_initial_data())
print(db.prepare(DatabaseInstance.SQLITE).command)
```

```text
LifecycleResult(command='insert_initial_data', instance=<DatabaseInstance.SQLITE: 'SQLITE'>, success=True, affected=23, message='0 Initial Data record(s) were inserted and 23 already present were skipped.')
prepare
```

## Instances

An Instance is one named database connection. The configured Instances are `SQLite` (active, the default) and `PostgreSQL` (inactive). `DatabaseInstance` has a member for each active Instance only, so today it holds `SQLITE` alone; an inactive Instance has no member and no Engine unit.

- **Default selection.** A call that omits `instance` runs on the default Instance, `SQLITE`. Passing `DatabaseInstance.SQLITE` is the same thing, written out.
- **Database-owned storage.** The SQLite Instance stores its data in one file inside the Database Component's own `db/` directory. Database creates and manages that file; it never resolves a location from an installed package, a virtual environment, the working directory, or a consumer, and it refuses any location that would leave `db/`. The directory is git-ignored.
- **No credentials.** Connection values and credentials stay in configuration; they never appear in `DatabaseInstance`, in an Operation request, or in a result or error.

## Setup

Database is a Python 3.14 library managed with `uv`. It consumes the Model library, which must sit next to it as the sibling directory `model/`.

```bash
cd database
uv sync
uv run python scripts/prepare.py
```

`uv sync` creates the virtual environment, installs the exact versions in `uv.lock`, and installs Model from `../model`. Generation runs Prepare automatically on the default Instance as its last step, so a generated Database is already prepared; running `scripts/prepare.py` again is safe and changes nothing. Run every example with `uv run python` from the `database/` directory.

## Use

All use goes through `database.interface`, with Field references and enumeration members and never strings. The groups below mirror the Interface.

**Entity Operations: change.** Add, update, switch on or off, and delete a record:

```python
broker = db.add(Broker(name="Use Broker", user_id=1))
broker.description = "Used in the walkthrough"
db.update(broker)
db.disable(Broker, broker.id)
db.enable(Broker, broker.id)
```

**Entity Operations: read.** Combine Filters, a combination, Orders, and a limit, or fetch one record by `id`:

```python
by_name = [Filter(Broker.name, FilterOperator.STARTS_WITH, "Use")]
print([item.description for item in db.list(Broker, by_name, orders=[Order(Broker.id, OrderDirection.DESCENDING)])])
print(db.get_by_id(Broker, broker.id).name)
```

```text
['Used in the walkthrough']
Use Broker
```

**Entity Operations: aggregate.** Summarize without fetching records:

```python
print(db.count(Broker), db.min(Broker, Broker.id) <= db.max(Broker, Broker.id), db.sum(Currency, Currency.decimal_digits))
```

```text
2 True 14
```

**Entity Operations: remove.** Delete one record, or empty an Entity with `truncate`:

```python
db.delete(Broker, broker.id)
print(db.count(Broker))
```

```text
1
```

**Database-wide Operation.** Run a native command when no Entity Operation covers the need:

```python
print(db.execute_command("select count(*) as records from Currency").rows)
```

```text
({'records': 8},)
```

**Lifecycle Commands.** Prepare an Instance, explicitly selecting one if you like:

```python
print(db.prepare(DatabaseInstance.SQLITE).success)
```

```text
True
```

## Lifecycle

CreateTables, InsertInitialData, and Prepare are public Lifecycle Commands, callable through the Interface (`db.create_tables()`, `db.insert_initial_data()`, `db.prepare()`) and by hand through the manual entry points. Each entry point only calls its command through the Interface and prints the same `LifecycleResult`.

```bash
uv run python scripts/create_tables.py
uv run python scripts/insert_initial_data.py
uv run python scripts/prepare.py
```

- **CreateTables** builds Tables only from the Model Entities and their Declarations; it never reads the Target. Running it again on matching Tables succeeds and changes nothing. If an existing Table differs from its Entity the command stops, names the Entity, and changes nothing: Database never alters an existing Table.
- **InsertInitialData** reads the complete Initial Data collection from its configuration, validates every record through its Entity, inserts the records that are missing, and skips records that are already present in identical form. A stored record that has the same identity (the same uniqueness-constraint values) but other values is a conflict: the command fails and inserts nothing. It never updates, deletes, duplicates, or overwrites a stored record. The result's `affected` is the number of records processed, so a repeat run reports every record as skipped.
- **Prepare** runs CreateTables and then InsertInitialData on the selected Instance. Generation runs it on the default Instance when it finishes, and a failure identifies the Instance and the command. Other active Instances are prepared only when you select them.

## Initial Data

Database inserts every Target-defined Initial Data record, in this order, with its values unchanged. Sensitivity markers and at-rest security instructions never omit, postpone, or block a record, and Database never hashes, encrypts, or masks a value. Where the Target does not give a concrete value (`Generate securely`), the record carries an empty string, which you fill in later. Records name each other by identity (for example an Instance's `user_id`), so they resolve when inserted into an empty Instance in this order.

| Entity | Records |
|---|---|
| User | `name` Admin, `username` admin, `password` empty, `api_key` empty |
| Trading Platform | MetaTrader 5 (`code` metatrader_5); Binance (`code` binance) |
| Instance | `name` MetaTrader, `user_id` 1, `trading_platform_id` 1, `ip` 127.0.0.1, `username` test, `password` empty, `api_key` empty |
| Currency | `user_id` 1 and: USD `$` United States (2 digits); EUR `€` Eurozone (2); GBP `£` United Kingdom (2); JPY `¥` Japan (0); CHF `CHF` Switzerland (2); CAD `C$` Canada (2); AUD `A$` Australia (2); NZD `NZ$` New Zealand (2) |
| Broker | `name` FxPro, `user_id` 1 |
| Asset | `broker_id` 1 and: EUR/USD Currency (`point_size` 0.0001, 5 digits); EUR/GBP Currency (0.001, 5); XAU/USD Commodity (0.01, 2); USOil Commodity (0.01, 3) |
| Account Group | `user_id` 1, `name` Default |
| Account | `name` Acc-1, `group_id` 1, `broker_id` 1, `instance_id` 1, `base_currency_id` 1, `username` test, `password` empty, `leverage` 100, `account_type` CFD |
| Trailing Group | `user_id` 1, `name` Default |
| Partial Group | `user_id` 1, `name` Default |
| Action Group | `user_id` 1, `name` Default |
| Action | `name` Default, `action_group_id` 1, `asset_id` 1, `account_id` 1, `partial_group_id` 1, `trailing_group_id` 1, `risk_by_reward` 1, `take_profit` 1, `stop_loss` 1 |

Trailing Rule, Partial Rule, and Position have no Initial Data. Once you change a seeded record, for example by filling an empty credential, InsertInitialData and Prepare report that record as a conflict instead of overwriting it.

## Verify

Run this script from the `database/` directory (`uv run python`, then paste it) after the Instance is prepared. It leaves the stored data as it found it and prints `OK` when every check holds.

```python
from pathlib import Path

import database.interface as interface
from database.interface import (
    CommandResult,
    Database,
    DatabaseInstance,
    Filter,
    FilterCombination,
    FilterOperator,
    Order,
    OrderDirection,
)
from model.interface import Broker, Currency

# public import: exactly the published contracts
published = {
    "Database", "DatabaseInstance", "Filter", "FilterOperator", "FilterCombination",
    "Order", "OrderDirection", "CommandResult", "LifecycleResult", "DatabaseError",
    "ConfigurationError", "InactiveInstanceError", "InvalidInputError",
    "DeclarationMismatchError", "ConnectionFailureError", "ExecutionError", "LifecycleError",
}
assert {name for name in vars(interface) if not name.startswith("_")} == published

# Instance selection: one active member, and the default Instance is the same Instance
assert [member.name for member in DatabaseInstance] == ["SQLITE"]
db = Database()
assert db.count(Currency) == db.count(Currency, instance=DatabaseInstance.SQLITE)

# query vocabulary: the closed member sets
assert [member.name for member in FilterOperator] == [
    "EQUALS", "NOT_EQUALS", "GREATER_THAN", "GREATER_OR_EQUAL", "LESS_THAN",
    "LESS_OR_EQUAL", "IN", "CONTAINS", "STARTS_WITH", "ENDS_WITH", "IS_NULL", "IS_NOT_NULL",
]
assert [member.name for member in FilterCombination] == ["AND", "OR"]
assert [member.name for member in OrderDirection] == ["ASCENDING", "DESCENDING"]

# each capability group, on a scratch record that is removed again
broker = db.add(Broker(name="Verify Broker", user_id=1))
try:
    assert db.get_by_id(Broker, broker.id).name == "Verify Broker"
    broker.description = "verified"
    assert db.update(broker).description == "verified"
    assert db.disable(Broker, broker.id).is_active is False
    assert db.enable(Broker, broker.id).is_active is True
    own = [Filter(Broker.name, FilterOperator.STARTS_WITH, "Verify")]
    assert [item.name for item in db.list(Broker, own, orders=[Order(Broker.id)])] == ["Verify Broker"]
    assert db.count(Broker, own) == 1
    assert db.min(Broker, Broker.id) <= db.max(Broker, Broker.id)
    assert db.sum(Currency, Currency.decimal_digits) == 14
    assert isinstance(db.execute_command("select 1 as one"), CommandResult)

    # persistent file location: a new gateway sees the record, stored in the Component's db directory
    assert Database().get_by_id(Broker, broker.id) is not None
    assert Path("db/application.db").resolve().parent == Path("db").resolve()
finally:
    assert db.delete(Broker, broker.id) is not None
assert db.get_by_id(Broker, broker.id) is None

# repeatable Lifecycle Commands: a second run succeeds and processes the same records
first, second = db.prepare(), db.prepare()
assert first.success and second.success and first.affected == second.affected
assert db.create_tables().success and db.insert_initial_data().success
print("OK")
```

```text
OK
```

## Troubleshooting

### An Instance is inactive

`InactiveInstanceError` means the selected Instance is configured but not active. `DatabaseInstance` has a member only for each active Instance, so an inactive Instance such as PostgreSQL cannot be selected by an imported member, and it has no Engine unit. To use an Instance, activate it in the Database Preferences and regenerate Database, which publishes its member and creates its Engine unit; until then use `SQLITE` or omit `instance`.

### A Table differs from its Entity

`DeclarationMismatchError` from `create_tables` or `prepare` means a Table that already exists no longer matches its Entity. The message names every differing Entity and what differs, for example `Broker (Field description is missing)`, and says that nothing was changed. Database never alters an existing Table and never migrates data. Restore the Table to match the Entity, or, when the stored data can be recreated, stop every consumer, delete the Instance's file `db/application.db` (Database owns it), and run `prepare` again to rebuild it from the current Entities and Initial Data.

### Initial Data values are empty

Where the Target asks for a value to be generated securely (the passwords and API keys of the seeded User, Instance, and Account), Database inserts an empty string and never generates a value. Fill the value in yourself by updating the stored record:

```python
from model.interface import User

admin = db.get_by_id(User, 1)
admin.password = "choose-a-password"
admin.api_key = "choose-an-api-key"
print(db.update(admin).username)
```

```text
admin
```

Database stores what you supply unchanged. After you change a seeded record, `insert_initial_data` and `prepare` report that record as a conflict and insert nothing, because they never overwrite stored data.
