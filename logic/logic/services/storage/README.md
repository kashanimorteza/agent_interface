# Storage Service

## Overview

Storage Service is Logic's gateway to Database. Every other Logic Service reaches persistence through it, so no Service has to know how Database is reached, and Database internals stay hidden. The gateway offers one Action for every Entity Operation and the Command Operation of Database's Interface group, with the same name, parameters and defaults; each Action hands its request to Database and returns Database's answer and errors unchanged. Storage adds no validation, retry or rule of its own.

This example needs a prepared database (see the Database README). It adds one User through Storage and counts the Users.

```python
from model import User

from logic.services.storage.interface import Storage

storage = Storage()
user = storage.add(
    User(name="Ada", username="ada", password="example-password", api_key="example-key")
)
print(user.id, storage.count(User))
```

## Interface

The Storage Interface publishes exactly five names and nothing else:

| Name | What it is |
|---|---|
| `Storage` | the gateway class, created with no argument; it holds one `database_interface` and every Action uses it |
| `database_value` | Database's Value group, republished as the identical object |
| `database_instance` | Database's Instance group, republished as the identical object |
| `database_result` | Database's Result group, republished as the identical object |
| `database_error` | Database's Error group, republished as the identical object |

### Actions

`Storage` has one Action for every Operation of Database's Interface group, in Database's order. Each Action keeps the Operation's name, parameter names, order, defaults and documentation (Database's README explains each Operation). Database's Setup Operations are not part of Storage.

| Action | Parameters |
|---|---|
| `add` | `entity`, `instance` |
| `update` | `entity`, `instance` |
| `list` | `entity`, `filters`, `combination`, `orders`, `limit`, `instance` |
| `get_by_id` | `entity`, `id`, `instance` |
| `delete` | `entity`, `id`, `instance` |
| `enable` | `entity`, `id`, `instance` |
| `disable` | `entity`, `id`, `instance` |
| `count` | `entity`, `filters`, `combination`, `instance` |
| `sum` | `entity`, `field`, `filters`, `combination`, `instance` |
| `min` | `entity`, `field`, `filters`, `combination`, `instance` |
| `max` | `entity`, `field`, `filters`, `combination`, `instance` |
| `truncate` | `entity`, `instance` |
| `execute_command` | `command`, `parameters`, `instance` |

One example for each Action:

```python
from model import Account, Broker, PartialRule, User

from logic.services.storage.interface import Storage, database_value

storage = Storage()
alan = storage.add(User(name="Alan", username="alan", password="x", api_key="y"))  # add
alan.description = "Analyst"
alan = storage.update(alan)  # update: replaces the mutable Fields
print(storage.get_by_id(User, alan.id).description)  # get_by_id
print(storage.disable(User, alan.id).is_active)  # disable
print(storage.enable(User, alan.id).is_active)  # enable
active = [
    database_value.Filter(User.is_active, database_value.FilterOperator.EQUALS, True)
]
print([user.name for user in storage.list(User, filters=active, limit=5)])  # list
print(storage.count(User, active))  # count
print(storage.sum(Account, Account.leverage))  # sum
print(storage.min(User, User.name), storage.max(User, User.name))  # min and max
broker = storage.add(Broker(name="Example", user_id=alan.id))
print(storage.delete(Broker, broker.id).name)  # delete
print(storage.truncate(PartialRule))  # truncate
result = storage.execute_command(
    "SELECT COUNT(*) AS total FROM User"
)  # execute_command
print(result.rows[0]["total"])
```

### Republished contracts

The four groups are the identical objects Database's Interface publishes, so a Service never imports Database to build a request, read a result or catch an error. Each group's members are explained in the Database README; one example each:

```python
from model import User

from logic.services.storage.interface import (
    Storage,
    database_error,
    database_instance,
    database_result,
    database_value,
)

storage = Storage()
admin_only = [
    database_value.Filter(User.name, database_value.FilterOperator.EQUALS, "Admin")
]
print(
    storage.count(User, admin_only, instance=database_instance.SQLITE)
)  # Value and Instance groups
print(
    isinstance(storage.execute_command("SELECT 1"), database_result.CommandResult)
)  # Result group
try:
    storage.get_by_id("User", 1)  # a string where an Entity class is required
except database_error.InvalidInputError as error:  # Error group
    print("refused:", error)
```

## Use

Another Logic Service imports Storage from the Storage Interface, creates one gateway, and calls its Actions. It never imports Database.

```python
from model import Currency

from logic.services.storage.interface import Storage, database_error, database_value


class CurrencyCodes:
    """A tiny Service that adds Behaviour around a Storage call."""

    def __init__(self) -> None:
        self._storage = Storage()

    def codes(self) -> list[str]:
        ordered = [database_value.Order(Currency.code)]
        return [
            currency.code for currency in self._storage.list(Currency, orders=ordered)
        ]


try:
    print(CurrencyCodes().codes())
except database_error.DatabaseError as error:
    print("storage failed:", error)
```

## Verify

Run this from the `logic` directory. It checks that Storage has one Action for every Operation of Database's Interface group, in Database's order and with the same parameters, and that it republishes Database's four groups unchanged. It prints `verified` when everything holds.

```python
import inspect

import database

from logic.services.storage import interface as storage

operations = [
    name
    for name, member in vars(database.database_interface).items()
    if not name.startswith("_") and callable(member)
]
actions = [
    name
    for name, member in vars(storage.Storage).items()
    if not name.startswith("_") and callable(member)
]
assert actions == operations
for name in operations:
    mirrored = inspect.signature(getattr(storage.Storage, name))
    original = inspect.signature(getattr(database.database_interface, name))
    assert [(p.name, p.default) for p in mirrored.parameters.values()] == [
        (p.name, p.default) for p in original.parameters.values()
    ]
for group in (
    "database_value",
    "database_instance",
    "database_result",
    "database_error",
):
    assert getattr(storage, group) is getattr(database, group)
assert sorted(storage.__all__) == sorted(
    [
        "Storage",
        "database_value",
        "database_instance",
        "database_result",
        "database_error",
    ]
)
print("verified")
```
