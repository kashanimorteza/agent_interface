# Logic

## Overview

Logic is the reusable library that holds the application's Behavior in modular Services. It has nothing of its own: its Interface publishes every Service's Interface under that Service's name, so a consumer finds every Service in one place and never depends on where a Service lives inside Logic.

```python
from logic.interface import Entity

print(Entity.Service.User().get_by_id(1).username)
```

## Interface

Logic Interface publishes exactly one name for every Service listed for Logic, and nothing else. It is the identical Interface object of that Service, never a copy, wrapper or added Action.

| Name | Service | What it is |
| --- | --- | --- |
| `Entity` | Entity Service | the Interface of the Entity Service |

```python
from logic.interface import Entity

print(sorted(Entity.__all__))
```

## Services

Every Service owns one coherent responsibility, its own directory and its own Interface, Definition and Preferences. Their contracts live there and are not copied here.

| Service | Documentation | Definition | Preferences |
| --- | --- | --- | --- |
| Entity | [README](logic/services/entity/README.md) | [Definition](../.interface/implementation/development/logic/services/entity/entity.md) | [Preferences](../.interface/implementation/development/logic/services/entity/entity.yaml) |

For Logic as a whole see its [Definition](../.interface/implementation/development/logic/logic.md) and [Preferences](../.interface/implementation/development/logic/logic.yaml).

## Setup

Logic is a Python library managed with [uv](https://docs.astral.sh/uv/). It needs Python 3.14 or newer, and it needs the Model and Database libraries of this project next to it, because it uses both as local path dependencies.

1. Open the Logic directory.
2. Install the locked dependencies, Model and Database included, into an isolated environment:

   ```bash
   uv sync
   ```

3. Prepare Database storage once, from the Database directory (Logic never prepares it):

   ```bash
   uv run python scripts/prepare.py
   ```

4. Confirm the Interface loads:

   ```bash
   uv run python -c "import logic.interface"
   ```

Another Component of this project uses Logic as a local path dependency on this directory, never from a package index. In the consumer's `pyproject.toml`:

```toml
[project]
dependencies = ["logic", "database", "model"]

[tool.uv.sources]
logic = { path = "../logic" }
database = { path = "../database" }
model = { path = "../model" }
```

## Use

A consumer imports a Service by the name Logic Interface publishes and uses what that Service publishes. Logic starts no process, owns no transport schema and depends on no consumer's framework.

```python
from logic.interface import Entity

currencies = Entity.Service.Currency()
value = Entity.database_value
usd = currencies.list(
    [value.Filter(Entity.Model.Currency.code, value.FilterOperator.EQUALS, "USD")]
)
print([currency.code for currency in usd])
```

## Verify

Run the script below with `uv run python` from the Logic directory. It checks that Logic Interface publishes exactly one entry for every listed Service, under its configured name, and nothing else; that each entry is the identical Interface object of its Service; that no Service imports Logic Interface; that only Entity Service imports Database Interface; and that no two Services share a name or directory. It prints `Logic verified` when every check holds.

```python
import ast
from pathlib import Path

import logic.interface as interface
import logic.services.entity.interface as entity

SERVICES = {"Entity": "entity"}

assert (
    sorted(n for n in vars(interface) if not n.startswith("_"))
    == sorted(SERVICES)
    == sorted(interface.__all__)
)
assert interface.Entity is entity

package = Path(interface.__file__).parent
directories = sorted(
    p.name
    for p in (package / "services").iterdir()
    if p.is_dir() and p.name != "__pycache__"
)
assert directories == sorted(SERVICES.values()) and len(set(directories)) == len(
    directories
)


def imported(path):
    names = set()
    for node in ast.walk(ast.parse(path.read_text())):
        if isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
        elif isinstance(node, ast.Import):
            names |= {alias.name for alias in node.names}
    return names


for path in (package / "services").rglob("*.py"):
    assert "logic.interface" not in imported(path), path
    if "database" in {n.split(".")[0] for n in imported(path)}:
        assert path.parts[-3:-1] == ("services", "entity"), path

print("Logic verified")
```

## Troubleshooting

- **`ModuleNotFoundError: No module named 'logic'`** — the library is not installed in the interpreter you are using. Run commands through `uv run` inside the Logic directory, or declare Logic as a local path dependency in the consumer.
- **`ModuleNotFoundError: No module named 'model'` or `'database'`** — Logic needs both libraries as local path dependencies; run `uv sync` in the Logic directory with the Model and Database directories next to it.
- **`ConnectionFailureError` or an empty result on the first call** — Database storage has not been prepared. Prepare it from the Database directory (see Setup).
- **`InvalidInputError` when calling an Action** — a string was passed where an imported value is required, a Field belongs to another Entity, or an `add` or `update` received an instance of another Entity than the Child Service binds. Use `Entity.Model.<Name>` and the `Entity.database_value` members.
- **`TypeError` about a missing or unexpected argument** — an Action takes the parameters of its Database Operation without the Entity class; read its signature in the Entity Service documentation.
- **A name is missing from the Interface** — Logic publishes only `Entity`; reach everything else through it.
