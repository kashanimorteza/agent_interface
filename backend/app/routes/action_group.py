from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.action_group import ActionGroupCreate, ActionGroupRead
from app.services import action_group as service

router = APIRouter(prefix="/action-groups", tags=["action_groups"])


@router.get("", response_model=list[ActionGroupRead])
def list_action_groups(db: Session = Depends(get_db)):
    return service.list_all(db)


@router.post("", response_model=ActionGroupRead, status_code=status.HTTP_201_CREATED)
def create_action_group(data: ActionGroupCreate, db: Session = Depends(get_db)):
    return service.create(db, data)


@router.get("/{id}", response_model=ActionGroupRead)
def get_action_group(id: int, db: Session = Depends(get_db)):
    return service.get(db, id)


@router.put("/{id}", response_model=ActionGroupRead)
def update_action_group(id: int, data: ActionGroupCreate, db: Session = Depends(get_db)):
    return service.update(db, id, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_action_group(id: int, db: Session = Depends(get_db)):
    service.delete(db, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
