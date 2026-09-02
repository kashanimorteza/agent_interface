from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.broker import BrokerCreate, BrokerRead, BrokerUpdate
from app.services import broker as service

router = APIRouter(prefix="/brokers", tags=["brokers"])


@router.get("", response_model=list[BrokerRead])
def list_brokers(db: Session = Depends(get_db)):
    return service.list_brokers(db)


@router.post("", response_model=BrokerRead, status_code=status.HTTP_201_CREATED)
def create_broker(data: BrokerCreate, db: Session = Depends(get_db)):
    return service.create_broker(db, data)


@router.get("/{id}", response_model=BrokerRead)
def get_broker(id: int, db: Session = Depends(get_db)):
    obj = service.get_broker(db, id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Broker not found")
    return obj


@router.put("/{id}", response_model=BrokerRead)
def update_broker(id: int, data: BrokerUpdate, db: Session = Depends(get_db)):
    obj = service.update_broker(db, id, data)
    if obj is None:
        raise HTTPException(status_code=404, detail="Broker not found")
    return obj


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_broker(id: int, db: Session = Depends(get_db)):
    if not service.delete_broker(db, id):
        raise HTTPException(status_code=404, detail="Broker not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
