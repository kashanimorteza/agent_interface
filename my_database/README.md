# my_database

Reusable persistence library for the Trading Assistant. It stores the Entities published by `my_model` and gives Logic one standard set of data Operations, so no other Component needs to know how or where the data is stored.

## Overview

Database has three public layers:

```text
Interface  →  Mapping  →  Engine
```

- **Interface** (`my_database.interface.Interface`) is the standard entry point. Logic calls one of its Operations with an imported Entity class or an Entity instance and receives a `Result`.
- **Mapping** (`my_database.mapping.Mapping`) resolves which Database Instance and Engine serve the request, forwards it to that Engine, and returns the answer in the standard form.
- **Engine** (`my_database.engine.SqliteEngine`) carries out the Operation against its own storage technology. Each declared Engine has its own isolated implementation.

Every layer is public; use `Interface` unless you need to reach a layer directly.

A request travels from Interface to Mapping to the Engine of its Database Instance. A Database Instance is a named storage declared in the Database Configuration (`database.yaml`); a request that names none uses the default Database Instance, and a request that names an undeclared one is refused with a failure result.

Every Operation answers with a `Result` holding an `outcome` (`success`, `not_found`, or `failure`), the `value` it returns, and a `message`. A stored credential is never kept in plain form: credentials that Model classifies as hashed or encrypted are protected before they reach storage.

Database imports its Entities from `my_model.interface` and never defines Fields, constraints, relationships, or indexes of its own.

## Interface

`my_database.interface.Interface` publishes ten Operations. Each takes an imported Entity class or an Entity instance directly, never a Model name or identity, and returns a `Result`. Every Operation also accepts a keyword `instance=` naming the Database Instance to use; the default Database Instance is used when it is omitted.

The examples run in order against a prepared Database that holds the initial data (see Setup and Run). Each prints the outcome of its Operation; the comment shows what it prints.

| Operation | Method | Takes | Returns in `value` |
| --- | --- | --- | --- |
| Add | `add(record)` | an Entity instance | the created record |
| Edit | `edit(entity, record_id)` | an Entity class and an identifier | the record's Field values as a `dict` |
| Update | `update(record)` | an Entity instance with `id` and the changed Fields | the updated record |
| List | `list_(entity, filters=None, order_by=())` | an Entity class, optional filters, optional Field ordering | the matching records |
| Delete | `delete(entity, record_id)` | an Entity class and an identifier | nothing; the `message` states what happened |
| Enable | `enable(entity, record_id)` | an Entity class and an identifier | the enabled record |
| Disable | `disable(entity, record_id)` | an Entity class and an identifier | the disabled record |
| Get by ID | `get_by_id(entity, record_id)` | an Entity class and an identifier | the matching record |
| Report | `report(name, criteria=None)` | a declared report name and its criteria | the report |
| Execute Command | `execute_command(name, parameters=None)` | a declared command name and its parameters | the command's result |

A record that does not exist answers `not_found`; a broken rule (uniqueness, reference, length, required value), an unknown Field, or an undeclared Database Instance answers `failure`. A record that other records still reference is not deleted and answers `failure`.

### Add

Stores a new record from an Entity instance and returns the created record.

```python
from my_database.interface import Interface
from my_model.interface import Currency

interface = Interface()
result = interface.add(Currency(user_id=1, code="SEK", symbol="kr", country="Sweden"))
print(result.outcome.value, result.value.id, result.value.code)
# -> success 9 SEK
```

### Edit

Returns a record's Field values as a `dict` that can be changed and submitted through Update.

```python
from my_database.interface import Interface
from my_model.interface import Currency

interface = Interface()
result = interface.edit(Currency, 9)
print(result.outcome.value, result.value["code"], result.value["is_active"])
# -> success SEK True
```

### Update

Stores the Fields set on an Entity instance onto the record its `id` names; every other Field is left as it is.

```python
from my_database.interface import Interface
from my_model.interface import Currency

interface = Interface()
result = interface.update(Currency(id=9, description="Swedish krona"))
print(result.outcome.value, result.value.description)
# -> success Swedish krona
```

### List

Returns the records of an Entity class. `filters` maps a Field name to the value a record must hold; `order_by` names Fields to order by, and a leading `-` orders descending.

```python
from my_database.interface import Interface
from my_model.interface import Asset

interface = Interface()
result = interface.list_(
    Asset, filters={"category": "Commodity"}, order_by=("-symbol",)
)
print(result.outcome.value, [asset.symbol for asset in result.value])
# -> success ['XAU/USD', 'USOil']
```

### Delete

Removes a record. A missing record and a record that other records still reference both remove nothing, and the message says so.

```python
from my_database.interface import Interface
from my_model.interface import Currency

interface = Interface()
result = interface.delete(Currency, 9)
print(result.outcome.value, result.message)
# -> success Currency 9 was deleted.
```

### Enable

Marks a record active and returns it.

```python
from my_database.interface import Interface
from my_model.interface import Currency

interface = Interface()
result = interface.enable(Currency, 2)
print(result.outcome.value, result.value.is_active)
# -> success True
```

### Disable

Marks a record inactive and returns it.

```python
from my_database.interface import Interface
from my_model.interface import Currency

interface = Interface()
result = interface.disable(Currency, 2)
print(result.outcome.value, result.value.is_active)
# -> success False
```

### Get by ID

Returns one record by identifier, or `not_found`.

```python
from my_database.interface import Interface
from my_model.interface import Currency

interface = Interface()
found = interface.get_by_id(Currency, 1)
missing = interface.get_by_id(Currency, 999)
print(found.outcome.value, found.value.code, missing.outcome.value)
# -> success USD not_found
```

### Report

Produces a declared report. A report is a function that receives a session and the criteria as keyword arguments; declare it once, then request it by name. It need not concern one Model.

```python
from my_database.interface import Interface
from my_model.interface import Currency
from sqlmodel import func, select


def active_currencies(session, active=True):
    return session.exec(
        select(func.count()).select_from(Currency).where(Currency.is_active == active)
    ).one()


interface = Interface()
interface.declare_report("active_currencies", active_currencies)
result = interface.report("active_currencies", {"active": True})
print(result.outcome.value, result.value)
# -> success 7
```

### Execute Command

Runs a declared database command. A command is a function that receives a session and the parameters as keyword arguments; parameters it cannot accept are refused without running it.

```python
from my_database.interface import Interface
from my_model.interface import Broker
from sqlmodel import func, select


def count_records(session, entity):
    return session.exec(select(func.count()).select_from(entity)).one()


interface = Interface()
interface.declare_command("count_records", count_records)
result = interface.execute_command("count_records", {"entity": Broker})
print(result.outcome.value, result.value)
# -> success 1
```

## Setup

Requires Python 3.14 or newer and [uv](https://docs.astral.sh/uv/). Database consumes `my_model`, so both libraries are added to a consumer project.

**1. Make the library available.** From the consumer project's directory:

```bash
uv add /path/to/my_model /path/to/my_database
```

**2. Provide the Database Configuration.** `database.yaml` declares the supported Engines, the named Database Instances, and the Settings (default Database Instance and secret references). Copy the one shipped with the library and adjust it if needed; it holds references to secrets, never their values:

```bash
cp /path/to/my_database/database.yaml .
```

Database reads the configuration from the `MY_DATABASE_CONFIG` variable when it is set, otherwise from `database.yaml` in the working directory. Relative locations inside it (the storage path and the secret file) resolve against the configuration's own directory.

**3. Create the encryption key.** Credentials that Model classifies as encrypted (an Instance's and an Account's `password` and `api_key`) are stored encrypted with a key that the Settings reference as `file:.secrets/encryption.key`. Create it once and keep it out of version control:

```bash
mkdir -p .secrets
uv run python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())" > .secrets/encryption.key
chmod 600 .secrets/encryption.key
```

Losing the key makes encrypted credentials unrecoverable; replacing it makes existing ones unreadable. To read the key from an environment variable instead, change the reference to `env:NAME`.

**4. Prepare the storage.** Apply the migrations from the library's directory, pointing at your configuration:

```bash
cd /path/to/my_database
MY_DATABASE_CONFIG=/path/to/your_project/database.yaml uv run alembic upgrade head
```

This creates one Table for every Model Entity in the default Database Instance. To create them directly instead (`SqliteEngine(...).create_tables()`), bring that storage under migration afterwards with `uv run alembic stamp head`; migration comparison (`uv run alembic check`) needs the storage to be marked as current.

To work on the library itself, install its locked environment from the library directory with `uv sync`, then follow steps 3 and 4 in that directory without setting `MY_DATABASE_CONFIG`.

## Run

Database is a library, so there is no process to start. Once the storage is prepared (see Setup), run your own code through the consumer project's environment (`uv run python your_script.py`).

**Load the initial data.** The Target defines initial records for twelve Entities (a user, the trading platforms, an instance, currencies, a broker, assets, an account group and account, the rule groups, an action group, and an action). Insert them into the default Database Instance from the consumer project's directory:

```bash
uv run python -m my_database.initial_data
```

Each Entity is filled in dependency order, and an Entity whose Table already holds records is left untouched, so the command is safe to repeat. Credentials the Target asks to be generated securely are generated fresh. The Admin user's password and API key are stored hashed and cannot be recovered afterwards, so the command prints them once, and only when it created the user; copy them from that output. The credentials generated for the instance and the account are stored encrypted and are not printed.

**Use the Operations.** With the initial data loaded, work through the Interface (see Interface for every Operation):

```python
from my_database.interface import Interface
from my_model.interface import Currency

interface = Interface()
result = interface.list_(Currency, order_by=("code",))
print([currency.code for currency in result.value])
# -> ['AUD', 'CAD', 'CHF', 'EUR', 'GBP', 'JPY', 'NZD', 'USD']
```

**Check the library's own source.** From the library directory:

```bash
uv run ruff format --check .
uv run ruff check .
uv run pyright
```

## Verify

Two checks confirm that Database works: the stored schema matches the Model, and the initial data is present.

**The schema matches the Model.** From the library directory, compare the storage with the Entity metadata. A correct Database reports that no upgrade operations are needed; any difference (a missing Table, a Field added to or removed from an Entity, a changed type or constraint) is listed and the command exits with an error:

```bash
cd /path/to/my_database
MY_DATABASE_CONFIG=/path/to/your_project/database.yaml uv run alembic check
```

The storage must have been prepared with the migrations, or marked as current with `uv run alembic stamp head` (see Setup).

**The initial data is present.** From the consumer project's directory, count the records of each Entity that has initial data. The script prints one line per Entity and exits with an error when any count differs:

```python
from my_database.interface import Interface
from my_model.interface import (
    Account,
    AccountGroup,
    Action,
    ActionGroup,
    Asset,
    Broker,
    Currency,
    Instance,
    PartialGroup,
    TradingPlatform,
    TrailingGroup,
    User,
)

interface = Interface()
expected = {
    User: 1,
    TradingPlatform: 2,
    Instance: 1,
    Currency: 8,
    Broker: 1,
    Asset: 4,
    AccountGroup: 1,
    Account: 1,
    TrailingGroup: 1,
    PartialGroup: 1,
    ActionGroup: 1,
    Action: 1,
}
wrong = []
for entity, count in expected.items():
    found = len(interface.list_(entity).value)
    print(entity.__name__, found)
    if found != count:
        wrong.append(entity.__name__)
if wrong:
    raise SystemExit(f"Unexpected record counts for: {', '.join(wrong)}")
# -> User 1
# -> TradingPlatform 2
# -> Instance 1
# -> Currency 8
# -> Broker 1
# -> Asset 4
# -> AccountGroup 1
# -> Account 1
# -> TrailingGroup 1
# -> PartialGroup 1
# -> ActionGroup 1
# -> Action 1
```

Run it in your own environment with `uv run python your_script.py`. It reflects the initial data as loaded; records you add or delete later change the counts.

## Troubleshooting

Each problem below shows how it appears and how to resolve it.

**`FileNotFoundError` for `database.yaml`.** Database could not find its configuration. Run your code from the directory that holds `database.yaml`, or point at the file with `MY_DATABASE_CONFIG=/path/to/database.yaml`.

**`FileNotFoundError` for `.secrets/encryption.key`.** A credential that must be stored encrypted (an Instance's or an Account's `password` or `api_key`) was written, or the initial data was loaded, before the key existed. Create the key as shown in Setup, then repeat the command; loading the initial data is safe to repeat and continues where it stopped. If the load stopped after creating the Admin user, the credentials it generated were still printed before the failure: keep them.

**`ConfigurationError` when Database starts.** The configuration breaks a rule: an Instance names an Engine that is not declared, the default Database Instance or an assignment names an Instance that is not declared, or a secret is written as a value instead of a reference such as `file:.secrets/encryption.key` or `env:NAME`. Correct `database.yaml` as the message says.

**A result with outcome `failure` and the message `Database Instance '…' is not declared.`** The request named a Database Instance that `database.yaml` does not declare. Use a declared key, or declare the Instance under `instances`.

**`OperationalError: no such table`.** The storage has not been prepared. Apply the migrations as shown in Setup step 4.

**`Target database is not up to date` from `alembic check`.** The storage was created directly (`create_tables()`), so it carries no migration marker. Run `uv run alembic stamp head` from the library directory, then check again.

**`InvalidToken` when reading an encrypted credential.** The key that Settings reference is not the one the credential was encrypted with, for example after the key file was replaced. Restore the original key. Values that were stored under the lost key cannot be recovered; set the credentials again through Update with their plain values, which are then encrypted under the current key.

**`uv add` reports that the required Python version is not satisfied.** The libraries need Python 3.14 or newer. Install it with `uv python install 3.14` and run `uv add` again.
