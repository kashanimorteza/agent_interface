from pydantic import BaseModel, ConfigDict


class AssetBase(BaseModel):
    name: str
    status: str
    description: str | None = None


class AssetCreate(AssetBase):
    pass


class AssetRead(AssetBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
