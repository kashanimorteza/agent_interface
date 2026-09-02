from sqlalchemy.orm import Session

from app.errors import NotFoundError, ValidationError
from app.models.trailing_group import TrailingGroup
from app.schemas.trailing_group import TrailingGroupCreate


def list_all(db: Session) -> list[TrailingGroup]:
    return list(db.query(TrailingGroup).order_by(TrailingGroup.id).all())


def get(db: Session, id: int) -> TrailingGroup:
    row = db.get(TrailingGroup, id)
    if row is None:
        raise NotFoundError("Trailing group not found")
    return row


def create(db: Session, data: TrailingGroupCreate) -> TrailingGroup:
    row = TrailingGroup(**data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def update(db: Session, id: int, data: TrailingGroupCreate) -> TrailingGroup:
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
