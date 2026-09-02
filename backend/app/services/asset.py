from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.asset import Asset
from app.schemas.asset import AssetCreate, AssetUpdate


def list_assets(db: Session) -> list[Asset]:
    return list(db.scalars(select(Asset).order_by(Asset.id)).all())


def get_asset(db: Session, id: int) -> Asset | None:
    return db.get(Asset, id)


def create_asset(db: Session, data: AssetCreate) -> Asset:
    obj = Asset(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_asset(db: Session, id: int, data: AssetUpdate) -> Asset | None:
    obj = db.get(Asset, id)
    if obj is None:
        return None
    for field, value in data.model_dump().items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete_asset(db: Session, id: int) -> bool:
    obj = db.get(Asset, id)
    if obj is None:
        return False
    db.delete(obj)
    db.commit()
    return True
