import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import MedicationCategory

if TYPE_CHECKING:
    from app.models.dose import Dose
    from app.models.rotation_group import RotationGroup


class Medication(Base):
    __tablename__ = 'medications'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    category: Mapped[MedicationCategory] = mapped_column(
        SQLEnum(MedicationCategory),
        nullable=False,
    )
    min_interval_hours: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=6,
    )
    is_as_needed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    notes: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    rotation_group_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('rotation_groups.id', ondelete='SET NULL'),
        nullable=True,
    )

    rotation_group: Mapped[Optional['RotationGroup']] = relationship(
        'RotationGroup',
        back_populates='medications',
        lazy='selectin',
    )
    doses: Mapped[List['Dose']] = relationship(
        'Dose',
        back_populates='medication',
        cascade='all, delete-orphan',
    )
