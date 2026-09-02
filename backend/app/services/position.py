from sqlalchemy.orm import Session

from app.errors import NotFoundError, ValidationError
from app.models.position import Position
from app.schemas.position import PositionCreate


def list_all(db: Session) -> list[Position]:
    return list(db.query(Position).order_by(Position.id).all())


def get(db: Session, id: int) -> Position:
    row = db.get(Position, id)
    if row is None:
        raise NotFoundError("Position not found")
    return row


def create(db: Session, data: PositionCreate) -> Position:
    row = Position(**data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def update(db: Session, id: int, data: PositionCreate) -> Position:
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
