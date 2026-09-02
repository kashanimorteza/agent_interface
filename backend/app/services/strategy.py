from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.strategy import Strategy
from app.schemas.strategy import StrategyCreate, StrategyUpdate


def list_strategys(db: Session) -> list[Strategy]:
    return list(db.scalars(select(Strategy).order_by(Strategy.id)).all())


def get_strategy(db: Session, id: int) -> Strategy | None:
    return db.get(Strategy, id)


def create_strategy(db: Session, data: StrategyCreate) -> Strategy:
    obj = Strategy(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_strategy(db: Session, id: int, data: StrategyUpdate) -> Strategy | None:
    obj = db.get(Strategy, id)
    if obj is None:
        return None
    for field, value in data.model_dump().items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete_strategy(db: Session, id: int) -> bool:
    obj = db.get(Strategy, id)
    if obj is None:
        return False
    db.delete(obj)
    db.commit()
    return True
