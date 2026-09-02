from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.trailing_rule import TrailingRule
from app.schemas.trailing_rule import TrailingRuleCreate, TrailingRuleUpdate


def list_trailing_rules(db: Session) -> list[TrailingRule]:
    return list(db.scalars(select(TrailingRule).order_by(TrailingRule.id)).all())


def get_trailing_rule(db: Session, id: int) -> TrailingRule | None:
    return db.get(TrailingRule, id)


def create_trailing_rule(db: Session, data: TrailingRuleCreate) -> TrailingRule:
    obj = TrailingRule(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_trailing_rule(db: Session, id: int, data: TrailingRuleUpdate) -> TrailingRule | None:
    obj = db.get(TrailingRule, id)
    if obj is None:
        return None
    for field, value in data.model_dump().items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete_trailing_rule(db: Session, id: int) -> bool:
    obj = db.get(TrailingRule, id)
    if obj is None:
        return False
    db.delete(obj)
    db.commit()
    return True
