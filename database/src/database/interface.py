from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

from model.foundation import ModelBase
from pydantic import SecretStr
from sqlalchemy import select
from sqlalchemy.orm import Session

from .adapter import get_engine
from .convert import from_orm_row, to_orm_kwargs
from .foundation import StorageBase, credential_fields, protect_credential
from .mapping import MAPPINGS


class UnknownModelError(ValueError):
    pass


class NotFoundError(LookupError):
    pass


def _orm_class[ModelT: ModelBase](model_type: type[ModelT]) -> type[StorageBase]:
    try:
        return MAPPINGS[model_type]
    except KeyError:
        raise UnknownModelError(
            f"{model_type.__name__} has no registered storage mapping"
        ) from None


@contextmanager
def transaction(instance: str | None = None) -> Iterator[Session]:
    engine = get_engine(instance)
    with Session(engine) as session, session.begin():
        yield session


def create[ModelT: ModelBase](
    instance_obj: ModelT, *, session: Session | None = None, instance: str | None = None
) -> ModelT:
    orm_cls = _orm_class(type(instance_obj))
    row = orm_cls(**to_orm_kwargs(instance_obj))

    def _create(tx: Session) -> ModelT:
        tx.add(row)
        tx.flush()
        result = from_orm_row(type(instance_obj), row)
        return result  # type: ignore[return-value]

    if session is not None:
        return _create(session)
    with transaction(instance) as tx:
        return _create(tx)


def get_by_id[ModelT: ModelBase](
    model_type: type[ModelT],
    id_: int,
    *,
    session: Session | None = None,
    instance: str | None = None,
) -> ModelT | None:
    orm_cls = _orm_class(model_type)

    def _get(tx: Session) -> ModelT | None:
        row = tx.get(orm_cls, id_)
        return from_orm_row(model_type, row) if row is not None else None  # type: ignore[return-value]

    if session is not None:
        return _get(session)
    with transaction(instance) as tx:
        return _get(tx)


def list_[ModelT: ModelBase](
    model_type: type[ModelT],
    *,
    session: Session | None = None,
    instance: str | None = None,
    **criteria: Any,
) -> list[ModelT]:
    orm_cls = _orm_class(model_type)

    def _list(tx: Session) -> list[ModelT]:
        stmt = select(orm_cls)
        for field, value in criteria.items():
            stmt = stmt.where(getattr(orm_cls, field) == value)
        rows = tx.scalars(stmt).all()
        return [from_orm_row(model_type, row) for row in rows]  # type: ignore[misc]

    if session is not None:
        return _list(session)
    with transaction(instance) as tx:
        return _list(tx)


def update[ModelT: ModelBase](
    model_type: type[ModelT],
    id_: int,
    changes: dict[str, Any],
    *,
    session: Session | None = None,
    instance: str | None = None,
) -> ModelT:
    orm_cls = _orm_class(model_type)
    modes = credential_fields(model_type)

    def _update(tx: Session) -> ModelT:
        row = tx.get(orm_cls, id_)
        if row is None:
            raise NotFoundError(f"{model_type.__name__} {id_} does not exist")
        for field, value in changes.items():
            if field in modes and value is not None:
                plain = (
                    value.get_secret_value() if isinstance(value, SecretStr) else value
                )
                value = protect_credential(plain, modes[field])
            setattr(row, field, value)
        tx.flush()
        return from_orm_row(model_type, row)  # type: ignore[return-value]

    if session is not None:
        return _update(session)
    with transaction(instance) as tx:
        return _update(tx)


def delete[ModelT: ModelBase](
    model_type: type[ModelT],
    id_: int,
    *,
    session: Session | None = None,
    instance: str | None = None,
) -> None:
    orm_cls = _orm_class(model_type)

    def _delete(tx: Session) -> None:
        row = tx.get(orm_cls, id_)
        if row is None:
            raise NotFoundError(f"{model_type.__name__} {id_} does not exist")
        tx.delete(row)
        tx.flush()

    if session is not None:
        _delete(session)
        return
    with transaction(instance) as tx:
        _delete(tx)


def set_active[ModelT: ModelBase](
    model_type: type[ModelT],
    id_: int,
    active: bool,
    *,
    session: Session | None = None,
    instance: str | None = None,
) -> ModelT:
    if "is_active" not in model_type.model_fields:
        raise ValueError(
            f"{model_type.__name__} has no is_active field; activation is not applicable"
        )
    return update(
        model_type, id_, {"is_active": active}, session=session, instance=instance
    )
