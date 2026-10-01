# Logic

Logic is the Behaviour layer of the Trading Assistant. It organizes what the application does into Services, and consumers reach it through one Interface: select a Service, select an Entity once, and call an Action. Consumers use only `logic.interface`; the Core, the Services' implementation, and every dependency behind them are never part of the public surface.

## Overview

```python
from logic.interface import Entity
from model.interface import Broker

brokers = Entity.BrokerService()
added = brokers.add(Broker(name="Example Broker", user_id=1))
print([broker.name for broker in brokers.list()])
brokers.delete(added.id)  # tidy up: Broker names are unique per user
```

Output:

```text
['FxPro', 'Example Broker']
```

## Interface

`logic.interface` is the single root gateway of Logic. It publishes the Interface of every Service whose publication is enabled, unchanged and under the Service's configured name, and nothing else. It defines no Action, wrapper, Category, or dependency of its own, and loading it opens no connection, creates no data, and starts no process. Today one Service is published:

| Name | What it is |
| --- | --- |
| `Entity` | The Entity Service Interface: one Child Service per Model Entity and the types its Actions accept. |

```python
import logic.interface

print([name for name in dir(logic.interface) if not name.startswith("_")])
```

```text
['Entity']
```

Logic has one further internal Service. It is not published, so it is not part of what a consumer can use, and it is not described here.

The examples in this README continue one Python session on a prepared Instance (see [Setup](#setup)). Every one of them starts from these imports; Entities and their Fields always come from Model, which Logic never republishes:

```python
from decimal import Decimal

from logic.interface import Entity
from model.interface import Asset, Broker, TrailingRule, User
```

## Services

### Entity

`Entity` is the Entity Service Interface. A consumer first selects the Child Service of an Entity and then calls one of its Actions, so the Entity is named once and never repeated for each request. It presents:

- one Child Service for every Entity Model publishes, named after the Entity with the suffix `Service`, for example `Entity.BrokerService`;
- `children`, the ordered tuple of all Child Services, in Model's Entity order;
- the types the Actions accept: `DatabaseInstance`, `Filter`, `FilterOperator`, `FilterCombination`, `Order`, and `OrderDirection`, exactly the objects Database publishes.

It does not present the shared mechanism the Child Services receive, a flat list of Actions, or any storage capability.

```python
print([child.__name__ for child in Entity.children])
```

```text
['UserService', 'TradingPlatformService', 'InstanceService', 'CurrencyService', 'BrokerService', 'AssetService', 'AccountGroupService', 'AccountService', 'TrailingGroupService', 'TrailingRuleService', 'PartialGroupService', 'PartialRuleService', 'ActionGroupService', 'ActionService', 'PositionService']
```

| Entity | Child Service |
| --- | --- |
| User | `Entity.UserService` |
| Trading Platform | `Entity.TradingPlatformService` |
| Instance | `Entity.InstanceService` |
| Currency | `Entity.CurrencyService` |
| Broker | `Entity.BrokerService` |
| Asset | `Entity.AssetService` |
| Account Group | `Entity.AccountGroupService` |
| Account | `Entity.AccountService` |
| Trailing Group | `Entity.TrailingGroupService` |
| Trailing Rule | `Entity.TrailingRuleService` |
| Partial Group | `Entity.PartialGroupService` |
| Partial Rule | `Entity.PartialRuleService` |
| Action Group | `Entity.ActionGroupService` |
| Action | `Entity.ActionService` |
| Position | `Entity.PositionService` |

Every Child Service offers the same twelve Actions. Every Action takes an optional last parameter, `instance`, a member of `Entity.DatabaseInstance`; when it is omitted the call runs on the default Instance. `DatabaseInstance` has one member per active Instance, today `SQLITE`:

```python
print([member.name for member in Entity.DatabaseInstance])
```

```text
['SQLITE']
```

An absent record is not an error: Actions that look a record up return `None`. A failure Database raises reaches the caller unchanged. An instance of another Entity given to Add or Update is rejected with `TypeError` before anything is stored.

#### Add

`add(entity, instance)` stores one new instance of the Child's Entity and returns the stored Entity, including generated values.

```python
brokers = Entity.BrokerService()
added = brokers.add(Broker(name="Example Broker", user_id=1))
print(added.name, added.is_active)
```

```text
Example Broker True
```

#### Update

`update(entity, instance)` replaces the mutable Fields of the stored record the instance's `id` locates, and returns the stored Entity, or `None` when no record exists.

```python
added.description = "A broker added by the documentation"
updated = brokers.update(added)
print(updated.description)
```

```text
A broker added by the documentation
```

#### List

`list(filters, combination, orders, limit, instance)` returns the Child's records that match, ordered and limited. Filters, combination, orders, and limit are all optional; a zero or negative limit means no limit.

```python
for broker in brokers.list(orders=[Entity.Order(Broker.name, Entity.OrderDirection.ASCENDING)]):
    print(broker.name)
```

```text
Example Broker
FxPro
```

#### Get By Id

`get_by_id(id, instance)` returns the record with the identity, or `None` when none exists.

```python
print(brokers.get_by_id(added.id).name)
print(brokers.get_by_id(99999))
```

```text
Example Broker
None
```

#### Enable

`enable(id, instance)` sets only `is_active` to true and returns the final Entity, including when it was already enabled, or `None` when none exists.

```python
print(brokers.enable(added.id).is_active)
```

```text
True
```

#### Disable

`disable(id, instance)` sets only `is_active` to false and returns the final Entity, including when it was already disabled, or `None` when none exists.

```python
print(brokers.disable(added.id).is_active)
```

```text
False
```

#### Delete

`delete(id, instance)` deletes the record and returns it as it was, or `None` when none exists.

```python
deleted = brokers.delete(added.id)
print(deleted.name, brokers.get_by_id(added.id))
```

```text
Example Broker None
```

#### Count

`count(filters, combination, instance)` returns how many records match.

```python
assets = Entity.AssetService()
commodity = Entity.Filter(Asset.category, Entity.FilterOperator.EQUALS, "Commodity")
print(assets.count(), assets.count([commodity]))
```

```text
4 2
```

#### Sum

`sum(field, filters, combination, instance)` returns the total of a numeric Field, ignoring nulls, or zero when nothing matches.

```python
print(assets.sum(Asset.digits))
```

```text
15
```

#### Min

`min(field, filters, combination, instance)` returns the smallest value of a comparable Field, ignoring nulls, or `None` when nothing matches.

```python
print(assets.min(Asset.digits))
```

```text
2
```

#### Max

`max(field, filters, combination, instance)` returns the largest value of a comparable Field, ignoring nulls, or `None` when nothing matches.

```python
print(assets.max(Asset.digits))
```

```text
5
```

#### Truncate

`truncate(instance)` removes every record of the Child's Entity, keeps its storage, and returns the deleted count.

```python
rules = Entity.TrailingRuleService()
for name, percent in (("First", "10"), ("Second", "20")):
    rules.add(TrailingRule(name=name, trailing_group_id=1, trigger_percentage=Decimal(percent)))
print(rules.truncate(), rules.count())
```

```text
2 0
```

## Setup

Logic is a Python 3.14 library managed with `uv`. It consumes Model and Database, which must sit next to it as the sibling directories `model/` and `database/`. Database must be set up first, because Logic stores and reads only through it.

```bash
cd database
uv sync
uv run python scripts/prepare.py
cd ../logic
uv sync
```

`uv sync` creates each virtual environment, installs the exact versions in `uv.lock`, and installs the sibling libraries by path. Preparing creates Database's tables and Initial Data on its default Instance; Database's generation already does this, so repeating it is safe and changes nothing. Logic needs no runtime value: its configuration is reserved and empty, and nothing is read from the environment, so there is nothing to supply and no credential to protect. Run every example with `uv run python` from the `logic/` directory.

## Use

Reach Logic only through `logic.interface`: select a Child Service, then call an Action. Choosing an Instance, building Filters and Orders, and reading an absent record all use the types and results the Entity Service publishes.

Choosing an Instance means passing a `DatabaseInstance` member as the last argument; omitting it runs on the default Instance, so the two calls below agree.

```python
brokers = Entity.BrokerService()
print(brokers.count(instance=Entity.DatabaseInstance.SQLITE), brokers.count())
```

```text
1 1
```

Filters, combinations, and Orders are built from the published types and Field references of the Entity, never from strings.

```python
users = Entity.UserService()
active = [Entity.Filter(User.is_active, Entity.FilterOperator.EQUALS, True)]
newest_first = [Entity.Order(User.name, Entity.OrderDirection.DESCENDING)]
print([user.name for user in users.list(active, Entity.FilterCombination.AND, newest_first, limit=5)])
```

```text
['Admin']
```

Reading or changing a record that is not there returns `None` instead of raising:

```python
temporary = brokers.add(Broker(name="Temporary Broker", user_id=1))
brokers.delete(temporary.id)
print(brokers.get_by_id(temporary.id), brokers.update(temporary), brokers.delete(temporary.id))
```

```text
None None None
```

Selecting a Child Service selects the Entity, so an instance of any other Entity is refused before anything is stored:

```python
try:
    brokers.add(User(name="Other", username="other", password="x", api_key="y"))
except TypeError as error:
    print(error)
```

```text
BrokerService accepts only Broker instances, not User.
```

A failure Database raises, such as a name that must be unique, reaches the caller unchanged:

```python
try:
    brokers.add(Broker(name="FxPro", user_id=1))
except Exception as error:
    print(type(error).__name__)
```

```text
ExecutionError
```

## Verify

This script checks Logic through its public Interface only, on a prepared Instance. It leaves no record behind and prints `OK` when every check passes.

```python
import logic.interface
from logic.interface import Entity
from model.interface import Broker, User, entities

# public import: the root gateway presents exactly the publication-enabled Services
assert [name for name in dir(logic.interface) if not name.startswith("_")] == ["Entity"]

# every Entity has one bound Child Service, in Model's Entity order, and a Child serves only its own Entity
assert [child.__name__ for child in Entity.children] == [f"{entity.__name__}Service" for entity in entities]
for child, entity in zip(Entity.children, entities, strict=True):
    assert all(isinstance(record, entity) for record in child().list())

# an instance of a different Entity is rejected, and nothing is stored
users, brokers = Entity.UserService(), Entity.BrokerService()
before = users.count()
try:
    brokers.add(User(name="Other", username="other", password="x", api_key="y"))
except TypeError:
    pass
else:
    raise AssertionError("a User was accepted by the Broker Child Service")
assert users.count() == before

# an Action reaches storage through the Instance that is chosen, and through the default when none is
chosen = Entity.DatabaseInstance.SQLITE
assert brokers.count(instance=chosen) == brokers.count()
record = brokers.add(Broker(name="Verify Broker", user_id=1), chosen)
assert brokers.get_by_id(record.id, chosen).name == "Verify Broker"
assert brokers.get_by_id(record.id).name == "Verify Broker"
brokers.delete(record.id, chosen)
assert brokers.get_by_id(record.id, chosen) is None

print("OK")
```

```text
OK
```

## Troubleshooting

### A Service is not published

`logic.interface` presents a Service only when that Service's publication setting is enabled, so a name such as `Storage` raises `AttributeError`. The Service exists inside Logic whatever its setting; only its publication is off. Change the Service's publication setting in Logic's Preferences, which are human-owned, and regenerate.

```python
print(hasattr(logic.interface, "Entity"), hasattr(logic.interface, "Storage"))
```

```text
True False
```

### A Service identity is invalid or collides

Loading `logic.interface` raises `ConfigurationError` when a configured Service name or location is not a valid identifier, is a reserved word, or equals another Service's name or location after normalization. The message names the value, for example `'Entity Service' is not a valid identifier.`. Logic never repairs, suffixes, or renames an identity: correct the configured value in Logic's Preferences and regenerate.

### Storage does not match Database Interface

Loading Logic raises `ConfigurationError` when the Storage gateway does not publish exactly one Action for every capability Database Interface publishes and every contract it publishes, for example `... missing ['storage_archive'], unexpected [].`. This happens when Database Interface changes after Logic was generated; regenerate Logic so that Storage follows it.
