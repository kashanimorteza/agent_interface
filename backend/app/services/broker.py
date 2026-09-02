from sqlalchemy.orm import Session

from app.errors import NotFoundError, ValidationError
from app.models.broker import Broker
from app.models.trading_platform import TradingPlatform
from app.schemas.broker import BrokerCreate


def _check_references(db: Session, data: BrokerCreate) -> None:
    if db.get(TradingPlatform, data.trading_platform_id) is None:
        raise ValidationError("Trading platform not found", field="trading_platform_id")


def list_all(db: Session) -> list[Broker]:
    return list(db.query(Broker).order_by(Broker.id).all())


def get(db: Session, id: int) -> Broker:
    row = db.get(Broker, id)
    if row is None:
        raise NotFoundError("Broker not found")
    return row


def create(db: Session, data: BrokerCreate) -> Broker:
    _check_references(db, data)
    row = Broker(**data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def update(db: Session, id: int, data: BrokerCreate) -> Broker:
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
