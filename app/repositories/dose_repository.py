from datetime import datetime
from typing import Optional, Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.dose import Dose
from app.models.enums import DoseStatus
from app.models.medication import Medication
from app.repositories.base_repository import BaseRepository


class DoseRepository(BaseRepository[Dose]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Dose, session)

    async def get_by_id_with_medication(self, id: UUID) -> Optional[Dose]:
        query = (
            select(Dose)
            .where(Dose.id == id)
            .options(selectinload(Dose.medication))
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def list_all_ordered_by_scheduled_time(self) -> Sequence[Dose]:
        query = (
            select(Dose)
            .order_by(Dose.scheduled_at.asc())
            .options(selectinload(Dose.medication))
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def list_pending_doses_until(
        self, cutoff_time: datetime
    ) -> Sequence[Dose]:
        query = (
            select(Dose)
            .where(
                Dose.scheduled_at <= cutoff_time,
                Dose.status == DoseStatus.PENDING,
            )
            .options(selectinload(Dose.medication))
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def list_pending_ready_for_dispatch(
        self, cutoff_time: datetime
    ) -> Sequence[Dose]:
        query = (
            select(Dose)
            .where(
                Dose.scheduled_at <= cutoff_time,
                Dose.status == DoseStatus.PENDING,
                Dose.telegram_message_id.is_(None),
            )
            .options(selectinload(Dose.medication))
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def list_pending_doses_for_nagging(
        self, cutoff_time: datetime, max_reminders: int = 3
    ) -> Sequence[Dose]:
        query = (
            select(Dose)
            .where(
                Dose.status == DoseStatus.PENDING,
                Dose.telegram_message_id.is_not(None),
                Dose.last_notified_at.is_not(None),
                Dose.last_notified_at <= cutoff_time,
                Dose.reminder_count < max_reminders,
            )
            .order_by(Dose.scheduled_at.asc())
            .options(selectinload(Dose.medication))
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_next_pending_dose_by_medication(
        self, medication_id: UUID, after_time: datetime
    ) -> Optional[Dose]:
        query = (
            select(Dose)
            .where(
                Dose.medication_id == medication_id,
                Dose.scheduled_at >= after_time,
                Dose.status == DoseStatus.PENDING,
            )
            .order_by(Dose.scheduled_at.asc())
            .options(selectinload(Dose.medication))
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def list_subsequent_pending_doses_in_group(
        self, rotation_group_id: UUID, after_time: datetime
    ) -> Sequence[Dose]:
        query = (
            select(Dose)
            .join(Medication, Dose.medication_id == Medication.id)
            .where(
                Medication.rotation_group_id == rotation_group_id,
                Dose.scheduled_at >= after_time,
                Dose.status == DoseStatus.PENDING,
            )
            .order_by(Dose.scheduled_at.asc())
            .options(selectinload(Dose.medication))
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def update(self, dose: Dose) -> Dose:
        await self.session.commit()
        await self.session.refresh(dose)
        return dose
