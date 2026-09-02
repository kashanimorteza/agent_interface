from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.partial_group import PartialGroupCreate, PartialGroupRead
from app.services import partial_group as service

router = APIRouter(prefix="/partial-groups", tags=["partial_groups"])


@router.get("", response_model=list[PartialGroupRead])
def list_partial_groups(db: Session = Depends(get_db)):
    return service.list_all(db)


@router.post("", response_model=PartialGroupRead, status_code=status.HTTP_201_CREATED)
def create_partial_group(data: PartialGroupCreate, db: Session = Depends(get_db)):
    return service.create(db, data)


@router.get("/{id}", response_model=PartialGroupRead)
def get_partial_group(id: int, db: Session = Depends(get_db)):
    return service.get(db, id)


@router.put("/{id}", response_model=PartialGroupRead)
def update_partial_group(id: int, data: PartialGroupCreate, db: Session = Depends(get_db)):
    return service.update(db, id, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_partial_group(id: int, db: Session = Depends(get_db)):
    service.delete(db, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
