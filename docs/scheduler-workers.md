# Agendador e Mecanismo de Insistencia (Nagging)

O agendamento temporal e gerenciado assincronamente pelo **APScheduler** integrado ao ciclo de vida da aplicacao FastAPI.

---

## Ciclo de Vida do FastAPI (Lifespan)

Em `app/main.py`, o agendador e inicializado e encerrado de maneira graciosa:

- Na inicializacao (`startup`): o `AsyncIOScheduler` inicia os jobs periodicos (exceto em ambiente de teste `ENVIRONMENT=test`).
- No encerramento (`shutdown`): o scheduler finaliza qualquer execucao em andamento de forma segura.

---

## Jobs Periodicos

### 1. `check_and_dispatch_pending_doses`
- **Frequencia**: A cada 1 minuto.
- **Criterio**: Doses com `status = PENDING`, `scheduled_at <= now` e `telegram_message_id IS NULL`.
- **Acao**: Envia lembrete no Telegram, registra `telegram_message_id`, define `last_notified_at = now` e incrementa `reminder_count = 1`.

### 2. `check_and_dispatch_nagging_reminders`
- **Frequencia**: A cada 1 minuto.
- **Criterio**: Doses com `status = PENDING`, `telegram_message_id IS NOT NULL`, `last_notified_at <= now - 10 minutos` e `reminder_count < 3`.
- **Acao**: Envia notificacao de insistencia destacando o atraso, inclui botoes inline para registro imediato, atualiza `last_notified_at = now` e incrementa `reminder_count`.
- **Limite de Seguranca**: O limite maximo de 3 avisos de insistencia impede envio ininterrupto de notificacoes.
