from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.account import AccountCreate, AccountRead
from app.services import account as service

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("", response_model=list[AccountRead])
def list_accounts(db: Session = Depends(get_db)):
    return service.list_account(db)


@router.post("", response_model=AccountRead, status_code=status.HTTP_201_CREATED)
def create_account(data: AccountCreate, db: Session = Depends(get_db)):
    return service.create_account(db, data)


@router.get("/{id}", response_model=AccountRead)
def read_account(id: int, db: Session = Depends(get_db)):
    row = service.get_account(db, id)
    if row is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return row


@router.put("/{id}", response_model=AccountRead)
def replace_account(id: int, data: AccountCreate, db: Session = Depends(get_db)):
    row = service.replace_account(db, id, data)
    if row is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return row


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_account(id: int, db: Session = Depends(get_db)):
    if not service.delete_account(db, id):
        raise HTTPException(status_code=404, detail="Account not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
