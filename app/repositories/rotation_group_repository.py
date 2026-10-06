from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.rotation_group import RotationGroup
from app.repositories.base_repository import BaseRepository


class RotationGroupRepository(BaseRepository[RotationGroup]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(RotationGroup, session)

    async def get_by_name(self, name: str) -> Optional[RotationGroup]:
        query = select(RotationGroup).where(RotationGroup.name == name)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
