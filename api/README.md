# API

## Overview

API is the one running network boundary of the application: it serves every Group beneath its own address segment and has no Endpoint of its own. A client sends a `POST` with a JSON body to an address that names a Group, an Adapter, and an operation and receives exactly what that Group's Endpoint answers, and interactive documentation of every Endpoint is served beside them. For example, this request lists the first three currencies through the Entity Group:

```bash
curl -s -X POST http://127.0.0.1:8000/<key>/entity/currency/list -H 'Content-Type: application/json' -d '{"orders": [{"field": "id"}], "limit": 3}'
```

## Configuration

API reads every runtime value from `config.yaml` at the API root when it starts; source holds none of them. They are:

| Value | Setting | Meaning |
| --- | --- | --- |
| `title` | `Target API` | the title the running API carries |
| `description` | empty | the description the running API carries |
| `key` | `<key>` | a random URL-safe segment of 32 characters, generated once when the key setting is on and kept on every later generation; it is placed before every Group segment and is not authentication |
| `host` | `127.0.0.1` | the address API listens on |
| `port` | `8000` | the port API listens on |
| `workers` | `2` | the number of worker processes serving requests |
| `transport_protocol` | `HTTP` | the protocol used to form the Base URL |
| `url` | `http://127.0.0.1:8000/<key>` | the Base URL, derived from the protocol, host, port, and key |
| `documentation.swagger` | `http://127.0.0.1:8000/<key>/docs` | the address of the first interactive documentation page, derived from the Base URL |
| `documentation.redoc` | `http://127.0.0.1:8000/<key>/redoc` | the address of the second interactive documentation page, derived from the Base URL |

The Base URL is the protocol in lower case, `://`, the host, `:`, and the port, followed by `/` and the key when the key is not empty. With these values it is `http://127.0.0.1:8000/<key>`. The two documentation pages sit at the Base URL followed by `/docs` and `/redoc`, and the schema document they load at the Base URL followed by `/openapi.json`; every Endpoint address below follows the Base URL too.

The key is the `key` value in `config.yaml`; read it there and place it where `<key>` appears in this documentation. Generating again keeps the key; removing `config.yaml` and generating gives a new one, and every address then changes with it.

## Groups

Every Group is registered beneath the Base URL (which already ends with the key) at the segment of its name. Its Endpoints are explained in its own documentation, not here.

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
curl -s -X POST http://127.0.0.1:8000/<key>/entity/broker/get_by_id/1 -H 'Content-Type: application/json' -d '{}'
```

Interactive documentation of every Endpoint is at `http://127.0.0.1:8000/<key>/docs` and `http://127.0.0.1:8000/<key>/redoc`. Every Endpoint of every Group is also listed in that Group's own documentation (see [Groups](#groups)).

## Verify

To see that every listed Group is served beneath its segment and nothing else is served as an Endpoint:

1. For each Group in the [Groups](#groups) table, send one of its documented requests to `<Base URL>/<segment>/...`; it answers with the Group's own result.
2. Open the two documentation addresses: each answers with an interactive page that lists exactly the Endpoints of the listed Groups.
3. Send requests to addresses that belong to no Group and are not the documentation: the root, a made-up address beneath the key, and the documentation locations without the key. None is served.

```bash
# expect 200
curl -s -o /dev/null -w '%{http_code}\n' -X POST http://127.0.0.1:8000/<key>/entity/user/count -H 'Content-Type: application/json' -d '{}'
# expect 200
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8000/<key>/docs
# expect 200
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8000/<key>/redoc
# expect 404
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8000/
# expect 404
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8000/<key>/nothing-here
# expect 404
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8000/docs
# expect 404
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8000/openapi.json
```

The first three print `200` and the other four print `404`.

## Troubleshooting

- **`404 Not Found`** — the address is wrong: the key is missing or misspelled, or a Group, Adapter, or operation is. Rebuild the address from the Base URL (with its key), the Group segment, the Adapter segment, and the operation. A record that does not exist is not a 404: its Endpoint answers `200` with `null`. The documentation pages are also 404 without the key.
- **`405 Method Not Allowed`** — every Endpoint answers `POST` only; a `GET` (for example opening the address in a browser) is refused. Use `curl -X POST ...` or an HTTP client, or try the Endpoint from the interactive documentation.
- **`422 Unprocessable Entity`** — the request does not fit the operation's parameters: the body is not a JSON object, a required parameter is missing, or a value has the wrong type. The answer names the parameter.
- **`500 Internal Server Error`** — the Action behind the Endpoint failed and its failure is passed on unchanged. Common causes are an unprepared Database (prepare it as its documentation explains), adding a record that breaks a uniqueness rule, referring to a record that does not exist, or removing a record another record refers to; the server's log shows the Action's own error message.
- **The key is lost or every address stopped working** — read the current `key` in `config.yaml`. If `config.yaml` was removed and generated again, the key is new and every address, including the documentation, follows it.
- **The browser blocks a request from another site** — API allows every origin, method, and header and sends no credentials; check that the page sends a `POST` with `Content-Type: application/json` to the full address, including the key.
- **`Address already in use` when starting** — another process already listens on the configured port. Stop it, then start API again.
- **`Connection refused`** — API is not running or not on the configured host and port; start it as in [Setup](#setup).
