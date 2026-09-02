from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.action_group import ActionGroup
from app.schemas.action_group import ActionGroupCreate, ActionGroupUpdate


def list_action_groups(db: Session) -> list[ActionGroup]:
    return list(db.scalars(select(ActionGroup).order_by(ActionGroup.id)).all())


def get_action_group(db: Session, id: int) -> ActionGroup | None:
    return db.get(ActionGroup, id)


def create_action_group(db: Session, data: ActionGroupCreate) -> ActionGroup:
    obj = ActionGroup(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_action_group(db: Session, id: int, data: ActionGroupUpdate) -> ActionGroup | None:
    obj = db.get(ActionGroup, id)
    if obj is None:
        return None
    for field, value in data.model_dump().items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete_action_group(db: Session, id: int) -> bool:
    obj = db.get(ActionGroup, id)
    if obj is None:
        return False
    db.delete(obj)
    db.commit()
    return True
