from sqlalchemy.orm import Session

from app.errors import NotFoundError, ValidationError
from app.models.trailing_group import TrailingGroup
from app.models.trailing_rule import TrailingRule
from app.schemas.trailing_rule import TrailingRuleCreate


def _check_references(db: Session, data: TrailingRuleCreate) -> None:
    if db.get(TrailingGroup, data.trailing_group_id) is None:
        raise ValidationError("Trailing group not found", field="trailing_group_id")


def list_all(db: Session) -> list[TrailingRule]:
    return list(db.query(TrailingRule).order_by(TrailingRule.id).all())


def get(db: Session, id: int) -> TrailingRule:
    row = db.get(TrailingRule, id)
    if row is None:
        raise NotFoundError("Trailing rule not found")
    return row


def create(db: Session, data: TrailingRuleCreate) -> TrailingRule:
    _check_references(db, data)
    row = TrailingRule(**data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def update(db: Session, id: int, data: TrailingRuleCreate) -> TrailingRule:
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
