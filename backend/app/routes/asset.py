from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.asset import AssetCreate, AssetRead
from app.services import asset as service

router = APIRouter(prefix="/assets", tags=["assets"])


@router.get("", response_model=list[AssetRead])
def list_assets(db: Session = Depends(get_db)):
    return service.list_all(db)


@router.post("", response_model=AssetRead, status_code=status.HTTP_201_CREATED)
def create_asset(data: AssetCreate, db: Session = Depends(get_db)):
    return service.create(db, data)


@router.get("/{id}", response_model=AssetRead)
def get_asset(id: int, db: Session = Depends(get_db)):
    return service.get(db, id)


@router.put("/{id}", response_model=AssetRead)
def update_asset(id: int, data: AssetCreate, db: Session = Depends(get_db)):
    return service.update(db, id, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_asset(id: int, db: Session = Depends(get_db)):
    service.delete(db, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
