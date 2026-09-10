from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator, Literal

import sqlalchemy as sa
from my_model import DomainModel

from . import _credentials as creds
from ._engine import engine_for
from ._schema import TABLES

_DDL_KEYWORDS = ("create ", "alter ", "drop ", "truncate ")


class Database:
    def __init__(self, instance: str | None = None) -> None:
        self._instance = instance

    def _table(self, model_cls: type[DomainModel]) -> sa.Table:
        if model_cls not in TABLES:
            raise TypeError(f"{model_cls.__name__} is not a persistent Model known to Database.")
        return TABLES[model_cls]

    def _to_storage(self, model_cls: type[DomainModel], data: dict) -> dict:
        row = dict(data)
        for field in model_cls.credential_fields:
            if row.get(field) is not None:
                mode = model_cls.credential_storage.get(field, "plaintext")
                if mode == "hash":
                    row[field] = creds.hash_value(row[field])
                elif mode == "encrypted":
                    row[field] = creds.encrypt_value(row[field])
        return row

    def _from_storage(self, model_cls: type[DomainModel], row: dict) -> DomainModel:
        data = dict(row)
        for field in model_cls.credential_fields:
            if data.get(field) is not None:
                data[field] = creds.REDACTED
        return model_cls(**data)

    def _connection(self, conn):
        if conn is not None:
            return conn, False
        return engine_for(self._instance).begin(), True

    def create(self, model_cls: type[DomainModel], data: dict, *, conn=None) -> DomainModel:
        table = self._table(model_cls)
        payload = self._to_storage(model_cls, data)
        payload.pop("id", None)

        def _do(c):
            result = c.execute(sa.insert(table).values(**payload))
            new_id = result.inserted_primary_key[0]
            row = c.execute(sa.select(table).where(table.c.id == new_id)).mappings().one()
            return self._from_storage(model_cls, dict(row))

        if conn is not None:
            return _do(conn)
        with engine_for(self._instance).begin() as c:
            return _do(c)

    def get(self, model_cls: type[DomainModel], id_: int, *, conn=None) -> DomainModel | None:
        table = self._table(model_cls)

        def _do(c):
            row = c.execute(sa.select(table).where(table.c.id == id_)).mappings().first()
            return self._from_storage(model_cls, dict(row)) if row else None

        if conn is not None:
            return _do(conn)
        with engine_for(self._instance).begin() as c:
            return _do(c)

    def list(self, model_cls: type[DomainModel], *, where: dict | None = None, conn=None) -> list[DomainModel]:
        table = self._table(model_cls)
        stmt = sa.select(table)
        for key, value in (where or {}).items():
            stmt = stmt.where(table.c[key] == value)

        def _do(c):
            rows = c.execute(stmt).mappings().all()
            return [self._from_storage(model_cls, dict(row)) for row in rows]

        if conn is not None:
            return _do(conn)
        with engine_for(self._instance).begin() as c:
            return _do(c)

    def update(self, model_cls: type[DomainModel], id_: int, data: dict, *, conn=None) -> DomainModel:
        table = self._table(model_cls)
        payload = self._to_storage(model_cls, data)
        payload.pop("id", None)

        def _do(c):
            c.execute(sa.update(table).where(table.c.id == id_).values(**payload))
            row = c.execute(sa.select(table).where(table.c.id == id_)).mappings().first()
            if row is None:
                raise LookupError(f"{model_cls.__name__} {id_} not found")
            return self._from_storage(model_cls, dict(row))

        if conn is not None:
            return _do(conn)
        with engine_for(self._instance).begin() as c:
            return _do(c)

    def delete(self, model_cls: type[DomainModel], id_: int, *, conn=None) -> bool:
        table = self._table(model_cls)

        def _do(c):
            result = c.execute(sa.delete(table).where(table.c.id == id_))
            return result.rowcount > 0

        if conn is not None:
            return _do(conn)
        with engine_for(self._instance).begin() as c:
            return _do(c)

    def set_status(
        self, model_cls: type[DomainModel], id_: int, action: Literal["enable", "disable"], *, conn=None
    ) -> DomainModel:
        if "status" not in model_cls.model_fields:
            raise TypeError(f"{model_cls.__name__} does not declare a status field.")
        if action not in ("enable", "disable"):
            raise ValueError("status action must be 'enable' or 'disable'")
        return self.update(model_cls, id_, {"status": action == "enable"}, conn=conn)

    def execute_sql(
        self,
        model_cls: type[DomainModel],
        sql: str,
        params: dict | None = None,
        *,
        engine_dialect: str = "sqlite",
        conn=None,
    ) -> list[dict]:
        table = self._table(model_cls)
        lowered = sql.strip().lower()
        if lowered.startswith(_DDL_KEYWORDS) or any(f" {kw}" in f" {lowered}" for kw in _DDL_KEYWORDS):
            raise ValueError("Controlled SQL may not perform structural changes; use Migration for those.")
        if any(field in lowered for field in model_cls.credential_fields):
            raise ValueError("Controlled SQL may not read or write a credential field.")
        if engine_dialect != "sqlite":
            raise ValueError("Only the sqlite dialect is currently supported.")

        statement = sa.text(sql)

        def _do(c):
            result = c.execute(statement, params or {})
            returned = [dict(r) for r in result.mappings().all()] if result.returns_rows else []
            current_rows = c.execute(sa.select(table)).mappings().all()
            for row in current_rows:
                model_cls(**dict(row))
            return returned

        if conn is not None:
            return _do(conn)
        with engine_for(self._instance).begin() as c:
            return _do(c)

    @contextmanager
    def transaction(self) -> Iterator["BoundDatabase"]:
        with engine_for(self._instance).begin() as conn:
            yield BoundDatabase(self, conn)


class BoundDatabase:
    def __init__(self, db: Database, conn) -> None:
        self._db = db
        self._conn = conn

    def create(self, model_cls, data):
        return self._db.create(model_cls, data, conn=self._conn)

    def get(self, model_cls, id_):
        return self._db.get(model_cls, id_, conn=self._conn)

    def list(self, model_cls, *, where=None):
        return self._db.list(model_cls, where=where, conn=self._conn)

    def update(self, model_cls, id_, data):
        return self._db.update(model_cls, id_, data, conn=self._conn)

    def delete(self, model_cls, id_):
        return self._db.delete(model_cls, id_, conn=self._conn)

    def set_status(self, model_cls, id_, action):
        return self._db.set_status(model_cls, id_, action, conn=self._conn)

    def execute_sql(self, model_cls, sql, params=None, *, engine_dialect="sqlite"):
        return self._db.execute_sql(model_cls, sql, params, engine_dialect=engine_dialect, conn=self._conn)
