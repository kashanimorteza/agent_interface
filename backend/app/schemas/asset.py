from pydantic import BaseModel, ConfigDict


class AssetCreate(BaseModel):
    name: str
    status: str
    description: str | None = None


class AssetUpdate(BaseModel):
    name: str
    status: str
    description: str | None = None


class AssetRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    status: str
    description: str | None = None
