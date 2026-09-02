from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.partial_rule import PartialRuleCreate, PartialRuleRead, PartialRuleUpdate
from app.services import partial_rule as service

router = APIRouter(prefix="/partial-rules", tags=["partial-rules"])


@router.get("", response_model=list[PartialRuleRead])
def list_partial_rules(db: Session = Depends(get_db)):
    return service.list_partial_rules(db)


@router.post("", response_model=PartialRuleRead, status_code=status.HTTP_201_CREATED)
def create_partial_rule(data: PartialRuleCreate, db: Session = Depends(get_db)):
    return service.create_partial_rule(db, data)


@router.get("/{id}", response_model=PartialRuleRead)
def get_partial_rule(id: int, db: Session = Depends(get_db)):
    obj = service.get_partial_rule(db, id)
    if obj is None:
        raise HTTPException(status_code=404, detail="PartialRule not found")
    return obj


@router.put("/{id}", response_model=PartialRuleRead)
def update_partial_rule(id: int, data: PartialRuleUpdate, db: Session = Depends(get_db)):
    obj = service.update_partial_rule(db, id, data)
    if obj is None:
        raise HTTPException(status_code=404, detail="PartialRule not found")
    return obj


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_partial_rule(id: int, db: Session = Depends(get_db)):
    if not service.delete_partial_rule(db, id):
        raise HTTPException(status_code=404, detail="PartialRule not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
