from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.trailing_rule import TrailingRule
from app.schemas.trailing_rule import TrailingRuleCreate


def list_trailing_rule(db: Session) -> list[TrailingRule]:
    return list(db.scalars(select(TrailingRule).order_by(TrailingRule.id)).all())


def create_trailing_rule(db: Session, data: TrailingRuleCreate) -> TrailingRule:
    row = TrailingRule(**data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def get_trailing_rule(db: Session, id: int) -> TrailingRule | None:
    return db.get(TrailingRule, id)


def replace_trailing_rule(db: Session, id: int, data: TrailingRuleCreate) -> TrailingRule | None:
    row = db.get(TrailingRule, id)
    if row is None:
        return None
    for field, value in data.model_dump().items():
        setattr(row, field, value)
    db.commit()
    db.refresh(row)
    return row


def delete_trailing_rule(db: Session, id: int) -> bool:
    row = db.get(TrailingRule, id)
    if row is None:
        return False
    db.delete(row)
    db.commit()
    return True
