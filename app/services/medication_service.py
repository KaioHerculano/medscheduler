from typing import Sequence
from uuid import UUID
from fastapi import HTTPException, status
from app.models.medication import Medication
from app.models.rotation_group import RotationGroup
from app.repositories.medication_repository import MedicationRepository
from app.repositories.rotation_group_repository import RotationGroupRepository
from app.schemas.medication import MedicationCreate
from app.schemas.rotation_group import RotationGroupCreate


class MedicationService:
    def __init__(
        self,
        medication_repository: MedicationRepository,
        rotation_group_repository: RotationGroupRepository,
    ) -> None:
        self.medication_repository = medication_repository
        self.rotation_group_repository = rotation_group_repository

    async def list_medications(self) -> Sequence[Medication]:
        return await self.medication_repository.list_all_with_rotation_group()

    async def get_medication_by_id(self, medication_id: UUID) -> Medication:
        medication = await self.medication_repository.get_by_id_with_rotation_group(medication_id)
        if not medication:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Medication not found",
            )
        return medication

    async def create_medication(self, medication_data: MedicationCreate) -> Medication:
        if medication_data.rotation_group_id:
            group = await self.rotation_group_repository.get_by_id(medication_data.rotation_group_id)
            if not group:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Rotation group not found",
                )

        medication = Medication(**medication_data.model_dump())
        return await self.medication_repository.create(medication)

    async def list_rotation_groups(self) -> Sequence[RotationGroup]:
        return await self.rotation_group_repository.list_all()

    async def create_rotation_group(self, group_data: RotationGroupCreate) -> RotationGroup:
        group = RotationGroup(**group_data.model_dump())
        return await self.rotation_group_repository.create(group)
