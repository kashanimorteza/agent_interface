# Logic

Logic is the reusable library that holds the Trading Assistant's Behaviour in modular Services. It has nothing of its own: its Interface publishes every Service's Interface, unchanged, under that Service's name, so a consumer finds every Service in one place and never depends on where a Service lives inside Logic. Logic is a library: it starts no process and owns no transport.

```python
from logic.interface import Entity

users = Entity.User()
print(users.count())
```

## Interface

`logic.interface` publishes exactly two names, one for each Service Logic lists, each the Service's own Interface (the identical object, never a copy or wrapper):

| Name | What it is |
| --- | --- |
| `Entity` | The Entity Service Interface: one Child Service for every Model Entity, and the contracts a caller needs. |
| `Storage` | The Storage Service Interface: Logic's gateway to Database, and the Database contracts republished. |

Logic Interface defines no Action, wrapper or rule of its own.

## Services

Logic has two fixed Services. This section names them and points to their own documentation and authorities; it does not repeat their contracts.

### Entity

- README: [logic/services/entity/README.md](logic/services/entity/README.md)
- Definition: [Entity Service Definition](../.interface/implementation/development/logic/services/entity/entity.md)
- Preferences: [Entity Service Preferences](../.interface/implementation/development/logic/services/entity/entity.yaml)

### Storage

- README: [logic/services/storage/README.md](logic/services/storage/README.md)
- Definition: [Storage Service Definition](../.interface/implementation/development/logic/services/storage/storage.md)
- Preferences: [Storage Service Preferences](../.interface/implementation/development/logic/services/storage/storage.yaml)

## Setup

Logic requires Python 3.14, [uv](https://docs.astral.sh/uv/), and the Model and Database Components next to it (it declares `../model` and `../database` as editable path dependencies). All dependencies are pinned in `pyproject.toml` and `uv.lock`.

1. Open a terminal in the Component root, the directory that holds `pyproject.toml`.
2. Create the isolated environment and install the pinned dependencies:

   ```bash
   uv sync
   ```

3. Confirm that the Interface loads:

   ```bash
   uv run python -c "import logic.interface"
   ```

Logic works on data that Database holds, so prepare Database once before using the Services. From the Database Component root:

```bash
uv run python -m database.scripts.prepare
```

The development tools are installed by `uv sync`:

```bash
uv run ruff check logic
uv run ruff format --check logic
uv run pyright
```

## Use

Import from `logic.interface` and choose a Service by name.

A Child Service of the Entity Service is selected once and then used without passing the Entity again:

```python
from logic.interface import Entity
from model import interface as model

users = Entity.User()
print([user.name for user in users.list()])
print(Entity.Currency().count(), Entity.Currency().sum(model.Currency.decimal_digits))
```

The Contracts a caller needs (Filters, Orders, enumerations and errors) are republished by the Entity Service, so one import is enough:

```python
from logic.interface import Entity
from model import interface as model

active = Entity.User().list(filters=[Entity.Filter(model.User.is_active, Entity.FilterOperator.EQUALS, True)])
print(len(active))
```

The Storage Service is Logic's route to Database for other Services:

```python
from logic.interface import Storage
from model import interface as model

storage = Storage.Storage()
print(storage.count(model.User))
```

## Verify

This shows that Logic Interface publishes exactly every listed Service, each as the identical Interface object:

```python
import logic.interface as logic
import logic.services.entity.interface as entity
import logic.services.storage.interface as storage

assert sorted(name for name in vars(logic) if not name.startswith("_")) == ["Entity", "Storage"]
assert sorted(logic.__all__) == ["Entity", "Storage"]
assert logic.Entity is entity
assert logic.Storage is storage
```

## Troubleshooting

- **`ModuleNotFoundError: No module named 'model'` or `'database'`.** Logic needs the Model and Database Components beside it, at `../model` and `../database`, and an environment built from the Component root with `uv sync`. Run commands there with `uv run`.
- **`ExecutionError` saying `no such table`.** Database has not been prepared. Run `uv run python -m database.scripts.prepare` from the Database Component root.
- **`InvalidInputError` from a Child Service.** An Entity instance of another kind was passed (for example a `Broker` instance to the `User` Child Service), or a name was given in place of an Entity, a Field reference or an enumeration member. Pass Model values and imported members.
- **`InvalidInputError` or `TypeError` after passing the Entity class to a Child Service Action.** A Child Service is already bound to its Entity, so the class must not be passed again: it lands in the next parameter, which is then refused (`get_by_id(User, 1)` raises `InvalidInputError` because the id must be an integer) or cannot be used (`count(User)` raises `TypeError` because the class is taken for the filters). Call `Entity.User().get_by_id(1)` and `Entity.User().count()`. Only `add` and `update` take an Entity instance; an unknown keyword such as `entity=` raises `TypeError`.
- **`ConfigurationError` saying the configuration cannot be read.** Database is not installed as an editable dependency, so it cannot find its own configuration and storage. Logic declares it that way; keep that declaration when moving the Component.
- **A Service or Child Service name is missing after Model or Database changed.** Logic's Services are generated from Model's Entity Collection and Database's Interface. Generate Logic again after either changes.
