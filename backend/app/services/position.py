from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.position import Position
from app.schemas.position import PositionCreate


def list_position(db: Session) -> list[Position]:
    return list(db.scalars(select(Position).order_by(Position.id)).all())


def create_position(db: Session, data: PositionCreate) -> Position:
    row = Position(**data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def get_position(db: Session, id: int) -> Position | None:
    return db.get(Position, id)


def replace_position(db: Session, id: int, data: PositionCreate) -> Position | None:
    row = db.get(Position, id)
    if row is None:
        return None
    for field, value in data.model_dump().items():
        setattr(row, field, value)
    db.commit()
    db.refresh(row)
    return row


def delete_position(db: Session, id: int) -> bool:
    row = db.get(Position, id)
    if row is None:
        return False
    db.delete(row)
    db.commit()
    return True
