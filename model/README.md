# my_model

The shared logical Model package of Trading Assistant. It defines every domain
Model once — its fields, relationships, domain rules, and initial records — and
publishes them as an importable Python package.

## Purpose and boundaries

`my_model` owns one shared logical meaning for each of the fourteen domain Models
and the validation of Model instances. The Database, Backend, and Frontend layers
consume that one meaning instead of maintaining private copies of it.

The package does **not** own:

- persistence — tables, columns, foreign keys, migrations, credential storage, and
  seeding belong to Database;
- application behaviour and API transport — they belong to Backend;
- presentation and interaction — they belong to Frontend;
- runtime configuration, composition, and deployment — they belong to Platform.

## Public interface

Import only from `my_model`. No other module of the package is public.

| Export | What it is |
| --- | --- |
| `User`, `Currency`, `TradingPlatform`, `Broker`, `AccountGroup`, `Account`, `Asset`, `TrailingGroup`, `TrailingRule`, `PartialGroup`, `PartialRule`, `ActionGroup`, `Action`, `Position` | The fourteen Models. Constructing one validates field types, nullability, and defaults; an invalid value raises `pydantic.ValidationError`. |
| `MODELS` | An immutable mapping from each Model key to its class, in project order. |
| `model_metadata(model)` | The resolved definition of one Model, given its class or an instance. Returns `key`, `purpose`, `fields` in declared order, `relationships`, `rules`, and `initial_data`. Anything that is not a shared Model raises `LookupError`. |
| `ModelSpec`, `FieldSpec`, `RelationshipSpec`, `RuleSpec`, `LogicalType`, `GenerateValue`, `UNSET` | The types a definition is made of, so consumers can name what `model_metadata` returns. |

Two conventions matter to every consumer:

- **The primary key is absent until it is assigned.** `id` is `None` on a Model you
  construct; the Database assigns it on create.
- **Credential values are never carried back.** A field marked `credential` (such as
  `User.password` or `Account.api_key`) is `None` on instances the Database returns,
  and is write-only at the API boundary. Its declared nullability stays `false` —
  the field is required *in the domain*, not optional.

A field property the project does not declare is `UNSET`, which is distinct from a
declared `None`. A `GenerateValue` in `initial_data` is an instruction, not a value:
the package never produces it, and the layer that seeds the data fulfils it.

## Dependencies

- Python 3.14.7 (`requires-python >=3.14,<3.15`)
- [pydantic](https://docs.pydantic.dev/) 2.13.5 — the only run-time dependency
- [uv](https://docs.astral.sh/uv/) 0.12.10 — environment and build tool

## Configuration

None. The package reads no configuration file and no environment variable at run
time, and nothing about it changes between environments.

## Installation and startup

The package is a library; it has nothing to start. From this directory:

```
uv sync
```

A consumer installs it as an editable local path dependency. In the consumer's
`pyproject.toml`:

```toml
[project]
dependencies = ["my-model"]

[tool.uv.sources]
my-model = { path = "../model", editable = true }
```

The distribution is named `my-model` and the import package is `my_model`. It is
internal and is never published to a registry.

## Usage examples

Construct a Model and let it validate itself:

```python
from decimal import Decimal

from my_model import Account

account = Account(
    name="Acc-1",
    account_group_id=1,
    broker_id=1,
    base_currency_id=1,
    username="test",
    leverage=100,
    account_type="CFD",
)

assert account.id is None            # the Database assigns the primary key on create
assert account.password is None      # a credential is never carried back from storage
assert account.balance == Decimal("0")  # declared default
assert account.status is True           # declared default
```

Read one Model's definition instead of restating it:

```python
from my_model import MODELS, model_metadata

broker = model_metadata(MODELS["broker"])

assert broker.key == "broker"
assert [f.name for f in broker.fields][:2] == ["id", "name"]
assert broker.field("user_id").type == "integer"
assert [r.target for r in broker.relationships] == ["user", "trading_platform"]
assert broker.rules[0].fields == ("user_id", "name")   # unique in combination
```

Walk every Model, and recognize an initial value that must be generated:

```python
from my_model import MODELS, GenerateValue, User, model_metadata

assert len(MODELS) == 14
for key, model in MODELS.items():
    assert model_metadata(model).key == key

admin = model_metadata(User).initial_data[0]
assert admin["name"] == "Admin"
assert isinstance(admin["password"], GenerateValue)  # produced securely when seeded
```
