# Storage Service

## Overview

Storage is Logic's complete gateway to Database. For every capability that Database publishes it offers one Action
with the same name, parameters, defaults, and documentation, hands each request to Database through one Database access
that the gateway holds, and returns Database's answer and errors unchanged. It adds no validation, retry, selection of
an Engine or Instance, or rule of its own, so that every other Logic Service reaches persistence one way and Database's
internals stay hidden.

```python
from logic.services.storage.interface import Storage
from model.interface import User

storage = Storage()
print([user.name for user in storage.list(User)])  # ['Admin']
```

## Interface

The Storage Service Interface publishes the gateway `Storage` and 16 republished Database contracts, each the
same object that the Database Interface publishes, never a copy. Nothing else is published, and loading the Interface opens
no connection and creates no data or file.

### Actions

| Action | Parameters | What it does |
|---|---|---|
| `add` | `entity, instance=None` | Store one complete new Entity instance and return the stored Entity. |
| `update` | `entity, instance=None` | Replace every mutable Field of the stored record; null when no record exists. |
| `list` | `entity, filters=None, combination=None, orders=None, limit=None, instance=None` | Return the Entities that match; a zero or negative limit means no limit. |
| `get_by_id` | `entity, id, instance=None` | Return the Entity with the given id, or null. |
| `delete` | `entity, id, instance=None` | Remove the record and return the final deleted Entity, or null. |
| `enable` | `entity, id, instance=None` | Set only the activity Field to true and return the final Entity, or null. |
| `disable` | `entity, id, instance=None` | Set only the activity Field to false and return the final Entity, or null. |
| `count` | `entity, filters=None, combination=None, instance=None` | Return the number of matching records. |
| `sum` | `entity, field, filters=None, combination=None, instance=None` | Return the total of a numeric Field, ignoring nulls, or zero. |
| `min` | `entity, field, filters=None, combination=None, instance=None` | Return the smallest value of a comparable Field, ignoring nulls, or null. |
| `max` | `entity, field, filters=None, combination=None, instance=None` | Return the largest value of a comparable Field, ignoring nulls, or null. |
| `truncate` | `entity, instance=None` | Remove every record of the Entity, keep its Table, and return the deleted count. |
| `execute_command` | `command, parameters=None, instance=None` | Run a native command in the Instance Engine's query language. |
| `create_tables` | `instance=None` | Create every Table from the Model Entities; stop on a difference with an existing one. |
| `insert_initial_data` | `instance=None` | Insert every missing configured Initial Data record; skip identical present ones. |
| `prepare` | `instance=None` | Run create_tables and then insert_initial_data; stop if create_tables fails. |

Every Action takes the optional `instance` last and runs on the default Instance when it is omitted.

### Republished contracts

| Contract | What it is | Example |
|---|---|---|
| `ConfigurationError` | The configuration or a selected Instance is invalid. | `except ConfigurationError:` |
| `ConnectionFailureError` | The Instance could not be reached. | `except ConnectionFailureError:` |
| `DatabaseError` | The base of every Database failure. | `except DatabaseError:` |
| `DeclarationMismatchError` | Storage and an Entity's Declaration are incompatible. | `except DeclarationMismatchError:` |
| `ExecutionError` | A request failed or violates a constraint. | `except ExecutionError:` |
| `InactiveInstanceError` | An inactive Instance was selected. | `except InactiveInstanceError:` |
| `InvalidInputError` | An input, Entity, or Field is invalid. | `except InvalidInputError:` |
| `LifecycleError` | A Lifecycle Command left an incomplete state. | `except LifecycleError:` |
| `CommandResult` | The outcome of `execute_command`. | `result = storage.execute_command('select 1 as one'); result.success` |
| `DatabaseInstance` | The active configured Instances; it carries no connection values. | `DatabaseInstance.SQLITE` |
| `Filter` | An immutable condition: a Field reference, an operator, and a value. | `Filter(User.is_active, FilterOperator.EQUALS, True)` |
| `FilterCombination` | How Filters combine: `AND` or `OR`. | `FilterCombination.OR` |
| `FilterOperator` | The comparison operators of a Filter. | `FilterOperator.CONTAINS` |
| `LifecycleResult` | The outcome of a Lifecycle Command. | `storage.prepare().success` |
| `Order` | An immutable ordering: a Field reference and a direction. | `Order(User.name, OrderDirection.DESCENDING)` |
| `OrderDirection` | `ASCENDING` or `DESCENDING`. | `OrderDirection.ASCENDING` |

### Examples

Every Action, run in order against a prepared Database:

```python
from logic.services.storage.interface import (
    DatabaseInstance,
    Filter,
    FilterOperator,
    InvalidInputError,
    Order,
    OrderDirection,
    Storage,
)
from model.interface import Asset, Broker, Currency, Position, User

storage = Storage()

broker = storage.add(Broker(name="Storage broker", user_id=1))  # add
broker.description = "updated"
broker = storage.update(broker)  # update
print(broker.description)  # updated
usd = storage.list(  # list
    Currency,
    filters=[Filter(Currency.code, FilterOperator.EQUALS, "USD")],
    orders=[Order(Currency.code, OrderDirection.DESCENDING)],
    limit=1,
    instance=DatabaseInstance.SQLITE,
)
print(usd[0].symbol)  # $
print(storage.get_by_id(User, 1).name)  # get_by_id: Admin
print(storage.disable(Currency, 1).is_active)  # disable: False
print(storage.enable(Currency, 1).is_active)  # enable: True
print(storage.count(Currency))  # count: 8
print(storage.sum(Asset, Asset.digits))  # sum: 15
print(
    storage.min(Asset, Asset.point_size), storage.max(Asset, Asset.point_size)
)  # min, max: 0.0001 0.01
print(storage.delete(Broker, broker.id).name)  # delete: Storage broker
print(storage.truncate(Position))  # truncate: 0
result = storage.execute_command('select count(*) as n from "Currency"')  # execute_command
print(result.success, result.rows[0]["n"])  # True 8
print(storage.create_tables().success)  # create_tables: True
print(storage.insert_initial_data().success)  # insert_initial_data: True
print(storage.prepare().success)  # prepare: True
try:
    storage.list("Currency")
except InvalidInputError:
    print("refused")  # the Database's own error, unchanged
```

## Use

Another Logic Service imports from the Storage Service Interface and from nowhere else:

```python
from logic.services.storage.interface import Storage, Filter, FilterOperator
```

Only the Storage Service imports the Database Interface; every other Service reaches Database through Storage, and no
Service imports the Logic Interface. Create one gateway where it is needed: creating it creates one Database access, and
every Action uses that access.

## Verify

This script checks that Storage matches the Database Interface exactly. It prints `all checks passed` when every check holds.

```python
import inspect

import database.interface as database
import logic.services.storage.interface as storage_interface

capabilities = [
    (name, member)
    for name, member in vars(database.Database).items()
    if not name.startswith("_") and callable(member)
]
actions = [
    (name, member)
    for name, member in vars(storage_interface.Storage).items()
    if not name.startswith("_") and callable(member)
]
assert [name for name, _ in actions] == [name for name, _ in capabilities]
for (name, action), (_, capability) in zip(actions, capabilities):
    expected, found = inspect.signature(capability).parameters, inspect.signature(action).parameters
    assert list(found) == list(expected), name
    assert all(found[key].default == expected[key].default for key in found), name
    assert inspect.getdoc(action) == inspect.getdoc(capability), name

contracts = [name for name in vars(database) if not name.startswith("_") and name != "Database"]
published = {name for name in vars(storage_interface) if not name.startswith("_")}
assert published == {"Storage", *contracts}
assert all(getattr(storage_interface, name) is getattr(database, name) for name in contracts)

print("all checks passed")
```
