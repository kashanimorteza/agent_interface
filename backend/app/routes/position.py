from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.position import PositionCreate, PositionRead
from app.services import position as service

router = APIRouter(prefix="/positions", tags=["positions"])


@router.get("", response_model=list[PositionRead])
def list_positions(db: Session = Depends(get_db)):
    return service.list_all(db)


@router.post("", response_model=PositionRead, status_code=status.HTTP_201_CREATED)
def create_position(data: PositionCreate, db: Session = Depends(get_db)):
    return service.create(db, data)


@router.get("/{id}", response_model=PositionRead)
def get_position(id: int, db: Session = Depends(get_db)):
    return service.get(db, id)


@router.put("/{id}", response_model=PositionRead)
def update_position(id: int, data: PositionCreate, db: Session = Depends(get_db)):
    return service.update(db, id, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_position(id: int, db: Session = Depends(get_db)):
    service.delete(db, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
