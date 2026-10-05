# Database

Database is the persistence gateway of the Trading Assistant. It stores the Model Entities in a Database-owned storage and offers one stable, typed boundary, the Interface, through which a consumer adds, updates, finds, counts, changes and removes Entity data on a selected Instance.

## Overview

Create a `Database` and call it with Model Entities. Nothing is a string: Entities, Fields, operators and Instances are imported values.

```python
from database.interface import Database
from model.interface import Broker

db = Database()
broker = db.add(Broker(name="Overview Example", user_id=1))
print(broker.id, [item.name for item in db.list(Broker)])
```

Creating `Database()` opens no connection. A connection is made, on the default Instance unless another is chosen, when a call is made.

## Interface

Everything is imported from `database.interface`. The Interface publishes exactly these contracts and nothing else; Core, Engine implementations, the configuration, connection values and storage paths are never published.

| Contract | What it is |
| --- | --- |
| `Database` | The object that carries every Operation and Lifecycle Command. |
| `DatabaseInstance` | The enumeration of the active configured Instances. |
| `Filter`, `FilterOperator`, `FilterCombination` | The condition value and the vocabulary used to build queries. |
| `Order`, `OrderDirection` | The ordering value and its directions. |
| `CommandResult` | The result of `execute_command`. |
| `LifecycleResult` | The result of a Lifecycle Command. |
| `DatabaseError` and seven specific errors | The failure kinds, listed below. |

Every Operation and Lifecycle Command takes an optional `instance` as its last parameter. When it is omitted, the call runs on the configured default Instance. A missing record is never an error: Operations that look for one return `None`.

### DatabaseInstance

An enumeration with one member per active configured Instance and none for an inactive one. Each member's value equals its name and carries no connection value. With the shipped configuration it has one member, `DatabaseInstance.SQLITE`.

```python
from database.interface import Database, DatabaseInstance
from model.interface import User

db = Database()
print([member.name for member in DatabaseInstance])
print(db.count(User, instance=DatabaseInstance.SQLITE))
```

### FilterOperator

An enumeration of twelve comparison operators. A `Filter` uses one of them.

| Member | Selects records whose Field value… | Value |
| --- | --- | --- |
| `EQUALS` | equals the value | one value |
| `NOT_EQUALS` | differs from the value | one value |
| `GREATER_THAN` | is greater than the value | one value |
| `GREATER_OR_EQUAL` | is greater than or equal to the value | one value |
| `LESS_THAN` | is less than the value | one value |
| `LESS_OR_EQUAL` | is less than or equal to the value | one value |
| `IN` | is one of the values | a collection of values |
| `CONTAINS` | contains the text | text, textual Field only |
| `STARTS_WITH` | starts with the text | text, textual Field only |
| `ENDS_WITH` | ends with the text | text, textual Field only |
| `IS_NULL` | is null | none |
| `IS_NOT_NULL` | is not null | none |

A comparison never selects a null value; only the two null checks do. Text operators are case-sensitive. Ordering operators (`GREATER_THAN` to `LESS_OR_EQUAL`) need an integer, float, decimal, text or datetime Field. Decimal Fields are compared exactly.

### Filter

An immutable condition: `Filter(field, operator, value)`. `field` is a Field reference, which is the Entity's class attribute such as `User.is_active`, never a name string. `operator` is a `FilterOperator` member. `value` must have exactly the Field's Type (a `Decimal` for a decimal Field, an offset-aware `datetime` for a datetime Field, no integer for a float Field) and is omitted for the two null checks.

```python
from database.interface import Filter, FilterOperator
from model.interface import Currency, User

active = Filter(User.is_active, FilterOperator.EQUALS, True)
major = Filter(Currency.code, FilterOperator.IN, ["USD", "EUR"])
no_description = Filter(User.description, FilterOperator.IS_NULL)
```

### FilterCombination

An enumeration with `AND` and `OR`. It says how several Filters combine. The default is `AND`.

```python
from database.interface import Database, Filter, FilterCombination, FilterOperator
from model.interface import Currency

db = Database()
either = db.list(
    Currency,
    filters=[
        Filter(Currency.code, FilterOperator.EQUALS, "USD"),
        Filter(Currency.code, FilterOperator.EQUALS, "JPY"),
    ],
    combination=FilterCombination.OR,
)
print([item.code for item in either])
```

### Order and OrderDirection

`Order(field, direction)` is an immutable ordering. `OrderDirection` has `ASCENDING` and `DESCENDING`; an `Order` without a direction is ascending. Only `list` accepts Orders. Supplied Orders replace the default order (the Entity's `id`, ascending) and apply in the sequence given; ties are always broken by ascending `id`.

```python
from database.interface import Database, Order, OrderDirection
from model.interface import Currency

db = Database()
by_digits = db.list(
    Currency,
    orders=[Order(Currency.decimal_digits, OrderDirection.DESCENDING), Order(Currency.code)],
)
print([(item.code, item.decimal_digits) for item in by_digits][:3])
```

### CommandResult

The immutable result of `execute_command`, with the fields `rows`, `affected`, `columns`, `success`, `message` and `instance`. For a query, `rows` is a tuple of read-only mappings, `columns` the ordered column names and `affected` is `None`. For a change, `affected` is the affected row count and `rows` and `columns` are `None`. `instance` is the `DatabaseInstance` that ran it.

### LifecycleResult

The immutable result of a Lifecycle Command, with the fields `command`, `instance`, `success`, `affected` and `message`. `affected` is the number of Tables created or records inserted.

### Errors

Every failure is one of these, all derived from `DatabaseError`, and none exposes a credential.

| Error | Meaning |
| --- | --- |
| `ConfigurationError` | The configuration or an Instance is invalid or unknown. |
| `InactiveInstanceError` | The selected Instance is not active. |
| `InvalidInputError` | An Entity, Field, id, Filter, Order or value is not valid for the call; raised before any storage is touched. |
| `DeclarationMismatchError` | An existing Table, or a stored row, does not match its Entity. |
| `ConnectionFailureError` | The Instance could not be reached. |
| `ExecutionError` | The storage rejected a request, for example a broken uniqueness or Relation rule. |
| `LifecycleError` | A Lifecycle Command stopped part way and left an incomplete state. |

```python
from database.interface import Database, DatabaseError, InvalidInputError
from model.interface import User

db = Database()
try:
    db.get_by_id(User, "1")
except InvalidInputError as error:
    print("rejected:", error)
except DatabaseError:
    raise
```

### Entity Operations

An Entity is passed as the Model class (`User`) or, for `add` and `update`, as an Entity instance. Every Operation runs in one transaction: it completes fully or changes nothing, and separate calls share no transaction.

#### add(entity, instance)

Stores one complete new Entity instance, whose `id` is still pending, and returns the stored Entity including the values storage generated.

```python
from database.interface import Database
from model.interface import Broker

db = Database()
stored = db.add(Broker(name="Add Example", user_id=1))
print(stored.id)
```

#### update(entity, instance)

Replaces every mutable Field of the stored record that the given Entity's `id` identifies, never changing `id`. Returns the stored Entity, or `None` when no record exists.

```python
from database.interface import Database
from model.interface import Broker

db = Database()
stored = db.add(Broker(name="Update Example", user_id=1))
stored.description = "changed"
print(db.update(stored).description)
```

#### list(entity, filters, combination, orders, limit, instance)

Returns the Entities that match `filters` (a sequence of `Filter`, default none), joined by `combination` (default `AND`), ordered by `orders` (default the Entity's `id`, ascending) and capped by `limit`. An omitted limit, zero and any negative limit mean no limit; a positive limit is the maximum count.

```python
from database.interface import Database, Filter, FilterOperator, Order, OrderDirection
from model.interface import Currency

db = Database()
found = db.list(
    Currency,
    filters=[Filter(Currency.country, FilterOperator.STARTS_WITH, "United")],
    orders=[Order(Currency.code, OrderDirection.DESCENDING)],
    limit=5,
)
print([item.code for item in found])
```

#### get_by_id(entity, id, instance)

Returns the Entity with that `id`, or `None` when no record exists.

```python
from database.interface import Database
from model.interface import User

db = Database()
print(db.get_by_id(User, 1).username, db.get_by_id(User, 999))
```

#### delete(entity, id, instance)

Removes the record and returns the final deleted Entity, or `None` when no record exists. A record that other records still reference is refused with `ExecutionError`.

```python
from database.interface import Database
from model.interface import Broker

db = Database()
created = db.add(Broker(name="Delete Example", user_id=1))
print(db.delete(Broker, created.id).name, db.get_by_id(Broker, created.id))
```

#### enable(entity, id, instance) and disable(entity, id, instance)

Set only `is_active` to `True` or `False` and return the final Entity, also when it already had that value, or `None` when no record exists.

```python
from database.interface import Database
from model.interface import Broker

db = Database()
created = db.add(Broker(name="Disable Example", user_id=1))
print(db.disable(Broker, created.id).is_active, db.enable(Broker, created.id).is_active)
```

#### count(entity, filters, combination, instance)

Returns the number of matching records.

```python
from database.interface import Database, Filter, FilterOperator
from model.interface import Currency

db = Database()
print(db.count(Currency, [Filter(Currency.decimal_digits, FilterOperator.EQUALS, 2)]))
```

#### sum(entity, field, filters, combination, instance)

Returns the total of one numeric Field (integer, float or decimal) over the matching records, ignoring nulls, or zero when nothing matches. Decimal totals are exact.

```python
from database.interface import Database
from model.interface import Currency

db = Database()
print(db.sum(Currency, Currency.decimal_digits))
```

#### min(entity, field, filters, combination, instance) and max(entity, field, filters, combination, instance)

Return the smallest or largest value of one comparable Field (integer, float, decimal, text or datetime) over the matching records, ignoring nulls, or `None` when nothing matches.

```python
from database.interface import Database
from model.interface import Asset

db = Database()
print(db.min(Asset, Asset.point_size), db.max(Asset, Asset.point_size))
```

#### truncate(entity, instance)

Removes every record of the Entity, keeps its Table and returns the number removed. It is refused with `ExecutionError` while other records reference the Entity's records.

```python
from decimal import Decimal

from database.interface import Database
from model.interface import TrailingRule

db = Database()
db.add(TrailingRule(name="Truncate Example", trailing_group_id=1, trigger_percentage=Decimal("1")))
print(db.truncate(TrailingRule))
```

### Database-wide Operation

#### execute_command(command, parameters, instance)

Runs a native command of the Instance's Engine, with `parameters` bound as values (a sequence for `?` placeholders or a mapping for `:name` placeholders), and returns a `CommandResult`. Any valid command is allowed, including a schema change, though `create_tables` remains the standard way to prepare Tables. A command the Engine rejects is returned as `success=False` with its message; nothing it started is kept.

```python
from database.interface import Database

db = Database()
result = db.execute_command("select id, name from User where id = ?", [1])
print(result.success, result.columns, result.rows[0]["name"])
```

### Lifecycle Commands

CreateTables, InsertInitialData and Prepare are separate from the Operations and are described in [Lifecycle](#lifecycle).

```python
from database.interface import Database

db = Database()
print(db.prepare().message)
```

## Instances

An Instance is one named database connection and storage identity. The configuration (`config.yaml` in the Component root) defines each Instance and which one is the default; the Interface exposes only the active ones, as `DatabaseInstance` members, and never their connection values.

| Instance | Engine | Active | Default |
| --- | --- | --- | --- |
| `sqlite` (`DatabaseInstance.SQLITE`) | SQLite | yes | yes |
| `postgresql` | PostgreSQL | no | no |

Only the SQLite Instance is active, so only the SQLite Engine has an implementation in this Component. A call without an `instance` runs on the default Instance; a call with a `DatabaseInstance` member runs on that Instance. Passing a string, or anything that is not a `DatabaseInstance` member, raises `InvalidInputError` before storage is touched.

Storage is owned by Database. A file-backed Instance's database file lives under the Component's `db/` directory, created on first use, whatever the consumer's working directory is. A location that would escape that directory is refused before any connection. For this the Component must be installed as a path (editable) dependency of the consumer, so that it resolves its own directory.

## Setup

Database requires Python 3.14, [uv](https://docs.astral.sh/uv/) and the Model Component next to it (this Component declares `../model` as an editable path dependency). All dependencies are pinned in `pyproject.toml` and `uv.lock`.

1. Open a terminal in the Component root, the directory that holds `pyproject.toml` and `config.yaml`.
2. Create the isolated environment and install the pinned dependencies:

   ```bash
   uv sync
   ```

3. Prepare the default Instance (create its Tables, then insert the Initial Data):

   ```bash
   uv run python -m database.scripts.prepare
   ```

Generation runs this Prepare step automatically: the configuration enables after-generation preparation on the default Instance, and a failure fails the generation.

To use Database from another project, add the Component root as an editable dependency of that project, so that Database finds its own `db/` storage and `config.yaml`:

```bash
uv add --editable ../database
```

The development tools are installed by `uv sync`:

```bash
uv run ruff check database
uv run ruff format --check database
uv run pyright
```

## Use

Use Database only through the Interface, with Field references (`User.is_active`) and enumeration members (`FilterOperator.EQUALS`), never strings. This example uses each capability group once.

Entity Operations:

```python
from database.interface import Database, Filter, FilterOperator, Order, OrderDirection
from model.interface import Asset, Broker

db = Database()

broker = db.add(Broker(name="Use Example", user_id=1))
db.add(Asset(broker_id=broker.id, symbol="USE/ABC", category="Currency", point_size=0.5))

assets = db.list(
    Asset,
    filters=[Filter(Asset.broker_id, FilterOperator.EQUALS, broker.id)],
    orders=[Order(Asset.symbol, OrderDirection.ASCENDING)],
)
print(len(assets), db.count(Asset, [Filter(Asset.is_active, FilterOperator.EQUALS, True)]))
print(db.sum(Asset, Asset.point_size, [Filter(Asset.broker_id, FilterOperator.EQUALS, broker.id)]))
```

A Database-wide Operation:

```python
from database.interface import Database

db = Database()
result = db.execute_command("select count(*) as total from Asset")
print(result.rows[0]["total"])
```

Instance selection:

```python
from database.interface import Database, DatabaseInstance
from model.interface import Asset

db = Database()
print(db.count(Asset), db.count(Asset, instance=DatabaseInstance.SQLITE))
```

Lifecycle Commands (see [Lifecycle](#lifecycle)):

```python
from database.interface import Database

db = Database()
print(db.create_tables().message)
```

Values are never converted: decimal Fields take `decimal.Decimal`, float Fields take `float`, datetime Fields take offset-aware `datetime` values, and every Entity comes back built by its own construction.

## Lifecycle

CreateTables, InsertInitialData and Prepare prepare an Instance's storage. They are separate from the Operations, so an everyday call never changes the schema or seeds data. Each is a method of `Database` that returns a `LifecycleResult`, and each has a manual entry point that only calls it. Run the entry points from the Component root:

| Command | Method | Manual entry point |
| --- | --- | --- |
| CreateTables | `create_tables(instance)` | `uv run python -m database.scripts.create_tables` |
| InsertInitialData | `insert_initial_data(instance)` | `uv run python -m database.scripts.insert_initial_data` |
| Prepare | `prepare(instance)` | `uv run python -m database.scripts.prepare` |

**CreateTables** creates, in dependency order and in one transaction, a Table for every Entity of the Model Entity Collection, with the Fields, Primary Key, Relations and Uniqueness Constraints its Declaration states. It reads nothing else. Run again on matching Tables it succeeds and changes nothing. If an existing Table differs from its Entity's Declaration, it stops with `DeclarationMismatchError`, names the Entity and the differing aspects, and changes nothing; it never alters a Table by judgment.

**InsertInitialData** inserts every Initial Data record (see [Initial Data](#initial-data)) that is missing, in one transaction. A record that is already present and identical on the Fields the Target supplies is skipped; a record that differs fails with `ExecutionError` naming the Entity, the record and the differing Fields, and the whole run is rolled back. Records are matched by the Entity's uniqueness constraints. The Target's records refer to each other by id (for example `user_id` 1), so they assume an empty database: ids are assigned from 1 and a database that previously held and lost rows does not reuse them.

**Prepare** runs CreateTables and then InsertInitialData on the selected Instance, and does not run InsertInitialData when CreateTables fails.

When a Lifecycle Command fails, its message names the command and the Instance. Generation runs Prepare on the default Instance only; any other active Instance is prepared only when you pass it explicitly.

```python
from database.interface import Database

db = Database()
print(db.prepare().message)
```

## Initial Data

Database inserts these records, defined by the Target, unchanged and without any omission based on security, sensitivity or at-rest instructions. A value that the Target leaves to be generated securely is stored as an empty string: Database never produces a value itself, so fill such values after preparation. Values are listed in the form stored in `config.yaml`; decimal values are written as exact strings.


### User

| `name` | `username` | `password` | `api_key` |
| --- | --- | --- | --- |
| Admin | admin | (empty) | (empty) |

### Trading Platform

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

### Account Group

| `user_id` | `name` |
| --- | --- |
| 1 | Default |

### Account

| `name` | `group_id` | `broker_id` | `instance_id` | `base_currency_id` | `username` | `password` | `leverage` | `account_type` |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Acc-1 | 1 | 1 | 1 | 1 | test | (empty) | 100 | CFD |

### Trailing Group

| `user_id` | `name` |
| --- | --- |
| 1 | Default |

### Partial Group

| `user_id` | `name` |
| --- | --- |
| 1 | Default |

### Action Group

| `user_id` | `name` |
| --- | --- |
| 1 | Default |

### Action

| `name` | `action_group_id` | `asset_id` | `account_id` | `partial_group_id` | `trailing_group_id` | `risk_by_reward` | `take_profit` | `stop_loss` |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Default | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |

## Verify

Run this from the Component root on a prepared database (`uv run python -m database.scripts.prepare`). Every assertion states one observation; the script ends silently when all of them hold, and it removes what it creates, so it can be repeated.

```python
import subprocess
import sys
from pathlib import Path

import database.interface as interface
from database.interface import (
    Database, DatabaseInstance, Filter, FilterCombination, FilterOperator, InvalidInputError, Order, OrderDirection,
)
from model.interface import Broker, Currency, TrailingRule, User, entities
from decimal import Decimal

# Public import: exactly the published contracts.
published = {name for name in vars(interface) if not name.startswith("_")}
assert published == {
    "Database", "DatabaseInstance", "Filter", "FilterOperator", "FilterCombination", "Order", "OrderDirection",
    "CommandResult", "LifecycleResult", "DatabaseError", "ConfigurationError", "InactiveInstanceError",
    "InvalidInputError", "DeclarationMismatchError", "ConnectionFailureError", "ExecutionError", "LifecycleError",
}

# Query vocabulary: closed member sets whose values equal their names.
assert [m.name for m in FilterOperator] == [
    "EQUALS", "NOT_EQUALS", "GREATER_THAN", "GREATER_OR_EQUAL", "LESS_THAN", "LESS_OR_EQUAL", "IN", "CONTAINS",
    "STARTS_WITH", "ENDS_WITH", "IS_NULL", "IS_NOT_NULL",
]
assert [m.name for m in FilterCombination] == ["AND", "OR"]
assert [m.name for m in OrderDirection] == ["ASCENDING", "DESCENDING"]
assert all(m.value == m.name for enum in (FilterOperator, FilterCombination, OrderDirection, DatabaseInstance) for m in enum)

# Instance selection: one member per active Instance; no selection means the default; strings are refused.
db = Database()
assert [m.name for m in DatabaseInstance] == ["SQLITE"]
assert db.count(User) == db.count(User, instance=DatabaseInstance.SQLITE)
for refused in (lambda: db.count(User, instance="sqlite"), lambda: db.list("User"), lambda: db.get_by_id(User, "1")):
    try:
        refused()
    except InvalidInputError:
        pass
    else:
        raise AssertionError("a string must be refused")

# Entity Operations: add, get, update, list, count, disable, enable, delete.
broker = db.add(Broker(name="Verify Example", user_id=1))
assert broker.id is not None and db.get_by_id(Broker, broker.id).name == "Verify Example"
broker.description = "verified"
assert db.update(broker).description == "verified"
found = db.list(Broker, [Filter(Broker.name, FilterOperator.STARTS_WITH, "Verify")], orders=[Order(Broker.id, OrderDirection.DESCENDING)], limit=1)
assert [item.id for item in found] == [broker.id]
assert db.count(Broker, [Filter(Broker.name, FilterOperator.EQUALS, "Verify Example")]) == 1
assert db.disable(Broker, broker.id).is_active is False and db.enable(Broker, broker.id).is_active is True
assert db.delete(Broker, broker.id).id == broker.id and db.get_by_id(Broker, broker.id) is None

# Aggregates and truncation, with exact decimals.
db.add(TrailingRule(name="Verify A", trailing_group_id=1, trigger_percentage=Decimal("0.1")))
db.add(TrailingRule(name="Verify B", trailing_group_id=1, trigger_percentage=Decimal("0.2")))
assert db.sum(TrailingRule, TrailingRule.trigger_percentage) == Decimal("0.3")
assert db.min(TrailingRule, TrailingRule.trigger_percentage) == Decimal("0.1")
assert db.max(Currency, Currency.decimal_digits) == 2 and db.sum(Currency, Currency.decimal_digits) == 14
assert db.truncate(TrailingRule) == 2

# Database-wide Operation.
result = db.execute_command("select count(*) as total from User")
assert result.success and result.rows[0]["total"] == db.count(User)

# Persistent file location, and persistence across processes.
assert Path("db/application.db").is_file()
check = "from database.interface import Database; from model.interface import User; print(Database().count(User))"
assert subprocess.run([sys.executable, "-c", check], capture_output=True, text=True).stdout.strip() == str(db.count(User))

# Repeatable Lifecycle Commands: a second run creates and inserts nothing.
total = sum(db.count(entity) for entity in entities)
again = db.prepare()
assert again.success and again.affected == 0 and sum(db.count(entity) for entity in entities) == total
```

## Troubleshooting

- **`InvalidInputError`.** The call was refused before any storage was touched. Give Entities as imported Model classes (or instances for `add` and `update`), Fields as Field references of that same Entity (`User.name`), operators, combinations and directions as enumeration members, ids as integers, and values of exactly the Field's Type.
- **An inactive Instance.** Only active Instances are `DatabaseInstance` members, so an inactive one cannot be selected. To use another Instance, set its `active` value to `true` in `config.yaml`, give it the connection values its Engine requires, and generate Database again so that the Engine implementation it needs is provided. Until then the call fails with `ConfigurationError` stating that the implementation has not been generated.
- **`ConfigurationError` when importing.** `config.yaml` is invalid, unreadable, or Database is not installed as an editable dependency so it cannot find its own configuration. The message names the fault, never a value. Fix `config.yaml`, or install with `uv add --editable`.
- **A Table that differs from its Entity.** CreateTables, and therefore Prepare, stops with `DeclarationMismatchError` naming the Entity and the differing aspects (`columns`, `unique`, `foreign_keys`, `indexes`) and changes nothing. Database never alters a Table by judgment and owns no data migration: bring the Table in line with the Entity, or move the old storage aside and prepare a new one.
- **Empty Initial Data values.** Values the Target leaves to be generated securely (the passwords and API keys of the User, the Instance and the Account) are stored as empty strings. Database never creates them: set them yourself after preparation, for example with `update`.
- **`ExecutionError` when inserting Initial Data.** A message about a foreign key means the database is not empty in the way the Target assumes: its records refer to each other by id starting at 1, and rows that were once stored and removed do not free their ids. Use a fresh database. A message about a conflicting record names the Entity, the record and the differing Fields: the stored record differs from the Target's; Database never overwrites it.
- **`ExecutionError` on other calls.** The storage refused the request, for example a repeated unique value or a record that is still referenced by another. The message names the broken rule, and the call changed nothing.
- **`ConnectionFailureError`.** The Instance could not be reached or its storage location could not be prepared. For the file-backed Instance, check that the Component's `db/` directory is writable and is not a file.
- **`DeclarationMismatchError` on a read.** A stored row does not satisfy its Entity contract (for example a null in a required Field). Database never repairs a row; correct the stored data.
- **`LifecycleError`.** A Lifecycle Command stopped part way and left an incomplete schema. The message states how many Tables were created; with SQLite schema work is rolled back, so this appears only for an Engine that cannot do that.
