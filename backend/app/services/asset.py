from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.asset import Asset
from app.schemas.asset import AssetCreate


def list_asset(db: Session) -> list[Asset]:
    return list(db.scalars(select(Asset).order_by(Asset.id)).all())


def create_asset(db: Session, data: AssetCreate) -> Asset:
    row = Asset(**data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def get_asset(db: Session, id: int) -> Asset | None:
    return db.get(Asset, id)


def replace_asset(db: Session, id: int, data: AssetCreate) -> Asset | None:
    row = db.get(Asset, id)
    if row is None:
        return None
    for field, value in data.model_dump().items():
        setattr(row, field, value)
    db.commit()
    db.refresh(row)
    return row


def delete_asset(db: Session, id: int) -> bool:
    row = db.get(Asset, id)
    if row is None:
        return False
    db.delete(row)
    db.commit()
    return True
