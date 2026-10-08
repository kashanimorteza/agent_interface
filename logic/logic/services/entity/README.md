# Entity Service

## Overview

Entity Service gives every Entity published by Model one Child Service, so a caller selects an Entity once and then calls its Actions without passing the Entity again. A Child Service adds its bound Entity to each request and hands it to Database, and returns Database's answer unchanged.

```python
from logic.interface import Entity

users = Entity.Service.User()
print(users.get_by_id(1).username)
```

## Interface

A caller imports `Entity` from Logic and reaches exactly five names: the groups `Service` and `Model`, and Database's `database_value`, `database_instance` and `database_error` groups. Base, Database's Interface, Setup and Result groups are never published. Loading the Interface opens no connection and creates no data or file.

### Service

`Entity.Service` holds exactly one Child Service for every Entity of Model's Entity Collection, under the Entity's name. Create one with no argument, then call its Actions without passing the Entity.

| Child Service | Binds | Example |
| --- | --- | --- |
| `Service.User` | `Model.User` | `Entity.Service.User().count()` |
| `Service.TradingPlatform` | `Model.TradingPlatform` | `Entity.Service.TradingPlatform().count()` |
| `Service.Instance` | `Model.Instance` | `Entity.Service.Instance().count()` |
| `Service.Currency` | `Model.Currency` | `Entity.Service.Currency().count()` |
| `Service.Broker` | `Model.Broker` | `Entity.Service.Broker().count()` |
| `Service.Asset` | `Model.Asset` | `Entity.Service.Asset().count()` |
| `Service.AccountGroup` | `Model.AccountGroup` | `Entity.Service.AccountGroup().count()` |
| `Service.Account` | `Model.Account` | `Entity.Service.Account().count()` |
| `Service.TrailingGroup` | `Model.TrailingGroup` | `Entity.Service.TrailingGroup().count()` |
| `Service.TrailingRule` | `Model.TrailingRule` | `Entity.Service.TrailingRule().count()` |
| `Service.PartialGroup` | `Model.PartialGroup` | `Entity.Service.PartialGroup().count()` |
| `Service.PartialRule` | `Model.PartialRule` | `Entity.Service.PartialRule().count()` |
| `Service.ActionGroup` | `Model.ActionGroup` | `Entity.Service.ActionGroup().count()` |
| `Service.Action` | `Model.Action` | `Entity.Service.Action().count()` |
| `Service.Position` | `Model.Position` | `Entity.Service.Position().count()` |

```python
from logic.interface import Entity

children = [
    Entity.Service.User,
    Entity.Service.TradingPlatform,
    Entity.Service.Instance,
    Entity.Service.Currency,
    Entity.Service.Broker,
    Entity.Service.Asset,
    Entity.Service.AccountGroup,
    Entity.Service.Account,
    Entity.Service.TrailingGroup,
    Entity.Service.TrailingRule,
    Entity.Service.PartialGroup,
    Entity.Service.PartialRule,
    Entity.Service.ActionGroup,
    Entity.Service.Action,
    Entity.Service.Position,
]
for child in children:
    print(child.__name__, child().count())
```

### Actions

Every Child Service has one Action for every Entity Operation of Database's Interface group, in Database's order, with the same name and parameters except the removed Entity class. Each Action calls Database through the one Database object its Child Service holds and returns Database's answer and errors unchanged.

#### `add(entity, instance=None)`

Store one new Entity instance and return the stored Entity, including generated values.

- **Accepts:** an Entity instance of the bound Entity whose generated Fields are still pending.
- **Returns:** the stored Entity, including generated values.
- **Entity:** the Child Service supplies its bound Entity; the Entity class is never passed, and an instance of any other Entity is refused with `database_error.InvalidInputError` before Database is called.
- **Instance:** the optional last parameter selects a `database_instance` member.

```python
from logic.interface import Entity

currencies = Entity.Service.Currency()
stored = currencies.add(
    Entity.Model.Currency(user_id=1, code="XAU", symbol="Au", decimal_digits=2)
)
print(stored.id, stored.code)
currencies.delete(stored.id)
```

#### `update(entity, instance=None)`

Replace every mutable Field of the stored record of an Entity instance; None when it does not exist.

- **Accepts:** an Entity instance of the bound Entity that carries its stored id.
- **Returns:** the stored Entity, or None when no record has that id.
- **Entity:** the Child Service supplies its bound Entity; the Entity class is never passed, and an instance of any other Entity is refused with `database_error.InvalidInputError` before Database is called.
- **Instance:** the optional last parameter selects a `database_instance` member.

```python
from logic.interface import Entity

brokers = Entity.Service.Broker()
broker = brokers.get_by_id(1)
broker.description = "Primary broker"
print(brokers.update(broker).description)
broker.description = None
brokers.update(broker)
```

#### `list(filters=None, combination=None, orders=None, limit=None, instance=None)`

Return the matching Entity instances; a zero or negative limit means no limit.

- **Accepts:** optional filters, combination, orders and limit.
- **Returns:** the matching Entity instances; id ascending, AND and no limit by default.
- **Entity:** the Child Service supplies its bound Entity; the Entity class is never passed, and an instance of any other Entity is refused with `database_error.InvalidInputError` before Database is called.
- **Instance:** the optional last parameter selects a `database_instance` member.

```python
from logic.interface import Entity

value = Entity.database_value
currencies = Entity.Service.Currency()
found = currencies.list(
    filters=[
        value.Filter(
            Entity.Model.Currency.decimal_digits, value.FilterOperator.EQUALS, 2
        )
    ],
    orders=[value.Order(Entity.Model.Currency.code, value.OrderDirection.DESCENDING)],
    limit=3,
)
print([currency.code for currency in found])
```

#### `get_by_id(id, instance=None)`

Return the Entity with that id, or None when no record exists.

- **Accepts:** an integer id.
- **Returns:** the Entity, or None when no record exists.
- **Entity:** the Child Service supplies its bound Entity; the Entity class is never passed, and an instance of any other Entity is refused with `database_error.InvalidInputError` before Database is called.
- **Instance:** the optional last parameter selects a `database_instance` member.

```python
from logic.interface import Entity

users = Entity.Service.User()
print(users.get_by_id(1).username, users.get_by_id(999))
```

#### `delete(id, instance=None)`

Remove the record and return the deleted Entity, or None when no record exists.

- **Accepts:** an integer id.
- **Returns:** the final deleted Entity, or None when no record exists.
- **Entity:** the Child Service supplies its bound Entity; the Entity class is never passed, and an instance of any other Entity is refused with `database_error.InvalidInputError` before Database is called.
- **Instance:** the optional last parameter selects a `database_instance` member.

```python
from logic.interface import Entity

currencies = Entity.Service.Currency()
stored = currencies.add(Entity.Model.Currency(user_id=1, code="TMP"))
print(currencies.delete(stored.id).code, currencies.delete(stored.id))
```

#### `enable(id, instance=None)`

Set only is_active to true and return the final Entity, or None when no record exists.

- **Accepts:** an integer id.
- **Returns:** the final Entity (also when it was already enabled), or None when no record exists.
- **Entity:** the Child Service supplies its bound Entity; the Entity class is never passed, and an instance of any other Entity is refused with `database_error.InvalidInputError` before Database is called.
- **Instance:** the optional last parameter selects a `database_instance` member.

```python
from logic.interface import Entity

print(Entity.Service.Broker().enable(1).is_active)
```

#### `disable(id, instance=None)`

Set only is_active to false and return the final Entity, or None when no record exists.

- **Accepts:** an integer id.
- **Returns:** the final Entity (also when it was already disabled), or None when no record exists.
- **Entity:** the Child Service supplies its bound Entity; the Entity class is never passed, and an instance of any other Entity is refused with `database_error.InvalidInputError` before Database is called.
- **Instance:** the optional last parameter selects a `database_instance` member.

```python
from logic.interface import Entity

brokers = Entity.Service.Broker()
print(brokers.disable(1).is_active)
brokers.enable(1)
```

#### `count(filters=None, combination=None, instance=None)`

Return the number of matching records.

- **Accepts:** optional filters and combination.
- **Returns:** the matching count.
- **Entity:** the Child Service supplies its bound Entity; the Entity class is never passed, and an instance of any other Entity is refused with `database_error.InvalidInputError` before Database is called.
- **Instance:** the optional last parameter selects a `database_instance` member.

```python
from logic.interface import Entity

value = Entity.database_value
assets = Entity.Service.Asset()
print(
    assets.count(),
    assets.count(
        [
            value.Filter(
                Entity.Model.Asset.category, value.FilterOperator.EQUALS, "Commodity"
            )
        ]
    ),
)
```

#### `sum(field, filters=None, combination=None, instance=None)`

Return the total of a numeric Field, ignoring null values, or zero when nothing matches.

- **Accepts:** a numeric Field reference, then optional filters and combination.
- **Returns:** the total, or zero when nothing matches.
- **Entity:** the Child Service supplies its bound Entity; the Entity class is never passed, and an instance of any other Entity is refused with `database_error.InvalidInputError` before Database is called.
- **Instance:** the optional last parameter selects a `database_instance` member.

```python
from logic.interface import Entity

print(Entity.Service.Currency().sum(Entity.Model.Currency.decimal_digits))
```

#### `min(field, filters=None, combination=None, instance=None)`

Return the smallest non-null value of a comparable Field, or None when nothing matches.

- **Accepts:** a comparable Field reference, then optional filters and combination.
- **Returns:** the smallest value, or None when nothing matches.
- **Entity:** the Child Service supplies its bound Entity; the Entity class is never passed, and an instance of any other Entity is refused with `database_error.InvalidInputError` before Database is called.
- **Instance:** the optional last parameter selects a `database_instance` member.

```python
from logic.interface import Entity

print(Entity.Service.Currency().min(Entity.Model.Currency.code))
```

#### `max(field, filters=None, combination=None, instance=None)`

Return the largest non-null value of a comparable Field, or None when nothing matches.

- **Accepts:** a comparable Field reference, then optional filters and combination.
- **Returns:** the largest value, or None when nothing matches.
- **Entity:** the Child Service supplies its bound Entity; the Entity class is never passed, and an instance of any other Entity is refused with `database_error.InvalidInputError` before Database is called.
- **Instance:** the optional last parameter selects a `database_instance` member.

```python
from logic.interface import Entity

print(Entity.Service.Currency().max(Entity.Model.Currency.code))
```

#### `truncate(instance=None)`

Remove every record of the Entity, keep its Table, and return the deleted count.

- **Accepts:** nothing but the optional instance.
- **Returns:** the number of deleted records (the Table is kept).
- **Entity:** the Child Service supplies its bound Entity; the Entity class is never passed, and an instance of any other Entity is refused with `database_error.InvalidInputError` before Database is called.
- **Instance:** the optional last parameter selects a `database_instance` member.

```python
from logic.interface import Entity

print(Entity.Service.Position().truncate())
```

### Model

`Entity.Model` holds the Entity each Child Service binds, under the same name as its Child Service, as the original object Model Interface publishes. A caller builds Entity instances from it without importing Model.

| Entity | Example |
| --- | --- |
| `Model.User` | `Entity.Model.User.declaration.name` |
| `Model.TradingPlatform` | `Entity.Model.TradingPlatform.declaration.name` |
| `Model.Instance` | `Entity.Model.Instance.declaration.name` |
| `Model.Currency` | `Entity.Model.Currency.declaration.name` |
| `Model.Broker` | `Entity.Model.Broker.declaration.name` |
| `Model.Asset` | `Entity.Model.Asset.declaration.name` |
| `Model.AccountGroup` | `Entity.Model.AccountGroup.declaration.name` |
| `Model.Account` | `Entity.Model.Account.declaration.name` |
| `Model.TrailingGroup` | `Entity.Model.TrailingGroup.declaration.name` |
| `Model.TrailingRule` | `Entity.Model.TrailingRule.declaration.name` |
| `Model.PartialGroup` | `Entity.Model.PartialGroup.declaration.name` |
| `Model.PartialRule` | `Entity.Model.PartialRule.declaration.name` |
| `Model.ActionGroup` | `Entity.Model.ActionGroup.declaration.name` |
| `Model.Action` | `Entity.Model.Action.declaration.name` |
| `Model.Position` | `Entity.Model.Position.declaration.name` |

```python
from logic.interface import Entity

entities = [
    Entity.Model.User,
    Entity.Model.TradingPlatform,
    Entity.Model.Instance,
    Entity.Model.Currency,
    Entity.Model.Broker,
    Entity.Model.Asset,
    Entity.Model.AccountGroup,
    Entity.Model.Account,
    Entity.Model.TrailingGroup,
    Entity.Model.TrailingRule,
    Entity.Model.PartialGroup,
    Entity.Model.PartialRule,
    Entity.Model.ActionGroup,
    Entity.Model.Action,
    Entity.Model.Position,
]
for entity in entities:
    print(entity.__name__, entity.declaration.name, len(entity.declaration.fields))
```

### database_value

`Entity.database_value` is Database's Value group, passed on as the identical object.

#### `database_value.Filter`

```python
from logic.interface import Entity

value = Entity.database_value
condition = value.Filter(Entity.Model.Currency.code, value.FilterOperator.EQUALS, "USD")
print([currency.id for currency in Entity.Service.Currency().list([condition])])
```

#### `database_value.Order`

```python
from logic.interface import Entity

value = Entity.database_value
orders = [
    value.Order(Entity.Model.Asset.category),
    value.Order(Entity.Model.Asset.digits, value.OrderDirection.DESCENDING),
]
print([asset.symbol for asset in Entity.Service.Asset().list(orders=orders)])
```

#### `database_value.FilterOperator`

```python
from logic.interface import Entity

value = Entity.database_value
print([operator.name for operator in value.FilterOperator])
print(
    Entity.Service.Asset().count(
        [
            value.Filter(
                Entity.Model.Asset.symbol, value.FilterOperator.STARTS_WITH, "EUR"
            )
        ]
    )
)
```

#### `database_value.FilterCombination`

```python
from logic.interface import Entity

value = Entity.database_value
filters = [
    value.Filter(Entity.Model.Currency.code, value.FilterOperator.EQUALS, "USD"),
    value.Filter(Entity.Model.Currency.code, value.FilterOperator.EQUALS, "EUR"),
]
currencies = Entity.Service.Currency()
print(
    currencies.count(filters, value.FilterCombination.AND),
    currencies.count(filters, value.FilterCombination.OR),
)
```

#### `database_value.OrderDirection`

```python
from logic.interface import Entity

value = Entity.database_value
for direction in value.OrderDirection:
    found = Entity.Service.Currency().list(
        orders=[value.Order(Entity.Model.Currency.code, direction)], limit=2
    )
    print(direction.name, [currency.code for currency in found])
```

### database_instance

`Entity.database_instance` is Database's Instance group, the enumeration of active Instances, passed on as the identical object. With the delivered configuration its only member is `SQLITE`.

```python
from logic.interface import Entity

currencies = Entity.Service.Currency()
print([member.name for member in Entity.database_instance])
print(currencies.count(instance=Entity.database_instance.SQLITE) == currencies.count())
```

### database_error

`Entity.database_error` is Database's Error group, passed on as the identical object. Every error derives from `DatabaseError`.

#### `database_error.DatabaseError`

The base of every Database error; catch it to catch them all.

```python
from logic.interface import Entity

try:
    Entity.Service.Currency().get_by_id("1")
except Entity.database_error.DatabaseError as error:
    print(type(error).__name__)
```

#### `database_error.ConfigurationError`

The configuration or the selected Instance is invalid; raised when the Database loads.

```python
import importlib

try:
    entity = importlib.import_module("logic.interface").Entity
except Exception as error:
    print(type(error).__name__, error)
else:
    print("configuration valid:", sorted(entity.__all__))
```

#### `database_error.InactiveInstanceError`

A selected Instance is no longer active.

```python
from logic.interface import Entity

try:
    print(Entity.Service.Currency().count(instance=Entity.database_instance.SQLITE))
except Entity.database_error.InactiveInstanceError:
    print("the selected Instance is no longer active")
```

#### `database_error.InvalidInputError`

The request holds invalid input, for example an instance of another Entity.

```python
from logic.interface import Entity

try:
    Entity.Service.Currency().add(Entity.Model.Broker(name="x", user_id=1))
except Entity.database_error.InvalidInputError as error:
    print(error)
```

#### `database_error.DeclarationMismatchError`

An existing Table differs from the Declaration of its Entity, or a stored row breaks the contract of its Entity.

```python
from logic.interface import Entity

try:
    print(len(Entity.Service.Currency().list()))
except Entity.database_error.DeclarationMismatchError as error:
    print(error)
```

#### `database_error.ConnectionFailureError`

The storage of the Instance could not be opened.

```python
from logic.interface import Entity

try:
    print(Entity.Service.Currency().count())
except Entity.database_error.ConnectionFailureError:
    print("the storage could not be opened")
```

#### `database_error.ExecutionError`

A command or operation failed while running, for example by breaking a constraint.

```python
from logic.interface import Entity

try:
    Entity.Service.Currency().add(Entity.Model.Currency(user_id=1, code="USD"))
except Entity.database_error.ExecutionError as error:
    print(error)
```

#### `database_error.SetupError`

A Setup Operation did not complete. Entity Service never uses Database Setup; the kind is published so a caller can catch every Database error.

```python
from logic.interface import Entity

try:
    print(Entity.Service.User().count())
except Entity.database_error.SetupError:
    print("setup did not complete")
```

## Use

Import `Entity` from Logic and select a Child Service by the Entity's name. Create it once and keep it; it holds one Database object and opens no connection until an Action is called.

```python
from logic.interface import Entity

assets = Entity.Service.Asset()
value = Entity.database_value
cheap = assets.list(
    [value.Filter(Entity.Model.Asset.digits, value.FilterOperator.LESS_OR_EQUAL, 3)]
)
print([asset.symbol for asset in cheap])
```

A Child Service holds only Behavior specific to its Entity; every shared Action comes from Base, and a Child Service may override a Base Action for its own Entity but never detaches itself from Base. Add Behavior in the Entity's Child Service unit. The same shape in a caller's own code:

```python
from logic.interface import Entity


class ActiveUsers(Entity.Service.User):
    def active(self):
        value = Entity.database_value
        return self.list(
            [
                value.Filter(
                    Entity.Model.User.is_active, value.FilterOperator.EQUALS, True
                )
            ]
        )


print([user.username for user in ActiveUsers().active()])
```

## Verify

Run the script below with `uv run python` from the Logic directory. It checks, from the published Interfaces alone, that the Entity Service matches Model's Entity Collection and Database's Interface group: exactly five names are published, there is one Child Service and one Model entry per Entity in Collection order, every Model entry and Database group is the identical object its source publishes, every Child Service binds its own Entity and receives Base, there is one Action per Database Entity Operation in Database's order with its name, parameter names, order and defaults minus the Entity class, an instance of another Entity is refused, and loading opens no connection. It prints `Entity Service verified` when every check holds.

```python
import inspect
import sqlite3
import subprocess
import sys
import tempfile

import database.interface as database
import model.interface as model
from logic.interface import Entity

assert sorted(Entity.__all__) == [
    "Model",
    "Service",
    "database_error",
    "database_instance",
    "database_value",
]
assert sorted(n for n in vars(Entity) if not n.startswith("_")) == sorted(
    Entity.__all__
)

names = [entity.__name__ for entity in model.entities]
assert [n for n in vars(Entity.Service) if not n.startswith("_")] == names
assert [n for n in vars(Entity.Model) if not n.startswith("_")] == names
for entity in model.entities:
    child = getattr(Entity.Service, entity.__name__)
    assert getattr(Entity.Model, entity.__name__) is entity is child._entity
    assert [c.__name__ for c in child.__mro__[1:2]] == ["BaseEntity"]
    assert [n for n in vars(child) if not n.startswith("__")] == ["_entity"]

assert Entity.database_value is database.database_value
assert Entity.database_instance is database.database_instance
assert Entity.database_error is database.database_error

operations = [
    n
    for n, f in vars(database.database_interface).items()
    if inspect.isfunction(f)
    and not n.startswith("_")
    and list(inspect.signature(f).parameters)[1:2] == ["entity"]
]
child = Entity.Service.Currency
base = child.__mro__[1]
actions = [
    n for n, f in vars(base).items() if inspect.isfunction(f) and not n.startswith("_")
]
assert actions == operations
for name in operations:
    published = list(
        inspect.signature(
            getattr(database.database_interface, name)
        ).parameters.values()
    )
    mirrored = list(inspect.signature(getattr(child, name)).parameters.values())
    kept = mirrored[1].name == "entity"
    expected = published[1:] if kept else published[2:]
    assert [(p.name, p.default) for p in mirrored[1:]] == [
        (p.name, p.default) for p in expected
    ]

try:
    Entity.Service.Currency().add(Entity.Model.Broker(name="x", user_id=1))
except Entity.database_error.InvalidInputError:
    pass
else:
    raise AssertionError("an instance of another Entity was accepted")

with tempfile.TemporaryDirectory() as directory:
    code = "import sqlite3\nsqlite3.connect = lambda *a, **k: 1 / 0\nimport logic.interface"
    done = subprocess.run(
        [sys.executable, "-c", code], cwd=directory, capture_output=True
    )
    assert done.returncode == 0

print("Entity Service verified")
```
