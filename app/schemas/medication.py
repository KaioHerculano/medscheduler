import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.models.enums import MedicationCategory
from app.schemas.rotation_group import RotationGroupRead


class MedicationBase(BaseModel):
    name: str
    category: MedicationCategory
    min_interval_hours: int = 6
    is_as_needed: bool = False
    notes: Optional[str] = None
    rotation_group_id: Optional[uuid.UUID] = None


class MedicationCreate(MedicationBase):
    pass


class MedicationRead(MedicationBase):
    id: uuid.UUID
    rotation_group: Optional[RotationGroupRead] = None

    model_config = ConfigDict(from_attributes=True)
