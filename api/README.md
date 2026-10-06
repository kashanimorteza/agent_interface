# API

## Overview

API is the application's one network boundary: a separate executable that serves every Group beneath its own URL
segment over the Logic library and has no Endpoint of its own. Bootstrap reads the runtime Configuration, creates the
API, registers every Group, and starts serving, and the interactive documentation of every Endpoint is always served.

`BASE` below is the Base URL from the runtime Configuration (`url`), and `JSON` is the header
`Content-Type: application/json`.

```sh
curl -s -X POST "$BASE/entity/currency/count" -H "$JSON" -d '{}'  # 200
```

```json
8
```

## Configuration

Every value that identifies or runs the API lives in `config.yaml` in the API directory, and Bootstrap reads it
only from there. Regenerating the API keeps the URL Key already in it.

| Value | Meaning | Prepared value |
|---|---|---|
| `title` | The name the API and its documentation present. | `Target API` |
| `description` | The description they present. | empty |
| `key` | An opaque URL path segment placed before every Group segment: random URL-safe text of 32 characters, generated once and kept. It only changes the path; it does not authenticate a request. | generated, not shown here |
| `host` | The address the API binds to. | `127.0.0.1` |
| `port` | The port it binds to. | `8000` |
| `workers` | The number of worker processes. | `2` |
| `transport_protocol` | The transport protocol of the Base URL. | `HTTP` |
| `url` | The Base URL, derived from the values above. | `http://127.0.0.1:8000/<key>` |
| `documentation` | The addresses of the two interactive documentation interfaces, derived from `url`. | `<url>/docs` and `<url>/redoc` |

The Base URL is the transport protocol in lower case, `://`, the host, `:`, the port, and then `/` and the key when the
key is not empty. Each documentation address is the Base URL followed by `/docs` or `/redoc`. `url` and `documentation`
are derived, so when you edit the host, port, or key, edit them together.

## Groups

| Group | URL segment | Served beneath | Documentation |
|---|---|---|---|
| Entity | `entity` | `<Base URL>/entity/<adapter>/<operation>` | [Entity Group](api/groups/entity/README.md) |

Every Group is served exactly as its own documentation states; the API adds no Endpoint, wrapper, or behaviour to
it.

## Setup

Requirements: Python 3.14 or newer, [uv](https://docs.astral.sh/uv/), and the sibling `logic`, `database`, and `model`
projects: the API depends on Logic, and Logic depends on Database and Model.

```bash
cd api
uv sync
```

`uv sync` creates the isolated environment in `.venv` from `pyproject.toml` and `uv.lock`, with Logic installed from
its sibling directory. The Database storage must hold its Tables and Initial Data before the first request. Prepare
it once; repeating it changes nothing:

```bash
uv run python -c "from logic.interface import Storage; Storage.Storage().prepare()"
```

Start the API from the API directory. It serves at the configured host and port with the configured number of worker
processes until it is stopped:

```bash
uv run python -m api.bootstrap
```

## Use

A client reaches a Group at the Base URL, the Group's URL segment, the Adapter's segment, and the operation. The Entity
Group's Adapters and Endpoints are in its own documentation.

```sh
curl -s "$BASE/entity/currency/get_by_id/2"  # 200
```

```json
{
  "id": 2,
  "user_id": 1,
  "code": "EUR",
  "symbol": "€",
  "country": "Eurozone",
  "decimal_digits": 2,
  "is_active": true,
  "description": null
}
```

Every Endpoint is listed in the interactive documentation at the `documentation` addresses of the Configuration,
organized in one section per Group and, within it, one per Adapter. A request that cannot be served returns Problem
Details (`application/problem+json`) whose `type` is the error's class name.

## Verify

Start the API, then run this script from the API directory with `uv run python`. It reads the Base URL from the
runtime Configuration, fetches the API's machine-readable description, and checks that every Group in the API's Groups
area is registered and served beneath the segment of its name with exactly the Endpoints of its Adapters, that nothing
else is served, that both documentation addresses answer, and that the address without the URL Key is not served. It
prints `all checks passed` when every check holds. Each Group's own documentation shows how to check that every one
of its Adapters and Actions has its Endpoint.

```python
import json
import urllib.error
import urllib.request
from pathlib import Path

import api.groups
import yaml
from api.groups import GROUPS

configuration = yaml.safe_load((Path.cwd() / "config.yaml").read_text())
base = configuration["url"]
with urllib.request.urlopen(f"{base}/openapi.json") as response:
    schema = json.load(response)

present = {
    path.name
    for path in Path(api.groups.__file__).parent.iterdir()
    if path.is_dir() and path.name != "__pycache__"
}
registered = {group.__name__.rsplit(".", 1)[1] for group in GROUPS}
assert registered == present, sorted(registered ^ present)

key = Path(base.split("//", 1)[1]).parts[1:]
served = {tuple(path.strip("/").split("/")[len(key) :]) for path in schema["paths"]}
expected = {
    (group.SEGMENT, adapter, *route.path.strip("/").split("/"))
    for group in GROUPS
    for adapter, router in group.ADAPTERS.items()
    for route in router.routes
}
assert served == expected, (sorted(served - expected), sorted(expected - served))

for address in configuration["documentation"].values():
    assert urllib.request.urlopen(address).status == 200

if key:
    try:
        urllib.request.urlopen(base.rsplit("/", 1)[0] + "/docs")
        raise AssertionError("the documentation answers without the URL Key")
    except urllib.error.HTTPError as error:
        assert error.code == 404

print("all checks passed")
```

## Troubleshooting

- **Every request answers 404.** The request is missing the URL Key or the Group segment. Use the `url` of the
  Configuration, which includes the key, and the Group's segment:

  ```sh
  curl -s -X POST "${BASE%/*}/entity/currency/count" -H "$JSON" -d '{}'  # 404
  ```

- **A request answers 405.** The Method does not match the Endpoint: `list` is a `POST`, for example. Use the Method
  from the Group's table:

  ```sh
  curl -s "$BASE/entity/currency/list"  # 405
  ```

- **A request answers 422 `InvalidInputError`.** A Parameter is missing, has the wrong type, or is not in its stated
  form. The `detail` names the Parameter and the reason, never the value you sent:

  ```sh
  curl -s -X POST "$BASE/entity/currency/count" -H "$JSON" -d '{"filters": "x"}'  # 422
  ```

- **The first request answers 500 `ExecutionError`** with `The request could not be executed or violates a
  constraint`. The Database storage has no Tables yet: prepare it as shown in Setup. The same error is also returned
  for a request that violates a constraint, such as a duplicate or a record another record still references.
- **The API does not start and the log says `address already in use`.** Another process holds the configured port.
  Stop that process, or change `port` in the Configuration together with `url` and `documentation`.
- **The interactive documentation answers 404.** It is served at the `documentation` addresses of the Configuration,
  which include the URL Key, not at `/docs` on the bare address.
