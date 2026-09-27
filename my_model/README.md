# my_model

Reusable, technology-independent Domain Entity library for the Trading Assistant. Every meaningful domain concept (User, Trading Platform, Instance, Currency, Broker, Asset, Account Group, Account, Trailing Group, Trailing Rule, Partial Group, Partial Rule, Action Group, Action, Position) has exactly one Domain Entity here, realized as a SQLModel table model. Logic and Database both import these same Entity classes directly.

## Overview

Every Entity is flat, carries its own Fields and explicit Relationships (foreign keys), and shares one conversion behaviour through `Model_Foundation`. A minimal example using the `User` Entity:

```python
from my_model.model_interface import User

user = User(name="Admin", username="admin", password="secret", api_key="key")
data = user.to_json()          # {"id": None, "name": "Admin", "username": "admin", ...}
same_user = User.from_json(data)
```

## Interface

Every public Entity is reachable through `my_model.model_interface`. Fields are listed below without usage examples.

### User

| Field | Type | Nullable | Notes |
|---|---|---|---|
| id | integer | false | primary key, auto increment |
| name | string | false | unique |
| username | string | false | unique |
| password | string | false | sensitivity: password |
| api_key | string | false | sensitivity: sensitive |
| is_active | boolean | false | default: true |
| description | string | true | |

### Trading Platform

| Field | Type | Nullable | Notes |
|---|---|---|---|
| id | integer | false | primary key, auto increment |
| name | string | false | unique |
| code | string | false | |
| is_active | boolean | false | default: true |
| description | string | true | |

### Instance

| Field | Type | Nullable | Notes |
|---|---|---|---|
| id | integer | false | primary key, auto increment |
| user_id | integer | false | references User |
| trading_platform_id | integer | false | references Trading Platform |
| name | string | false | unique with user_id |
| ip | string | true | |
| username | string | true | |
| password | string | true | sensitivity: password |
| api_key | string | true | sensitivity: sensitive |
| is_active | boolean | false | default: true |
| description | string | true | |

### Currency

| Field | Type | Nullable | Notes |
|---|---|---|---|
| id | integer | false | primary key, auto increment |
| user_id | integer | false | references User |
| code | string(3) | false | unique with user_id |
| symbol | string | true | |
| country | string | true | |
| decimal_digits | integer | false | default: 2 |
| is_active | boolean | false | default: true |
| description | string | true | |

### Broker

| Field | Type | Nullable | Notes |
|---|---|---|---|
| id | integer | false | primary key, auto increment |
| name | string | false | unique with user_id |
| user_id | integer | false | references User |
| is_active | boolean | false | default: true |
| description | string | true | |

### Asset

| Field | Type | Nullable | Notes |
|---|---|---|---|
| id | integer | false | primary key, auto increment |
| broker_id | integer | false | references Broker, unique with symbol |
| symbol | string | false | unique with broker_id |
| category | string | false | |
| point_size | float | false | default: 0.0 |
| digits | integer | false | default: 0 |
| is_active | boolean | false | default: true |
| description | string | true | |

### Account Group

| Field | Type | Nullable | Notes |
|---|---|---|---|
| id | integer | false | primary key, auto increment |
| user_id | integer | false | references User |
| name | string | false | unique with user_id |
| is_active | boolean | false | default: true |
| description | string | true | |

### Account

| Field | Type | Nullable | Notes |
|---|---|---|---|
| id | integer | false | primary key, auto increment |
| name | string | false | unique |
| group_id | integer | false | references Account Group, unique with broker_id, instance_id |
| broker_id | integer | false | references Broker |
| instance_id | integer | false | references Instance |
| base_currency_id | integer | false | references Currency |
| username | string | false | |
| password | string | false | sensitivity: password |
| leverage | integer | false | |
| balance | decimal | false | default: 0 |
| account_type | string | false | |
| is_active | boolean | false | default: true |
| description | string | true | |

### Trailing Group

| Field | Type | Nullable | Notes |
|---|---|---|---|
| id | integer | false | primary key, auto increment |
| user_id | integer | false | references User |
| name | string | false | unique with user_id |
| is_active | boolean | false | default: true |
| description | string | true | |

### Trailing Rule

| Field | Type | Nullable | Notes |
|---|---|---|---|
| id | integer | false | primary key, auto increment |
| name | string | false | unique |
| trailing_group_id | integer | false | references Trailing Group, unique with trigger_percentage |
| trigger_percentage | decimal | false | unique with trailing_group_id |
| take_profit_adjustment | decimal | true | |
| stop_loss_adjustment | decimal | true | |
| is_active | boolean | false | default: true |
| description | string | true | |

### Partial Group

| Field | Type | Nullable | Notes |
|---|---|---|---|
| id | integer | false | primary key, auto increment |
| user_id | integer | false | references User |
| name | string | false | unique with user_id |
| is_active | boolean | false | default: true |
| description | string | true | |

### Partial Rule

| Field | Type | Nullable | Notes |
|---|---|---|---|
| id | integer | false | primary key, auto increment |
| name | string | false | unique |
| partial_group_id | integer | false | references Partial Group, unique with profit_percentage |
| profit_percentage | decimal | false | unique with partial_group_id |
| close_percentage | decimal | false | |
| is_active | boolean | false | default: true |
| description | string | true | |

### Action Group

| Field | Type | Nullable | Notes |
|---|---|---|---|
| id | integer | false | primary key, auto increment |
| user_id | integer | false | references User |
| name | string | false | unique with user_id |
| is_active | boolean | false | default: true |
| description | string | true | |

### Action

| Field | Type | Nullable | Notes |
|---|---|---|---|
| id | integer | false | primary key, auto increment |
| name | string | false | unique with action_group_id |
| action_group_id | integer | false | references Action Group |
| asset_id | integer | false | references Asset |
| account_id | integer | false | references Account |
| partial_group_id | integer | false | references Partial Group |
| trailing_group_id | integer | false | references Trailing Group |
| risk_by_reward | decimal | false | |
| take_profit | decimal | false | |
| stop_loss | decimal | false | |
| is_active | boolean | false | default: true |
| description | string | true | |

### Position

| Field | Type | Nullable | Notes |
|---|---|---|---|
| id | integer | false | primary key, auto increment |
| user_id | integer | false | references User |
| name | string | false | unique |
| trading_platform_id | integer | false | references Trading Platform |
| broker_id | integer | false | references Broker |
| account_id | integer | false | references Account |
| trailing_group_id | integer | false | references Trailing Group |
| partial_group_id | integer | false | references Partial Group |
| action_group_id | integer | false | references Action Group |
| action_id | integer | false | references Action |
| date | datetime | false | |
| volume | decimal | false | |
| profit | decimal | false | default: 0 |
| is_executed | boolean | false | default: false |
| order_type | string | false | |
| base_tp | decimal | false | |
| base_sl | decimal | false | |
| real_tp | decimal | false | |
| real_sl | decimal | false | |
| is_active | boolean | false | default: true |
| description | string | true | |

## Foundation

`Model_Foundation` gives every Entity two shared capabilities, with no Entity re-implementing them:

`to_json()` converts any Entity instance to its JSON-compatible representation:

```python
from my_model.model_interface import Currency

currency = Currency(user_id=1, code="USD", symbol="$", country="United States", decimal_digits=2)
payload = currency.to_json()
```

`from_json()` reconstructs an equivalent instance from that representation:

```python
rebuilt = Currency.from_json(payload)
```

Complete round-trip example using one Entity:

```python
from my_model.model_interface import User

user = User(name="Admin", username="admin", password="secret", api_key="key")
payload = user.to_json()
rebuilt = User.from_json(payload)
assert rebuilt.name == user.name and rebuilt.username == user.username
```

## Setup

```bash
uv sync
```

Installs Python 3.12 and this package's declared dependency, SQLModel.

## Run

`my_model` is a library, not an executable. Consuming Components import it directly:

```python
from my_model.model_interface import User, TradingPlatform  # any public Entity
```

To exercise it standalone during development:

```bash
uv run python -c "from my_model.model_interface import User; print(User(name='a', username='b', password='c', api_key='d').to_json())"
```

## Troubleshooting

- `ModuleNotFoundError: No module named 'my_model'` — run commands with `uv run`, or `uv sync` first so the project's virtual environment has the package installed in editable mode.
- `sqlalchemy.exc.NoReferencedTableError` or a table metadata error — occurs only when an Entity module is imported in isolation before the Entity it references; import Entities through `my_model.model_interface`, which imports every Entity in dependency order.
