# Database

Persistence gateway for the Trading Assistant. It stores and retrieves the Entities published by Model in an active Instance, through one public surface.

```python
from database.interface import Database
from model.interface import Currency

db = Database()
print(db.get_by_id(Currency, 1).code)
```

```text
USD
```

## Interface

`database.interface` is the only public Database surface. Other files are internal.

### Importing Database and the active Instances

Import `Database` and create it once. Every Operation accepts an optional `instance`; when it is omitted the configured default Instance, `sqlite`, is used. The active Instances are the members of `DatabaseInstance`:

- `DatabaseInstance.SQLITE` selects the `sqlite` Instance.
- `DatabaseInstance.POSTGRESQL` selects the `postgresql` Instance.

```python
from database.interface import Database, DatabaseInstance

db = Database()
print([instance.value for instance in DatabaseInstance])
```

```text
['sqlite', 'postgresql']
```

Operations receive an Entity class or an Entity instance published by Model, never a Model name. Filters, Filter Combinations, Orders, and Instances are enum members, never strings.

### Operations

#### Add

Persists a complete Entity instance and returns the created Entity instance with its generated `id`.

```python
from database.interface import Database
from model.interface import Currency

db = Database()
created = db.add(Currency(user_id=1, code="SEK", symbol="kr", country="Sweden"))
print(created.code, isinstance(created.id, int))
db.delete(Currency, created.id)
```

```text
SEK True
```

Adding the same `user_id` and `code` twice is refused by the Uniqueness Constraint; the last line above removes the record so the example can run again.

#### Update

Locates the record by the Entity instance's `id`, never changes `id` or an immutable Field, replaces every mutable Field, and returns the updated Entity instance, or `None` when no record has that `id`.

```python
from database.interface import Database
from model.interface import Currency

db = Database()
currency = db.get_by_id(Currency, 1)
currency.description = "Reserve currency"
print(db.update(currency).description)
currency.description = None
db.update(currency)
```

```text
Reserve currency
```

#### List

Returns matching Entity instances. It accepts optional Filters, a Filter Combination (`AND` by default), an ordered list of Orders (ascending `id` by default), and a limit (`0` or a negative value means no limit).

```python
from database.interface import Database, Filter, FilterOperator, Order, OrderDirection
from model.interface import Currency

db = Database()
currencies = db.list(
    Currency,
    filters=[Filter("decimal_digits", FilterOperator.EQUALS, 2)],
    orders=[Order("code", OrderDirection.DESCENDING)],
    limit=3,
)
print([currency.code for currency in currencies])
```

```text
['USD', 'NZD', 'GBP']
```

The Filter Operators are `EQUALS`, `NOT_EQUALS`, `GREATER_THAN`, `GREATER_OR_EQUAL`, `LESS_THAN`, `LESS_OR_EQUAL`, `IN`, `CONTAINS`, `STARTS_WITH`, `ENDS_WITH`, `IS_NULL`, and `IS_NOT_NULL`. Several Filters combine with `FilterCombination.AND` or `FilterCombination.OR`, without grouping.

#### Delete

Deletes the record with the given `id` and returns `True`, or returns `False` when no record has that `id`.

```python
from database.interface import Database
from model.interface import Currency

db = Database()
created = db.add(Currency(user_id=1, code="NOK"))
print(db.delete(Currency, created.id))
print(db.delete(Currency, created.id))
```

```text
True
False
```

#### Enable

Sets the record's `is_active` Field to `true` and returns the Entity instance, or `None` when no record has that `id`.

```python
from database.interface import Database
from model.interface import Currency

db = Database()
db.disable(Currency, 2)
print(db.enable(Currency, 2).is_active)
```

```text
True
```

#### Disable

Sets the record's `is_active` Field to `false` and returns the Entity instance, or `None` when no record has that `id`.

```python
from database.interface import Database
from model.interface import Currency

db = Database()
print(db.disable(Currency, 3).is_active)
db.enable(Currency, 3)
```

```text
False
```

#### Get by ID

Returns the Entity instance with the given `id`, or `None`.

```python
from database.interface import Database
from model.interface import User

db = Database()
print(db.get_by_id(User, 1).username, db.get_by_id(User, 999))
```

```text
admin None
```

#### Count

Returns the number of matching records, and `0` when none match.

```python
from database.interface import Database, Filter, FilterOperator
from model.interface import Currency

db = Database()
print(db.count(Currency), db.count(Currency, [Filter("decimal_digits", FilterOperator.EQUALS, 0)]))
```

```text
8 1
```

#### Sum

Returns the total of a numeric Field over the matching records. It ignores `null` values and returns `0` when no usable value exists.

```python
from database.interface import Database
from model.interface import Currency

db = Database()
print(db.sum(Currency, "decimal_digits"))
```

```text
14
```

#### Min

Returns the smallest non-null value of a Field over the matching records, or `None` when no usable value exists.

```python
from database.interface import Database
from model.interface import Currency

db = Database()
print(db.min(Currency, "code"))
```

```text
AUD
```

#### Max

Returns the largest non-null value of a Field over the matching records, or `None` when no usable value exists.

```python
from database.interface import Database
from model.interface import Currency

db = Database()
print(db.max(Currency, "code"))
```

```text
USD
```

#### Truncate

Removes every record of an Entity, keeps its table structure, and returns the number of records removed.

```python
from database.interface import Database
from model.interface import Position

db = Database()
print(db.truncate(Position))
```

```text
0
```

#### Execute Command

Executes a SQL command with named bound parameters through the selected Instance and returns a `CommandResult` with `rows` and `affected_count`; a value that does not apply is `None`. It does not change schema; schema changes belong to Create Tables.

```python
from database.interface import Database

db = Database()
result = db.execute_command(
    "select code, decimal_digits from currency where code = :code", {"code": "JPY"}
)
print(result.rows, result.affected_count)
```

```text
[{'code': 'JPY', 'decimal_digits': 0}] None
```

### Create Tables

Creates or migrates every table the Model Entities declare on an Instance. It creates what is missing and adds missing Fields, indexes, and constraints to existing tables without losing records. It is safe to run again. It is also a manual command: `uv run database create-tables [--instance sqlite|postgresql]`.

```python
from database.interface import DatabaseInstance, create_tables

create_tables(DatabaseInstance.SQLITE)
print("Tables are ready")
```

```text
Tables are ready
```

### Insert Initial Data

Inserts the declared Initial Data into an Instance whose tables exist and returns the number of records inserted. Credential Fields receive securely generated values that are never displayed. A record the Instance already holds is left unchanged, so running it again inserts nothing. It is also a manual command: `uv run database insert-initial-data [--instance sqlite|postgresql]`.

```python
from database.interface import insert_initial_data

print(insert_initial_data())
```

```text
0
```

The example prints `23` on an Instance that has not received the Initial Data yet.

## Setup

1. Install Python 3.14 and [uv](https://docs.astral.sh/uv/).
2. From the Database directory, install the locked dependencies. Model is a read-only dependency found next to this directory:

   ```text
   uv sync
   ```

3. Prepare the default Instance:

   ```text
   uv run database create-tables
   uv run database insert-initial-data
   ```

   ```text
   Tables are ready
   Inserted 23 records
   ```

The default `sqlite` Instance stores its data in the `db` directory of the package. The `postgresql` Instance connects to `127.0.0.1:5432`, database `application`, as user `postgres`. To use it, create that role and database on your server (or edit its entries in `config.yaml`), supply the password through the `PGPASSWORD` environment variable when one is required, then run the two commands with `--instance postgresql`. Never write a password into `config.yaml`.

## Use

Choose the Instance per request, or omit it to use the default:

```python
from database.interface import Database, DatabaseInstance
from model.interface import Currency

db = Database()
print(db.count(Currency), db.count(Currency, instance=DatabaseInstance.SQLITE))
```

```text
8 8
```

Combine Filters with `FilterCombination` and order the result:

```python
from database.interface import Database, Filter, FilterCombination, FilterOperator, Order
from model.interface import Currency

db = Database()
found = db.list(
    Currency,
    filters=[
        Filter("code", FilterOperator.STARTS_WITH, "C"),
        Filter("code", FilterOperator.EQUALS, "JPY"),
    ],
    combination=FilterCombination.OR,
    orders=[Order("code")],
)
print([currency.code for currency in found])
```

```text
['CAD', 'CHF', 'JPY']
```

Totals over a filtered selection:

```python
from database.interface import Database, Filter, FilterOperator
from model.interface import Currency

db = Database()
print(db.sum(Currency, "decimal_digits", [Filter("code", FilterOperator.IN, ["USD", "JPY"])]))
```

```text
2
```

## Verify

Confirm that a prepared Database holds its structure and Initial Data through the public surface:

```python
from database.interface import Database
from model.interface import Currency, User

db = Database()
print(db.count(User), db.count(Currency), db.get_by_id(User, 1).username)
```

```text
1 8 admin
```

## Troubleshooting

| Problem | Message | Resolution |
|---|---|---|
| An Instance is passed as text | `instance must be a DatabaseInstance member` | Pass a `DatabaseInstance` member such as `DatabaseInstance.SQLITE`. |
| An Entity is passed by name | `an Entity class published by Model is required` | Pass the Entity class imported from `model.interface`. |
| Add or Update receives a class | `an Entity instance published by Model is required` | Pass an Entity instance, for example `Currency(user_id=1, code="SEK")`. |
| A Filter, Order, or aggregate names an unknown Field | `Currency declares no Field colour` | Use a Field the Entity declares. |
| A Filter Combination is passed as text | `combination must be a FilterCombination member` | Pass `FilterCombination.AND` or `FilterCombination.OR`. |
| A Filter Operator is passed as text | `Filter operator must be a FilterOperator member` | Pass a `FilterOperator` member such as `FilterOperator.EQUALS`. |
| Update receives an Entity without an `id` | `Update requires an Entity instance that has an id` | Read the record first, change it, and pass that Entity instance. |
| A record id is not an integer | `a record id must be an integer` | Pass an integer `id`. |
| A Filter is malformed | `code: in requires a collection of values`, `code: contains requires a string value` | Give `IN` a list of values and `CONTAINS`, `STARTS_WITH`, and `ENDS_WITH` a string. |
| Sum receives a non-numeric Field | `code: Sum requires a numeric Field` | Use Sum on an integer, float, or decimal Field. |
| Execute Command receives positional parameters | `parameters must map each parameter name to its value` | Use `:name` markers in the command and pass a mapping. |
| A record repeats a Uniqueness Constraint | `UNIQUE constraint failed: broker.user_id, broker.name` | Change a value that takes part in the constraint, or Update the existing record. The wording comes from the Engine. |
| A record refers to a record that does not exist | `FOREIGN KEY constraint failed` | Add the referenced record first, or use an `id` that exists. The wording comes from the Engine. |
| A request runs before the tables exist | `no such table: user` | Run `uv run database create-tables`. |
| The `postgresql` Instance cannot connect | `connection failed: ... role "postgres" does not exist` | Create the role and database `config.yaml` names, or edit their entries, and set `PGPASSWORD` if a password is required. |
| The Configuration is invalid | `Instance postgresql names undeclared Engine oracle`, `default Instance postgresql is inactive`, `'XOR' is not a valid FilterCombination` | Make every Instance name a declared Engine, keep the default Instance active, and use only `AND` or `OR` and the directions `ascending` or `descending`. The Instance Enum lists the active Instances, so activating or deactivating one also changes the Enum. |
