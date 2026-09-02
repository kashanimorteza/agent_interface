from collections.abc import Generator

from fastapi import HTTPException, Query
from sqlalchemy.orm import Session

from app import config
from app.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_api_key(key: str | None = Query(default=None)) -> None:
    if key is None or config.API_KEY is None or key != config.API_KEY:
        raise HTTPException(status_code=401, detail="API key is missing or invalid")
