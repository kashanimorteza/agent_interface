# Storage Service

## Overview

Storage Service is Logic's one gateway to Database. For every capability the Database Interface publishes it offers
one Action with the same name, parameters, and result, and it hands each request to Database without adding
validation, retry, Instance selection, or any rule of its own. Other Logic Services use Database only through it,
and Storage republishes the Database contracts they need, so none of them imports Database.

```python
from logic.services.storage.interface import Storage
from model.interface import Asset, Broker, Currency, Position, User

storage = Storage()
storage.prepare()  # creates the Tables and the Initial Data once; repeating it changes nothing
print(storage.get_by_id(User, 1).name)  # Admin
```

## Interface

`logic.services.storage.interface` publishes exactly the gateway and the Database contracts below, and nothing
else. Every Action is a method of the gateway. Entities and Field references are passed as the imported values
Model publishes, never as text, and every Action takes an optional `DatabaseInstance` as its last parameter.

| Name | What it is |
|---|---|
| `Storage` | The gateway. Creating it takes one access to Database, which every Action uses. |
| `DatabaseInstance` | The enumeration of the active configured Instances. |
| `Filter`, `FilterOperator`, `FilterCombination` | A condition, its comparison operators, and how conditions combine. |
| `Order`, `OrderDirection` | An ordering and its directions. |
| `CommandResult`, `LifecycleResult` | The results of a Database-wide Operation and of a Lifecycle Command. |
| `DatabaseError` and seven failure-kind errors | Every error Database raises. |

### Entity Operations

A missing record returns `None`, never an error.

**`add(entity, instance=None)`** stores one complete new Entity instance and returns the stored Entity, including
its generated `id`.

```python
broker = storage.add(Broker(name="Scratch broker", user_id=1))
print(broker.name)  # Scratch broker
```

**`update(entity, instance=None)`** replaces every mutable Field of the stored record that the Entity's `id`
locates and returns the stored Entity, or `None`.

```python
broker.description = "Backup broker"
print(storage.update(broker).description)  # Backup broker
```

**`list(entity, filters=None, combination=None, orders=None, limit=None, instance=None)`** returns the matching
Entities; a zero or negative limit means no limit.

```python
from logic.services.storage.interface import Filter, FilterOperator, Order, OrderDirection

rows = storage.list(
    Currency,
    filters=[Filter(Currency.decimal_digits, FilterOperator.EQUALS, 2)],
    orders=[Order(Currency.code, OrderDirection.DESCENDING)],
    limit=3,
)
print([currency.code for currency in rows])  # ['USD', 'NZD', 'GBP']
```

**`get_by_id(entity, id, instance=None)`** returns the Entity with that `id`, or `None`.

```python
print(storage.get_by_id(User, 999))  # None
```

**`delete(entity, id, instance=None)`** removes the record and returns the final deleted Entity, or `None`.

```python
print(storage.delete(Broker, broker.id).name)  # Scratch broker
```

**`enable(entity, id, instance=None)`** and **`disable(entity, id, instance=None)`** set only `is_active` and
return the final Entity, also when it already had that value, or `None`.

```python
print(storage.disable(Currency, 1).is_active)  # False
print(storage.enable(Currency, 1).is_active)  # True
```

**`count(entity, filters=None, combination=None, instance=None)`** returns the number of matching records.

```python
from logic.services.storage.interface import FilterCombination

usd_or_eur = Filter(Currency.code, FilterOperator.IN, ["USD", "EUR"])
print(storage.count(Currency, [usd_or_eur], FilterCombination.AND))  # 2
```

**`sum(entity, field, filters=None, combination=None, instance=None)`** returns the total of a numeric Field,
ignoring nulls, or zero. **`min(...)`** and **`max(...)`** take the same parameters for a comparable Field and
return the smallest or largest value, ignoring nulls, or `None`.

```python
print(storage.sum(Asset, Asset.digits))  # 15
print(storage.min(Currency, Currency.code), storage.max(Currency, Currency.code))  # AUD USD
```

**`truncate(entity, instance=None)`** removes every record of the Entity, keeps its Table, and returns the deleted
count. It affects no other Entity.

```python
print(storage.truncate(Position))  # 0
```

### Database-wide Operation

**`execute_command(command, parameters=None, instance=None)`** runs a native command in the Instance's query
language with bound parameters and returns a `CommandResult`.

```python
result = storage.execute_command('select code, symbol from "Currency" where code = ?', ["EUR"])
print(result.success, result.columns, result.rows[0]["symbol"])  # True ('code', 'symbol') €
```

### Lifecycle Commands

**`create_tables(instance=None)`** creates every Table from the Model Entities and stops on a difference with an
existing one. **`insert_initial_data(instance=None)`** inserts every missing configured Initial Data record and
skips identical present ones. **`prepare(instance=None)`** runs the first and then the second and stops when the
first fails. Each returns a `LifecycleResult`.

```python
print(storage.create_tables().success, storage.insert_initial_data().success)  # True True
print(storage.prepare().command)  # prepare
```

### Contracts

Every contract is the identical object the Database Interface publishes, never a copy, so a value built from one
is accepted by the Database and an error raised by the Database is caught by the matching one.

| Contract | Example |
|---|---|
| `DatabaseInstance` | `DatabaseInstance.SQLITE` selects the active Instance explicitly. |
| `Filter` | `Filter(Currency.code, FilterOperator.EQUALS, "USD")` |
| `FilterOperator` | `FilterOperator.STARTS_WITH` |
| `FilterCombination` | `FilterCombination.OR` |
| `Order` | `Order(Currency.code, OrderDirection.ASCENDING)` |
| `OrderDirection` | `OrderDirection.DESCENDING` |
| `CommandResult` | `storage.execute_command(...)` returns one with `rows`, `affected`, `columns`, `success`, `message`, `instance`. |
| `LifecycleResult` | `storage.prepare()` returns one with `command`, `instance`, `success`, `affected`, `message`. |
| `DatabaseError` | `except DatabaseError:` catches every error below. |
| `ConfigurationError` | `except ConfigurationError:` when the configuration or a selected Instance is invalid. |
| `InactiveInstanceError` | `except InactiveInstanceError:` when an inactive Instance is selected. |
| `InvalidInputError` | `except InvalidInputError:` when an input, Entity, or Field is invalid. |
| `DeclarationMismatchError` | `except DeclarationMismatchError:` when a stored row or Table differs from its Declaration. |
| `ConnectionFailureError` | `except ConnectionFailureError:` when the Instance cannot be reached. |
| `ExecutionError` | `except ExecutionError:` when a request fails or violates a constraint. |
| `LifecycleError` | `except LifecycleError:` when a Lifecycle Command leaves an incomplete state. |

```python
from logic.services.storage.interface import DatabaseError, DatabaseInstance, InvalidInputError

print([member.name for member in DatabaseInstance])  # ['SQLITE']
try:
    storage.list("Currency")
except InvalidInputError as error:
    print(isinstance(error, DatabaseError))  # True
```

## Use

Another Logic Service imports from the Storage Service Interface only, never from Database:

```python
from logic.services.storage.interface import Filter, FilterOperator, Storage
from model.interface import Currency


class Currencies:
    def __init__(self) -> None:
        self._storage = Storage()

    def with_code(self, code: str) -> list[Currency]:
        return self._storage.list(Currency, [Filter(Currency.code, FilterOperator.EQUALS, code)])


print([currency.symbol for currency in Currencies().with_code("EUR")])  # ['€']
```

A Service owns any Behaviour it adds around a Storage call; Storage itself adds none.

## Verify

Run this script from the Logic directory with `uv run python`. It checks that the gateway has exactly one Action for
every Database capability in Database's order, with the same signature and documentation, that every contract is
the identical object the Database Interface publishes, that nothing else is published, and that importing the
Interface and creating the gateway open no connection and start no process. It prints `all checks passed` when
every check holds.

```python
import inspect
import subprocess
import sys

import database.interface as database
import logic.services.storage.interface as storage

capabilities = [
    name
    for name, value in vars(database.Database).items()
    if not name.startswith("_") and callable(value)
]
actions = [
    name
    for name, value in vars(storage.Storage).items()
    if not name.startswith("_") and callable(value)
]
assert actions == capabilities

for name in actions:
    assert inspect.signature(getattr(storage.Storage, name)) == inspect.signature(
        getattr(database.Database, name)
    )
    assert inspect.getdoc(getattr(storage.Storage, name)) == inspect.getdoc(
        getattr(database.Database, name)
    )

contracts = [name for name in vars(database) if not name.startswith("_") and name != "Database"]
assert sorted(storage.__all__) == sorted([*contracts, "Storage"])
assert all(getattr(storage, name) is getattr(database, name) for name in contracts)
assert sorted(name for name in vars(storage) if not name.startswith("_")) == sorted(storage.__all__)

probe = """
import sys
events = []
sys.addaudithook(lambda event, args: events.append(event) if event in ("socket.connect", "subprocess.Popen", "sqlite3.connect") else None)
from logic.services.storage.interface import Storage
Storage()
sys.exit(1 if events else 0)
"""
assert subprocess.run([sys.executable, "-c", probe], check=False).returncode == 0

print("all checks passed")
```
