# my_model

The independent Model layer for the Trading Assistant Target: flat, technology-independent Domain Entities shared by Logic and Database.

## Overview

Every Domain Entity is a public SQLModel class. For example, `User`:

```python
from my_model import User

admin = User(name="Admin", username="admin", password="secret", api_key="secret-key")
```

## Interface

Every public Entity, with its Fields.

### User

| Field | Type | Notes |
|---|---|---|
| id | integer | primary key |
| name | string | unique |
| username | string | unique |
| password | string | sensitivity marker: password |
| api_key | string | sensitivity marker: password |
| is_active | boolean | default true |
| description | string | optional |

### TradingPlatform

| Field | Type | Notes |
|---|---|---|
| id | integer | primary key |
| name | string | unique |
| code | string | |
| is_active | boolean | default true |
| description | string | optional |

### Instance

| Field | Type | Notes |
|---|---|---|
| id | integer | primary key |
| user_id | integer | references User |
| trading_platform_id | integer | references TradingPlatform |
| name | string | unique with user_id |
| ip | string | optional |
| username | string | optional |
| password | string | optional; sensitivity marker: password |
| api_key | string | optional; sensitivity marker: password |
| is_active | boolean | default true |
| description | string | optional |

### Currency

| Field | Type | Notes |
|---|---|---|
| id | integer | primary key |
| user_id | integer | references User |
| code | string (3) | unique with user_id |
| symbol | string | optional |
| country | string | optional |
| decimal_digits | integer | default 2 |
| is_active | boolean | default true |
| description | string | optional |

### Broker

| Field | Type | Notes |
|---|---|---|
| id | integer | primary key |
| name | string | unique with user_id |
| user_id | integer | references User |
| is_active | boolean | default true |
| description | string | optional |

### Asset

| Field | Type | Notes |
|---|---|---|
| id | integer | primary key |
| broker_id | integer | references Broker |
| symbol | string | unique with broker_id |
| category | string | |
| point_size | float | default 0.0 |
| digits | integer | default 0 |
| is_active | boolean | default true |
| description | string | optional |

### AccountGroup

| Field | Type | Notes |
|---|---|---|
| id | integer | primary key |
| user_id | integer | references User |
| name | string | unique with user_id |
| is_active | boolean | default true |
| description | string | optional |

### Account

| Field | Type | Notes |
|---|---|---|
| id | integer | primary key |
| name | string | unique |
| group_id | integer | references AccountGroup; unique with broker_id, instance_id |
| broker_id | integer | references Broker |
| instance_id | integer | references Instance |
| base_currency_id | integer | references Currency |
| username | string | |
| password | string | sensitivity marker: password |
| leverage | integer | |
| balance | decimal | default 0 |
| account_type | string | |
| is_active | boolean | default true |
| description | string | optional |

### TrailingGroup

| Field | Type | Notes |
|---|---|---|
| id | integer | primary key |
| user_id | integer | references User |
| name | string | unique with user_id |
| is_active | boolean | default true |
| description | string | optional |

### TrailingRule

| Field | Type | Notes |
|---|---|---|
| id | integer | primary key |
| name | string | unique |
| trailing_group_id | integer | references TrailingGroup; unique with trigger_percentage |
| trigger_percentage | decimal | |
| take_profit_adjustment | decimal | optional |
| stop_loss_adjustment | decimal | optional |
| is_active | boolean | default true |
| description | string | optional |

### PartialGroup

| Field | Type | Notes |
|---|---|---|
| id | integer | primary key |
| user_id | integer | references User |
| name | string | unique with user_id |
| is_active | boolean | default true |
| description | string | optional |

### PartialRule

| Field | Type | Notes |
|---|---|---|
| id | integer | primary key |
| name | string | unique |
| partial_group_id | integer | references PartialGroup; unique with profit_percentage |
| profit_percentage | decimal | |
| close_percentage | decimal | |
| is_active | boolean | default true |
| description | string | optional |

### ActionGroup

| Field | Type | Notes |
|---|---|---|
| id | integer | primary key |
| user_id | integer | references User |
| name | string | unique with user_id |
| is_active | boolean | default true |
| description | string | optional |

### Action

| Field | Type | Notes |
|---|---|---|
| id | integer | primary key |
| name | string | unique with action_group_id |
| action_group_id | integer | references ActionGroup |
| asset_id | integer | references Asset |
| account_id | integer | references Account |
| partial_group_id | integer | references PartialGroup |
| trailing_group_id | integer | references TrailingGroup |
| risk_by_reward | decimal | |
| take_profit | decimal | |
| stop_loss | decimal | |
| is_active | boolean | default true |
| description | string | optional |

### Position

| Field | Type | Notes |
|---|---|---|
| id | integer | primary key |
| user_id | integer | references User |
| name | string | unique |
| trading_platform_id | integer | references TradingPlatform |
| broker_id | integer | references Broker |
| account_id | integer | references Account |
| trailing_group_id | integer | references TrailingGroup |
| partial_group_id | integer | references PartialGroup |
| action_group_id | integer | references ActionGroup |
| action_id | integer | references Action |
| date | datetime | |
| volume | decimal | |
| profit | decimal | default 0 |
| is_executed | boolean | default false |
| order_type | string | |
| base_tp | decimal | |
| base_sl | decimal | |
| real_tp | decimal | |
| real_sl | decimal | |
| is_active | boolean | default true |
| description | string | optional |

## Foundation

`to_json()` converts an Entity instance to a JSON-compatible representation:

```python
data = admin.to_json()
```

`from_json()` constructs an Entity instance from a JSON-compatible representation:

```python
from my_model import User

rebuilt = User.from_json(data)
```

Complete example using both capabilities with one Entity:

```python
from my_model import User

admin = User(name="Admin", username="admin", password="secret", api_key="secret-key")
data = admin.to_json()
rebuilt = User.from_json(data)
assert rebuilt.name == admin.name
```

## Setup

```bash
python3.12 -m venv .venv
.venv/bin/pip install -e .
```

## Run

`my_model` is a library, not an executable. Import the Entities you need from `my_model`:

```python
from my_model import User, Account, Position
```

## Troubleshooting

- **`ValueError: Datetime values must have timezone information`** — `Position.date` requires a timezone-aware `datetime` (for example `datetime.now(timezone.utc)`), not a naive one.
- **Foreign key errors on insert** — create referenced Entities (for example `User`, `TradingPlatform`) and commit them before creating an Entity that references them by id.
