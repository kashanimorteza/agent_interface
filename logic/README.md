# Logic

## Overview

Logic is the reusable library that holds the application's Behaviour in modular Services. It has nothing of its own: its
Interface publishes every Service's Interface under that Service's name, so that a consumer finds every Service in one
place and none depends on where a Service lives inside Logic. Logic starts no process, owns no transport, and depends on no
consumer's framework.

```python
from logic.interface import Entity

users = Entity.User()
print([user.name for user in users.list()])  # ['Admin']
```

## Interface

`logic.interface` publishes exactly these names and nothing else:

| Name | What it is |
|---|---|
| `Entity` | The Entity Service's own Interface: one Child Service for every Model Entity and the contracts they need. |
| `Storage` | The Storage Service's own Interface: the gateway to Database and the Database contracts it republishes. |

Each name is the identical Interface object of its Service, never a copy or wrapper, and `__all__` lists exactly these names.

## Services

- **Entity** — [README](logic/services/entity/README.md), [Definition](../.interface/implementation/development/logic/services/entity/entity.md), [Preferences](../.interface/implementation/development/logic/services/entity/entity.yaml)
- **Storage** — [README](logic/services/storage/README.md), [Definition](../.interface/implementation/development/logic/services/storage/storage.md), [Preferences](../.interface/implementation/development/logic/services/storage/storage.yaml)

A Service's contract lives in its own documentation, Definition, and Preferences, not here.

## Setup

Logic needs Python 3.14 or newer, [uv](https://docs.astral.sh/uv/), and, next to it, the sibling `model` and `database`
projects, which it depends on. Database must be prepared (its Tables and Initial Data) before Logic reads or writes data.

```sh
cd logic
uv sync
(cd ../database && uv run python scripts/prepare.py)
```

`uv sync` creates the isolated environment in `.venv` from `pyproject.toml` and `uv.lock`; run Python in it with `uv run python`.

## Use

Import a Service from the Logic Interface, then use what that Service publishes:

```python
from logic.interface import Entity, Storage
from model.interface import Currency

print(Entity.Currency().count())  # 8
print(Storage.Storage().count(Currency))  # 8
```

Contracts that a Service republishes, such as `Filter` or `InvalidInputError`, are available from that Service's name:

```python
from logic.interface import Entity
from model.interface import User

active = Entity.User().list(
    filters=[Entity.Filter(User.is_active, Entity.FilterOperator.EQUALS, True)]
)
print(len(active))  # 1
```

## Verify

This script checks that the Logic Interface publishes exactly every listed Service. It prints `all checks passed` when every
check holds.

```python
import logic.interface as logic_interface
import logic.services.entity.interface as entity_interface
import logic.services.storage.interface as storage_interface

published = {name for name in vars(logic_interface) if not name.startswith("_")}
assert published == {"Entity", "Storage"} == set(logic_interface.__all__)
assert logic_interface.Entity is entity_interface
assert logic_interface.Storage is storage_interface

print("all checks passed")
```

## Troubleshooting

- **`ModuleNotFoundError: No module named 'model'` (or `database`).** Python is not running in Logic's environment. Run it
  from the `logic` directory with `uv run python`, with the `model` and `database` projects next to it.
- **`ExecutionError` on every read or write, or no data where Initial Data is expected.** Database has not been prepared,
  so its Tables and Initial Data do not exist yet. The error carries only the generic message that the request could not
  be executed or violates a constraint, and the first read also creates Database's empty storage file. Run
  `uv run python scripts/prepare.py` in the `database` directory.
- **`ConfigurationError` saying the Database must run from its own Component.** An installed copy of Database was loaded. Use
  the editable `database` project that `uv sync` links.
- **`InvalidInputError` from a Child Service.** An instance of another Entity was passed to `add` or `update`, or a value does not
  match the Field's Type. Use the Child Service of the Entity you are working with.
- **A name is not found on a Service.** Only the names listed under Interface are published; Base, the Storage gateway inside
  the Entity Service, and Action implementations are internal.
