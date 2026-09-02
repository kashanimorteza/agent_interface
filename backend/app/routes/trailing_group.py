from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.trailing_group import TrailingGroupCreate, TrailingGroupRead
from app.services import trailing_group as service

router = APIRouter(prefix="/trailing-groups", tags=["trailing_groups"])


@router.get("", response_model=list[TrailingGroupRead])
def list_trailing_groups(db: Session = Depends(get_db)):
    return service.list_trailing_group(db)


@router.post("", response_model=TrailingGroupRead, status_code=status.HTTP_201_CREATED)
def create_trailing_group(data: TrailingGroupCreate, db: Session = Depends(get_db)):
    return service.create_trailing_group(db, data)


@router.get("/{id}", response_model=TrailingGroupRead)
def read_trailing_group(id: int, db: Session = Depends(get_db)):
    row = service.get_trailing_group(db, id)
    if row is None:
        raise HTTPException(status_code=404, detail="TrailingGroup not found")
    return row


@router.put("/{id}", response_model=TrailingGroupRead)
def replace_trailing_group(id: int, data: TrailingGroupCreate, db: Session = Depends(get_db)):
    row = service.replace_trailing_group(db, id, data)
    if row is None:
        raise HTTPException(status_code=404, detail="TrailingGroup not found")
    return row


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_trailing_group(id: int, db: Session = Depends(get_db)):
    if not service.delete_trailing_group(db, id):
        raise HTTPException(status_code=404, detail="TrailingGroup not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
