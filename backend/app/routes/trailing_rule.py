from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.trailing_rule import TrailingRuleCreate, TrailingRuleRead
from app.services import trailing_rule as service

router = APIRouter(prefix="/trailing-rules", tags=["trailing_rules"])


@router.get("", response_model=list[TrailingRuleRead])
def list_trailing_rules(db: Session = Depends(get_db)):
    return service.list_all(db)


@router.post("", response_model=TrailingRuleRead, status_code=status.HTTP_201_CREATED)
def create_trailing_rule(data: TrailingRuleCreate, db: Session = Depends(get_db)):
    return service.create(db, data)


@router.get("/{id}", response_model=TrailingRuleRead)
def get_trailing_rule(id: int, db: Session = Depends(get_db)):
    return service.get(db, id)


@router.put("/{id}", response_model=TrailingRuleRead)
def update_trailing_rule(id: int, data: TrailingRuleCreate, db: Session = Depends(get_db)):
    return service.update(db, id, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_trailing_rule(id: int, db: Session = Depends(get_db)):
    service.delete(db, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
