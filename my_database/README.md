# my_database

The independent Database layer for the Trading Assistant Target: persists every `my_model` Domain Entity through SQLite and publishes Database Operations to Logic through `Database`.

## Overview

`Database` is the only public layer. Every Operation receives an imported Entity class or Entity instance directly, never a Model name or identity:

```python
from my_database import Database
from my_model import User

admin = Database.add(User(name="Admin", username="admin", password="secret", api_key="secret-key"))
```

## Interface

Every published Operation, with one complete example.

### Add

Accepts an Entity instance for a new record; returns the created record.

```python
from my_database import Database
from my_model import TradingPlatform

platform = Database.add(TradingPlatform(name="Binance", code="binance"))
print(platform.id)
```

### Edit

Accepts an imported Entity class and record identifier; returns that record in editable form, or `None` (not found).

```python
editable = Database.edit(TradingPlatform, platform.id)
editable.description = "Crypto exchange"
```

### Update

Accepts an Entity instance containing its record identifier and changed values; returns the updated record.

```python
updated = Database.update(editable)
print(updated.description)
```

### List

Accepts an imported Entity class, optional filters, and optional field ordering; returns matching records.

```python
platforms = Database.list(TradingPlatform, filters={"is_active": True}, order_by="name")
```

### Delete

Accepts an imported Entity class and record identifier; returns the deletion outcome.

```python
outcome = Database.delete(TradingPlatform, platform.id)
print(outcome)  # {"deleted": True}
```

### Enable

Accepts an imported Entity class and record identifier; returns the enabled record.

```python
platform = Database.enable(TradingPlatform, platform.id)
```

### Disable

Accepts an imported Entity class and record identifier; returns the disabled record.

```python
platform = Database.disable(TradingPlatform, platform.id)
```

### Get by ID

Accepts an imported Entity class and record identifier; returns the matching record, or `None` (not found).

```python
platform = Database.get_by_id(TradingPlatform, platform.id)
```

### Count

Accepts an imported Entity class and optional filters; returns the number of matching records.

```python
active_count = Database.count(TradingPlatform, filters={"is_active": True})
```

### Sum

Accepts an imported Entity class, one numeric field, and optional filters; returns that field's total across matching records.

```python
from my_model import Broker

total = Database.sum(Broker, "id", filters={"user_id": admin.id})
```

### Min

Accepts an imported Entity class, one comparable field, and optional filters; returns the smallest matching value.

```python
smallest = Database.min(Broker, "id", filters={"user_id": admin.id})
```

### Max

Accepts an imported Entity class, one comparable field, and optional filters; returns the largest matching value.

```python
largest = Database.max(Broker, "id", filters={"user_id": admin.id})
```

### Truncate

Accepts an imported Entity class; removes all of its records while keeping its Table structure.

```python
Database.truncate(Broker)
```

### Execute Command

Accepts a SQL command and optional parameters; executes it through the selected Engine and returns its result. Its purpose need not concern one Entity.

```python
rows = Database.execute_command("SELECT COUNT(*) FROM broker WHERE user_id = :uid", {"uid": admin.id})
```

## Setup

```bash
uv sync
```

This installs `sqlmodel`, `alembic`, `pyyaml`, and the local `my_model` package (editable) into `my_database/.venv`.

## Run

Provision the default Instance (creates `data/application.db` with a Table for every `my_model` Entity):

```bash
uv run alembic upgrade head
```

Insert the Target-declared initial data (safe to re-run; skips when already present):

```bash
uv run python seed_initial_data.py
```

Use `Database` from any script or dependent Component after the default Instance is provisioned:

```python
from my_database import Database
from my_model import User

admins = Database.list(User, filters={"username": "admin"})
```

## Verify

Confirm every `my_model` Entity has a matching Table in the default Instance:

```bash
uv run python -c "
import sqlite3
con = sqlite3.connect('data/application.db')
cur = con.cursor()
cur.execute(\"select name from sqlite_master where type='table' and name != 'alembic_version'\")
print(sorted(r[0] for r in cur.fetchall()))
"
```

## Troubleshooting

- **`unable to open database file`** — the configured Database Directory (`data/`) does not exist yet. Create it (`mkdir -p data`) before the first `alembic upgrade head`, or use `Database`/`Data.create_all`, which creates it automatically.
- **`NameError: name 'sqlmodel' is not defined` in a generated migration** — `migrations/script.py.mako` imports `sqlmodel` for every new revision; if a migration was generated before that import existed, add `import sqlmodel` to its header manually.
- **Foreign key errors when seeding** — insert referenced Entities (for example `User`, `TradingPlatform`) before an Entity that references them by id; `seed_initial_data.py` already inserts in that order.
