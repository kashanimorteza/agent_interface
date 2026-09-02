from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.trading_platform import TradingPlatformCreate, TradingPlatformRead, TradingPlatformUpdate
from app.services import trading_platform as service

router = APIRouter(prefix="/trading-platforms", tags=["trading-platforms"])


@router.get("", response_model=list[TradingPlatformRead])
def list_trading_platforms(db: Session = Depends(get_db)):
    return service.list_trading_platforms(db)


@router.post("", response_model=TradingPlatformRead, status_code=status.HTTP_201_CREATED)
def create_trading_platform(data: TradingPlatformCreate, db: Session = Depends(get_db)):
    return service.create_trading_platform(db, data)


@router.get("/{id}", response_model=TradingPlatformRead)
def get_trading_platform(id: int, db: Session = Depends(get_db)):
    obj = service.get_trading_platform(db, id)
    if obj is None:
        raise HTTPException(status_code=404, detail="TradingPlatform not found")
    return obj


@router.put("/{id}", response_model=TradingPlatformRead)
def update_trading_platform(id: int, data: TradingPlatformUpdate, db: Session = Depends(get_db)):
    obj = service.update_trading_platform(db, id, data)
    if obj is None:
        raise HTTPException(status_code=404, detail="TradingPlatform not found")
    return obj


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_trading_platform(id: int, db: Session = Depends(get_db)):
    if not service.delete_trading_platform(db, id):
        raise HTTPException(status_code=404, detail="TradingPlatform not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
