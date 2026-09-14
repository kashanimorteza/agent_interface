# model

Model is the shared domain library for the Trading Assistant. It defines the authoritative logical
meaning of every domain concept in the system — users, trading platforms, connection instances,
currencies, brokers, assets, accounts, trailing and partial rules, actions, and positions — as
reusable Domain Definitions.

Model owns domain meaning only. It does not persist data, expose an API, or talk to any trading
platform; those responsibilities belong to the `database`, `backend`, and later platform components.

## Public surface

Every Domain Definition is reachable directly from the top-level package:

```python
from model import (
    Account,
    AccountGroup,
    Action,
    ActionGroup,
    Asset,
    Broker,
    Currency,
    Instance,
    ModelBase,
    PartialGroup,
    PartialRule,
    Position,
    TimezoneAwareDatetime,
    TradingPlatform,
    TrailingGroup,
    TrailingRule,
    UniqueConstraints,
    User,
)
```

`ModelBase` is the shared Model Foundation every Domain Definition builds on: it rejects unknown
fields and re-validates on assignment, so all of them behave consistently.

## Structure

Each Domain Definition lives in its own module (`model.user`, `model.account`, `model.position`, …)
and is a [Pydantic](https://docs.pydantic.dev/) `BaseModel` subclass. Fields, nullability, and
defaults match the Trading Assistant's Target definition exactly.

Three kinds of domain meaning are recorded declaratively rather than enforced here, because
enforcing them is another component's job:

- **Identity** — `id` carries `{"identity": true, "generated": true}` in its JSON Schema. Model does
  not generate identity values; supply one when constructing a Domain Definition.
- **Credential meaning** — fields such as `User.password` or `Instance.api_key` carry
  `{"credential": true}`. Model records that a value is a credential but never chooses how it is
  stored at rest.
- **Uniqueness** — each class exposes `unique_constraints`, a tuple of field-name tuples taken from
  the Target. Deciding whether a set of records violates uniqueness needs records other than the one
  in hand, so Model declares the rule and the persistence layer enforces it.

```python
from model import Account, User

User.unique_constraints
# (('name',),)
Account.unique_constraints
# (('name',), ('group_id', 'broker_id', 'instance_id'))
```

Absolute-instant fields such as `Position.date` require a timezone-aware `datetime`.

## Setup

Requires [uv](https://docs.astral.sh/uv/). From this directory:

```bash
uv sync
```

That creates a `.venv` on Python 3.13 and installs Pydantic 2 plus the development tools (pytest,
ruff, pyright) from `uv.lock`.

## Use

```python
from model import User

admin = User(
    id=1, name="Admin", username="admin", password="<password>", api_key="<api-key>"
)
admin.model_dump()  # -> dict
admin.model_dump_json()  # -> JSON string
User.model_json_schema()  # -> JSON Schema for the Domain Definition
```

Every Domain Definition round-trips through `model_dump_json()` / `model_validate_json()` and
generates a JSON Schema via `model_json_schema()`.

## Verification

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run pyright
```

All four must pass before a change is complete. The suite has one module per Domain Definition,
each checking its fields against the Target, plus Foundation and Public Interface modules.

## Troubleshooting

- **`ValidationError: Extra inputs are not permitted`** — Domain Definitions reject fields the Target
  does not define. Check the field name against that concept's module.
- **`ValidationError` on a numeric field** — monetary and percentage fields use `decimal.Decimal`,
  not `float`, to keep exact precision. Pass a `Decimal` or a numeric string such as
  `Decimal("1.50")`.
- **`ValidationError` on a datetime field** — `Position.date` requires a timezone-aware `datetime`,
  for example `datetime(2026, 1, 1, tzinfo=UTC)`. Naive values are rejected.
- **An `id` is required when constructing a Domain Definition** — identity generation belongs to the
  persistence layer, so Model expects the value to be supplied.
- **A uniqueness rule is not being enforced** — that is deliberate. Read `unique_constraints` and
  enforce it where records are stored.
