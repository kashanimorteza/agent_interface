# Entity Service

## Overview

Entity Service gives every Entity of the Model one Child Service. A caller selects an Entity once by creating its Child Service and then calls Actions without passing the Entity again; each Child Service adds its bound Entity to the request, hands it to Storage Service, and returns Storage's answer or error unchanged. Every Child Service receives the same shared Base, so each Entity has one place for Behaviour of its own.

```python
from logic.services.entity.interface import User

users = User()
print(users.count())
```

## Interface

The Entity Service Interface publishes one Child Service for every Entity in the Model's Entity Collection and the Storage Service contracts a caller needs, each the identical object Storage Service publishes. Base and the Storage gateway are never published, and importing the Interface opens no connection and creates no data or file.

Import from `logic.services.entity.interface`. Every Child Service is created with no arguments.

### Child Services

One Child Service per Entity, in the Model's Entity Collection order. Each example counts the Entity's records.

#### `User`

The Child Service of the Model's User Entity.

```python
from logic.services.entity.interface import User

print(User().count())
```

#### `TradingPlatform`

The Child Service of the Model's Trading Platform Entity.

```python
from logic.services.entity.interface import TradingPlatform

print(TradingPlatform().count())
```

#### `Instance`

The Child Service of the Model's Instance Entity.

```python
from logic.services.entity.interface import Instance

print(Instance().count())
```

#### `Currency`

The Child Service of the Model's Currency Entity.

```python
from logic.services.entity.interface import Currency

print(Currency().count())
```

#### `Broker`

The Child Service of the Model's Broker Entity.

```python
from logic.services.entity.interface import Broker

print(Broker().count())
```

#### `Asset`

The Child Service of the Model's Asset Entity.

```python
from logic.services.entity.interface import Asset

print(Asset().count())
```

#### `AccountGroup`

The Child Service of the Model's Account Group Entity.

```python
from logic.services.entity.interface import AccountGroup

print(AccountGroup().count())
```

#### `Account`

The Child Service of the Model's Account Entity.

```python
from logic.services.entity.interface import Account

print(Account().count())
```

#### `TrailingGroup`

The Child Service of the Model's Trailing Group Entity.

```python
from logic.services.entity.interface import TrailingGroup

print(TrailingGroup().count())
```

#### `TrailingRule`

The Child Service of the Model's Trailing Rule Entity.

```python
from logic.services.entity.interface import TrailingRule

print(TrailingRule().count())
```

#### `PartialGroup`

The Child Service of the Model's Partial Group Entity.

```python
from logic.services.entity.interface import PartialGroup

print(PartialGroup().count())
```

#### `PartialRule`

The Child Service of the Model's Partial Rule Entity.

```python
from logic.services.entity.interface import PartialRule

print(PartialRule().count())
```

#### `ActionGroup`

The Child Service of the Model's Action Group Entity.

```python
from logic.services.entity.interface import ActionGroup

print(ActionGroup().count())
```

#### `Action`

The Child Service of the Model's Action Entity.

```python
from logic.services.entity.interface import Action

print(Action().count())
```

#### `Position`

The Child Service of the Model's Position Entity.

```python
from logic.services.entity.interface import Position

print(Position().count())
```

### Actions

Every Child Service offers these Actions, in the order Storage Service publishes them. They are the Storage Actions that take an Entity, without the Entity type: the bound Entity is supplied for you, while an Entity instance you pass to `add` or `update` must be of the bound Entity. Every Action accepts an optional `DatabaseInstance` as its last parameter; a missing record is a `None` result, never an error. The examples use the `Currency` Child Service, and `truncate` uses `Position`.

#### `add(entity, instance=None)`

Store one complete new Entity and return the stored Entity, including generated values.

```python
from logic.services.entity.interface import Currency
import model

currencies = Currency()
stored = currencies.add(
    model.Currency(
        user_id=1, code="SEK", symbol="kr", country="Sweden", decimal_digits=2
    )
)
print(stored.id)
```

#### `update(entity, instance=None)`

Replace every mutable Field of the record the Entity's id locates; null when there is none.

```python
from logic.services.entity.interface import Currency

currencies = Currency()
currency = currencies.get_by_id(1)
currency.description = "Reserve currency"
print(currencies.update(currency).description)
```

#### `list(filters=None, combination=None, orders=None, limit=None, instance=None)`

The matching Entities, ordered and limited; a limit of zero or below means no limit.

```python
from logic.services.entity.interface import (
    Currency,
    Filter,
    FilterOperator,
    Order,
    OrderDirection,
)
import model

currencies = Currency()
active = currencies.list(
    filters=[Filter(model.Currency.is_active, FilterOperator.EQUALS, True)],
    orders=[Order(model.Currency.code, OrderDirection.ASCENDING)],
    limit=3,
)
print([currency.code for currency in active])
```

#### `get_by_id(id, instance=None)`

The Entity with the given id, or null when there is none.

```python
from logic.services.entity.interface import Currency

currencies = Currency()
print(currencies.get_by_id(1).code, currencies.get_by_id(9999))
```

#### `delete(id, instance=None)`

Remove the record with the given id and return it as it was; null when there is none.

```python
from logic.services.entity.interface import Currency

print(Currency().delete(8).code)
```

#### `enable(id, instance=None)`

Set only the activity flag to active; the final Entity, or null when there is none.

```python
from logic.services.entity.interface import Currency

print(Currency().enable(2).is_active)
```

#### `disable(id, instance=None)`

Set only the activity flag to inactive; the final Entity, or null when there is none.

```python
from logic.services.entity.interface import Currency

print(Currency().disable(2).is_active)
```

#### `count(filters=None, combination=None, instance=None)`

The number of matching records.

```python
from logic.services.entity.interface import Currency, Filter, FilterOperator
import model

print(
    Currency().count(
        filters=[Filter(model.Currency.decimal_digits, FilterOperator.EQUALS, 2)]
    )
)
```

#### `sum(field, filters=None, combination=None, instance=None)`

The total of one numeric Field, ignoring nulls; zero when nothing matches.

```python
from logic.services.entity.interface import Currency
import model

print(Currency().sum(model.Currency.decimal_digits))
```

#### `min(field, filters=None, combination=None, instance=None)`

The smallest value of one comparable Field, ignoring nulls; null when nothing matches.

```python
from logic.services.entity.interface import Currency
import model

print(Currency().min(model.Currency.decimal_digits))
```

#### `max(field, filters=None, combination=None, instance=None)`

The largest value of one comparable Field, ignoring nulls; null when nothing matches.

```python
from logic.services.entity.interface import Currency
import model

print(Currency().max(model.Currency.decimal_digits))
```

#### `truncate(instance=None)`

Remove every record of the Entity, keep its Table, and return the number removed.

```python
from logic.services.entity.interface import Position

print(Position().truncate())
```

### Contracts

These are republished from Storage Service, which republishes them from Database, unchanged.

#### `CommandResult`

The result of a Database-wide Operation. Entity Service has no Action that returns it, but it is republished for a caller that uses Storage Service directly.

```python
from logic.services.entity.interface import CommandResult

print(CommandResult.__name__)
```

#### `ConfigurationError`

The configuration or the selected Instance is invalid.

```python
from logic.services.entity.interface import ConfigurationError, Currency

try:
    Currency().count()
except ConfigurationError:
    print("check the Database configuration")
```

#### `ConnectionFailureError`

A connection to the selected Instance could not be established.

```python
from logic.services.entity.interface import ConnectionFailureError, Currency

try:
    Currency().count()
except ConnectionFailureError:
    print("the Instance is unreachable")
```

#### `DatabaseError`

The base of every Database error; catching it catches every failure kind below.

```python
from logic.services.entity.interface import Currency, DatabaseError

try:
    Currency().count(instance="sqlite")
except DatabaseError as error:
    print(type(error).__name__)
```

#### `DatabaseInstance`

The enumeration of the active configured Instances; it carries no connection values.

```python
from logic.services.entity.interface import Currency, DatabaseInstance

print(Currency().count(instance=DatabaseInstance.SQLITE))
```

#### `DeclarationMismatchError`

An Entity Declaration and an existing Table or stored row are incompatible.

```python
from logic.services.entity.interface import Currency, DeclarationMismatchError

try:
    Currency().count()
except DeclarationMismatchError:
    print("a stored Table differs from its Entity")
```

#### `ExecutionError`

The Engine failed to execute a request.

```python
from logic.services.entity.interface import Currency, ExecutionError

try:
    Currency().delete(1)
except ExecutionError as error:
    print(error)
```

#### `Filter`

An immutable condition value naming a Field of the Entity, an operator, and a value.

```python
from logic.services.entity.interface import Filter, FilterOperator
import model

condition = Filter(model.Currency.code, FilterOperator.EQUALS, "USD")
print(condition.operator)
```

#### `FilterCombination`

The ways Filters combine: `AND` and `OR`.

```python
from logic.services.entity.interface import (
    Currency,
    Filter,
    FilterCombination,
    FilterOperator,
)
import model

either = [
    Filter(model.Currency.code, FilterOperator.EQUALS, "USD"),
    Filter(model.Currency.code, FilterOperator.EQUALS, "EUR"),
]
print(Currency().count(either, FilterCombination.OR))
```

#### `FilterOperator`

The comparison operators a Filter may use: `EQUALS`, `NOT_EQUALS`, `GREATER_THAN`, `GREATER_OR_EQUAL`, `LESS_THAN`, `LESS_OR_EQUAL`, `IN`, `CONTAINS`, `STARTS_WITH`, `ENDS_WITH`, `IS_NULL`, and `IS_NOT_NULL`.

```python
from logic.services.entity.interface import FilterOperator

print([operator.name for operator in FilterOperator][:3])
```

#### `InactiveInstanceError`

An inactive Instance was selected.

```python
from logic.services.entity.interface import Currency, InactiveInstanceError

try:
    Currency().count()
except InactiveInstanceError:
    print("select an active Instance")
```

#### `InvalidInputError`

A request carried invalid input or an invalid Field. An Action also raises it when given an instance of a different Entity than the Child Service is bound to.

```python
from logic.services.entity.interface import Currency, InvalidInputError
import model

try:
    Currency().add(model.Broker(name="FxPro", user_id=1))
except InvalidInputError as error:
    print(error)
```

#### `LifecycleError`

A Lifecycle Command ended in an incomplete state.

```python
from logic.services.entity.interface import Currency, LifecycleError

try:
    Currency().count()
except LifecycleError:
    print("preparation was incomplete")
```

#### `LifecycleResult`

The result of a Lifecycle Command. Entity Service has no Action that returns it, but it is republished for a caller that uses Storage Service directly.

```python
from logic.services.entity.interface import LifecycleResult

print(LifecycleResult.__name__)
```

#### `Order`

An immutable ordering value naming a Field and a direction; the direction is `ASCENDING` when omitted.

```python
from logic.services.entity.interface import Order
import model

print(Order(model.Currency.code).direction)
```

#### `OrderDirection`

The ordering directions: `ASCENDING` and `DESCENDING`.

```python
from logic.services.entity.interface import OrderDirection

print([direction.name for direction in OrderDirection])
```

## Use

Create the Child Service of the Entity you work with and call its Actions. The Entity is never passed again, and an Entity instance given to `add` or `update` must be of that Entity:

```python
from logic.services.entity.interface import Currency, InvalidInputError
import model

currencies = Currency()
print(currencies.count())

try:
    currencies.add(model.Broker(name="FxPro", user_id=1))
except InvalidInputError as error:
    print(error)
```

A Child Service holds only what is specific to its Entity; everything shared comes from Base. To give one Entity Behaviour of its own, add a method to that Entity's Child Service. It can call the inherited Actions, so it never copies them. The example below adds the method in a subclass only so it can run without changing the library; in the library the method belongs in the Child Service's own unit:

```python
from logic.services.entity.interface import Currency


class CurrencyWithCodes(Currency):
    def first_codes(self) -> list[str]:
        return [currency.code for currency in self.list(limit=3)]


print(CurrencyWithCodes().first_codes())
```

A Child Service may override an inherited Action for its own Entity, but it never detaches from Base and never touches Database: all persistence goes through Storage Service. Entity Service imports Storage Service's Interface only, and no Service imports the Logic Interface.

## Verify

Entity Service matches the Model and Storage when every Entity of the Model's Entity Collection has exactly one Child Service bound to it, Base has exactly one Action for each Storage Action that takes an Entity (in Storage's order, without the Entity type), and every republished contract is the identical object Storage publishes. This script prints `True` for each observation:

```python
import inspect

import model
from logic.services.entity import interface as entity_interface
from logic.services.entity.base import BaseEntity
from logic.services.storage import interface as storage_interface
from logic.services.storage.core import Storage

children = [getattr(entity_interface, entity.__name__) for entity in model.entities]
print(
    [child.__name__ for child in children]
    == [entity.__name__ for entity in model.entities]
)
print(
    all(
        child._entity is entity and issubclass(child, BaseEntity)
        for child, entity in zip(children, model.entities)
    )
)

storage_actions = [
    name
    for name, value in vars(Storage).items()
    if not name.startswith("_")
    and callable(value)
    and list(inspect.signature(value).parameters)[1:2] == ["entity"]
]
base_actions = [
    name
    for name, value in vars(BaseEntity).items()
    if not name.startswith("_") and callable(value)
]
print(base_actions == storage_actions)

contracts = [name for name in storage_interface.__all__ if name != "Storage"]
child_names = [entity.__name__ for entity in model.entities]
print(sorted(entity_interface.__all__) == sorted([*contracts, *child_names]))
print(
    all(
        getattr(entity_interface, name) is getattr(storage_interface, name)
        for name in contracts
    )
)
```

Loading the Interface opens no connection and creates no data or file; the Database storage is the same before and after `import`.
