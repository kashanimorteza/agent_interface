from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.asset import AssetCreate, AssetRead
from app.services import asset as service

router = APIRouter(prefix="/assets", tags=["assets"])


@router.get("", response_model=list[AssetRead])
def list_assets(db: Session = Depends(get_db)):
    return service.list_asset(db)


@router.post("", response_model=AssetRead, status_code=status.HTTP_201_CREATED)
def create_asset(data: AssetCreate, db: Session = Depends(get_db)):
    return service.create_asset(db, data)


@router.get("/{id}", response_model=AssetRead)
def read_asset(id: int, db: Session = Depends(get_db)):
    row = service.get_asset(db, id)
    if row is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    return row


@router.put("/{id}", response_model=AssetRead)
def replace_asset(id: int, data: AssetCreate, db: Session = Depends(get_db)):
    row = service.replace_asset(db, id, data)
    if row is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    return row


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_asset(id: int, db: Session = Depends(get_db)):
    if not service.delete_asset(db, id):
        raise HTTPException(status_code=404, detail="Asset not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
