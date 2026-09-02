from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.account import AccountCreate, AccountRead, AccountUpdate
from app.services import account as service

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("", response_model=list[AccountRead])
def list_accounts(db: Session = Depends(get_db)):
    return service.list_accounts(db)


@router.post("", response_model=AccountRead, status_code=status.HTTP_201_CREATED)
def create_account(data: AccountCreate, db: Session = Depends(get_db)):
    return service.create_account(db, data)


@router.get("/{id}", response_model=AccountRead)
def get_account(id: int, db: Session = Depends(get_db)):
    obj = service.get_account(db, id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return obj


@router.put("/{id}", response_model=AccountRead)
def update_account(id: int, data: AccountUpdate, db: Session = Depends(get_db)):
    obj = service.update_account(db, id, data)
    if obj is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return obj


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(id: int, db: Session = Depends(get_db)):
    if not service.delete_account(db, id):
        raise HTTPException(status_code=404, detail="Account not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
