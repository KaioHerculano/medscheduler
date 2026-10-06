from typing import Optional, Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.medication import Medication
from app.repositories.base_repository import BaseRepository


class MedicationRepository(BaseRepository[Medication]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Medication, session)

    async def get_by_id_with_rotation_group(self, id: UUID) -> Optional[Medication]:
        query = (
            select(Medication)
            .where(Medication.id == id)
            .options(selectinload(Medication.rotation_group))
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def list_all_with_rotation_group(self) -> Sequence[Medication]:
        query = select(Medication).options(selectinload(Medication.rotation_group))
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_name(self, name: str) -> Optional[Medication]:
        query = select(Medication).where(Medication.name == name)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
