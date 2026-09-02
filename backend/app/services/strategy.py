from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.strategy import Strategy
from app.schemas.strategy import StrategyCreate


def list_strategy(db: Session) -> list[Strategy]:
    return list(db.scalars(select(Strategy).order_by(Strategy.id)).all())


def create_strategy(db: Session, data: StrategyCreate) -> Strategy:
    row = Strategy(**data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def get_strategy(db: Session, id: int) -> Strategy | None:
    return db.get(Strategy, id)


def replace_strategy(db: Session, id: int, data: StrategyCreate) -> Strategy | None:
    row = db.get(Strategy, id)
    if row is None:
        return None
    for field, value in data.model_dump().items():
        setattr(row, field, value)
    db.commit()
    db.refresh(row)
    return row


def delete_strategy(db: Session, id: int) -> bool:
    row = db.get(Strategy, id)
    if row is None:
        return False
    db.delete(row)
    db.commit()
    return True
