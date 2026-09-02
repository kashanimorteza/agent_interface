from sqlalchemy.orm import Session

from app.errors import NotFoundError, ValidationError
from app.models.action_group import ActionGroup
from app.schemas.action_group import ActionGroupCreate


def list_all(db: Session) -> list[ActionGroup]:
    return list(db.query(ActionGroup).order_by(ActionGroup.id).all())


def get(db: Session, id: int) -> ActionGroup:
    row = db.get(ActionGroup, id)
    if row is None:
        raise NotFoundError("Action group not found")
    return row


def create(db: Session, data: ActionGroupCreate) -> ActionGroup:
    row = ActionGroup(**data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def update(db: Session, id: int, data: ActionGroupCreate) -> ActionGroup:
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
