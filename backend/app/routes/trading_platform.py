from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.trading_platform import TradingPlatformCreate, TradingPlatformRead
from app.services import trading_platform as service

router = APIRouter(prefix="/trading-platforms", tags=["trading_platforms"])


@router.get("", response_model=list[TradingPlatformRead])
def list_trading_platforms(db: Session = Depends(get_db)):
    return service.list_all(db)


@router.post("", response_model=TradingPlatformRead, status_code=status.HTTP_201_CREATED)
def create_trading_platform(data: TradingPlatformCreate, db: Session = Depends(get_db)):
    return service.create(db, data)


@router.get("/{id}", response_model=TradingPlatformRead)
def get_trading_platform(id: int, db: Session = Depends(get_db)):
    return service.get(db, id)


@router.put("/{id}", response_model=TradingPlatformRead)
def update_trading_platform(id: int, data: TradingPlatformCreate, db: Session = Depends(get_db)):
    return service.update(db, id, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_trading_platform(id: int, db: Session = Depends(get_db)):
    service.delete(db, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
