from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.position import PositionCreate, PositionRead, PositionUpdate
from app.services import position as service

router = APIRouter(prefix="/positions", tags=["positions"])


@router.get("", response_model=list[PositionRead])
def list_positions(db: Session = Depends(get_db)):
    return service.list_positions(db)


@router.post("", response_model=PositionRead, status_code=status.HTTP_201_CREATED)
def create_position(data: PositionCreate, db: Session = Depends(get_db)):
    return service.create_position(db, data)


@router.get("/{id}", response_model=PositionRead)
def get_position(id: int, db: Session = Depends(get_db)):
    obj = service.get_position(db, id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Position not found")
    return obj


@router.put("/{id}", response_model=PositionRead)
def update_position(id: int, data: PositionUpdate, db: Session = Depends(get_db)):
    obj = service.update_position(db, id, data)
    if obj is None:
        raise HTTPException(status_code=404, detail="Position not found")
    return obj


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_position(id: int, db: Session = Depends(get_db)):
    if not service.delete_position(db, id):
        raise HTTPException(status_code=404, detail="Position not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
