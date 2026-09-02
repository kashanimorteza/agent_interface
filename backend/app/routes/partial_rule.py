from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.partial_rule import PartialRuleCreate, PartialRuleRead
from app.services import partial_rule as service

router = APIRouter(prefix="/partial-rules", tags=["partial_rules"])


@router.get("", response_model=list[PartialRuleRead])
def list_partial_rules(db: Session = Depends(get_db)):
    return service.list_all(db)


@router.post("", response_model=PartialRuleRead, status_code=status.HTTP_201_CREATED)
def create_partial_rule(data: PartialRuleCreate, db: Session = Depends(get_db)):
    return service.create(db, data)


@router.get("/{id}", response_model=PartialRuleRead)
def get_partial_rule(id: int, db: Session = Depends(get_db)):
    return service.get(db, id)


@router.put("/{id}", response_model=PartialRuleRead)
def update_partial_rule(id: int, data: PartialRuleCreate, db: Session = Depends(get_db)):
    return service.update(db, id, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_partial_rule(id: int, db: Session = Depends(get_db)):
    service.delete(db, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
