from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.dose import Dose
from app.models.enums import DoseStatus, MedicationCategory
from app.models.medication import Medication
from app.models.rotation_group import RotationGroup
from app.repositories.dose_repository import DoseRepository
from app.repositories.medication_repository import MedicationRepository
from app.services.dose_service import DoseService
from app.services.scheduler_engine import SchedulerEngine


@pytest.mark.asyncio
async def test_on_time_confirmation_does_not_reschedule(
    db_session: AsyncSession,
) -> None:
    dose_repo = DoseRepository(db_session)
    med_repo = MedicationRepository(db_session)
    dose_service = DoseService(
        dose_repository=dose_repo, medication_repository=med_repo
    )

    med = Medication(
        name='Dipirona',
        category=MedicationCategory.ANALGESIC,
        min_interval_hours=6,
    )
    db_session.add(med)
    await db_session.flush()

    scheduled_time = datetime(2026, 10, 7, 8, 0, tzinfo=timezone.utc)
    dose_1 = Dose(
        medication_id=med.id,
        scheduled_at=scheduled_time,
        status=DoseStatus.PENDING,
    )
    dose_2 = Dose(
        medication_id=med.id,
        scheduled_at=scheduled_time + timedelta(hours=6),
        status=DoseStatus.PENDING,
    )
    db_session.add_all([dose_1, dose_2])
    await db_session.commit()

    taken_time = scheduled_time + timedelta(minutes=20)
    updated_dose_1 = await dose_service.mark_dose_as_taken(
        dose_1.id, taken_time
    )

    assert updated_dose_1.status == DoseStatus.TAKEN
    assert updated_dose_1.taken_at is not None
    assert SchedulerEngine._to_utc(updated_dose_1.taken_at) == taken_time

    refreshed_dose_2 = await dose_repo.get_by_id(dose_2.id)
    assert refreshed_dose_2 is not None
    assert SchedulerEngine._to_utc(
        refreshed_dose_2.scheduled_at
    ) == scheduled_time + timedelta(hours=6)


@pytest.mark.asyncio
async def test_delayed_confirmation_cascades_rescheduling(
    db_session: AsyncSession,
) -> None:
    dose_repo = DoseRepository(db_session)
    med_repo = MedicationRepository(db_session)
    dose_service = DoseService(
        dose_repository=dose_repo, medication_repository=med_repo
    )

    group = RotationGroup(name='Analgesia Rotativa', spacing_hours=2)
    db_session.add(group)
    await db_session.flush()

    dipirona = Medication(
        name='Dipirona',
        category=MedicationCategory.ANALGESIC,
        min_interval_hours=6,
        rotation_group_id=group.id,
    )
    toragesic = Medication(
        name='Toragesic',
        category=MedicationCategory.ANALGESIC,
        min_interval_hours=6,
        rotation_group_id=group.id,
    )
    db_session.add_all([dipirona, toragesic])
    await db_session.flush()

    start_time = datetime(2026, 10, 7, 8, 0, tzinfo=timezone.utc)
    dose_dipirona_1 = Dose(
        medication_id=dipirona.id,
        scheduled_at=start_time,
        status=DoseStatus.PENDING,
    )
    dose_toragesic_1 = Dose(
        medication_id=toragesic.id,
        scheduled_at=start_time + timedelta(hours=3),
        status=DoseStatus.PENDING,
    )
    dose_dipirona_2 = Dose(
        medication_id=dipirona.id,
        scheduled_at=start_time + timedelta(hours=6),
        status=DoseStatus.PENDING,
    )
    db_session.add_all([
        dose_dipirona_1,
        dose_toragesic_1,
        dose_dipirona_2,
    ])
    await db_session.commit()

    delayed_taken_time = start_time + timedelta(hours=1, minutes=30)
    await dose_service.mark_dose_as_taken(
        dose_dipirona_1.id, delayed_taken_time
    )

    refreshed_dipirona_2 = await dose_repo.get_by_id(dose_dipirona_2.id)
    assert refreshed_dipirona_2 is not None
    expected_dipirona_2_time = delayed_taken_time + timedelta(hours=6)
    assert (
        SchedulerEngine._to_utc(refreshed_dipirona_2.scheduled_at)
        == expected_dipirona_2_time
    )

    refreshed_toragesic_1 = await dose_repo.get_by_id(dose_toragesic_1.id)
    assert refreshed_toragesic_1 is not None
    expected_toragesic_1_time = delayed_taken_time + timedelta(hours=2)
    assert (
        SchedulerEngine._to_utc(refreshed_toragesic_1.scheduled_at)
        == expected_toragesic_1_time
    )
