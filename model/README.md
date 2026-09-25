# Trading Assistant Model

## Overview

Model is a reusable library that holds the Domain Entities of the Trading Assistant: the fifteen
concepts the Target defines, with their Fields, defaults, uniqueness, relationships and
credential sensitivity. Database and Logic use it; it stores nothing and performs no workflow.

Model is a library (it has nothing to start). Every Domain Entity is one kind of Model: an
independent class in the shape the Target declares, checked whenever it is built.

| Entity | Entity | Entity |
|---|---|---|
| `User` | `TradingPlatform` | `Instance` |
| `Currency` | `Broker` | `Asset` |
| `AccountGroup` | `Account` | `TrailingGroup` |
| `TrailingRule` | `PartialGroup` | `PartialRule` |
| `ActionGroup` | `Action` | `Position` |

Model has four layers. **Interface** is the only public one. **Entity**, **Declaration** and
**Foundation** are private implementation: do not import from them.

## Interface

Import everything from `trading_assistant_model.interface`.

```python
from decimal import Decimal

from trading_assistant_model.interface import Account, User
```

### Direct construction

Build an Entity with keyword arguments. It is checked as it is built: a wrong type, a missing
required Field, an explicit `None` on a Field that is not nullable, or a value that breaks a
declared restriction raises `pydantic.ValidationError`. A Field you omit takes its declared
default (or `None` when it is nullable). An input that is not a Field is ignored. `id` stays
`None` until the value is generated.

The examples use placeholders only; never put a real credential in code or documentation.

```python
user = User(
    name="<display name>",
    username="<username>",
    password="<password placeholder>",
    api_key="<api key placeholder>",
)
assert user.is_active is True  # the declared default
assert user.description is None  # nullable, omitted
assert user.id is None  # generated later
```

A failure names the Field and the rule. The value of a sensitive Field (a credential) is never
shown in it, and every other value is:

```python
from pydantic import ValidationError

try:
    User(
        name="<display name>",
        username="<username>",
        password=12345,
        api_key="<placeholder>",
    )
except ValidationError as error:
    assert "12345" not in str(error)  # the sensitive value is hidden
    assert error.errors()[0]["loc"] == ("password",)
```

Assigning to a Field is checked the same way, and a Field the Target declares immutable cannot
be changed once the Entity exists.

```python
user.name = "<another display name>"
```

### Conversion to and from JSON

`to_json()` returns JSON text holding every declared Field. Exact decimals and date-times are
written as strings. `from_json()` accepts JSON text, bytes, or an already parsed JSON object,
reads those string forms back, and then follows exactly the rules of direct construction.
Invalid JSON text, or JSON that is not an object, raises `ValueError`.

`to_json()` includes credential Fields, because a round trip needs them; decide what to expose.

```python
account = Account(
    name="<account name>",
    group_id=1,
    broker_id=1,
    instance_id=1,
    base_currency_id=1,
    username="<account username>",
    password="<password placeholder>",
    leverage=100,
    balance=Decimal("1500.25"),
    account_type="<account type>",
)
text = account.to_json()
assert '"balance": "1500.25"' in text  # exact decimals are strings

again = Account.from_json(text)
assert again.balance == Decimal("1500.25")
assert again.to_json() == text
```

Exact decimals must be `Decimal` values (a `float` is refused), and date-times must carry a time
zone.

### Declared meaning

Each Entity publishes its technology-independent meaning as `Entity.declaration`: every Field
with its type, nullability, default, sensitivity and length, the primary key, the uniqueness
constraints and the references to other Entities. Database reads this to build storage, and
it contains no storage syntax. A property the Target does not state reads as `OMITTED`, which is
different from an explicit `None` or `False`.

```python
from trading_assistant_model.interface import OMITTED, FieldType

fields = {field.name: field for field in Account.declaration.fields}
assert fields["balance"].type is FieldType.DECIMAL
assert fields["password"].sensitive is True
assert fields["name"].sensitive is OMITTED
assert [reference.entity for reference in Account.declaration.references] == [
    "AccountGroup",
    "Broker",
    "Instance",
    "Currency",
]
```

The description of every Entity is its documentation (`help(User)`), and the description of
every Field is available as `User.model_fields["name"].description`.

## Setup

Model needs Python 3.14 and [uv](https://docs.astral.sh/uv/). It has no configuration: no
environment variables, no files, no secrets.

To work on Model itself, create its environment from the lock file:

```bash
cd model
uv sync
```

To use Model from another Component (Database or Logic), add it as a dependency of that
Component's project, giving the path to the Model folder:

```bash
uv add <path to the model folder>
```

## Run

Model is a library, so there is nothing to start. Use it by importing from
`trading_assistant_model.interface`, as shown in the Interface section. To see it work:

```bash
uv run python -c "from trading_assistant_model.interface import User; print(User.declaration.entity)"
```

## Verify

Model ships no test suite of its own. Verify it with the project's quality checks, run from the
Model folder, and a short end-to-end check that builds an Entity and converts it to and from JSON:

```bash
uv run ruff format --check .
uv run ruff check .
uv run pyright
```

```bash
uv run python - <<'PY'
from trading_assistant_model.interface import User

user = User(
    name="<display name>",
    username="<username>",
    password="<password placeholder>",
    api_key="<api key placeholder>",
)
assert User.from_json(user.to_json()).username == user.username
print("Model verified")
PY
```

Each check ends with no findings, and the last command prints `Model verified`. The Python
examples in the Interface section can also be run as written.

## Troubleshooting

- **`pydantic.ValidationError` when building an Entity, or when assigning to a Field.** Read
  `error.errors()`: each item names the Field (`loc`), the rule (`msg`) and its value. The usual
  causes are a wrong type (for example a `float` for an exact decimal, or a string for an
  integer), a date-time without a time zone, a missing required Field, an explicit `None` on a
  Field that is not nullable, a string longer than its declared length, and a change to a Field
  declared immutable (type `frozen_field`).
- **A value shows as `[hidden]` in an error.** That Field is a credential; its value is never
  shown. Look at the Field name and rule instead.
- **`ValueError: Invalid JSON` or `ValueError: JSON must be an object` from `from_json()`.** The
  text is not valid JSON, or it is valid JSON that is not an object. The message never contains
  the text itself.
- **`from_json()` refuses a number for an exact decimal or a date-time string without an
  offset.** Write exact decimals as strings or integers (`"1500.25"`), and date-times with an
  offset (`"2026-01-01T10:00:00+00:00"` or a trailing `Z`).
- **`TypeError: ... differs from its Declaration` on import.** This happens only while changing
  Model itself: an Entity's Fields no longer match its Declaration (names, types, nullability,
  defaults or length). Make the Entity and its Declaration agree.
- **`ImportError: cannot import name ... from 'trading_assistant_model.interface'`.** Interface
  presents only the fifteen Entities and the vocabulary for reading their declared meaning. Do not
  reach into the Entity, Declaration or Foundation layers to work around it: they are private and
  may change without notice.
- **`uv sync` reports that Python 3.14 is not available.** Run `uv python install 3.14` and try
  again.
