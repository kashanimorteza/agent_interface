from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.strategy import StrategyCreate, StrategyRead
from app.services import strategy as service

router = APIRouter(prefix="/strategies", tags=["strategies"])


@router.get("", response_model=list[StrategyRead])
def list_strategies(db: Session = Depends(get_db)):
    return service.list_strategy(db)


@router.post("", response_model=StrategyRead, status_code=status.HTTP_201_CREATED)
def create_strategy(data: StrategyCreate, db: Session = Depends(get_db)):
    return service.create_strategy(db, data)


@router.get("/{id}", response_model=StrategyRead)
def read_strategy(id: int, db: Session = Depends(get_db)):
    row = service.get_strategy(db, id)
    if row is None:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return row


@router.put("/{id}", response_model=StrategyRead)
def replace_strategy(id: int, data: StrategyCreate, db: Session = Depends(get_db)):
    row = service.replace_strategy(db, id, data)
    if row is None:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return row


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_strategy(id: int, db: Session = Depends(get_db)):
    if not service.delete_strategy(db, id):
        raise HTTPException(status_code=404, detail="Strategy not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
