from datetime import datetime
from typing import Optional, Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.dose import Dose
from app.models.enums import DoseStatus
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

    async def update(self, dose: Dose) -> Dose:
        await self.session.commit()
        await self.session.refresh(dose)
        return dose
