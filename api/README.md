# API

The external HTTP boundary of the Trading Assistant application.

## Overview

The API is one HTTP address through which external consumers use the application's capabilities. Every capability the application publishes for external use is reachable here, through one running API with one address and one lifecycle. Nothing else is reachable.

How to reach it:

- The operator decides the address and port the API listens on; this document calls it `<base>`.
- Every capability is served under the version prefix `/v1`, for example `<base>/v1/entity/currency/list`. A request without the prefix, or under another version, is not answered by any capability.
- The health and readiness signals (see Lifecycle) and the description of the boundary, below, are the only routes outside the version prefix.
- No authentication is required or checked.
- The machine-readable description of the whole boundary, with every Group, Endpoint, request, response, version and failure, is served by the running API at `<base>/openapi.json`, and interactive views of it at `<base>/docs` and `<base>/redoc`.

Requests and responses use JSON. Every response carries an `X-Request-ID` header holding a non-secret identifier for that request, which you can quote when you report a problem.

## Groups

The API is divided into Groups. Each Group is the external surface of exactly one published application Service, has its own routes under `/v1/<group>`, and is documented below on its own. A Service the application keeps internal has no Group.

### Entity

Group `entity` corresponds to the Entity Service. It offers the same set of capabilities for each kind of record the application stores. Each kind of record is a resource of the Group with its own routes, `/v1/entity/<resource>/<action>`. The resources are:

| Resource | Records it manages |
|---|---|
| `user` | User |
| `trading_platform` | Trading Platform |
| `instance` | Instance |
| `currency` | Currency |
| `broker` | Broker |
| `asset` | Asset |
| `account_group` | Account Group |
| `account` | Account |
| `trailing_group` | Trailing Group |
| `trailing_rule` | Trailing Rule |
| `partial_group` | Partial Group |
| `partial_rule` | Partial Rule |
| `action_group` | Action Group |
| `action` | Action |
| `position` | Position |

## Endpoints

### Entity

Every resource of the Entity Group offers the same twelve Endpoints, so each one is described once, with `<resource>` standing for any resource listed under Groups (for example `currency`). All routes are under `/v1/entity/<resource>/`. The Requests, Responses, Failures and Collections sections describe the columns in detail.

| Action | Method and route | Purpose | Request | Response | Failures |
|---|---|---|---|---|---|
| `add` | `POST /v1/entity/<resource>/add` | Create a record. | JSON body: the record; optional `instance`. | `201`, the created record. | `409`, `422`, `500` |
| `update` | `PUT /v1/entity/<resource>/update` | Replace every mutable field of a record. | JSON body: the whole record including its `id`; optional `instance`. | `200`, the updated record. | `404`, `409`, `422`, `500` |
| `list` | `GET /v1/entity/<resource>/list` | List records. | Optional `limit` and `instance`. | `200`, a list of records. | `409`, `422`, `500` |
| `get_by_id` | `GET /v1/entity/<resource>/get_by_id` | Retrieve one record by its id. | `record_id`; optional `instance`. | `200`, the record. | `404`, `409`, `422`, `500` |
| `count` | `GET /v1/entity/<resource>/count` | Count the records. | Optional `instance`. | `200`, a whole number. | `409`, `422`, `500` |
| `sum` | `GET /v1/entity/<resource>/sum` | Total one field over the records. | `field`; optional `instance`. | `200`, the total. | `409`, `422`, `500` |
| `min` | `GET /v1/entity/<resource>/min` | Find the smallest value of one field. | `field`; optional `instance`. | `200`, the value, or `null` when there is none. | `409`, `422`, `500` |
| `max` | `GET /v1/entity/<resource>/max` | Find the largest value of one field. | `field`; optional `instance`. | `200`, the value, or `null` when there is none. | `409`, `422`, `500` |
| `enable` | `POST /v1/entity/<resource>/enable` | Mark a record active. | `record_id`; optional `instance`. | `200`, the record. | `404`, `409`, `422`, `500` |
| `disable` | `POST /v1/entity/<resource>/disable` | Mark a record inactive. | `record_id`; optional `instance`. | `200`, the record. | `404`, `409`, `422`, `500` |
| `delete` | `DELETE /v1/entity/<resource>/delete` | Delete a record. | `record_id`; optional `instance`. | `200`, `true`. | `404`, `409`, `422`, `500` |
| `truncate` | `DELETE /v1/entity/<resource>/truncate` | Delete every record of the resource. | Optional `instance`. | `200`, the number of records deleted. | `409`, `422`, `500` |

`truncate` removes all records of the resource at once and, because the API requires no authentication, any caller can use it.

## Requests

Every input is either a value in the query string or, for `add` and `update`, a JSON body. No input is carried in the route. An input that is not described here, in the query string or in the body, is refused (see Failures).

### Inputs

| Input | Where | Type | Meaning |
|---|---|---|---|
| `record_id` | query, required | whole number | The id of the record to retrieve, enable, disable or delete. |
| `field` | query, required | one of the fields the resource returns | The field that `sum`, `min` and `max` work on. Any other name is refused; fields that are never returned (see Credentials) cannot be named. |
| `limit` | query, optional | whole number from `1` to `100` | The number of records `list` returns; `50` when omitted. See Collections. |
| `instance` | query, optional | `sqlite` or `postgresql` | Selects which of the active data instances the request works on. When omitted, the API uses its default instance. Any other value is refused. |
| the record | JSON body | object | The record to create (`add`) or the whole record to replace (`update`); see Records. |

Each Endpoint takes only the inputs listed for it under Endpoints.

### Records

The body of `add` and `update` is a JSON object with exactly the fields of the resource, described in the tables below. A field that is not in its table is refused, and so is a value of the wrong type or a missing required field.

- `add` creates a record. The `id` is generated and is not accepted.
- `update` replaces the whole record whose `id` is given. Send every field of the record: an optional field you leave out takes its default value, and the record's current value is not kept.
- Fields that refer to another record (those ending in `_id`) must name a record that exists. A reference to a record that does not exist makes the request fail, and nothing is created or changed (see Failures).
- A value the application refuses, for example a text longer than its limit or an unmet rule, is answered with a failure that names the rule (see Failures).

#### Credentials

Some fields are credentials: `password` and `api_key` of `user`, `password` and `api_key` of `instance`, and `password` of `account`. You supply them in `add` and `update` exactly as they are, and the application stores them protected. They are never returned by any Endpoint, and they cannot be used as the `field` of `sum`, `min` or `max`. Because `update` replaces the whole record, an `update` of one of these records must supply its credentials again, and they become the stored credentials.

#### `user`

| Field | Type | On `add` | On `update` | In responses |
|---|---|---|---|---|
| `id` | whole number | not accepted (generated) | required | yes |
| `name` | text | required | required | yes |
| `username` | text | required | required | yes |
| `password` | text | required | required | never returned |
| `api_key` | text | required | required | never returned |
| `is_active` | `true` or `false` | optional | optional | yes |
| `description` | text, may be `null` | optional | optional | yes |

#### `trading_platform`

| Field | Type | On `add` | On `update` | In responses |
|---|---|---|---|---|
| `id` | whole number | not accepted (generated) | required | yes |
| `name` | text | required | required | yes |
| `code` | text | required | required | yes |
| `is_active` | `true` or `false` | optional | optional | yes |
| `description` | text, may be `null` | optional | optional | yes |

#### `instance`

| Field | Type | On `add` | On `update` | In responses |
|---|---|---|---|---|
| `id` | whole number | not accepted (generated) | required | yes |
| `user_id` | whole number | required | required | yes |
| `trading_platform_id` | whole number | required | required | yes |
| `name` | text | required | required | yes |
| `ip` | text, may be `null` | optional | optional | yes |
| `username` | text, may be `null` | optional | optional | yes |
| `password` | text, may be `null` | optional | optional | never returned |
| `api_key` | text, may be `null` | optional | optional | never returned |
| `is_active` | `true` or `false` | optional | optional | yes |
| `description` | text, may be `null` | optional | optional | yes |

#### `currency`

| Field | Type | On `add` | On `update` | In responses |
|---|---|---|---|---|
| `id` | whole number | not accepted (generated) | required | yes |
| `user_id` | whole number | required | required | yes |
| `code` | text, at most 3 characters | required | required | yes |
| `symbol` | text, may be `null` | optional | optional | yes |
| `country` | text, may be `null` | optional | optional | yes |
| `decimal_digits` | whole number | optional | optional | yes |
| `is_active` | `true` or `false` | optional | optional | yes |
| `description` | text, may be `null` | optional | optional | yes |

#### `broker`

| Field | Type | On `add` | On `update` | In responses |
|---|---|---|---|---|
| `id` | whole number | not accepted (generated) | required | yes |
| `name` | text | required | required | yes |
| `user_id` | whole number | required | required | yes |
| `is_active` | `true` or `false` | optional | optional | yes |
| `description` | text, may be `null` | optional | optional | yes |

#### `asset`

| Field | Type | On `add` | On `update` | In responses |
|---|---|---|---|---|
| `id` | whole number | not accepted (generated) | required | yes |
| `broker_id` | whole number | required | required | yes |
| `symbol` | text | required | required | yes |
| `category` | text | required | required | yes |
| `point_size` | number | optional | optional | yes |
| `digits` | whole number | optional | optional | yes |
| `is_active` | `true` or `false` | optional | optional | yes |
| `description` | text, may be `null` | optional | optional | yes |

#### `account_group`

| Field | Type | On `add` | On `update` | In responses |
|---|---|---|---|---|
| `id` | whole number | not accepted (generated) | required | yes |
| `user_id` | whole number | required | required | yes |
| `name` | text | required | required | yes |
| `is_active` | `true` or `false` | optional | optional | yes |
| `description` | text, may be `null` | optional | optional | yes |

#### `account`

| Field | Type | On `add` | On `update` | In responses |
|---|---|---|---|---|
| `id` | whole number | not accepted (generated) | required | yes |
| `name` | text | required | required | yes |
| `group_id` | whole number | required | required | yes |
| `broker_id` | whole number | required | required | yes |
| `instance_id` | whole number | required | required | yes |
| `base_currency_id` | whole number | required | required | yes |
| `username` | text | required | required | yes |
| `password` | text | required | required | never returned |
| `leverage` | whole number | required | required | yes |
| `balance` | decimal number (JSON number or numeric text) | optional | optional | yes |
| `account_type` | text | required | required | yes |
| `is_active` | `true` or `false` | optional | optional | yes |
| `description` | text, may be `null` | optional | optional | yes |

#### `trailing_group`

| Field | Type | On `add` | On `update` | In responses |
|---|---|---|---|---|
| `id` | whole number | not accepted (generated) | required | yes |
| `user_id` | whole number | required | required | yes |
| `name` | text | required | required | yes |
| `is_active` | `true` or `false` | optional | optional | yes |
| `description` | text, may be `null` | optional | optional | yes |

#### `trailing_rule`

| Field | Type | On `add` | On `update` | In responses |
|---|---|---|---|---|
| `id` | whole number | not accepted (generated) | required | yes |
| `name` | text | required | required | yes |
| `trailing_group_id` | whole number | required | required | yes |
| `trigger_percentage` | decimal number (JSON number or numeric text) | required | required | yes |
| `take_profit_adjustment` | decimal number (JSON number or numeric text), may be `null` | optional | optional | yes |
| `stop_loss_adjustment` | decimal number (JSON number or numeric text), may be `null` | optional | optional | yes |
| `is_active` | `true` or `false` | optional | optional | yes |
| `description` | text, may be `null` | optional | optional | yes |

#### `partial_group`

| Field | Type | On `add` | On `update` | In responses |
|---|---|---|---|---|
| `id` | whole number | not accepted (generated) | required | yes |
| `user_id` | whole number | required | required | yes |
| `name` | text | required | required | yes |
| `is_active` | `true` or `false` | optional | optional | yes |
| `description` | text, may be `null` | optional | optional | yes |

#### `partial_rule`

| Field | Type | On `add` | On `update` | In responses |
|---|---|---|---|---|
| `id` | whole number | not accepted (generated) | required | yes |
| `name` | text | required | required | yes |
| `partial_group_id` | whole number | required | required | yes |
| `profit_percentage` | decimal number (JSON number or numeric text) | required | required | yes |
| `close_percentage` | decimal number (JSON number or numeric text) | required | required | yes |
| `is_active` | `true` or `false` | optional | optional | yes |
| `description` | text, may be `null` | optional | optional | yes |

#### `action_group`

| Field | Type | On `add` | On `update` | In responses |
|---|---|---|---|---|
| `id` | whole number | not accepted (generated) | required | yes |
| `user_id` | whole number | required | required | yes |
| `name` | text | required | required | yes |
| `is_active` | `true` or `false` | optional | optional | yes |
| `description` | text, may be `null` | optional | optional | yes |

#### `action`

| Field | Type | On `add` | On `update` | In responses |
|---|---|---|---|---|
| `id` | whole number | not accepted (generated) | required | yes |
| `name` | text | required | required | yes |
| `action_group_id` | whole number | required | required | yes |
| `asset_id` | whole number | required | required | yes |
| `account_id` | whole number | required | required | yes |
| `partial_group_id` | whole number | required | required | yes |
| `trailing_group_id` | whole number | required | required | yes |
| `risk_by_reward` | decimal number (JSON number or numeric text) | required | required | yes |
| `take_profit` | decimal number (JSON number or numeric text) | required | required | yes |
| `stop_loss` | decimal number (JSON number or numeric text) | required | required | yes |
| `is_active` | `true` or `false` | optional | optional | yes |
| `description` | text, may be `null` | optional | optional | yes |

#### `position`

| Field | Type | On `add` | On `update` | In responses |
|---|---|---|---|---|
| `id` | whole number | not accepted (generated) | required | yes |
| `user_id` | whole number | required | required | yes |
| `name` | text | required | required | yes |
| `trading_platform_id` | whole number | required | required | yes |
| `broker_id` | whole number | required | required | yes |
| `account_id` | whole number | required | required | yes |
| `trailing_group_id` | whole number | required | required | yes |
| `partial_group_id` | whole number | required | required | yes |
| `action_group_id` | whole number | required | required | yes |
| `action_id` | whole number | required | required | yes |
| `date` | date and time (ISO 8601, for example `2026-01-02T03:04:05Z`) | required | required | yes |
| `volume` | decimal number (JSON number or numeric text) | required | required | yes |
| `profit` | decimal number (JSON number or numeric text) | optional | optional | yes |
| `is_executed` | `true` or `false` | optional | optional | yes |
| `order_type` | text | required | required | yes |
| `base_tp` | decimal number (JSON number or numeric text) | required | required | yes |
| `base_sl` | decimal number (JSON number or numeric text) | required | required | yes |
| `real_tp` | decimal number (JSON number or numeric text) | required | required | yes |
| `real_sl` | decimal number (JSON number or numeric text) | required | required | yes |
| `is_active` | `true` or `false` | optional | optional | yes |
| `description` | text, may be `null` | optional | optional | yes |

## Responses

A successful request returns its result directly as JSON, with no wrapping envelope, and with the status shown under Endpoints.

### Records

`add`, `update`, `get_by_id`, `enable` and `disable` return one record, and `list` returns an array of records. A record is a JSON object with the fields marked `yes` in the Records tables under Requests, and with no other field. Values are represented as follows:

| Field type | In a response |
|---|---|
| whole number | a JSON number, for example `2` |
| number | a JSON number, for example `0.0211` |
| decimal number | text, for example `"1.5"` |
| text | text |
| `true` or `false` | `true` or `false` |
| date and time | text in ISO 8601 with a time zone, for example `"2026-01-02T03:04:05Z"` |
| an optional field with no value | `null` |

Example, the response to `GET /v1/entity/currency/get_by_id?record_id=1` on a prepared store:

```json
{"id":1,"user_id":1,"code":"USD","symbol":"$","country":"United States","decimal_digits":2,"is_active":true,"description":null}
```

`list` returns `[]` when the resource holds no records.

### Values

| Endpoint | Response |
|---|---|
| `count` | the number of records, a whole number |
| `truncate` | the number of records deleted, a whole number |
| `delete` | `true` |
| `sum` | the total of the field over the records, in the field's own representation; zero when there is no usable value (`0`, or `"0"` for a decimal number field) |
| `min`, `max` | the smallest or largest value of the field in the field's own representation, or `null` when there is none |

`sum` totals numbers. Asking for the sum of a field that holds text, dates or true/false values fails (see Failures). `min` and `max` work on any field the resource returns.

### Credentials

No response carries a credential value in any form: the fields listed under Credentials in Requests are left out of every record, and no other response contains them.

## Failures

Every failure has the same JSON body:

```json
{"detail": "No record has the requested id", "request_id": "3f2a9c0d5e7b4c1a8d6e0f1b2c3d4e5f"}
```

`detail` says what went wrong and never repeats a value you sent, and `request_id` is the non-secret identifier of the request, equal to the `X-Request-ID` response header. Quote it when you report a problem. A failure is always a failing status: it is never answered as a success.

| Status | When | `detail` |
|---|---|---|
| `404` | The record named by `record_id`, or by the `id` of an `update`, does not exist. | `No record has the requested id` |
| `404` | The route is not served (an unknown route, a route without the version prefix, another version). | `Not Found` |
| `405` | The route exists but not for that method. | `Method Not Allowed` |
| `409` | The application refuses the request because one of its rules is not met. | The rule that was not met, for example `An Account password must not duplicate the password or api_key of its Instance` |
| `422` | The input does not match what the Endpoint accepts: a required input or field is missing, an input or field is not described in this document, a value has the wrong type, or a number is out of range. | Each problem as `location: message`, separated by `;`, for example `body.name: Field required` or `query.limit: Input should be less than or equal to 100` |
| `500` | Any failure the API does not declare. | `Internal server error`. Nothing about the cause is revealed. |

Some requests that the stored data forbids are answered with `500` today, and change nothing:

- a field ending in `_id` that names a record that does not exist;
- a value that must be unique and duplicates an existing one, such as the `code` of a currency;
- deleting a record that another record still refers to;
- `sum` of a field that holds text, dates or true/false values.

## Collections

A collection is what `list` returns, and what `count`, `sum`, `min` and `max` work over: all the records of one resource.

### Page size

`list` returns at most `limit` records. `limit` is a whole number from `1` to `100`; when you leave it out, `50` records are returned at most. A `limit` outside that range, or one that is not a whole number, is refused with `422`, so no request returns more than 100 records and none is unbounded.

### No following page

`list` always returns records from the start of the collection. The API offers no way to ask for a following page, so when a resource holds more than 100 records the ones beyond the first 100 cannot be listed. `count` tells you how many records a resource holds.

### No filtering or ordering

No Endpoint accepts a filter, a combination of filters, or an ordering. An input that asks for one is not described in this document and is refused with `422`, exactly like any other undescribed input. The order in which records are listed is not defined by this document.

### Aggregates

`count` counts every record of the resource, whatever `limit` would allow. `sum`, `min` and `max` work over every record and need the input `field`, which must be the name of a field the resource returns (see the Records tables under Requests). Any other name is refused with `422`; that includes the credential fields, which are never returned.

### Data instance

The collection inputs `limit` and `field` behave the same whichever `instance` you select; the optional `instance` chooses which data instance the whole request works on.

## Lifecycle

The API always serves two signals, health and readiness. They belong to the API as a whole, not to any Group, so they are not Endpoints and do not appear in the contract of Group Endpoints. Neither can be disabled.

### Health

Health reports that the API process is alive. It answers the same way whether or not the API is ready to serve requests, so an operator can tell a running process from one that cannot yet serve.

```text
GET /health
200  {"status": "alive"}
```

### Readiness

Readiness reports whether the API can serve requests. It is positive only after the API has started with all of its required runtime values validated, and only while the application capabilities it serves are available. It is negative before startup completes, while those capabilities are unavailable, and once the API is shutting down.

```text
GET /ready
200  {"status": "ready"}
503  {"status": "not ready"}
```

Readiness reflects only what the API itself can observe about the capabilities it serves. It does not check anything beyond them.

### Locations

The locations are `/health` and `/ready` by default. Each can be moved with an optional runtime value, supplied through the environment:

| Runtime value | Meaning | Default |
|---|---|---|
| `API_HEALTH_PATH` | Location of the health signal | `/health` |
| `API_READINESS_PATH` | Location of the readiness signal | `/ready` |

A location must be an absolute path such as `/alive`. The two locations must differ, and neither may be a reserved documentation location (`/docs`, `/redoc`, `/openapi.json`). A value that is empty, is a word such as `off`, or is otherwise not a usable location is refused when the API starts, naming the value; there is no setting that removes a signal.

```text
API_HEALTH_PATH=/alive API_READINESS_PATH=/serving
GET /alive     200  {"status": "alive"}
GET /serving   200  {"status": "ready"}
GET /health    404
```

## Examples

The examples use `curl` and work through one currency from creation to deletion. They assume the API's data holds its initial records (User 1 exists and there are eight currencies), so the currency created below gets id `9`; your ids are those your data gives you. Set `BASE` to the address the operator gave you first:

```bash
BASE=http://127.0.0.1:8000
```

No example sends or shows a credential.

### Check that the API is alive

```bash
curl -s "$BASE/health"
```

```text
{"status":"alive"}
```

### Create a currency

```bash
curl -s -X POST "$BASE/v1/entity/currency/add" -H 'Content-Type: application/json' -d '{"user_id": 1, "code": "SEK", "symbol": "kr", "country": "Sweden", "decimal_digits": 2}'
```

```text
{"id":9,"user_id":1,"code":"SEK","symbol":"kr","country":"Sweden","decimal_digits":2,"is_active":true,"description":null}
```

### Retrieve it

```bash
curl -s "$BASE/v1/entity/currency/get_by_id?record_id=9"
```

```text
{"id":9,"user_id":1,"code":"SEK","symbol":"kr","country":"Sweden","decimal_digits":2,"is_active":true,"description":null}
```

### Replace it

`update` takes the whole record, so every field is sent again.

```bash
curl -s -X PUT "$BASE/v1/entity/currency/update" -H 'Content-Type: application/json' -d '{"id": 9, "user_id": 1, "code": "SEK", "symbol": "Skr", "country": "Sweden", "decimal_digits": 2}'
```

```text
{"id":9,"user_id":1,"code":"SEK","symbol":"Skr","country":"Sweden","decimal_digits":2,"is_active":true,"description":null}
```

### Disable it

```bash
curl -s -X POST "$BASE/v1/entity/currency/disable?record_id=9"
```

```text
{"id":9,"user_id":1,"code":"SEK","symbol":"Skr","country":"Sweden","decimal_digits":2,"is_active":false,"description":null}
```

### Enable it again

```bash
curl -s -X POST "$BASE/v1/entity/currency/enable?record_id=9"
```

```text
{"id":9,"user_id":1,"code":"SEK","symbol":"Skr","country":"Sweden","decimal_digits":2,"is_active":true,"description":null}
```

### List the first two currencies

```bash
curl -s "$BASE/v1/entity/currency/list?limit=2"
```

```text
[{"id":1,"user_id":1,"code":"USD","symbol":"$","country":"United States","decimal_digits":2,"is_active":true,"description":null},{"id":2,"user_id":1,"code":"EUR","symbol":"€","country":"Eurozone","decimal_digits":2,"is_active":true,"description":null}]
```

### Count the records

```bash
curl -s "$BASE/v1/entity/currency/count"
```

```text
9
```

### Find the largest id

```bash
curl -s "$BASE/v1/entity/currency/max?field=id"
```

```text
9
```

### Work on a chosen data instance

`instance` is optional; the accepted values are listed under Requests.

```bash
curl -s "$BASE/v1/entity/currency/count?instance=sqlite"
```

```text
9
```

### Delete it

```bash
curl -s -X DELETE "$BASE/v1/entity/currency/delete?record_id=9"
```

```text
true
```

### See a failure

The record was deleted, so it is no longer found. Your `request_id` differs.

```bash
curl -s -w "\n%{http_code}\n" "$BASE/v1/entity/currency/get_by_id?record_id=9"
```

```text
{"detail":"No record has the requested id","request_id":"69bb4ddbfd6a45bca4575a08b43b2943"}
404
```

### See a refused input

`limit` may not exceed 100. Your `request_id` differs.

```bash
curl -s -w "\n%{http_code}\n" "$BASE/v1/entity/currency/list?limit=101"
```

```text
{"detail":"query.limit: Input should be less than or equal to 100","request_id":"d1cbb81a4d0e40d3819ea797d8951c8d"}
422
```
