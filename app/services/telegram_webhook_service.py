from datetime import datetime, timezone
from typing import Any, Optional
from uuid import UUID
from app.services.dose_service import DoseService
from app.services.telegram_service import TelegramService


class TelegramWebhookService:
    def __init__(
        self,
        dose_service: DoseService,
        telegram_service: TelegramService,
    ) -> None:
        self.dose_service = dose_service
        self.telegram_service = telegram_service

    async def process_update(
        self, update_data: dict[str, Any]
    ) -> dict[str, str]:
        if 'callback_query' not in update_data:
            return {'status': 'ignored'}

        callback_query = update_data['callback_query']
        callback_id = callback_query['id']
        callback_data = callback_query.get('data', '')
        message = callback_query.get('message', {})
        chat_id = str(message.get('chat', {}).get('id'))
        message_id = message.get('message_id')

        parts = callback_data.split(':')
        if len(parts) != 3 or parts[0] != 'dose':
            await self.telegram_service.answer_callback_query(
                callback_id, 'Comando desconhecido'
            )
            return {'status': 'unrecognized'}

        try:
            dose_id = UUID(parts[1])
        except ValueError:
            await self.telegram_service.answer_callback_query(
                callback_id, 'Identificador invalido'
            )
            return {'status': 'invalid_id'}

        action = parts[2]
        return await self._execute_action(
            action=action,
            dose_id=dose_id,
            callback_id=callback_id,
            chat_id=chat_id,
            message_id=message_id,
        )

    async def _execute_action(
        self,
        action: str,
        dose_id: UUID,
        callback_id: str,
        chat_id: str,
        message_id: Optional[int],
    ) -> dict[str, str]:
        now = datetime.now(timezone.utc)
        time_formatted = now.strftime('%H:%M')

        if action == 'taken':
            await self.dose_service.mark_dose_as_taken(dose_id, now)
            await self.telegram_service.answer_callback_query(
                callback_id, 'Dose registrada com sucesso'
            )
            if message_id:
                await self.telegram_service.edit_message_text(
                    chat_id,
                    message_id,
                    f'Dose confirmada como tomada as {time_formatted}',
                )
            return {'status': 'processed'}

        if action == 'snooze_15':
            await self.dose_service.snooze_dose(dose_id, 15)
            await self.telegram_service.answer_callback_query(
                callback_id, 'Lembrete adiado em 15 minutos'
            )
            if message_id:
                await self.telegram_service.edit_message_text(
                    chat_id, message_id, 'Lembrete adiado em 15 minutos'
                )
            return {'status': 'processed'}

        if action == 'skip':
            await self.dose_service.skip_dose(dose_id)
            await self.telegram_service.answer_callback_query(
                callback_id, 'Dose pulada'
            )
            if message_id:
                await self.telegram_service.edit_message_text(
                    chat_id, message_id, 'Dose marcada como pulada'
                )
            return {'status': 'processed'}

        await self.telegram_service.answer_callback_query(
            callback_id, 'Acao invalida'
        )
        return {'status': 'unsupported_action'}
