import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base
from app.models.enums import DoseStatus

if TYPE_CHECKING:
    from app.models.medication import Medication


class Dose(Base):
    __tablename__ = "doses"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    medication_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("medications.id", ondelete="CASCADE"),
        nullable=False,
    )
    scheduled_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    taken_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    status: Mapped[DoseStatus] = mapped_column(
        SQLEnum(DoseStatus),
        default=DoseStatus.PENDING,
        nullable=False,
    )
    telegram_message_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    medication: Mapped["Medication"] = relationship(
        "Medication",
        back_populates="doses",
        lazy="selectin",
    )
