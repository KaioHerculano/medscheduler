import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock

import pytest
from httpx import AsyncClient

from app.core.config import settings
from app.main import app
from app.models.enums import DoseStatus
from app.routers.dependencies import get_telegram_service
from app.services.telegram_service import TelegramService


@pytest.fixture
def mock_telegram_service() -> TelegramService:
    service = TelegramService(bot_token='mock_token')
    service.send_dose_reminder = AsyncMock(return_value=123)
    service.answer_callback_query = AsyncMock(return_value=True)
    service.edit_message_text = AsyncMock(return_value=True)
    return service


@pytest.mark.asyncio
async def test_telegram_send_dose_reminder_success() -> None:
    mock_client = AsyncMock()
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'result': {'message_id': 999}}
    mock_client.post.return_value = mock_response

    service = TelegramService(bot_token='test_token', http_client=mock_client)
    message_id = await service.send_dose_reminder(
        chat_id='12345',
        dose_id=str(uuid.uuid4()),
        medication_name='Toragesic',
        notes='Sublingual',
    )

    assert message_id == 999
    assert mock_client.post.called


@pytest.mark.asyncio
async def test_webhook_dose_taken(
    async_client: AsyncClient,
    mock_telegram_service: TelegramService,
) -> None:
    app.dependency_overrides[get_telegram_service] = lambda: (
        mock_telegram_service
    )

    med_response = await async_client.post(
        '/medications/',
        json={
            'name': 'Dipirona',
            'category': 'ANALGESIC',
            'min_interval_hours': 6,
        },
    )
    med_id = med_response.json()['id']

    dose_response = await async_client.post(
        '/doses/',
        json={
            'medication_id': med_id,
            'scheduled_at': datetime.now(timezone.utc).isoformat(),
        },
    )
    dose_id = dose_response.json()['id']

    webhook_payload = {
        'callback_query': {
            'id': 'cq_123',
            'data': f'dose:{dose_id}:taken',
            'message': {
                'message_id': 456,
                'chat': {'id': 789},
            },
        }
    }

    response = await async_client.post(
        '/webhooks/telegram', json=webhook_payload
    )
    assert response.status_code == 200
    assert response.json()['status'] == 'processed'

    timeline_response = await async_client.get('/doses/timeline')
    timeline = timeline_response.json()
    taken_doses = timeline[DoseStatus.TAKEN.value]
    assert any(d['id'] == dose_id for d in taken_doses)

    assert mock_telegram_service.answer_callback_query.called
    assert mock_telegram_service.edit_message_text.called

    app.dependency_overrides.pop(get_telegram_service, None)


@pytest.mark.asyncio
async def test_webhook_dose_snooze(
    async_client: AsyncClient,
    mock_telegram_service: TelegramService,
) -> None:
    app.dependency_overrides[get_telegram_service] = lambda: (
        mock_telegram_service
    )

    med_response = await async_client.post(
        '/medications/',
        json={
            'name': 'Paco',
            'category': 'ANALGESIC',
            'min_interval_hours': 6,
        },
    )
    med_id = med_response.json()['id']

    dose_response = await async_client.post(
        '/doses/',
        json={
            'medication_id': med_id,
            'scheduled_at': datetime.now(timezone.utc).isoformat(),
        },
    )
    dose_id = dose_response.json()['id']

    webhook_payload = {
        'callback_query': {
            'id': 'cq_456',
            'data': f'dose:{dose_id}:snooze_15',
            'message': {
                'message_id': 789,
                'chat': {'id': 101112},
            },
        }
    }

    response = await async_client.post(
        '/webhooks/telegram', json=webhook_payload
    )
    assert response.status_code == 200
    assert response.json()['status'] == 'processed'

    timeline_response = await async_client.get('/doses/timeline')
    timeline = timeline_response.json()
    snoozed_doses = timeline[DoseStatus.SNOOZED.value]
    assert any(d['id'] == dose_id for d in snoozed_doses)

    app.dependency_overrides.pop(get_telegram_service, None)


@pytest.mark.asyncio
async def test_webhook_dose_skip(
    async_client: AsyncClient,
    mock_telegram_service: TelegramService,
) -> None:
    app.dependency_overrides[get_telegram_service] = lambda: (
        mock_telegram_service
    )

    med_response = await async_client.post(
        '/medications/',
        json={
            'name': 'Vonau',
            'category': 'ANTIEMETIC',
            'min_interval_hours': 8,
            'is_as_needed': True,
        },
    )
    med_id = med_response.json()['id']

    dose_response = await async_client.post(
        '/doses/',
        json={
            'medication_id': med_id,
            'scheduled_at': datetime.now(timezone.utc).isoformat(),
        },
    )
    dose_id = dose_response.json()['id']

    webhook_payload = {
        'callback_query': {
            'id': 'cq_789',
            'data': f'dose:{dose_id}:skip',
            'message': {
                'message_id': 999,
                'chat': {'id': 333},
            },
        }
    }

    response = await async_client.post(
        '/webhooks/telegram', json=webhook_payload
    )
    assert response.status_code == 200
    assert response.json()['status'] == 'processed'

    timeline_response = await async_client.get('/doses/timeline')
    timeline = timeline_response.json()
    skipped_doses = timeline[DoseStatus.SKIPPED.value]
    assert any(d['id'] == dose_id for d in skipped_doses)

    app.dependency_overrides.pop(get_telegram_service, None)


@pytest.mark.asyncio
async def test_webhook_security_token_rejected(
    async_client: AsyncClient,
) -> None:
    original_secret = settings.TELEGRAM_WEBHOOK_SECRET
    settings.TELEGRAM_WEBHOOK_SECRET = 'secret_token_123'

    try:
        response = await async_client.post(
            '/webhooks/telegram',
            json={'callback_query': {}},
            headers={'x-telegram-bot-api-secret-token': 'wrong_token'},
        )
        assert response.status_code == 403
    finally:
        settings.TELEGRAM_WEBHOOK_SECRET = original_secret
