from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.action import Action
from app.schemas.action import ActionCreate, ActionUpdate


def list_actions(db: Session) -> list[Action]:
    return list(db.scalars(select(Action).order_by(Action.id)).all())


def get_action(db: Session, id: int) -> Action | None:
    return db.get(Action, id)


def create_action(db: Session, data: ActionCreate) -> Action:
    obj = Action(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_action(db: Session, id: int, data: ActionUpdate) -> Action | None:
    obj = db.get(Action, id)
    if obj is None:
        return None
    for field, value in data.model_dump().items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete_action(db: Session, id: int) -> bool:
    obj = db.get(Action, id)
    if obj is None:
        return False
    db.delete(obj)
    db.commit()
    return True
