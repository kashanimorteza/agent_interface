from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.partial_group import PartialGroupCreate, PartialGroupRead, PartialGroupUpdate
from app.services import partial_group as service

router = APIRouter(prefix="/partial-groups", tags=["partial-groups"])


@router.get("", response_model=list[PartialGroupRead])
def list_partial_groups(db: Session = Depends(get_db)):
    return service.list_partial_groups(db)


@router.post("", response_model=PartialGroupRead, status_code=status.HTTP_201_CREATED)
def create_partial_group(data: PartialGroupCreate, db: Session = Depends(get_db)):
    return service.create_partial_group(db, data)


@router.get("/{id}", response_model=PartialGroupRead)
def get_partial_group(id: int, db: Session = Depends(get_db)):
    obj = service.get_partial_group(db, id)
    if obj is None:
        raise HTTPException(status_code=404, detail="PartialGroup not found")
    return obj


@router.put("/{id}", response_model=PartialGroupRead)
def update_partial_group(id: int, data: PartialGroupUpdate, db: Session = Depends(get_db)):
    obj = service.update_partial_group(db, id, data)
    if obj is None:
        raise HTTPException(status_code=404, detail="PartialGroup not found")
    return obj


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_partial_group(id: int, db: Session = Depends(get_db)):
    if not service.delete_partial_group(db, id):
        raise HTTPException(status_code=404, detail="PartialGroup not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
