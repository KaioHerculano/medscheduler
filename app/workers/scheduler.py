from datetime import datetime, timezone
from typing import Optional

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.core.config import settings
from app.core.database import async_session_factory
from app.repositories.dose_repository import DoseRepository
from app.services.telegram_service import TelegramService


async def check_and_dispatch_pending_doses(
    session_factory=async_session_factory,
    telegram_service: Optional[TelegramService] = None,
) -> int:
    if not settings.TELEGRAM_CHAT_ID:
        return 0

    client = telegram_service or TelegramService()
    now = datetime.now(timezone.utc)
    dispatched_count = 0

    async with session_factory() as session:
        dose_repository = DoseRepository(session)
        doses = await dose_repository.list_pending_ready_for_dispatch(now)

        for dose in doses:
            medication_name = (
                dose.medication.name if dose.medication else 'Medicamento'
            )
            notes = dose.medication.notes if dose.medication else None

            message_id = await client.send_dose_reminder(
                chat_id=settings.TELEGRAM_CHAT_ID,
                dose_id=str(dose.id),
                medication_name=medication_name,
                notes=notes,
            )
            if message_id:
                dose.telegram_message_id = message_id
                await dose_repository.update(dose)
                dispatched_count += 1

    return dispatched_count


def create_scheduler() -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        check_and_dispatch_pending_doses,
        'interval',
        minutes=1,
        id='pending_doses_checker',
        replace_existing=True,
    )
    return scheduler
