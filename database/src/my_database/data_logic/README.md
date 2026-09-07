# my_database.data_logic

The Data Logic and Mapping layer of `my_database`. Shared setup is described in
the parent [database/README.md](../../../README.md).

## Purpose and boundaries

Implements the one Model-driven operation pipeline used for every persistent
Model and resolves how the shared Models are persisted: the table derived from
each Model class combined with the persistence facts Database owns (table name,
uniqueness, composite uniqueness, relationships, credential modes), the
credential at-rest transformations, and the idempotent application of initial
data. It talks to the Engine only through the Storage Adapter and contains no
application behaviour.

## Public interface

Available to the Database Interface layer and to the migration tooling only;
consumers of `my_database` never import it.

- `Operations(storage, key)` — `create`, `read`, `list`, `update`, `delete`, `status`, `sql`;
- `mapped(Model)` / `TABLES` / `metadata` — the resolved mapping of a Model (its `Table`, fields, credential modes);
- `credentials` — `hash_credential`, `verify_hashed`, `encrypt_credential`, `decrypt_credential`, `transform`, `generate_credential`;
- `seeding` — `Seed`, `apply`, `remove`, `requires_key`, `GENERATE`.

## Dependencies

`my_model` (the Model classes), SQLAlchemy (Core statements and types),
`cryptography` (reversible encryption), and `my_database.storage_adapter`.
Managed by the parent project.

## Configuration

None of its own. The credential-encryption key is supplied by the caller as a
provider resolved through the Storage Adapter's settings boundary.

## Usage examples

Inside the package (for instance from a migration):

```python
from my_database.data_logic import mapped
from my_model import Broker

table = mapped(Broker).table
print(table.name, [c.name for c in table.columns], [k.name for k in table.constraints])
```
