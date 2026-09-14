# model

The shared domain Model of the Trading Assistant. This library is the Model Component of the
Target's layered architecture: it defines the authoritative logical meaning of every domain
concept (User, Trading Platform, Instance, Currency, Broker, Asset, Account Group, Account,
Trailing Group, Trailing Rule, Partial Group, Partial Rule, Action Group, Action, Position) and
owns nothing else — no persistence, no transport, no presentation.

## Public surface

Every Domain Definition is exported at package level:

```python
from model import User, TradingPlatform, Broker, Instance, Currency, Asset
from model import AccountGroup, Account, TrailingGroup, TrailingRule
from model import PartialGroup, PartialRule, ActionGroup, Action, Position
```

Each Domain Definition is a `pydantic.BaseModel` built through the shared `ModelFoundation`
(`model.foundation.ModelFoundation`), which every concrete Domain Definition receives its common
configuration and behaviour through without redeclaring it:

- **Strict**: an unknown field is rejected (`extra="forbid"`).
- **Exact decimal**: a Field explicitly typed `decimal` in the Target uses `model.ExactDecimal`
  (`Annotated[decimal.Decimal, ...]`), which accepts `int`, `str`, or `Decimal` but rejects
  `float` — float-to-Decimal coercion can silently hide invalid domain data.
- **Timezone-aware UTC**: an absolute-instant Field (e.g. `Position.date`) uses
  `model.UTCDateTime`, which requires a timezone-aware `datetime` and normalizes it to UTC.
- **Generated identity**: `id` defaults to `None` and is never required at construction — a
  downstream Component (outside Model's boundary) assigns the concrete generated value.
- **Declared credential storage**: `User.credential_storage()`, `Instance.credential_storage()`,
  and `Account.credential_storage()` report each credential Field's storage-at-rest meaning
  (`"hash"` or `"encrypted"`) as stated by the Target. Model records this meaning; it does not
  implement hashing or encryption itself (that remains a persistence concern).
- **Declared Model Operations**: `<DomainDefinition>.model_operations()` reports the shared
  Model Operation vocabulary (`create`, `get_by_id`, `list`, `search`, `update`, `enable`,
  `disable`, `delete`) applicable to that Domain Definition's lifecycle.

## Structure

```text
model/
  src/model/
    foundation.py   # ModelFoundation, ExactDecimal, UTCDateTime, common Field helpers
    <domain>.py      # one module per Domain Definition
    __init__.py      # Public Interface (re-exports)
  tests/
    conftest.py      # shared verification helpers
    test_<domain>.py # one test module per Domain Definition
```

## Setup

```bash
cd model
uv sync
```

## Use

```python
from model import User

admin = User(name="Admin", username="admin", password="…", api_key="…")
admin.model_dump()  # -> dict
admin.model_dump_json()  # -> JSON string
User.model_json_schema()  # -> JSON Schema
User.credential_storage()  # -> {"password": "hash", "api_key": "hash"}
```

Constructing with an unknown field, a missing required field, `null` for a non-nullable field, or
the wrong type raises `pydantic.ValidationError`.

## Verification

```bash
uv run pytest      # 142 tests: public interface, validation behaviour, serialization/schema
uv run ruff check . && uv run ruff format --check .
uv run pyright
```

All three must pass cleanly; this is the phase completion gate for this Component.

## Troubleshooting

- **`pydantic.ValidationError: … Input should be a valid decimal … float …`** — an `ExactDecimal`
  Field received a `float`. Pass an `int`, `str`, or `decimal.Decimal` instead.
- **`pydantic.ValidationError: … tzinfo …`** — a `UTCDateTime` Field received a naive
  `datetime`. Pass a timezone-aware `datetime` (e.g. `datetime.datetime(..., tzinfo=datetime.UTC)`).
- **`pydantic.ValidationError: … Extra inputs are not permitted …`** — an unknown field was
  passed; every Domain Definition rejects fields it does not declare.

## Active capabilities

Logging, error handling, and authentication are **not** active for this Component: the Target's
Development/Scope explicitly excludes them project-wide, overriding Development Preferences'
default applicability. Encryption remains active at the Model boundary only as the declared
credential-storage metadata described above (no cross-cutting testing capability applies to
`model` under Development Preferences; `pytest` here is Development's general Python test
tooling, used to satisfy this Component's own verification requirement).
