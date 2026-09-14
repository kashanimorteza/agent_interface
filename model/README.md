# model

The shared domain Model for the Trading Assistant Target. `model` is a Python library that defines the authoritative, technology-independent Domain Definitions for the system's trading domain — Users, Trading Platforms, Instances, Currencies, Brokers, Assets, Account Groups, Accounts, Trailing/Partial rule sets, Action Groups, Actions, and Positions — and nothing else. It owns no persistence, no Initial Data, and no application workflow; Database, Backend, and other Components consume it through this Public Interface.

## Public Interface

Every Domain Definition is reachable directly from the `model` package — never from a private submodule:

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

Each Domain Definition is a Pydantic `BaseModel` subclass (via the shared `ModelBase` foundation). Unknown fields are rejected, and every field not explicitly provided resolves to its Target-declared default (or `None` when nullable).

## Setup

```bash
cd model
uv sync
```

## Usage

```python
from model import User

user = User(name="Admin", username="admin", password="change-me", api_key="change-me")
user.model_dump()  # dict, with password/api_key masked
user.password.get_secret_value()  # the actual credential value, read explicitly
```

## Conventions (consequential implementation choices)

These choices are not prescribed by the Target; they were made during implementation within Model Principles and are recorded here so a consumer or reviewer can find them without reading the source.

- **Cross-record constraints (uniqueness) are declared, not enforced.** A rule such as "the combination of `user_id` and `name` must be unique" requires comparing against every other persisted record — that is not something one Domain Definition instance can evaluate from its own data, and Model performs no I/O. Each Domain Definition instead declares `unique_together: ClassVar[tuple[tuple[str, ...], ...]]` (inherited from `ModelBase`), e.g. `User.unique_together == (("name",),)`. Database is expected to realize each declared tuple as an actual uniqueness constraint.
- **Credential fields are typed `SecretStr` and marked with their required at-rest storage.** `User.password`, `User.api_key`, `Instance.password`, `Instance.api_key`, and `Account.password` use `pydantic.SecretStr` (so accidental logging or `repr()` never exposes the plaintext value) and carry `json_schema_extra={"credential_storage": "hash" | "encrypted"}` exactly as the Target's Rules state. Model does not perform the hashing or encryption itself — that is a persistence-time concern owned by Database.
- **Two Target-stated rules are out of Model's scope**, per the Plan's recorded constraint: Instance's "the selected Trading Platform defines which connection fields are required" and Account's "Instance and Account credentials must not be duplicated unless the platform requires it in both roles". Both depend on per-platform configuration that no Target field expresses, so they cannot be evaluated from Model's own data. They are expected to be realized by whichever Component implements platform-specific connection logic (Backend / the Trading Platform module), not by Model.
- **Domain Relationships are represented exactly as the Target states them** — as the literal foreign-key id field (e.g. `user_id: int`), not as an embedded object reference — since the Target already pins down that field's name and type explicitly.

## Verification

```bash
uv run pytest       # 38 tests: one Domain Definition's fields/relationships/rules per group, plus Foundation and Public Interface
uv run ruff check .
uv run ruff format --check .
uv run pyright
```

## Scope exclusions

Per the Target's Development section, this Component (like every Component in this Target) has no HTTPS/TLS, authentication/authorization, logging, or custom error-handling machinery. Pydantic's native `ValidationError` is the only error surface.
