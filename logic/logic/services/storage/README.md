# Storage Service

Storage Service is Logic's gateway to Database. It offers one Action for every capability Database publishes, passes each request to that capability through one Database access and returns its answer and errors unchanged, and republishes the Database contracts a caller needs, so that no other Logic Service has to import Database. It adds no validation, retry or rule of its own.

```python
from logic.services.storage.interface import Storage
from model.interface import User

storage = Storage()
print(storage.count(User))
```

## Interface

`logic.services.storage.interface` publishes exactly two kinds of names: the gateway `Storage`, and the contracts of Database's Interface republished as the identical objects (every Database contract except the `Database` object itself). Nothing else is published.

### Actions

`Storage` has one Action for every capability of Database, named and shaped exactly like it, in Database's order. Creating a `Storage` creates one Database access that every Action uses.

| Action | What it does | Signature |
| --- | --- | --- |
| `add` | Stores one complete new Entity instance and returns the stored Entity. | `add(entity: Any, instance: enum.Enum | None = None) -> Any` |
| `update` | Replaces every mutable Field of the stored record the Entity's id identifies. | `update(entity: Any, instance: enum.Enum | None = None) -> Any` |
| `list` | Returns the Entities that match Filters, ordered and limited. | `list(entity: Any, filters: collections.abc.Sequence[database.core.data.Filter] | None = None, combination: database.core.data.FilterCombination | None = None, orders: collections.abc.Sequence[database.core.data.Order] | None = None, limit: int | None = None, instance: enum.Enum | None = None) -> collections.abc.Sequence[typing.Any]` |
| `get_by_id` | Returns the Entity with that id, or None. | `get_by_id(entity: Any, id: int, instance: enum.Enum | None = None) -> Any` |
| `delete` | Removes the record and returns the deleted Entity, or None. | `delete(entity: Any, id: int, instance: enum.Enum | None = None) -> Any` |
| `enable` | Sets is_active to True and returns the Entity, or None. | `enable(entity: Any, id: int, instance: enum.Enum | None = None) -> Any` |
| `disable` | Sets is_active to False and returns the Entity, or None. | `disable(entity: Any, id: int, instance: enum.Enum | None = None) -> Any` |
| `count` | Counts the matching records. | `count(entity: Any, filters: collections.abc.Sequence[database.core.data.Filter] | None = None, combination: database.core.data.FilterCombination | None = None, instance: enum.Enum | None = None) -> int` |
| `sum` | Totals a numeric Field over the matching records. | `sum(entity: Any, field: Any, filters: collections.abc.Sequence[database.core.data.Filter] | None = None, combination: database.core.data.FilterCombination | None = None, instance: enum.Enum | None = None) -> Any` |
| `min` | Smallest value of a comparable Field over the matching records, or None. | `min(entity: Any, field: Any, filters: collections.abc.Sequence[database.core.data.Filter] | None = None, combination: database.core.data.FilterCombination | None = None, instance: enum.Enum | None = None) -> Any` |
| `max` | Largest value of a comparable Field over the matching records, or None. | `max(entity: Any, field: Any, filters: collections.abc.Sequence[database.core.data.Filter] | None = None, combination: database.core.data.FilterCombination | None = None, instance: enum.Enum | None = None) -> Any` |
| `truncate` | Removes every record of an Entity and returns the removed count. | `truncate(entity: Any, instance: enum.Enum | None = None) -> int` |
| `execute_command` | Runs a native command with bound parameters and returns a CommandResult. | `execute_command(command: str, parameters: collections.abc.Mapping[str, Any] | collections.abc.Sequence[Any] | None = None, instance: enum.Enum | None = None) -> database.core.data.CommandResult` |
| `create_tables` | Creates the Tables of the Model Entities and returns a LifecycleResult. | `create_tables(instance: enum.Enum | None = None) -> database.core.data.LifecycleResult` |
| `insert_initial_data` | Inserts the configured Initial Data and returns a LifecycleResult. | `insert_initial_data(instance: enum.Enum | None = None) -> database.core.data.LifecycleResult` |
| `prepare` | Runs create_tables, then insert_initial_data. | `prepare(instance: enum.Enum | None = None) -> database.core.data.LifecycleResult` |

One example for each Action, using one gateway and the data Database prepared:

#### add

```python
from decimal import Decimal

from logic.services.storage.interface import Filter, FilterOperator, Order, OrderDirection, Storage
from model.interface import Broker, Currency, TrailingRule, User

storage = Storage()
stored = storage.add(Broker(name="Storage Add", user_id=1))
```

#### update

```python
from decimal import Decimal

from logic.services.storage.interface import Filter, FilterOperator, Order, OrderDirection, Storage
from model.interface import Broker, Currency, TrailingRule, User

storage = Storage()
stored = storage.add(Broker(name="Storage Update", user_id=1))
stored.description = "changed"
storage.update(stored)
```

#### list

```python
from decimal import Decimal

from logic.services.storage.interface import Filter, FilterOperator, Order, OrderDirection, Storage
from model.interface import Broker, Currency, TrailingRule, User

storage = Storage()
storage.list(
    Currency,
    filters=[Filter(Currency.code, FilterOperator.IN, ["USD", "EUR"])],
    orders=[Order(Currency.code, OrderDirection.DESCENDING)],
    limit=5,
)
```

#### get_by_id

```python
from decimal import Decimal

from logic.services.storage.interface import Filter, FilterOperator, Order, OrderDirection, Storage
from model.interface import Broker, Currency, TrailingRule, User

storage = Storage()
storage.get_by_id(User, 1)
```

#### delete

```python
from decimal import Decimal

from logic.services.storage.interface import Filter, FilterOperator, Order, OrderDirection, Storage
from model.interface import Broker, Currency, TrailingRule, User

storage = Storage()
storage.delete(Broker, storage.add(Broker(name="Storage Delete", user_id=1)).id)
```

#### enable

```python
from decimal import Decimal

from logic.services.storage.interface import Filter, FilterOperator, Order, OrderDirection, Storage
from model.interface import Broker, Currency, TrailingRule, User

storage = Storage()
storage.enable(Broker, storage.add(Broker(name="Storage Enable", user_id=1)).id)
```

#### disable

```python
from decimal import Decimal

from logic.services.storage.interface import Filter, FilterOperator, Order, OrderDirection, Storage
from model.interface import Broker, Currency, TrailingRule, User

storage = Storage()
storage.disable(Broker, storage.add(Broker(name="Storage Disable", user_id=1)).id)
```

#### count

```python
from decimal import Decimal

from logic.services.storage.interface import Filter, FilterOperator, Order, OrderDirection, Storage
from model.interface import Broker, Currency, TrailingRule, User

storage = Storage()
storage.count(Currency)
```

#### sum

```python
from decimal import Decimal

from logic.services.storage.interface import Filter, FilterOperator, Order, OrderDirection, Storage
from model.interface import Broker, Currency, TrailingRule, User

storage = Storage()
storage.sum(Currency, Currency.decimal_digits)
```

#### min

```python
from decimal import Decimal

from logic.services.storage.interface import Filter, FilterOperator, Order, OrderDirection, Storage
from model.interface import Broker, Currency, TrailingRule, User

storage = Storage()
storage.min(Currency, Currency.code)
```

#### max

```python
from decimal import Decimal

from logic.services.storage.interface import Filter, FilterOperator, Order, OrderDirection, Storage
from model.interface import Broker, Currency, TrailingRule, User

storage = Storage()
storage.max(Currency, Currency.code)
```

#### truncate

```python
from decimal import Decimal

from logic.services.storage.interface import Filter, FilterOperator, Order, OrderDirection, Storage
from model.interface import Broker, Currency, TrailingRule, User

storage = Storage()
storage.add(TrailingRule(name="Storage Truncate", trailing_group_id=1, trigger_percentage=Decimal("1")))
storage.truncate(TrailingRule)
```

#### execute_command

```python
from decimal import Decimal

from logic.services.storage.interface import Filter, FilterOperator, Order, OrderDirection, Storage
from model.interface import Broker, Currency, TrailingRule, User

storage = Storage()
storage.execute_command("select count(*) as total from User")
```

#### create_tables

```python
from decimal import Decimal

from logic.services.storage.interface import Filter, FilterOperator, Order, OrderDirection, Storage
from model.interface import Broker, Currency, TrailingRule, User

storage = Storage()
storage.create_tables()
```

#### insert_initial_data

```python
from decimal import Decimal

from logic.services.storage.interface import Filter, FilterOperator, Order, OrderDirection, Storage
from model.interface import Broker, Currency, TrailingRule, User

storage = Storage()
storage.insert_initial_data()
```

#### prepare

```python
from decimal import Decimal

from logic.services.storage.interface import Filter, FilterOperator, Order, OrderDirection, Storage
from model.interface import Broker, Currency, TrailingRule, User

storage = Storage()
storage.prepare()
```

### Republished contracts

Each is the same object `database.interface` publishes; import it from here instead of from Database.

#### CommandResult

The result of execute_command.

```python
from logic.services.storage.interface import (
    CommandResult,
    ConfigurationError,
    ConnectionFailureError,
    DatabaseError,
    DatabaseInstance,
    DeclarationMismatchError,
    ExecutionError,
    Filter,
    FilterCombination,
    FilterOperator,
    InactiveInstanceError,
    InvalidInputError,
    LifecycleError,
    LifecycleResult,
    Order,
    OrderDirection,
    Storage,
)
from model.interface import Broker, Currency, User

storage = Storage()
result = storage.execute_command("select 1 as one")
print(type(result) is CommandResult, result.rows[0]["one"])
```

#### ConfigurationError

The configuration or an Instance is invalid.

```python
from logic.services.storage.interface import (
    CommandResult,
    ConfigurationError,
    ConnectionFailureError,
    DatabaseError,
    DatabaseInstance,
    DeclarationMismatchError,
    ExecutionError,
    Filter,
    FilterCombination,
    FilterOperator,
    InactiveInstanceError,
    InvalidInputError,
    LifecycleError,
    LifecycleResult,
    Order,
    OrderDirection,
    Storage,
)
from model.interface import Broker, Currency, User

storage = Storage()
ConfigurationError.__mro__[1] is DatabaseError
```

#### ConnectionFailureError

The Instance could not be reached.

```python
from logic.services.storage.interface import (
    CommandResult,
    ConfigurationError,
    ConnectionFailureError,
    DatabaseError,
    DatabaseInstance,
    DeclarationMismatchError,
    ExecutionError,
    Filter,
    FilterCombination,
    FilterOperator,
    InactiveInstanceError,
    InvalidInputError,
    LifecycleError,
    LifecycleResult,
    Order,
    OrderDirection,
    Storage,
)
from model.interface import Broker, Currency, User

storage = Storage()
issubclass(ConnectionFailureError, DatabaseError)
```

#### DatabaseError

The base of every Database failure.

```python
from logic.services.storage.interface import (
    CommandResult,
    ConfigurationError,
    ConnectionFailureError,
    DatabaseError,
    DatabaseInstance,
    DeclarationMismatchError,
    ExecutionError,
    Filter,
    FilterCombination,
    FilterOperator,
    InactiveInstanceError,
    InvalidInputError,
    LifecycleError,
    LifecycleResult,
    Order,
    OrderDirection,
    Storage,
)
from model.interface import Broker, Currency, User

storage = Storage()
try:
    storage.get_by_id(User, "1")
except DatabaseError as error:
    print(type(error).__name__)
```

#### DatabaseInstance

The enumeration of the active Instances.

```python
from logic.services.storage.interface import (
    CommandResult,
    ConfigurationError,
    ConnectionFailureError,
    DatabaseError,
    DatabaseInstance,
    DeclarationMismatchError,
    ExecutionError,
    Filter,
    FilterCombination,
    FilterOperator,
    InactiveInstanceError,
    InvalidInputError,
    LifecycleError,
    LifecycleResult,
    Order,
    OrderDirection,
    Storage,
)
from model.interface import Broker, Currency, User

storage = Storage()
storage.count(User, instance=DatabaseInstance.SQLITE)
```

#### DeclarationMismatchError

A Table or a stored row does not match its Entity.

```python
from logic.services.storage.interface import (
    CommandResult,
    ConfigurationError,
    ConnectionFailureError,
    DatabaseError,
    DatabaseInstance,
    DeclarationMismatchError,
    ExecutionError,
    Filter,
    FilterCombination,
    FilterOperator,
    InactiveInstanceError,
    InvalidInputError,
    LifecycleError,
    LifecycleResult,
    Order,
    OrderDirection,
    Storage,
)
from model.interface import Broker, Currency, User

storage = Storage()
issubclass(DeclarationMismatchError, DatabaseError)
```

#### ExecutionError

The storage refused a request.

```python
from logic.services.storage.interface import (
    CommandResult,
    ConfigurationError,
    ConnectionFailureError,
    DatabaseError,
    DatabaseInstance,
    DeclarationMismatchError,
    ExecutionError,
    Filter,
    FilterCombination,
    FilterOperator,
    InactiveInstanceError,
    InvalidInputError,
    LifecycleError,
    LifecycleResult,
    Order,
    OrderDirection,
    Storage,
)
from model.interface import Broker, Currency, User

storage = Storage()
try:
    storage.add(Broker(name="FxPro", user_id=1))
except ExecutionError:
    print("refused")
```

#### Filter

An immutable condition.

```python
from logic.services.storage.interface import (
    CommandResult,
    ConfigurationError,
    ConnectionFailureError,
    DatabaseError,
    DatabaseInstance,
    DeclarationMismatchError,
    ExecutionError,
    Filter,
    FilterCombination,
    FilterOperator,
    InactiveInstanceError,
    InvalidInputError,
    LifecycleError,
    LifecycleResult,
    Order,
    OrderDirection,
    Storage,
)
from model.interface import Broker, Currency, User

storage = Storage()
Filter(User.is_active, FilterOperator.EQUALS, True)
```

#### FilterCombination

How Filters combine: AND or OR.

```python
from logic.services.storage.interface import (
    CommandResult,
    ConfigurationError,
    ConnectionFailureError,
    DatabaseError,
    DatabaseInstance,
    DeclarationMismatchError,
    ExecutionError,
    Filter,
    FilterCombination,
    FilterOperator,
    InactiveInstanceError,
    InvalidInputError,
    LifecycleError,
    LifecycleResult,
    Order,
    OrderDirection,
    Storage,
)
from model.interface import Broker, Currency, User

storage = Storage()
storage.count(
    Currency,
    [Filter(Currency.code, FilterOperator.EQUALS, "USD"), Filter(Currency.code, FilterOperator.EQUALS, "EUR")],
    FilterCombination.OR,
)
```

#### FilterOperator

The twelve comparison operators.

```python
from logic.services.storage.interface import (
    CommandResult,
    ConfigurationError,
    ConnectionFailureError,
    DatabaseError,
    DatabaseInstance,
    DeclarationMismatchError,
    ExecutionError,
    Filter,
    FilterCombination,
    FilterOperator,
    InactiveInstanceError,
    InvalidInputError,
    LifecycleError,
    LifecycleResult,
    Order,
    OrderDirection,
    Storage,
)
from model.interface import Broker, Currency, User

storage = Storage()
[member.name for member in FilterOperator]
```

#### InactiveInstanceError

The selected Instance is not active.

```python
from logic.services.storage.interface import (
    CommandResult,
    ConfigurationError,
    ConnectionFailureError,
    DatabaseError,
    DatabaseInstance,
    DeclarationMismatchError,
    ExecutionError,
    Filter,
    FilterCombination,
    FilterOperator,
    InactiveInstanceError,
    InvalidInputError,
    LifecycleError,
    LifecycleResult,
    Order,
    OrderDirection,
    Storage,
)
from model.interface import Broker, Currency, User

storage = Storage()
issubclass(InactiveInstanceError, DatabaseError)
```

#### InvalidInputError

A call was refused as invalid before storage was touched.

```python
from logic.services.storage.interface import (
    CommandResult,
    ConfigurationError,
    ConnectionFailureError,
    DatabaseError,
    DatabaseInstance,
    DeclarationMismatchError,
    ExecutionError,
    Filter,
    FilterCombination,
    FilterOperator,
    InactiveInstanceError,
    InvalidInputError,
    LifecycleError,
    LifecycleResult,
    Order,
    OrderDirection,
    Storage,
)
from model.interface import Broker, Currency, User

storage = Storage()
try:
    storage.list("User")
except InvalidInputError as error:
    print("refused")
```

#### LifecycleError

A Lifecycle Command stopped part way.

```python
from logic.services.storage.interface import (
    CommandResult,
    ConfigurationError,
    ConnectionFailureError,
    DatabaseError,
    DatabaseInstance,
    DeclarationMismatchError,
    ExecutionError,
    Filter,
    FilterCombination,
    FilterOperator,
    InactiveInstanceError,
    InvalidInputError,
    LifecycleError,
    LifecycleResult,
    Order,
    OrderDirection,
    Storage,
)
from model.interface import Broker, Currency, User

storage = Storage()
issubclass(LifecycleError, DatabaseError)
```

#### LifecycleResult

The result of a Lifecycle Command.

```python
from logic.services.storage.interface import (
    CommandResult,
    ConfigurationError,
    ConnectionFailureError,
    DatabaseError,
    DatabaseInstance,
    DeclarationMismatchError,
    ExecutionError,
    Filter,
    FilterCombination,
    FilterOperator,
    InactiveInstanceError,
    InvalidInputError,
    LifecycleError,
    LifecycleResult,
    Order,
    OrderDirection,
    Storage,
)
from model.interface import Broker, Currency, User

storage = Storage()
result = storage.prepare()
print(type(result) is LifecycleResult, result.command)
```

#### Order

An immutable ordering.

```python
from logic.services.storage.interface import (
    CommandResult,
    ConfigurationError,
    ConnectionFailureError,
    DatabaseError,
    DatabaseInstance,
    DeclarationMismatchError,
    ExecutionError,
    Filter,
    FilterCombination,
    FilterOperator,
    InactiveInstanceError,
    InvalidInputError,
    LifecycleError,
    LifecycleResult,
    Order,
    OrderDirection,
    Storage,
)
from model.interface import Broker, Currency, User

storage = Storage()
Order(Currency.code, OrderDirection.DESCENDING)
```

#### OrderDirection

ASCENDING or DESCENDING.

```python
from logic.services.storage.interface import (
    CommandResult,
    ConfigurationError,
    ConnectionFailureError,
    DatabaseError,
    DatabaseInstance,
    DeclarationMismatchError,
    ExecutionError,
    Filter,
    FilterCombination,
    FilterOperator,
    InactiveInstanceError,
    InvalidInputError,
    LifecycleError,
    LifecycleResult,
    Order,
    OrderDirection,
    Storage,
)
from model.interface import Broker, Currency, User

storage = Storage()
[member.name for member in OrderDirection]
```

## Use

Another Logic Service imports from the Storage Service Interface only, never from Database and never from the Storage implementation. Pass Model Entities, Field references and the republished vocabulary as values:

```python
from logic.services.storage.interface import Filter, FilterOperator, Storage
from model.interface import User

storage = Storage()
active = storage.list(User, filters=[Filter(User.is_active, FilterOperator.EQUALS, True)])
print([user.name for user in active])
```

Errors are Database's own, republished: catch `DatabaseError` or one of its kinds.

## Verify

Run this from a prepared environment. It shows that the Storage Interface matches Database's Interface:

```python
import database.interface as database
import logic.services.storage.interface as storage

capabilities = [n for n, m in vars(database.Database).items() if callable(m) and not n.startswith("_")]
actions = [n for n, m in vars(storage.Storage).items() if callable(m) and not n.startswith("_")]
assert actions == capabilities

contracts = [n for n in vars(database) if not n.startswith("_") and n != "Database"]
assert sorted(n for n in storage.__all__ if n != "Storage") == sorted(contracts)
assert all(getattr(storage, n) is getattr(database, n) for n in contracts)
assert "Database" not in vars(storage)
```
