from sqlalchemy.orm import Session

from app.errors import NotFoundError, ValidationError
from app.models.partial_group import PartialGroup
from app.schemas.partial_group import PartialGroupCreate


def list_all(db: Session) -> list[PartialGroup]:
    return list(db.query(PartialGroup).order_by(PartialGroup.id).all())


def get(db: Session, id: int) -> PartialGroup:
    row = db.get(PartialGroup, id)
    if row is None:
        raise NotFoundError("Partial group not found")
    return row


def create(db: Session, data: PartialGroupCreate) -> PartialGroup:
    row = PartialGroup(**data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def update(db: Session, id: int, data: PartialGroupCreate) -> PartialGroup:
    row = get(db, id)
    for field, value in data.model_dump().items():
        setattr(row, field, value)
    db.commit()
    db.refresh(row)
    return row


def delete(db: Session, id: int) -> None:
    row = get(db, id)
    db.delete(row)
    db.commit()
