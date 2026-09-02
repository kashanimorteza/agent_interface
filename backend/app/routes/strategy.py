from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.strategy import StrategyCreate, StrategyRead
from app.services import strategy as service

router = APIRouter(prefix="/strategies", tags=["strategies"])


@router.get("", response_model=list[StrategyRead])
def list_strategies(db: Session = Depends(get_db)):
    return service.list_all(db)


@router.post("", response_model=StrategyRead, status_code=status.HTTP_201_CREATED)
def create_strategy(data: StrategyCreate, db: Session = Depends(get_db)):
    return service.create(db, data)


@router.get("/{id}", response_model=StrategyRead)
def get_strategy(id: int, db: Session = Depends(get_db)):
    return service.get(db, id)


@router.put("/{id}", response_model=StrategyRead)
def update_strategy(id: int, data: StrategyCreate, db: Session = Depends(get_db)):
    return service.update(db, id, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_strategy(id: int, db: Session = Depends(get_db)):
    service.delete(db, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
