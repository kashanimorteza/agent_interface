# Logic

## Overview

Logic is the application's reusable library of Services. It has nothing of its own: its Interface publishes the
Interface of every Service under that Service's name, so a consumer imports Logic Interface, selects a Service, and
uses what that Service publishes. Logic starts no process, owns no transport, and depends on no consumer's
framework. Entity Service gives every Entity that Model publishes its own Child Service, and Storage Service is the
only route to Database.

```python
from logic.interface import Entity, Storage

Storage.Storage().prepare()  # the Database storage must hold its Tables and Initial Data
print(Entity.Service.User().get_by_id(1).name)  # Admin
```

## Interface

`logic.interface` publishes exactly one entry for every Service Logic lists, each the Service's own Interface and
never a copy or wrapper, and nothing else.

| Name | What it is |
|---|---|
| `Entity` | The Entity Service Interface: the groups `Service`, `Model`, `Parameter`, and `Error`. |
| `Storage` | The Storage Service Interface: the gateway `Storage` and the Database contracts it republishes. |

## Services

| Service | Documentation | Definition | Preferences |
|---|---|---|---|
| `Entity` | [README](logic/services/entity/README.md) | [Definition](../.interface/implementation/development/logic/services/entity/entity.md) | [Preferences](../.interface/implementation/development/logic/services/entity/entity.yaml) |
| `Storage` | [README](logic/services/storage/README.md) | [Definition](../.interface/implementation/development/logic/services/storage/storage.md) | [Preferences](../.interface/implementation/development/logic/services/storage/storage.yaml) |

## Setup

Requirements: Python 3.14 or newer, [uv](https://docs.astral.sh/uv/), and the sibling `database` and `model`
projects, which Logic depends on. The `database` project depends on `model` as well.

```sh
cd logic
uv sync
```

`uv sync` creates the isolated environment in `.venv` from `pyproject.toml` and `uv.lock`, with Database and Model
installed from their sibling directories. Run Python in it with `uv run python`. Logic stores no data: the
Database storage must hold its Tables and Initial Data before the first request, which `Storage.Storage().prepare()`
does once and repeating it changes nothing.

## Use

A consumer imports from `logic.interface` only, selects a Service, and uses what it publishes:

```python
from logic.interface import Entity

currencies = Entity.Service.Currency()
print(currencies.count())  # 8
parameter, model = Entity.Parameter, Entity.Model
is_usd = parameter.Filter(model.Currency.code, parameter.FilterOperator.EQUALS, "USD")
print(currencies.list([is_usd])[0].symbol)  # $
```

Storage Service takes the Entity on every request, and a Child Service binds it once:

```python
from logic.interface import Storage
from model.interface import Currency

print(Storage.Storage().count(Currency))  # 8
```

## Verify

Run this script from the Logic directory with `uv run python`. It checks that Logic Interface publishes exactly one
entry for every Service directory, each the identical Interface of that Service, that no Service imports Logic
Interface, that only Storage Service imports Database, and that importing Logic Interface starts no process and
opens no connection. It prints `all checks passed` when every check holds.

```python
import ast
import subprocess
import sys
from importlib import import_module
from pathlib import Path

import logic.interface as interface

root = Path(interface.__file__).parent / "services"
services = sorted(
    path.name for path in root.iterdir() if path.is_dir() and path.name != "__pycache__"
)
assert sorted(interface.__all__) == sorted(name.capitalize() for name in services)
assert sorted(name for name in vars(interface) if not name.startswith("_")) == sorted(
    interface.__all__
)
for directory in services:
    assert getattr(interface, directory.capitalize()) is import_module(
        f"logic.services.{directory}.interface"
    )

for source in root.rglob("*.py"):
    modules = []
    for node in ast.walk(ast.parse(source.read_text())):
        if isinstance(node, ast.ImportFrom) and node.level == 0:
            modules.append(node.module or "")
        elif isinstance(node, ast.Import):
            modules += [alias.name for alias in node.names]
    assert "logic.interface" not in modules and "logic" not in modules, source
    if source.relative_to(root).parts[0] != "storage":
        assert not any(module.split(".")[0] == "database" for module in modules), source

probe = """
import sys
events = []
sys.addaudithook(lambda event, args: events.append(event) if event in ("socket.connect", "subprocess.Popen", "sqlite3.connect") else None)
import logic.interface
sys.exit(1 if events else 0)
"""
assert subprocess.run([sys.executable, "-c", probe], check=False).returncode == 0

print("all checks passed")
```

## Troubleshooting

- **`ModuleNotFoundError: No module named 'model'`** (or `'database'`): Python ran outside the project
  environment. Run `uv run python` from the Logic directory after `uv sync`, with the `database` and `model` projects
  next to it.
- **`ExecutionError: The request could not be executed or violates a constraint`** on the first request: the
  Database storage has no Tables yet. Run `Storage.Storage().prepare()` once. The same error is also raised for a
  record that violates a constraint, such as an owner that does not exist.
- **`InvalidInputError: Expected an instance of Broker`**: an Action of the Broker Child Service was given an
  instance of another Entity. Give it a `Entity.Model.Broker`, or select the Child Service of the Entity you have.
- **`InvalidInputError: The Entity must be an Entity imported from Model`**: a Storage Action received the Entity's
  name as text. Pass the Entity itself, for example `Entity.Model.Currency` or `Currency` from Model.
- **`InvalidInputError: Every filter must be a Filter value`**: a filter was given as a Field or text. Build it with
  `Entity.Parameter.Filter(field, operator, value)`.
- **`ImportError: cannot import name 'User' from 'logic.interface'`**: Logic publishes Services, not their members.
  Import the Service and select the member: `from logic.interface import Entity`, then `Entity.Service.User`.
