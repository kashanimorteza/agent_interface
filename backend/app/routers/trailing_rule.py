from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.trailing_rule import TrailingRuleCreate, TrailingRuleRead, TrailingRuleUpdate
from app.services import trailing_rule as service

router = APIRouter(prefix="/trailing-rules", tags=["trailing-rules"])


@router.get("", response_model=list[TrailingRuleRead])
def list_trailing_rules(db: Session = Depends(get_db)):
    return service.list_trailing_rules(db)


@router.post("", response_model=TrailingRuleRead, status_code=status.HTTP_201_CREATED)
def create_trailing_rule(data: TrailingRuleCreate, db: Session = Depends(get_db)):
    return service.create_trailing_rule(db, data)


@router.get("/{id}", response_model=TrailingRuleRead)
def get_trailing_rule(id: int, db: Session = Depends(get_db)):
    obj = service.get_trailing_rule(db, id)
    if obj is None:
        raise HTTPException(status_code=404, detail="TrailingRule not found")
    return obj


@router.put("/{id}", response_model=TrailingRuleRead)
def update_trailing_rule(id: int, data: TrailingRuleUpdate, db: Session = Depends(get_db)):
    obj = service.update_trailing_rule(db, id, data)
    if obj is None:
        raise HTTPException(status_code=404, detail="TrailingRule not found")
    return obj


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_trailing_rule(id: int, db: Session = Depends(get_db)):
    if not service.delete_trailing_rule(db, id):
        raise HTTPException(status_code=404, detail="TrailingRule not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
