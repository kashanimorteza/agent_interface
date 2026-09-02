from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.action import ActionCreate, ActionRead
from app.services import action as service

router = APIRouter(prefix="/actions", tags=["actions"])


@router.get("", response_model=list[ActionRead])
def list_actions(db: Session = Depends(get_db)):
    return service.list_action(db)


@router.post("", response_model=ActionRead, status_code=status.HTTP_201_CREATED)
def create_action(data: ActionCreate, db: Session = Depends(get_db)):
    return service.create_action(db, data)


@router.get("/{id}", response_model=ActionRead)
def read_action(id: int, db: Session = Depends(get_db)):
    row = service.get_action(db, id)
    if row is None:
        raise HTTPException(status_code=404, detail="Action not found")
    return row


@router.put("/{id}", response_model=ActionRead)
def replace_action(id: int, data: ActionCreate, db: Session = Depends(get_db)):
    row = service.replace_action(db, id, data)
    if row is None:
        raise HTTPException(status_code=404, detail="Action not found")
    return row


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_action(id: int, db: Session = Depends(get_db)):
    if not service.delete_action(db, id):
        raise HTTPException(status_code=404, detail="Action not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
