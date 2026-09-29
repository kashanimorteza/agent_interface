# Logic

## Overview

Application Behaviour library for the Trading Assistant. Consumers reach every capability through one root, choose a Service, and call one of its Actions. Logic starts no process, defines no transport, and depends on no API framework.

Logic sits between its consumers and the two Components it uses: Model supplies the Entities and Database stores them. A consumer states what it wants done and receives Database's own result; it never learns which Component did the work.

## Interface

`logic.interface` is the only public Logic surface. It publishes two Service Interfaces, unchanged, under their Service names:

- `Storage` — one Action for every Operation Database publishes, plus the Database Instance Enum.
- `Entity` — one Child Service for every Entity Model publishes.

The root defines no Actions, wrappers, Categories, or duplicated dependency symbols. There are two ways to reach persistence:

- Directly, through the Actions of `Storage`.
- Through an Entity Child Service of `Entity`; choosing the Child Service chooses the Entity.

```python
from logic.interface import Entity, Storage

print(Storage.storage_get_by_id.__name__, Entity.CurrencyService.entity.__name__)
```

```text
storage_get_by_id Currency
```

The next example reads the seeded Currency with id 1, which must exist (see Setup).

```python
from logic.interface import Entity

print(Entity.CurrencyService.get_by_id(1).code)
```

```text
USD
```

## Services

### Storage

Storage is Logic's gateway to every Database Operation. Every Action is named `storage_<operation>`, takes the request its Database Operation takes together with an optional `instance`, and returns Database's result unchanged. When `instance` is omitted, Database uses its configured default Instance. `Storage.DatabaseInstance` is Database's own Instance Enum: `DatabaseInstance.SQLITE` and `DatabaseInstance.POSTGRESQL`.

Entity classes come from Model (`model.interface`). Filters, Filter Combinations, and Orders are Database's request vocabulary (`database.interface`); Logic does not republish them.

#### Add

Persists a complete Entity instance and returns it with its generated `id`.

```python
from logic.interface import Storage
from model.interface import Currency

created = Storage.storage_add(Currency(user_id=1, code="SEK", symbol="kr", country="Sweden"))
print(created.code, isinstance(created.id, int))
Storage.storage_delete(Currency, created.id)
```

```text
SEK True
```

#### Update

Replaces every mutable Field of the record with the instance's `id`; returns the record, or `None` when no record has that `id`.

```python
from logic.interface import Storage
from model.interface import Currency

created = Storage.storage_add(Currency(user_id=1, code="SEK", symbol="kr", country="Sweden"))
created.symbol = "Skr"
print(Storage.storage_update(created).symbol)
Storage.storage_delete(Currency, created.id)
```

```text
Skr
```

#### List

Returns matching records. `filters`, `combination`, `orders`, and `limit` are optional; Database applies its defaults for any that are omitted.

```python
from database.interface import Filter, FilterOperator
from logic.interface import Storage
from model.interface import Currency

found = Storage.storage_list(Currency, [Filter("code", FilterOperator.IN, ["USD", "EUR"])])
print([currency.code for currency in found])
```

```text
['USD', 'EUR']
```

#### Delete

Returns `True` when a record was deleted and `False` when no record has that `id`.

```python
from logic.interface import Storage
from model.interface import Currency

created = Storage.storage_add(Currency(user_id=1, code="SEK", symbol="kr", country="Sweden"))
print(Storage.storage_delete(Currency, created.id), Storage.storage_delete(Currency, created.id))
```

```text
True False
```

#### Enable and Disable

Set the record's `is_active` Field and return the record, or `None` when no record has that `id`.

```python
from logic.interface import Storage
from model.interface import Currency

created = Storage.storage_add(Currency(user_id=1, code="SEK", symbol="kr", country="Sweden"))
print(Storage.storage_disable(Currency, created.id).is_active)
print(Storage.storage_enable(Currency, created.id).is_active)
Storage.storage_delete(Currency, created.id)
```

```text
False
True
```

#### Get by ID

Returns the record, or `None` when no record has that `id`.

```python
from logic.interface import Storage
from model.interface import Currency

print(Storage.storage_get_by_id(Currency, 1).code, Storage.storage_get_by_id(Currency, 999999))
```

```text
USD None
```

#### Count

Returns the number of matching records.

```python
from database.interface import Filter, FilterOperator
from logic.interface import Storage
from model.interface import Currency

print(Storage.storage_count(Currency, [Filter("code", FilterOperator.IN, ["USD", "EUR"])]))
```

```text
2
```

#### Sum, Min, and Max

Total, smallest, and largest usable value of one Field over the matching records; `null` values are ignored.

```python
from database.interface import Filter, FilterOperator
from logic.interface import Storage
from model.interface import Currency

only = [Filter("code", FilterOperator.IN, ["USD", "JPY"])]
print(Storage.storage_sum(Currency, "decimal_digits", only))
print(Storage.storage_min(Currency, "decimal_digits", only))
print(Storage.storage_max(Currency, "decimal_digits", only))
```

```text
2
0
2
```

#### Truncate

Removes every record of an Entity and returns how many were removed. The example empties Position, which holds no Initial Data.

```python
from logic.interface import Storage
from model.interface import Position

print(Storage.storage_truncate(Position))
```

```text
0
```

#### Execute Command

Executes a SQL command with named bound parameters and returns Database's Command Result, with `rows` and `affected_count`. Logic never repeats the command on its own.

```python
from logic.interface import Storage

result = Storage.storage_execute_command("SELECT code FROM currency WHERE id = :id", {"id": 1})
print(result.rows)
```

```text
[{'code': 'USD'}]
```

#### Create Tables and Insert Initial Data

Prepare an Instance. Create Tables creates or migrates every Table the Model Entities need; Insert Initial Data inserts the declared Initial Data the Instance does not already hold and returns how many records it inserted.

```python
from logic.interface import Storage

Storage.storage_create_tables()
print(Storage.storage_insert_initial_data())
```

```text
0
```

### Entity

Entity offers one Child Service per Model Entity, named `<Entity>Service`: `UserService`, `TradingPlatformService`, `InstanceService`, `CurrencyService`, `BrokerService`, `AssetService`, `AccountGroupService`, `AccountService`, `TrailingGroupService`, `TrailingRuleService`, `PartialGroupService`, `PartialRuleService`, `ActionGroupService`, `ActionService`, and `PositionService`. Selecting a Child Service selects the Entity, so its Actions never take an Entity class. Add and Update accept only an instance of that Child Service's own Entity. Every Action accepts an optional `instance` from `Storage.DatabaseInstance`.

Every Child Service has the same twelve Actions: `add`, `update`, `list`, `delete`, `enable`, `disable`, `get_by_id`, `count`, `sum`, `min`, `max`, and `truncate`. Create Tables, Insert Initial Data, and Execute Command are Database-wide and stay in `Storage`.

#### Add

```python
from logic.interface import Entity
from model.interface import Currency

service = Entity.CurrencyService
created = service.add(Currency(user_id=1, code="SEK", symbol="kr", country="Sweden"))
print(created.code, isinstance(created.id, int))
service.delete(created.id)
```

```text
SEK True
```

#### Update

```python
from logic.interface import Entity
from model.interface import Currency

service = Entity.CurrencyService
created = service.add(Currency(user_id=1, code="SEK", symbol="kr", country="Sweden"))
created.symbol = "Skr"
print(service.update(created).symbol)
service.delete(created.id)
```

```text
Skr
```

#### List

```python
from database.interface import Filter, FilterOperator
from logic.interface import Entity

found = Entity.CurrencyService.list([Filter("code", FilterOperator.IN, ["USD", "EUR"])])
print([currency.code for currency in found])
```

```text
['USD', 'EUR']
```

#### Delete

```python
from logic.interface import Entity
from model.interface import Currency

service = Entity.CurrencyService
created = service.add(Currency(user_id=1, code="SEK", symbol="kr", country="Sweden"))
print(service.delete(created.id), service.delete(created.id))
```

```text
True False
```

#### Enable and Disable

```python
from logic.interface import Entity
from model.interface import Currency

service = Entity.CurrencyService
created = service.add(Currency(user_id=1, code="SEK", symbol="kr", country="Sweden"))
print(service.disable(created.id).is_active, service.enable(created.id).is_active)
service.delete(created.id)
```

```text
False True
```

#### Get by ID

```python
from logic.interface import Entity

service = Entity.CurrencyService
print(service.get_by_id(1).code, service.get_by_id(999999))
```

```text
USD None
```

#### Count

```python
from database.interface import Filter, FilterOperator
from logic.interface import Entity

print(Entity.CurrencyService.count([Filter("code", FilterOperator.IN, ["USD", "EUR"])]))
```

```text
2
```

#### Sum, Min, and Max

```python
from database.interface import Filter, FilterOperator
from logic.interface import Entity

service = Entity.CurrencyService
only = [Filter("code", FilterOperator.IN, ["USD", "JPY"])]
print(service.sum("decimal_digits", only), service.min("decimal_digits", only), service.max("decimal_digits", only))
```

```text
2 0 2
```

#### Truncate

```python
from logic.interface import Entity

print(Entity.PositionService.truncate())
```

```text
0
```

#### Choosing an Instance

Every Action of both Services accepts an optional member of `Storage.DatabaseInstance`. The Instance is passed to Database unchanged.

```python
from logic.interface import Entity, Storage

print(Entity.CurrencyService.get_by_id(1, Storage.DatabaseInstance.SQLITE).code)
```

```text
USD
```

#### Credential Fields

The Target requires credentials to be protected at rest, and the Entity Child Services apply it whenever a record is written through them:

- User `password` and `api_key` are stored only as salted one-way hashes; the plain value cannot be recovered.
- Instance `password` and `api_key`, and Account `password`, are stored only in encrypted form; the plain value is recoverable only with the runtime value `LOGIC_ENCRYPTION_KEY` (see Setup).
- A credential left unchanged by an update keeps its stored form; a new value is protected again.
- An Account password may not equal the password or `api_key` of its Instance, and an Instance credential may not equal the password of an Account that uses it.

Reads return the stored, protected form. Protection is applied by the Entity Child Services only; a record written through `Storage` is stored exactly as given.

```python
from logic.interface import Entity
from model.interface import User

created = Entity.UserService.add(User(name="Docs", username="docs", password="example-password", api_key="example-key"))
print(created.password != "example-password", created.password.startswith("scrypt$"))
Entity.UserService.delete(created.id)
```

```text
True True
```

An Instance is protected the same way, with encryption:

```python
from logic.interface import Entity
from model.interface import Instance

created = Entity.InstanceService.add(Instance(user_id=1, trading_platform_id=1, name="Docs", password="example-password"))
print(created.password != "example-password", created.api_key)
Entity.InstanceService.delete(created.id)
```

```text
True None
```

## Setup

1. Install Logic. From the Logic directory run `uv sync`; Model and Database are installed with it as path dependencies.
2. Prepare the Database that Logic uses. Still in the Logic directory, run `uv run database create-tables` and then `uv run database insert-initial-data`; the examples above read the seeded Currency records. The commands act on the copy of Database installed with Logic, not on the Database directory.
3. Supply the runtime value Logic requires. Logic owns the contract and validates the value before the Behaviour that needs it runs, but never stores it or its source.

| Runtime value | Needed by | Content |
|---|---|---|
| `LOGIC_ENCRYPTION_KEY` | Adding or updating an Instance or Account credential | A secret key of 32 url-safe base64-encoded bytes |

Generate a key once and keep it in your secret store; losing it makes previously encrypted credentials unrecoverable.

```bash
export LOGIC_ENCRYPTION_KEY="$(uv run python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())')"
```

`config.yaml` is Logic's reserved configuration record. It is empty because Logic declares no file-based configuration.

## Use

A consumer imports the root, selects a Service, calls an Action, and reads the outcome. The same exchange serves every consumer, whether an API process, a command-line entry point, or another Component.

1. Import `Entity` and `Storage` from `logic.interface`.
2. Select a Child Service from `Entity`, or use an Action of `Storage` directly.
3. Call the Action; the result is the Action's own declared result, with no wrapper.

The two routes reach the same data:

```python
from logic.interface import Entity, Storage
from model.interface import Currency

created = Entity.CurrencyService.add(Currency(user_id=1, code="SEK", symbol="kr", country="Sweden"))
print(Storage.storage_get_by_id(Currency, created.id).code)
Entity.CurrencyService.delete(created.id)
```

```text
SEK
```

## Verify

Confirm that a prepared Logic works through its public surface alone. With the Database prepared, this prints the code of the seeded Currency with id 1:

```python
from logic.interface import Entity

print(Entity.CurrencyService.get_by_id(1).code)
```

```text
USD
```

With the runtime value missing, an Action that needs it fails clearly instead of storing an unprotected credential:

```python
import os
from logic.interface import Entity
from model.interface import Instance

os.environ.pop("LOGIC_ENCRYPTION_KEY", None)
try:
    Entity.InstanceService.add(Instance(user_id=1, trading_platform_id=1, name="Docs", password="example-password"))
except ValueError as error:
    print(error)
```

```text
Required runtime value LOGIC_ENCRYPTION_KEY is missing
```

## Troubleshooting

Each situation below reproduces as shown and is corrected as described.

### An Entity is given to the wrong Child Service

Cause: Add and Update accept only an instance of the Child Service's own Entity, and refuse anything else before any request reaches storage.

```python
from logic.interface import Entity
from model.interface import User

try:
    Entity.CurrencyService.add(User(name="Docs", username="docs", password="example-password", api_key="example-key"))
except TypeError as error:
    print(error)
```

```text
CurrencyService accepts only Currency instances, not User
```

Remedy: select the Child Service that matches the Entity.

### A required runtime value is missing or invalid

Cause: `LOGIC_ENCRYPTION_KEY` is not set, or is not 32 url-safe base64-encoded bytes. The message names the value and never contains it.

```python
import os
from logic.interface import Entity
from model.interface import Instance

os.environ["LOGIC_ENCRYPTION_KEY"] = "not-a-key"
try:
    Entity.InstanceService.add(Instance(user_id=1, trading_platform_id=1, name="Docs", password="example-password"))
except ValueError as error:
    print(error)
```

```text
Required runtime value LOGIC_ENCRYPTION_KEY is invalid: expected 32 url-safe base64-encoded bytes
```

Remedy: set the variable to a valid key, as in Setup.

### A credential is duplicated between an Account and its Instance

Cause: an Account password equals the password or `api_key` of its Instance, or an Instance credential equals the password of an Account that uses it.

```python
import os
from cryptography.fernet import Fernet
from logic.interface import Entity
from model.interface import Account, AccountGroup, Instance

os.environ["LOGIC_ENCRYPTION_KEY"] = Fernet.generate_key().decode()
instance = Entity.InstanceService.add(Instance(user_id=1, trading_platform_id=1, name="Docs", password="shared-example"))
group = Entity.AccountGroupService.add(AccountGroup(user_id=1, name="Docs"))
account = Account(name="Docs", group_id=group.id, broker_id=1, instance_id=instance.id, base_currency_id=1, username="docs", password="shared-example", leverage=100, account_type="CFD")
try:
    Entity.AccountService.add(account)
except ValueError as error:
    print(error)
Entity.AccountGroupService.delete(group.id)
Entity.InstanceService.delete(instance.id)
```

```text
An Account password must not duplicate the password or api_key of its Instance
```

Remedy: give the Account a password that differs from every credential of its Instance.

### An Instance cannot be used

Cause: the selected Instance is not reachable, for example a PostgreSQL server that is not running or whose configured role or database does not exist. Database reports its own connection error and Logic passes it on unchanged.

```python
from logic.interface import Entity, Storage

try:
    Entity.CurrencyService.count(instance=Storage.DatabaseInstance.POSTGRESQL)
except Exception as error:
    print("Database refused the request:", type(error).__name__)
```

```text
Database refused the request: OperationalError
```

Remedy: start the server and correct the Instance in Database's configuration, or select an Instance that is reachable.
