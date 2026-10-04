# Entity Group

## Overview

Entity Group is the part of API that serves Entity Service over HTTP: every Entity has one Adapter, and every Action of that Entity has one Endpoint. A request reaches an Endpoint, the Endpoint calls the same Action on the Entity's Child Service through Logic, and the Action's result is the response. Nothing is added, wrapped, or retried, so a failure of the Action is a failure of the request. For example, this request lists the first five currencies:

```bash
curl -s -X POST http://127.0.0.1:8000/entity/currency/list -H 'Content-Type: application/json' -d '{"orders": [{"field": "id"}], "limit": 5}'
```

Every address below is shown beneath the Base URL (`http://127.0.0.1:8000` unless the API's configuration says otherwise; a configured key comes before `/entity`).

## Endpoints

Every Endpoint answers `POST`. Its address is `/entity/<entity>/<action>`, or `/entity/<entity>/<action>/{id}` when the Action takes an `id`. `id` is part of the address; every other parameter is a member of one JSON object in the request body. Parameters marked *optional* may be left out and then reach the Action as omitted. Each parameter has one form, shown here once:

- `id` (path): the record's integer identity.
- `entity` (body): the Entity as one JSON object whose keys are its Field names; decimals, dates, and datetimes are text; `id` is `null` when adding.
- `filters` (body): a list of conditions `{"field": <Field name>, "operator": <operator>, "value": <value>}`; the operators are EQUALS, NOT_EQUALS, GREATER_THAN, GREATER_OR_EQUAL, LESS_THAN, LESS_OR_EQUAL, IN (a list of values), CONTAINS, STARTS_WITH, ENDS_WITH, IS_NULL, and IS_NOT_NULL (the last two take no `value`).
- `combination` (body): how several conditions combine: `AND` or `OR`.
- `orders` (body): a list of orderings `{"field": <Field name>, "direction": "ASCENDING" or "DESCENDING"}`; the direction may be left out.
- `limit` (body): an integer; zero or below means no limit.
- `field` (body): the Field name an aggregate works on.
- `instance` (body): the name of a configured Database Instance, such as `SQLITE`; left out, the application picks its default.

A result is JSON: an Entity is its JSON object, a list is an array, a number is a number, a decimal or date is text, and a record that does not exist is `null`. The examples below follow the order of the Models and are meant to be run in order on a fresh installation: an example may refer to a record an earlier one added or to a record the application starts with. The destructive examples (`delete` and `truncate`) come last.

### User

| Action | Address | Parameters |
| --- | --- | --- |
| `add` | `/entity/user/add` | `entity` (body), `instance` (body, optional) |
| `update` | `/entity/user/update` | `entity` (body), `instance` (body, optional) |
| `get_by_id` | `/entity/user/get_by_id/{id}` | `id` (path), `instance` (body, optional) |
| `list` | `/entity/user/list` | `filters` (body, optional), `combination` (body, optional), `orders` (body, optional), `limit` (body, optional), `instance` (body, optional) |
| `enable` | `/entity/user/enable/{id}` | `id` (path), `instance` (body, optional) |
| `disable` | `/entity/user/disable/{id}` | `id` (path), `instance` (body, optional) |
| `count` | `/entity/user/count` | `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `sum` | `/entity/user/sum` | `field` (body), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `min` | `/entity/user/min` | `field` (body), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `max` | `/entity/user/max` | `field` (body), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `delete` | `/entity/user/delete/{id}` | `id` (path), `instance` (body, optional) |
| `truncate` | `/entity/user/truncate` | `instance` (body, optional) |

```bash
# add
curl -s -X POST http://127.0.0.1:8000/entity/user/add -H 'Content-Type: application/json' -d '{"entity": {"id": null, "name": "Analyst", "username": "analyst", "password": "example-password", "api_key": "example-api-key", "is_active": true, "description": null}}'
# update
curl -s -X POST http://127.0.0.1:8000/entity/user/update -H 'Content-Type: application/json' -d '{"entity": {"id": 2, "name": "Analyst", "username": "analyst", "password": "example-password", "api_key": "example-api-key", "is_active": true, "description": "Updated"}}'
# get_by_id
curl -s -X POST http://127.0.0.1:8000/entity/user/get_by_id/2 -H 'Content-Type: application/json' -d '{}'
# list
curl -s -X POST http://127.0.0.1:8000/entity/user/list -H 'Content-Type: application/json' -d '{"filters": [{"field": "id", "operator": "GREATER_THAN", "value": 0}], "orders": [{"field": "id", "direction": "DESCENDING"}], "limit": 5}'
# enable
curl -s -X POST http://127.0.0.1:8000/entity/user/enable/2 -H 'Content-Type: application/json' -d '{}'
# disable
curl -s -X POST http://127.0.0.1:8000/entity/user/disable/2 -H 'Content-Type: application/json' -d '{}'
# count
curl -s -X POST http://127.0.0.1:8000/entity/user/count -H 'Content-Type: application/json' -d '{"filters": [{"field": "id", "operator": "GREATER_THAN", "value": 0}], "combination": "AND"}'
# sum
curl -s -X POST http://127.0.0.1:8000/entity/user/sum -H 'Content-Type: application/json' -d '{"field": "id"}'
# min
curl -s -X POST http://127.0.0.1:8000/entity/user/min -H 'Content-Type: application/json' -d '{"field": "id"}'
# max
curl -s -X POST http://127.0.0.1:8000/entity/user/max -H 'Content-Type: application/json' -d '{"field": "id"}'
```

### TradingPlatform

| Action | Address | Parameters |
| --- | --- | --- |
| `add` | `/entity/trading_platform/add` | `entity` (body), `instance` (body, optional) |
| `update` | `/entity/trading_platform/update` | `entity` (body), `instance` (body, optional) |
| `get_by_id` | `/entity/trading_platform/get_by_id/{id}` | `id` (path), `instance` (body, optional) |
| `list` | `/entity/trading_platform/list` | `filters` (body, optional), `combination` (body, optional), `orders` (body, optional), `limit` (body, optional), `instance` (body, optional) |
| `enable` | `/entity/trading_platform/enable/{id}` | `id` (path), `instance` (body, optional) |
| `disable` | `/entity/trading_platform/disable/{id}` | `id` (path), `instance` (body, optional) |
| `count` | `/entity/trading_platform/count` | `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `sum` | `/entity/trading_platform/sum` | `field` (body), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `min` | `/entity/trading_platform/min` | `field` (body), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `max` | `/entity/trading_platform/max` | `field` (body), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `delete` | `/entity/trading_platform/delete/{id}` | `id` (path), `instance` (body, optional) |
| `truncate` | `/entity/trading_platform/truncate` | `instance` (body, optional) |

```bash
# add
curl -s -X POST http://127.0.0.1:8000/entity/trading_platform/add -H 'Content-Type: application/json' -d '{"entity": {"id": null, "name": "Example Exchange", "code": "example_exchange", "is_active": true, "description": null}}'
# update
curl -s -X POST http://127.0.0.1:8000/entity/trading_platform/update -H 'Content-Type: application/json' -d '{"entity": {"id": 3, "name": "Example Exchange", "code": "example_exchange", "is_active": true, "description": "Updated"}}'
# get_by_id
curl -s -X POST http://127.0.0.1:8000/entity/trading_platform/get_by_id/3 -H 'Content-Type: application/json' -d '{}'
# list
curl -s -X POST http://127.0.0.1:8000/entity/trading_platform/list -H 'Content-Type: application/json' -d '{"filters": [{"field": "id", "operator": "GREATER_THAN", "value": 0}], "orders": [{"field": "id", "direction": "DESCENDING"}], "limit": 5}'
# enable
curl -s -X POST http://127.0.0.1:8000/entity/trading_platform/enable/3 -H 'Content-Type: application/json' -d '{}'
# disable
curl -s -X POST http://127.0.0.1:8000/entity/trading_platform/disable/3 -H 'Content-Type: application/json' -d '{}'
# count
curl -s -X POST http://127.0.0.1:8000/entity/trading_platform/count -H 'Content-Type: application/json' -d '{"filters": [{"field": "id", "operator": "GREATER_THAN", "value": 0}], "combination": "AND"}'
# sum
curl -s -X POST http://127.0.0.1:8000/entity/trading_platform/sum -H 'Content-Type: application/json' -d '{"field": "id"}'
# min
curl -s -X POST http://127.0.0.1:8000/entity/trading_platform/min -H 'Content-Type: application/json' -d '{"field": "id"}'
# max
curl -s -X POST http://127.0.0.1:8000/entity/trading_platform/max -H 'Content-Type: application/json' -d '{"field": "id"}'
```

### Instance

| Action | Address | Parameters |
| --- | --- | --- |
| `add` | `/entity/instance/add` | `entity` (body), `instance` (body, optional) |
| `update` | `/entity/instance/update` | `entity` (body), `instance` (body, optional) |
| `get_by_id` | `/entity/instance/get_by_id/{id}` | `id` (path), `instance` (body, optional) |
| `list` | `/entity/instance/list` | `filters` (body, optional), `combination` (body, optional), `orders` (body, optional), `limit` (body, optional), `instance` (body, optional) |
| `enable` | `/entity/instance/enable/{id}` | `id` (path), `instance` (body, optional) |
| `disable` | `/entity/instance/disable/{id}` | `id` (path), `instance` (body, optional) |
| `count` | `/entity/instance/count` | `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `sum` | `/entity/instance/sum` | `field` (body), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `min` | `/entity/instance/min` | `field` (body), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `max` | `/entity/instance/max` | `field` (body), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `delete` | `/entity/instance/delete/{id}` | `id` (path), `instance` (body, optional) |
| `truncate` | `/entity/instance/truncate` | `instance` (body, optional) |

```bash
# add
curl -s -X POST http://127.0.0.1:8000/entity/instance/add -H 'Content-Type: application/json' -d '{"entity": {"id": null, "user_id": 1, "trading_platform_id": 1, "name": "Demo", "ip": "127.0.0.1", "username": "demo", "password": "example-password", "api_key": null, "is_active": true, "description": null}}'
# update
curl -s -X POST http://127.0.0.1:8000/entity/instance/update -H 'Content-Type: application/json' -d '{"entity": {"id": 2, "user_id": 1, "trading_platform_id": 1, "name": "Demo", "ip": "127.0.0.1", "username": "demo", "password": "example-password", "api_key": null, "is_active": true, "description": "Updated"}}'
# get_by_id
curl -s -X POST http://127.0.0.1:8000/entity/instance/get_by_id/2 -H 'Content-Type: application/json' -d '{}'
# list
curl -s -X POST http://127.0.0.1:8000/entity/instance/list -H 'Content-Type: application/json' -d '{"filters": [{"field": "id", "operator": "GREATER_THAN", "value": 0}], "orders": [{"field": "id", "direction": "DESCENDING"}], "limit": 5}'
# enable
curl -s -X POST http://127.0.0.1:8000/entity/instance/enable/2 -H 'Content-Type: application/json' -d '{}'
# disable
curl -s -X POST http://127.0.0.1:8000/entity/instance/disable/2 -H 'Content-Type: application/json' -d '{}'
# count
curl -s -X POST http://127.0.0.1:8000/entity/instance/count -H 'Content-Type: application/json' -d '{"filters": [{"field": "id", "operator": "GREATER_THAN", "value": 0}], "combination": "AND"}'
# sum
curl -s -X POST http://127.0.0.1:8000/entity/instance/sum -H 'Content-Type: application/json' -d '{"field": "id"}'
# min
curl -s -X POST http://127.0.0.1:8000/entity/instance/min -H 'Content-Type: application/json' -d '{"field": "id"}'
# max
curl -s -X POST http://127.0.0.1:8000/entity/instance/max -H 'Content-Type: application/json' -d '{"field": "id"}'
```

### Currency

| Action | Address | Parameters |
| --- | --- | --- |
| `add` | `/entity/currency/add` | `entity` (body), `instance` (body, optional) |
| `update` | `/entity/currency/update` | `entity` (body), `instance` (body, optional) |
| `get_by_id` | `/entity/currency/get_by_id/{id}` | `id` (path), `instance` (body, optional) |
| `list` | `/entity/currency/list` | `filters` (body, optional), `combination` (body, optional), `orders` (body, optional), `limit` (body, optional), `instance` (body, optional) |
| `enable` | `/entity/currency/enable/{id}` | `id` (path), `instance` (body, optional) |
| `disable` | `/entity/currency/disable/{id}` | `id` (path), `instance` (body, optional) |
| `count` | `/entity/currency/count` | `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `sum` | `/entity/currency/sum` | `field` (body), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `min` | `/entity/currency/min` | `field` (body), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `max` | `/entity/currency/max` | `field` (body), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `delete` | `/entity/currency/delete/{id}` | `id` (path), `instance` (body, optional) |
| `truncate` | `/entity/currency/truncate` | `instance` (body, optional) |

```bash
# add
curl -s -X POST http://127.0.0.1:8000/entity/currency/add -H 'Content-Type: application/json' -d '{"entity": {"id": null, "user_id": 1, "code": "SEK", "symbol": "kr", "country": "Sweden", "decimal_digits": 2, "is_active": true, "description": null}}'
# update
curl -s -X POST http://127.0.0.1:8000/entity/currency/update -H 'Content-Type: application/json' -d '{"entity": {"id": 9, "user_id": 1, "code": "SEK", "symbol": "kr", "country": "Sweden", "decimal_digits": 2, "is_active": true, "description": "Updated"}}'
# get_by_id
curl -s -X POST http://127.0.0.1:8000/entity/currency/get_by_id/9 -H 'Content-Type: application/json' -d '{}'
# list
curl -s -X POST http://127.0.0.1:8000/entity/currency/list -H 'Content-Type: application/json' -d '{"filters": [{"field": "id", "operator": "GREATER_THAN", "value": 0}], "orders": [{"field": "id", "direction": "DESCENDING"}], "limit": 5}'
# enable
curl -s -X POST http://127.0.0.1:8000/entity/currency/enable/9 -H 'Content-Type: application/json' -d '{}'
# disable
curl -s -X POST http://127.0.0.1:8000/entity/currency/disable/9 -H 'Content-Type: application/json' -d '{}'
# count
curl -s -X POST http://127.0.0.1:8000/entity/currency/count -H 'Content-Type: application/json' -d '{"filters": [{"field": "id", "operator": "GREATER_THAN", "value": 0}], "combination": "AND"}'
# sum
curl -s -X POST http://127.0.0.1:8000/entity/currency/sum -H 'Content-Type: application/json' -d '{"field": "id"}'
# min
curl -s -X POST http://127.0.0.1:8000/entity/currency/min -H 'Content-Type: application/json' -d '{"field": "id"}'
# max
curl -s -X POST http://127.0.0.1:8000/entity/currency/max -H 'Content-Type: application/json' -d '{"field": "id"}'
```

### Broker

| Action | Address | Parameters |
| --- | --- | --- |
| `add` | `/entity/broker/add` | `entity` (body), `instance` (body, optional) |
| `update` | `/entity/broker/update` | `entity` (body), `instance` (body, optional) |
| `get_by_id` | `/entity/broker/get_by_id/{id}` | `id` (path), `instance` (body, optional) |
| `list` | `/entity/broker/list` | `filters` (body, optional), `combination` (body, optional), `orders` (body, optional), `limit` (body, optional), `instance` (body, optional) |
| `enable` | `/entity/broker/enable/{id}` | `id` (path), `instance` (body, optional) |
| `disable` | `/entity/broker/disable/{id}` | `id` (path), `instance` (body, optional) |
| `count` | `/entity/broker/count` | `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `sum` | `/entity/broker/sum` | `field` (body), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `min` | `/entity/broker/min` | `field` (body), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `max` | `/entity/broker/max` | `field` (body), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `delete` | `/entity/broker/delete/{id}` | `id` (path), `instance` (body, optional) |
| `truncate` | `/entity/broker/truncate` | `instance` (body, optional) |

```bash
# add
curl -s -X POST http://127.0.0.1:8000/entity/broker/add -H 'Content-Type: application/json' -d '{"entity": {"id": null, "name": "Example Broker", "user_id": 1, "is_active": true, "description": null}}'
# update
curl -s -X POST http://127.0.0.1:8000/entity/broker/update -H 'Content-Type: application/json' -d '{"entity": {"id": 2, "name": "Example Broker", "user_id": 1, "is_active": true, "description": "Updated"}}'
# get_by_id
curl -s -X POST http://127.0.0.1:8000/entity/broker/get_by_id/2 -H 'Content-Type: application/json' -d '{}'
# list
curl -s -X POST http://127.0.0.1:8000/entity/broker/list -H 'Content-Type: application/json' -d '{"filters": [{"field": "id", "operator": "GREATER_THAN", "value": 0}], "orders": [{"field": "id", "direction": "DESCENDING"}], "limit": 5}'
# enable
curl -s -X POST http://127.0.0.1:8000/entity/broker/enable/2 -H 'Content-Type: application/json' -d '{}'
# disable
curl -s -X POST http://127.0.0.1:8000/entity/broker/disable/2 -H 'Content-Type: application/json' -d '{}'
# count
curl -s -X POST http://127.0.0.1:8000/entity/broker/count -H 'Content-Type: application/json' -d '{"filters": [{"field": "id", "operator": "GREATER_THAN", "value": 0}], "combination": "AND"}'
# sum
curl -s -X POST http://127.0.0.1:8000/entity/broker/sum -H 'Content-Type: application/json' -d '{"field": "id"}'
# min
curl -s -X POST http://127.0.0.1:8000/entity/broker/min -H 'Content-Type: application/json' -d '{"field": "id"}'
# max
curl -s -X POST http://127.0.0.1:8000/entity/broker/max -H 'Content-Type: application/json' -d '{"field": "id"}'
```

### Asset

| Action | Address | Parameters |
| --- | --- | --- |
| `add` | `/entity/asset/add` | `entity` (body), `instance` (body, optional) |
| `update` | `/entity/asset/update` | `entity` (body), `instance` (body, optional) |
| `get_by_id` | `/entity/asset/get_by_id/{id}` | `id` (path), `instance` (body, optional) |
| `list` | `/entity/asset/list` | `filters` (body, optional), `combination` (body, optional), `orders` (body, optional), `limit` (body, optional), `instance` (body, optional) |
| `enable` | `/entity/asset/enable/{id}` | `id` (path), `instance` (body, optional) |
| `disable` | `/entity/asset/disable/{id}` | `id` (path), `instance` (body, optional) |
| `count` | `/entity/asset/count` | `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `sum` | `/entity/asset/sum` | `field` (body), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `min` | `/entity/asset/min` | `field` (body), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `max` | `/entity/asset/max` | `field` (body), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `delete` | `/entity/asset/delete/{id}` | `id` (path), `instance` (body, optional) |
| `truncate` | `/entity/asset/truncate` | `instance` (body, optional) |

```bash
# add
curl -s -X POST http://127.0.0.1:8000/entity/asset/add -H 'Content-Type: application/json' -d '{"entity": {"id": null, "broker_id": 1, "symbol": "GBP/USD", "category": "Currency", "point_size": 0.0001, "digits": 5, "is_active": true, "description": null}}'
# update
curl -s -X POST http://127.0.0.1:8000/entity/asset/update -H 'Content-Type: application/json' -d '{"entity": {"id": 5, "broker_id": 1, "symbol": "GBP/USD", "category": "Currency", "point_size": 0.0001, "digits": 5, "is_active": true, "description": "Updated"}}'
# get_by_id
curl -s -X POST http://127.0.0.1:8000/entity/asset/get_by_id/5 -H 'Content-Type: application/json' -d '{}'
# list
curl -s -X POST http://127.0.0.1:8000/entity/asset/list -H 'Content-Type: application/json' -d '{"filters": [{"field": "id", "operator": "GREATER_THAN", "value": 0}], "orders": [{"field": "id", "direction": "DESCENDING"}], "limit": 5}'
# enable
curl -s -X POST http://127.0.0.1:8000/entity/asset/enable/5 -H 'Content-Type: application/json' -d '{}'
# disable
curl -s -X POST http://127.0.0.1:8000/entity/asset/disable/5 -H 'Content-Type: application/json' -d '{}'
# count
curl -s -X POST http://127.0.0.1:8000/entity/asset/count -H 'Content-Type: application/json' -d '{"filters": [{"field": "id", "operator": "GREATER_THAN", "value": 0}], "combination": "AND"}'
# sum
curl -s -X POST http://127.0.0.1:8000/entity/asset/sum -H 'Content-Type: application/json' -d '{"field": "id"}'
# min
curl -s -X POST http://127.0.0.1:8000/entity/asset/min -H 'Content-Type: application/json' -d '{"field": "id"}'
# max
curl -s -X POST http://127.0.0.1:8000/entity/asset/max -H 'Content-Type: application/json' -d '{"field": "id"}'
```

### AccountGroup

| Action | Address | Parameters |
| --- | --- | --- |
| `add` | `/entity/account_group/add` | `entity` (body), `instance` (body, optional) |
| `update` | `/entity/account_group/update` | `entity` (body), `instance` (body, optional) |
| `get_by_id` | `/entity/account_group/get_by_id/{id}` | `id` (path), `instance` (body, optional) |
| `list` | `/entity/account_group/list` | `filters` (body, optional), `combination` (body, optional), `orders` (body, optional), `limit` (body, optional), `instance` (body, optional) |
| `enable` | `/entity/account_group/enable/{id}` | `id` (path), `instance` (body, optional) |
| `disable` | `/entity/account_group/disable/{id}` | `id` (path), `instance` (body, optional) |
| `count` | `/entity/account_group/count` | `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `sum` | `/entity/account_group/sum` | `field` (body), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `min` | `/entity/account_group/min` | `field` (body), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `max` | `/entity/account_group/max` | `field` (body), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `delete` | `/entity/account_group/delete/{id}` | `id` (path), `instance` (body, optional) |
| `truncate` | `/entity/account_group/truncate` | `instance` (body, optional) |

```bash
# add
curl -s -X POST http://127.0.0.1:8000/entity/account_group/add -H 'Content-Type: application/json' -d '{"entity": {"id": null, "user_id": 1, "name": "Demo accounts", "is_active": true, "description": null}}'
# update
curl -s -X POST http://127.0.0.1:8000/entity/account_group/update -H 'Content-Type: application/json' -d '{"entity": {"id": 2, "user_id": 1, "name": "Demo accounts", "is_active": true, "description": "Updated"}}'
# get_by_id
curl -s -X POST http://127.0.0.1:8000/entity/account_group/get_by_id/2 -H 'Content-Type: application/json' -d '{}'
# list
curl -s -X POST http://127.0.0.1:8000/entity/account_group/list -H 'Content-Type: application/json' -d '{"filters": [{"field": "id", "operator": "GREATER_THAN", "value": 0}], "orders": [{"field": "id", "direction": "DESCENDING"}], "limit": 5}'
# enable
curl -s -X POST http://127.0.0.1:8000/entity/account_group/enable/2 -H 'Content-Type: application/json' -d '{}'
# disable
curl -s -X POST http://127.0.0.1:8000/entity/account_group/disable/2 -H 'Content-Type: application/json' -d '{}'
# count
curl -s -X POST http://127.0.0.1:8000/entity/account_group/count -H 'Content-Type: application/json' -d '{"filters": [{"field": "id", "operator": "GREATER_THAN", "value": 0}], "combination": "AND"}'
# sum
curl -s -X POST http://127.0.0.1:8000/entity/account_group/sum -H 'Content-Type: application/json' -d '{"field": "id"}'
# min
curl -s -X POST http://127.0.0.1:8000/entity/account_group/min -H 'Content-Type: application/json' -d '{"field": "id"}'
# max
curl -s -X POST http://127.0.0.1:8000/entity/account_group/max -H 'Content-Type: application/json' -d '{"field": "id"}'
```

### Account

| Action | Address | Parameters |
| --- | --- | --- |
| `add` | `/entity/account/add` | `entity` (body), `instance` (body, optional) |
| `update` | `/entity/account/update` | `entity` (body), `instance` (body, optional) |
| `get_by_id` | `/entity/account/get_by_id/{id}` | `id` (path), `instance` (body, optional) |
| `list` | `/entity/account/list` | `filters` (body, optional), `combination` (body, optional), `orders` (body, optional), `limit` (body, optional), `instance` (body, optional) |
| `enable` | `/entity/account/enable/{id}` | `id` (path), `instance` (body, optional) |
| `disable` | `/entity/account/disable/{id}` | `id` (path), `instance` (body, optional) |
| `count` | `/entity/account/count` | `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `sum` | `/entity/account/sum` | `field` (body), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `min` | `/entity/account/min` | `field` (body), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `max` | `/entity/account/max` | `field` (body), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `delete` | `/entity/account/delete/{id}` | `id` (path), `instance` (body, optional) |
| `truncate` | `/entity/account/truncate` | `instance` (body, optional) |

```bash
# add
curl -s -X POST http://127.0.0.1:8000/entity/account/add -H 'Content-Type: application/json' -d '{"entity": {"id": null, "name": "Acc-2", "group_id": 2, "broker_id": 1, "instance_id": 1, "base_currency_id": 1, "username": "demo", "password": "example-password", "leverage": 50, "balance": "1000.00", "account_type": "CFD", "is_active": true, "description": null}}'
# update
curl -s -X POST http://127.0.0.1:8000/entity/account/update -H 'Content-Type: application/json' -d '{"entity": {"id": 2, "name": "Acc-2", "group_id": 2, "broker_id": 1, "instance_id": 1, "base_currency_id": 1, "username": "demo", "password": "example-password", "leverage": 50, "balance": "1000.00", "account_type": "CFD", "is_active": true, "description": "Updated"}}'
# get_by_id
curl -s -X POST http://127.0.0.1:8000/entity/account/get_by_id/2 -H 'Content-Type: application/json' -d '{}'
# list
curl -s -X POST http://127.0.0.1:8000/entity/account/list -H 'Content-Type: application/json' -d '{"filters": [{"field": "id", "operator": "GREATER_THAN", "value": 0}], "orders": [{"field": "id", "direction": "DESCENDING"}], "limit": 5}'
# enable
curl -s -X POST http://127.0.0.1:8000/entity/account/enable/2 -H 'Content-Type: application/json' -d '{}'
# disable
curl -s -X POST http://127.0.0.1:8000/entity/account/disable/2 -H 'Content-Type: application/json' -d '{}'
# count
curl -s -X POST http://127.0.0.1:8000/entity/account/count -H 'Content-Type: application/json' -d '{"filters": [{"field": "id", "operator": "GREATER_THAN", "value": 0}], "combination": "AND"}'
# sum
curl -s -X POST http://127.0.0.1:8000/entity/account/sum -H 'Content-Type: application/json' -d '{"field": "id"}'
# min
curl -s -X POST http://127.0.0.1:8000/entity/account/min -H 'Content-Type: application/json' -d '{"field": "id"}'
# max
curl -s -X POST http://127.0.0.1:8000/entity/account/max -H 'Content-Type: application/json' -d '{"field": "id"}'
```

### TrailingGroup

| Action | Address | Parameters |
| --- | --- | --- |
| `add` | `/entity/trailing_group/add` | `entity` (body), `instance` (body, optional) |
| `update` | `/entity/trailing_group/update` | `entity` (body), `instance` (body, optional) |
| `get_by_id` | `/entity/trailing_group/get_by_id/{id}` | `id` (path), `instance` (body, optional) |
| `list` | `/entity/trailing_group/list` | `filters` (body, optional), `combination` (body, optional), `orders` (body, optional), `limit` (body, optional), `instance` (body, optional) |
| `enable` | `/entity/trailing_group/enable/{id}` | `id` (path), `instance` (body, optional) |
| `disable` | `/entity/trailing_group/disable/{id}` | `id` (path), `instance` (body, optional) |
| `count` | `/entity/trailing_group/count` | `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `sum` | `/entity/trailing_group/sum` | `field` (body), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `min` | `/entity/trailing_group/min` | `field` (body), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `max` | `/entity/trailing_group/max` | `field` (body), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `delete` | `/entity/trailing_group/delete/{id}` | `id` (path), `instance` (body, optional) |
| `truncate` | `/entity/trailing_group/truncate` | `instance` (body, optional) |

```bash
# add
curl -s -X POST http://127.0.0.1:8000/entity/trailing_group/add -H 'Content-Type: application/json' -d '{"entity": {"id": null, "user_id": 1, "name": "Tight", "is_active": true, "description": null}}'
# update
curl -s -X POST http://127.0.0.1:8000/entity/trailing_group/update -H 'Content-Type: application/json' -d '{"entity": {"id": 2, "user_id": 1, "name": "Tight", "is_active": true, "description": "Updated"}}'
# get_by_id
curl -s -X POST http://127.0.0.1:8000/entity/trailing_group/get_by_id/2 -H 'Content-Type: application/json' -d '{}'
# list
curl -s -X POST http://127.0.0.1:8000/entity/trailing_group/list -H 'Content-Type: application/json' -d '{"filters": [{"field": "id", "operator": "GREATER_THAN", "value": 0}], "orders": [{"field": "id", "direction": "DESCENDING"}], "limit": 5}'
# enable
curl -s -X POST http://127.0.0.1:8000/entity/trailing_group/enable/2 -H 'Content-Type: application/json' -d '{}'
# disable
curl -s -X POST http://127.0.0.1:8000/entity/trailing_group/disable/2 -H 'Content-Type: application/json' -d '{}'
# count
curl -s -X POST http://127.0.0.1:8000/entity/trailing_group/count -H 'Content-Type: application/json' -d '{"filters": [{"field": "id", "operator": "GREATER_THAN", "value": 0}], "combination": "AND"}'
# sum
curl -s -X POST http://127.0.0.1:8000/entity/trailing_group/sum -H 'Content-Type: application/json' -d '{"field": "id"}'
# min
curl -s -X POST http://127.0.0.1:8000/entity/trailing_group/min -H 'Content-Type: application/json' -d '{"field": "id"}'
# max
curl -s -X POST http://127.0.0.1:8000/entity/trailing_group/max -H 'Content-Type: application/json' -d '{"field": "id"}'
```

### TrailingRule

| Action | Address | Parameters |
| --- | --- | --- |
| `add` | `/entity/trailing_rule/add` | `entity` (body), `instance` (body, optional) |
| `update` | `/entity/trailing_rule/update` | `entity` (body), `instance` (body, optional) |
| `get_by_id` | `/entity/trailing_rule/get_by_id/{id}` | `id` (path), `instance` (body, optional) |
| `list` | `/entity/trailing_rule/list` | `filters` (body, optional), `combination` (body, optional), `orders` (body, optional), `limit` (body, optional), `instance` (body, optional) |
| `enable` | `/entity/trailing_rule/enable/{id}` | `id` (path), `instance` (body, optional) |
| `disable` | `/entity/trailing_rule/disable/{id}` | `id` (path), `instance` (body, optional) |
| `count` | `/entity/trailing_rule/count` | `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `sum` | `/entity/trailing_rule/sum` | `field` (body), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `min` | `/entity/trailing_rule/min` | `field` (body), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `max` | `/entity/trailing_rule/max` | `field` (body), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `delete` | `/entity/trailing_rule/delete/{id}` | `id` (path), `instance` (body, optional) |
| `truncate` | `/entity/trailing_rule/truncate` | `instance` (body, optional) |

```bash
# add
curl -s -X POST http://127.0.0.1:8000/entity/trailing_rule/add -H 'Content-Type: application/json' -d '{"entity": {"id": null, "name": "Trail at 50", "trailing_group_id": 1, "trigger_percentage": "50", "take_profit_adjustment": "1", "stop_loss_adjustment": null, "is_active": true, "description": null}}'
# update
curl -s -X POST http://127.0.0.1:8000/entity/trailing_rule/update -H 'Content-Type: application/json' -d '{"entity": {"id": 1, "name": "Trail at 50", "trailing_group_id": 1, "trigger_percentage": "50", "take_profit_adjustment": "1", "stop_loss_adjustment": null, "is_active": true, "description": "Updated"}}'
# get_by_id
curl -s -X POST http://127.0.0.1:8000/entity/trailing_rule/get_by_id/1 -H 'Content-Type: application/json' -d '{}'
# list
curl -s -X POST http://127.0.0.1:8000/entity/trailing_rule/list -H 'Content-Type: application/json' -d '{"filters": [{"field": "id", "operator": "GREATER_THAN", "value": 0}], "orders": [{"field": "id", "direction": "DESCENDING"}], "limit": 5}'
# enable
curl -s -X POST http://127.0.0.1:8000/entity/trailing_rule/enable/1 -H 'Content-Type: application/json' -d '{}'
# disable
curl -s -X POST http://127.0.0.1:8000/entity/trailing_rule/disable/1 -H 'Content-Type: application/json' -d '{}'
# count
curl -s -X POST http://127.0.0.1:8000/entity/trailing_rule/count -H 'Content-Type: application/json' -d '{"filters": [{"field": "id", "operator": "GREATER_THAN", "value": 0}], "combination": "AND"}'
# sum
curl -s -X POST http://127.0.0.1:8000/entity/trailing_rule/sum -H 'Content-Type: application/json' -d '{"field": "id"}'
# min
curl -s -X POST http://127.0.0.1:8000/entity/trailing_rule/min -H 'Content-Type: application/json' -d '{"field": "id"}'
# max
curl -s -X POST http://127.0.0.1:8000/entity/trailing_rule/max -H 'Content-Type: application/json' -d '{"field": "id"}'
```

### PartialGroup

| Action | Address | Parameters |
| --- | --- | --- |
| `add` | `/entity/partial_group/add` | `entity` (body), `instance` (body, optional) |
| `update` | `/entity/partial_group/update` | `entity` (body), `instance` (body, optional) |
| `get_by_id` | `/entity/partial_group/get_by_id/{id}` | `id` (path), `instance` (body, optional) |
| `list` | `/entity/partial_group/list` | `filters` (body, optional), `combination` (body, optional), `orders` (body, optional), `limit` (body, optional), `instance` (body, optional) |
| `enable` | `/entity/partial_group/enable/{id}` | `id` (path), `instance` (body, optional) |
| `disable` | `/entity/partial_group/disable/{id}` | `id` (path), `instance` (body, optional) |
| `count` | `/entity/partial_group/count` | `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `sum` | `/entity/partial_group/sum` | `field` (body), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `min` | `/entity/partial_group/min` | `field` (body), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `max` | `/entity/partial_group/max` | `field` (body), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `delete` | `/entity/partial_group/delete/{id}` | `id` (path), `instance` (body, optional) |
| `truncate` | `/entity/partial_group/truncate` | `instance` (body, optional) |

```bash
# add
curl -s -X POST http://127.0.0.1:8000/entity/partial_group/add -H 'Content-Type: application/json' -d '{"entity": {"id": null, "user_id": 1, "name": "Scale out", "is_active": true, "description": null}}'
# update
curl -s -X POST http://127.0.0.1:8000/entity/partial_group/update -H 'Content-Type: application/json' -d '{"entity": {"id": 2, "user_id": 1, "name": "Scale out", "is_active": true, "description": "Updated"}}'
# get_by_id
curl -s -X POST http://127.0.0.1:8000/entity/partial_group/get_by_id/2 -H 'Content-Type: application/json' -d '{}'
# list
curl -s -X POST http://127.0.0.1:8000/entity/partial_group/list -H 'Content-Type: application/json' -d '{"filters": [{"field": "id", "operator": "GREATER_THAN", "value": 0}], "orders": [{"field": "id", "direction": "DESCENDING"}], "limit": 5}'
# enable
curl -s -X POST http://127.0.0.1:8000/entity/partial_group/enable/2 -H 'Content-Type: application/json' -d '{}'
# disable
curl -s -X POST http://127.0.0.1:8000/entity/partial_group/disable/2 -H 'Content-Type: application/json' -d '{}'
# count
curl -s -X POST http://127.0.0.1:8000/entity/partial_group/count -H 'Content-Type: application/json' -d '{"filters": [{"field": "id", "operator": "GREATER_THAN", "value": 0}], "combination": "AND"}'
# sum
curl -s -X POST http://127.0.0.1:8000/entity/partial_group/sum -H 'Content-Type: application/json' -d '{"field": "id"}'
# min
curl -s -X POST http://127.0.0.1:8000/entity/partial_group/min -H 'Content-Type: application/json' -d '{"field": "id"}'
# max
curl -s -X POST http://127.0.0.1:8000/entity/partial_group/max -H 'Content-Type: application/json' -d '{"field": "id"}'
```

### PartialRule

| Action | Address | Parameters |
| --- | --- | --- |
| `add` | `/entity/partial_rule/add` | `entity` (body), `instance` (body, optional) |
| `update` | `/entity/partial_rule/update` | `entity` (body), `instance` (body, optional) |
| `get_by_id` | `/entity/partial_rule/get_by_id/{id}` | `id` (path), `instance` (body, optional) |
| `list` | `/entity/partial_rule/list` | `filters` (body, optional), `combination` (body, optional), `orders` (body, optional), `limit` (body, optional), `instance` (body, optional) |
| `enable` | `/entity/partial_rule/enable/{id}` | `id` (path), `instance` (body, optional) |
| `disable` | `/entity/partial_rule/disable/{id}` | `id` (path), `instance` (body, optional) |
| `count` | `/entity/partial_rule/count` | `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `sum` | `/entity/partial_rule/sum` | `field` (body), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `min` | `/entity/partial_rule/min` | `field` (body), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `max` | `/entity/partial_rule/max` | `field` (body), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `delete` | `/entity/partial_rule/delete/{id}` | `id` (path), `instance` (body, optional) |
| `truncate` | `/entity/partial_rule/truncate` | `instance` (body, optional) |

```bash
# add
curl -s -X POST http://127.0.0.1:8000/entity/partial_rule/add -H 'Content-Type: application/json' -d '{"entity": {"id": null, "name": "Close a quarter", "partial_group_id": 1, "profit_percentage": "50", "close_percentage": "25", "is_active": true, "description": null}}'
# update
curl -s -X POST http://127.0.0.1:8000/entity/partial_rule/update -H 'Content-Type: application/json' -d '{"entity": {"id": 1, "name": "Close a quarter", "partial_group_id": 1, "profit_percentage": "50", "close_percentage": "25", "is_active": true, "description": "Updated"}}'
# get_by_id
curl -s -X POST http://127.0.0.1:8000/entity/partial_rule/get_by_id/1 -H 'Content-Type: application/json' -d '{}'
# list
curl -s -X POST http://127.0.0.1:8000/entity/partial_rule/list -H 'Content-Type: application/json' -d '{"filters": [{"field": "id", "operator": "GREATER_THAN", "value": 0}], "orders": [{"field": "id", "direction": "DESCENDING"}], "limit": 5}'
# enable
curl -s -X POST http://127.0.0.1:8000/entity/partial_rule/enable/1 -H 'Content-Type: application/json' -d '{}'
# disable
curl -s -X POST http://127.0.0.1:8000/entity/partial_rule/disable/1 -H 'Content-Type: application/json' -d '{}'
# count
curl -s -X POST http://127.0.0.1:8000/entity/partial_rule/count -H 'Content-Type: application/json' -d '{"filters": [{"field": "id", "operator": "GREATER_THAN", "value": 0}], "combination": "AND"}'
# sum
curl -s -X POST http://127.0.0.1:8000/entity/partial_rule/sum -H 'Content-Type: application/json' -d '{"field": "id"}'
# min
curl -s -X POST http://127.0.0.1:8000/entity/partial_rule/min -H 'Content-Type: application/json' -d '{"field": "id"}'
# max
curl -s -X POST http://127.0.0.1:8000/entity/partial_rule/max -H 'Content-Type: application/json' -d '{"field": "id"}'
```

### ActionGroup

| Action | Address | Parameters |
| --- | --- | --- |
| `add` | `/entity/action_group/add` | `entity` (body), `instance` (body, optional) |
| `update` | `/entity/action_group/update` | `entity` (body), `instance` (body, optional) |
| `get_by_id` | `/entity/action_group/get_by_id/{id}` | `id` (path), `instance` (body, optional) |
| `list` | `/entity/action_group/list` | `filters` (body, optional), `combination` (body, optional), `orders` (body, optional), `limit` (body, optional), `instance` (body, optional) |
| `enable` | `/entity/action_group/enable/{id}` | `id` (path), `instance` (body, optional) |
| `disable` | `/entity/action_group/disable/{id}` | `id` (path), `instance` (body, optional) |
| `count` | `/entity/action_group/count` | `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `sum` | `/entity/action_group/sum` | `field` (body), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `min` | `/entity/action_group/min` | `field` (body), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `max` | `/entity/action_group/max` | `field` (body), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `delete` | `/entity/action_group/delete/{id}` | `id` (path), `instance` (body, optional) |
| `truncate` | `/entity/action_group/truncate` | `instance` (body, optional) |

```bash
# add
curl -s -X POST http://127.0.0.1:8000/entity/action_group/add -H 'Content-Type: application/json' -d '{"entity": {"id": null, "user_id": 1, "name": "Low risk", "is_active": true, "description": null}}'
# update
curl -s -X POST http://127.0.0.1:8000/entity/action_group/update -H 'Content-Type: application/json' -d '{"entity": {"id": 2, "user_id": 1, "name": "Low risk", "is_active": true, "description": "Updated"}}'
# get_by_id
curl -s -X POST http://127.0.0.1:8000/entity/action_group/get_by_id/2 -H 'Content-Type: application/json' -d '{}'
# list
curl -s -X POST http://127.0.0.1:8000/entity/action_group/list -H 'Content-Type: application/json' -d '{"filters": [{"field": "id", "operator": "GREATER_THAN", "value": 0}], "orders": [{"field": "id", "direction": "DESCENDING"}], "limit": 5}'
# enable
curl -s -X POST http://127.0.0.1:8000/entity/action_group/enable/2 -H 'Content-Type: application/json' -d '{}'
# disable
curl -s -X POST http://127.0.0.1:8000/entity/action_group/disable/2 -H 'Content-Type: application/json' -d '{}'
# count
curl -s -X POST http://127.0.0.1:8000/entity/action_group/count -H 'Content-Type: application/json' -d '{"filters": [{"field": "id", "operator": "GREATER_THAN", "value": 0}], "combination": "AND"}'
# sum
curl -s -X POST http://127.0.0.1:8000/entity/action_group/sum -H 'Content-Type: application/json' -d '{"field": "id"}'
# min
curl -s -X POST http://127.0.0.1:8000/entity/action_group/min -H 'Content-Type: application/json' -d '{"field": "id"}'
# max
curl -s -X POST http://127.0.0.1:8000/entity/action_group/max -H 'Content-Type: application/json' -d '{"field": "id"}'
```

### Action

| Action | Address | Parameters |
| --- | --- | --- |
| `add` | `/entity/action/add` | `entity` (body), `instance` (body, optional) |
| `update` | `/entity/action/update` | `entity` (body), `instance` (body, optional) |
| `get_by_id` | `/entity/action/get_by_id/{id}` | `id` (path), `instance` (body, optional) |
| `list` | `/entity/action/list` | `filters` (body, optional), `combination` (body, optional), `orders` (body, optional), `limit` (body, optional), `instance` (body, optional) |
| `enable` | `/entity/action/enable/{id}` | `id` (path), `instance` (body, optional) |
| `disable` | `/entity/action/disable/{id}` | `id` (path), `instance` (body, optional) |
| `count` | `/entity/action/count` | `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `sum` | `/entity/action/sum` | `field` (body), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `min` | `/entity/action/min` | `field` (body), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `max` | `/entity/action/max` | `field` (body), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `delete` | `/entity/action/delete/{id}` | `id` (path), `instance` (body, optional) |
| `truncate` | `/entity/action/truncate` | `instance` (body, optional) |

```bash
# add
curl -s -X POST http://127.0.0.1:8000/entity/action/add -H 'Content-Type: application/json' -d '{"entity": {"id": null, "name": "Example action", "action_group_id": 1, "asset_id": 1, "account_id": 1, "partial_group_id": 1, "trailing_group_id": 1, "risk_by_reward": "2", "take_profit": "2", "stop_loss": "1", "is_active": true, "description": null}}'
# update
curl -s -X POST http://127.0.0.1:8000/entity/action/update -H 'Content-Type: application/json' -d '{"entity": {"id": 2, "name": "Example action", "action_group_id": 1, "asset_id": 1, "account_id": 1, "partial_group_id": 1, "trailing_group_id": 1, "risk_by_reward": "2", "take_profit": "2", "stop_loss": "1", "is_active": true, "description": "Updated"}}'
# get_by_id
curl -s -X POST http://127.0.0.1:8000/entity/action/get_by_id/2 -H 'Content-Type: application/json' -d '{}'
# list
curl -s -X POST http://127.0.0.1:8000/entity/action/list -H 'Content-Type: application/json' -d '{"filters": [{"field": "id", "operator": "GREATER_THAN", "value": 0}], "orders": [{"field": "id", "direction": "DESCENDING"}], "limit": 5}'
# enable
curl -s -X POST http://127.0.0.1:8000/entity/action/enable/2 -H 'Content-Type: application/json' -d '{}'
# disable
curl -s -X POST http://127.0.0.1:8000/entity/action/disable/2 -H 'Content-Type: application/json' -d '{}'
# count
curl -s -X POST http://127.0.0.1:8000/entity/action/count -H 'Content-Type: application/json' -d '{"filters": [{"field": "id", "operator": "GREATER_THAN", "value": 0}], "combination": "AND"}'
# sum
curl -s -X POST http://127.0.0.1:8000/entity/action/sum -H 'Content-Type: application/json' -d '{"field": "id"}'
# min
curl -s -X POST http://127.0.0.1:8000/entity/action/min -H 'Content-Type: application/json' -d '{"field": "id"}'
# max
curl -s -X POST http://127.0.0.1:8000/entity/action/max -H 'Content-Type: application/json' -d '{"field": "id"}'
```

### Position

| Action | Address | Parameters |
| --- | --- | --- |
| `add` | `/entity/position/add` | `entity` (body), `instance` (body, optional) |
| `update` | `/entity/position/update` | `entity` (body), `instance` (body, optional) |
| `get_by_id` | `/entity/position/get_by_id/{id}` | `id` (path), `instance` (body, optional) |
| `list` | `/entity/position/list` | `filters` (body, optional), `combination` (body, optional), `orders` (body, optional), `limit` (body, optional), `instance` (body, optional) |
| `enable` | `/entity/position/enable/{id}` | `id` (path), `instance` (body, optional) |
| `disable` | `/entity/position/disable/{id}` | `id` (path), `instance` (body, optional) |
| `count` | `/entity/position/count` | `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `sum` | `/entity/position/sum` | `field` (body), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `min` | `/entity/position/min` | `field` (body), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `max` | `/entity/position/max` | `field` (body), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `delete` | `/entity/position/delete/{id}` | `id` (path), `instance` (body, optional) |
| `truncate` | `/entity/position/truncate` | `instance` (body, optional) |

```bash
# add
curl -s -X POST http://127.0.0.1:8000/entity/position/add -H 'Content-Type: application/json' -d '{"entity": {"id": null, "user_id": 1, "name": "Example position", "trading_platform_id": 1, "broker_id": 1, "account_id": 1, "trailing_group_id": 1, "partial_group_id": 1, "action_group_id": 1, "action_id": 1, "date": "2026-10-04T10:00:00+00:00", "volume": "0.10", "profit": "0", "is_executed": false, "order_type": "BUY", "base_tp": "1.2", "base_sl": "1.1", "real_tp": "1.2", "real_sl": "1.1", "is_active": true, "description": null}}'
# update
curl -s -X POST http://127.0.0.1:8000/entity/position/update -H 'Content-Type: application/json' -d '{"entity": {"id": 1, "user_id": 1, "name": "Example position", "trading_platform_id": 1, "broker_id": 1, "account_id": 1, "trailing_group_id": 1, "partial_group_id": 1, "action_group_id": 1, "action_id": 1, "date": "2026-10-04T10:00:00+00:00", "volume": "0.10", "profit": "0", "is_executed": false, "order_type": "BUY", "base_tp": "1.2", "base_sl": "1.1", "real_tp": "1.2", "real_sl": "1.1", "is_active": true, "description": "Updated"}}'
# get_by_id
curl -s -X POST http://127.0.0.1:8000/entity/position/get_by_id/1 -H 'Content-Type: application/json' -d '{}'
# list
curl -s -X POST http://127.0.0.1:8000/entity/position/list -H 'Content-Type: application/json' -d '{"filters": [{"field": "id", "operator": "GREATER_THAN", "value": 0}], "orders": [{"field": "id", "direction": "DESCENDING"}], "limit": 5}'
# enable
curl -s -X POST http://127.0.0.1:8000/entity/position/enable/1 -H 'Content-Type: application/json' -d '{}'
# disable
curl -s -X POST http://127.0.0.1:8000/entity/position/disable/1 -H 'Content-Type: application/json' -d '{}'
# count
curl -s -X POST http://127.0.0.1:8000/entity/position/count -H 'Content-Type: application/json' -d '{"filters": [{"field": "id", "operator": "GREATER_THAN", "value": 0}], "combination": "AND"}'
# sum
curl -s -X POST http://127.0.0.1:8000/entity/position/sum -H 'Content-Type: application/json' -d '{"field": "id"}'
# min
curl -s -X POST http://127.0.0.1:8000/entity/position/min -H 'Content-Type: application/json' -d '{"field": "id"}'
# max
curl -s -X POST http://127.0.0.1:8000/entity/position/max -H 'Content-Type: application/json' -d '{"field": "id"}'
```

### Delete

`delete` removes the record the address names and answers with it. These examples remove the records the examples above added, dependants first, because the Database refuses to remove a record another record still refers to.

```bash
# delete Position
curl -s -X POST http://127.0.0.1:8000/entity/position/delete/1 -H 'Content-Type: application/json' -d '{}'
# delete Action
curl -s -X POST http://127.0.0.1:8000/entity/action/delete/2 -H 'Content-Type: application/json' -d '{}'
# delete ActionGroup
curl -s -X POST http://127.0.0.1:8000/entity/action_group/delete/2 -H 'Content-Type: application/json' -d '{}'
# delete PartialRule
curl -s -X POST http://127.0.0.1:8000/entity/partial_rule/delete/1 -H 'Content-Type: application/json' -d '{}'
# delete PartialGroup
curl -s -X POST http://127.0.0.1:8000/entity/partial_group/delete/2 -H 'Content-Type: application/json' -d '{}'
# delete TrailingRule
curl -s -X POST http://127.0.0.1:8000/entity/trailing_rule/delete/1 -H 'Content-Type: application/json' -d '{}'
# delete TrailingGroup
curl -s -X POST http://127.0.0.1:8000/entity/trailing_group/delete/2 -H 'Content-Type: application/json' -d '{}'
# delete Account
curl -s -X POST http://127.0.0.1:8000/entity/account/delete/2 -H 'Content-Type: application/json' -d '{}'
# delete AccountGroup
curl -s -X POST http://127.0.0.1:8000/entity/account_group/delete/2 -H 'Content-Type: application/json' -d '{}'
# delete Asset
curl -s -X POST http://127.0.0.1:8000/entity/asset/delete/5 -H 'Content-Type: application/json' -d '{}'
# delete Broker
curl -s -X POST http://127.0.0.1:8000/entity/broker/delete/2 -H 'Content-Type: application/json' -d '{}'
# delete Currency
curl -s -X POST http://127.0.0.1:8000/entity/currency/delete/9 -H 'Content-Type: application/json' -d '{}'
# delete Instance
curl -s -X POST http://127.0.0.1:8000/entity/instance/delete/2 -H 'Content-Type: application/json' -d '{}'
# delete TradingPlatform
curl -s -X POST http://127.0.0.1:8000/entity/trading_platform/delete/3 -H 'Content-Type: application/json' -d '{}'
# delete User
curl -s -X POST http://127.0.0.1:8000/entity/user/delete/2 -H 'Content-Type: application/json' -d '{}'
```

### Truncate

`truncate` removes every record of an Entity and answers with how many it removed. These examples run last and dependants first, for the same reason: truncating an Entity whose records are still referred to fails with an error.

```bash
# truncate Position
curl -s -X POST http://127.0.0.1:8000/entity/position/truncate -H 'Content-Type: application/json' -d '{}'
# truncate Action
curl -s -X POST http://127.0.0.1:8000/entity/action/truncate -H 'Content-Type: application/json' -d '{}'
# truncate ActionGroup
curl -s -X POST http://127.0.0.1:8000/entity/action_group/truncate -H 'Content-Type: application/json' -d '{}'
# truncate PartialRule
curl -s -X POST http://127.0.0.1:8000/entity/partial_rule/truncate -H 'Content-Type: application/json' -d '{}'
# truncate PartialGroup
curl -s -X POST http://127.0.0.1:8000/entity/partial_group/truncate -H 'Content-Type: application/json' -d '{}'
# truncate TrailingRule
curl -s -X POST http://127.0.0.1:8000/entity/trailing_rule/truncate -H 'Content-Type: application/json' -d '{}'
# truncate TrailingGroup
curl -s -X POST http://127.0.0.1:8000/entity/trailing_group/truncate -H 'Content-Type: application/json' -d '{}'
# truncate Account
curl -s -X POST http://127.0.0.1:8000/entity/account/truncate -H 'Content-Type: application/json' -d '{}'
# truncate AccountGroup
curl -s -X POST http://127.0.0.1:8000/entity/account_group/truncate -H 'Content-Type: application/json' -d '{}'
# truncate Asset
curl -s -X POST http://127.0.0.1:8000/entity/asset/truncate -H 'Content-Type: application/json' -d '{}'
# truncate Broker
curl -s -X POST http://127.0.0.1:8000/entity/broker/truncate -H 'Content-Type: application/json' -d '{}'
# truncate Currency
curl -s -X POST http://127.0.0.1:8000/entity/currency/truncate -H 'Content-Type: application/json' -d '{}'
# truncate Instance
curl -s -X POST http://127.0.0.1:8000/entity/instance/truncate -H 'Content-Type: application/json' -d '{}'
# truncate TradingPlatform
curl -s -X POST http://127.0.0.1:8000/entity/trading_platform/truncate -H 'Content-Type: application/json' -d '{}'
# truncate User
curl -s -X POST http://127.0.0.1:8000/entity/user/truncate -H 'Content-Type: application/json' -d '{}'
```

## Use

1. Start API (see its documentation) and note its Base URL.
2. Choose the Entity and the Action, and form the address `<Base URL>/entity/<entity>/<action>`; add `/<id>` for an Action that takes an `id`.
3. Send a `POST` with `Content-Type: application/json` and a body that is one JSON object holding the Action's other parameters by name (`{}` when there are none).
4. Read the JSON response. A missing record answers `null`. A failure of the Action, or a body that does not fit the parameters, is answered as an error, never as a result.

```bash
curl -s -X POST http://127.0.0.1:8000/entity/broker/get_by_id/1 -H 'Content-Type: application/json' -d '{}'
```

## Verify

Each Entity has one Adapter and each Adapter has one Endpoint per Action, and nothing else is served beneath `/entity`. To see it:

1. Read the list of Entities and Actions from Logic's Interface (the Entity Service lists 15 Entities and every Child Service offers the same 12 Actions: `add`, `update`, `list`, `get_by_id`, `delete`, `enable`, `disable`, `count`, `sum`, `min`, `max`, and `truncate`).
2. For every Entity and Action, the address in the [Endpoints](#endpoints) tables answers; for example `POST /entity/user/count` answers a number.
3. An Action that does not exist, such as `/entity/user/archive`, an Entity that does not exist, such as `/entity/widget/list`, and `GET` on any Endpoint are not served (not found or method not allowed).

```bash
curl -s -o /dev/null -w '%{http_code}\n' -X POST http://127.0.0.1:8000/entity/user/count -H 'Content-Type: application/json' -d '{}'
curl -s -o /dev/null -w '%{http_code}\n' -X POST http://127.0.0.1:8000/entity/user/archive -H 'Content-Type: application/json' -d '{}'
```

The first prints `200` and the second `404`.
