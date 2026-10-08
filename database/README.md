# Database

## Overview

Database persists the Model Entities and gives every consumer one stable way to read and write them. A consumer imports the Interface, creates `database_interface` once, and calls an Operation with Entities, Fields and Instances passed as imported values, never as strings.

```python
from database.interface import database_interface
from model.interface import Currency

db = database_interface()
stored = db.add(Currency(user_id=1, code="XAU", symbol="Au", decimal_digits=2))
print(stored.id, [currency.code for currency in db.list(Currency)])
db.delete(Currency, stored.id)
```

## Interface

The Interface is the module `database.interface`. It publishes exactly six groups and nothing else. Each group is named `database_` followed by its key, and a consumer imports a group and reaches every member through it.

| Group | What it is |
| --- | --- |
| `database_interface` | the class a consumer creates once to call every Entity Operation and the Command Operation |
| `database_setup` | the class a consumer creates to call the Setup Operations |
| `database_value` | what a consumer passes to an Operation: Filters, Orders and their vocabulary |
| `database_instance` | the active Instances a call can run on |
| `database_result` | what a consumer reads back from a command or a Setup Operation |
| `database_error` | every error, so a consumer can catch it |

Every Operation takes exactly the parameters listed below, in that order. The optional `instance` is always last. An Entity is passed as the Entity class (or, for `add` and `update`, an Entity instance) imported from Model, and a Field is passed as the Entity's class attribute for it, such as `Currency.code`. A string is never accepted in their place.

### database_interface

Creating it takes no argument and opens no connection.

```python
from database.interface import database_interface

db = database_interface()
```

#### `add(entity, instance=None)`

Store one new Entity instance.

- **Accepts:** an Entity instance whose generated Fields are still pending.
- **Returns:** the stored Entity, including generated values such as `id`.
- **Instance:** the optional last parameter selects a `database_instance` member; without it the call runs on the default Instance.

```python
from database.interface import database_interface
from model.interface import Currency

db = database_interface()
stored = db.add(Currency(user_id=1, code="XAU", symbol="Au", decimal_digits=2))
print(stored.id, stored.code)
db.delete(Currency, stored.id)
```

#### `update(entity, instance=None)`

Replace every mutable Field of a stored record. The Entity's `id` only locates the record; `id` and any other immutable Field never change.

- **Accepts:** an Entity instance that carries its stored `id`.
- **Returns:** the stored Entity, or `None` when no record has that `id`.
- **Instance:** the optional last parameter selects a `database_instance` member; without it the call runs on the default Instance.

```python
from database.interface import database_interface
from model.interface import Broker

db = database_interface()
broker = db.get_by_id(Broker, 1)
broker.description = "Primary broker"
print(db.update(broker).description)
broker.description = None
db.update(broker)
```

#### `list(entity, filters=None, combination=None, orders=None, limit=None, instance=None)`

Read the records that match optional Filters, ordered and limited.

- **Accepts:** an Entity class, then optional `filters`, `combination`, `orders` and `limit`.
- **Returns:** the matching Entity instances; with no Order they are ordered by `id` ascending, with no `combination` the Filters are combined with `AND`, and with no `limit` (or a zero or negative one) every match is returned.
- **Instance:** the optional last parameter selects a `database_instance` member; without it the call runs on the default Instance.

```python
from database.interface import database_interface, database_value
from model.interface import Currency

db = database_interface()
found = db.list(
    Currency,
    filters=[
        database_value.Filter(
            Currency.decimal_digits, database_value.FilterOperator.EQUALS, 2
        )
    ],
    orders=[
        database_value.Order(Currency.code, database_value.OrderDirection.DESCENDING)
    ],
    limit=3,
)
print([currency.code for currency in found])
```

#### `get_by_id(entity, id, instance=None)`

Read one record by its `id`.

- **Accepts:** an Entity class and an integer `id`.
- **Returns:** the Entity, or `None` when no record exists.
- **Instance:** the optional last parameter selects a `database_instance` member; without it the call runs on the default Instance.

```python
from database.interface import database_interface
from model.interface import User

db = database_interface()
print(db.get_by_id(User, 1).username)
print(db.get_by_id(User, 999))
```

#### `delete(entity, id, instance=None)`

Remove one record.

- **Accepts:** an Entity class and an integer `id`.
- **Returns:** the final deleted Entity, or `None` when no record exists.
- **Instance:** the optional last parameter selects a `database_instance` member; without it the call runs on the default Instance.

```python
from database.interface import database_interface
from model.interface import Currency

db = database_interface()
stored = db.add(Currency(user_id=1, code="TMP", decimal_digits=2))
print(db.delete(Currency, stored.id).code)
print(db.delete(Currency, stored.id))
```

#### `enable(entity, id, instance=None)`

Set only `is_active` to true.

- **Accepts:** an Entity class and an integer `id`.
- **Returns:** the final Entity, including when it was already enabled, or `None` when no record exists.
- **Instance:** the optional last parameter selects a `database_instance` member; without it the call runs on the default Instance.

```python
from database.interface import database_interface
from model.interface import Broker

db = database_interface()
print(db.enable(Broker, 1).is_active)
```

#### `disable(entity, id, instance=None)`

Set only `is_active` to false.

- **Accepts:** an Entity class and an integer `id`.
- **Returns:** the final Entity, including when it was already disabled, or `None` when no record exists.
- **Instance:** the optional last parameter selects a `database_instance` member; without it the call runs on the default Instance.

```python
from database.interface import database_interface
from model.interface import Broker

db = database_interface()
print(db.disable(Broker, 1).is_active)
db.enable(Broker, 1)
```

#### `count(entity, filters=None, combination=None, instance=None)`

Count the records that match optional Filters.

- **Accepts:** an Entity class, then optional `filters` and `combination`.
- **Returns:** the matching count.
- **Instance:** the optional last parameter selects a `database_instance` member; without it the call runs on the default Instance.

```python
from database.interface import database_interface, database_value
from model.interface import Asset

db = database_interface()
print(db.count(Asset))
print(
    db.count(
        Asset,
        [
            database_value.Filter(
                Asset.category, database_value.FilterOperator.EQUALS, "Commodity"
            )
        ],
    )
)
```

#### `sum(entity, field, filters=None, combination=None, instance=None)`

Add up a numeric Field (`integer`, `float` or `decimal`), ignoring null values.

- **Accepts:** an Entity class, a Field reference, then optional `filters` and `combination`.
- **Returns:** the total, or zero when nothing matches; decimal totals are exact.
- **Instance:** the optional last parameter selects a `database_instance` member; without it the call runs on the default Instance.

```python
from database.interface import database_interface
from model.interface import Currency

db = database_interface()
print(db.sum(Currency, Currency.decimal_digits))
```

#### `min(entity, field, filters=None, combination=None, instance=None)`

Find the smallest value of a comparable Field (`string`, `integer`, `float`, `decimal`, `datetime`, `date` or `time`), ignoring null values.

- **Accepts:** an Entity class, a Field reference, then optional `filters` and `combination`.
- **Returns:** the smallest value, or `None` when nothing matches.
- **Instance:** the optional last parameter selects a `database_instance` member; without it the call runs on the default Instance.

```python
from database.interface import database_interface
from model.interface import Currency

db = database_interface()
print(db.min(Currency, Currency.code))
```

#### `max(entity, field, filters=None, combination=None, instance=None)`

Find the largest value of a comparable Field, ignoring null values.

- **Accepts:** an Entity class, a Field reference, then optional `filters` and `combination`.
- **Returns:** the largest value, or `None` when nothing matches.
- **Instance:** the optional last parameter selects a `database_instance` member; without it the call runs on the default Instance.

```python
from database.interface import database_interface
from model.interface import Currency

db = database_interface()
print(db.max(Currency, Currency.code))
```

#### `truncate(entity, instance=None)`

Remove every record of one Entity and keep its Table.

- **Accepts:** an Entity class.
- **Returns:** the number of deleted records.
- **Instance:** the optional last parameter selects a `database_instance` member; without it the call runs on the default Instance.

```python
from database.interface import database_interface
from model.interface import Position

db = database_interface()
print(db.truncate(Position))
```

#### `execute_command(command, parameters=None, instance=None)`

Run a native command in the Engine's query language, including a schema change; `create_tables` remains the standard way to prepare Tables.

- **Accepts:** a non-empty `command` text and optional `parameters` (a sequence for `?` placeholders or a mapping for `:name` placeholders).
- **Returns:** a `CommandResult`; a command that fails to run returns an unsuccessful result with a public message.
- **Instance:** the optional last parameter selects a `database_instance` member; without it the call runs on the default Instance.

```python
from database.interface import database_interface

db = database_interface()
result = db.execute_command("select code from Currency where code = ?", ["USD"])
print(result.success, result.rows, result.columns)
```

### database_setup

Creating it takes no argument and opens no connection. Each Setup Operation takes only the optional `instance`.

#### `create_tables(instance=None)`

Create every Table of the Model Entity Collection from the Entities and their Declarations. Matching Tables are left unchanged; a Table that differs from its Entity stops the command with `DeclarationMismatchError`, naming the Table. It returns a `SetupResult`.

```python
from database.interface import database_setup

result = database_setup().create_tables()
print(result.success, result.affected)
```

#### `insert_initial_data(instance=None)`

Insert every configured Initial Data record that is missing. An identical record that is already stored is skipped; a record that conflicts with a different stored record fails with `SetupError` and inserts nothing. It returns a `SetupResult`.

```python
from database.interface import database_setup

result = database_setup().insert_initial_data()
print(result.success, result.affected)
```

#### `prepare(instance=None)`

Run `create_tables` and then `insert_initial_data`. When `create_tables` does not complete, `insert_initial_data` is not run and the result is unsuccessful. It returns a `SetupResult`.

```python
from database.interface import database_setup

result = database_setup().prepare()
print(result.success, result.message)
```

### database_value

`database_value` holds what a consumer builds and passes to `list`, `count`, `sum`, `min` and `max`. A Field is always the Entity's class attribute for it, never its name.

#### `Filter(field, operator, value=None)`

One condition: a Field reference of the Entity, a `FilterOperator` member, and a value compatible with the Field (integers are accepted for `float` and `decimal` Fields, floats never for `decimal`; a `datetime` must carry a timezone). `IS_NULL` and `IS_NOT_NULL` take no value; `IN` takes a non-empty collection. A Filter is immutable.

```python
from database.interface import database_interface, database_value
from model.interface import Currency

db = database_interface()
condition = database_value.Filter(
    Currency.code, database_value.FilterOperator.EQUALS, "USD"
)
print([currency.id for currency in db.list(Currency, [condition])])
```

#### `Order(field, direction=OrderDirection.ASCENDING)`

One ordering over any Field of the Entity; booleans order as `False` before `True`. Orders are applied in the order supplied and replace the default order (`id` ascending). Aggregate Operations accept no Order. An Order is immutable.

```python
from database.interface import database_interface, database_value
from model.interface import Asset

db = database_interface()
orders = [
    database_value.Order(Asset.category),
    database_value.Order(Asset.digits, database_value.OrderDirection.DESCENDING),
]
print([asset.symbol for asset in db.list(Asset, orders=orders)])
```

#### `FilterCombination`

How several Filters are combined: `AND` (the default) or `OR`.

```python
from database.interface import database_interface, database_value
from model.interface import Currency

db = database_interface()
value = database_value
filters = [
    value.Filter(Currency.code, value.FilterOperator.EQUALS, "USD"),
    value.Filter(Currency.code, value.FilterOperator.EQUALS, "EUR"),
]
print(
    db.count(Currency, filters, value.FilterCombination.AND),
    db.count(Currency, filters, value.FilterCombination.OR),
)
```

#### `OrderDirection`

`ASCENDING` (the default) or `DESCENDING`.

```python
from database.interface import database_interface, database_value
from model.interface import Currency

db = database_interface()
value = database_value
for direction in value.OrderDirection:
    found = db.list(Currency, orders=[value.Order(Currency.code, direction)], limit=2)
    print(direction.name, [currency.code for currency in found])
```

#### `FilterOperator`

Every member, with what it means and an example (a zero or negative `limit` means no limit; every enumeration member's value equals its name):

| Member | Meaning | Example |
| --- | --- | --- |
| `EQUALS` | the Field equals the value | `Filter(Currency.code, FilterOperator.EQUALS, "USD")` |
| `NOT_EQUALS` | the Field differs from the value; records whose Field is null do not match | `Filter(Currency.code, FilterOperator.NOT_EQUALS, "USD")` |
| `GREATER_THAN` | greater than the value | `Filter(Asset.digits, FilterOperator.GREATER_THAN, 2)` |
| `GREATER_OR_EQUAL` | greater than or equal to the value | `Filter(Asset.digits, FilterOperator.GREATER_OR_EQUAL, 3)` |
| `LESS_THAN` | less than the value | `Filter(Asset.point_size, FilterOperator.LESS_THAN, 0.01)` |
| `LESS_OR_EQUAL` | less than or equal to the value | `Filter(Asset.point_size, FilterOperator.LESS_OR_EQUAL, 0.01)` |
| `IN` | the Field equals one of a non-empty collection of values | `Filter(Currency.code, FilterOperator.IN, ["USD", "EUR"])` |
| `CONTAINS` | a text Field contains the text (wildcard characters are literal) | `Filter(Asset.symbol, FilterOperator.CONTAINS, "/")` |
| `STARTS_WITH` | a text Field starts with the text | `Filter(Asset.symbol, FilterOperator.STARTS_WITH, "EUR")` |
| `ENDS_WITH` | a text Field ends with the text | `Filter(Asset.symbol, FilterOperator.ENDS_WITH, "USD")` |
| `IS_NULL` | the Field is null (takes no value) | `Filter(User.description, FilterOperator.IS_NULL)` |
| `IS_NOT_NULL` | the Field is not null (takes no value) | `Filter(Currency.symbol, FilterOperator.IS_NOT_NULL)` |

```python
from database.interface import database_interface, database_value
from model.interface import Asset, Currency, User

db = database_interface()
value = database_value
operator = value.FilterOperator
examples = [
    (Currency, value.Filter(Currency.code, operator.EQUALS, "USD")),
    (Currency, value.Filter(Currency.code, operator.NOT_EQUALS, "USD")),
    (Asset, value.Filter(Asset.digits, operator.GREATER_THAN, 2)),
    (Asset, value.Filter(Asset.digits, operator.GREATER_OR_EQUAL, 3)),
    (Asset, value.Filter(Asset.point_size, operator.LESS_THAN, 0.01)),
    (Asset, value.Filter(Asset.point_size, operator.LESS_OR_EQUAL, 0.01)),
    (Currency, value.Filter(Currency.code, operator.IN, ["USD", "EUR"])),
    (Asset, value.Filter(Asset.symbol, operator.CONTAINS, "/")),
    (Asset, value.Filter(Asset.symbol, operator.STARTS_WITH, "EUR")),
    (Asset, value.Filter(Asset.symbol, operator.ENDS_WITH, "USD")),
    (User, value.Filter(User.description, operator.IS_NULL)),
    (Currency, value.Filter(Currency.symbol, operator.IS_NOT_NULL)),
]
for entity, condition in examples:
    print(condition.operator.name, db.count(entity, [condition]))
```


### database_instance

`database_instance` is itself an enumeration with one member per active configured Instance, named by the Instance key in upper case. An inactive Instance has no member. It carries no connection value.

```python
from database.interface import database_instance

print([member.name for member in database_instance])
```

### database_result

Both results are immutable.

#### `CommandResult`

Returned by `execute_command`: `rows` (a tuple of row mappings, or `None`), `affected` (the affected row count, or `None`), `columns` (ordered column names, or `None`), `success`, `message` and `instance`.

```python
from database.interface import database_instance, database_interface, database_result

db = database_interface()
result = db.execute_command("select code from Currency where code = ?", ["USD"])
print(
    isinstance(result, database_result.CommandResult),
    result.success,
    result.rows,
    result.columns,
)
print(result.affected, result.message, result.instance is database_instance.SQLITE)

failed = db.execute_command("select * from no_such_table")
print(failed.success, failed.rows, failed.message)
```

#### `SetupResult`

Returned by every Setup Operation: `command`, `instance`, `success`, `affected` (the processed Table or record count), and `message`.

```python
import dataclasses

from database.interface import database_result, database_setup

result = database_setup().prepare()
print(
    isinstance(result, database_result.SetupResult),
    result.command,
    result.success,
    result.affected,
)
print(result.instance.name, result.message)
try:
    result.success = False
except dataclasses.FrozenInstanceError:
    print("immutable")
```


### database_error

Every error derives from `DatabaseError`; each kind is its own error. No error carries a connection value or a credential.

#### `DatabaseError`

The base of every Database error; catch it to catch them all.

```python
from database.interface import database_error, database_interface

db = database_interface()
try:
    db.list("Currency")
except database_error.DatabaseError as error:
    print(type(error).__name__)
```

#### `ConfigurationError`

The configuration or the selected Instance is invalid. Raised when the Database loads, before any connection is opened.

```python
import importlib

# An invalid configuration fails when the Interface loads, before any connection is opened.
try:
    interface = importlib.import_module("database.interface")
except Exception as error:
    print(type(error).__name__, error)
else:
    print("configuration valid:", sorted(interface.__all__))
```

#### `InactiveInstanceError`

An Instance that is no longer active was selected.

```python
from database.interface import database_error, database_instance, database_interface
from model.interface import Currency

db = database_interface()
try:
    print(db.count(Currency, instance=database_instance.SQLITE))
except database_error.InactiveInstanceError:
    print("the selected Instance is no longer active")
```

#### `InvalidInputError`

A request holds invalid input: a string where an imported value is required, a Field of another Entity, an incompatible operator or value, an unsuitable aggregate Field. Raised before any storage is touched.

```python
from database.interface import database_error, database_interface

db = database_interface()
try:
    db.get_by_id("Currency", 1)
except database_error.InvalidInputError as error:
    print(error)
```

#### `DeclarationMismatchError`

An existing Table differs from the Declaration of its Entity, or a stored row does not satisfy its Entity's contract.

```python
from database.interface import database_error, database_interface, database_setup

db = database_interface()
db.execute_command("alter table Broker add column extra text")
try:
    database_setup().create_tables()
except database_error.DeclarationMismatchError as error:
    print(error)
finally:
    db.execute_command("alter table Broker drop column extra")
```

#### `ConnectionFailureError`

The connection to the Instance's storage could not be established.

```python
from database.interface import database_error, database_interface
from model.interface import Currency

db = database_interface()
try:
    print(db.count(Currency))
except database_error.ConnectionFailureError:
    print("the storage could not be opened")
```

#### `ExecutionError`

A command or operation failed while running, for example by breaking a constraint.

```python
from database.interface import database_error, database_interface
from model.interface import Currency

db = database_interface()
try:
    db.add(Currency(user_id=1, code="USD"))
except database_error.ExecutionError as error:
    print(error)
```

#### `SetupError`

A Setup Operation did not complete, for example because an Initial Data record conflicts with a stored record.

```python
from database.interface import database_error, database_interface, database_setup
from model.interface import User

db = database_interface()
user = db.get_by_id(User, 1)
user.password = "changed"
db.update(user)
try:
    database_setup().insert_initial_data()
except database_error.SetupError as error:
    print(error)
finally:
    user.password = ""
    db.update(user)
```

## Instances

An Instance is one named database connection and storage identity. Which Instances exist, which are active and which is the default are set in the Database Configuration at the Component root; a consumer never supplies or sees a connection value.

- `database_instance` has exactly one member for every active Instance, named by its key in upper case, and none for an inactive one. With the delivered configuration the only member is `database_instance.SQLITE`.
- Every Operation and Setup Operation accepts an optional `instance`. Without it the call runs on the default Instance. A string, or anything that is not a `database_instance` member, is refused with `InvalidInputError` before any storage is touched.
- Storage is owned by Database. A file-backed Instance keeps its database file inside the `db` directory of the Component, named by the Instance's database value, and the file can never resolve outside that directory. Database creates the directory and the file when it first needs them; no consumer, installed package, virtual environment or working directory chooses the location.

```python
from database.interface import database_instance, database_interface
from model.interface import User

db = database_interface()
print(db.get_by_id(User, 1, database_instance.SQLITE).username)
print(db.get_by_id(User, 1).username)
```

## Setup

Database is a Python library managed with [uv](https://docs.astral.sh/uv/). It needs Python 3.14 or newer and uses the Model library of this project as a local path dependency.

1. Open the Database directory.
2. Install the locked dependencies, Model included, into an isolated environment:

   ```bash
   uv sync
   ```

3. Prepare the default Instance's storage:

   ```bash
   uv run python scripts/prepare.py
   ```

4. Confirm the Interface loads:

   ```bash
   uv run python -c "import database.interface"
   ```

Another Component of this project uses Database as a local path dependency on this directory, never from a package index. A consumer that imports Entities also depends on Model the same way. In the consumer's `pyproject.toml`:

```toml
[project]
dependencies = ["database", "model"]

[tool.uv.sources]
database = { path = "../database" }
model = { path = "../model" }
```

## Use

Everything is reached through the Interface. Entities, Fields and vocabulary are imported values; a Field is the Entity's class attribute for it.

```python
from database.interface import (
    database_error,
    database_instance,
    database_interface,
    database_value,
)
from model.interface import Asset, Currency

db = database_interface()
value = database_value

# Create, read, change, enable and disable, delete.
currency = db.add(Currency(user_id=1, code="XAU", symbol="Au", decimal_digits=2))
currency.symbol = "AU"
print(db.update(currency).symbol)
print(
    db.disable(Currency, currency.id).is_active,
    db.enable(Currency, currency.id).is_active,
)
print(db.get_by_id(Currency, currency.id).code)
db.delete(Currency, currency.id)

# Filters, combination, orders and limit.
commodities = db.list(
    Asset,
    filters=[
        value.Filter(Asset.category, value.FilterOperator.EQUALS, "Commodity"),
        value.Filter(Asset.digits, value.FilterOperator.GREATER_OR_EQUAL, 3),
    ],
    combination=value.FilterCombination.OR,
    orders=[value.Order(Asset.symbol, value.OrderDirection.DESCENDING)],
    limit=3,
    instance=database_instance.SQLITE,
)
print([asset.symbol for asset in commodities])

# Aggregates.
print(
    db.count(Asset),
    db.sum(Asset, Asset.digits),
    db.min(Asset, Asset.point_size),
    db.max(Asset, Asset.symbol),
)

# A native command and its result.
result = db.execute_command("select count(*) as total from Asset")
print(result.success, result.rows[0]["total"])

# Errors are catchable under one base.
try:
    db.list("Asset")
except database_error.InvalidInputError as error:
    print("refused:", type(error).__name__)
```

## Setup Operations

Preparing storage is a different act from using it, so it has its own group, `database_setup`, and its own manual entry points. Each Setup Operation returns a `SetupResult`.

| Setup Operation | Manual entry point | What it does |
| --- | --- | --- |
| `create_tables` | `uv run python scripts/create_tables.py` | creates the Table of every Model Entity from its Declaration; stops on a difference with an existing Table |
| `insert_initial_data` | `uv run python scripts/insert_initial_data.py` | inserts the configured Initial Data that is missing; skips identical records; fails on a conflicting one |
| `prepare` | `uv run python scripts/prepare.py` | runs `create_tables` and then `insert_initial_data`; stops when `create_tables` fails |

Each entry point runs its Setup Operation on the default Instance through the Interface, prints the result, and exits with status 1 and a message when it fails. They hold no logic of their own. Running any of them again changes nothing that already matches.

Generation runs `prepare` automatically on the default Instance; a failure fails generation. Other active Instances are prepared only when you select them explicitly:

```python
from database.interface import database_instance, database_setup

result = database_setup().prepare(database_instance.SQLITE)
print(result.success, result.instance.name)
```

## Initial Data

Initial Data is the shared, repeatable collection of records the Target defines, kept in the Database Configuration. `insert_initial_data` validates each record through its Entity, inserts the records that are missing, and skips records that are already stored. Database inserts every value unchanged and never omits or delays a record because of what a Field means, including credential Fields.

A value the Target does not state concretely (`Generate securely`) is stored as an empty string. Database never produces a value itself; fill such values afterwards with `update`.

The collection holds 23 records, in this order:

### User

1. `name` = `Admin`, `username` = `admin`, `password` = empty, `api_key` = empty

### TradingPlatform

1. `name` = `MetaTrader 5`, `code` = `metatrader_5`
2. `name` = `Binance`, `code` = `binance`

### Instance

1. `name` = `MetaTrader`, `user_id` = `1`, `trading_platform_id` = `1`, `ip` = `127.0.0.1`, `username` = `test`, `password` = empty, `api_key` = empty

### Currency

1. `user_id` = `1`, `code` = `USD`, `symbol` = `$`, `country` = `United States`, `decimal_digits` = `2`
2. `user_id` = `1`, `code` = `EUR`, `symbol` = `€`, `country` = `Eurozone`, `decimal_digits` = `2`
3. `user_id` = `1`, `code` = `GBP`, `symbol` = `£`, `country` = `United Kingdom`, `decimal_digits` = `2`
4. `user_id` = `1`, `code` = `JPY`, `symbol` = `¥`, `country` = `Japan`, `decimal_digits` = `0`
5. `user_id` = `1`, `code` = `CHF`, `symbol` = `CHF`, `country` = `Switzerland`, `decimal_digits` = `2`
6. `user_id` = `1`, `code` = `CAD`, `symbol` = `C$`, `country` = `Canada`, `decimal_digits` = `2`
7. `user_id` = `1`, `code` = `AUD`, `symbol` = `A$`, `country` = `Australia`, `decimal_digits` = `2`
8. `user_id` = `1`, `code` = `NZD`, `symbol` = `NZ$`, `country` = `New Zealand`, `decimal_digits` = `2`

### Broker

1. `name` = `FxPro`, `user_id` = `1`

### Asset

1. `broker_id` = `1`, `symbol` = `EUR/USD`, `category` = `Currency`, `point_size` = `0.0001`, `digits` = `5`
2. `broker_id` = `1`, `symbol` = `EUR/GBP`, `category` = `Currency`, `point_size` = `0.001`, `digits` = `5`
3. `broker_id` = `1`, `symbol` = `XAU/USD`, `category` = `Commodity`, `point_size` = `0.01`, `digits` = `2`
4. `broker_id` = `1`, `symbol` = `USOil`, `category` = `Commodity`, `point_size` = `0.01`, `digits` = `3`

### AccountGroup

1. `user_id` = `1`, `name` = `Default`

### Account

1. `name` = `Acc-1`, `group_id` = `1`, `broker_id` = `1`, `instance_id` = `1`, `base_currency_id` = `1`, `username` = `test`, `password` = empty, `leverage` = `100`, `account_type` = `CFD`

### TrailingGroup

1. `user_id` = `1`, `name` = `Default`

### PartialGroup

1. `user_id` = `1`, `name` = `Default`

### ActionGroup

1. `user_id` = `1`, `name` = `Default`

### Action

1. `name` = `Default`, `action_group_id` = `1`, `asset_id` = `1`, `account_id` = `1`, `partial_group_id` = `1`, `trailing_group_id` = `1`, `risk_by_reward` = `1`, `take_profit` = `1`, `stop_loss` = `1`

## Verify

Run the script below from the Database directory with `uv run python`, after `prepare` has run. It checks, using only the Interface: the public import, Instance selection, the query vocabulary, each published group, the persistent file location, and that the Setup Operations are repeatable. It restores everything it changes and prints `Database verified` when every check holds. It does not run `truncate`, which removes data.

```python
import dataclasses
from enum import Enum
from pathlib import Path

import database.interface as interface
from database.interface import (
    database_error,
    database_instance,
    database_interface,
    database_result,
    database_setup,
    database_value,
)
from model.interface import Asset, Currency, User

GROUPS = [
    "database_error",
    "database_instance",
    "database_interface",
    "database_result",
    "database_setup",
    "database_value",
]


def refused(action, error=database_error.InvalidInputError):
    try:
        action()
    except error:
        return True
    return False


# Public import: exactly the six groups.
assert sorted(name for name in vars(interface) if not name.startswith("_")) == GROUPS
assert sorted(interface.__all__) == GROUPS

# Instance selection: the group is the enumeration; a call without an Instance uses the default.
assert issubclass(database_instance, Enum) and [m.name for m in database_instance] == [
    "SQLITE"
]
db = database_interface()
assert (
    db.get_by_id(User, 1).id == db.get_by_id(User, 1, database_instance.SQLITE).id == 1
)
assert refused(lambda: db.get_by_id(User, 1, "SQLITE"))

# Query vocabulary: closed enumerations whose values equal their names, immutable values.
value = database_value
assert [m.name for m in value.FilterOperator] == [
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
assert [m.name for m in value.FilterCombination] == ["AND", "OR"]
assert [m.name for m in value.OrderDirection] == ["ASCENDING", "DESCENDING"]
assert all(
    m.value == m.name
    for e in (value.FilterOperator, value.FilterCombination, value.OrderDirection)
    for m in e
)
condition = value.Filter(Currency.code, value.FilterOperator.EQUALS, "USD")
assert refused(
    lambda: setattr(condition, "value", "EUR"), dataclasses.FrozenInstanceError
)
assert refused(
    lambda: db.list(
        Currency, [value.Filter("code", value.FilterOperator.EQUALS, "USD")]
    )
)
assert refused(
    lambda: db.list(Currency, [value.Filter(Currency.code, "EQUALS", "USD")])
)
assert refused(lambda: db.list("Currency"))

# Interface group: every Entity Operation and the Command Operation.
stored = db.add(Currency(user_id=1, code="VFY", symbol="V", decimal_digits=2))
assert stored.id is not None and db.get_by_id(Currency, stored.id).code == "VFY"
stored.symbol = "W"
assert db.update(stored).symbol == "W"
assert (
    db.disable(Currency, stored.id).is_active is False
    and db.enable(Currency, stored.id).is_active is True
)
assert [
    c.code
    for c in db.list(
        Currency, [value.Filter(Currency.code, value.FilterOperator.EQUALS, "VFY")]
    )
] == ["VFY"]
assert (
    db.count(
        Currency, [value.Filter(Currency.code, value.FilterOperator.EQUALS, "VFY")]
    )
    == 1
)
assert db.min(Currency, Currency.code) <= "VFY" <= db.max(Currency, Currency.code)
assert db.sum(Currency, Currency.decimal_digits) >= 2
assert (
    db.delete(Currency, stored.id).code == "VFY"
    and db.delete(Currency, stored.id) is None
)
assert db.get_by_id(Currency, stored.id) is None
assert db.count(Asset) == len(db.list(Asset)) == 4
command = db.execute_command("select 1 as one")
assert (
    isinstance(command, database_result.CommandResult)
    and command.success
    and command.rows == ({"one": 1},)
)
assert command.instance is database_instance.SQLITE

# Setup group and repeatable Setup Operations: running them again changes nothing.
setup = database_setup()
before = {e.__name__: db.count(e) for e in (User, Currency, Asset)}
first = setup.prepare()
second = setup.prepare()
assert (
    isinstance(first, database_result.SetupResult) and first.success and second.success
)
assert first.affected == second.affected and first.command == "prepare"
assert setup.create_tables().success and setup.insert_initial_data().success
assert before == {e.__name__: db.count(e) for e in (User, Currency, Asset)}

# Error group: one base, distinct kinds.
kinds = [
    getattr(database_error, name)
    for name in vars(database_error)
    if name.endswith("Error")
]
assert len(kinds) == 8 and all(
    issubclass(k, database_error.DatabaseError) for k in kinds
)

# Persistent file location: the database file lives in the Database-owned storage directory.
location = Path("db") / "application.db"
assert location.is_file() and location.resolve().parent.name == "db"
assert location.resolve().parent.parent == Path.cwd().resolve()

print("Database verified")
```

## Troubleshooting

- **`ConfigurationError` when the Interface loads** — the Database Configuration is invalid: a missing section or Instance member, an Instance that names an unknown Engine, a default Instance that is missing or inactive, an unknown enumeration name, or a database value that would leave the storage directory. The message names the item, never a value. Fix `config.yaml`; Database never repairs it.
- **An inactive Instance has no `database_instance` member** — only active Instances are members. Set the Instance's `active` to true in the configuration, make sure its Engine has a unit, and reload.
- **`InactiveInstanceError`** — the selected Instance is not active in the configuration.
- **`InvalidInputError`** — a string was passed where an imported value is required (an Entity, a Field, an operator, an Instance), a Field belongs to another Entity, or a value does not fit the Field. Import the Entity from Model, use `Entity.field` references, and use `database_value` and `database_instance` members.
- **`DeclarationMismatchError` naming a Table** — an existing Table differs from the Declaration of its Entity (for example after the Model changed). Database only creates Tables from the current Entities and never alters an existing Table. Restore the Table to match its Entity, or remove the database file in the `db` directory and run `prepare` again to start from empty storage.
- **Initial Data values are empty** — a value the Target gives as `Generate securely` is stored as an empty string. Fill it with `update`; Database never generates values.
- **`SetupError` from `insert_initial_data`** — a configured Initial Data record conflicts with a different stored record that shares its uniqueness key (for example you changed the stored record). Nothing was inserted. Restore the stored record or change the configured one.
- **`ExecutionError`** — an operation broke a constraint (a duplicate unique value or a missing related record). The message names the constraint, never a value.
- **`ConnectionFailureError`** — the storage directory or database file could not be created or opened; check that the Component directory is writable.
