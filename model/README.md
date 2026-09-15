# Model

The shared domain Model for the Trading Assistant Target. Model owns the authoritative logical
meaning of the domain: every Domain Definition's fields, relationships, rules, and
persistence-relevant metadata, independent of any storage, transport, or presentation technology.

## Public surface

Everything a consumer needs is importable from the `model` package root:

```python
from model import User, TradingPlatform, Instance, Currency, Broker, Asset, AccountGroup, \
    Account, TrailingGroup, TrailingRule, PartialGroup, PartialRule, ActionGroup, Action, \
    Position, DomainModel, ForeignKey, Credential
```

- **15 Domain Definitions** — `User`, `TradingPlatform`, `Instance`, `Currency`, `Broker`,
  `Asset`, `AccountGroup`, `Account`, `TrailingGroup`, `TrailingRule`, `PartialGroup`,
  `PartialRule`, `ActionGroup`, `Action`, `Position` — each a `pydantic.BaseModel` subclass
  built on the shared `DomainModel` foundation (`model.foundation`).
- **`DomainModel`** — the Model Foundation every Domain Definition builds on. Provides
  strict validation, JSON serialization/schema generation, and
  `persistence_metadata()`, a classmethod publishing technology-independent storage-relevant
  metadata (primary key, auto-increment, uniqueness, composite uniqueness, nullability,
  defaults, foreign keys, cardinality, and required credential treatment) for the Database
  Component to consume.
- **`ForeignKey`** and **`Credential`** — supporting types used by that metadata.

## Structure

```text
model/
├── src/model/          # the package: foundation.py + one module per Domain Definition
├── tests/               # pytest suite: public interface, validation, serialization, metadata
└── pyproject.toml
```

## Setup

```bash
cd model
uv sync
```

Installs the package (editable) and its dev dependencies (`pytest`, `ruff`, `pyright`) into
`.venv`.

## Use

```python
from model import User

admin = User(
    id=1,
    name="Admin",
    username="admin",
    password="hashed-or-plaintext-input",  # Database applies the declared hash treatment
    api_key="hashed-or-plaintext-input",
)

admin.model_dump()          # dict representation
admin.model_dump_json()     # JSON representation
User.model_json_schema()    # JSON Schema for the Domain Definition
User.persistence_metadata() # technology-independent persistence metadata for Database
```

Every Domain Definition rejects construction with a missing required field, an undeclared
field, or data that violates a declared constraint (for example, `Currency.code` longer than
3 characters, or `Position.date` without timezone information).

## Verification

```bash
uv run pytest      # behavior: public interface, validation, serialization, persistence metadata
uv run ruff check src tests
uv run ruff format --check src tests
uv run pyright
```

## Conventions applied

- Modern Python typing (`str | None`, built-in generics).
- `Decimal` for every exact monetary or ratio value; `float` only where the Target explicitly
  declares a `float` field.
- Timezone-aware `datetime` for absolute instants (`Position.date`), validated at construction.
- Credential fields (`password`, `api_key`) carry their Target-declared at-rest treatment
  (`hash` or `encrypted`) as metadata; Model never stores a raw credential's treatment decision
  anywhere but this metadata, and never applies the hashing or encryption itself — that
  enforcement belongs to Database.

## Troubleshooting

- **`ValidationError: extra fields not permitted`** — the Domain Definition rejects any field
  not declared by the Target; remove the unexpected key from the input data.
- **`ValidationError` on a credential or numeric field** — construction is strict; coerce the
  value to the declared type (for example, pass a `Decimal`, not a `float`, for a decimal
  field) before constructing the Domain Definition.
