# Database — the persistence layer of Trading Assistant

`my_database` stores the domain definitions the Model layer publishes. You work
with the entities you already know — `User`, `Account`, `Position` — and this
layer works out how each one is held, which rules its records must satisfy, and
where the data actually lives.

There is one way in: `Database`. Everything below it exists so that boundary can
keep its promises, and none of it is yours to depend on.

## Purpose and boundaries

**This layer does:** map every published definition to stored structure; keep the
whole structure rebuildable from a recorded, reversible history; enforce the
rules that only stored records can settle — uniqueness across records, and
references that resolve; transform every credential on its way in; hold the
declared starting records; and serve every definition through one set of
operations, with an explicit boundary for changes that belong together.

**This layer does not:** decide what the domain means. Fields, connections and
rules are the Model layer's, and this one only maps and enforces them. It holds
no application behaviour, no API and no other layer's secrets. A rule that needs
an operation's context belongs to the layer that has that context, not here.

## Public interface

```python
from my_database import Database

db = Database()
```

### Stored identities

Which databases exist, and which one is used when you name none:

```python
db.instances.identities()          # every identity you may select
db.instances.default               # the one used when you name none
db.instances.get("general")        # one by key; an unknown key is refused
```

An identity carries a key, a name, a purpose and the engine behind it — never a
connection and never a secret. Pass one (or its key) as `instance=` to any
operation. Naming an Instance nobody declared is refused rather than quietly
answered with the default.

### Operations

The same five work for every definition. You pass the definition itself, not its
name:

```python
from my_model import Currency

stored  = db.create(Currency, {"name": "Swedish Krona", "code": "SEK", "decimal_digits": 2})
one     = db.read(Currency, {"code": "SEK"})
active  = db.list(Currency, {"status": True}, limit=10, order_by="code")
changed = db.update(Currency, {"code": "SEK"}, {"symbol": "kr"})
removed = db.delete(Currency, {"code": "SEK"})
```

An update changes only the fields it states: a field you leave out keeps its
value, and one you state as `None` is cleared where the definition allows it.
That difference comes from the Model layer's partial view, so you can pass one
of those directly.

What comes back is the definition's own partial view **without its credential
fields**. That is deliberate: a credential's stored form never leaves this
layer.

### Enabling and disabling

```python
from my_database import DISABLE, ENABLE

db.set_status(Currency, {"code": "JPY"}, DISABLE)
```

Only those two actions, and only for a definition that declares a `status`
field. Anything else is refused.

### Using a credential without receiving it

```python
from my_model import User

attempt = "the value someone typed"
db.credential_matches(User, {"username": "admin"}, "password", attempt)
```

This answers yes or no. It never hands back the credential, and it works for the
one-way treatments too — checking is what they are for.

### Changes that belong together

```python
from my_model import Account, Broker

with db.transaction() as unit:
    broker = unit.create(Broker, {"name": "New broker", "user_id": 1, "trading_platform_id": 1})
    unit.create(Account, {
        "name": "Acc-2", "group_id": 1, "broker_id": broker.stated_fields()["id"],
        "base_currency_id": 1, "username": "u", "password": "…",
        "leverage": 100, "account_type": "CFD",
    })
```

Either both records exist afterwards or neither does. Raise anything inside the
group, or call `unit.cancel()`, and none of it stands. A write outside a group is
atomic on its own.

### The declared starting records

```python
db.seed()   # SeedOutcome(stored=…, already_present=…)
```

Stores the records the definitions declare, in an order where every reference
already exists. Safe to run again: it recognises what is already there, and a
value it generated the first time is left alone.

### Controlled commands

For the little that the operations above cannot express:

```python
result = db.execute(
    "select code, count(*) as used from currencies group by code",
    {},
)
result.rows
```

Values travel as parameters and stay values. Structural change is refused —
that belongs to the recorded history alone. So is anything that would read or
write a credential column, or return every column of a table that has one. A
command that changes data is judged by the definitions it touched before its
changes stand, in the same unit of work, and undone if they do not hold. A
command written for one engine's dialect says so with `engine_specific=`.

## Internal, and not yours to depend on

`storage_adapter` (the engine, the connections, the settings), `data_logic` (the
mapping, the pipeline, the credential treatments) and `history` (the recorded
structural changes) are internal. They are reachable only from inside this
package and are absent from everything above. If you find yourself wanting one
of them, the boundary is missing something — say so, rather than reaching
around it.

## Dependencies

Python 3.14, the shared `my_model` layer, SQLAlchemy 2.0.52, Alembic 1.19.2,
cryptography 50.0.1 and PyYAML 6.0.3.

The Preferences name a reversible at-rest treatment and where its key comes
from, but no library for it. `cryptography` is this layer's choice for that.

## Configuration

`database.yaml`, beside this file, holds the settings this layer owns: which
engines it has adapters for, which Instances it offers, and which is the
default. It is checked before anything is served — an Instance naming an engine
with no adapter, a missing required setting, or a default naming nothing all
stop the layer rather than surfacing later on someone's first write.

Secrets are named there and valued only in `.env` beside it, which is never
committed. `.env.example` lists the names. The runtime environment overrides the
file for a name this layer declares. A required secret that is absent is
reported by name; nothing is substituted for it.

Cross-layer bindings — what this layer consumes and offers — live in
`application.yaml` at the project root, not here.

Under the file-backed engine this project runs on, data lives under `data/`
beside this file, resolved from the layer's own location rather than from
wherever you happen to run. It is not committed.

## Installation

```bash
cd database
uv sync
cp .env.example .env      # then fill in the key
uv run alembic upgrade head
```

The last command builds the whole structure from the recorded history. Reverse
it with `uv run alembic downgrade base`, which leaves nothing behind.

A consuming layer takes this one by local path:

```bash
uv add ./database
```

## Usage

```python
from my_model import Account, Asset, Currency
from my_database import Database

db = Database()
db.seed()

dollar = db.read(Currency, {"code": "USD"})
gold   = db.read(Asset, {"symbol": "XAU/USD"})

account = db.read(Account, {"name": "Acc-1"})
account.stated_fields()["balance"]        # the stored balance
"password" in account.stated_fields()     # False — credentials do not come back

db.close()
```
