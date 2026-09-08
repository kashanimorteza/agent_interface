# Model — the shared domain layer of Trading Assistant

`my_model` is where Trading Assistant says what its entities are. A user, a
currency, a broker, an account, an action, a position: each is defined once
here, and every other layer reads that definition instead of keeping its own.
That is what makes persistence, application logic and presentation agree on
what the data means.

## Purpose and boundaries

**This layer does:** define the domain entities, their fields, the connections
between them, the rules that constrain them, and the records the project must
contain when it begins.

**This layer does not:** store anything, call anything, or expose anything over
a network. It validates only what an entity can judge from its own values. A
rule that needs stored records — uniqueness across records, or the existence of
a referenced one — is *declared* here and enforced by the layer that holds the
records. A rule that needs an operation's context is enforced by application
logic. Producing the values the declared records leave to be generated belongs
to whichever layer stores them.

## Public interface

Everything supported is reachable from the package itself. Nothing inside it is
part of the promise.

```python
from my_model import Account, Currency, User, records_in_resolution_order
```

### Entities

`User`, `Currency`, `TradingPlatform`, `Broker`, `AccountGroup`, `Account`,
`Asset`, `TrailingGroup`, `TrailingRule`, `PartialGroup`, `PartialRule`,
`ActionGroup`, `Action`, `Position` — and `ENTITIES`, all of them in project
order.

Each entity validates its own values and carries its declaration:

```python
currency = Currency(name="US Dollar", code="USD", symbol="$", decimal_digits=2)

Currency.entity_fields            # every field, with its resolved properties
Currency.relationships            # what it connects to, and through which field
Currency.rules                    # every rule declared for it
Currency.rules_for(RuleScope.STORED_STATE)   # the ones another layer enforces
Account.credential_fields()       # {"password": CredentialStorage.ENCRYPTED}
Account.relationship_fields()     # {"group_id": ..., "broker_id": ...}
```

An entity refuses what it can tell is wrong on its own — a code that is not
three characters, a leverage that is not a number, a missing required
connection — and reports why. It never refuses something only stored records
could settle.

### Telling "not given" from "given as nothing"

Every entity carries a partial view, for an operation that changes only some
fields. Leaving a field out and setting it to nothing are different things
there, which is what a partial update needs:

```python
change = TrailingRule.Partial.model_validate({"take_profit_adjustment": None})
change.states("take_profit_adjustment")   # True — deliberately cleared
change.stated_fields()                    # only what was actually given
```

### Declared records

```python
declared_records()              # every starting record, keyed by entity
records_in_resolution_order()   # (entity, record) pairs, references first
unresolved_references()         # empty when every reference resolves
```

A reference in a declared record identifies a record of the entity it points at
by that record's position among the declarations, counting from one. The
identifiers themselves are assigned by whichever layer stores the records.

Where the project requires a value to be generated — the admin password, the
admin API key, the account credential — the record carries `GENERATE_SECURELY`
in its place. There is no credential value anywhere in this package, and
`InitialRecord.generated_fields()` says which values the storing layer must
produce.

### Declaration types

`FieldSpec`, `FieldType`, `Relationship`, `Cardinality`, `DomainRule`,
`RuleScope`, `CredentialStorage`, `InitialRecord`, `Generated`, `Entity`,
`PartialView`, `UNSET`, `is_stated`, `awaits_generation` — for a consumer that
reads definitions rather than instances, such as a layer deriving storage or a
transport representation from them.

## Dependencies

Python 3.14 and [Pydantic](https://docs.pydantic.dev) 2.13.5. Nothing else, and
no dependency on another layer of this project.

## Configuration

`model.yaml`, beside this file, holds the settings this layer owns. It owns
none: what an entity is belongs to the definitions, not to configuration, since
changing it would change what the project means rather than how it runs.

The layer requires no secret, so it keeps no private secret file. The
credentials it declares are fields of domain records, held by whichever layer
stores them, under the treatment the field declares.

Cross-layer bindings live in `application.yaml` at the project root. This layer
consumes nothing, so its bindings are empty; it appears there because it is what
the other layers bind *to*.

## Installation

The layer keeps its own isolated environment:

```bash
cd model
uv sync
```

Another layer in this project consumes it by local path rather than from a
registry:

```bash
uv add ./model          # from the consuming layer
```

## Usage

```python
from my_model import Account, CredentialStorage, records_in_resolution_order

account = Account(
    name="Acc-1",
    group_id=1,
    broker_id=1,
    base_currency_id=1,
    username="test",
    password="…",
    leverage=100,
    account_type="CFD",
)
account.balance                       # Decimal("0") — the declared default

# Before storing it, ask how its credential must be held.
Account.credential_fields()["password"] is CredentialStorage.ENCRYPTED

# Seeding a fresh system: read the records in an order where every reference
# it meets has already been seen.
for entity, record in records_in_resolution_order():
    values = record.declared_values()          # what is stated
    generate = record.generated_fields()       # what must be produced instead
```
