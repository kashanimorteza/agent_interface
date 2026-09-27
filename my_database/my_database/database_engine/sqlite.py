"""SQLite Engine: performs every published Database Operation with SQLModel/SQLAlchemy over a SQLite file."""

from pathlib import Path
from typing import Any, Dict, Optional, Sequence, Type, TypeVar

from sqlalchemy import func, text
from sqlmodel import Session, SQLModel, create_engine, select

T = TypeVar("T", bound=SQLModel)

_engine_cache: Dict[str, Any] = {}

_AGGREGATES = {"sum": func.sum, "min": func.min, "max": func.max}


def _engine(instance: Dict[str, Any]):
    db_path = Path(instance["path"])
    db_path.parent.mkdir(parents=True, exist_ok=True)
    url = f"sqlite:///{db_path}"
    if url not in _engine_cache:
        _engine_cache[url] = create_engine(url, connect_args={"check_same_thread": False})
    return _engine_cache[url]


def _apply_filters(statement, entity_class, filters: Optional[Dict[str, Any]]):
    if filters:
        for field, value in filters.items():
            statement = statement.where(getattr(entity_class, field) == value)
    return statement


def create_all(instance: Dict[str, Any], metadata) -> None:
    metadata.create_all(_engine(instance))


def add(instance: Dict[str, Any], entity: T) -> T:
    with Session(_engine(instance)) as session:
        session.add(entity)
        session.commit()
        session.refresh(entity)
        session.expunge(entity)
        return entity


def update(instance: Dict[str, Any], entity: T) -> T:
    with Session(_engine(instance)) as session:
        merged = session.merge(entity)
        session.commit()
        session.refresh(merged)
        session.expunge(merged)
        return merged


def get_by_id(instance: Dict[str, Any], entity_class: Type[T], record_id: Any) -> Optional[T]:
    with Session(_engine(instance)) as session:
        record = session.get(entity_class, record_id)
        if record is None:
            return None
        session.expunge(record)
        return record


def list_records(
    instance: Dict[str, Any],
    entity_class: Type[T],
    filters: Optional[Dict[str, Any]] = None,
    order_by: Optional[str] = None,
) -> Sequence[T]:
    with Session(_engine(instance)) as session:
        statement = _apply_filters(select(entity_class), entity_class, filters)
        if order_by:
            statement = statement.order_by(getattr(entity_class, order_by))
        records = list(session.exec(statement))
        for record in records:
            session.expunge(record)
        return records


def delete(instance: Dict[str, Any], entity_class: Type[T], record_id: Any) -> Dict[str, bool]:
    with Session(_engine(instance)) as session:
        record = session.get(entity_class, record_id)
        if record is None:
            return {"deleted": False}
        session.delete(record)
        session.commit()
        return {"deleted": True}


def set_active(instance: Dict[str, Any], entity_class: Type[T], record_id: Any, active: bool) -> Optional[T]:
    with Session(_engine(instance)) as session:
        record = session.get(entity_class, record_id)
        if record is None:
            return None
        record.is_active = active
        session.add(record)
        session.commit()
        session.refresh(record)
        session.expunge(record)
        return record


def count(instance: Dict[str, Any], entity_class: Type[SQLModel], filters: Optional[Dict[str, Any]] = None) -> int:
    with Session(_engine(instance)) as session:
        statement = _apply_filters(select(func.count()).select_from(entity_class), entity_class, filters)
        return session.exec(statement).one()


def aggregate(
    instance: Dict[str, Any],
    entity_class: Type[SQLModel],
    kind: str,
    field: str,
    filters: Optional[Dict[str, Any]] = None,
):
    with Session(_engine(instance)) as session:
        column = getattr(entity_class, field)
        statement = _apply_filters(select(_AGGREGATES[kind](column)), entity_class, filters)
        return session.exec(statement).one()


def truncate(instance: Dict[str, Any], entity_class: Type[SQLModel]) -> None:
    with Session(_engine(instance)) as session:
        session.execute(entity_class.__table__.delete())
        session.commit()


def execute_command(instance: Dict[str, Any], command: str, parameters: Optional[Dict[str, Any]] = None):
    with Session(_engine(instance)) as session:
        result = session.execute(text(command), parameters or {})
        session.commit()
        try:
            return result.fetchall()
        except Exception:
            return None
