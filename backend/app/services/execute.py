from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.execute import Execute
from app.schemas.execute import ExecuteCreate, ExecuteUpdate


def list_executes(db: Session) -> list[Execute]:
    return list(db.scalars(select(Execute).order_by(Execute.id)).all())


def get_execute(db: Session, id: int) -> Execute | None:
    return db.get(Execute, id)


def create_execute(db: Session, data: ExecuteCreate) -> Execute:
    obj = Execute(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_execute(db: Session, id: int, data: ExecuteUpdate) -> Execute | None:
    obj = db.get(Execute, id)
    if obj is None:
        return None
    for field, value in data.model_dump().items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete_execute(db: Session, id: int) -> bool:
    obj = db.get(Execute, id)
    if obj is None:
        return False
    db.delete(obj)
    db.commit()
    return True
