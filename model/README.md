# my_model

## Purpose and boundaries

The shared domain Model package for the Trading Assistant. It is the single
logical source of the project's domain entities — their fields, relationships,
domain rules, and initial data — reused by every other application layer
instead of each layer keeping a private copy.

The package owns domain representation and self-contained validation only. It
does not persist data, enforce rules that require stored state (such as
uniqueness across records), perform business behaviour, or expose an API.

## Public interface

An import surface. Every resolved Model is exposed once from the package root:

`User`, `TradingPlatform`, `Instance`, `Currency`, `Broker`, `Asset`,
`AccountGroup`, `Account`, `TrailingGroup`, `TrailingRule`, `PartialGroup`,
`PartialRule`, `ActionGroup`, `Action`, `Position`.

Each Model is a Pydantic model carrying its fields with their types,
optionality, and defaults. Beyond fields, a Model may declare, as class
attributes:

- `relationships` — the Models it conceptually connects to, their cardinality,
  and the field that carries the connection.
- `unique_fields` / `unique_together` — the field or field combinations whose
  values must be unique, enforced by whichever layer holds stored state.
- `credential_fields` / `credential_storage` — which fields carry a credential
  and the at-rest storage mode required for it.
- `domain_rules` — rules that need application or operational context to
  evaluate, stated for Backend Logic to enforce.

Every Model also exposes a module-level `..._INITIAL_DATA` list of the records
that must exist when the project begins, where the current definition declares
any (e.g. `USER_INITIAL_DATA`, `CURRENCY_INITIAL_DATA`). A credential value
awaiting secure generation is marked `"<generate securely>"`; inserting the
record and generating the real value is Database's responsibility.

## Dependencies

- Python (this package's declared `requires-python`)
- [Pydantic](https://docs.pydantic.dev/) for model definition and validation

## Configuration

None. The package has no runtime configuration or secrets of its own.

## Installation and startup

This is a library package, not a running service. A consumer in the same
workspace adds it as a local dependency through its own package manager;
there is no separate process to start.

## Usage examples

```python
from my_model import User, USER_INITIAL_DATA

admin = User(**USER_INITIAL_DATA[0])
print(admin.name, admin.status)
```

```python
from my_model import Account

print(Account.relationships["instance"].target)   # "Instance"
print(Account.unique_together)                    # [("group_id", "broker_id", "instance_id")]
print(Account.credential_storage)                  # {"password": "encrypted"}
```
