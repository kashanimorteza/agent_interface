from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.position import PositionCreate, PositionRead
from app.services import position as service

router = APIRouter(prefix="/positions", tags=["positions"])


@router.get("", response_model=list[PositionRead])
def list_positions(db: Session = Depends(get_db)):
    return service.list_position(db)


@router.post("", response_model=PositionRead, status_code=status.HTTP_201_CREATED)
def create_position(data: PositionCreate, db: Session = Depends(get_db)):
    return service.create_position(db, data)


@router.get("/{id}", response_model=PositionRead)
def read_position(id: int, db: Session = Depends(get_db)):
    row = service.get_position(db, id)
    if row is None:
        raise HTTPException(status_code=404, detail="Position not found")
    return row


@router.put("/{id}", response_model=PositionRead)
def replace_position(id: int, data: PositionCreate, db: Session = Depends(get_db)):
    row = service.replace_position(db, id, data)
    if row is None:
        raise HTTPException(status_code=404, detail="Position not found")
    return row


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_position(id: int, db: Session = Depends(get_db)):
    if not service.delete_position(db, id):
        raise HTTPException(status_code=404, detail="Position not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
