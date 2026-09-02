from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.broker import Broker
from app.schemas.broker import BrokerCreate


def list_broker(db: Session) -> list[Broker]:
    return list(db.scalars(select(Broker).order_by(Broker.id)).all())


def create_broker(db: Session, data: BrokerCreate) -> Broker:
    row = Broker(**data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def get_broker(db: Session, id: int) -> Broker | None:
    return db.get(Broker, id)


def replace_broker(db: Session, id: int, data: BrokerCreate) -> Broker | None:
    row = db.get(Broker, id)
    if row is None:
        return None
    for field, value in data.model_dump().items():
        setattr(row, field, value)
    db.commit()
    db.refresh(row)
    return row


def delete_broker(db: Session, id: int) -> bool:
    row = db.get(Broker, id)
    if row is None:
        return False
    db.delete(row)
    db.commit()
    return True
