import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.models.enums import DoseStatus
from app.schemas.medication import MedicationRead


class DoseBase(BaseModel):
    medication_id: uuid.UUID
    scheduled_at: datetime


class DoseCreate(DoseBase):
    pass


class DoseUpdate(BaseModel):
    taken_at: Optional[datetime] = None
    status: Optional[DoseStatus] = None
    telegram_message_id: Optional[int] = None


class DoseRead(DoseBase):
    id: uuid.UUID
    taken_at: Optional[datetime] = None
    status: DoseStatus
    telegram_message_id: Optional[int] = None
    created_at: datetime
    medication: Optional[MedicationRead] = None

    model_config = ConfigDict(from_attributes=True)
