from sqlalchemy.orm import Session

from app.errors import NotFoundError, ValidationError
from app.models.partial_group import PartialGroup
from app.models.partial_rule import PartialRule
from app.schemas.partial_rule import PartialRuleCreate


def _check_references(db: Session, data: PartialRuleCreate) -> None:
    if db.get(PartialGroup, data.partial_group_id) is None:
        raise ValidationError("Partial group not found", field="partial_group_id")


def list_all(db: Session) -> list[PartialRule]:
    return list(db.query(PartialRule).order_by(PartialRule.id).all())


def get(db: Session, id: int) -> PartialRule:
    row = db.get(PartialRule, id)
    if row is None:
        raise NotFoundError("Partial rule not found")
    return row


def create(db: Session, data: PartialRuleCreate) -> PartialRule:
    _check_references(db, data)
    row = PartialRule(**data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def update(db: Session, id: int, data: PartialRuleCreate) -> PartialRule:
    row = get(db, id)
    _check_references(db, data)
    for field, value in data.model_dump().items():
        setattr(row, field, value)
    db.commit()
    db.refresh(row)
    return row


def delete(db: Session, id: int) -> None:
    row = get(db, id)
    db.delete(row)
    db.commit()
