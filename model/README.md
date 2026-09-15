# Model

The independent, reusable Model Component of the Trading Assistant. It defines the authoritative logical meaning of the domain — every Domain Definition, its fields, relationships, and storage-relevant constraints — independently of any persistence, transport, or presentation technology.

## Public surface

Everything a consumer needs is importable from the top-level `model` package:

```python
from model import User, TradingPlatform, Instance, Currency, Broker, Asset
from model import AccountGroup, Account
from model import TrailingGroup, TrailingRule, PartialGroup, PartialRule
from model import ActionGroup, Action, Position
from model import DomainModel, PersistenceContract, FieldContract, RelationshipContract
```

- **15 Domain Definitions** — `User`, `TradingPlatform`, `Instance`, `Currency`, `Broker`, `Asset`, `AccountGroup`, `Account`, `TrailingGroup`, `TrailingRule`, `PartialGroup`, `PartialRule`, `ActionGroup`, `Action`, `Position`. Each is a Pydantic model built on the shared `DomainModel` foundation.
- **Model Foundation** — `DomainModel` gives every Domain Definition validation (via Pydantic), serialization (`model_dump`, `model_dump_json`), and JSON Schema generation (`model_json_schema`) without imposing any field or relationship of its own.
- **Persistence contract** — every Domain Definition publishes technology-independent, storage-relevant metadata for Database to consume, without prescribing tables, indexes, or engine-specific constraints:

```python
contract = User.persistence_contract()
contract.persistent  # True — Database must store User
contract.fields["password"]  # FieldContract(nullable=False, credential="hash", ...)
contract.unique_sets  # composite uniqueness constraints, e.g. (("group_id", "broker_id", "instance_id"),)
contract.relationships  # RelationshipContract entries naming the referenced Domain Definition
```

## Setup

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
cd model
uv sync
```

## Use

```python
from model import User

user = User.model_validate(
    {
        "name": "Ada Trader",
        "username": "ada",
        "password": "a-hashed-value",
        "api_key": "a-hashed-value",
    }
)
user.is_active  # True (declared default)
user.model_dump_json()  # serialize
User.model_json_schema()  # JSON Schema for the public surface
```

Every Domain Definition rejects unknown fields and raises `pydantic.ValidationError` when a required field is missing or a declared constraint (such as `Currency.code` being exactly three characters, or `Position.date` needing to be timezone-aware) is violated.

Credential fields (`User.password`, `User.api_key`, `Instance.password`, `Instance.api_key`, `Account.password`) carry no at-rest treatment themselves — Model only classifies the required treatment (`hash` or `encrypted`) through `persistence_contract()`; Database applies it.

## Verification

```bash
uv run pytest       # 81 tests: construction, validation, persistence-contract metadata, serialization, and schema generation for every Domain Definition
uv run ruff check .
uv run ruff format --check .
uv run pyright
```

## Troubleshooting

- **`pydantic.ValidationError: Extra inputs are not permitted`** — a field not declared by the Target was passed; every Domain Definition rejects unknown fields (`extra="forbid"`).
- **`ValueError: date must be timezone-aware`** — `Position.date` requires a timezone-aware `datetime` (the Target states no exception requiring naive datetimes).
- **Uniqueness or foreign-key violations are not raised by Model** — uniqueness and referenced-record integrity require comparing multiple stored records, which is Database's responsibility; Model only publishes the requirement through `persistence_contract()`.

## Active capabilities

- **Validation** — declarative Pydantic constraints first; the one custom rule (`Position.date` timezone-awareness) exists only because declarative constraints cannot express it.
- **Logging, Error Handling, Authentication, Encryption** — Model is deterministic and performs no I/O (Model Principle 7), so these apply here as: validation failures surface as structured `ValidationError`s (error handling), and credential fields are classified with their required at-rest treatment (`hash` / `encrypted`) for Database and Logic to apply (authentication/encryption). Model itself performs no logging, authentication, or encryption I/O.
