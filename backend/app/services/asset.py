from sqlalchemy.orm import Session

from app.errors import NotFoundError, ValidationError
from app.models.asset import Asset
from app.schemas.asset import AssetCreate


def list_all(db: Session) -> list[Asset]:
    return list(db.query(Asset).order_by(Asset.id).all())


def get(db: Session, id: int) -> Asset:
    row = db.get(Asset, id)
    if row is None:
        raise NotFoundError("Asset not found")
    return row


def create(db: Session, data: AssetCreate) -> Asset:
    row = Asset(**data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def update(db: Session, id: int, data: AssetCreate) -> Asset:
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
