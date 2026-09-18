# model

The Model Component: the shared domain language of the Trading Assistant. It defines one authoritative Domain Definition for every domain concept the Target declares — identity, trading infrastructure, accounts, trailing and partial rules, actions, and positions — in a standard, technology-independent vocabulary. Every other Component reads that vocabulary through this package's Public Interface; Database is one consumer of it, deriving physical storage from these declarations without reinterpreting the Target.

## Structure

- `model.foundation` — the shared foundation. `DomainModel` is the base class every Domain Definition subclasses for validation, serialization, and metadata publishing. `domain_field(...)` declares one Field's complete vocabulary (type, length, precision, nullability, default, primary key, auto-increment, uniqueness, index, foreign key, credential treatment). `ForeignKeyDeclaration` and `CredentialDeclaration` are the typed shapes of a relationship and a credential declaration.
- One module per Domain Definition, each exporting one `DomainModel` subclass: `User`, `TradingPlatform`, `Instance`, `Currency`, `Broker`, `Asset`, `AccountGroup`, `Account`, `TrailingGroup`, `TrailingRule`, `PartialGroup`, `PartialRule`, `ActionGroup`, `Action`, `Position`.
- All of the above are re-exported from the package root (`model`), which is the Public Interface — consumers import from `model` rather than reaching into a submodule.

## Setup

From this directory:

```bash
uv sync
```

This resolves and installs the pinned dependencies (Pydantic 2.x) into a project-local `.venv`, using the `uv.lock` lockfile.

## Run

`model` is a library, not an executable; there is no process to start. Import it from a consuming Component's own code:

```python
from model import User

admin = User(name="Admin", username="admin", password="...", api_key="...")
```

## Capabilities

**Construct a Domain Definition with valid data.** Required fields must be provided; a field the Target leaves nullable without a stated default may be omitted and defaults to `None`; an auto-increment identity is absent (`None`) until persistence assigns it.

```python
from model import Broker

broker = Broker(name="FxPro", user_id=1)
assert broker.id is None  # not yet persisted
```

**Invalid data is rejected deterministically**, with no partial construction:

```python
from pydantic import ValidationError
from model import TradingPlatform

try:
    TradingPlatform(name="MetaTrader 5")  # missing required `code`
except ValidationError:
    ...  # rejected
```

**Publish a Domain Definition's complete declaration vocabulary** — every Component's route to type, nullability, defaults, identity, uniqueness, foreign keys, and credential treatment, without a second schema artifact:

```python
from model import Instance

Instance.declaration()
# {
#   "persistent": True,
#   "unique_sets": [["user_id", "name"]],
#   "fields": {
#     "user_id": {"type": "integer", "nullable": False, ...,
#                 "foreign_key": {"references": "User", "field": "id",
#                                 "cardinality": "many_to_one", "optional": False}},
#     "password": {"type": "string", "nullable": True, ...,
#                  "credential": {"classification": "credential", "treatment": "encrypted"}},
#     ...
#   },
# }
```

**Serialize a Domain Definition** through Pydantic's standard mechanism, inherited from the Foundation:

```python
broker.model_dump()       # dict
broker.model_dump_json()  # JSON string
```

## Verify

There is no persisted test suite in this Component — Development Preferences activate the shared testing capability only for `logic` and `api`, so Model's checks are run transiently and leave nothing behind. To re-run the same checks this Component was verified with:

```bash
uv run ruff format --check src   # formatting
uv run ruff check src            # linting
uv run pyright src               # type-checking
```

Behavioral checks — construction, rejection, declaration output, serialization — were run the same way, as one-off `uv run python -c "..."` scripts, and are not stored in this Component.

## Troubleshooting

- **A field rejects a value you expected it to accept.** Validation is strict (`model_config = ConfigDict(strict=True, ...)`): a `str` is never silently coerced from an `int`, for example. Pass the exact declared type.
- **A construction call raises for a missing field you expected to be optional.** Only a field the Target declares with a stated `Default`, or one the Target declares `Nullable: true` with no stated default, is optional. A `Nullable: false` field with no stated default is always required — Model never invents a default the Target does not state.
- **Uniqueness or cross-field rules aren't enforced here.** Model declares `unique` and `unique_sets` metadata but does not enforce them — enforcement over persisted records belongs to Database, per Model's separation from persistence concerns.
