# my_database.database_interface

The Database Interface layer — the only boundary published to consumers of
`my_database`. Shared setup (installation, configuration, migrations) is
described in the parent [database/README.md](../../../README.md).

## Purpose and boundaries

Exposes the generic Model operations and Instance discovery and selection, and
nothing else. It delegates every operation to Data Logic and never touches the
Engine, a connection, a table, or a migration itself.

## Public interface

Re-exported from the `my_database` root, which is where consumers import it:

- `InstanceRegistry` — `default`, `instances` (a tuple of `InstanceIdentity`), `get(key)`;
- `InstanceIdentity` — `key`, `name`, `purpose`, `engine`;
- `Database(instance=None)` — `create`, `read`, `list`, `update`, `delete`, `status`, `sql`, and the `instance` property with the selected identity.

The call forms and error types are documented in the parent README.

## Dependencies

`my_database.data_logic` (operations and mapping) and `my_database.storage_adapter`
(settings, Engine binding). Managed by the parent project; this package declares
none of its own.

## Configuration

None of its own. The Instance and its settings are resolved through the Storage
Adapter's settings boundary (`DATABASE__*` variables) described in the parent
README.

## Usage examples

```python
from my_database import Database, InstanceRegistry
from my_model import Asset

registry = InstanceRegistry()
db = Database(instance=registry.default)
print(db.instance.name, [a.symbol for a in db.list(Asset, order_by="symbol")])
```
