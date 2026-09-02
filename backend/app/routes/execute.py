from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.execute import ExecuteCreate, ExecuteRead
from app.services import execute as service

router = APIRouter(prefix="/executes", tags=["executes"])


@router.get("", response_model=list[ExecuteRead])
def list_executes(db: Session = Depends(get_db)):
    return service.list_execute(db)


@router.post("", response_model=ExecuteRead, status_code=status.HTTP_201_CREATED)
def create_execute(data: ExecuteCreate, db: Session = Depends(get_db)):
    return service.create_execute(db, data)


@router.get("/{id}", response_model=ExecuteRead)
def read_execute(id: int, db: Session = Depends(get_db)):
    row = service.get_execute(db, id)
    if row is None:
        raise HTTPException(status_code=404, detail="Execute not found")
    return row


@router.put("/{id}", response_model=ExecuteRead)
def replace_execute(id: int, data: ExecuteCreate, db: Session = Depends(get_db)):
    row = service.replace_execute(db, id, data)
    if row is None:
        raise HTTPException(status_code=404, detail="Execute not found")
    return row


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_execute(id: int, db: Session = Depends(get_db)):
    if not service.delete_execute(db, id):
        raise HTTPException(status_code=404, detail="Execute not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
