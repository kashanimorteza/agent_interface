from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.trailing_group import TrailingGroupCreate, TrailingGroupRead, TrailingGroupUpdate
from app.services import trailing_group as service

router = APIRouter(prefix="/trailing-groups", tags=["trailing-groups"])


@router.get("", response_model=list[TrailingGroupRead])
def list_trailing_groups(db: Session = Depends(get_db)):
    return service.list_trailing_groups(db)


@router.post("", response_model=TrailingGroupRead, status_code=status.HTTP_201_CREATED)
def create_trailing_group(data: TrailingGroupCreate, db: Session = Depends(get_db)):
    return service.create_trailing_group(db, data)


@router.get("/{id}", response_model=TrailingGroupRead)
def get_trailing_group(id: int, db: Session = Depends(get_db)):
    obj = service.get_trailing_group(db, id)
    if obj is None:
        raise HTTPException(status_code=404, detail="TrailingGroup not found")
    return obj


@router.put("/{id}", response_model=TrailingGroupRead)
def update_trailing_group(id: int, data: TrailingGroupUpdate, db: Session = Depends(get_db)):
    obj = service.update_trailing_group(db, id, data)
    if obj is None:
        raise HTTPException(status_code=404, detail="TrailingGroup not found")
    return obj


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_trailing_group(id: int, db: Session = Depends(get_db)):
    if not service.delete_trailing_group(db, id):
        raise HTTPException(status_code=404, detail="TrailingGroup not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
