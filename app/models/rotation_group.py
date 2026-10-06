import uuid
from typing import TYPE_CHECKING, List

from sqlalchemy import Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.medication import Medication


class RotationGroup(Base):
    __tablename__ = "rotation_groups"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    spacing_hours: Mapped[int] = mapped_column(
        Integer,
        default=2,
        nullable=False,
    )

    medications: Mapped[List["Medication"]] = relationship(
        "Medication",
        back_populates="rotation_group",
    )
