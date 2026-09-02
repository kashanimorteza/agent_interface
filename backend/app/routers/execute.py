from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.execute import ExecuteCreate, ExecuteRead, ExecuteUpdate
from app.services import execute as service

router = APIRouter(prefix="/executes", tags=["executes"])


@router.get("", response_model=list[ExecuteRead])
def list_executes(db: Session = Depends(get_db)):
    return service.list_executes(db)


@router.post("", response_model=ExecuteRead, status_code=status.HTTP_201_CREATED)
def create_execute(data: ExecuteCreate, db: Session = Depends(get_db)):
    return service.create_execute(db, data)


@router.get("/{id}", response_model=ExecuteRead)
def get_execute(id: int, db: Session = Depends(get_db)):
    obj = service.get_execute(db, id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Execute not found")
    return obj


@router.put("/{id}", response_model=ExecuteRead)
def update_execute(id: int, data: ExecuteUpdate, db: Session = Depends(get_db)):
    obj = service.update_execute(db, id, data)
    if obj is None:
        raise HTTPException(status_code=404, detail="Execute not found")
    return obj


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_execute(id: int, db: Session = Depends(get_db)):
    if not service.delete_execute(db, id):
        raise HTTPException(status_code=404, detail="Execute not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
