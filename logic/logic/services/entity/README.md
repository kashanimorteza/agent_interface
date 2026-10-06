# Entity Service

## Overview

Entity Service gives every Entity that Model publishes its own Child Service. A caller selects a Child Service once
and then calls its Actions without passing the Entity again. Each Child Service receives the one shared Base, which
offers one Action for every Storage Action that takes an Entity and hands the request to Storage, so Entity Service
never reaches Database. Its Interface publishes four groups: `Service` (the Child Services), `Model` (the Entity
each binds), `Parameter` (the Storage contracts that are not errors), and `Error` (the Storage errors).

```python
from logic.services.entity.interface import Service
from logic.services.storage.interface import Storage

Storage().prepare()  # the Database storage must hold its Tables and Initial Data
users = Service.User()
print(users.get_by_id(1).name)  # Admin
```

## Interface

`logic.services.entity.interface` publishes exactly the four groups below and nothing else. Base, the Storage
gateway, and the Child Service implementations are never published, and loading the Interface opens no connection
and creates no data.

### Service

One Child Service for every Entity in Model's Entity Collection, in the Collection's order and under the Entity's
own name. Create one with no arguments; it takes one access to Storage.

| Child Service | Example |
|---|---|
| `Service.User` | `Service.User().count()` |
| `Service.TradingPlatform` | `Service.TradingPlatform().count()` |
| `Service.Instance` | `Service.Instance().count()` |
| `Service.Currency` | `Service.Currency().count()` |
| `Service.Broker` | `Service.Broker().count()` |
| `Service.Asset` | `Service.Asset().count()` |
| `Service.AccountGroup` | `Service.AccountGroup().count()` |
| `Service.Account` | `Service.Account().count()` |
| `Service.TrailingGroup` | `Service.TrailingGroup().count()` |
| `Service.TrailingRule` | `Service.TrailingRule().count()` |
| `Service.PartialGroup` | `Service.PartialGroup().count()` |
| `Service.PartialRule` | `Service.PartialRule().count()` |
| `Service.ActionGroup` | `Service.ActionGroup().count()` |
| `Service.Action` | `Service.Action().count()` |
| `Service.Position` | `Service.Position().count()` |

```python
from logic.services.entity.interface import Service

names = [
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
]
counts = {name: getattr(Service, name)().count() for name in names}
print(len(counts), sum(counts.values()))  # 15 23
print(counts["Currency"], counts["TrailingRule"])  # 8 0
```

### Actions of every Child Service

Every Child Service has exactly the Actions below, which mirror the Storage Actions that take an Entity, in
Storage's order and with Storage's parameter names, order, defaults, and results. The Entity class is not a
parameter: the Child Service supplies its own. Add and Update take an Entity instance, which must be an instance
of the Child Service's own Entity; any other instance is refused with `InvalidInputError` before Storage is
called. Every other argument, the result, and every error are Storage's, unchanged. Every Action takes an optional
`DatabaseInstance` as its last parameter, and a missing record returns `None`.

**`add(entity, instance=None)`** stores one complete new Entity instance and returns the stored Entity.

```python
from logic.services.entity.interface import Error, Model, Service

brokers = Service.Broker()
broker = brokers.add(Model.Broker(name="Scratch broker", user_id=1))
print(broker.name)  # Scratch broker
```

**`update(entity, instance=None)`** replaces every mutable Field of the stored record the Entity's `id` locates.

```python
broker.description = "Backup broker"
print(brokers.update(broker).description)  # Backup broker
```

**`list(filters=None, combination=None, orders=None, limit=None, instance=None)`** returns the matching Entities.

```python
from logic.services.entity.interface import Parameter

rows = Service.Currency().list(
    filters=[Parameter.Filter(Model.Currency.decimal_digits, Parameter.FilterOperator.EQUALS, 2)],
    orders=[Parameter.Order(Model.Currency.code, Parameter.OrderDirection.DESCENDING)],
    limit=3,
)
print([currency.code for currency in rows])  # ['USD', 'NZD', 'GBP']
```

**`get_by_id(id, instance=None)`** returns the Entity with that `id`, or `None`.

```python
print(Service.User().get_by_id(999))  # None
```

**`delete(id, instance=None)`** removes the record and returns the final deleted Entity, or `None`.

```python
print(brokers.delete(broker.id).name)  # Scratch broker
```

**`enable(id, instance=None)`** and **`disable(id, instance=None)`** set only `is_active` and return the final
Entity, or `None`.

```python
currencies = Service.Currency()
print(currencies.disable(1).is_active)  # False
print(currencies.enable(1).is_active)  # True
```

**`count(filters=None, combination=None, instance=None)`** returns the number of matching records.

```python
usd_or_eur = Parameter.Filter(Model.Currency.code, Parameter.FilterOperator.IN, ["USD", "EUR"])
print(currencies.count([usd_or_eur], Parameter.FilterCombination.AND))  # 2
```

**`sum(field, filters=None, combination=None, instance=None)`** returns the total of a numeric Field, ignoring
nulls, or zero. **`min(...)`** and **`max(...)`** take the same parameters for a comparable Field and return the
smallest or largest value, or `None`.

```python
print(Service.Asset().sum(Model.Asset.digits))  # 15
print(currencies.min(Model.Currency.code), currencies.max(Model.Currency.code))  # AUD USD
```

**`truncate(instance=None)`** removes every record of the Entity, keeps its Table, and returns the deleted count.

```python
print(Service.Position().truncate())  # 0
```

An Action given an instance of another Entity is refused before Storage is called:

```python
try:
    brokers.add(Model.Currency(user_id=1, code="USD"))
except Error.InvalidInputError as error:
    print(error)  # Expected an instance of Broker
```

### Model

The Entity each Child Service binds, under the same name as its Child Service, as the original object Model
publishes, so a caller builds an Entity without importing Model. `Model.User`, `Model.TradingPlatform`,
`Model.Instance`, `Model.Currency`, `Model.Broker`, `Model.Asset`, `Model.AccountGroup`, `Model.Account`,
`Model.TrailingGroup`, `Model.TrailingRule`, `Model.PartialGroup`, `Model.PartialRule`, `Model.ActionGroup`,
`Model.Action`, and `Model.Position` are each the Entity of that name.

```python
currency = Model.Currency(user_id=1, code="CHF")
bound = Service.Currency._entity
print(isinstance(currency, bound), Model.Currency is bound)  # True True
```

### Parameter

Every contract the Storage Service Interface publishes that is not an error, except the Storage gateway, as the
original object.

| Member | Example |
|---|---|
| `Parameter.DatabaseInstance` | `Parameter.DatabaseInstance.SQLITE` selects the active Instance explicitly. |
| `Parameter.Filter` | `Parameter.Filter(Model.Currency.code, Parameter.FilterOperator.EQUALS, "USD")` |
| `Parameter.FilterOperator` | `Parameter.FilterOperator.STARTS_WITH` |
| `Parameter.FilterCombination` | `Parameter.FilterCombination.OR` |
| `Parameter.Order` | `Parameter.Order(Model.Currency.code, Parameter.OrderDirection.ASCENDING)` |
| `Parameter.OrderDirection` | `Parameter.OrderDirection.DESCENDING` |
| `Parameter.CommandResult` | the result type of a Database-wide command run through Storage |
| `Parameter.LifecycleResult` | the result type of a Lifecycle Command run through Storage |

```python
members = [member.name for member in Parameter.DatabaseInstance]
print(members, Parameter.FilterCombination.OR.name)  # ['SQLITE'] OR
```

### Error

Every error the Storage Service Interface publishes, as the original object.

| Member | Example |
|---|---|
| `Error.DatabaseError` | `except Error.DatabaseError:` catches every error below. |
| `Error.ConfigurationError` | `except Error.ConfigurationError:` when the configuration or a selected Instance is invalid. |
| `Error.InactiveInstanceError` | `except Error.InactiveInstanceError:` when an inactive Instance is selected. |
| `Error.InvalidInputError` | `except Error.InvalidInputError:` when an input, Entity, or Field is invalid. |
| `Error.DeclarationMismatchError` | `except Error.DeclarationMismatchError:` when a stored row differs from its Declaration. |
| `Error.ConnectionFailureError` | `except Error.ConnectionFailureError:` when the Instance cannot be reached. |
| `Error.ExecutionError` | `except Error.ExecutionError:` when a request fails or violates a constraint. |
| `Error.LifecycleError` | `except Error.LifecycleError:` when a Lifecycle Command leaves an incomplete state. |

```python
try:
    Service.Currency().list(filters="USD")
except Error.DatabaseError as error:
    print(type(error).__name__)  # InvalidInputError
```

## Use

A caller imports the groups it needs from the Entity Service Interface, selects a Child Service, and calls its
Actions:

```python
from logic.services.entity.interface import Error, Model, Parameter, Service

users = Service.User()
admins = users.list(
    [Parameter.Filter(Model.User.username, Parameter.FilterOperator.EQUALS, "admin")]
)
print([user.name for user in admins])  # ['Admin']
```

A Child Service holds only Behaviour or Actions specific to its Entity; everything shared comes from Base. To add
Behaviour for one Entity, add a method to that Entity's Child Service, which stays a subclass of Base. An override of
a Base Action applies to that Entity only.

```python
from logic.services.entity.base import BaseEntity
from model import interface as model


class Currency(BaseEntity):
    _entity = model.Currency

    def with_symbol(self, symbol: str) -> list:
        return self.list(
            [Parameter.Filter(model.Currency.symbol, Parameter.FilterOperator.EQUALS, symbol)]
        )


print([currency.code for currency in Currency().with_symbol("€")])  # ['EUR']
```

## Verify

Run this script from the Logic directory with `uv run python`. It checks that the Interface publishes exactly four
groups, that the Child Services are one for every Entity of Model's Entity Collection in the Collection's order and
each binds its own Entity, that Model, Parameter, and Error hold the identical objects their sources publish, that
Base has one Action for every Storage Action that takes an Entity with Storage's parameters minus the Entity class,
and that importing the Interface and creating a Child Service open no connection and start no process. It prints
`all checks passed` when every check holds.

```python
import inspect
import subprocess
import sys

import logic.services.entity.interface as entity
import logic.services.storage.interface as storage
import model.interface as model
from logic.services.entity.base import BaseEntity

assert sorted(entity.__all__) == ["Error", "Model", "Parameter", "Service"]
assert sorted(name for name in vars(entity) if not name.startswith("_")) == sorted(entity.__all__)

names = [name for name in vars(entity.Service) if not name.startswith("_")]
assert names == [entity_class.__name__ for entity_class in model.entities]
for name in names:
    child = getattr(entity.Service, name)
    assert issubclass(child, BaseEntity) and child._entity is getattr(model, name)
    assert getattr(entity.Model, name) is getattr(model, name)
assert [name for name in vars(entity.Model) if not name.startswith("_")] == names


def is_error(name):
    value = getattr(storage, name)
    return isinstance(value, type) and issubclass(value, BaseException)


parameters = [name for name in storage.__all__ if name != "Storage" and not is_error(name)]
errors = [name for name in storage.__all__ if is_error(name)]
assert [name for name in vars(entity.Parameter) if not name.startswith("_")] == parameters
assert [name for name in vars(entity.Error) if not name.startswith("_")] == errors
assert all(getattr(entity.Parameter, name) is getattr(storage, name) for name in parameters)
assert all(getattr(entity.Error, name) is getattr(storage, name) for name in errors)

takes_instance = {"add", "update"}
gateway = [
    name
    for name, value in vars(storage.Storage).items()
    if not name.startswith("_") and callable(value)
]
with_entity = [
    name
    for name in gateway
    if list(inspect.signature(getattr(storage.Storage, name)).parameters)[1:2] == ["entity"]
]
actions = [
    name for name, value in vars(BaseEntity).items() if not name.startswith("_") and callable(value)
]
assert actions == with_entity
for name in actions:
    expected = list(inspect.signature(getattr(storage.Storage, name)).parameters.values())
    if name not in takes_instance:
        del expected[1]
    assert list(inspect.signature(getattr(BaseEntity, name)).parameters.values()) == expected
    assert inspect.getdoc(getattr(BaseEntity, name)) == inspect.getdoc(
        getattr(storage.Storage, name)
    )

probe = """
import sys
events = []
sys.addaudithook(lambda event, args: events.append(event) if event in ("socket.connect", "subprocess.Popen", "sqlite3.connect") else None)
from logic.services.entity.interface import Service
Service.User()
sys.exit(1 if events else 0)
"""
assert subprocess.run([sys.executable, "-c", probe], check=False).returncode == 0

print("all checks passed")
```
