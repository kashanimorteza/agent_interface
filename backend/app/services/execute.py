from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.execute import Execute
from app.schemas.execute import ExecuteCreate


def list_execute(db: Session) -> list[Execute]:
    return list(db.scalars(select(Execute).order_by(Execute.id)).all())


def create_execute(db: Session, data: ExecuteCreate) -> Execute:
    row = Execute(**data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def get_execute(db: Session, id: int) -> Execute | None:
    return db.get(Execute, id)


def replace_execute(db: Session, id: int, data: ExecuteCreate) -> Execute | None:
    row = db.get(Execute, id)
    if row is None:
        return None
    for field, value in data.model_dump().items():
        setattr(row, field, value)
    db.commit()
    db.refresh(row)
    return row


def delete_execute(db: Session, id: int) -> bool:
    row = db.get(Execute, id)
    if row is None:
        return False
    db.delete(row)
    db.commit()
    return True
