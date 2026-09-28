# Database

## Overview

Database persists Entity data and publishes the standard data Operations. A consumer works with it only through its Interface: every Operation takes an Entity class or Entity instance from the shared Model and an optional Instance. An Instance is a named database that uses one Engine, and when it is omitted the configured default Instance is used.

Behind Interface, an internal Data layer resolves each request's Instance and Engine, and an internal Engine layer carries the Operation out. Consumers never use those two layers directly.

## Interface

Interface is the only public layer of Database. Every Operation below receives an Entity class or Entity instance from the shared Model and accepts an optional `instance` argument naming the Instance to use; when it is omitted, the configured default Instance is used. Operations that change data are atomic: a failed Operation leaves no partial change.

The Operations that would shadow a Python built-in end in an underscore: `list_`, `sum_`, `min_`, and `max_`. The examples assume the default Instance is provisioned and holds the initial data, as described in Setup.

### Add

Stores a new record for an Entity instance and returns the created Entity. Fields left out take their declared Default Values, the `id` is generated, and a missing required Field is refused.

```python
from database.interface import add
from model.interface import Currency

krona = add(Currency(user_id=1, code="SEK", symbol="kr", country="Sweden"))
print(krona.id, krona.decimal_digits, krona.is_active)
```

```text
9 2 True
```

### Update

Changes only the Fields you supply on the record with the Entity's `id`, keeps every other Field, stores an explicit `None` as a value, never changes `id`, and returns the updated Entity, or `None` when no record has that `id`.

```python
from database.interface import get_by_id, update
from model.interface import Currency

updated = update(Currency(id=1, symbol="US$"))
print(updated.code, updated.symbol)
print(get_by_id(Currency, 1).country)
```

```text
USD US$
United States
```

### Delete

Removes the record with the given `id` and returns `True`, or returns `False` when no record has that `id`.

```python
from database.interface import delete
from model.interface import Currency

print(delete(Currency, 8))
print(delete(Currency, 8))
```

```text
True
False
```

### Enable

Sets `is_active` to `True` on the record with the given `id` and returns the Entity, or `None` when no record has that `id`.

```python
from database.interface import disable, enable
from model.interface import Asset

disable(Asset, 1)
print(enable(Asset, 1).is_active)
print(enable(Asset, 999))
```

```text
True
None
```

### Disable

Sets `is_active` to `False` on the record with the given `id` and returns the Entity, or `None` when no record has that `id`.

```python
from database.interface import disable
from model.interface import Asset

print(disable(Asset, 1).is_active)
print(disable(Asset, 999))
```

```text
False
None
```

### Truncate

Removes every record of an Entity class, keeps its structure, and returns the number of records removed.

```python
from decimal import Decimal

from database.interface import add, truncate
from model.interface import TrailingRule

add(TrailingRule(name="first", trailing_group_id=1, trigger_percentage=Decimal(50)))
print(truncate(TrailingRule))
```

```text
1
```

### Get by ID

Returns the record with the given `id`, or `None` when no record has that `id`.

```python
from database.interface import get_by_id
from model.interface import Currency

print(get_by_id(Currency, 2).code)
print(get_by_id(Currency, 999))
```

```text
EUR
None
```

### List

Returns the records of an Entity class that match optional Filters, combined with `AND` or `OR`, in the order of optional Orders, up to an optional limit. An omitted combination or Order uses the configured default, and an omitted limit returns every match.

```python
from database.interface import Filter, FilterOperator, Order, OrderDirection, list_
from model.interface import Currency

rows = list_(
    Currency,
    filters=[Filter("decimal_digits", FilterOperator.EQUALS, 2)],
    orders=[Order("code", OrderDirection.ASCENDING)],
    limit=3,
)
print([currency.code for currency in rows])
```

```text
['AUD', 'CAD', 'CHF']
```

### Count

Returns the number of records of an Entity class, `0` when there are none.

```python
from database.interface import count
from model.interface import Currency

print(count(Currency))
```

```text
8
```

### Sum

Returns the total of a numeric Field, ignoring `None`, or `0` when no usable value exists.

```python
from database.interface import sum_
from model.interface import Asset

print(sum_(Asset, "digits"))
```

```text
15
```

### Min

Returns the smallest value of a Field, ignoring `None`, or `None` when no usable value exists.

```python
from database.interface import min_
from model.interface import Asset

print(min_(Asset, "point_size"))
```

```text
0.0001
```

### Max

Returns the largest value of a Field, ignoring `None`, or `None` when no usable value exists.

```python
from database.interface import max_
from model.interface import Asset

print(max_(Asset, "digits"))
```

```text
5
```

### Execute Command

Runs one SQL command with optional named parameters through the selected Engine and returns a Command Result. `rows` holds the returned rows as mappings from column name to value, and `affected_count` holds the number of rows a changing command affected. The value that does not apply is `None`.

```python
from database.interface import execute_command

result = execute_command(
    "select code, decimal_digits from currency where decimal_digits = :digits order by code",
    {"digits": 0},
)
print(result.rows)
print(result.affected_count)
```

```text
[{'code': 'JPY', 'decimal_digits': 0}]
None
```

## Setup

Database needs Python 3.14 or newer and is managed with [uv](https://docs.astral.sh/uv/). It uses the shared Model, so keep the `model` and `database` directories side by side.

To use Database from another project, add it from the directory that holds both, as an editable dependency. uv installs the Model that Database depends on together with it. Database finds its configuration and its database directory relative to its own source, so it must be installed in editable form:

```bash
uv add --editable ../database
```

To work on Database itself, or to provision its default Instance for the first time, install the environment and apply the migrations from the Database component root:

```bash
uv sync
uv run alembic upgrade head
```

The first migration creates the storage structure of every Entity, and the following ones insert the initial data the Target defines. The default Instance is stored in the database directory of the Component and is not committed. The credentials in the initial data are generated at that moment, stored as generated, and never displayed or written to any file, so set new ones through your application before relying on those accounts.

Confirm that the default Instance is provisioned:

```bash
uv run alembic current
```

```text
0013 (head)
```

## Use

Every Operation works on the configured default Instance unless you pass `instance="<key>"`, where the key is one of the Instances declared in the Component's configuration. An Instance that is not declared is refused:

```python
from database.interface import count
from model.interface import Currency

print(count(Currency, instance="application"))
try:
    count(Currency, instance="reports")
except ValueError as error:
    print(error)
```

```text
8
Instance 'reports' is not declared
```

`list_` takes any number of Filters. They are combined with `AND` unless you pass `combination=FilterCombination.OR`, and the records come back in ascending `id` order unless you pass Orders. There is no grouping of Filters:

```python
from database.interface import Filter, FilterCombination, FilterOperator, list_
from model.interface import Currency

usd_or_jpy = [
    Filter("code", FilterOperator.EQUALS, "USD"),
    Filter("code", FilterOperator.EQUALS, "JPY"),
]
print([c.code for c in list_(Currency, filters=usd_or_jpy, combination=FilterCombination.OR)])
print([c.code for c in list_(Currency, filters=usd_or_jpy)])
```

```text
['USD', 'JPY']
[]
```

Read results as the Entities you asked for. `is_null` and `is_not_null` ignore the Filter's value, `in` takes a list of values, and `contains`, `starts_with`, and `ends_with` treat `%` and `_` in the value as ordinary characters. Values are stored and returned exactly as you supply them, including credentials, so protect any such value before you pass it to Database.

## Verify

The default Instance is correct when it holds the storage structure of every Entity that Model publishes. With the SQLite Engine, list the tables the Instance holds and compare them with the Entities:

```python
import model.interface as entities
from database.interface import execute_command

result = execute_command("select name from sqlite_master where type = 'table'")
present = {row["name"] for row in result.rows or []}
missing = [name for name in entities.__all__ if getattr(entities, name).__tablename__ not in present]
print(missing)
```

```text
[]
```

An empty list means every Entity has its structure. Any name in the list is an Entity whose structure is missing, which means the Instance was changed outside the migrations. Back up its data, then provision the Instance again from an empty database as described in Setup.

## Troubleshooting

### `FileNotFoundError` naming `database.yaml`

Database was installed as a regular dependency. It finds its configuration and its database directory relative to its own source, so it must be installed in editable form. Reinstall it:

```bash
uv remove database
uv add --editable ../database
```

### `OperationalError: no such table: currency`

The default Instance exists but has not been provisioned. The failed request may also have created an empty storage file, which the migrations can use. From the Database component root, apply the migrations as described in Setup:

```bash
uv run alembic upgrade head
```

### `ValueError: 'name' is required`

Add received an Entity that leaves out a required Field, or sets it to `None`, and the Field has no Default Value. Supply every Field the Entity requires; the Fields of each Entity are listed in the Model documentation.

### `IntegrityError: UNIQUE constraint failed` or `FOREIGN KEY constraint failed`

The Operation would break a rule the Model declares, so it was refused and changed nothing. A unique failure means a record with the same value already exists. A foreign key failure means the record refers to a parent that does not exist, or you tried to delete a record that other records still refer to. Use a different value, create the parent first, or remove the dependent records before deleting the parent.

### `ValueError: Instance '<key>' is not declared`

The `instance` argument names an Instance that the Component's configuration does not declare. Use a declared key, or omit the argument to use the default Instance.
