# Logic

## Overview

Logic is the Trading Assistant's reusable Behaviour library. It holds the application's Behaviour in modular Services and publishes every Service through one Interface, so a consumer finds each Service in one place and never depends on where a Service lives inside Logic. Logic starts no process, owns no transport schema and depends on no consumer's framework, so any consumer can use it.

This example needs a prepared database (see [Setup](#setup)). It selects the User Child Service of Entity Service, adds a User and lists the Users.

```python
from logic.interface import Entity

users = Entity.Service.User()
user = users.add(
    Entity.Model.User(
        name="Ada", username="ada", password="example-password", api_key="example-key"
    )
)
print(user.id, [stored.username for stored in users.list()])
```

## Interface

Logic Interface (`logic.interface`, contract version 1.1) publishes exactly two names, one for each Service, and nothing else:

| Name | What it is |
|---|---|
| `Entity` | Entity Service's own Interface, as the identical object |
| `Storage` | Storage Service's own Interface, as the identical object |

The package root `logic` publishes nothing: always import from `logic.interface`.

```python
from logic.interface import Entity, Storage

print(Entity.__name__, Storage.__name__)
```

## Services

Each Service owns one coherent responsibility, its own directory and its own Interface. The sections below only point to a Service's own documents; its contract is never copied here.

| Service | Documentation | Definition | Preferences |
|---|---|---|---|
| `Entity` | [README](logic/services/entity/README.md) | [Definition](../.interface/implementation/development/logic/services/entity/entity.md) | [Preferences](../.interface/implementation/development/logic/services/entity/entity.yaml) |
| `Storage` | [README](logic/services/storage/README.md) | [Definition](../.interface/implementation/development/logic/services/storage/storage.md) | [Preferences](../.interface/implementation/development/logic/services/storage/storage.yaml) |

## Setup

Logic needs Python 3.14 or newer and `uv`. It needs the Model and Database Components next to it in the repository (`../model` and `../database`), and a prepared Database.

1. Prepare Database once, from the `database` directory (see its README):

   ```text
   uv sync
   uv run python scripts/prepare.py
   ```

2. Install Logic, from the `logic` directory:

   ```text
   uv sync
   ```

3. To use Logic from another project in this repository, declare it as a local path dependency of that project. `uv` follows Logic's own path sources to Database and Model:

   ```toml
   [project]
   dependencies = ["logic"]

   [tool.uv.sources]
   logic = { path = "../logic", editable = true }
   ```

## Use

A consumer imports Logic Interface, selects a Service, and uses what that Service publishes. Entity Service gives one Child Service for every Entity; Storage Service gives the raw gateway to Database.

```python
from logic.interface import Entity, Storage

currencies = Entity.Service.Currency()
print(currencies.count())

storage = Storage.Storage()
print(storage.count(Entity.Model.Currency, instance=Storage.database_instance.SQLITE))
```

A Service reached this way is a module, so a consumer may also import what it needs directly from a Service's own Interface, as the Service READMEs show.

## Verify

Run this from the `logic` directory. It checks that Logic Interface publishes exactly one entry for every listed Service, that each entry is the identical object of its Service's Interface, and that no Service imports Logic Interface. It prints `verified` when everything holds.

```python
import subprocess
import sys
from pathlib import Path

from logic import interface
from logic.services.entity import interface as entity
from logic.services.storage import interface as storage

services = {"Entity": entity, "Storage": storage}
assert interface.__all__ == list(services)
for name, service in services.items():
    assert getattr(interface, name) is service
for path in Path("logic/services").rglob("*.py"):
    assert "logic.interface" not in path.read_text(), path
for module in ("logic.services.entity.interface", "logic.services.storage.interface"):
    code = f"import sys, {module}; assert 'logic.interface' not in sys.modules"
    subprocess.run([sys.executable, "-c", code], check=True)
print("verified")
```

## Troubleshooting

| Symptom | Cause | Remedy |
|---|---|---|
| `ModuleNotFoundError: No module named 'logic'` (or `database`, or `model`) | The code runs outside an environment that has Logic installed, for example with the system Python | Run it with `uv run` from the `logic` directory, or declare `logic` as a path dependency of your project, as shown in [Setup](#setup). |
| `ImportError: cannot import name 'Entity' from 'logic'` | The package root publishes nothing | Use `from logic.interface import Entity, Storage`. |
| `ExecutionError` containing `no such table` | Database has not been prepared | Run `uv run python scripts/prepare.py` in the `database` directory. |
| `InvalidInputError` with `The entity must be an instance of User` | A Child Service's `add` or `update` received an instance of another Entity | Use the Child Service that matches the Entity, or build the instance from the matching `Entity.Model` entry. |
| `InvalidInputError` with `An entity must be an Entity class imported from Model` | A Storage Action received a string or another value instead of an Entity class | Pass an Entity from `Entity.Model`, or use a Child Service, which supplies its own Entity. |
| `InvalidInputError` with `An id for ... must suit its id Field` from `update` | The instance given to `update` was built by hand and carries no stored identifier | Read the record first (`get_by_id` or `list`), change it, then call `update`. |
| `AttributeError: ... has no attribute 'execute_command'` on a Child Service | The native command Action takes no Entity, so only Storage Service has it | Call `Storage.Storage().execute_command(...)`. |
| `ConfigurationError` raised on the first call | Database's `config.yaml` is invalid or incomplete | Fix the item the error names; Logic never reads or changes Database's configuration. |
