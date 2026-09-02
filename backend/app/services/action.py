from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.action import Action
from app.schemas.action import ActionCreate


def list_action(db: Session) -> list[Action]:
    return list(db.scalars(select(Action).order_by(Action.id)).all())


def create_action(db: Session, data: ActionCreate) -> Action:
    row = Action(**data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def get_action(db: Session, id: int) -> Action | None:
    return db.get(Action, id)


def replace_action(db: Session, id: int, data: ActionCreate) -> Action | None:
    row = db.get(Action, id)
    if row is None:
        return None
    for field, value in data.model_dump().items():
        setattr(row, field, value)
    db.commit()
    db.refresh(row)
    return row


def delete_action(db: Session, id: int) -> bool:
    row = db.get(Action, id)
    if row is None:
        return False
    db.delete(row)
    db.commit()
    return True
