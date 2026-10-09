# Entity Service

## Overview

Entity Service gives every Model Entity one Child Service, so a caller selects an Entity once and then calls its Actions without passing the Entity again. Database takes the Entity on every request; Entity Service binds it once per Child Service and hands every request to Database unchanged. A caller reaches it through the Logic Interface as `Entity`.

```python
from logic.interface import Entity

currency = Entity.Service.Currency()
stored = currency.add(
    Entity.Model.Currency(user_id=1, code="XAU", symbol="Au", decimal_digits=2)
)
print(stored.id, [item.code for item in currency.list()])
currency.delete(stored.id)
```

## Interface

The Entity Service Interface is the module `logic.services.entity.interface`, reached by a consumer as `Entity` from `logic.interface`. It publishes exactly five groups and nothing else: its own two groups, `Service` and `Model`, and Database's Value, Instance and Error groups, each passed on unchanged under its own name.

| Group | What it is |
| --- | --- |
| `Service` | one Child Service for every Model Entity, under the name of the Entity |
| `Model` | the Entity each Child Service binds, under the same name as its Child Service |
| `database_value` | Database's Filter, Order and their vocabulary, for building requests |
| `database_instance` | Database's active Instances, for selecting where a call runs |
| `database_error` | Database's errors, so a caller can catch them |

The examples below import the five groups from the Logic Interface:

```python
from logic.interface import Entity

print(Entity.__all__)
```

### Service

`Service` holds one Child Service for every Entity in Model's Entity Collection, in the Collection's order. A Child Service is created once with no argument, opens no connection, and offers the twelve Actions below for its own Entity.

| Child Service | Entity it binds |
| --- | --- |
| `Service.User` | `Model.User` |
| `Service.TradingPlatform` | `Model.TradingPlatform` |
| `Service.Instance` | `Model.Instance` |
| `Service.Currency` | `Model.Currency` |
| `Service.Broker` | `Model.Broker` |
| `Service.Asset` | `Model.Asset` |
| `Service.AccountGroup` | `Model.AccountGroup` |
| `Service.Account` | `Model.Account` |
| `Service.TrailingGroup` | `Model.TrailingGroup` |
| `Service.TrailingRule` | `Model.TrailingRule` |
| `Service.PartialGroup` | `Model.PartialGroup` |
| `Service.PartialRule` | `Model.PartialRule` |
| `Service.ActionGroup` | `Model.ActionGroup` |
| `Service.Action` | `Model.Action` |
| `Service.Position` | `Model.Position` |

```python
from logic.interface import Entity

user = Entity.Service.User()
print(user.get_by_id(1).username)
```

Every Child Service is used the same way. This example creates each of the fifteen and counts the records of its Entity:

```python
from logic.interface import Entity

for name in (
    "User",
    "TradingPlatform",
    "Instance",
    "Currency",
    "Broker",
    "Asset",
    "AccountGroup",
    "Account",
    "TrailingGroup",
    "TrailingRule",
    "PartialGroup",
    "PartialRule",
    "ActionGroup",
    "Action",
    "Position",
):
    print(name, getattr(Entity.Service, name)().count())
```

Every Action has the name, the parameters, their order and their defaults of the Database Entity Operation it mirrors, without the Entity class parameter, which the Child Service supplies. The optional `instance` is always last. Every Action passes its arguments to Database unchanged and returns Database's answer and Database's errors unchanged. An Action that takes an Entity instance (`add` and `update`) rejects an instance of any other Entity with `database_error.InvalidInputError` before Database is called. A Field is passed as the Entity's class attribute for it, such as `Model.Currency.code`, and never as a string.

#### `add(entity, instance=None)`

Store one new Entity instance.

- **Accepts:** an instance of the bound Entity whose generated Fields are still pending.
- **Returns:** the stored Entity, including generated values such as `id`.
- **Rejects:** an instance of another Entity, with `InvalidInputError`.

```python
from logic.interface import Entity

currency = Entity.Service.Currency()
stored = currency.add(
    Entity.Model.Currency(user_id=1, code="XAU", symbol="Au", decimal_digits=2)
)
print(stored.id, stored.code)
currency.delete(stored.id)
```

#### `update(entity, instance=None)`

Replace every mutable Field of a stored record. The Entity's `id` only locates the record.

- **Accepts:** an instance of the bound Entity that carries its stored `id`.
- **Returns:** the stored Entity, or `None` when no record has that `id`.
- **Rejects:** an instance of another Entity, with `InvalidInputError`.

```python
from logic.interface import Entity

broker = Entity.Service.Broker()
item = broker.get_by_id(1)
item.description = "Primary broker"
print(broker.update(item).description)
item.description = None
broker.update(item)
```

#### `list(filters=None, combination=None, orders=None, limit=None, instance=None)`

Read the records that match optional Filters, ordered and limited.

- **Accepts:** optional `filters`, `combination`, `orders` and `limit`.
- **Returns:** the matching Entity instances; with no Order they are ordered by `id` ascending, with no `combination` the Filters are combined with `AND`, and with no `limit` (or a zero or negative one) every match is returned.

```python
from logic.interface import Entity

currency = Entity.Service.Currency()
found = currency.list(
    filters=[
        Entity.database_value.Filter(
            Entity.Model.Currency.decimal_digits,
            Entity.database_value.FilterOperator.EQUALS,
            2,
        )
    ],
    orders=[
        Entity.database_value.Order(
            Entity.Model.Currency.code, Entity.database_value.OrderDirection.DESCENDING
        )
    ],
    limit=3,
)
print([item.code for item in found])
```

#### `get_by_id(id, instance=None)`

Read one record by its `id`.

- **Accepts:** an integer `id`.
- **Returns:** the Entity, or `None` when no record exists.

```python
from logic.interface import Entity

user = Entity.Service.User()
print(user.get_by_id(1).username)
print(user.get_by_id(999))
```

#### `delete(id, instance=None)`

Remove one record.

- **Accepts:** an integer `id`.
- **Returns:** the final deleted Entity, or `None` when no record exists.

```python
from logic.interface import Entity

currency = Entity.Service.Currency()
stored = currency.add(
    Entity.Model.Currency(user_id=1, code="XAG", symbol="Ag", decimal_digits=2)
)
print(currency.delete(stored.id).code)
print(currency.delete(stored.id))
```

#### `enable(id, instance=None)`

Set only `is_active` to true.

- **Accepts:** an integer `id`.
- **Returns:** the final Entity, including when it was already enabled, or `None` when no record exists.

```python
from logic.interface import Entity

broker = Entity.Service.Broker()
print(broker.enable(1).is_active)
print(broker.enable(999))
```

#### `disable(id, instance=None)`

Set only `is_active` to false.

- **Accepts:** an integer `id`.
- **Returns:** the final Entity, including when it was already disabled, or `None` when no record exists.

```python
from logic.interface import Entity

broker = Entity.Service.Broker()
print(broker.disable(1).is_active)
broker.enable(1)
```

#### `count(filters=None, combination=None, instance=None)`

Count the matching records.

- **Accepts:** optional `filters` and `combination`.
- **Returns:** the number of matching records.

```python
from logic.interface import Entity

currency = Entity.Service.Currency()
print(currency.count())
print(
    currency.count(
        [
            Entity.database_value.Filter(
                Entity.Model.Currency.code,
                Entity.database_value.FilterOperator.STARTS_WITH,
                "U",
            )
        ]
    )
)
```

#### `sum(field, filters=None, combination=None, instance=None)`

Add up a numeric Field, ignoring null values.

- **Accepts:** one numeric Field of the bound Entity, then optional `filters` and `combination`.
- **Returns:** the total, or zero when nothing matches.

```python
from logic.interface import Entity

currency = Entity.Service.Currency()
print(currency.sum(Entity.Model.Currency.decimal_digits))
```

#### `min(field, filters=None, combination=None, instance=None)`

Find the smallest value of a comparable Field, ignoring null values.

- **Accepts:** one comparable Field of the bound Entity, then optional `filters` and `combination`.
- **Returns:** the smallest value, or `None` when nothing matches.

```python
from logic.interface import Entity

currency = Entity.Service.Currency()
print(currency.min(Entity.Model.Currency.decimal_digits))
```

#### `max(field, filters=None, combination=None, instance=None)`

Find the largest value of a comparable Field, ignoring null values.

- **Accepts:** one comparable Field of the bound Entity, then optional `filters` and `combination`.
- **Returns:** the largest value, or `None` when nothing matches.

```python
from logic.interface import Entity

currency = Entity.Service.Currency()
print(currency.max(Entity.Model.Currency.decimal_digits))
```

#### `truncate(instance=None)`

Remove every record of the bound Entity and keep its table.

- **Accepts:** nothing but the optional `instance`.
- **Returns:** the deleted count.

The example empties the Position table, which holds no record after the standard preparation; run `truncate` on any other Entity only when every record of it should go.

```python
from logic.interface import Entity

print(Entity.Service.Position().truncate())
```

### Model

`Model` holds, under the name of each Child Service, the Entity that Child Service binds, as the original object Model publishes and never a copy. A caller builds requests with it and never imports Model directly.

```python
from logic.interface import Entity

user = Entity.Model.User(
    name="Ada", username="ada", password="placeholder", api_key="placeholder"
)
stored = Entity.Service.User().get_by_id(1)
print(user.username, isinstance(stored, Entity.Model.User))
```

Its members are `Model.User`, `Model.TradingPlatform`, `Model.Instance`, `Model.Currency`, `Model.Broker`, `Model.Asset`, `Model.AccountGroup`, `Model.Account`, `Model.TrailingGroup`, `Model.TrailingRule`, `Model.PartialGroup`, `Model.PartialRule`, `Model.ActionGroup`, `Model.Action` and `Model.Position`, one for each Child Service in the table above.

### database_value

`database_value` is Database's group of the values a caller builds and passes to `list`, `count`, `sum`, `min` and `max`. It is the identical object Database publishes.

#### `Filter(field, operator, value=None)`

One condition: a Field of the Entity, a `FilterOperator` member and a value compatible with the Field. `IS_NULL` and `IS_NOT_NULL` take no value; `IN` takes a non-empty collection.

```python
from logic.interface import Entity

condition = Entity.database_value.Filter(
    Entity.Model.Currency.code, Entity.database_value.FilterOperator.EQUALS, "USD"
)
print([item.id for item in Entity.Service.Currency().list([condition])])
```

#### `FilterOperator`

The twelve comparisons a Filter can make: `EQUALS`, `NOT_EQUALS`, `GREATER_THAN`, `GREATER_OR_EQUAL`, `LESS_THAN`, `LESS_OR_EQUAL`, `IN`, `CONTAINS`, `STARTS_WITH`, `ENDS_WITH`, `IS_NULL` and `IS_NOT_NULL`.

```python
from logic.interface import Entity

print([operator.name for operator in Entity.database_value.FilterOperator])
```

#### `FilterCombination`

How several Filters combine: `AND` (the default) or `OR`.

```python
from logic.interface import Entity

filters = [
    Entity.database_value.Filter(
        Entity.Model.Currency.code, Entity.database_value.FilterOperator.EQUALS, "USD"
    ),
    Entity.database_value.Filter(
        Entity.Model.Currency.code, Entity.database_value.FilterOperator.EQUALS, "EUR"
    ),
]
found = Entity.Service.Currency().list(
    filters, combination=Entity.database_value.FilterCombination.OR
)
print([item.code for item in found])
```

#### `Order(field, direction=OrderDirection.ASCENDING)`

One ordering over any Field of the Entity. Orders are applied in the order supplied and replace the default order (`id` ascending).

```python
from logic.interface import Entity

order = Entity.database_value.Order(Entity.Model.Asset.symbol)
print([item.symbol for item in Entity.Service.Asset().list(orders=[order])])
```

#### `OrderDirection`

The direction of an Order: `ASCENDING` (the default) or `DESCENDING`.

```python
from logic.interface import Entity

order = Entity.database_value.Order(
    Entity.Model.Asset.symbol, Entity.database_value.OrderDirection.DESCENDING
)
print([item.symbol for item in Entity.Service.Asset().list(orders=[order])])
```

### database_instance

`database_instance` is Database's group of the active Instances, the identical object Database publishes. It has one member for every active Instance, named by its key in upper case, and none for an inactive one. With the delivered configuration the only member is `database_instance.SQLITE`. Every Action accepts an optional `instance` as its last parameter; without it the call runs on the default Instance.

```python
from logic.interface import Entity

user = Entity.Service.User()
print(user.get_by_id(1, Entity.database_instance.SQLITE).username)
print(user.get_by_id(1).username)
```

### database_error

`database_error` is Database's group of errors, the identical object Database publishes. Every error derives from `DatabaseError`; each kind is its own error. An Action raises exactly the error Database raises.

#### `DatabaseError`

The base of every Database error; catch it to catch them all.

```python
from logic.interface import Entity

try:
    Entity.Service.Currency().get_by_id("1")
except Entity.database_error.DatabaseError as error:
    print(type(error).__name__)
```

#### `ConfigurationError`

The configuration or the selected Instance is invalid. Raised when Database loads, before any connection is opened.

```python
import importlib

try:
    interface = importlib.import_module("logic.interface")
except Exception as error:
    print(type(error).__name__, error)
else:
    print("configuration valid:", sorted(interface.__all__))
```

#### `InactiveInstanceError`

An Instance that is no longer active was selected.

```python
from logic.interface import Entity

try:
    print(Entity.Service.Currency().count(instance=Entity.database_instance.SQLITE))
except Entity.database_error.InactiveInstanceError:
    print("the selected Instance is no longer active")
```

#### `InvalidInputError`

A request holds invalid input: a string where an imported value is required, a Field of another Entity, or, for an Action that takes an Entity instance, an instance of another Entity.

```python
from logic.interface import Entity

try:
    Entity.Service.Currency().add(Entity.Model.Broker(name="Not a currency", user_id=1))
except Entity.database_error.InvalidInputError as error:
    print(error)
```

#### `DeclarationMismatchError`

An existing table differs from the Declaration of its Entity, or a stored row does not satisfy its Entity's contract.

```python
from logic.interface import Entity

try:
    print(len(Entity.Service.Currency().list()))
except Entity.database_error.DeclarationMismatchError:
    print("the stored data does not match the Entity")
```

#### `ConnectionFailureError`

The connection to the Instance could not be established.

```python
from logic.interface import Entity

try:
    print(Entity.Service.Currency().count())
except Entity.database_error.ConnectionFailureError:
    print("the Instance could not be reached")
```

#### `ExecutionError`

An Operation failed while running, for example when a record is still referenced by another and cannot be removed.

```python
from logic.interface import Entity

try:
    Entity.Service.User().delete(1)
except Entity.database_error.ExecutionError:
    print("the user is still referenced and was not removed")
```

#### `SetupError`

A Setup Operation did not complete. Entity Service offers no Setup Operation, so this error is raised only by Database's own Setup entry points; it is published so a caller can handle it alongside the others.

```python
from logic.interface import Entity

print(issubclass(Entity.database_error.SetupError, Entity.database_error.DatabaseError))
```

## Use

A caller imports the Logic Interface, selects a Child Service once, and calls its Actions without naming the Entity again. Requests are built with `Entity.Model` and `Entity.database_value`, and errors are caught with `Entity.database_error`; nothing else needs to be imported.

```python
from logic.interface import Entity

currency = Entity.Service.Currency()
condition = Entity.database_value.Filter(
    Entity.Model.Currency.code, Entity.database_value.FilterOperator.EQUALS, "USD"
)
try:
    usd = currency.list([condition])[0]
    print(usd.code, usd.symbol, currency.count([condition]))
except Entity.database_error.DatabaseError as error:
    print(type(error).__name__)
```

A Child Service holds only what belongs to its own Entity; every shared Action comes from Base. To give one Entity Behaviour of its own, change that Entity's Child Service only: it may add an Action, override a Base Action for its own Entity, or override one to make it unavailable for its Entity. It never detaches itself from Base and never copies or redefines its Entity. The example shows the three forms on a subclass of the published Currency Child Service; the same methods written inside the Currency Child Service give the same result for Currency alone and leave every other Child Service unchanged.

```python
from logic.interface import Entity


class Currency(Entity.Service.Currency):
    def list_active(self):
        active = Entity.database_value.Filter(
            Entity.Model.Currency.is_active,
            Entity.database_value.FilterOperator.EQUALS,
            True,
        )
        return self.list([active])

    def count(self, filters=None, combination=None, instance=None):
        return super().count(filters, combination, instance)

    def truncate(self, instance=None):
        raise NotImplementedError("truncate is not available for Currency")


currency = Currency()
print(len(currency.list_active()), currency.count())
try:
    currency.truncate()
except NotImplementedError as error:
    print(error)
print(Entity.Service.User().count())
```

## Verify

Run the script below from the Logic directory with `uv run python`. It checks, using the published Interfaces and reaching Base only as the parent class of a Child Service, that Entity Service publishes exactly its five groups; that `Service` has one Child Service for every Entity of Model's Entity Collection, in order, each binding its own Entity; that `Model` and the three Database groups are the identical objects their sources publish; that Base holds one Action for every Entity Operation of Database's Interface group, in Database's order, with the parameters of that Operation except the Entity class; that each Child Service gives the answer Database gives; that an instance of another Entity is rejected; and that loading opens no connection. It reads records only and prints `Entity Service verified` when every check holds.

```python
import inspect
import subprocess
import sys

import database.interface as database
import model.interface as model
from logic.interface import Entity

assert Entity.__all__ == [
    "Model",
    "Service",
    "database_error",
    "database_instance",
    "database_value",
]

names = [entity.__name__ for entity in model.entities]
assert [n for n in vars(Entity.Service) if not n.startswith("_")] == names
assert [n for n in vars(Entity.Model) if not n.startswith("_")] == names
for name, entity in zip(names, model.entities, strict=True):
    assert getattr(Entity.Model, name) is entity
    child = getattr(Entity.Service, name)()
    is_set = Entity.database_value.FilterOperator.IS_NOT_NULL
    child.count([Entity.database_value.Filter(entity.id, is_set)])
    foreign = next(other for other in model.entities if other is not entity)
    try:
        child.count([Entity.database_value.Filter(foreign.id, is_set)])
    except Entity.database_error.InvalidInputError:
        pass
    else:
        raise AssertionError(f"{name} is not bound to its own Entity only")

assert Entity.database_value is database.database_value
assert Entity.database_instance is database.database_instance
assert Entity.database_error is database.database_error

interface = database.database_interface
operations = [
    n
    for n, f in vars(interface).items()
    if inspect.isfunction(f)
    and not n.startswith("_")
    and "entity" in inspect.signature(f).parameters
]
base = Entity.Service.User.__mro__[1]
assert [n for n in vars(base) if not n.startswith("_")] == operations

TAKES_INSTANCE = {"add", "update"}
for operation in operations:
    expected = list(inspect.signature(getattr(interface, operation)).parameters)[1:]
    if operation not in TAKES_INSTANCE:
        expected.remove("entity")
    action = getattr(base, operation)
    assert list(inspect.signature(action).parameters)[1:] == expected, operation
    assert action.__doc__ == getattr(interface, operation).__doc__

db = interface()
for name, entity in zip(names, model.entities, strict=True):
    child = getattr(Entity.Service, name)()
    assert child.count() == db.count(entity)
    assert [r.id for r in child.list()] == [r.id for r in db.list(entity)]
    assert child.get_by_id(10**9) is None

other = Entity.Model.Broker(name="Not a currency", user_id=1)
before = Entity.Service.Currency().count()
try:
    Entity.Service.Currency().add(other)
except Entity.database_error.InvalidInputError:
    pass
else:
    raise AssertionError("an instance of another Entity was accepted")
assert Entity.Service.Currency().count() == before

check = (
    "import sqlite3, sqlalchemy\n"
    "def refuse(*a, **k):\n"
    "    raise SystemExit('a connection was opened')\n"
    "sqlite3.connect = refuse\n"
    "sqlalchemy.create_engine = refuse\n"
    "from logic.interface import Entity\n"
    "for n in vars(Entity.Service):\n"
    "    if not n.startswith('_'):\n"
    "        getattr(Entity.Service, n)()\n"
)
subprocess.run([sys.executable, "-c", check], check=True)

print("Entity Service verified")
```
