from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.partial_group import PartialGroupCreate, PartialGroupRead
from app.services import partial_group as service

router = APIRouter(prefix="/partial-groups", tags=["partial_groups"])


@router.get("", response_model=list[PartialGroupRead])
def list_partial_groups(db: Session = Depends(get_db)):
    return service.list_partial_group(db)


@router.post("", response_model=PartialGroupRead, status_code=status.HTTP_201_CREATED)
def create_partial_group(data: PartialGroupCreate, db: Session = Depends(get_db)):
    return service.create_partial_group(db, data)


@router.get("/{id}", response_model=PartialGroupRead)
def read_partial_group(id: int, db: Session = Depends(get_db)):
    row = service.get_partial_group(db, id)
    if row is None:
        raise HTTPException(status_code=404, detail="PartialGroup not found")
    return row


@router.put("/{id}", response_model=PartialGroupRead)
def replace_partial_group(id: int, data: PartialGroupCreate, db: Session = Depends(get_db)):
    row = service.replace_partial_group(db, id, data)
    if row is None:
        raise HTTPException(status_code=404, detail="PartialGroup not found")
    return row


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_partial_group(id: int, db: Session = Depends(get_db)):
    if not service.delete_partial_group(db, id):
        raise HTTPException(status_code=404, detail="PartialGroup not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
