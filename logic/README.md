# Logic

Application Behaviour for the Trading Assistant. Logic is a reusable library: a consumer names an Operation on one Interface and receives an Outcome, and never learns which Components were involved, in what order, or how their answers were combined. It stores and retrieves the Entities published by Model through Database, applies the rules that depend on the operation, and protects credentials before they reach storage.

```python
from logic.interface import Logic

logic = Logic()
outcome = logic.entity.currency.get_by_id(1)
print(outcome.kind, outcome.value.code)
```

```text
success USD
```

## Interface

`logic.interface` is the only public Logic surface. Every other file, including every Service, is internal and is not a dependency of a consumer.

The Interface gathers Operations into Categories, organized first by Service and, inside the Entity Service, by Entity:

```text
Logic
├── entity                      Entity Service Category
│   ├── user                    one Class Category for each Entity Model publishes:
│   ├── trading_platform        user, trading_platform, instance, currency, broker, asset,
│   ├── instance                account_group, account, trailing_group, trailing_rule,
│   ├── ...                     partial_group, partial_rule, action_group, action, position
│   └── position                each offers add, get_by_id, update, delete, enable, disable,
│                               list, count, sum, min, max, and truncate
└── database                    Database Service Category
    └── execute_command
```

Import `Logic` once and create it. Creating it validates the runtime configuration (see Setup) and fails at once when a value is missing or malformed. The Interface also re-exports what a consumer needs to make a request: the Entities Model publishes, Database's request vocabulary (`Filter`, `FilterOperator`, `FilterCombination`, `Order`, `OrderDirection`, `CommandResult`), the Outcome types (`Outcome`, `OutcomeKind`), `Configuration`, `ConfigurationError`, and `WITHHELD`, the marker that stands in for a credential.

```python
from logic.interface import Logic, OutcomeKind, User

logic = Logic()
users = logic.entity.user
print(type(users).__name__, users.count().kind is OutcomeKind.SUCCESS)
```

```text
EntityOperations True
```

Every Operation answers with an `Outcome` that holds a `kind`, a `value` on success, and a safe `reason` on failure. The kinds are `success`, `not_found`, `invalid`, `conflict`, `broken_reference`, and `unavailable`. Each Operation's docstring states what it accepts, what it returns, and which failures it can produce.

## Services

Logic is composed of internal Services. Each Service keeps its files in its own directory and publishes its usable classes and Actions through its own Service Interface. The outward Interface gathers those Actions as Operations. A Service Interface is not a consumer boundary: import `logic.interface`, never a Service.

### Entity Service

The Entity Service handles every Database Operation that applies to an Entity. Its Service Interface publishes one Service for each Entity Model publishes, and each Service offers the same twelve Actions. The shared foundation the Services inherit from is private and is not published.

Handled Entities: User, Trading Platform, Instance, Currency, Broker, Asset, Account Group, Account, Trailing Group, Trailing Rule, Partial Group, Partial Rule, Action Group, Action, and Position.

Credential Fields need special care, so three Services add Behaviour of their own:

- **User** stores `password` and `api_key` as one-way hashes.
- **Instance** stores `password` and `api_key` encrypted with the configured secret.
- **Account** stores `password` encrypted, and refuses an Account whose credential equals a credential of the Instance it uses.

Logic never returns an original credential. Every record it returns holds `WITHHELD` (`"********"`) in each credential Field that has a value. To edit a record without changing a credential, send the record back with `WITHHELD` in that Field; the stored credential is kept. A credential Field cannot be used in a Filter, an Order, or a total. `WITHHELD` cannot be used when adding a record.

The examples below use the User Service as the pattern for every other Entity. They run in order and share `logic` and `user`.

**Add**

```python
from logic.interface import Logic, User

logic = Logic()
created = logic.entity.user.add(
    User(name="Ada", username="ada", password="a-placeholder-password", api_key="a-placeholder-key")
)
user = created.value
print(created.kind, user.id, user.password)
```

```text
success 2 ********
```

**Get by ID**

```python
found = logic.entity.user.get_by_id(user.id)
print(found.kind, found.value.username)
```

```text
success ada
```

**Update**

```python
user.description = "Swing trader"
updated = logic.entity.user.update(user)
print(updated.kind, updated.value.description)
```

```text
success Swing trader
```

**Disable**

```python
disabled = logic.entity.user.disable(user.id)
print(disabled.kind, disabled.value.is_active)
```

```text
success False
```

**Enable**

```python
enabled = logic.entity.user.enable(user.id)
print(enabled.kind, enabled.value.is_active)
```

```text
success True
```

**List**

```python
from logic.interface import Filter, FilterOperator, Order, OrderDirection

listed = logic.entity.user.list(
    filters=[Filter("username", FilterOperator.EQUALS, "ada")],
    orders=[Order("id", OrderDirection.DESCENDING)],
    limit=10,
)
print(listed.kind, [record.username for record in listed.value])
```

```text
success ['ada']
```

**Count**

```python
counted = logic.entity.user.count()
print(counted.kind, counted.value)
```

```text
success 2
```

**Sum**

```python
total = logic.entity.user.sum("id")
print(total.kind, total.value)
```

```text
success 3
```

**Min**

```python
smallest = logic.entity.user.min("id")
print(smallest.kind, smallest.value)
```

```text
success 1
```

**Max**

```python
largest = logic.entity.user.max("id")
print(largest.kind, largest.value)
```

```text
success 2
```

**Delete**

```python
deleted = logic.entity.user.delete(user.id)
print(deleted.kind, deleted.value)
```

```text
success True
```

**Truncate**

Truncate removes every record of an Entity. Here other records refer to the seeded User, so nothing is removed and the Outcome says why:

```python
refused = logic.entity.user.truncate()
print(refused.kind, logic.entity.user.count().value)
```

```text
broken_reference 1
```

### Database Service

The Database Service handles the one Database Operation that concerns no single Entity. Its Service Interface publishes `DatabaseService` with the Action `execute_command`, which the outward Interface offers as `logic.database.execute_command`. A command is attempted once, because repeating it could change data twice.

**Execute Command**

```python
result = logic.database.execute_command(
    "SELECT code FROM currency WHERE code = :code", {"code": "USD"}
)
print(result.kind, result.value.rows)
```

```text
success [{'code': 'USD'}]
```

## Setup

1. Install Python 3.14 and [uv](https://docs.astral.sh/uv/).
2. From the Logic directory, install the locked dependencies. Model and Database are found next to this directory:

   ```text
   uv sync
   ```

3. Prepare the Database Instance Logic will use. These are Database's own commands:

   ```text
   uv run database create-tables
   uv run database insert-initial-data
   ```

4. Supply the runtime values. Logic reads them from the environment when it is created and never stores them:

   | Value | Meaning |
   |---|---|
   | `LOGIC_CREDENTIAL_SECRET` | Secret that protects encrypted credentials; at least 32 characters. Keep it in a secret source and never in code or documentation. |
   | `LOGIC_DEPENDENCY_TIMEOUT_SECONDS` | Longest wait, in seconds, for one call into Database; a finite number above zero. |
   | `LOGIC_DEPENDENCY_RETRIES` | Most repeats of a safe or idempotent call after a temporary failure; a whole number of zero or more. |

   ```text
   export LOGIC_CREDENTIAL_SECRET="<a secret of at least 32 characters>"
   export LOGIC_DEPENDENCY_TIMEOUT_SECONDS=10
   export LOGIC_DEPENDENCY_RETRIES=2
   ```

   To supply the values from code instead, pass `Configuration(credential_secret, dependency_timeout_seconds, dependency_retries)` to `Logic`.

Changing the secret makes credentials that were encrypted with the old one unreadable to Logic, so keep it stable.

## Use

Create `Logic` once and call its Operations. Every Operation returns an `Outcome`; check `succeeded`, or match on `kind`, instead of catching errors:

```python
from logic.interface import Logic, OutcomeKind

logic = Logic()
outcome = logic.entity.user.get_by_id(9999)
match outcome.kind:
    case OutcomeKind.SUCCESS:
        print("found", outcome.value.username)
    case OutcomeKind.NOT_FOUND:
        print("not found:", outcome.reason)
    case _:
        print("failed:", outcome.kind, outcome.reason)
```

```text
not found: no User has that id
```

The Outcome kinds mean:

| Kind | Meaning |
|---|---|
| `success` | The Operation worked; `value` holds the result. |
| `not_found` | No record has the id that was requested. |
| `invalid` | The request is malformed, breaks a constraint Model declares, names a Field the Entity does not have, or breaks a Behaviour rule. |
| `conflict` | A stored record already holds one of the unique values. |
| `broken_reference` | The request refers to a record that does not exist, or the record is still referred to by another. |
| `unavailable` | The stored data could not be reached or did not answer in time. |

An unexpected failure is not turned into an Outcome; it surfaces as itself.

## Verify

With the Database Instance prepared and the runtime values supplied, this check confirms Logic works through its public Interface:

```python
from logic.interface import Logic

logic = Logic()
assert logic.entity.currency.get_by_id(1).succeeded
assert logic.entity.user.count().value >= 1
print("Logic is ready")
```

```text
Logic is ready
```

## Troubleshooting

| Problem | Message | Resolution |
|---|---|---|
| A runtime value is not supplied | `missing required runtime values: LOGIC_CREDENTIAL_SECRET, LOGIC_DEPENDENCY_TIMEOUT_SECONDS` | Supply every value listed in Setup before creating `Logic`. |
| A runtime value is malformed | `LOGIC_CREDENTIAL_SECRET must be text of at least 32 characters`, `LOGIC_DEPENDENCY_TIMEOUT_SECONDS must be a finite number of seconds above zero`, `LOGIC_DEPENDENCY_RETRIES must be a whole number of zero or more` | Correct the value the message names. The message never shows the value. |
| A record does not exist | `not_found`: `no User has that id` | Use an id that exists. |
| An Entity of the wrong type is passed | `invalid`: `a User is required` | Pass the Entity that belongs to the Service you called. |
| A value breaks a declared constraint | `invalid`: the message names the Entity and Field | Correct the named Field. |
| A Field name is unknown | `invalid`: `Database refused the request: User declares no Field colour` | Use a Field the Entity declares. |
| A credential Field is used to select or total | `invalid`: `a credential Field cannot be used to select, order, or total records` | Filter, order, and total on other Fields. |
| A new record carries the withheld marker | `invalid`: `a new record needs its credentials supplied` | Supply the real credentials when adding. |
| An Account reuses a credential of its Instance | `invalid`: `an Account cannot reuse a credential of its Instance` | Give the Account a credential of its own. |
| A unique value is already stored | `conflict`: `a stored record already holds one of the unique values` | Change a value that takes part in the constraint, or update the existing record. |
| A referred record is missing, or a record is still referred to | `broken_reference`: `the request refers to a record that does not exist, or the record is still referred to by another` | Add the referred record first, or remove the records that refer to this one before deleting or truncating it. |
| The stored data does not answer | `unavailable`: `the stored data did not answer within 10 seconds` | Check that Database is reachable, then retry; raise `LOGIC_DEPENDENCY_TIMEOUT_SECONDS` if the data is slow. |
| The tables do not exist | `unavailable`: `the stored data could not be reached` | Run `uv run database create-tables` and `uv run database insert-initial-data`. |
| A command is malformed | `invalid`: `Database refused the command as malformed` | Correct the command and pass parameters as a mapping for its `:name` markers. |
