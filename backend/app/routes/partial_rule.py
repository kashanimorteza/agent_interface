from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.partial_rule import PartialRuleCreate, PartialRuleRead
from app.services import partial_rule as service

router = APIRouter(prefix="/partial-rules", tags=["partial_rules"])


@router.get("", response_model=list[PartialRuleRead])
def list_partial_rules(db: Session = Depends(get_db)):
    return service.list_partial_rule(db)


@router.post("", response_model=PartialRuleRead, status_code=status.HTTP_201_CREATED)
def create_partial_rule(data: PartialRuleCreate, db: Session = Depends(get_db)):
    return service.create_partial_rule(db, data)


@router.get("/{id}", response_model=PartialRuleRead)
def read_partial_rule(id: int, db: Session = Depends(get_db)):
    row = service.get_partial_rule(db, id)
    if row is None:
        raise HTTPException(status_code=404, detail="PartialRule not found")
    return row


@router.put("/{id}", response_model=PartialRuleRead)
def replace_partial_rule(id: int, data: PartialRuleCreate, db: Session = Depends(get_db)):
    row = service.replace_partial_rule(db, id, data)
    if row is None:
        raise HTTPException(status_code=404, detail="PartialRule not found")
    return row


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_partial_rule(id: int, db: Session = Depends(get_db)):
    if not service.delete_partial_rule(db, id):
        raise HTTPException(status_code=404, detail="PartialRule not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
