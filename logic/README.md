# Logic

Application Behaviour for the Trading Assistant, organized as modular Services behind one Interface. A consumer selects a Service, selects an Entity, and calls an Action; Logic works out the rest.

```python
from logic.interface import Entity

admin = Entity.UserService().get_by_id(1)
print(admin.username)
```

```text
admin
```

## Interface

`logic.interface` is the only public Logic surface. It publishes each Service Interface whose publication setting is enabled, unchanged and under the Service's configured name, and nothing else. Other files are internal.

| Name | Service Interface | Reaches |
|---|---|---|
| `Entity` | Entity Service Interface | one Child Service for every Entity Model publishes, and the Database Instance Enum |

Storage Service is a fixed internal Service that is not published, so it is not part of the Logic Interface.

## Services

### Entity

Entity Service gives every Entity Model publishes one Child Service. Select the Child Service once, then call an Action on it; the Child supplies its own Entity, so it is never passed again.

| Entity | Child Service |
|---|---|
| User | `UserService` |
| Trading Platform | `TradingPlatformService` |
| Instance | `InstanceService` |
| Currency | `CurrencyService` |
| Broker | `BrokerService` |
| Asset | `AssetService` |
| Account Group | `AccountGroupService` |
| Account | `AccountService` |
| Trailing Group | `TrailingGroupService` |
| Trailing Rule | `TrailingRuleService` |
| Partial Group | `PartialGroupService` |
| Partial Rule | `PartialRuleService` |
| Action Group | `ActionGroupService` |
| Action | `ActionService` |
| Position | `PositionService` |

Every Action accepts an optional `instance`, a member of `Entity.DatabaseInstance`; when it is omitted, Database uses its default Instance.

```python
from logic.interface import Entity

currencies = Entity.CurrencyService()
print(currencies.count(instance=Entity.DatabaseInstance.SQLITE))
```

```text
8
```

Add and Update accept only an instance of the Child Service's own Entity. The Entity classes come from Model, which Logic does not republish. Filters and Orders are Database vocabulary that Entity Service accepts and does not republish.

#### Actions that change data

Add persists a complete Entity instance and returns it with its generated `id`.

```python
from logic.interface import Entity
from model.interface import Broker

brokers = Entity.BrokerService()
created = brokers.add(Broker(name="Example Broker", user_id=1))
print(created.name, isinstance(created.id, int))
brokers.delete(created.id)
```

```text
Example Broker True
```

Update replaces the mutable Fields of the record with the Entity's `id` and returns it, or returns `None` when no record has that `id`.

```python
from logic.interface import Entity
from model.interface import Broker

brokers = Entity.BrokerService()
created = brokers.add(Broker(name="Example Broker", user_id=1))
created.description = "Updated"
print(brokers.update(created).description)
brokers.delete(created.id)
```

```text
Updated
```

Enable sets `is_active` to `true` and returns the record, or `None` when no record has the `id`.

```python
from logic.interface import Entity

brokers = Entity.BrokerService()
brokers.disable(1)
print(brokers.enable(1).is_active)
```

```text
True
```

Disable sets `is_active` to `false` and returns the record, or `None` when no record has the `id`.

```python
from logic.interface import Entity

brokers = Entity.BrokerService()
print(brokers.disable(1).is_active)
brokers.enable(1)
```

```text
False
```

Delete removes a record and returns whether one existed.

```python
from logic.interface import Entity
from model.interface import Broker

brokers = Entity.BrokerService()
created = brokers.add(Broker(name="Example Broker", user_id=1))
print(brokers.delete(created.id), brokers.delete(created.id))
```

```text
True False
```

Truncate removes every record of the Entity and returns how many were removed.

```python
from logic.interface import Entity

print(Entity.PositionService().truncate())
```

```text
0
```

#### Actions that read data

Get by ID returns the record with the `id`, or `None`.

```python
from logic.interface import Entity

currencies = Entity.CurrencyService()
print(currencies.get_by_id(1).code, currencies.get_by_id(999))
```

```text
USD None
```

List returns the matching records; `limit` bounds how many, and Filters and Orders narrow and order them.

```python
from logic.interface import Entity

print([currency.code for currency in Entity.CurrencyService().list(limit=3)])
```

```text
['USD', 'EUR', 'GBP']
```

Count returns the number of matching records.

```python
from logic.interface import Entity

print(Entity.CurrencyService().count())
```

```text
8
```

Sum returns the total of a Field over the matching records.

```python
from logic.interface import Entity

print(Entity.CurrencyService().sum("decimal_digits"))
```

```text
14
```

Min returns the smallest value of a Field over the matching records.

```python
from logic.interface import Entity

print(Entity.CurrencyService().min("decimal_digits"))
```

```text
0
```

Max returns the largest value of a Field over the matching records.

```python
from logic.interface import Entity

print(Entity.CurrencyService().max("decimal_digits"))
```

```text
2
```

#### Credentials at rest

Entity Service stores credential Fields as the Target requires. User `password` and `api_key` are stored as one-way hashes. Instance `password` and `api_key` and Account `password` are stored encrypted, which needs the protection value `LOGIC_CREDENTIAL_PROTECTION_KEY` in the environment. A credential equal to the stored value is kept as it is, so updating another Field never treats a credential twice, and a returned Entity carries the stored value, never the plaintext.

```python
from logic.interface import Entity
from model.interface import User

users = Entity.UserService()
created = users.add(User(name="Ada", username="ada", password="a-plain-password", api_key="an-api-key"))
print(created.password.startswith("scrypt$"), "a-plain-password" in created.password)
users.delete(created.id)
```

```text
True False
```

```python
import os

from cryptography.fernet import Fernet

from logic.interface import Entity
from model.interface import Instance

os.environ["LOGIC_CREDENTIAL_PROTECTION_KEY"] = Fernet.generate_key().decode()
instances = Entity.InstanceService()
created = instances.add(Instance(user_id=1, trading_platform_id=1, name="Example", password="a-plain-password"))
print(created.password != "a-plain-password")
instances.delete(created.id)
```

```text
True
```

## Setup

Install Logic and its dependencies into an isolated environment, prepare the Database Instance, and provide the protection value.

1. Install: `uv sync`
2. Create the Tables: `uv run database create-tables`
3. Insert the Initial Data: `uv run database insert-initial-data`
4. Provide the protection value for encrypted credentials, without writing it into source:

```text
export LOGIC_CREDENTIAL_PROTECTION_KEY="$(uv run python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())')"
```

## Use

Reach Logic only through `logic.interface`: import `Entity`, select a Child Service, and call an Action. Do not import Logic's other files, Database, or a Storage Action.

```python
from logic.interface import Entity

assets = Entity.AssetService()
print([asset.symbol for asset in assets.list(limit=2)])
```

```text
['EUR/USD', 'EUR/GBP']
```

## Verify

Confirm a prepared Logic through the public surface: the Initial Data must be reachable.

```python
from logic.interface import Entity

print("Logic is ready" if Entity.UserService().count() >= 1 else "Database is empty")
```

```text
Logic is ready
```

## Troubleshooting

### Required value is missing

Adding or updating an Instance or Account with a credential needs the protection value. Without it the write is refused before anything is stored.

```python
import os

from logic.interface import Entity
from model.interface import Instance

os.environ.pop("LOGIC_CREDENTIAL_PROTECTION_KEY", None)
try:
    Entity.InstanceService().add(Instance(user_id=1, trading_platform_id=1, name="Example", password="secret"))
except ValueError as error:
    print(error)
```

```text
Required value 'credential_protection_key' is missing; set LOGIC_CREDENTIAL_PROTECTION_KEY
```

Set `LOGIC_CREDENTIAL_PROTECTION_KEY` as shown in Setup.

### Required value is invalid

A value that is not a valid protection key is refused, and its text is never repeated.

```python
import os

from logic.interface import Entity
from model.interface import Instance

os.environ["LOGIC_CREDENTIAL_PROTECTION_KEY"] = "not-a-key"
try:
    Entity.InstanceService().add(Instance(user_id=1, trading_platform_id=1, name="Example", password="secret"))
except ValueError as error:
    print(error)
```

```text
Required value 'credential_protection_key' in LOGIC_CREDENTIAL_PROTECTION_KEY is invalid (fernet_key)
```

Generate a valid key as shown in Setup.

### Entity does not belong to the Child Service

Add and Update accept only the Child Service's own Entity.

```python
from logic.interface import Entity
from model.interface import User

try:
    Entity.BrokerService().add(User(name="Ada", username="ada", password="p", api_key="k"))
except TypeError as error:
    print(error)
```

```text
BrokerService accepts only Broker instances, not User
```

Select the Child Service of the Entity you are storing.
