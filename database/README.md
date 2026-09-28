# Database

Reusable library that persists Entity data and publishes standard data Operations. Consumers use it only through `database.interface`: Interface hands each request to Data, which resolves the Instance and its Engine and returns the result.

```python
from database.interface import add, get_by_id
from model.interface import Broker

broker = add(Broker(name="Example Broker", user_id=1))
print(get_by_id(Broker, broker.id).name)  # Example Broker
```

## Interface

Every Operation names an Entity class or Entity instance directly, never a Model name or identity, and accepts an optional `instance` (the key of a configured Instance). When `instance` is omitted, Database uses the configured default Instance. Changes are atomic: an Operation that fails leaves no partial change. Every example below assumes the default Instance is provisioned and holds the Initial Data (see Setup).

| Operation | Function |
|---|---|
| Add | `add` |
| Update | `update` |
| List | `list_` |
| Delete | `delete` |
| Enable | `enable` |
| Disable | `disable` |
| Get by ID | `get_by_id` |
| Count | `count` |
| Sum | `sum_` |
| Min | `min_` |
| Max | `max_` |
| Truncate | `truncate` |
| Execute Command | `execute_command` |

### Add

Stores a new record and returns the created Entity instance with its generated `id`. Add applies Value Generation first, then Default Values for omitted Fields, then refuses a record that omits a required Field or holds null in a non-nullable Field. The instance you pass is left unchanged.

```python
from database.interface import add
from model.interface import Currency

created = add(Currency(user_id=1, code="SEK", symbol="kr", country="Sweden"))
print(created.id, created.decimal_digits)  # 9 2
```

### Update

Changes only the Fields supplied on the Entity instance, locating the record by its `id`. It never changes `id` or an immutable Field, keeps omitted Fields, stores an explicit `None` as null, and returns the updated instance, or `None` when no record has that `id`.

```python
from database.interface import update
from model.interface import Currency

updated = update(Currency(id=1, symbol="US$"))
print(updated.code, updated.symbol)  # USD US$
print(update(Currency(id=999, symbol="?")))  # None
```

### List

Returns the records of an Entity class that satisfy the Filters. A Filter receives an Entity Field, an `Operator` enum member, and a value. `filter_combination` receives a `Combination` enum member and defaults to the configured value (`AND`). Orders receive an Entity Field and a `Direction` enum member, and default to the configured Order (`id`, ascending). A `limit` caps the number of records; without it every match is returned.

```python
from database.interface import Combination, Direction, Filter, Operator, Order, list_
from model.interface import Currency

rows = list_(
    Currency,
    filters=[Filter(Currency.decimal_digits, Operator.EQUALS, 2), Filter(Currency.code, Operator.STARTS_WITH, "C")],
    filter_combination=Combination.AND,
    orders=[Order(Currency.code, Direction.DESCENDING)],
    limit=2,
)
print([currency.code for currency in rows])  # ['CHF', 'CAD']
```

### Delete

Removes one record and returns `True`, or `False` when no record has that `id`. A record that other records still refer to cannot be deleted.

```python
from database.interface import add, delete
from model.interface import Currency

temporary = add(Currency(user_id=1, code="NOK"))
print(delete(Currency, temporary.id))  # True
print(delete(Currency, temporary.id))  # False
```

### Enable

Sets a record's `is_active` Field to `true` and returns the Entity instance, or `None` when no record has that `id`.

```python
from database.interface import disable, enable
from model.interface import Broker

disable(Broker, 1)
print(enable(Broker, 1).is_active)  # True
```

### Disable

Sets a record's `is_active` Field to `false` and returns the Entity instance, or `None` when no record has that `id`.

```python
from database.interface import disable, enable
from model.interface import Broker

print(disable(Broker, 1).is_active)  # False
enable(Broker, 1)
```

### Get by ID

Returns the record as an Entity instance, or `None` when no record has that `id`.

```python
from database.interface import get_by_id
from model.interface import Currency

print(get_by_id(Currency, 1).code)  # USD
print(get_by_id(Currency, 999))  # None
```

### Count

Returns the number of records of an Entity, `0` when there are none.

```python
from database.interface import count
from model.interface import Asset, Position

print(count(Asset), count(Position))  # 4 0
```

### Sum

Totals a numeric Field, ignoring null values, and returns `0` when no usable value exists.

```python
from database.interface import sum_
from model.interface import Asset

print(sum_(Asset, Asset.digits))  # 15
```

### Min

Returns the smallest value of a Field, ignoring null values, or `None` when no usable value exists.

```python
from database.interface import min_
from model.interface import Asset

print(min_(Asset, Asset.point_size))  # 0.0001
```

### Max

Returns the largest value of a Field, ignoring null values, or `None` when no usable value exists.

```python
from database.interface import max_
from model.interface import Asset

print(max_(Asset, Asset.point_size))  # 0.01
```

### Truncate

Removes every record of an Entity, keeps its Table structure, and returns the number of records removed.

```python
from decimal import Decimal

from database.interface import add, truncate
from model.interface import TrailingRule

add(TrailingRule(name="example", trailing_group_id=1, trigger_percentage=Decimal("50")))
print(truncate(TrailingRule))  # 1
```

### Execute Command

Runs a SQL command through the selected Engine in one transaction and returns a Command Result with `rows` and `affected_count`. `rows` is a list of column-name-to-value mappings for a command that returns rows, `affected_count` is the number of affected records for a command that changes data, and the value that does not apply is `None`. Write parameters as named `:placeholders` and pass their values separately.

```python
from database.interface import execute_command

selected = execute_command(
    "SELECT code FROM currency WHERE decimal_digits = :digits ORDER BY code",
    {"digits": 0},
)
print(selected.rows, selected.affected_count)  # [{'code': 'JPY'}] None

changed = execute_command(
    "UPDATE broker SET description = :text WHERE id = :id",
    {"text": "Primary broker", "id": 1},
)
print(changed.rows, changed.affected_count)  # None 1
```

## Setup

Database requires Python 3.14 or newer and is managed with `uv`. It depends on the Model library, which it finds beside it.

```bash
cd database
uv sync
uv run alembic upgrade head
uv run python -m database.initial_data
```

- `uv run alembic upgrade head` provisions the configured default Instance from the Entities that Model publishes, and `uv run alembic downgrade -1` reverses the latest migration step.
- `uv run python -m database.initial_data` inserts the Initial Data once. It also generates the credentials the Initial Data needs, stores them protected (User credentials hashed, Instance and Account credentials encrypted), and writes the plaintext to an owner-only file in `database/.secrets/`, which version control ignores. Credentials are never printed or logged.
- The configuration lives in `database/database.yaml`. To run against another copy, for example to try the examples safely, point `DATABASE_CONFIGURATION` at a copy of that file in another directory and provision that copy in the same way; its storage is created beside the copy.

To use Database from another Component, add both libraries as dependencies of that Component, because a dependency's own source locations are not inherited:

```bash
uv add --editable <path to the model directory>
uv add --editable <path to the database directory>
```

## Use

Import Operations from `database.interface`. Pass an Entity class or instance from `model.interface`, and optionally the key of an Instance. The configuration declares one Instance, `application`, which is also the default.

```python
from database.interface import Filter, Operator, add, list_
from model.interface import Currency

add(
    Currency(user_id=1, code="DKK", symbol="kr"), instance="application"
)  # the named Instance
add(Currency(user_id=1, code="PLN", symbol="zł"))  # the default Instance
codes = [
    c.code
    for c in list_(
        Currency, filters=[Filter(Currency.code, Operator.IN, ["DKK", "PLN"])], instance="application"
    )
]
print(codes)  # ['DKK', 'PLN']
```

Operations return Entity instances, so their Fields, `to_json()`, and `declaration` are available as described in the Model documentation. Database stores every Field value as received, including Fields that carry a sensitivity marker; any special handling of such values belongs to the Component that uses Database.

## Verify

Confirm that the default Instance holds the structure of every Entity:

```bash
uv run python -m database.verification
```

It prints `15 of 15 Tables found` and exits with status 0, or names the missing Tables and exits with status 1. To confirm the Initial Data, compare the record counts with the defined values and check that no record refers to a missing target:

```python
from database.interface import count, execute_command
from model.interface import Account, Asset, Broker, Currency, TradingPlatform, User

counts = [
    count(entity)
    for entity in (User, TradingPlatform, Currency, Broker, Asset, Account)
]
print(counts)  # [1, 2, 8, 1, 4, 1]
print(execute_command("PRAGMA foreign_key_check").rows)  # []
```

## Troubleshooting

- **`ValueError: Unknown Instance '...'`.** The `instance` argument must be the key of an Instance declared in `database.yaml`; here that is `application`.
- **`ValueError: <Entity>.<Field> is required and cannot be null`.** Add refuses a record that omits a required Field or holds null in a Field that is not nullable. Supply the Field.
- **`IntegrityError` on Add or Update.** A uniqueness rule was violated, or a Reference points to a record that does not exist. The change is rolled back and nothing is stored.
- **`IntegrityError` on Delete or Truncate.** Other records still refer to a record you are removing. Remove or change the records that refer to it first.
- **`RuntimeError: The Instance already holds Initial Data`.** The Initial Data is inserted once. To start over, delete the storage file under `database/db/`, run `uv run alembic upgrade head`, and run the Initial Data again. This generates new credentials and replaces the delivered credentials file.
- **`alembic` cannot find its configuration.** Run the `uv run alembic ...` commands from the `database` directory.
- **A SQL command fails with a missing parameter.** In Execute Command, a colon followed by a name is a placeholder. Pass its value in `parameters`, and keep literal text out of the command.
