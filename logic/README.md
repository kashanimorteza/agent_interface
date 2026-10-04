# Logic

## Overview

Logic is the reusable library that holds the application's Behaviour in modular Services. It has nothing of its own: its Interface publishes every Service's own Interface under that Service's name, so a consumer finds every Service in one place and never depends on where a Service lives inside Logic. It starts no process, owns no transport schema, and depends on no consumer's framework.

```python
from logic.interface import Entity

users = Entity.User()
print(users.count())
```

## Interface

Logic publishes exactly two names from `logic.interface`. Each is the identical Interface object of one Service, never a copy or a wrapper, and Logic adds no Action or rule of its own:

| Name | What it is |
| --- | --- |
| `Entity` | The Entity Service Interface: one Child Service for every Entity of the Model, and the Storage contracts a caller needs. |
| `Storage` | The Storage Service Interface: the gateway to every public Database capability, and the Database contracts a Service needs. |

Importing the Interface opens no connection and creates no data or file.

```python
from logic.interface import Entity, Storage

print(Entity.Currency, Storage.Storage)
```

## Services

Every Service lives in its own directory inside Logic, with its own Interface, documentation, Definition, and Preferences. Each Service's documentation explains its contract; this section never copies it.

| Service | Documentation | Definition | Preferences |
| --- | --- | --- | --- |
| Entity | [Entity Service documentation](logic/services/entity/README.md) | [Entity Service Definition](../.interface/implementation/development/logic/services/entity/entity.md) | [Entity Service Preferences](../.interface/implementation/development/logic/services/entity/entity.yaml) |
| Storage | [Storage Service documentation](logic/services/storage/README.md) | [Storage Service Definition](../.interface/implementation/development/logic/services/storage/storage.md) | [Storage Service Preferences](../.interface/implementation/development/logic/services/storage/storage.yaml) |

Logic's own [Definition](../.interface/implementation/development/logic/logic.md) and [Preferences](../.interface/implementation/development/logic/logic.yaml) govern the library as a whole.

## Setup

Logic needs Python 3.14 or newer, the package manager `uv`, and two sibling libraries beside it: the Model (`../model`) and the Database (`../database`). Logic reaches both through their public Interfaces only.

1. From the Logic directory, create the isolated environment from the recorded dependency resolution:

   ```text
   uv sync --locked
   ```

   This installs Logic, the Model, the Database, and their dependencies at the versions in `uv.lock`.

2. Make sure the Database has been prepared, so its Tables and Initial Data exist. The Database documentation explains how, and a prepared default Instance is already present when the project has been generated.

3. Check that Logic loads and can reach the Database:

   ```text
   uv run python -c "from logic.interface import Entity; print(Entity.Currency().count())"
   ```

Nothing here starts a process or changes any data.

## Use

Import the Services from `logic.interface`, select a Service, and use what it publishes:

```python
import model
from logic.interface import Entity, Storage

currencies = Entity.Currency()
print(currencies.count())

gateway = Storage.Storage()
print(gateway.count(model.Currency))
```

Select an Entity once by creating its Child Service from the Entity Service, then call its Actions; the Entity is never passed again. Use the Storage Service when a Service needs a Database capability that takes no Entity, such as a native command or a Lifecycle Command. The contracts a caller needs to build requests and catch errors are published by both Services as the identical Database objects, so a caller never imports Database directly:

```python
from logic.interface import Entity

try:
    Entity.Currency().count(instance="sqlite")
except Entity.InvalidInputError as error:
    print(error)
```

Only Storage Service uses the Database; every other Service reaches it through Storage. No Service imports `logic.interface`; a Service that collaborates with another imports that Service's own Interface directly.

## Verify

Logic is conformant when its Interface publishes exactly one entry for every Service in its Service list (Entity and Storage), under the configured name, and each entry is the identical Interface object of its Service. This script prints `True` for each observation:

```python
from logic import interface as logic_interface
from logic.services.entity import interface as entity_interface
from logic.services.storage import interface as storage_interface

published = sorted(name for name in dir(logic_interface) if not name.startswith("_"))
print(published == sorted(logic_interface.__all__) == ["Entity", "Storage"])
print(logic_interface.Entity is entity_interface)
print(logic_interface.Storage is storage_interface)
```

The dependency rules can be observed from the source. This script prints `True` when no Service imports the Logic Interface and no Service other than Storage imports the Database:

```python
import ast
from pathlib import Path

import logic

services = Path(logic.__file__).parent / "services"


def imported(path: Path) -> set[str]:
    names = set()
    for node in ast.walk(ast.parse(path.read_text())):
        if isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
        elif isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
    return names


sources = {path: imported(path) for path in services.rglob("*.py")}
print(
    not any(name == "logic.interface" for names in sources.values() for name in names)
)
print(
    not any(
        name.split(".")[0] == "database"
        for path, names in sources.items()
        if "storage" not in path.relative_to(services).parts
        for name in names
    )
)
```

Every Service has its own name and its own directory under `logic/services`, and loading the Interface opens no connection and creates no data or file.

## Troubleshooting

### `ModuleNotFoundError` for `model` or `database`

Logic reaches the Model and the Database as installed libraries. The error means the environment was not built from Logic's lockfile, or the sibling `../model` and `../database` libraries are missing. Run `uv sync --locked` from the Logic directory and make sure both siblings exist beside it.

### `ImportError: cannot import name 'Entity' from 'logic'`

The package root publishes nothing. Import the Services from the Interface: `from logic.interface import Entity, Storage`.

### `ExecutionError: The operation failed (OperationalError).` on the first call

The Database has not been prepared, so its Tables do not exist. Prepare it once and call again:

```python
from logic.interface import Storage

print(Storage.Storage().prepare().success)
```

### `InvalidInputError: An instance of <Entity> is required.`

A Child Service accepts only instances of the Entity it is bound to. `Entity.Currency().add(...)` needs a Model `Currency`, not a `Broker` or any other object. Create the Child Service of the Entity you are working with.

### `InvalidInputError: An Instance must be passed as the imported value, never as text.`

Pass a `DatabaseInstance` member, not its name as text: `Entity.DatabaseInstance.SQLITE`, never `"sqlite"`. Leave the Instance out to use the default Instance.

### `ExecutionError: The operation failed (IntegrityError).`

The Database refused the request and changed nothing, for example when deleting a record that another record refers to, or adding one that breaks a uniqueness rule. Remove or change the referring records first, or adjust the new record.

### `ConfigurationError`

The Database's own configuration could not be read or an Instance is invalid. Logic neither reads nor changes it; fix the Database's configuration as its own documentation explains.
