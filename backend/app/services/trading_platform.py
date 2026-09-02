from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.trading_platform import TradingPlatform
from app.schemas.trading_platform import TradingPlatformCreate, TradingPlatformUpdate


def list_trading_platforms(db: Session) -> list[TradingPlatform]:
    return list(db.scalars(select(TradingPlatform).order_by(TradingPlatform.id)).all())


def get_trading_platform(db: Session, id: int) -> TradingPlatform | None:
    return db.get(TradingPlatform, id)


def create_trading_platform(db: Session, data: TradingPlatformCreate) -> TradingPlatform:
    obj = TradingPlatform(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_trading_platform(db: Session, id: int, data: TradingPlatformUpdate) -> TradingPlatform | None:
    obj = db.get(TradingPlatform, id)
    if obj is None:
        return None
    for field, value in data.model_dump().items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete_trading_platform(db: Session, id: int) -> bool:
    obj = db.get(TradingPlatform, id)
    if obj is None:
        return False
    db.delete(obj)
    db.commit()
    return True
