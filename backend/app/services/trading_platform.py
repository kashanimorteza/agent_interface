from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.trading_platform import TradingPlatform
from app.schemas.trading_platform import TradingPlatformCreate


def list_trading_platform(db: Session) -> list[TradingPlatform]:
    return list(db.scalars(select(TradingPlatform).order_by(TradingPlatform.id)).all())


def create_trading_platform(db: Session, data: TradingPlatformCreate) -> TradingPlatform:
    row = TradingPlatform(**data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def get_trading_platform(db: Session, id: int) -> TradingPlatform | None:
    return db.get(TradingPlatform, id)


def replace_trading_platform(db: Session, id: int, data: TradingPlatformCreate) -> TradingPlatform | None:
    row = db.get(TradingPlatform, id)
    if row is None:
        return None
    for field, value in data.model_dump().items():
        setattr(row, field, value)
    db.commit()
    db.refresh(row)
    return row


def delete_trading_platform(db: Session, id: int) -> bool:
    row = db.get(TradingPlatform, id)
    if row is None:
        return False
    db.delete(row)
    db.commit()
    return True
