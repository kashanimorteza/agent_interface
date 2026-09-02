from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.trailing_group import TrailingGroup
from app.schemas.trailing_group import TrailingGroupCreate, TrailingGroupUpdate


def list_trailing_groups(db: Session) -> list[TrailingGroup]:
    return list(db.scalars(select(TrailingGroup).order_by(TrailingGroup.id)).all())


def get_trailing_group(db: Session, id: int) -> TrailingGroup | None:
    return db.get(TrailingGroup, id)


def create_trailing_group(db: Session, data: TrailingGroupCreate) -> TrailingGroup:
    obj = TrailingGroup(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_trailing_group(db: Session, id: int, data: TrailingGroupUpdate) -> TrailingGroup | None:
    obj = db.get(TrailingGroup, id)
    if obj is None:
        return None
    for field, value in data.model_dump().items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete_trailing_group(db: Session, id: int) -> bool:
    obj = db.get(TrailingGroup, id)
    if obj is None:
        return False
    db.delete(obj)
    db.commit()
    return True
