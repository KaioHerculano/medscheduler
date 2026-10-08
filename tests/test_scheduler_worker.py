from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.dose import Dose
from app.models.enums import DoseStatus, MedicationCategory
from app.models.medication import Medication
from app.repositories.dose_repository import DoseRepository
from app.services.telegram_service import TelegramService
from app.workers.scheduler import (
    check_and_dispatch_pending_doses,
    create_scheduler,
)
from tests.conftest import test_session_factory as db_session_factory


@pytest.mark.asyncio
async def test_check_and_dispatch_without_chat_id(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(settings, 'TELEGRAM_CHAT_ID', None)
    mock_service = TelegramService(bot_token='dummy_token')
    mock_service.send_dose_reminder = AsyncMock(return_value=123)

    count = await check_and_dispatch_pending_doses(
        session_factory=db_session_factory,
        telegram_service=mock_service,
    )
    assert count == 0
    mock_service.send_dose_reminder.assert_not_called()


@pytest.mark.asyncio
async def test_check_and_dispatch_pending_doses_success(
    db_session: AsyncSession,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(settings, 'TELEGRAM_CHAT_ID', 'test_chat_id')

    medication = Medication(
        name='Toragesic',
        category=MedicationCategory.ANALGESIC,
        min_interval_hours=6,
        notes='Sublingual',
    )
    db_session.add(medication)
    await db_session.flush()

    past_time = datetime.now(timezone.utc) - timedelta(minutes=5)
    future_time = datetime.now(timezone.utc) + timedelta(hours=2)

    due_dose = Dose(
        medication_id=medication.id,
        scheduled_at=past_time,
        status=DoseStatus.PENDING,
        telegram_message_id=None,
    )
    future_dose = Dose(
        medication_id=medication.id,
        scheduled_at=future_time,
        status=DoseStatus.PENDING,
        telegram_message_id=None,
    )
    db_session.add_all([due_dose, future_dose])
    await db_session.commit()

    mock_service = TelegramService(bot_token='dummy_token')
    mock_service.send_dose_reminder = AsyncMock(return_value=98765)

    dispatched = await check_and_dispatch_pending_doses(
        session_factory=db_session_factory,
        telegram_service=mock_service,
    )
    assert dispatched == 1
    mock_service.send_dose_reminder.assert_called_once_with(
        chat_id='test_chat_id',
        dose_id=str(due_dose.id),
        medication_name='Toragesic',
        notes='Sublingual',
    )

    dose_repo = DoseRepository(db_session)
    refreshed_due_dose = await dose_repo.get_by_id(due_dose.id)
    assert refreshed_due_dose is not None
    await db_session.refresh(refreshed_due_dose)
    assert refreshed_due_dose.telegram_message_id == 98765

    second_run_count = await check_and_dispatch_pending_doses(
        session_factory=db_session_factory,
        telegram_service=mock_service,
    )
    assert second_run_count == 0


def test_create_scheduler_configures_job() -> None:
    scheduler = create_scheduler()
    jobs = scheduler.get_jobs()
    assert len(jobs) == 1
    assert jobs[0].id == 'pending_doses_checker'
