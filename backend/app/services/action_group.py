from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.action_group import ActionGroup
from app.schemas.action_group import ActionGroupCreate


def list_action_group(db: Session) -> list[ActionGroup]:
    return list(db.scalars(select(ActionGroup).order_by(ActionGroup.id)).all())


def create_action_group(db: Session, data: ActionGroupCreate) -> ActionGroup:
    row = ActionGroup(**data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def get_action_group(db: Session, id: int) -> ActionGroup | None:
    return db.get(ActionGroup, id)


def replace_action_group(db: Session, id: int, data: ActionGroupCreate) -> ActionGroup | None:
    row = db.get(ActionGroup, id)
    if row is None:
        return None
    for field, value in data.model_dump().items():
        setattr(row, field, value)
    db.commit()
    db.refresh(row)
    return row


def delete_action_group(db: Session, id: int) -> bool:
    row = db.get(ActionGroup, id)
    if row is None:
        return False
    db.delete(row)
    db.commit()
    return True
