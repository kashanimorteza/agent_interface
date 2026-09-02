from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.strategy import StrategyCreate, StrategyRead, StrategyUpdate
from app.services import strategy as service

router = APIRouter(prefix="/strategies", tags=["strategies"])


@router.get("", response_model=list[StrategyRead])
def list_strategys(db: Session = Depends(get_db)):
    return service.list_strategys(db)


@router.post("", response_model=StrategyRead, status_code=status.HTTP_201_CREATED)
def create_strategy(data: StrategyCreate, db: Session = Depends(get_db)):
    return service.create_strategy(db, data)


@router.get("/{id}", response_model=StrategyRead)
def get_strategy(id: int, db: Session = Depends(get_db)):
    obj = service.get_strategy(db, id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return obj


@router.put("/{id}", response_model=StrategyRead)
def update_strategy(id: int, data: StrategyUpdate, db: Session = Depends(get_db)):
    obj = service.update_strategy(db, id, data)
    if obj is None:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return obj


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_strategy(id: int, db: Session = Depends(get_db)):
    if not service.delete_strategy(db, id):
        raise HTTPException(status_code=404, detail="Strategy not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
