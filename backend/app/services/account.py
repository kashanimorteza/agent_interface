from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.account import Account
from app.schemas.account import AccountCreate, AccountUpdate


def list_accounts(db: Session) -> list[Account]:
    return list(db.scalars(select(Account).order_by(Account.id)).all())


def get_account(db: Session, id: int) -> Account | None:
    return db.get(Account, id)


def create_account(db: Session, data: AccountCreate) -> Account:
    obj = Account(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_account(db: Session, id: int, data: AccountUpdate) -> Account | None:
    obj = db.get(Account, id)
    if obj is None:
        return None
    for field, value in data.model_dump().items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete_account(db: Session, id: int) -> bool:
    obj = db.get(Account, id)
    if obj is None:
        return False
    db.delete(obj)
    db.commit()
    return True
