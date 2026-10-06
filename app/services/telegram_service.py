from typing import Any, Optional
import httpx
from app.core.config import settings


class TelegramService:
    def __init__(
        self,
        bot_token: Optional[str] = None,
        http_client: Optional[httpx.AsyncClient] = None,
    ) -> None:
        self.bot_token = bot_token or settings.TELEGRAM_BOT_TOKEN
        self.base_url = (
            f'https://api.telegram.org/bot{self.bot_token}'
            if self.bot_token
            else ''
        )
        self.http_client = http_client

    async def _send_request(
        self, endpoint: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        if not self.bot_token:
            return {}

        url = f'{self.base_url}/{endpoint}'
        if self.http_client:
            response = await self.http_client.post(url, json=payload)
            response.raise_for_status()
            return response.json()

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            return response.json()

    async def send_dose_reminder(
        self,
        chat_id: str,
        dose_id: str,
        medication_name: str,
        notes: Optional[str] = None,
    ) -> Optional[int]:
        text = f'<b>Hora do Remedio:</b> {medication_name}'
        if notes:
            text += f'\n<i>Nota:</i> {notes}'

        keyboard = {
            'inline_keyboard': [
                [
                    {
                        'text': 'Tomei Agora',
                        'callback_data': f'dose:{dose_id}:taken',
                    },
                    {
                        'text': 'Adiar 15 min',
                        'callback_data': f'dose:{dose_id}:snooze_15',
                    },
                ],
                [
                    {
                        'text': 'Pular Dose',
                        'callback_data': f'dose:{dose_id}:skip',
                    }
                ],
            ]
        }

        payload = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'HTML',
            'reply_markup': keyboard,
        }

        data = await self._send_request('sendMessage', payload)
        return data.get('result', {}).get('message_id')

    async def answer_callback_query(
        self, callback_query_id: str, text: str = 'Confirmado'
    ) -> bool:
        payload = {
            'callback_query_id': callback_query_id,
            'text': text,
        }
        await self._send_request('answerCallbackQuery', payload)
        return True

    async def edit_message_text(
        self, chat_id: str, message_id: int, text: str
    ) -> bool:
        payload = {
            'chat_id': chat_id,
            'message_id': message_id,
            'text': text,
            'parse_mode': 'HTML',
        }
        await self._send_request('editMessageText', payload)
        return True
