# Database

The Database Component: the complete persistence boundary for the Trading Assistant. It maps every persistent `model` Domain Definition to physical SQLite storage and exposes one generic Database Interface — no consumer imports a per-Model adapter or writes SQL.

## Public surface

```python
from database import interface as db
```

- `db.create(instance)`, `db.get_by_id(ModelType, id)`, `db.list_(ModelType)`, `db.search(ModelType, **criteria)`, `db.update(instance)`, `db.delete(ModelType, id)` — one generic pipeline for every persistent Model, typed by whatever Model you pass.
- `db.set_active(ModelType, id, active=True|False)` — for any Model declaring `is_active`.
- `db.transaction()` — a context manager grouping related operations into one atomic commit-or-rollback unit; a standalone call above is its own atomic unit.
- `db.execute_command(name, **params)` — the capability-restricted, allow-listed route for operations standard CRUD can't express (currently: `increment_account_balance`).
- `database.adapter.instance_registry()` / `default_instance_key()` — the selectable Instance identities; no connections or secrets.
- `database.initial_data.import_initial_data()` — imports every Target-declared initial record, safe to re-run.
- `database.schema_check.is_up_to_date()` — startup drift check between the running structure and the recorded Migration history.

## Structure

```text
database/
  src/database/
    adapter.py        # Storage Adapter: Engine connections, Instance Registry
    mapping.py         # generic Model -> SQLAlchemy Table derivation
    credentials.py      # hash / encrypted at-rest treatment
    interface.py        # the generic Database Interface (CRUD, activation, Transaction, controlled command)
    initial_data.py      # Target-declared initial data import
    schema_check.py      # startup drift detection
  migrations/          # Alembic environment + the one recorded schema Migration
  tests/               # one test module per capability
```

## Setup

```bash
cd database
uv sync
uv run alembic upgrade head        # create the storage structure
uv run python -c "from database.initial_data import import_initial_data; import_initial_data()"
```

Requires Python 3.14+. The default Instance (`general`) stores its SQLite file at `database/data/trading_assistant_general.db` (untracked — see `.gitignore`).

## Migrations

```bash
uv run alembic upgrade head       # apply
uv run alembic downgrade base     # reverse (tested: removes exactly what upgrade created)
```

A new Migration is generated with `uv run alembic revision --autogenerate -m "<message>"` after `mapping.ALL_MODELS` changes, and reviewed before committing — autogenerate is a starting point, not a guarantee.

## Credentials

Every credential field is stored using the classification `model`'s `persistence_metadata()` publishes for it — `hash` (one-way, PBKDF2-HMAC-SHA256) or `encrypted` (reversible, Fernet/AES). Database never infers a treatment from a field name, and rejects an unclassified or unsupported one.

The encryption key is read from the `DATABASE_CREDENTIAL_KEY` environment variable. If unset, an ephemeral key is generated for that process — sufficient for local development and the test suite, but **a real deployment must set `DATABASE_CREDENTIAL_KEY` explicitly** (Platform's Runtime Binding, once Launch is implemented) or previously encrypted values become unrecoverable across restarts. No credential value or key ever appears in this repository.

`update()` never touches credential fields — an already-persisted value read back is already transformed, so re-applying treatment would corrupt it. Credential rotation is a distinct capability, not exposed by this generic operation.

## Verification

```bash
uv run pytest      # 30 tests: adapter, mapping, credentials, migrations (incl. reversal + drift), interface, initial data
uv run ruff check . && uv run ruff format --check .
uv run pyright
```

## Troubleshooting

- `IntegrityError` on create/update: a declared uniqueness constraint or foreign-key reference was violated — Database enforces exactly what `model` publishes, nothing more.
- `NotPersistentError`: the Model passed declares `persistent=False` and has no physical structure.
- `UnsupportedOperationError`: either `set_active` was called on a Model with no `is_active` field, or `execute_command` was called with a name outside the allow-list.
- Drift detected by `schema_check.is_up_to_date()`: the running structure was changed outside a Migration — never repair this by hand; add a new Migration.
