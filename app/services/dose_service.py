from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional
from uuid import UUID

from fastapi import HTTPException, status

from app.models.dose import Dose
from app.models.enums import DoseStatus
from app.repositories.dose_repository import DoseRepository
from app.repositories.medication_repository import MedicationRepository
from app.schemas.dose import DoseCreate
from app.services.scheduler_engine import SchedulerEngine


class DoseService:
    def __init__(
        self,
        dose_repository: DoseRepository,
        medication_repository: MedicationRepository,
        scheduler_engine: Optional[SchedulerEngine] = None,
    ) -> None:
        self.dose_repository = dose_repository
        self.medication_repository = medication_repository
        self.scheduler_engine = scheduler_engine or SchedulerEngine()

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
        updated_dose = await self.dose_repository.update(dose)

        if self.scheduler_engine.is_delayed_confirmation(
            dose.scheduled_at, taken_at
        ):
            await self._reschedule_after_delay(dose, taken_at)

        return updated_dose

    async def _reschedule_after_delay(
        self, dose: Dose, taken_at: datetime
    ) -> None:
        medication = dose.medication
        if not medication:
            return

        next_dose = (
            await self.dose_repository.get_next_pending_dose_by_medication(
                medication.id, dose.scheduled_at
            )
        )
        if next_dose:
            recalculated_time = (
                self.scheduler_engine.calculate_rescheduled_time(
                    taken_at, medication.min_interval_hours
                )
            )
            next_sched = SchedulerEngine._to_utc(next_dose.scheduled_at)
            if recalculated_time > next_sched:
                next_dose.scheduled_at = recalculated_time
                await self.dose_repository.update(next_dose)

        if medication.rotation_group_id:
            spacing_hours = (
                medication.rotation_group.spacing_hours
                if medication.rotation_group
                else 2
            )
            group_doses = await (
                self.dose_repository.list_subsequent_pending_doses_in_group(
                    medication.rotation_group_id, taken_at
                )
            )
            current_reference = taken_at
            for group_dose in group_doses:
                adjusted_time = (
                    self.scheduler_engine.calculate_group_spacing_adjustment(
                        current_reference,
                        group_dose.scheduled_at,
                        spacing_hours,
                    )
                )
                current_sched = SchedulerEngine._to_utc(
                    group_dose.scheduled_at
                )
                if adjusted_time != current_sched:
                    group_dose.scheduled_at = adjusted_time
                    await self.dose_repository.update(group_dose)
                current_reference = group_dose.scheduled_at

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
        dose.scheduled_at = datetime.now(timezone.utc) + timedelta(
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
