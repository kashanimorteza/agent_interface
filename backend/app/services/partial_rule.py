from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.partial_rule import PartialRule
from app.schemas.partial_rule import PartialRuleCreate


def list_partial_rule(db: Session) -> list[PartialRule]:
    return list(db.scalars(select(PartialRule).order_by(PartialRule.id)).all())


def create_partial_rule(db: Session, data: PartialRuleCreate) -> PartialRule:
    row = PartialRule(**data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def get_partial_rule(db: Session, id: int) -> PartialRule | None:
    return db.get(PartialRule, id)


def replace_partial_rule(db: Session, id: int, data: PartialRuleCreate) -> PartialRule | None:
    row = db.get(PartialRule, id)
    if row is None:
        return None
    for field, value in data.model_dump().items():
        setattr(row, field, value)
    db.commit()
    db.refresh(row)
    return row


def delete_partial_rule(db: Session, id: int) -> bool:
    row = db.get(PartialRule, id)
    if row is None:
        return False
    db.delete(row)
    db.commit()
    return True
