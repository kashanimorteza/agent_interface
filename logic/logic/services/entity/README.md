# Entity Service

## Overview

Entity Service gives every Entity of Model one Child Service. Storage Service takes the Entity on every request; a Child Service binds that Entity once, so a caller selects an Entity and then calls its Actions without passing the Entity again. Each Child Service receives the same Actions from one shared Base, and each Action hands its request to Storage and returns Storage's answer and errors unchanged. The Interface also publishes the Entities themselves and Database's four groups, so a caller needs no other import.

This example needs a prepared database (see the Database README). It adds one User and reads it back.

```python
from logic.services.entity.interface import Model, Service

users = Service.User()
user = users.add(
    Model.User(
        name="Ada", username="ada", password="example-password", api_key="example-key"
    )
)
print(user.id, users.get_by_id(user.id).username)
```

## Interface

The Entity Service Interface publishes exactly six names and nothing else; the Base and the Storage gateway are never published.

| Name | What it is |
|---|---|
| `Service` | a namespace holding one Child Service class for every Entity, under the Entity's name |
| `Model` | a namespace holding the Entity each Child Service binds, under the same name, as the original object Model publishes |
| `database_value` | Database's Value group, republished as the identical object |
| `database_instance` | Database's Instance group, republished as the identical object |
| `database_result` | Database's Result group, republished as the identical object |
| `database_error` | Database's Error group, republished as the identical object |

### Service: the Child Services

`Service` holds one Child Service for each of Model's Entities, in the Entity Collection's order: `User`, `TradingPlatform`, `Instance`, `Currency`, `Broker`, `Asset`, `AccountGroup`, `Account`, `TrailingGroup`, `TrailingRule`, `PartialGroup`, `PartialRule`, `ActionGroup`, `Action` and `Position`. Create one with no argument:

```python
from logic.services.entity.interface import Service

for name, child in vars(Service).items():
    if not name.startswith("_"):
        print(name, type(child()).__name__)
```

### Actions

Every Child Service has these Actions, one for each Storage Action that takes an Entity, in Storage's order, with the same name, parameter order and defaults. The Entity class is not a parameter: the Child Service supplies its bound Entity. `add` and `update` take an Entity instance, which must be an instance of the bound Entity, otherwise they raise `InvalidInputError` before Storage is called (only the Entity's identity is checked, never its Field values). The Database README explains each Operation.

| Action | Parameters |
|---|---|
| `add` | `entity`, `instance` |
| `update` | `entity`, `instance` |
| `list` | `filters`, `combination`, `orders`, `limit`, `instance` |
| `get_by_id` | `id`, `instance` |
| `delete` | `id`, `instance` |
| `enable` | `id`, `instance` |
| `disable` | `id`, `instance` |
| `count` | `filters`, `combination`, `instance` |
| `sum` | `field`, `filters`, `combination`, `instance` |
| `min` | `field`, `filters`, `combination`, `instance` |
| `max` | `field`, `filters`, `combination`, `instance` |
| `truncate` | `instance` |

The native command Action takes no Entity, so a Child Service does not have it; use Storage Service for it.

One example for each Action, on the `Currency`, `Account` and `User` Child Services:

```python
from logic.services.entity.interface import Model, Service, database_value

users = Service.User()
alan = users.add(
    Model.User(name="Alan", username="alan", password="x", api_key="y")
)  # add
alan.description = "Analyst"
alan = users.update(alan)  # update: replaces the mutable Fields
print(users.get_by_id(alan.id).description)  # get_by_id
print(
    users.disable(alan.id).is_active, users.enable(alan.id).is_active
)  # disable, enable
active = [
    database_value.Filter(
        Model.User.is_active, database_value.FilterOperator.EQUALS, True
    )
]
print([user.name for user in users.list(filters=active, limit=5)])  # list
print(users.count(active))  # count
print(Service.Account().sum(Model.Account.leverage))  # sum
currencies = Service.Currency()
print(
    currencies.min(Model.Currency.code), currencies.max(Model.Currency.code)
)  # min and max
print(users.delete(alan.id).name)  # delete
print(Service.PartialRule().truncate())  # truncate
```

### Model: the bound Entities

`Model` holds the same Entity objects Model publishes, under the same names as the Child Services. A caller can build an Entity without importing Model:

```python
from logic.services.entity.interface import Model, Service

currency = Model.Currency(user_id=1, code="XTS")
print(currency.code, Service.Currency._entity is Model.Currency)
```

### The four Storage groups

These are the identical objects Storage's Interface republishes, which are Database's own groups; each member is explained in the Database README. One example each:

```python
from logic.services.entity.interface import (
    Model,
    Service,
    database_error,
    database_instance,
    database_result,
    database_value,
)

users = Service.User()
admin = [
    database_value.Filter(
        Model.User.name, database_value.FilterOperator.EQUALS, "Admin"
    )
]
print(
    users.count(admin, instance=database_instance.SQLITE)
)  # Value and Instance groups
print(database_result.CommandResult.__name__)  # Result group
try:
    users.add(Model.Broker(name="Wrong", user_id=1))  # an instance of another Entity
except database_error.InvalidInputError as error:  # Error group
    print("refused:", error)
```

## Use

A caller imports a Child Service from the Entity Service Interface, creates it, and calls its Actions:

```python
from logic.services.entity.interface import Service

print(Service.Currency().count())
```

A Child Service adds Behaviour of its own by holding only what is specific to its Entity in its own unit, while everything shared stays in the Base. For example, a Child Service can inherit all Actions and add one Action around them. Subclassing a Child in your own code shows the idea; the Child keeps its Base:

```python
from logic.services.entity.interface import Model, Service, database_value


class Currencies(Service.Currency):
    """A Currency Child Service with one Action of its own."""

    def with_digits(self, digits: int) -> list[str]:
        digit_filter = [
            database_value.Filter(
                Model.Currency.decimal_digits,
                database_value.FilterOperator.EQUALS,
                digits,
            )
        ]
        return [currency.code for currency in self.list(filters=digit_filter)]


print(Currencies().with_digits(0))
```

## Verify

Run this from the `logic` directory. It checks that Entity Service has one Child Service for every Entity of Model's Entity Collection, that the Base mirrors Storage's Entity-taking Actions, and that the four groups are the Storage groups, unchanged. It prints `verified` when everything holds.

```python
import inspect

from model import interface as model

from logic.services.entity import interface as entity
from logic.services.entity.base import BaseEntity
from logic.services.storage import interface as storage

entities = list(model.entities)
children = [name for name in vars(entity.Service) if not name.startswith("_")]
assert children == [e.__name__ for e in entities]
for e in entities:
    assert getattr(entity.Model, e.__name__) is e
    assert getattr(entity.Service, e.__name__)._entity is e
taking_entity = [
    name
    for name, member in vars(storage.Storage).items()
    if not name.startswith("_")
    and callable(member)
    and list(inspect.signature(member).parameters)[1:2] == ["entity"]
]
actions = [
    name
    for name, member in vars(BaseEntity).items()
    if not name.startswith("_") and callable(member)
]
assert actions == taking_entity
for group in (
    "database_value",
    "database_instance",
    "database_result",
    "database_error",
):
    assert getattr(entity, group) is getattr(storage, group)
assert sorted(entity.__all__) == sorted(
    [
        "Service",
        "Model",
        "database_value",
        "database_instance",
        "database_result",
        "database_error",
    ]
)
print("verified")
```
