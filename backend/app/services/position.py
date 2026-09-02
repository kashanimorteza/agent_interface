from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.position import Position
from app.schemas.position import PositionCreate, PositionUpdate


def list_positions(db: Session) -> list[Position]:
    return list(db.scalars(select(Position).order_by(Position.id)).all())


def get_position(db: Session, id: int) -> Position | None:
    return db.get(Position, id)


def create_position(db: Session, data: PositionCreate) -> Position:
    obj = Position(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_position(db: Session, id: int, data: PositionUpdate) -> Position | None:
    obj = db.get(Position, id)
    if obj is None:
        return None
    for field, value in data.model_dump().items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete_position(db: Session, id: int) -> bool:
    obj = db.get(Position, id)
    if obj is None:
        return False
    db.delete(obj)
    db.commit()
    return True
