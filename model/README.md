# Model

The Model Component of the Trading Assistant. A Python library publishing the domain's authoritative Domain Definitions — the one shared logical meaning for Trading Assistant data that every other Component reads through this package's Public Interface.

## What this is

Fifteen Domain Definitions (User, Trading Platform, Instance, Currency, Broker, Asset, Account Group, Account, Trailing Group, Trailing Rule, Partial Group, Partial Rule, Action Group, Action, Position), each declaring its Fields, relationships, and rules in one standard, technology-independent vocabulary — type, length/precision, nullability, default, primary key, auto-increment, uniqueness, and relationships. This package realizes that vocabulary with [Pydantic](https://docs.pydantic.dev/) 2.x models; the vocabulary itself is not Pydantic-specific and is published by every Domain Definition through `declaration_vocabulary()`.

Model owns domain meaning only. It has no persistence, no transport, no workflow orchestration, and performs no I/O — later phases (Database, Logic, API, Presentation) build on this package.

## Public Interface

Import every Domain Definition from the package root:

```python
from model import User, Account, Position  # etc.
```

Each Domain Definition is a `DomainModel` (the shared Model Foundation, `model.foundation.DomainModel`) with:

- ordinary Pydantic construction and validation (`User(name=..., username=..., ...)`),
- `.model_dump()` / `.model_dump_json()` for serialization,
- `.model_json_schema()` for schema generation,
- `ClassName.declaration_vocabulary()` — a class method returning this Domain Definition's published vocabulary (`fields`, `unique_sets`, `persistent`) as plain data, for any consumer (Database included) to map to its own technology.

## What Model does and does not enforce

Model validates only **Intrinsic Rules** — conditions decidable from one instance's own data (required fields, value types, format). Per Model's Principles, it never enforces conditions that require comparing against other stored records or external context:

- **Uniqueness** (single-field or composite `unique_sets`) is *declared*, not enforced at construction time — enforcement is Database's responsibility.
- **Referential integrity** (a foreign key referencing a real row) is *declared* via `foreign_key`/`cardinality` metadata, not checked against a database.
- **Instance's Trading Platform-conditional required fields** (which of `ip`/`username`/`password`/`api_key` a given Trading Platform actually needs) depends on external, operation-specific context and is left to the Component that has that context (Logic), not enforced here.

## Setup

```bash
cd model
uv sync
```

## Verification

```bash
uv run ruff format .   # formatting
uv run ruff check .    # linting
uv run pyright         # type checking
```

Model is not in this project's testing-applicability list (`logic` and `api` are), so this package carries no persisted test suite; its behavior was proven with a one-off script during development (construction, required-field rejection, credential classification, vocabulary publication, serialization, and schema generation) and is re-provable the same way after any change.

## Troubleshooting

- **`uv sync` fails to resolve Python** — this package requires Python ≥3.13; run `uv python install 3.13` first.
- **`ValidationError` on construction** — the rejected value violates a Target-declared type, required-field, or format constraint; the error names the offending field.
