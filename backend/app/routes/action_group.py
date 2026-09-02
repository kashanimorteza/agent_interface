from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.action_group import ActionGroupCreate, ActionGroupRead
from app.services import action_group as service

router = APIRouter(prefix="/action-groups", tags=["action_groups"])


@router.get("", response_model=list[ActionGroupRead])
def list_action_groups(db: Session = Depends(get_db)):
    return service.list_action_group(db)


@router.post("", response_model=ActionGroupRead, status_code=status.HTTP_201_CREATED)
def create_action_group(data: ActionGroupCreate, db: Session = Depends(get_db)):
    return service.create_action_group(db, data)


@router.get("/{id}", response_model=ActionGroupRead)
def read_action_group(id: int, db: Session = Depends(get_db)):
    row = service.get_action_group(db, id)
    if row is None:
        raise HTTPException(status_code=404, detail="ActionGroup not found")
    return row


@router.put("/{id}", response_model=ActionGroupRead)
def replace_action_group(id: int, data: ActionGroupCreate, db: Session = Depends(get_db)):
    row = service.replace_action_group(db, id, data)
    if row is None:
        raise HTTPException(status_code=404, detail="ActionGroup not found")
    return row


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_action_group(id: int, db: Session = Depends(get_db)):
    if not service.delete_action_group(db, id):
        raise HTTPException(status_code=404, detail="ActionGroup not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
