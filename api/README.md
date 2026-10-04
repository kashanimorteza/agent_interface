# API

## Overview

API is the one running network boundary of the application: it serves every Group beneath its own address segment and has no Endpoint of its own. A client sends a `POST` with a JSON body to an address that names a Group, an Adapter, and an operation, and receives exactly what that Group's Endpoint answers. For example, this request lists the first three currencies through the Entity Group:

```bash
curl -s -X POST http://127.0.0.1:8000/entity/currency/list -H 'Content-Type: application/json' -d '{"orders": [{"field": "id"}], "limit": 3}'
```

## Configuration

API reads its runtime values from `config.yaml` at the API root when it starts. They are:

| Value | Setting | Meaning |
| --- | --- | --- |
| `title` | `Target API` | the title the running API carries |
| `description` | empty | the description the running API carries (empty here) |
| `key` | empty | an optional opaque address segment placed before every Group segment; it only changes the address and is not authentication (empty here) |
| `host` | `127.0.0.1` | the address API listens on |
| `port` | `8000` | the port API listens on |
| `workers` | `2` | the number of worker processes serving requests |
| `transport_protocol` | `HTTP` | the protocol used to form the Base URL |
| `url` | `http://127.0.0.1:8000` | the Base URL, derived from the protocol, host, port, and key |

The Base URL is the protocol in lower case, `://`, the host, `:`, and the port, followed by `/` and the key when the key is not empty. With these values it is `http://127.0.0.1:8000`; with the key `abc` it would be `http://127.0.0.1:8000/abc`, and every address below would follow it.

## Groups

Every Group is registered beneath the Base URL (after the key, when there is one) at the segment of its name. Its Endpoints are explained in its own documentation, not here.

| Group | Segment | Documentation |
| --- | --- | --- |
| Entity | `/entity` | [Entity Group](api/groups/entity/README.md) |

## Setup

API needs Python 3.14 or newer and [uv](https://docs.astral.sh/uv/). It runs from the application's directory layout: the `logic`, `database`, and `model` directories sit beside `api`, and the Database's storage must already be prepared (see the Database documentation).

```bash
cd api
uv sync --locked
uv run python -m api.bootstrap
```

The first two commands install exactly the locked dependencies into `.venv`; the last starts API on the configured host and port with the configured number of workers (`127.0.0.1:8000`, 2 workers). Stop it with Ctrl+C.

## Use

A client reaches a Group by sending a `POST` to `<Base URL>/<group segment>/...` with `Content-Type: application/json` and a JSON object as the body. For the Entity Group the address continues with an Entity and an operation, and the body holds the operation's parameters by name:

```bash
curl -s -X POST http://127.0.0.1:8000/entity/broker/get_by_id/1 -H 'Content-Type: application/json' -d '{}'
```

Every Endpoint of every Group is listed in that Group's documentation (see [Groups](#groups)).

## Verify

To see that every listed Group is served beneath its segment and nothing else is:

1. For each Group in the [Groups](#groups) table, send one of its documented requests to `<Base URL>/<segment>/...`; it answers with the Group's own result.
2. Send requests to addresses that belong to no Group: the Base URL itself, a made-up path, and the framework's usual documentation addresses. None is served.

```bash
curl -s -o /dev/null -w '%{http_code}\n' -X POST http://127.0.0.1:8000/entity/user/count -H 'Content-Type: application/json' -d '{}'
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8000/
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8000/docs
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8000/openapi.json
```

The first prints `200`; the other three print `404`.

## Troubleshooting

- **`404 Not Found`** — the address is wrong: a missing or misspelled Group, Adapter, or operation, or a configured key left out of the address. Rebuild the address from the Base URL, the Group segment, the Adapter segment, and the operation. A record that does not exist is not a 404: its Endpoint answers `200` with `null`.
- **`405 Method Not Allowed`** — every Endpoint answers `POST` only; a `GET` (for example opening the address in a browser) is refused. Use `curl -X POST ...` or an HTTP client.
- **`422 Unprocessable Entity`** — the request does not fit the operation's parameters: the body is not a JSON object, a required parameter is missing, or a value has the wrong type. The answer names the parameter.
- **`500 Internal Server Error`** — the Action behind the Endpoint failed and its failure is passed on unchanged. Common causes are adding a record that breaks a uniqueness rule, referring to a record that does not exist, or removing a record another record refers to; the server's log shows the Action's own error message.
- **The browser blocks a request from another site** — API allows every origin, method, and header and sends no credentials; check that the page sends a `POST` with `Content-Type: application/json` to the full address.
- **`Address already in use` when starting** — another process already listens on port 8000. Stop it, then start API again.
- **`Connection refused`** — API is not running or not on `127.0.0.1:8000`; start it as in [Setup](#setup).
