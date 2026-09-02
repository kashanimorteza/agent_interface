from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.trailing_group import TrailingGroupCreate, TrailingGroupRead
from app.services import trailing_group as service

router = APIRouter(prefix="/trailing-groups", tags=["trailing_groups"])


@router.get("", response_model=list[TrailingGroupRead])
def list_trailing_groups(db: Session = Depends(get_db)):
    return service.list_all(db)


@router.post("", response_model=TrailingGroupRead, status_code=status.HTTP_201_CREATED)
def create_trailing_group(data: TrailingGroupCreate, db: Session = Depends(get_db)):
    return service.create(db, data)


@router.get("/{id}", response_model=TrailingGroupRead)
def get_trailing_group(id: int, db: Session = Depends(get_db)):
    return service.get(db, id)


@router.put("/{id}", response_model=TrailingGroupRead)
def update_trailing_group(id: int, data: TrailingGroupCreate, db: Session = Depends(get_db)):
    return service.update(db, id, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_trailing_group(id: int, db: Session = Depends(get_db)):
    service.delete(db, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
