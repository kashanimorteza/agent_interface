# Model

The `model` package is the authoritative logical domain layer of the Trading Assistant. It defines every domain concept — User, Trading Platform, Instance, Currency, Broker, Asset, Account Group, Account, Trailing Group, Trailing Rule, Partial Group, Partial Rule, Action Group, Action, and Position — as one strict, technology-independent Domain Definition, and publishes them through one stable Public Interface.

Model owns domain meaning only. It performs no persistence, transport, presentation, or workflow orchestration; other Components (Database, Logic, API, Presentation) consume Model through this Public Interface.

## Public surface

Every Domain Definition is importable directly from the top-level package:

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
    TradingPlatform,
    TrailingGroup,
    TrailingRule,
    User,
)
```

Each Domain Definition is a strict [Pydantic](https://docs.pydantic.dev/) model built on the shared `ModelBase` foundation (`model.foundation`), which provides:

- **Strict, deterministic validation** — no implicit type coercion, no unrecognized fields (`extra="forbid"`), assignment re-validated.
- **Standard serialization** — `model_dump()`, `model_dump_json()`, and `model_json_schema()` from Pydantic.
- **A metadata-publishing mechanism** — `<DomainDefinition>.persistence_contract()`, which publishes technology-independent, storage-relevant metadata (primary key, auto-increment, uniqueness, nullability, defaults, indexes, foreign keys, relationship cardinality, composite unique sets, and the `persistent` declaration) for the Database Component to consume. Model never maps this to tables, indexes, migrations, or SQL.

Credential fields (`User.password`, `User.api_key`, `Instance.password`, `Instance.api_key`, `Account.password`) publish their required at-rest treatment (`hash` or `encrypted`) through the same contract, under each field's `credential` metadata key.

## Structure

```text
model/
├── src/model/
│   ├── __init__.py          # Public Interface — exports every Domain Definition
│   ├── foundation.py        # ModelBase, persistence_field(), CredentialTreatment
│   ├── user.py, trading_platform.py, instance.py, currency.py, broker.py,
│   ├── asset.py, account_group.py, account.py, trailing_group.py,
│   ├── trailing_rule.py, partial_group.py, partial_rule.py,
│   ├── action_group.py, action.py, position.py   # one Domain Definition each
└── tests/                   # public interface, validation, and serialization checks
```

## Setup

Requires Python 3.14+ and [`uv`](https://docs.astral.sh/uv/).

```bash
cd model
uv sync
```

This creates `.venv/` and installs the runtime dependency (`pydantic>=2,<3`) and the development tools (`pytest`, `ruff`, `pyright`).

## Use

```python
from decimal import Decimal

from model import User

admin = User(
    id=1,
    name="Admin",
    username="admin",
    password="<hashed-value>",
    api_key="<hashed-value>",
)

admin.model_dump()  # -> dict representation
admin.model_dump_json()  # -> JSON string
User.persistence_contract()  # -> technology-independent storage metadata for Database
```

Invalid or incomplete data is rejected at construction time:

```python
User(id="1", name="Admin", username="admin", password="x", api_key="x")
# pydantic.ValidationError: id — Input should be a valid integer (strict mode; no coercion)
```

## Verification

```bash
cd model
uv run pytest      # public interface, validation behavior, serialization/schema generation
uv run ruff check . && uv run ruff format --check .
uv run pyright
```

All three must pass with zero errors before this Component is considered complete.

## Troubleshooting

- **`ValidationError` on construction** — the strict-mode Foundation rejects both missing required fields and any field of the wrong type (e.g. passing a `str` where an `int` Field is declared); supply exact types.
- **`ValidationError: Extra inputs are not permitted`** — every Domain Definition forbids undeclared fields; check the field name against the Domain Definition's declared fields.
- **`uv sync` fails to resolve Python 3.14** — ensure a Python 3.14+ interpreter is discoverable, or let `uv` manage one automatically.

## Active capabilities

- **Error handling** — every Domain Definition raises a structured `pydantic.ValidationError` on invalid domain data instead of silently accepting it.
- **Authentication / Encryption** — credential Fields declare their required at-rest treatment (`hash` or `encrypted`) through `persistence_contract()`, for Database to enforce; Model itself never performs hashing or encryption.
- **Logging** — Model raises structured, catchable errors; it performs no I/O of its own, so logging of those errors is the responsibility of the Component that invokes Model.
