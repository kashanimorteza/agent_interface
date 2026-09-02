from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.partial_group import PartialGroup
from app.schemas.partial_group import PartialGroupCreate, PartialGroupUpdate


def list_partial_groups(db: Session) -> list[PartialGroup]:
    return list(db.scalars(select(PartialGroup).order_by(PartialGroup.id)).all())


def get_partial_group(db: Session, id: int) -> PartialGroup | None:
    return db.get(PartialGroup, id)


def create_partial_group(db: Session, data: PartialGroupCreate) -> PartialGroup:
    obj = PartialGroup(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_partial_group(db: Session, id: int, data: PartialGroupUpdate) -> PartialGroup | None:
    obj = db.get(PartialGroup, id)
    if obj is None:
        return None
    for field, value in data.model_dump().items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete_partial_group(db: Session, id: int) -> bool:
    obj = db.get(PartialGroup, id)
    if obj is None:
        return False
    db.delete(obj)
    db.commit()
    return True
