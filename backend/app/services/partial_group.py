from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.partial_group import PartialGroup
from app.schemas.partial_group import PartialGroupCreate


def list_partial_group(db: Session) -> list[PartialGroup]:
    return list(db.scalars(select(PartialGroup).order_by(PartialGroup.id)).all())


def create_partial_group(db: Session, data: PartialGroupCreate) -> PartialGroup:
    row = PartialGroup(**data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def get_partial_group(db: Session, id: int) -> PartialGroup | None:
    return db.get(PartialGroup, id)


def replace_partial_group(db: Session, id: int, data: PartialGroupCreate) -> PartialGroup | None:
    row = db.get(PartialGroup, id)
    if row is None:
        return None
    for field, value in data.model_dump().items():
        setattr(row, field, value)
    db.commit()
    db.refresh(row)
    return row


def delete_partial_group(db: Session, id: int) -> bool:
    row = db.get(PartialGroup, id)
    if row is None:
        return False
    db.delete(row)
    db.commit()
    return True
