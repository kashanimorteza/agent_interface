from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.broker import Broker
from app.schemas.broker import BrokerCreate, BrokerUpdate


def list_brokers(db: Session) -> list[Broker]:
    return list(db.scalars(select(Broker).order_by(Broker.id)).all())


def get_broker(db: Session, id: int) -> Broker | None:
    return db.get(Broker, id)


def create_broker(db: Session, data: BrokerCreate) -> Broker:
    obj = Broker(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_broker(db: Session, id: int, data: BrokerUpdate) -> Broker | None:
    obj = db.get(Broker, id)
    if obj is None:
        return None
    for field, value in data.model_dump().items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete_broker(db: Session, id: int) -> bool:
    obj = db.get(Broker, id)
    if obj is None:
        return False
    db.delete(obj)
    db.commit()
    return True
