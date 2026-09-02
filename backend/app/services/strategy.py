from sqlalchemy.orm import Session

from app.errors import NotFoundError, ValidationError
from app.models.strategy import Strategy
from app.schemas.strategy import StrategyCreate


def list_all(db: Session) -> list[Strategy]:
    return list(db.query(Strategy).order_by(Strategy.id).all())


def get(db: Session, id: int) -> Strategy:
    row = db.get(Strategy, id)
    if row is None:
        raise NotFoundError("Strategy not found")
    return row


def create(db: Session, data: StrategyCreate) -> Strategy:
    row = Strategy(**data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def update(db: Session, id: int, data: StrategyCreate) -> Strategy:
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
