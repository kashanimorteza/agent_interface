# my-model

The shared domain Model package: the single logical definition of every domain Model, its
field declarations, relationships, rules, and initial records. Every other layer works from
these definitions instead of keeping its own copy.

## Purpose and boundaries

`my_model` owns:

- the logical Models and the resolved properties of their fields;
- validation that can be decided from one Model's own data: logical types, nullability,
  declared sizes, defaults, and values awaiting generation;
- declarations of relationships and of rules that need more than one Model's own data;
- the initial records, as declarations bound to their Models.

It does not own, and never performs:

- persistence: storage mapping, constraints, uniqueness across records, existence of
  referenced records, the at-rest transformation of credentials, inserting the initial records,
  and generating their pending values all belong to the Database layer;
- application behaviour and rules that need application context, which belong to Backend
  Logic, and API or presentation shapes, which the consuming layer derives from these Models.

The package has no I/O: validation never reads files, storage, or the network. Consumers use
only the public import interface, `my_model`. Modules whose names start with an underscore are
internal and may change without notice.

## Public interface

Everything below is importable from `my_model`.

### Models

Each Model is a validated class exposed exactly once, in project-definition order:
`User`, `TradingPlatform`, `Currency`, `Broker`, `Asset`, `Instance`, `AccountGroup`, `Account`,
`TrailingGroup`, `TrailingRule`, `PartialGroup`, `PartialRule`, `ActionGroup`, `Action`, and
`Position`. `Model.logical_name` gives the name the project definition uses, such as
`"Trading Platform"`.

`MODELS` is the tuple of all fifteen Model classes in that order.
The function `initial_records` takes a Model class and returns fresh copies of its declared
initial records, in declared order: an empty tuple when it declares none, and `TypeError` for
anything that is not one of these Models.

Every Model derives from `DomainModel` and offers:

| Member | Returns |
| --- | --- |
| `field_declarations()` | each field's resolved `FieldDeclaration`, in declared order |
| `credential_fields()` | the declarations of the fields that are credentials |
| `relationship_declarations()` | every declared `Relationship` |
| `relationship_for()` | the `Relationship` carried by a field, or `None` |
| `rule_declarations()` | every `RuleDeclaration` its own validation does not evaluate |
| `pending_fields()` | on a record, the fields whose values await generation |
| `is_complete()` | on a record, whether no field still awaits generation |

Records validate on construction and on assignment, and reject undeclared fields.
`model_fields_set` tells an omitted field from an explicit null, and `model_dump()`,
`model_dump_json()`, `model_validate()`, and `model_validate_json()` round-trip a record,
including pending values.

### Declarations

- `FieldDeclaration` has these properties: `logical_type` (a `LogicalType`), `nullable`,
  `primary_key`, `auto_increment`, `unique`, `default`, `size`, `credential`, `at_rest` (an
  `AtRestMode`), `generation` (a `GenerationMethod`), and `purpose`. A property the definition
  neither states nor inherits from a default is `NOT_DECLARED`, which is different from `False`
  or `None`. `FieldDeclaration.describe()` gives the declared properties as plain data.
- `AwaitingGeneration` is a value that is declared to be generated and has not been generated
  yet. It is distinct from an absent value and from `None`, and never counts as satisfying a
  required field. A field accepts it only when that field declares the same
  `GenerationMethod`: `AUTO_INCREMENT` for identities and `SECURE` for credentials the
  definition leaves to secure generation. JSON represents it as
  `{"awaiting_generation": "secure"}`.
- A `Relationship` has these properties: `role`, `target` (the related Model), `field` (the
  carrying field), `kind` (a `RelationshipKind`), `cardinality` (a `Cardinality`),
  `source_participation` and `target_participation` (each a `Participation`),
  `inverse_role`, and `statement`, which is the relationship exactly as the definition states
  it.
- A `RuleDeclaration` has these properties: `name`, `kind` (a `RuleKind`), `fields`,
  `requires` (a `RuleRequirement`), and `statement`. `STORED_STATE` rules are guaranteed by the
  Database layer and `APPLICATION_CONTEXT` rules by Backend Logic. The Model only declares
  them.

### Resolved choices

These are consequential choices made while implementing the definition:

- Every field property holds its resolved value: the value the project definition states,
  otherwise the Model field default from the Developer Preferences, applied one property at a
  time.
- A `name` field whose uniqueness the definition does not state is unique, following the
  name-field default. For Currency, Broker, Asset, Instance, Account Group, Trailing Group,
  Partial Group, and Action Group, the definition also declares a combined per-owner uniqueness
  rule. Whether their names should be unique only within that combination is an open question
  for the project owner. Answering it changes only the `unique` property of those fields.
- `size` is enforced as a maximum length.
- Omitting an identity gives it an `AwaitingGeneration` auto-increment value. Omitting a
  nullable field without a default gives it `None`, and the field stays out of
  `model_fields_set`.
- Credential values are excluded from a record's `repr`.
- Initial records keep reference identifiers exactly as the definition states them.
- Versions: Python 3.14 (developed on 3.14.4) and Pydantic 2.13.5 with pydantic-core 2.46.5,
  both pinned in `uv.lock`, built with `uv_build`.

## Dependencies

- Runtime: Python 3.14 or later, and `pydantic` 2.13.5 or later within major version 2.
- It depends on no other project package, and no package is installed on its behalf.
- Consumers: the Database and Backend layers import it directly. Layers that cannot import it
  derive their representations from these definitions through their own declared interfaces.

## Configuration

None. The package reads no environment variables, files, or settings, and it contains no
secrets. The initial records declare their credentials as awaiting secure generation instead of
carrying values.

## Installation

The distribution is `my-model` and the import name is `my_model`. It is internal and not
published to any registry. It is a library, so there is nothing to start.

To develop the package in its own isolated environment, run this from the package directory:

```sh
uv sync --locked
```

The environment it creates under `.venv/` is never committed.

To install it into another package, run this from that package's directory, with the path
pointing at this package:

```sh
uv add --no-editable ../model
```

## Usage examples

Discover the Models and their resolved field declarations:

```python
from my_model import MODELS, NOT_DECLARED, LogicalType, User

assert [model.logical_name for model in MODELS][:3] == ["User", "Trading Platform", "Currency"]
name = User.field_declarations()["name"]
assert name.logical_type is LogicalType.STRING and name.unique is True
assert User.field_declarations()["username"].unique is NOT_DECLARED
print(User.field_declarations()["status"].describe())
```

Validate data, with defaults applied and omission kept apart from an explicit null:

```python
import pydantic

from my_model import Currency

usd = Currency(user_id=1, name="US Dollar", code="USD")
assert usd.decimal_digits == 2 and usd.status is True
assert usd.symbol is None and "symbol" not in usd.model_fields_set
assert "symbol" in Currency(user_id=1, name="Euro", code="EUR", symbol=None).model_fields_set
try:
    Currency(user_id=1, name="Too Long", code="USDX")
except pydantic.ValidationError:
    print("rejected: code longer than its declared size")
else:
    raise AssertionError("an oversize code was accepted")
```

Identify credentials, and handle values that await generation:

```python
from my_model import AtRestMode, AwaitingGeneration, GenerationMethod, User

at_rest = {name: declaration.at_rest for name, declaration in User.credential_fields().items()}
assert at_rest == {"password": AtRestMode.HASH, "api_key": AtRestMode.HASH}

pending = AwaitingGeneration(GenerationMethod.SECURE)
user = User(name="Ada", username="ada", password=pending, api_key=pending)
assert user.pending_fields() == {"id", "password", "api_key"} and not user.is_complete()
assert "password" not in repr(user)
assert user.model_dump(mode="json")["password"] == {"awaiting_generation": "secure"}
assert User.model_validate_json(user.model_dump_json()).pending_fields() == user.pending_fields()
```

Read relationships and the rules another layer enforces:

```python
from my_model import Account, Currency, RuleKind, RuleRequirement

base = Account.relationship_for("base_currency_id")
assert base.target is Currency and base.role == "base currency"
(unique,) = [rule for rule in Currency.rule_declarations() if rule.kind is RuleKind.UNIQUE_TOGETHER]
assert unique.fields == ("user_id", "code") and unique.requires is RuleRequirement.STORED_STATE
for rule in Account.rule_declarations():
    print(rule.name, rule.requires.value, rule.fields)
```

Read the initial records the Database layer inserts:

```python
from my_model import MODELS, TradingPlatform, initial_records

platforms = initial_records(TradingPlatform)
assert [platform.code for platform in platforms] == ["metatrader_5", "binance"]
assert all(platform.pending_fields() == {"id"} for platform in platforms)
print({model.logical_name: len(initial_records(model)) for model in MODELS})
```
