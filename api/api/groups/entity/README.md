# Entity Group

## Overview

Entity Group is the API Group that serves Entity Service over HTTP. Every Entity has one Adapter, and every Adapter has one Endpoint for each Action of that Entity's Child Service; an Endpoint calls its Action and returns the result and the errors unchanged, so the Group adds no behaviour of its own. Every Endpoint is served at the Base URL followed by `/entity`, the Adapter segment and the Endpoint path.

```bash
# Run from the API directory; the Base URL, with its key, is the url value of config.yaml.
API=$(grep '^url:' config.yaml | cut -d' ' -f2)
curl -s "$API/entity/currency/get_by_id/1"
```

## Endpoints

Each Entity below has a table of its Endpoints with the Method, the Path and the Parameters of each, and one Python example that calls every Endpoint of that Adapter. The examples are run from the API directory with `uv run python`, against a running API, and read the Base URL from `config.yaml`.

Every Adapter has the same twelve Endpoints, because every Child Service has the same twelve Actions. A Parameter has the name, the requirement and the default of the Action's parameter, and it sits where the API places it: `id` in the path, every other simple Parameter in the query of a `GET` or `DELETE` and in the JSON body of a `POST`, `PUT` or `PATCH`, and every Action with a Parameter that a query cannot carry (an Entity, filters or orders) is a `POST` unless its verb makes it a `PUT`. A body Parameter is a member of one JSON object, named like the Parameter. Parameters that are not simple travel in one form for every Entity:

| Parameter | Form |
| --- | --- |
| `entity` | a JSON object of the Entity's Fields, as the Entity's own JSON text gives it; `update` takes the stored `id` in it, `add` takes none |
| `filters` | a list of `{"field": <Field name>, "operator": <operator name>, "value": <value>}`; `value` is absent for `IS_NULL` and `IS_NOT_NULL` and a list for `IN`; a decimal, a datetime or a uuid is sent as its text |
| `orders` | a list of `{"field": <Field name>, "direction": "ASCENDING" or "DESCENDING"}`; the direction is `ASCENDING` when absent |
| `combination` | `AND` or `OR` |
| `field` | the name of a Field of the Entity |
| `instance` | the name of a database Instance, such as `SQLITE`; the default Instance when absent |
| `limit` | an integer; zero or negative means no limit |

The operator names are `EQUALS`, `NOT_EQUALS`, `GREATER_THAN`, `GREATER_OR_EQUAL`, `LESS_THAN`, `LESS_OR_EQUAL`, `IN`, `CONTAINS`, `STARTS_WITH`, `ENDS_WITH`, `IS_NULL` and `IS_NOT_NULL`. A result is the Action's result as JSON: an Entity as an object holding every Field, a list as an array, a count or a total as a number, a record that does not exist as `null`. An error is Problem Details (`application/problem+json`) whose `type` is the error's class name.

### User

Segment `user`; every Endpoint below is served at the Base URL followed by `/entity/user`.

| Action | Method | Path | Parameters |
| --- | --- | --- | --- |
| `add` | `POST` | `/entity/user/add` | `entity` (body, required), `instance` (body, optional) |
| `update` | `PUT` | `/entity/user/update` | `entity` (body, required), `instance` (body, optional) |
| `list` | `POST` | `/entity/user/list` | `filters` (body, optional), `combination` (body, optional), `orders` (body, optional), `limit` (body, optional), `instance` (body, optional) |
| `get_by_id` | `GET` | `/entity/user/get_by_id/{id}` | `id` (path, required), `instance` (query, optional) |
| `delete` | `DELETE` | `/entity/user/delete/{id}` | `id` (path, required), `instance` (query, optional) |
| `enable` | `PATCH` | `/entity/user/enable/{id}` | `id` (path, required), `instance` (body, optional) |
| `disable` | `PATCH` | `/entity/user/disable/{id}` | `id` (path, required), `instance` (body, optional) |
| `count` | `POST` | `/entity/user/count` | `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `sum` | `POST` | `/entity/user/sum` | `field` (body, required), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `min` | `POST` | `/entity/user/min` | `field` (body, required), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `max` | `POST` | `/entity/user/max` | `field` (body, required), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `truncate` | `DELETE` | `/entity/user/truncate` | `instance` (query, optional) |

One example runs every Endpoint of the User Adapter in turn. It adds a record, reads it, changes it, queries it, disables and enables it and deletes it again, leaving the data as it was. The final truncate step then empties the whole User table (or is refused while other records refer to it), so run that step only on a table you mean to empty.

```python
import httpx
import yaml

api = yaml.safe_load(open("config.yaml"))["url"]
client = httpx.Client(base_url=f"{api}/entity/user")

new = {
    "name": "example",
    "username": "example",
    "password": "placeholder",
    "api_key": "placeholder",
    "is_active": True,
    "description": None,
}

# add: POST /add
added = client.post("/add", json={"entity": new}).json()
print(added)

# get_by_id: GET /get_by_id/{id}
print(client.get(f"/get_by_id/{added['id']}").json())

# update: PUT /update
added["description"] = "Changed by the example"
print(client.put("/update", json={"entity": added}).json())

# list: POST /list
only = [{"field": "id", "operator": "EQUALS", "value": added["id"]}]
print(
    client.post(
        "/list",
        json={
            "filters": only,
            "orders": [{"field": "id", "direction": "DESCENDING"}],
            "limit": 5,
        },
    ).json()
)

# count: POST /count
print(client.post("/count", json={"filters": only}).json())

# sum, min and max: POST /sum, /min, /max
print(client.post("/sum", json={"field": "id", "filters": only}).json())
print(client.post("/min", json={"field": "id", "filters": only}).json())
print(client.post("/max", json={"field": "id", "filters": only}).json())

# disable and enable: PATCH /disable/{id}, /enable/{id}
print(client.patch(f"/disable/{added['id']}").json()["is_active"])
print(
    client.patch(f"/enable/{added['id']}", json={"instance": "SQLITE"}).json()[
        "is_active"
    ]
)

# delete: DELETE /delete/{id}
print(client.delete(f"/delete/{added['id']}").json()["id"])

# truncate: DELETE /truncate removes every record of this Entity, or is refused while other records refer to them.
print(client.delete("/truncate").status_code)
```

### Trading Platform

Segment `trading_platform`; every Endpoint below is served at the Base URL followed by `/entity/trading_platform`.

| Action | Method | Path | Parameters |
| --- | --- | --- | --- |
| `add` | `POST` | `/entity/trading_platform/add` | `entity` (body, required), `instance` (body, optional) |
| `update` | `PUT` | `/entity/trading_platform/update` | `entity` (body, required), `instance` (body, optional) |
| `list` | `POST` | `/entity/trading_platform/list` | `filters` (body, optional), `combination` (body, optional), `orders` (body, optional), `limit` (body, optional), `instance` (body, optional) |
| `get_by_id` | `GET` | `/entity/trading_platform/get_by_id/{id}` | `id` (path, required), `instance` (query, optional) |
| `delete` | `DELETE` | `/entity/trading_platform/delete/{id}` | `id` (path, required), `instance` (query, optional) |
| `enable` | `PATCH` | `/entity/trading_platform/enable/{id}` | `id` (path, required), `instance` (body, optional) |
| `disable` | `PATCH` | `/entity/trading_platform/disable/{id}` | `id` (path, required), `instance` (body, optional) |
| `count` | `POST` | `/entity/trading_platform/count` | `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `sum` | `POST` | `/entity/trading_platform/sum` | `field` (body, required), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `min` | `POST` | `/entity/trading_platform/min` | `field` (body, required), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `max` | `POST` | `/entity/trading_platform/max` | `field` (body, required), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `truncate` | `DELETE` | `/entity/trading_platform/truncate` | `instance` (query, optional) |

One example runs every Endpoint of the Trading Platform Adapter in turn. It adds a record, reads it, changes it, queries it, disables and enables it and deletes it again, leaving the data as it was. The final truncate step then empties the whole Trading Platform table (or is refused while other records refer to it), so run that step only on a table you mean to empty.

```python
import httpx
import yaml

api = yaml.safe_load(open("config.yaml"))["url"]
client = httpx.Client(base_url=f"{api}/entity/trading_platform")

new = {
    "name": "Example Platform",
    "code": "example",
    "is_active": True,
    "description": None,
}

# add: POST /add
added = client.post("/add", json={"entity": new}).json()
print(added)

# get_by_id: GET /get_by_id/{id}
print(client.get(f"/get_by_id/{added['id']}").json())

# update: PUT /update
added["description"] = "Changed by the example"
print(client.put("/update", json={"entity": added}).json())

# list: POST /list
only = [{"field": "id", "operator": "EQUALS", "value": added["id"]}]
print(
    client.post(
        "/list",
        json={
            "filters": only,
            "orders": [{"field": "id", "direction": "DESCENDING"}],
            "limit": 5,
        },
    ).json()
)

# count: POST /count
print(client.post("/count", json={"filters": only}).json())

# sum, min and max: POST /sum, /min, /max
print(client.post("/sum", json={"field": "id", "filters": only}).json())
print(client.post("/min", json={"field": "id", "filters": only}).json())
print(client.post("/max", json={"field": "id", "filters": only}).json())

# disable and enable: PATCH /disable/{id}, /enable/{id}
print(client.patch(f"/disable/{added['id']}").json()["is_active"])
print(
    client.patch(f"/enable/{added['id']}", json={"instance": "SQLITE"}).json()[
        "is_active"
    ]
)

# delete: DELETE /delete/{id}
print(client.delete(f"/delete/{added['id']}").json()["id"])

# truncate: DELETE /truncate removes every record of this Entity, or is refused while other records refer to them.
print(client.delete("/truncate").status_code)
```

### Instance

Segment `instance`; every Endpoint below is served at the Base URL followed by `/entity/instance`.

| Action | Method | Path | Parameters |
| --- | --- | --- | --- |
| `add` | `POST` | `/entity/instance/add` | `entity` (body, required), `instance` (body, optional) |
| `update` | `PUT` | `/entity/instance/update` | `entity` (body, required), `instance` (body, optional) |
| `list` | `POST` | `/entity/instance/list` | `filters` (body, optional), `combination` (body, optional), `orders` (body, optional), `limit` (body, optional), `instance` (body, optional) |
| `get_by_id` | `GET` | `/entity/instance/get_by_id/{id}` | `id` (path, required), `instance` (query, optional) |
| `delete` | `DELETE` | `/entity/instance/delete/{id}` | `id` (path, required), `instance` (query, optional) |
| `enable` | `PATCH` | `/entity/instance/enable/{id}` | `id` (path, required), `instance` (body, optional) |
| `disable` | `PATCH` | `/entity/instance/disable/{id}` | `id` (path, required), `instance` (body, optional) |
| `count` | `POST` | `/entity/instance/count` | `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `sum` | `POST` | `/entity/instance/sum` | `field` (body, required), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `min` | `POST` | `/entity/instance/min` | `field` (body, required), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `max` | `POST` | `/entity/instance/max` | `field` (body, required), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `truncate` | `DELETE` | `/entity/instance/truncate` | `instance` (query, optional) |

One example runs every Endpoint of the Instance Adapter in turn. It adds a record, reads it, changes it, queries it, disables and enables it and deletes it again, leaving the data as it was. The final truncate step then empties the whole Instance table (or is refused while other records refer to it), so run that step only on a table you mean to empty.

```python
import httpx
import yaml

api = yaml.safe_load(open("config.yaml"))["url"]
client = httpx.Client(base_url=f"{api}/entity/instance")

new = {
    "user_id": 1,
    "trading_platform_id": 1,
    "name": "example",
    "ip": None,
    "username": None,
    "password": None,
    "api_key": None,
    "is_active": True,
    "description": None,
}

# add: POST /add
added = client.post("/add", json={"entity": new}).json()
print(added)

# get_by_id: GET /get_by_id/{id}
print(client.get(f"/get_by_id/{added['id']}").json())

# update: PUT /update
added["description"] = "Changed by the example"
print(client.put("/update", json={"entity": added}).json())

# list: POST /list
only = [{"field": "id", "operator": "EQUALS", "value": added["id"]}]
print(
    client.post(
        "/list",
        json={
            "filters": only,
            "orders": [{"field": "id", "direction": "DESCENDING"}],
            "limit": 5,
        },
    ).json()
)

# count: POST /count
print(client.post("/count", json={"filters": only}).json())

# sum, min and max: POST /sum, /min, /max
print(client.post("/sum", json={"field": "id", "filters": only}).json())
print(client.post("/min", json={"field": "id", "filters": only}).json())
print(client.post("/max", json={"field": "id", "filters": only}).json())

# disable and enable: PATCH /disable/{id}, /enable/{id}
print(client.patch(f"/disable/{added['id']}").json()["is_active"])
print(
    client.patch(f"/enable/{added['id']}", json={"instance": "SQLITE"}).json()[
        "is_active"
    ]
)

# delete: DELETE /delete/{id}
print(client.delete(f"/delete/{added['id']}").json()["id"])

# truncate: DELETE /truncate removes every record of this Entity, or is refused while other records refer to them.
print(client.delete("/truncate").status_code)
```

### Currency

Segment `currency`; every Endpoint below is served at the Base URL followed by `/entity/currency`.

| Action | Method | Path | Parameters |
| --- | --- | --- | --- |
| `add` | `POST` | `/entity/currency/add` | `entity` (body, required), `instance` (body, optional) |
| `update` | `PUT` | `/entity/currency/update` | `entity` (body, required), `instance` (body, optional) |
| `list` | `POST` | `/entity/currency/list` | `filters` (body, optional), `combination` (body, optional), `orders` (body, optional), `limit` (body, optional), `instance` (body, optional) |
| `get_by_id` | `GET` | `/entity/currency/get_by_id/{id}` | `id` (path, required), `instance` (query, optional) |
| `delete` | `DELETE` | `/entity/currency/delete/{id}` | `id` (path, required), `instance` (query, optional) |
| `enable` | `PATCH` | `/entity/currency/enable/{id}` | `id` (path, required), `instance` (body, optional) |
| `disable` | `PATCH` | `/entity/currency/disable/{id}` | `id` (path, required), `instance` (body, optional) |
| `count` | `POST` | `/entity/currency/count` | `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `sum` | `POST` | `/entity/currency/sum` | `field` (body, required), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `min` | `POST` | `/entity/currency/min` | `field` (body, required), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `max` | `POST` | `/entity/currency/max` | `field` (body, required), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `truncate` | `DELETE` | `/entity/currency/truncate` | `instance` (query, optional) |

One example runs every Endpoint of the Currency Adapter in turn. It adds a record, reads it, changes it, queries it, disables and enables it and deletes it again, leaving the data as it was. The final truncate step then empties the whole Currency table (or is refused while other records refer to it), so run that step only on a table you mean to empty.

```python
import httpx
import yaml

api = yaml.safe_load(open("config.yaml"))["url"]
client = httpx.Client(base_url=f"{api}/entity/currency")

new = {
    "user_id": 1,
    "code": "XXX",
    "symbol": "X",
    "country": None,
    "decimal_digits": 2,
    "is_active": True,
    "description": None,
}

# add: POST /add
added = client.post("/add", json={"entity": new}).json()
print(added)

# get_by_id: GET /get_by_id/{id}
print(client.get(f"/get_by_id/{added['id']}").json())

# update: PUT /update
added["description"] = "Changed by the example"
print(client.put("/update", json={"entity": added}).json())

# list: POST /list
only = [{"field": "id", "operator": "EQUALS", "value": added["id"]}]
print(
    client.post(
        "/list",
        json={
            "filters": only,
            "orders": [{"field": "id", "direction": "DESCENDING"}],
            "limit": 5,
        },
    ).json()
)

# count: POST /count
print(client.post("/count", json={"filters": only}).json())

# sum, min and max: POST /sum, /min, /max
print(client.post("/sum", json={"field": "id", "filters": only}).json())
print(client.post("/min", json={"field": "id", "filters": only}).json())
print(client.post("/max", json={"field": "id", "filters": only}).json())

# disable and enable: PATCH /disable/{id}, /enable/{id}
print(client.patch(f"/disable/{added['id']}").json()["is_active"])
print(
    client.patch(f"/enable/{added['id']}", json={"instance": "SQLITE"}).json()[
        "is_active"
    ]
)

# delete: DELETE /delete/{id}
print(client.delete(f"/delete/{added['id']}").json()["id"])

# truncate: DELETE /truncate removes every record of this Entity, or is refused while other records refer to them.
print(client.delete("/truncate").status_code)
```

### Broker

Segment `broker`; every Endpoint below is served at the Base URL followed by `/entity/broker`.

| Action | Method | Path | Parameters |
| --- | --- | --- | --- |
| `add` | `POST` | `/entity/broker/add` | `entity` (body, required), `instance` (body, optional) |
| `update` | `PUT` | `/entity/broker/update` | `entity` (body, required), `instance` (body, optional) |
| `list` | `POST` | `/entity/broker/list` | `filters` (body, optional), `combination` (body, optional), `orders` (body, optional), `limit` (body, optional), `instance` (body, optional) |
| `get_by_id` | `GET` | `/entity/broker/get_by_id/{id}` | `id` (path, required), `instance` (query, optional) |
| `delete` | `DELETE` | `/entity/broker/delete/{id}` | `id` (path, required), `instance` (query, optional) |
| `enable` | `PATCH` | `/entity/broker/enable/{id}` | `id` (path, required), `instance` (body, optional) |
| `disable` | `PATCH` | `/entity/broker/disable/{id}` | `id` (path, required), `instance` (body, optional) |
| `count` | `POST` | `/entity/broker/count` | `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `sum` | `POST` | `/entity/broker/sum` | `field` (body, required), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `min` | `POST` | `/entity/broker/min` | `field` (body, required), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `max` | `POST` | `/entity/broker/max` | `field` (body, required), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `truncate` | `DELETE` | `/entity/broker/truncate` | `instance` (query, optional) |

One example runs every Endpoint of the Broker Adapter in turn. It adds a record, reads it, changes it, queries it, disables and enables it and deletes it again, leaving the data as it was. The final truncate step then empties the whole Broker table (or is refused while other records refer to it), so run that step only on a table you mean to empty.

```python
import httpx
import yaml

api = yaml.safe_load(open("config.yaml"))["url"]
client = httpx.Client(base_url=f"{api}/entity/broker")

new = {"name": "Example Broker", "user_id": 1, "is_active": True, "description": None}

# add: POST /add
added = client.post("/add", json={"entity": new}).json()
print(added)

# get_by_id: GET /get_by_id/{id}
print(client.get(f"/get_by_id/{added['id']}").json())

# update: PUT /update
added["description"] = "Changed by the example"
print(client.put("/update", json={"entity": added}).json())

# list: POST /list
only = [{"field": "id", "operator": "EQUALS", "value": added["id"]}]
print(
    client.post(
        "/list",
        json={
            "filters": only,
            "orders": [{"field": "id", "direction": "DESCENDING"}],
            "limit": 5,
        },
    ).json()
)

# count: POST /count
print(client.post("/count", json={"filters": only}).json())

# sum, min and max: POST /sum, /min, /max
print(client.post("/sum", json={"field": "id", "filters": only}).json())
print(client.post("/min", json={"field": "id", "filters": only}).json())
print(client.post("/max", json={"field": "id", "filters": only}).json())

# disable and enable: PATCH /disable/{id}, /enable/{id}
print(client.patch(f"/disable/{added['id']}").json()["is_active"])
print(
    client.patch(f"/enable/{added['id']}", json={"instance": "SQLITE"}).json()[
        "is_active"
    ]
)

# delete: DELETE /delete/{id}
print(client.delete(f"/delete/{added['id']}").json()["id"])

# truncate: DELETE /truncate removes every record of this Entity, or is refused while other records refer to them.
print(client.delete("/truncate").status_code)
```
### Asset

Segment `asset`; every Endpoint below is served at the Base URL followed by `/entity/asset`.

| Action | Method | Path | Parameters |
| --- | --- | --- | --- |
| `add` | `POST` | `/entity/asset/add` | `entity` (body, required), `instance` (body, optional) |
| `update` | `PUT` | `/entity/asset/update` | `entity` (body, required), `instance` (body, optional) |
| `list` | `POST` | `/entity/asset/list` | `filters` (body, optional), `combination` (body, optional), `orders` (body, optional), `limit` (body, optional), `instance` (body, optional) |
| `get_by_id` | `GET` | `/entity/asset/get_by_id/{id}` | `id` (path, required), `instance` (query, optional) |
| `delete` | `DELETE` | `/entity/asset/delete/{id}` | `id` (path, required), `instance` (query, optional) |
| `enable` | `PATCH` | `/entity/asset/enable/{id}` | `id` (path, required), `instance` (body, optional) |
| `disable` | `PATCH` | `/entity/asset/disable/{id}` | `id` (path, required), `instance` (body, optional) |
| `count` | `POST` | `/entity/asset/count` | `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `sum` | `POST` | `/entity/asset/sum` | `field` (body, required), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `min` | `POST` | `/entity/asset/min` | `field` (body, required), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `max` | `POST` | `/entity/asset/max` | `field` (body, required), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `truncate` | `DELETE` | `/entity/asset/truncate` | `instance` (query, optional) |

One example runs every Endpoint of the Asset Adapter in turn. It adds a record, reads it, changes it, queries it, disables and enables it and deletes it again, leaving the data as it was. The final truncate step then empties the whole Asset table (or is refused while other records refer to it), so run that step only on a table you mean to empty.

```python
import httpx
import yaml

api = yaml.safe_load(open("config.yaml"))["url"]
client = httpx.Client(base_url=f"{api}/entity/asset")

new = {
    "broker_id": 1,
    "symbol": "EXAMPLE",
    "category": "Currency",
    "point_size": 0.0001,
    "digits": 5,
    "is_active": True,
    "description": None,
}

# add: POST /add
added = client.post("/add", json={"entity": new}).json()
print(added)

# get_by_id: GET /get_by_id/{id}
print(client.get(f"/get_by_id/{added['id']}").json())

# update: PUT /update
added["description"] = "Changed by the example"
print(client.put("/update", json={"entity": added}).json())

# list: POST /list
only = [{"field": "id", "operator": "EQUALS", "value": added["id"]}]
print(
    client.post(
        "/list",
        json={
            "filters": only,
            "orders": [{"field": "id", "direction": "DESCENDING"}],
            "limit": 5,
        },
    ).json()
)

# count: POST /count
print(client.post("/count", json={"filters": only}).json())

# sum, min and max: POST /sum, /min, /max
print(client.post("/sum", json={"field": "id", "filters": only}).json())
print(client.post("/min", json={"field": "id", "filters": only}).json())
print(client.post("/max", json={"field": "id", "filters": only}).json())

# disable and enable: PATCH /disable/{id}, /enable/{id}
print(client.patch(f"/disable/{added['id']}").json()["is_active"])
print(
    client.patch(f"/enable/{added['id']}", json={"instance": "SQLITE"}).json()[
        "is_active"
    ]
)

# delete: DELETE /delete/{id}
print(client.delete(f"/delete/{added['id']}").json()["id"])

# truncate: DELETE /truncate removes every record of this Entity, or is refused while other records refer to them.
print(client.delete("/truncate").status_code)
```

### Account Group

Segment `account_group`; every Endpoint below is served at the Base URL followed by `/entity/account_group`.

| Action | Method | Path | Parameters |
| --- | --- | --- | --- |
| `add` | `POST` | `/entity/account_group/add` | `entity` (body, required), `instance` (body, optional) |
| `update` | `PUT` | `/entity/account_group/update` | `entity` (body, required), `instance` (body, optional) |
| `list` | `POST` | `/entity/account_group/list` | `filters` (body, optional), `combination` (body, optional), `orders` (body, optional), `limit` (body, optional), `instance` (body, optional) |
| `get_by_id` | `GET` | `/entity/account_group/get_by_id/{id}` | `id` (path, required), `instance` (query, optional) |
| `delete` | `DELETE` | `/entity/account_group/delete/{id}` | `id` (path, required), `instance` (query, optional) |
| `enable` | `PATCH` | `/entity/account_group/enable/{id}` | `id` (path, required), `instance` (body, optional) |
| `disable` | `PATCH` | `/entity/account_group/disable/{id}` | `id` (path, required), `instance` (body, optional) |
| `count` | `POST` | `/entity/account_group/count` | `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `sum` | `POST` | `/entity/account_group/sum` | `field` (body, required), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `min` | `POST` | `/entity/account_group/min` | `field` (body, required), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `max` | `POST` | `/entity/account_group/max` | `field` (body, required), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `truncate` | `DELETE` | `/entity/account_group/truncate` | `instance` (query, optional) |

One example runs every Endpoint of the Account Group Adapter in turn. It adds a record, reads it, changes it, queries it, disables and enables it and deletes it again, leaving the data as it was. The final truncate step then empties the whole Account Group table (or is refused while other records refer to it), so run that step only on a table you mean to empty.

```python
import httpx
import yaml

api = yaml.safe_load(open("config.yaml"))["url"]
client = httpx.Client(base_url=f"{api}/entity/account_group")

new = {"user_id": 1, "name": "Example", "is_active": True, "description": None}

# add: POST /add
added = client.post("/add", json={"entity": new}).json()
print(added)

# get_by_id: GET /get_by_id/{id}
print(client.get(f"/get_by_id/{added['id']}").json())

# update: PUT /update
added["description"] = "Changed by the example"
print(client.put("/update", json={"entity": added}).json())

# list: POST /list
only = [{"field": "id", "operator": "EQUALS", "value": added["id"]}]
print(
    client.post(
        "/list",
        json={
            "filters": only,
            "orders": [{"field": "id", "direction": "DESCENDING"}],
            "limit": 5,
        },
    ).json()
)

# count: POST /count
print(client.post("/count", json={"filters": only}).json())

# sum, min and max: POST /sum, /min, /max
print(client.post("/sum", json={"field": "id", "filters": only}).json())
print(client.post("/min", json={"field": "id", "filters": only}).json())
print(client.post("/max", json={"field": "id", "filters": only}).json())

# disable and enable: PATCH /disable/{id}, /enable/{id}
print(client.patch(f"/disable/{added['id']}").json()["is_active"])
print(
    client.patch(f"/enable/{added['id']}", json={"instance": "SQLITE"}).json()[
        "is_active"
    ]
)

# delete: DELETE /delete/{id}
print(client.delete(f"/delete/{added['id']}").json()["id"])

# truncate: DELETE /truncate removes every record of this Entity, or is refused while other records refer to them.
print(client.delete("/truncate").status_code)
```

### Account

Segment `account`; every Endpoint below is served at the Base URL followed by `/entity/account`.

| Action | Method | Path | Parameters |
| --- | --- | --- | --- |
| `add` | `POST` | `/entity/account/add` | `entity` (body, required), `instance` (body, optional) |
| `update` | `PUT` | `/entity/account/update` | `entity` (body, required), `instance` (body, optional) |
| `list` | `POST` | `/entity/account/list` | `filters` (body, optional), `combination` (body, optional), `orders` (body, optional), `limit` (body, optional), `instance` (body, optional) |
| `get_by_id` | `GET` | `/entity/account/get_by_id/{id}` | `id` (path, required), `instance` (query, optional) |
| `delete` | `DELETE` | `/entity/account/delete/{id}` | `id` (path, required), `instance` (query, optional) |
| `enable` | `PATCH` | `/entity/account/enable/{id}` | `id` (path, required), `instance` (body, optional) |
| `disable` | `PATCH` | `/entity/account/disable/{id}` | `id` (path, required), `instance` (body, optional) |
| `count` | `POST` | `/entity/account/count` | `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `sum` | `POST` | `/entity/account/sum` | `field` (body, required), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `min` | `POST` | `/entity/account/min` | `field` (body, required), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `max` | `POST` | `/entity/account/max` | `field` (body, required), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `truncate` | `DELETE` | `/entity/account/truncate` | `instance` (query, optional) |

One example runs every Endpoint of the Account Adapter in turn. It adds a record, reads it, changes it, queries it, disables and enables it and deletes it again, leaving the data as it was. The final truncate step then empties the whole Account table (or is refused while other records refer to it), so run that step only on a table you mean to empty.

```python
import httpx
import yaml

api = yaml.safe_load(open("config.yaml"))["url"]
client = httpx.Client(base_url=f"{api}/entity/account")

# Account needs an Account Group of its own: its Group, Broker and Instance must be a new combination.
group = httpx.Client(base_url=f"{api}/entity/account_group")
own_group = group.post(
    "/add",
    json={
        "entity": {
            "user_id": 1,
            "name": "For the Account example",
            "is_active": True,
            "description": None,
        }
    },
).json()

new = {
    "name": "example",
    "group_id": own_group["id"],
    "broker_id": 1,
    "instance_id": 1,
    "base_currency_id": 1,
    "username": "example",
    "password": "placeholder",
    "leverage": 100,
    "balance": "0",
    "account_type": "cfd",
    "is_active": True,
    "description": None,
}

# add: POST /add
added = client.post("/add", json={"entity": new}).json()
print(added)

# get_by_id: GET /get_by_id/{id}
print(client.get(f"/get_by_id/{added['id']}").json())

# update: PUT /update
added["description"] = "Changed by the example"
print(client.put("/update", json={"entity": added}).json())

# list: POST /list
only = [{"field": "id", "operator": "EQUALS", "value": added["id"]}]
print(
    client.post(
        "/list",
        json={
            "filters": only,
            "orders": [{"field": "id", "direction": "DESCENDING"}],
            "limit": 5,
        },
    ).json()
)

# count: POST /count
print(client.post("/count", json={"filters": only}).json())

# sum, min and max: POST /sum, /min, /max
print(client.post("/sum", json={"field": "id", "filters": only}).json())
print(client.post("/min", json={"field": "id", "filters": only}).json())
print(client.post("/max", json={"field": "id", "filters": only}).json())

# disable and enable: PATCH /disable/{id}, /enable/{id}
print(client.patch(f"/disable/{added['id']}").json()["is_active"])
print(
    client.patch(f"/enable/{added['id']}", json={"instance": "SQLITE"}).json()[
        "is_active"
    ]
)

# delete: DELETE /delete/{id}
print(client.delete(f"/delete/{added['id']}").json()["id"])

# Remove the Account Group the example created.
group.delete(f"/delete/{own_group['id']}")

# truncate: DELETE /truncate removes every record of this Entity, or is refused while other records refer to them.
print(client.delete("/truncate").status_code)
```

### Trailing Group

Segment `trailing_group`; every Endpoint below is served at the Base URL followed by `/entity/trailing_group`.

| Action | Method | Path | Parameters |
| --- | --- | --- | --- |
| `add` | `POST` | `/entity/trailing_group/add` | `entity` (body, required), `instance` (body, optional) |
| `update` | `PUT` | `/entity/trailing_group/update` | `entity` (body, required), `instance` (body, optional) |
| `list` | `POST` | `/entity/trailing_group/list` | `filters` (body, optional), `combination` (body, optional), `orders` (body, optional), `limit` (body, optional), `instance` (body, optional) |
| `get_by_id` | `GET` | `/entity/trailing_group/get_by_id/{id}` | `id` (path, required), `instance` (query, optional) |
| `delete` | `DELETE` | `/entity/trailing_group/delete/{id}` | `id` (path, required), `instance` (query, optional) |
| `enable` | `PATCH` | `/entity/trailing_group/enable/{id}` | `id` (path, required), `instance` (body, optional) |
| `disable` | `PATCH` | `/entity/trailing_group/disable/{id}` | `id` (path, required), `instance` (body, optional) |
| `count` | `POST` | `/entity/trailing_group/count` | `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `sum` | `POST` | `/entity/trailing_group/sum` | `field` (body, required), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `min` | `POST` | `/entity/trailing_group/min` | `field` (body, required), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `max` | `POST` | `/entity/trailing_group/max` | `field` (body, required), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `truncate` | `DELETE` | `/entity/trailing_group/truncate` | `instance` (query, optional) |

One example runs every Endpoint of the Trailing Group Adapter in turn. It adds a record, reads it, changes it, queries it, disables and enables it and deletes it again, leaving the data as it was. The final truncate step then empties the whole Trailing Group table (or is refused while other records refer to it), so run that step only on a table you mean to empty.

```python
import httpx
import yaml

api = yaml.safe_load(open("config.yaml"))["url"]
client = httpx.Client(base_url=f"{api}/entity/trailing_group")

new = {"user_id": 1, "name": "Example", "is_active": True, "description": None}

# add: POST /add
added = client.post("/add", json={"entity": new}).json()
print(added)

# get_by_id: GET /get_by_id/{id}
print(client.get(f"/get_by_id/{added['id']}").json())

# update: PUT /update
added["description"] = "Changed by the example"
print(client.put("/update", json={"entity": added}).json())

# list: POST /list
only = [{"field": "id", "operator": "EQUALS", "value": added["id"]}]
print(
    client.post(
        "/list",
        json={
            "filters": only,
            "orders": [{"field": "id", "direction": "DESCENDING"}],
            "limit": 5,
        },
    ).json()
)

# count: POST /count
print(client.post("/count", json={"filters": only}).json())

# sum, min and max: POST /sum, /min, /max
print(client.post("/sum", json={"field": "id", "filters": only}).json())
print(client.post("/min", json={"field": "id", "filters": only}).json())
print(client.post("/max", json={"field": "id", "filters": only}).json())

# disable and enable: PATCH /disable/{id}, /enable/{id}
print(client.patch(f"/disable/{added['id']}").json()["is_active"])
print(
    client.patch(f"/enable/{added['id']}", json={"instance": "SQLITE"}).json()[
        "is_active"
    ]
)

# delete: DELETE /delete/{id}
print(client.delete(f"/delete/{added['id']}").json()["id"])

# truncate: DELETE /truncate removes every record of this Entity, or is refused while other records refer to them.
print(client.delete("/truncate").status_code)
```

### Trailing Rule

Segment `trailing_rule`; every Endpoint below is served at the Base URL followed by `/entity/trailing_rule`.

| Action | Method | Path | Parameters |
| --- | --- | --- | --- |
| `add` | `POST` | `/entity/trailing_rule/add` | `entity` (body, required), `instance` (body, optional) |
| `update` | `PUT` | `/entity/trailing_rule/update` | `entity` (body, required), `instance` (body, optional) |
| `list` | `POST` | `/entity/trailing_rule/list` | `filters` (body, optional), `combination` (body, optional), `orders` (body, optional), `limit` (body, optional), `instance` (body, optional) |
| `get_by_id` | `GET` | `/entity/trailing_rule/get_by_id/{id}` | `id` (path, required), `instance` (query, optional) |
| `delete` | `DELETE` | `/entity/trailing_rule/delete/{id}` | `id` (path, required), `instance` (query, optional) |
| `enable` | `PATCH` | `/entity/trailing_rule/enable/{id}` | `id` (path, required), `instance` (body, optional) |
| `disable` | `PATCH` | `/entity/trailing_rule/disable/{id}` | `id` (path, required), `instance` (body, optional) |
| `count` | `POST` | `/entity/trailing_rule/count` | `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `sum` | `POST` | `/entity/trailing_rule/sum` | `field` (body, required), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `min` | `POST` | `/entity/trailing_rule/min` | `field` (body, required), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `max` | `POST` | `/entity/trailing_rule/max` | `field` (body, required), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `truncate` | `DELETE` | `/entity/trailing_rule/truncate` | `instance` (query, optional) |

One example runs every Endpoint of the Trailing Rule Adapter in turn. It adds a record, reads it, changes it, queries it, disables and enables it and deletes it again, leaving the data as it was. The final truncate step then empties the whole Trailing Rule table (or is refused while other records refer to it), so run that step only on a table you mean to empty.

```python
import httpx
import yaml

api = yaml.safe_load(open("config.yaml"))["url"]
client = httpx.Client(base_url=f"{api}/entity/trailing_rule")

new = {
    "name": "example",
    "trailing_group_id": 1,
    "trigger_percentage": "50",
    "take_profit_adjustment": None,
    "stop_loss_adjustment": None,
    "is_active": True,
    "description": None,
}

# add: POST /add
added = client.post("/add", json={"entity": new}).json()
print(added)

# get_by_id: GET /get_by_id/{id}
print(client.get(f"/get_by_id/{added['id']}").json())

# update: PUT /update
added["description"] = "Changed by the example"
print(client.put("/update", json={"entity": added}).json())

# list: POST /list
only = [{"field": "id", "operator": "EQUALS", "value": added["id"]}]
print(
    client.post(
        "/list",
        json={
            "filters": only,
            "orders": [{"field": "id", "direction": "DESCENDING"}],
            "limit": 5,
        },
    ).json()
)

# count: POST /count
print(client.post("/count", json={"filters": only}).json())

# sum, min and max: POST /sum, /min, /max
print(client.post("/sum", json={"field": "id", "filters": only}).json())
print(client.post("/min", json={"field": "id", "filters": only}).json())
print(client.post("/max", json={"field": "id", "filters": only}).json())

# disable and enable: PATCH /disable/{id}, /enable/{id}
print(client.patch(f"/disable/{added['id']}").json()["is_active"])
print(
    client.patch(f"/enable/{added['id']}", json={"instance": "SQLITE"}).json()[
        "is_active"
    ]
)

# delete: DELETE /delete/{id}
print(client.delete(f"/delete/{added['id']}").json()["id"])

# truncate: DELETE /truncate removes every record of this Entity, or is refused while other records refer to them.
print(client.delete("/truncate").status_code)
```
### Partial Group

Segment `partial_group`; every Endpoint below is served at the Base URL followed by `/entity/partial_group`.

| Action | Method | Path | Parameters |
| --- | --- | --- | --- |
| `add` | `POST` | `/entity/partial_group/add` | `entity` (body, required), `instance` (body, optional) |
| `update` | `PUT` | `/entity/partial_group/update` | `entity` (body, required), `instance` (body, optional) |
| `list` | `POST` | `/entity/partial_group/list` | `filters` (body, optional), `combination` (body, optional), `orders` (body, optional), `limit` (body, optional), `instance` (body, optional) |
| `get_by_id` | `GET` | `/entity/partial_group/get_by_id/{id}` | `id` (path, required), `instance` (query, optional) |
| `delete` | `DELETE` | `/entity/partial_group/delete/{id}` | `id` (path, required), `instance` (query, optional) |
| `enable` | `PATCH` | `/entity/partial_group/enable/{id}` | `id` (path, required), `instance` (body, optional) |
| `disable` | `PATCH` | `/entity/partial_group/disable/{id}` | `id` (path, required), `instance` (body, optional) |
| `count` | `POST` | `/entity/partial_group/count` | `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `sum` | `POST` | `/entity/partial_group/sum` | `field` (body, required), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `min` | `POST` | `/entity/partial_group/min` | `field` (body, required), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `max` | `POST` | `/entity/partial_group/max` | `field` (body, required), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `truncate` | `DELETE` | `/entity/partial_group/truncate` | `instance` (query, optional) |

One example runs every Endpoint of the Partial Group Adapter in turn. It adds a record, reads it, changes it, queries it, disables and enables it and deletes it again, leaving the data as it was. The final truncate step then empties the whole Partial Group table (or is refused while other records refer to it), so run that step only on a table you mean to empty.

```python
import httpx
import yaml

api = yaml.safe_load(open("config.yaml"))["url"]
client = httpx.Client(base_url=f"{api}/entity/partial_group")

new = {"user_id": 1, "name": "Example", "is_active": True, "description": None}

# add: POST /add
added = client.post("/add", json={"entity": new}).json()
print(added)

# get_by_id: GET /get_by_id/{id}
print(client.get(f"/get_by_id/{added['id']}").json())

# update: PUT /update
added["description"] = "Changed by the example"
print(client.put("/update", json={"entity": added}).json())

# list: POST /list
only = [{"field": "id", "operator": "EQUALS", "value": added["id"]}]
print(
    client.post(
        "/list",
        json={
            "filters": only,
            "orders": [{"field": "id", "direction": "DESCENDING"}],
            "limit": 5,
        },
    ).json()
)

# count: POST /count
print(client.post("/count", json={"filters": only}).json())

# sum, min and max: POST /sum, /min, /max
print(client.post("/sum", json={"field": "id", "filters": only}).json())
print(client.post("/min", json={"field": "id", "filters": only}).json())
print(client.post("/max", json={"field": "id", "filters": only}).json())

# disable and enable: PATCH /disable/{id}, /enable/{id}
print(client.patch(f"/disable/{added['id']}").json()["is_active"])
print(
    client.patch(f"/enable/{added['id']}", json={"instance": "SQLITE"}).json()[
        "is_active"
    ]
)

# delete: DELETE /delete/{id}
print(client.delete(f"/delete/{added['id']}").json()["id"])

# truncate: DELETE /truncate removes every record of this Entity, or is refused while other records refer to them.
print(client.delete("/truncate").status_code)
```

### Partial Rule

Segment `partial_rule`; every Endpoint below is served at the Base URL followed by `/entity/partial_rule`.

| Action | Method | Path | Parameters |
| --- | --- | --- | --- |
| `add` | `POST` | `/entity/partial_rule/add` | `entity` (body, required), `instance` (body, optional) |
| `update` | `PUT` | `/entity/partial_rule/update` | `entity` (body, required), `instance` (body, optional) |
| `list` | `POST` | `/entity/partial_rule/list` | `filters` (body, optional), `combination` (body, optional), `orders` (body, optional), `limit` (body, optional), `instance` (body, optional) |
| `get_by_id` | `GET` | `/entity/partial_rule/get_by_id/{id}` | `id` (path, required), `instance` (query, optional) |
| `delete` | `DELETE` | `/entity/partial_rule/delete/{id}` | `id` (path, required), `instance` (query, optional) |
| `enable` | `PATCH` | `/entity/partial_rule/enable/{id}` | `id` (path, required), `instance` (body, optional) |
| `disable` | `PATCH` | `/entity/partial_rule/disable/{id}` | `id` (path, required), `instance` (body, optional) |
| `count` | `POST` | `/entity/partial_rule/count` | `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `sum` | `POST` | `/entity/partial_rule/sum` | `field` (body, required), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `min` | `POST` | `/entity/partial_rule/min` | `field` (body, required), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `max` | `POST` | `/entity/partial_rule/max` | `field` (body, required), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `truncate` | `DELETE` | `/entity/partial_rule/truncate` | `instance` (query, optional) |

One example runs every Endpoint of the Partial Rule Adapter in turn. It adds a record, reads it, changes it, queries it, disables and enables it and deletes it again, leaving the data as it was. The final truncate step then empties the whole Partial Rule table (or is refused while other records refer to it), so run that step only on a table you mean to empty.

```python
import httpx
import yaml

api = yaml.safe_load(open("config.yaml"))["url"]
client = httpx.Client(base_url=f"{api}/entity/partial_rule")

new = {
    "name": "example",
    "partial_group_id": 1,
    "profit_percentage": "50",
    "close_percentage": "25",
    "is_active": True,
    "description": None,
}

# add: POST /add
added = client.post("/add", json={"entity": new}).json()
print(added)

# get_by_id: GET /get_by_id/{id}
print(client.get(f"/get_by_id/{added['id']}").json())

# update: PUT /update
added["description"] = "Changed by the example"
print(client.put("/update", json={"entity": added}).json())

# list: POST /list
only = [{"field": "id", "operator": "EQUALS", "value": added["id"]}]
print(
    client.post(
        "/list",
        json={
            "filters": only,
            "orders": [{"field": "id", "direction": "DESCENDING"}],
            "limit": 5,
        },
    ).json()
)

# count: POST /count
print(client.post("/count", json={"filters": only}).json())

# sum, min and max: POST /sum, /min, /max
print(client.post("/sum", json={"field": "id", "filters": only}).json())
print(client.post("/min", json={"field": "id", "filters": only}).json())
print(client.post("/max", json={"field": "id", "filters": only}).json())

# disable and enable: PATCH /disable/{id}, /enable/{id}
print(client.patch(f"/disable/{added['id']}").json()["is_active"])
print(
    client.patch(f"/enable/{added['id']}", json={"instance": "SQLITE"}).json()[
        "is_active"
    ]
)

# delete: DELETE /delete/{id}
print(client.delete(f"/delete/{added['id']}").json()["id"])

# truncate: DELETE /truncate removes every record of this Entity, or is refused while other records refer to them.
print(client.delete("/truncate").status_code)
```

### Action Group

Segment `action_group`; every Endpoint below is served at the Base URL followed by `/entity/action_group`.

| Action | Method | Path | Parameters |
| --- | --- | --- | --- |
| `add` | `POST` | `/entity/action_group/add` | `entity` (body, required), `instance` (body, optional) |
| `update` | `PUT` | `/entity/action_group/update` | `entity` (body, required), `instance` (body, optional) |
| `list` | `POST` | `/entity/action_group/list` | `filters` (body, optional), `combination` (body, optional), `orders` (body, optional), `limit` (body, optional), `instance` (body, optional) |
| `get_by_id` | `GET` | `/entity/action_group/get_by_id/{id}` | `id` (path, required), `instance` (query, optional) |
| `delete` | `DELETE` | `/entity/action_group/delete/{id}` | `id` (path, required), `instance` (query, optional) |
| `enable` | `PATCH` | `/entity/action_group/enable/{id}` | `id` (path, required), `instance` (body, optional) |
| `disable` | `PATCH` | `/entity/action_group/disable/{id}` | `id` (path, required), `instance` (body, optional) |
| `count` | `POST` | `/entity/action_group/count` | `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `sum` | `POST` | `/entity/action_group/sum` | `field` (body, required), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `min` | `POST` | `/entity/action_group/min` | `field` (body, required), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `max` | `POST` | `/entity/action_group/max` | `field` (body, required), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `truncate` | `DELETE` | `/entity/action_group/truncate` | `instance` (query, optional) |

One example runs every Endpoint of the Action Group Adapter in turn. It adds a record, reads it, changes it, queries it, disables and enables it and deletes it again, leaving the data as it was. The final truncate step then empties the whole Action Group table (or is refused while other records refer to it), so run that step only on a table you mean to empty.

```python
import httpx
import yaml

api = yaml.safe_load(open("config.yaml"))["url"]
client = httpx.Client(base_url=f"{api}/entity/action_group")

new = {"user_id": 1, "name": "Example", "is_active": True, "description": None}

# add: POST /add
added = client.post("/add", json={"entity": new}).json()
print(added)

# get_by_id: GET /get_by_id/{id}
print(client.get(f"/get_by_id/{added['id']}").json())

# update: PUT /update
added["description"] = "Changed by the example"
print(client.put("/update", json={"entity": added}).json())

# list: POST /list
only = [{"field": "id", "operator": "EQUALS", "value": added["id"]}]
print(
    client.post(
        "/list",
        json={
            "filters": only,
            "orders": [{"field": "id", "direction": "DESCENDING"}],
            "limit": 5,
        },
    ).json()
)

# count: POST /count
print(client.post("/count", json={"filters": only}).json())

# sum, min and max: POST /sum, /min, /max
print(client.post("/sum", json={"field": "id", "filters": only}).json())
print(client.post("/min", json={"field": "id", "filters": only}).json())
print(client.post("/max", json={"field": "id", "filters": only}).json())

# disable and enable: PATCH /disable/{id}, /enable/{id}
print(client.patch(f"/disable/{added['id']}").json()["is_active"])
print(
    client.patch(f"/enable/{added['id']}", json={"instance": "SQLITE"}).json()[
        "is_active"
    ]
)

# delete: DELETE /delete/{id}
print(client.delete(f"/delete/{added['id']}").json()["id"])

# truncate: DELETE /truncate removes every record of this Entity, or is refused while other records refer to them.
print(client.delete("/truncate").status_code)
```

### Action

Segment `action`; every Endpoint below is served at the Base URL followed by `/entity/action`.

| Action | Method | Path | Parameters |
| --- | --- | --- | --- |
| `add` | `POST` | `/entity/action/add` | `entity` (body, required), `instance` (body, optional) |
| `update` | `PUT` | `/entity/action/update` | `entity` (body, required), `instance` (body, optional) |
| `list` | `POST` | `/entity/action/list` | `filters` (body, optional), `combination` (body, optional), `orders` (body, optional), `limit` (body, optional), `instance` (body, optional) |
| `get_by_id` | `GET` | `/entity/action/get_by_id/{id}` | `id` (path, required), `instance` (query, optional) |
| `delete` | `DELETE` | `/entity/action/delete/{id}` | `id` (path, required), `instance` (query, optional) |
| `enable` | `PATCH` | `/entity/action/enable/{id}` | `id` (path, required), `instance` (body, optional) |
| `disable` | `PATCH` | `/entity/action/disable/{id}` | `id` (path, required), `instance` (body, optional) |
| `count` | `POST` | `/entity/action/count` | `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `sum` | `POST` | `/entity/action/sum` | `field` (body, required), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `min` | `POST` | `/entity/action/min` | `field` (body, required), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `max` | `POST` | `/entity/action/max` | `field` (body, required), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `truncate` | `DELETE` | `/entity/action/truncate` | `instance` (query, optional) |

One example runs every Endpoint of the Action Adapter in turn. It adds a record, reads it, changes it, queries it, disables and enables it and deletes it again, leaving the data as it was. The final truncate step then empties the whole Action table (or is refused while other records refer to it), so run that step only on a table you mean to empty.

```python
import httpx
import yaml

api = yaml.safe_load(open("config.yaml"))["url"]
client = httpx.Client(base_url=f"{api}/entity/action")

new = {
    "name": "example",
    "action_group_id": 1,
    "asset_id": 1,
    "account_id": 1,
    "partial_group_id": 1,
    "trailing_group_id": 1,
    "risk_by_reward": "1",
    "take_profit": "1",
    "stop_loss": "1",
    "is_active": True,
    "description": None,
}

# add: POST /add
added = client.post("/add", json={"entity": new}).json()
print(added)

# get_by_id: GET /get_by_id/{id}
print(client.get(f"/get_by_id/{added['id']}").json())

# update: PUT /update
added["description"] = "Changed by the example"
print(client.put("/update", json={"entity": added}).json())

# list: POST /list
only = [{"field": "id", "operator": "EQUALS", "value": added["id"]}]
print(
    client.post(
        "/list",
        json={
            "filters": only,
            "orders": [{"field": "id", "direction": "DESCENDING"}],
            "limit": 5,
        },
    ).json()
)

# count: POST /count
print(client.post("/count", json={"filters": only}).json())

# sum, min and max: POST /sum, /min, /max
print(client.post("/sum", json={"field": "id", "filters": only}).json())
print(client.post("/min", json={"field": "id", "filters": only}).json())
print(client.post("/max", json={"field": "id", "filters": only}).json())

# disable and enable: PATCH /disable/{id}, /enable/{id}
print(client.patch(f"/disable/{added['id']}").json()["is_active"])
print(
    client.patch(f"/enable/{added['id']}", json={"instance": "SQLITE"}).json()[
        "is_active"
    ]
)

# delete: DELETE /delete/{id}
print(client.delete(f"/delete/{added['id']}").json()["id"])

# truncate: DELETE /truncate removes every record of this Entity, or is refused while other records refer to them.
print(client.delete("/truncate").status_code)
```

### Position

Segment `position`; every Endpoint below is served at the Base URL followed by `/entity/position`.

| Action | Method | Path | Parameters |
| --- | --- | --- | --- |
| `add` | `POST` | `/entity/position/add` | `entity` (body, required), `instance` (body, optional) |
| `update` | `PUT` | `/entity/position/update` | `entity` (body, required), `instance` (body, optional) |
| `list` | `POST` | `/entity/position/list` | `filters` (body, optional), `combination` (body, optional), `orders` (body, optional), `limit` (body, optional), `instance` (body, optional) |
| `get_by_id` | `GET` | `/entity/position/get_by_id/{id}` | `id` (path, required), `instance` (query, optional) |
| `delete` | `DELETE` | `/entity/position/delete/{id}` | `id` (path, required), `instance` (query, optional) |
| `enable` | `PATCH` | `/entity/position/enable/{id}` | `id` (path, required), `instance` (body, optional) |
| `disable` | `PATCH` | `/entity/position/disable/{id}` | `id` (path, required), `instance` (body, optional) |
| `count` | `POST` | `/entity/position/count` | `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `sum` | `POST` | `/entity/position/sum` | `field` (body, required), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `min` | `POST` | `/entity/position/min` | `field` (body, required), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `max` | `POST` | `/entity/position/max` | `field` (body, required), `filters` (body, optional), `combination` (body, optional), `instance` (body, optional) |
| `truncate` | `DELETE` | `/entity/position/truncate` | `instance` (query, optional) |

One example runs every Endpoint of the Position Adapter in turn. It adds a record, reads it, changes it, queries it, disables and enables it and deletes it again, leaving the data as it was. The final truncate step then empties the whole Position table (or is refused while other records refer to it), so run that step only on a table you mean to empty.

```python
import httpx
import yaml

api = yaml.safe_load(open("config.yaml"))["url"]
client = httpx.Client(base_url=f"{api}/entity/position")

new = {
    "user_id": 1,
    "name": "example",
    "trading_platform_id": 1,
    "broker_id": 1,
    "account_id": 1,
    "trailing_group_id": 1,
    "partial_group_id": 1,
    "action_group_id": 1,
    "action_id": 1,
    "date": "2026-01-02T03:04:05+00:00",
    "volume": "0.10",
    "profit": "0",
    "is_executed": False,
    "order_type": "buy",
    "base_tp": "1",
    "base_sl": "1",
    "real_tp": "1",
    "real_sl": "1",
    "is_active": True,
    "description": None,
}

# add: POST /add
added = client.post("/add", json={"entity": new}).json()
print(added)

# get_by_id: GET /get_by_id/{id}
print(client.get(f"/get_by_id/{added['id']}").json())

# update: PUT /update
added["description"] = "Changed by the example"
print(client.put("/update", json={"entity": added}).json())

# list: POST /list
only = [{"field": "id", "operator": "EQUALS", "value": added["id"]}]
print(
    client.post(
        "/list",
        json={
            "filters": only,
            "orders": [{"field": "id", "direction": "DESCENDING"}],
            "limit": 5,
        },
    ).json()
)

# count: POST /count
print(client.post("/count", json={"filters": only}).json())

# sum, min and max: POST /sum, /min, /max
print(client.post("/sum", json={"field": "id", "filters": only}).json())
print(client.post("/min", json={"field": "id", "filters": only}).json())
print(client.post("/max", json={"field": "id", "filters": only}).json())

# disable and enable: PATCH /disable/{id}, /enable/{id}
print(client.patch(f"/disable/{added['id']}").json()["is_active"])
print(
    client.patch(f"/enable/{added['id']}", json={"instance": "SQLITE"}).json()[
        "is_active"
    ]
)

# delete: DELETE /delete/{id}
print(client.delete(f"/delete/{added['id']}").json()["id"])

# truncate: DELETE /truncate removes every record of this Entity, or is refused while other records refer to them.
print(client.delete("/truncate").status_code)
```
## Use

A client sends an HTTP request to an Endpoint's address and reads the JSON answer. The address is the Base URL (which already ends with the key, when there is one), then `/entity`, the Adapter segment and the Endpoint path; the Method and the Parameters are the ones in the Entity's table. The Entity is chosen by the Adapter, so a request never names it.

```python
import httpx
import yaml

api = yaml.safe_load(open("config.yaml"))["url"]
currency = httpx.Client(base_url=f"{api}/entity/currency")

found = currency.post(
    "/list",
    json={
        "filters": [{"field": "code", "operator": "STARTS_WITH", "value": "U"}],
        "orders": [{"field": "code", "direction": "DESCENDING"}],
        "limit": 3,
    },
)
print(found.status_code, [item["code"] for item in found.json()])
print(currency.get("/get_by_id/1", params={"instance": "SQLITE"}).json()["code"])
```

An error is returned as Problem Details, with the error's class name as `type` and the status that class has: `InvalidInputError` 422, `InactiveInstanceError` and `ConnectionFailureError` 503, and `ExecutionError`, `DeclarationMismatchError` and `ConfigurationError` 500; a request the framework cannot read is `RequestValidationError` with 422.

```python
import httpx
import yaml

api = yaml.safe_load(open("config.yaml"))["url"]
answer = httpx.post(
    f"{api}/entity/currency/list",
    json={"filters": [{"field": "nope", "operator": "EQUALS", "value": 1}]},
)
print(answer.status_code, answer.headers["content-type"], answer.json()["type"])
```

The interactive documentation of all Endpoints, with one section per Adapter, is at the `docs` and `redoc` addresses of `config.yaml`.

## Verify

Run the script below from the API directory with `uv run python`. It checks, from the application itself, that the Entity Group has one Adapter for every Entity that Entity Service presents, in order, and one Endpoint for every Action of that Entity's Child Service, that no other Endpoint is served beneath the Group, and that every Adapter section of the interactive documentation holds exactly its Endpoints. It reads the Child Services and the published schema only, changes no data, and prints `Entity Group verified` when every check holds.

```python
import inspect
import re

from fastapi.testclient import TestClient
from logic.interface import Entity

from api.bootstrap import app, configuration

key = configuration["key"]
client = TestClient(app)
schema = client.get(f"/{key}/openapi.json").json()
adapters = {}
for path, item in schema["paths"].items():
    parts = path.removeprefix(f"/{key}" if key else "").strip("/").split("/")
    assert parts[0] == "entity", path
    adapters.setdefault(parts[1], []).append((parts[2], list(item)))

snake = lambda name: re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
entities = [name for name in vars(Entity.Service) if not name.startswith("_")]
assert list(adapters) == [snake(name) for name in entities]

for name in entities:
    child = getattr(Entity.Service, name)
    actions = sorted(
        member
        for member, value in inspect.getmembers(child, inspect.isfunction)
        if not member.startswith("_")
    )
    operations = sorted(operation for operation, methods in adapters[snake(name)])
    assert operations == actions, (name, operations, actions)
    assert all(len(methods) == 1 for _, methods in adapters[snake(name)]), name

for tag in schema["tags"]:
    holders = {
        path
        for path, item in schema["paths"].items()
        for operation in item.values()
        if tag["name"] in operation["tags"]
    }
    assert len(holders) == 12, tag
assert [tag["name"] for tag in schema["tags"]] == [
    f"Entity · {name}" for name in entities
]
assert schema["x-tagGroups"][0]["tags"] == [tag["name"] for tag in schema["tags"]]

print("Entity Group verified")
```
