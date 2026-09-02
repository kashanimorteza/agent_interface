from sqlalchemy.orm import Session

from app.errors import NotFoundError, ValidationError
from app.models.trading_platform import TradingPlatform
from app.schemas.trading_platform import TradingPlatformCreate


def list_all(db: Session) -> list[TradingPlatform]:
    return list(db.query(TradingPlatform).order_by(TradingPlatform.id).all())


def get(db: Session, id: int) -> TradingPlatform:
    row = db.get(TradingPlatform, id)
    if row is None:
        raise NotFoundError("Trading platform not found")
    return row


def create(db: Session, data: TradingPlatformCreate) -> TradingPlatform:
    row = TradingPlatform(**data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def update(db: Session, id: int, data: TradingPlatformCreate) -> TradingPlatform:
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
