from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.partial_rule import PartialRule
from app.schemas.partial_rule import PartialRuleCreate, PartialRuleUpdate


def list_partial_rules(db: Session) -> list[PartialRule]:
    return list(db.scalars(select(PartialRule).order_by(PartialRule.id)).all())


def get_partial_rule(db: Session, id: int) -> PartialRule | None:
    return db.get(PartialRule, id)


def create_partial_rule(db: Session, data: PartialRuleCreate) -> PartialRule:
    obj = PartialRule(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_partial_rule(db: Session, id: int, data: PartialRuleUpdate) -> PartialRule | None:
    obj = db.get(PartialRule, id)
    if obj is None:
        return None
    for field, value in data.model_dump().items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete_partial_rule(db: Session, id: int) -> bool:
    obj = db.get(PartialRule, id)
    if obj is None:
        return False
    db.delete(obj)
    db.commit()
    return True
