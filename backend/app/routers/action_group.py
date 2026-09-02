from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.action_group import ActionGroupCreate, ActionGroupRead, ActionGroupUpdate
from app.services import action_group as service

router = APIRouter(prefix="/action-groups", tags=["action-groups"])


@router.get("", response_model=list[ActionGroupRead])
def list_action_groups(db: Session = Depends(get_db)):
    return service.list_action_groups(db)


@router.post("", response_model=ActionGroupRead, status_code=status.HTTP_201_CREATED)
def create_action_group(data: ActionGroupCreate, db: Session = Depends(get_db)):
    return service.create_action_group(db, data)


@router.get("/{id}", response_model=ActionGroupRead)
def get_action_group(id: int, db: Session = Depends(get_db)):
    obj = service.get_action_group(db, id)
    if obj is None:
        raise HTTPException(status_code=404, detail="ActionGroup not found")
    return obj


@router.put("/{id}", response_model=ActionGroupRead)
def update_action_group(id: int, data: ActionGroupUpdate, db: Session = Depends(get_db)):
    obj = service.update_action_group(db, id, data)
    if obj is None:
        raise HTTPException(status_code=404, detail="ActionGroup not found")
    return obj


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_action_group(id: int, db: Session = Depends(get_db)):
    if not service.delete_action_group(db, id):
        raise HTTPException(status_code=404, detail="ActionGroup not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
