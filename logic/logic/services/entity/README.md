# Entity Service

## Overview

Entity Service gives every Entity that Model publishes one Child Service. A caller selects a Child Service once and then
calls its Actions without passing the Entity again; the Child Service adds its bound Entity to the request, hands it to
Storage, and returns Storage's answer and errors unchanged. All Actions live in one shared Base, which mirrors every
Storage Action that takes an Entity, so a Child Service only holds Behaviour that belongs to its own Entity.

```python
from logic.services.entity.interface import User

users = User()
print([user.name for user in users.list()])  # ['Admin']
```

## Interface

The Entity Service Interface publishes exactly one Child Service for every Entity in Model's Entity Collection, in that
order, and the 16 contracts that the Storage Service Interface republishes, as the same objects. Base, the Storage
gateway, and every Child implementation are never published, and loading the Interface opens no connection and creates no
data or file.

### Child Services

| Child Service | Entity | Example |
|---|---|---|
| `User` | User | `User().count()` |
| `TradingPlatform` | Trading Platform | `TradingPlatform().count()` |
| `Instance` | Instance | `Instance().count()` |
| `Currency` | Currency | `Currency().count()` |
| `Broker` | Broker | `Broker().count()` |
| `Asset` | Asset | `Asset().count()` |
| `AccountGroup` | Account Group | `AccountGroup().count()` |
| `Account` | Account | `Account().count()` |
| `TrailingGroup` | Trailing Group | `TrailingGroup().count()` |
| `TrailingRule` | Trailing Rule | `TrailingRule().count()` |
| `PartialGroup` | Partial Group | `PartialGroup().count()` |
| `PartialRule` | Partial Rule | `PartialRule().count()` |
| `ActionGroup` | Action Group | `ActionGroup().count()` |
| `Action` | Action | `Action().count()` |
| `Position` | Position | `Position().count()` |

### Actions

Every Child Service has these Actions, one for every Storage Action that takes an Entity, with Storage's names, parameters,
defaults, and documentation. The Entity class parameter is removed because the Child Service supplies it; `add` and
`update` take an Entity instance, which must be an instance of the bound Entity, otherwise the Invalid Input error is raised
before Storage is called.

| Action | Parameters | What it does |
|---|---|---|
| `add` | `entity, instance=None` | Store one complete new Entity instance and return the stored Entity. |
| `update` | `entity, instance=None` | Replace every mutable Field of the stored record; null when no record exists. |
| `list` | `filters=None, combination=None, orders=None, limit=None, instance=None` | Return the Entities that match; a zero or negative limit means no limit. |
| `get_by_id` | `id, instance=None` | Return the Entity with the given id, or null. |
| `delete` | `id, instance=None` | Remove the record and return the final deleted Entity, or null. |
| `enable` | `id, instance=None` | Set only the activity Field to true and return the final Entity, or null. |
| `disable` | `id, instance=None` | Set only the activity Field to false and return the final Entity, or null. |
| `count` | `filters=None, combination=None, instance=None` | Return the number of matching records. |
| `sum` | `field, filters=None, combination=None, instance=None` | Return the total of a numeric Field, ignoring nulls, or zero. |
| `min` | `field, filters=None, combination=None, instance=None` | Return the smallest value of a comparable Field, ignoring nulls, or null. |
| `max` | `field, filters=None, combination=None, instance=None` | Return the largest value of a comparable Field, ignoring nulls, or null. |
| `truncate` | `instance=None` | Remove every record of the Entity, keep its Table, and return the deleted count. |

### Republished contracts

These are the contracts of the Storage Service, without the Storage gateway; see the Storage Service documentation for what
each one is.

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

```python
from logic.services.entity.interface import (
    Account,
    Currency,
    Filter,
    FilterOperator,
    InvalidInputError,
    Order,
    OrderDirection,
    User,
)
from model import interface as model

users = User()
ada = users.add(
    model.User(name="Ada", username="ada", password="example-password", api_key="example-key")
)  # add
ada.description = "mathematician"
print(users.update(ada).description)  # update: mathematician
print(
    [
        user.name
        for user in users.list(orders=[Order(model.User.id, OrderDirection.DESCENDING)], limit=1)
    ]
)  # list: ['Ada']
print(users.get_by_id(ada.id).username)  # get_by_id: ada
print(
    users.disable(ada.id).is_active, users.enable(ada.id).is_active
)  # disable, enable: False True
print(users.count(filters=[Filter(model.User.is_active, FilterOperator.EQUALS, True)]))  # count: 2
print(
    users.sum(model.User.id), users.min(model.User.id), users.max(model.User.id)
)  # sum, min, max: 3 1 2
print(users.delete(ada.id).name)  # delete: Ada
currencies = Currency()
print(currencies.count())  # 8
try:
    currencies.add(model.User(name="x", username="x", password="p", api_key="k"))
except InvalidInputError:
    print("refused: not a Currency")  # an instance of another Entity
```

The numbers in the comments are for a freshly prepared Database.

## Use

Import a Child Service and the contracts you need from the Entity Service Interface, and create it where needed. Creating a
Child Service creates one Storage access that its Actions share.

A Child Service holds only Behaviour specific to its Entity and may override a Base Action for its own Entity; it never
detaches from Base. Behaviour of your own goes in the Child Service's own unit, for example:

```python
from logic.services.entity.interface import Filter, FilterOperator, User
from model import interface as model


class Users(User):
    def active(self):
        return self.list(filters=[Filter(model.User.is_active, FilterOperator.EQUALS, True)])


print([user.name for user in Users().active()])  # ['Admin']
```

## Verify

This script checks that Entity Service matches Model's Entity Collection and the Storage Interface. It prints
`all checks passed` when every check holds.

```python
import inspect

import logic.services.entity.interface as entity_interface
import logic.services.storage.interface as storage_interface
import model.interface as model
from logic.services.storage.interface import Storage

contracts = [name for name in storage_interface.__all__ if name != "Storage"]
children = [entity.__name__ for entity in model.entities]
assert set(entity_interface.__all__) == {*children, *contracts}
assert [name for name in entity_interface.__all__ if name in children] == children
assert all(
    getattr(entity_interface, name) is getattr(storage_interface, name) for name in contracts
)

taking = [
    (name, member)
    for name, member in vars(Storage).items()
    if not name.startswith("_")
    and callable(member)
    and list(inspect.signature(member).parameters)[1:2] == ["entity"]
]
for entity in model.entities:
    child = getattr(entity_interface, entity.__name__)()
    assert child.count() == Storage().count(entity)  # bound to exactly its own Entity
    base = [
        (name, member)
        for name, member in vars(type(child).__mro__[1]).items()
        if not name.startswith("_") and callable(member)
    ]
    assert [name for name, _ in base] == [name for name, _ in taking]
    for (name, action), (_, storage_action) in zip(base, taking):
        expected = [key for key in inspect.signature(storage_action).parameters if key != "self"]
        if name not in ("add", "update"):
            expected.remove("entity")
        assert [key for key in inspect.signature(action).parameters if key != "self"] == expected, (
            name
        )

print("all checks passed")
```
