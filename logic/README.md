# Logic

## Overview

Logic is the reusable library that holds the application's Behaviour. It has nothing of its own: every capability lives in one of its Services, and `logic.interface` publishes each Service's Interface under that Service's name. Every consumer reaches the application through it.

```python
from logic.interface import Entity

print(Entity.User().count())
```

## Interface

`logic.interface` publishes exactly these names, and nothing else:

| Name | What it is |
|---|---|
| `Entity` | Entity Service Interface |
| `Storage` | Storage Service Interface |

Each name is the Service's own Interface module, not a copy.

## Services

### Entity

One Child Service for every Model Entity. → [README](src/logic/services/entity/README.md) · [Definition](../.interface/implementation/development/logic/services/entity/entity.md) · [Preferences](../.interface/implementation/development/logic/services/entity/entity.yaml)

```python
from logic.interface import Entity
from model import interface as model

admin = Entity.User().add(model.User(name="Admin", ...))
```

### Storage

Logic's gateway to Database. → [README](src/logic/services/storage/README.md) · [Definition](../.interface/implementation/development/logic/services/storage/storage.md) · [Preferences](../.interface/implementation/development/logic/services/storage/storage.yaml)

```python
from logic.interface import Storage

Storage.Storage().prepare()
```

## Setup

Logic is a Python 3.14 library managed with `uv`. It consumes Model and Database, which must sit next to it as the sibling directories `model/` and `database/`. Set Database up first.

```bash
cd database
uv sync
uv run python scripts/prepare.py
cd ../logic
uv sync
```

Logic needs no runtime value. Run every example with `uv run python` from the `logic/` directory.

## Use

A consumer imports a Service from `logic.interface` and uses what that Service publishes:

```python
from logic.interface import Entity
from model import interface as model

active = Entity.Account().list(
    filters=[Entity.Filter(model.Account.is_active, Entity.FilterOperator.EQUALS, True)],
)
```

Inside Logic, one Service imports another Service's Interface directly, never `logic.interface`.

## Verify

```python
import logic.interface as logic
from logic.services.entity import interface as entity
from logic.services.storage import interface as storage

assert logic.__all__ == ["Entity", "Storage"]
assert logic.Entity is entity and logic.Storage is storage
print("Logic Interface publishes exactly every Service")
```

## Troubleshooting

### `ModuleNotFoundError: No module named 'model'` or `'database'`

Model or Database is not installed next to Logic. Make sure `model/` and `database/` are sibling directories and run `uv sync` in `logic/`.

### A Database error on the first call

Database's tables or Initial Data are missing. Run `uv run python scripts/prepare.py` in `database/`, or call `Storage.Storage().prepare()`; repeating it is safe.
