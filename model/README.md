# Model

The Model Component: the authoritative logical Domain Definitions for the Trading Assistant. It is a pure Python library with no persistence, transport, or workflow logic — only domain identity, fields, relationships, rules, and technology-independent storage-relevant metadata.

## Public surface

Every Domain Definition is exported from the top-level `model` package:

`User`, `TradingPlatform`, `Instance`, `Currency`, `Broker`, `Asset`, `AccountGroup`, `Account`, `TrailingGroup`, `TrailingRule`, `PartialGroup`, `PartialRule`, `ActionGroup`, `Action`, `Position`.

Each Domain Definition is a `pydantic.BaseModel` subclass built on the shared `model.foundation.DomainModel` base, which contributes only validation, serialization, and metadata-publication mechanics — never a Field or relationship.

Every Domain Definition also exposes `<Model>.persistence_metadata()`, a classmethod that publishes its technology-independent storage-relevant metadata: whether it is persistent, and per-field primary-key, generated-identity, uniqueness, index, foreign-key, cardinality, nullability, default, and credential-classification metadata, together with any declared composite uniqueness sets. Database (Phase 2) derives physical storage structure from this output; Model itself never enforces a rule that requires comparing against other stored records.

## Structure

```text
model/
  src/model/
    foundation.py       # DomainModel base + field_meta() helper
    user.py, trading_platform.py, instance.py, currency.py, broker.py,
    asset.py, account_group.py, account.py, trailing_group.py,
    trailing_rule.py, partial_group.py, partial_rule.py,
    action_group.py, action.py, position.py
    __init__.py          # Public Interface (re-exports)
  tests/                 # one test module per Domain Definition
```

## Setup

```bash
cd model
uv sync
```

Requires Python 3.14+ (resolved by `uv` from `.python-version`).

## Use

```python
from model import User

user = User(id=1, name="Admin", username="admin", password="secret", api_key="key")
user.model_dump()  # {'id': 1, 'name': 'Admin', ...}
User.persistence_metadata()  # {'persistent': True, 'fields': {...}, 'unique_sets': [...]}
```

Constructing a Domain Definition with a missing or invalid required Field raises `pydantic.ValidationError`. Model never rejects a value because it duplicates another stored record — single-field and composite uniqueness are published as metadata for Database to enforce.

## Verification

```bash
uv run pytest      # 99 tests: construction, validation, serialization round-trip, published metadata
uv run ruff check . && uv run ruff format --check .
uv run pyright
```

## Credential fields

`User.password`, `User.api_key` are classified `hash`. `Instance.password`, `Instance.api_key`, and `Account.password` are classified `encrypted`. Model never stores or transforms these values itself — it only publishes the declared classification for Database to apply the required at-rest treatment. No credential value appears in this repository or its documentation.

## Troubleshooting

- `ValidationError` on construction: a required Field is missing or has the wrong type — see the exception's field-level detail.
- `Position` rejects a naive `datetime` for `date`: the Target requires timezone-aware absolute instants; pass a `datetime` with `tzinfo` set (canonically UTC).
