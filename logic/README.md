# Logic

## Overview

Logic is the reusable library that holds the Trading Assistant's Services. It has nothing of its own: its Interface publishes every Service under that Service's name, so a consumer finds every Service in one place and never depends on where a Service lives inside Logic. Logic starts no process and owns no transport, so any consumer can use it and it can be tested without a running server.

```python
from logic.interface import Entity

print([currency.code for currency in Entity.Service.Currency().list(limit=3)])
```

## Interface

The Interface is the module `logic.interface`. It publishes exactly one name for every Service and nothing else:

| Name | What it is |
| --- | --- |
| `Entity` | the Interface of Entity Service, the identical object, never a copy or a wrapper |

```python
from logic.interface import Entity

print(Entity.__all__)
```

## Services

Logic has one Service. Each Service has its own directory, its own Interface, and its own Definition and Preferences; the links below lead to them and the contract of a Service is stated there only.

| Service | Name in the Logic Interface | README | Definition | Preferences |
| --- | --- | --- | --- | --- |
| Entity Service | `Entity` | [README](logic/services/entity/README.md) | [Definition](../.interface/implementation/development/logic/services/entity/entity.md) | [Preferences](../.interface/implementation/development/logic/services/entity/entity.yaml) |

## Setup

Logic is a Python library managed with [uv](https://docs.astral.sh/uv/). It needs Python 3.14 or newer and uses the Model and Database libraries of this project as local path dependencies, so the `model` and `database` directories must sit beside the `logic` directory.

1. Open the Logic directory.
2. Install the locked dependencies, Model and Database included, into an isolated environment:

   ```bash
   uv sync
   ```

3. Prepare the Database's default Instance once, from the Database directory, so the tables and the initial data exist:

   ```bash
   cd ../database
   uv run python scripts/prepare.py
   ```

4. Confirm the Interface loads, from the Logic directory:

   ```bash
   uv run python -c "import logic.interface"
   ```

Another Component of this project uses Logic as a local path dependency on this directory, never from a package index, and depends on Model and Database the same way. In the consumer's `pyproject.toml`:

```toml
[project]
dependencies = ["logic", "database", "model"]

[tool.uv.sources]
logic = { path = "../logic" }
database = { path = "../database" }
model = { path = "../model" }
```

## Use

A consumer imports a Service from the Logic Interface by name and reaches everything the Service offers through it. It never imports from a directory inside Logic.

```python
from logic.interface import Entity

users = Entity.Service.User()
print(users.get_by_id(1).username)
print(users.count())
```

Entity Service, and so everything it offers, is described in [its documentation](logic/services/entity/README.md).

## Verify

Run the script below from the Logic directory with `uv run python`. It checks that the Logic Interface publishes exactly one entry for every Service of Logic, under the name of that Service, that each entry is the identical Interface object of its Service, that nothing else is published, that no Service imports the Logic Interface, and that loading opens no connection and creates no file. It prints `Logic verified` when every check holds.

```python
import pathlib
import subprocess
import sys

import logic.interface as interface
import logic.services.entity.interface as entity_interface

SERVICES = {"Entity": entity_interface}

assert interface.__all__ == list(SERVICES)
assert sorted(n for n in vars(interface) if not n.startswith("_")) == sorted(SERVICES)
for name, source in SERVICES.items():
    assert getattr(interface, name) is source, name

package = pathlib.Path(interface.__file__).parent
services = sorted(
    p.name
    for p in (package / "services").iterdir()
    if p.is_dir() and p.name != "__pycache__"
)
assert services == ["entity"]
for source_file in (package / "services").rglob("*.py"):
    text = source_file.read_text()
    assert (
        "logic.interface" not in text and "from logic import interface" not in text
    ), source_file

before = sorted(str(p) for p in package.rglob("*") if "__pycache__" not in p.parts)
check = (
    "import sqlite3, sqlalchemy\n"
    "def refuse(*a, **k):\n"
    "    raise SystemExit('a connection was opened')\n"
    "sqlite3.connect = refuse\n"
    "sqlalchemy.create_engine = refuse\n"
    "import logic.interface\n"
)
subprocess.run([sys.executable, "-c", check], check=True)
after = sorted(str(p) for p in package.rglob("*") if "__pycache__" not in p.parts)
assert before == after

print("Logic verified")
```

## Troubleshooting

**`error: Distribution not found at: file:///.../database` (or `.../model`) when running `uv sync`.** Logic reaches Database and Model as local path dependencies, and the directory it names does not exist beside `logic`. Put the `database` and `model` directories next to the `logic` directory, then run `uv sync` again.

**`ModuleNotFoundError: No module named 'logic'` (or `'database'`, or `'model'`).** The script ran in an interpreter outside the Logic environment. Run it from the Logic directory with `uv run python ...`, after `uv sync` has installed the environment.

**`ExecutionError: The SQLite Engine could not complete the operation: no such table: ...` from an Action.** The default Instance has not been prepared, so its tables do not exist. Run `uv run python scripts/prepare.py` from the Database directory, then call the Action again.

**`InvalidInputError` from an Action.** The request holds a string where an imported value is required, a Field of another Entity, or an instance of another Entity given to `add` or `update`. Pass the Entity class attribute for a Field, such as `Entity.Model.Currency.code`, and an instance built from the Child Service's own Entity.

**`AttributeError: type object 'Service' has no attribute ...`.** A Child Service is named exactly like its Entity, without spaces, such as `Entity.Service.TradingPlatform` and not `Entity.Service.Trading_Platform`. List the names with `print([n for n in vars(Entity.Service) if not n.startswith("_")])`.
