# Storage Service

## Overview

Storage Service is Logic's gateway to Database. For every capability Database publishes it offers one Action with the same name and the same parameters, hands the request to Database, and returns Database's answer or error unchanged. It adds no validation, retry, or selection of its own, so every other Logic Service reaches persistence through this one route and Database's internals stay hidden.

```python
from logic.services.storage.interface import Storage
from model import Currency

storage = Storage()
print(storage.count(Currency))
```

## Interface

The Storage Service Interface publishes the `Storage` gateway and the Database contracts a Service needs to build a request, read a result, and catch an error without reaching Database. Each contract is the identical object Database publishes. Nothing else is published, and importing the Interface opens no connection and creates no data or file.

Every Action accepts an optional `DatabaseInstance` as its last parameter. When none is given, Database runs the call on its configured default Instance. A missing record is a `None` result, never an error.

### Actions

Actions appear in the order Database publishes them. Each example assumes `storage = Storage()` and Entities imported from the Model.

#### `add(entity, instance=None)`

Store one complete new Entity and return the stored Entity, including generated values.

```python
from logic.services.storage.interface import Storage
from model import Currency

storage = Storage()
stored = storage.add(
    Currency(user_id=1, code="SEK", symbol="kr", country="Sweden", decimal_digits=2)
)
print(stored.id)
```

#### `update(entity, instance=None)`

Replace every mutable Field of the record the Entity's id locates; `None` when there is none.

```python
from logic.services.storage.interface import Storage
from model import Currency

storage = Storage()
currency = storage.get_by_id(Currency, 1)
currency.description = "Reserve currency"
print(storage.update(currency).description)
```

#### `list(entity, filters=None, combination=None, orders=None, limit=None, instance=None)`

The matching Entities, ordered and limited; a limit of zero or below means no limit.

```python
from logic.services.storage.interface import (
    Filter,
    FilterOperator,
    Order,
    OrderDirection,
    Storage,
)
from model import Currency

storage = Storage()
active = storage.list(
    Currency,
    filters=[Filter(Currency.is_active, FilterOperator.EQUALS, True)],
    orders=[Order(Currency.code, OrderDirection.ASCENDING)],
    limit=3,
)
print([currency.code for currency in active])
```

#### `get_by_id(entity, id, instance=None)`

The Entity with the given id, or `None` when there is none.

```python
from logic.services.storage.interface import Storage
from model import Currency

storage = Storage()
print(storage.get_by_id(Currency, 1).code, storage.get_by_id(Currency, 9999))
```

#### `delete(entity, id, instance=None)`

Remove the record with the given id and return it as it was; `None` when there is none.

```python
from logic.services.storage.interface import Storage
from model import Currency

storage = Storage()
removed = storage.delete(Currency, 8)
print(removed.code)
```

#### `enable(entity, id, instance=None)`

Set only the activity flag to active; the final Entity, or `None` when there is none.

```python
from logic.services.storage.interface import Storage
from model import Currency

storage = Storage()
print(storage.enable(Currency, 2).is_active)
```

#### `disable(entity, id, instance=None)`

Set only the activity flag to inactive; the final Entity, or `None` when there is none.

```python
from logic.services.storage.interface import Storage
from model import Currency

storage = Storage()
print(storage.disable(Currency, 2).is_active)
```

#### `count(entity, filters=None, combination=None, instance=None)`

The number of matching records.

```python
from logic.services.storage.interface import Filter, FilterOperator, Storage
from model import Currency

storage = Storage()
print(
    storage.count(
        Currency, filters=[Filter(Currency.decimal_digits, FilterOperator.EQUALS, 2)]
    )
)
```

#### `sum(entity, field, filters=None, combination=None, instance=None)`

The total of one numeric Field, ignoring nulls; zero when nothing matches.

```python
from logic.services.storage.interface import Storage
from model import Currency

storage = Storage()
print(storage.sum(Currency, Currency.decimal_digits))
```

#### `min(entity, field, filters=None, combination=None, instance=None)`

The smallest value of one comparable Field, ignoring nulls; `None` when nothing matches.

```python
from logic.services.storage.interface import Storage
from model import Currency

storage = Storage()
print(storage.min(Currency, Currency.decimal_digits))
```

#### `max(entity, field, filters=None, combination=None, instance=None)`

The largest value of one comparable Field, ignoring nulls; `None` when nothing matches.

```python
from logic.services.storage.interface import Storage
from model import Currency

storage = Storage()
print(storage.max(Currency, Currency.decimal_digits))
```

#### `truncate(entity, instance=None)`

Remove every record of the Entity, keep its Table, and return the number removed.

```python
from logic.services.storage.interface import Storage
from model import Position

storage = Storage()
print(storage.truncate(Position))
```

#### `execute_command(command, parameters=None, instance=None)`

Run one native command in the Instance Engine's query language with bound parameters.

```python
from logic.services.storage.interface import Storage

storage = Storage()
result = storage.execute_command("select count(*) as total from currency")
print(result.success, result.rows)
```

#### `create_tables(instance=None)`

Create every Table of the Model's Entities; matching Tables are left unchanged.

```python
from logic.services.storage.interface import Storage

storage = Storage()
print(storage.create_tables().success)
```

#### `insert_initial_data(instance=None)`

Insert every configured Initial Data record that is not already stored.

```python
from logic.services.storage.interface import Storage

storage = Storage()
print(storage.insert_initial_data().success)
```

#### `prepare(instance=None)`

Run `create_tables` and then `insert_initial_data`; stop when `create_tables` fails.

```python
from logic.services.storage.interface import Storage

storage = Storage()
print(storage.prepare().success)
```

### Contracts

These are republished from Database unchanged. Each example imports the contract from the Storage Service Interface.

#### `DatabaseInstance`

The enumeration of the active configured Instances; it carries no connection values.

```python
from logic.services.storage.interface import DatabaseInstance, Storage
from model import Currency

print(Storage().count(Currency, instance=DatabaseInstance.SQLITE))
```

#### `Filter`

An immutable condition value naming a Field of the Entity, an operator, and a value.

```python
from logic.services.storage.interface import Filter, FilterOperator
from model import Currency

condition = Filter(Currency.code, FilterOperator.EQUALS, "USD")
print(condition.operator)
```

#### `FilterOperator`

The comparison operators a Filter may use: `EQUALS`, `NOT_EQUALS`, `GREATER_THAN`, `GREATER_OR_EQUAL`, `LESS_THAN`, `LESS_OR_EQUAL`, `IN`, `CONTAINS`, `STARTS_WITH`, `ENDS_WITH`, `IS_NULL`, and `IS_NOT_NULL`.

```python
from logic.services.storage.interface import FilterOperator

print([operator.name for operator in FilterOperator][:3])
```

#### `FilterCombination`

The ways Filters combine: `AND` and `OR`.

```python
from logic.services.storage.interface import (
    Filter,
    FilterCombination,
    FilterOperator,
    Storage,
)
from model import Currency

either = [
    Filter(Currency.code, FilterOperator.EQUALS, "USD"),
    Filter(Currency.code, FilterOperator.EQUALS, "EUR"),
]
print(Storage().count(Currency, either, FilterCombination.OR))
```

#### `Order`

An immutable ordering value naming a Field and a direction; the direction is `ASCENDING` when omitted.

```python
from logic.services.storage.interface import Order
from model import Currency

print(Order(Currency.code).direction)
```

#### `OrderDirection`

The ordering directions: `ASCENDING` and `DESCENDING`.

```python
from logic.services.storage.interface import OrderDirection

print([direction.name for direction in OrderDirection])
```

#### `CommandResult`

The result of a Database-wide Operation: returned rows, affected count, columns, success, message, and the Instance used.

```python
from logic.services.storage.interface import CommandResult, Storage

result = Storage().execute_command("select 1 as one")
print(isinstance(result, CommandResult), result.columns)
```

#### `LifecycleResult`

The result of a Lifecycle Command: the command name, the Instance used, success, the processed count, and a message.

```python
from logic.services.storage.interface import LifecycleResult, Storage

result = Storage().create_tables()
print(isinstance(result, LifecycleResult), result.command)
```

#### `DatabaseError`

The base of every Database error; catching it catches every failure kind below.

```python
from logic.services.storage.interface import DatabaseError, Storage

try:
    Storage().prepare()
except DatabaseError as error:
    print(type(error).__name__)
```

#### `ConfigurationError`

The configuration or the selected Instance is invalid.

```python
from logic.services.storage.interface import ConfigurationError, Storage

try:
    Storage().prepare()
except ConfigurationError:
    print("check the Database configuration")
```

#### `InactiveInstanceError`

An inactive Instance was selected.

```python
from logic.services.storage.interface import InactiveInstanceError, Storage

try:
    Storage().prepare()
except InactiveInstanceError:
    print("select an active Instance")
```

#### `InvalidInputError`

A request carried invalid input or an invalid Field.

```python
from logic.services.storage.interface import InvalidInputError, Storage
from model import Currency

try:
    Storage().count(Currency, instance="sqlite")
except InvalidInputError as error:
    print(error)
```

#### `DeclarationMismatchError`

An Entity Declaration and an existing Table or stored row are incompatible.

```python
from logic.services.storage.interface import DeclarationMismatchError, Storage

try:
    Storage().create_tables()
except DeclarationMismatchError:
    print("a stored Table differs from its Entity")
```

#### `ConnectionFailureError`

A connection to the selected Instance could not be established.

```python
from logic.services.storage.interface import ConnectionFailureError, Storage

try:
    Storage().prepare()
except ConnectionFailureError:
    print("the Instance is unreachable")
```

#### `ExecutionError`

The Engine failed to execute a request.

```python
from logic.services.storage.interface import ExecutionError, Storage

try:
    Storage().execute_command("select * from no_such_table")
except ExecutionError as error:
    print(error)
```

#### `LifecycleError`

A Lifecycle Command ended in an incomplete state.

```python
from logic.services.storage.interface import LifecycleError, Storage

try:
    Storage().prepare()
except LifecycleError:
    print("preparation was incomplete")
```

## Use

Another Logic Service imports what it needs from the Storage Service Interface, never from Database and never from the Logic Interface, creates one `Storage`, and keeps it for every call:

```python
from logic.services.storage.interface import InvalidInputError, Storage
from model import Currency


class Reporter:
    def __init__(self) -> None:
        self._storage = Storage()

    def currency_count(self) -> int:
        try:
            return self._storage.count(Currency)
        except InvalidInputError:
            return 0


print(Reporter().currency_count())
```

Storage is a raw gateway. Anything beyond forwarding, such as validation, retries, or choosing an Instance, belongs to the Service that calls it. Leave the Instance out to use Database's default, or pass a `DatabaseInstance` member as the last argument.

## Verify

Storage matches Database when it has exactly one Action for every capability Database publishes, in the same order, with the same parameters and documentation, and when every republished contract is the identical object Database publishes. This script prints `True` for each observation:

```python
import inspect

import database.interface as database_interface
from logic.services.storage import interface as storage_interface
from logic.services.storage.core import Storage

Database = database_interface.Database
database_actions = [
    name
    for name, value in vars(Database).items()
    if not name.startswith("_") and callable(value)
]
storage_actions = [
    name
    for name, value in vars(Storage).items()
    if not name.startswith("_") and callable(value)
]
print(storage_actions == database_actions)

same_shape = all(
    list(inspect.signature(getattr(Storage, name)).parameters)
    == list(inspect.signature(getattr(Database, name)).parameters)
    and getattr(Storage, name).__doc__ == getattr(Database, name).__doc__
    for name in database_actions
)
print(same_shape)

contracts = [name for name in database_interface.__all__ if name != "Database"]
print(sorted(storage_interface.__all__) == sorted([*contracts, "Storage"]))
print(
    all(
        getattr(storage_interface, name) is getattr(database_interface, name)
        for name in contracts
    )
)
```

Loading the Interface opens no connection and creates no data or file; the Database storage is the same before and after `import`.
