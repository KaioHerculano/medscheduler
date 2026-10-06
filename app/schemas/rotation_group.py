import uuid
from pydantic import BaseModel, ConfigDict


class RotationGroupBase(BaseModel):
    name: str
    spacing_hours: int = 2


class RotationGroupCreate(RotationGroupBase):
    pass


class RotationGroupRead(RotationGroupBase):
    id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)
