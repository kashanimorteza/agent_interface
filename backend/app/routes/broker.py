from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.broker import BrokerCreate, BrokerRead
from app.services import broker as service

router = APIRouter(prefix="/brokers", tags=["brokers"])


@router.get("", response_model=list[BrokerRead])
def list_brokers(db: Session = Depends(get_db)):
    return service.list_broker(db)


@router.post("", response_model=BrokerRead, status_code=status.HTTP_201_CREATED)
def create_broker(data: BrokerCreate, db: Session = Depends(get_db)):
    return service.create_broker(db, data)


@router.get("/{id}", response_model=BrokerRead)
def read_broker(id: int, db: Session = Depends(get_db)):
    row = service.get_broker(db, id)
    if row is None:
        raise HTTPException(status_code=404, detail="Broker not found")
    return row


@router.put("/{id}", response_model=BrokerRead)
def replace_broker(id: int, data: BrokerCreate, db: Session = Depends(get_db)):
    row = service.replace_broker(db, id, data)
    if row is None:
        raise HTTPException(status_code=404, detail="Broker not found")
    return row


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_broker(id: int, db: Session = Depends(get_db)):
    if not service.delete_broker(db, id):
        raise HTTPException(status_code=404, detail="Broker not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
