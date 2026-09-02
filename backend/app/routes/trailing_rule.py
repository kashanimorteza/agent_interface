from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.trailing_rule import TrailingRuleCreate, TrailingRuleRead
from app.services import trailing_rule as service

router = APIRouter(prefix="/trailing-rules", tags=["trailing_rules"])


@router.get("", response_model=list[TrailingRuleRead])
def list_trailing_rules(db: Session = Depends(get_db)):
    return service.list_trailing_rule(db)


@router.post("", response_model=TrailingRuleRead, status_code=status.HTTP_201_CREATED)
def create_trailing_rule(data: TrailingRuleCreate, db: Session = Depends(get_db)):
    return service.create_trailing_rule(db, data)


@router.get("/{id}", response_model=TrailingRuleRead)
def read_trailing_rule(id: int, db: Session = Depends(get_db)):
    row = service.get_trailing_rule(db, id)
    if row is None:
        raise HTTPException(status_code=404, detail="TrailingRule not found")
    return row


@router.put("/{id}", response_model=TrailingRuleRead)
def replace_trailing_rule(id: int, data: TrailingRuleCreate, db: Session = Depends(get_db)):
    row = service.replace_trailing_rule(db, id, data)
    if row is None:
        raise HTTPException(status_code=404, detail="TrailingRule not found")
    return row


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_trailing_rule(id: int, db: Session = Depends(get_db)):
    if not service.delete_trailing_rule(db, id):
        raise HTTPException(status_code=404, detail="TrailingRule not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
