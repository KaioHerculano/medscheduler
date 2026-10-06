from fastapi import Header, HTTPException, status

from app.core.config import settings


def verify_telegram_webhook(
    x_telegram_bot_api_secret_token: str = Header(None),
) -> bool:
    if (
        settings.TELEGRAM_WEBHOOK_SECRET
        and x_telegram_bot_api_secret_token != settings.TELEGRAM_WEBHOOK_SECRET
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid webhook secret',
        )
    return True
