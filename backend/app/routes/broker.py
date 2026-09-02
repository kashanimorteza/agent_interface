from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.broker import BrokerCreate, BrokerRead
from app.services import broker as service

router = APIRouter(prefix="/brokers", tags=["brokers"])


@router.get("", response_model=list[BrokerRead])
def list_brokers(db: Session = Depends(get_db)):
    return service.list_all(db)


@router.post("", response_model=BrokerRead, status_code=status.HTTP_201_CREATED)
def create_broker(data: BrokerCreate, db: Session = Depends(get_db)):
    return service.create(db, data)


@router.get("/{id}", response_model=BrokerRead)
def get_broker(id: int, db: Session = Depends(get_db)):
    return service.get(db, id)


@router.put("/{id}", response_model=BrokerRead)
def update_broker(id: int, data: BrokerCreate, db: Session = Depends(get_db)):
    return service.update(db, id, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_broker(id: int, db: Session = Depends(get_db)):
    service.delete(db, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
