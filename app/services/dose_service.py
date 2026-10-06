from datetime import datetime, timedelta
from typing import Dict, List
from uuid import UUID

from fastapi import HTTPException, status

from app.models.dose import Dose
from app.models.enums import DoseStatus
from app.repositories.dose_repository import DoseRepository
from app.repositories.medication_repository import MedicationRepository
from app.schemas.dose import DoseCreate


class DoseService:
    def __init__(
        self,
        dose_repository: DoseRepository,
        medication_repository: MedicationRepository,
    ) -> None:
        self.dose_repository = dose_repository
        self.medication_repository = medication_repository

    async def schedule_dose(self, dose_data: DoseCreate) -> Dose:
        medication = await self.medication_repository.get_by_id(
            dose_data.medication_id
        )
        if not medication:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Medication not found',
            )

        dose = Dose(
            medication_id=dose_data.medication_id,
            scheduled_at=dose_data.scheduled_at,
            status=DoseStatus.PENDING,
        )
        return await self.dose_repository.create(dose)

    async def get_timeline_grouped_by_status(self) -> Dict[str, List[Dose]]:
        doses = await self.dose_repository.list_all_ordered_by_scheduled_time()
        timeline: Dict[str, List[Dose]] = {
            DoseStatus.PENDING.value: [],
            DoseStatus.TAKEN.value: [],
            DoseStatus.SNOOZED.value: [],
            DoseStatus.SKIPPED.value: [],
        }

        for dose in doses:
            timeline[dose.status.value].append(dose)

        return timeline

    async def mark_dose_as_taken(
        self, dose_id: UUID, taken_at: datetime
    ) -> Dose:
        dose = await self.dose_repository.get_by_id_with_medication(dose_id)
        if not dose:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Dose not found',
            )

        dose.status = DoseStatus.TAKEN
        dose.taken_at = taken_at
        return await self.dose_repository.update(dose)

    async def snooze_dose(
        self, dose_id: UUID, delay_minutes: int = 15
    ) -> Dose:
        dose = await self.dose_repository.get_by_id_with_medication(dose_id)
        if not dose:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Dose not found',
            )

        dose.status = DoseStatus.SNOOZED
        dose.scheduled_at = datetime.utcnow() + timedelta(
            minutes=delay_minutes
        )
        return await self.dose_repository.update(dose)

    async def skip_dose(self, dose_id: UUID) -> Dose:
        dose = await self.dose_repository.get_by_id_with_medication(dose_id)
        if not dose:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Dose not found',
            )

        dose.status = DoseStatus.SKIPPED
        return await self.dose_repository.update(dose)
