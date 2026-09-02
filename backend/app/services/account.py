from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.account import Account
from app.schemas.account import AccountCreate


def list_account(db: Session) -> list[Account]:
    return list(db.scalars(select(Account).order_by(Account.id)).all())


def create_account(db: Session, data: AccountCreate) -> Account:
    row = Account(**data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def get_account(db: Session, id: int) -> Account | None:
    return db.get(Account, id)


def replace_account(db: Session, id: int, data: AccountCreate) -> Account | None:
    row = db.get(Account, id)
    if row is None:
        return None
    for field, value in data.model_dump().items():
        setattr(row, field, value)
    db.commit()
    db.refresh(row)
    return row


def delete_account(db: Session, id: int) -> bool:
    row = db.get(Account, id)
    if row is None:
        return False
    db.delete(row)
    db.commit()
    return True
