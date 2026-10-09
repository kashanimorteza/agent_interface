# API

## Overview

API is the one running network boundary of the Trading Assistant. It serves every Group of the application beneath its own URL segment and has no Endpoint of its own: a Group's Endpoints call the application's Logic and return what it returns. Today there is one Group, Entity, which serves every Entity of the Logic library.

```bash
# Run from the API directory; the Base URL, with its key, is the url value of config.yaml.
API=$(grep '^url:' config.yaml | cut -d' ' -f2)
curl -s "$API/entity/currency/get_by_id/1"
```

## Configuration

Every runtime value lives in `config.yaml` at the root of the API directory, and the running API reads it only from there. A value is changed in that file and takes effect when the API is started again.

| Value | Meaning |
| --- | --- |
| `title` | the title the API and its interactive documentation present |
| `description` | the description they present; empty by default |
| `key` | an opaque URL path segment placed before every Group segment; empty omits it |
| `host` | the network host or address the API binds to |
| `port` | the network port the API binds to |
| `workers` | the number of worker processes |
| `transport_protocol` | the protocol used to form the Base URL |
| `url` | the Base URL, derived from the protocol, host, port and key |
| `documentation` | the full addresses of the interactive documentation (`swagger` and `redoc`) |

The Base URL is `<transport_protocol>://<host>:<port>` followed by `/<key>` when the key is not empty, written with the protocol in lower case, such as `http://127.0.0.1:8000/<key>`. `url` and the `documentation` addresses are derived from the other values and are never set independently. The key only changes the path of every address; it is not a password and does not authenticate or authorize a request.

## Groups

Every Group is served at the Base URL followed by its segment, which is its name in lower case. The segment of a Group, its Adapters and its Endpoints is described in the Group's own documentation, never repeated here.

| Group | Segment | Documentation |
| --- | --- | --- |
| Entity | `/entity` | [Entity Group](api/groups/entity/README.md) |

## Setup

API is a Python application managed with [uv](https://docs.astral.sh/uv/). It needs Python 3.14 or newer and uses the Logic library of this project as a local path dependency, so the `logic` directory (and the `database` and `model` directories Logic uses) must sit beside the `api` directory.

1. Open the API directory.
2. Install the locked dependencies, Logic included, into an isolated environment:

   ```bash
   uv sync
   ```

3. Prepare the Database's default Instance once, from the Database directory, so the tables and the initial data exist:

   ```bash
   cd ../database
   uv run python scripts/prepare.py
   ```

4. Start the API from the API directory. It serves on the host and port of `config.yaml` with the configured number of workers, and stops with `Ctrl+C`:

   ```bash
   uv run api
   ```

## Use

A client sends an HTTP request to an address beneath the Base URL and reads the JSON answer. Start the API, then call an Endpoint of a Group; the Group's documentation lists its Endpoints.

```python
import httpx
import yaml

api = yaml.safe_load(open("config.yaml"))["url"]
print(httpx.get(f"{api}/entity/user/get_by_id/1").json()["username"])
print(httpx.post(f"{api}/entity/currency/count", json={}).json())
```

The interactive documentation lists every Endpoint of every Group, with one section per Adapter, lets a client try them, and is served at the `swagger` and `redoc` addresses of `config.yaml`.

## Verify

Run the script below from the API directory with `uv run python`, with the API started. It checks that every listed Group is served beneath its segment and that nothing else is: the schema lists only paths beneath the Base URL and the Group segment, the Entity Group answers beneath it, and the same paths answer nothing at the bare address, beneath another key, or without the Group segment. It changes no data and prints `API verified` when every check holds.

```python
import httpx
import yaml

configuration = yaml.safe_load(open("config.yaml"))
api = configuration["url"]
key = configuration["key"]
GROUPS = ["entity"]

schema = httpx.get(f"{api}/openapi.json").json()
prefix = f"/{key}" if key else ""
for path in schema["paths"]:
    segment = path.removeprefix(prefix).split("/")[1]
    assert segment in GROUPS, path
for group in GROUPS:
    assert any(p.startswith(f"{prefix}/{group}/") for p in schema["paths"]), group
    assert httpx.post(f"{api}/{group}/currency/count", json={}).status_code == 200

bare = api.removesuffix(f"/{key}") if key else api
if key:
    assert httpx.post(f"{bare}/entity/currency/count", json={}).status_code == 404
    assert httpx.post(f"{bare}/wrong/entity/currency/count", json={}).status_code == 404
assert httpx.post(f"{api}/currency/count", json={}).status_code == 404
assert httpx.get(f"{bare}/").status_code == 404

print("API verified")
```

## Troubleshooting

**`error: Distribution not found at: file:///.../logic` when running `uv sync`.** The API reaches Logic as a local path dependency and the directory it names does not exist beside `api`. Put the `logic` directory (with the `database` and `model` directories it needs) next to the `api` directory, then run `uv sync` again.

**`ModuleNotFoundError: No module named 'api'` (or `'logic'`).** The command ran in an interpreter outside the API environment. Run it from the API directory with `uv run`, after `uv sync` has installed the environment.

**`Address already in use` when starting.** Another process is using the port of `config.yaml`. Stop that process, or change `port` in `config.yaml` (and the port inside `url` and the `documentation` addresses with it) and start the API again.

**A request answers 404.** The path is outside the Base URL. Use the address `url` gives, including the key, then the Group segment, the Adapter segment and the Endpoint path; the key is the first path segment, and a path without it is not served.

**A request answers 500 with `ExecutionError` and `no such table`.** The default Instance has not been prepared, so its tables do not exist. Run `uv run python scripts/prepare.py` from the Database directory, then repeat the request.

**A request answers 422.** The request holds invalid input: an unknown Field, operator, direction or Instance name, a body the Entity refuses, or a path or body the framework cannot read. The Problem Details `type` names the error (`InvalidInputError` or `RequestValidationError`) and `detail` says where.
