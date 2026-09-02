from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.trailing_group import TrailingGroup
from app.schemas.trailing_group import TrailingGroupCreate


def list_trailing_group(db: Session) -> list[TrailingGroup]:
    return list(db.scalars(select(TrailingGroup).order_by(TrailingGroup.id)).all())


def create_trailing_group(db: Session, data: TrailingGroupCreate) -> TrailingGroup:
    row = TrailingGroup(**data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def get_trailing_group(db: Session, id: int) -> TrailingGroup | None:
    return db.get(TrailingGroup, id)


def replace_trailing_group(db: Session, id: int, data: TrailingGroupCreate) -> TrailingGroup | None:
    row = db.get(TrailingGroup, id)
    if row is None:
        return None
    for field, value in data.model_dump().items():
        setattr(row, field, value)
    db.commit()
    db.refresh(row)
    return row


def delete_trailing_group(db: Session, id: int) -> bool:
    row = db.get(TrailingGroup, id)
    if row is None:
        return False
    db.delete(row)
    db.commit()
    return True
