# model

The Trading Assistant's shared domain Model. It defines every domain concept
— User, Trading Platform, Instance, Currency, Broker, Asset, Account Group,
Account, Trailing Group, Trailing Rule, Partial Group, Partial Rule, Action
Group, Action, and Position — as one authoritative, technology-independent
Domain Definition, published through one explicit Public Interface.

This package owns domain meaning only: fields, relationships, validation
rules, and persistence-relevant metadata. It does not persist data, does not
seed initial records, and does not implement application behaviour — those
belong to later Components (Database, Logic, API, Presentation).

## Public Interface

Import every Domain Definition directly from `model`:

```python
from model import User, Instance, Account, Position

user = User(name="Admin", username="admin", password="hunter2", api_key="k-123")
```

No other module or attribute is supported for external use; the package's
internal file layout (including the shared `foundation` module) may change
without notice.

## Persistence-relevant metadata

Every Domain Definition publishes technology-independent metadata a future
Database Component can consume — primary keys, auto-increment identity,
uniqueness (including composite uniqueness), nullability, defaults,
relationships (as a referenced Domain Definition and field, not an ORM
mapping), and credential treatment (`hash` or `encrypted`). Read it with:

```python
from model import User
from model.foundation import persistence_contract

contract = persistence_contract(User)
print(contract.persistent)     # True
print(contract.unique_sets)    # (("name",)-style constraints reported per model)
for field in contract.fields:
    print(field.name, field.meta)
```

This is documentation-only metadata: it never contains SQL, an ORM mapping,
or an Engine-specific detail.

## Known documented (not enforced) rules

Two Target rules span more than one Domain Definition's own data and are
therefore not Intrinsic Rules — they are documented on the relevant class
rather than enforced by Model, since enforcing them would require comparing
stored records or external, currently-unspecified per-platform data:

- **Instance**: the selected Trading Platform determines which connection
  fields (`ip`, `username`, `password`, `api_key`) are required. Model does
  not evaluate this because Model preserves only the fields' own presence
  semantics.
- **Account**: `password` must not duplicate the associated Instance's
  credential unless the selected Trading Platform explicitly requires it in
  both roles.

A later Component with access to the related stored records is the correct
place to enforce both rules.

## Setup

```bash
cd model
uv sync
```

## Use

```bash
uv run python -c "from model import User; print(User(name='Admin', username='admin', password='x', api_key='y'))"
```

## Verification

```bash
uv run ruff format .
uv run ruff check .
uv run pyright
uv run pytest
```

All four must pass with no errors before a change to this package is
considered complete.

## Troubleshooting

- **`ValidationError` on construction**: a required field is missing, or a
  value violates a declared constraint (for example `Currency.code` must be
  exactly 3 characters, and `Position.date` must be timezone-aware).
- **`pyright` reports an unknown import**: run `uv sync` so the `model`
  package and its dependencies are installed into `.venv`.
