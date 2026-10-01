# Storage Service

## Overview

Storage is Logic's internal gateway to Database. Its one class, `Storage`, takes one Database access when it is created and offers one method for every capability Database Interface publishes, with exactly the same name and parameters. Each method hands the request to Database unchanged and returns Database's answer unchanged; Storage adds no behaviour of its own. Every other Logic Service reaches Database only through it.

```python
from logic.services.storage.interface import Storage
from model.interface import User

storage = Storage()
print(storage.count(User))
```

## Interface

`logic.services.storage.interface` publishes exactly `Storage` and the Database contracts below, and nothing else.

### Storage

Every method takes the same parameters, in the same order and with the same defaults, as the Database capability it mirrors, and returns its result or raises its error unchanged. `instance` is always optional and last; without it Database uses its default Instance.

| Method | Parameters |
|---|---|
| `add` | `entity, instance` |
| `update` | `entity, instance` |
| `delete` | `entity, id, instance` |
| `enable` | `entity, id, instance` |
| `disable` | `entity, id, instance` |
| `truncate` | `entity, instance` |
| `list` | `entity, filters, combination, orders, limit, instance` |
| `get_by_id` | `entity, id, instance` |
| `count` | `entity, filters, combination, instance` |
| `sum` | `entity, field, filters, combination, instance` |
| `min` | `entity, field, filters, combination, instance` |
| `max` | `entity, field, filters, combination, instance` |
| `execute_command` | `command, parameters, instance` |
| `create_tables` | `instance` |
| `insert_initial_data` | `instance` |
| `prepare` | `instance` |

```python
from logic.services.storage.interface import (
    DatabaseInstance,
    Filter,
    FilterOperator,
    Order,
    OrderDirection,
    Storage,
)
from model.interface import User

storage = Storage()
storage.prepare()  # create Tables, then insert Initial Data
user = storage.get_by_id(User, 1)
active = storage.list(
    User,
    filters=[Filter(User.is_active, FilterOperator.EQUALS, True)],
    orders=[Order(User.id, OrderDirection.DESCENDING)],
    limit=10,
    instance=DatabaseInstance.SQLITE,
)
```

### Republished contracts

Every supporting contract Database Interface publishes is republished as the same object, never a copy: `DatabaseInstance`, `Filter`, `FilterOperator`, `FilterCombination`, `Order`, `OrderDirection`, `CommandResult`, `LifecycleResult`, and every error — `DatabaseError` and `ConfigurationError`, `InactiveInstanceError`, `InvalidInputError`, `DeclarationMismatchError`, `ConnectionFailureError`, `ExecutionError`, `LifecycleError`.

```python
from logic.services.storage.interface import ConnectionFailureError, Storage

try:
    Storage().prepare()
except ConnectionFailureError as error:
    print("Database is unreachable:", error)
```

## Use

A Logic Service imports from the Storage Interface directly and never from Database Interface or `logic.interface`:

```python
from logic.services.storage.interface import Storage

storage = Storage()
```

Storage is not published through `logic.interface` unless its publication setting is enabled.

## Verify

```python
import database.interface as database
import logic.services.storage.interface as storage

# one method per Database capability, with the same name, in the same order
capabilities = [
    n
    for n, m in vars(database.Database).items()
    if not n.startswith("_") and callable(m)
]
methods = [
    n for n, m in vars(storage.Storage).items() if not n.startswith("_") and callable(m)
]
assert methods == capabilities
# every republished contract is Database's own object
contracts = [name for name in storage.__all__ if name != "Storage"]
assert all(getattr(storage, name) is getattr(database, name) for name in contracts)
print("Storage matches Database Interface")
```
