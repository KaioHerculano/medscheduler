from typing import Any
from fastapi import APIRouter, Depends
from app.core.security import verify_telegram_webhook
from app.routers.dependencies import get_telegram_webhook_service
from app.services.telegram_webhook_service import TelegramWebhookService

router = APIRouter()


@router.post('/telegram')
async def handle_telegram_webhook(
    update_data: dict[str, Any],
    service: TelegramWebhookService = Depends(
        get_telegram_webhook_service
    ),
    _: bool = Depends(verify_telegram_webhook),
) -> dict[str, str]:
    return await service.process_update(update_data)
