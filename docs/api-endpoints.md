# Endpoints da API

A API segue os padroes REST com serializacao e validacao estrita atraves do Pydantic v2.

---

## Health Check

### `GET /health`
Verifica a saude basica da aplicacao.

**Resposta de Sucesso (200 OK):**
```json
{
  "status": "ok"
}
```

---

## Medicamentos (`/medications`)

### `POST /medications/`
Cadastra um novo medicamento no catalogo.

**Corpo da Requisicao:**
```json
{
  "name": "Toragesic",
  "category": "ANALGESIC",
  "min_interval_hours": 6,
  "is_as_needed": false,
  "notes": "Sublingual",
  "rotation_group_id": null
}
```

### `GET /medications/`
Lista todos os medicamentos cadastrados.

---

## Doses e Cronograma (`/doses`)

### `POST /doses/`
Cria um agendamento de dose.

**Corpo da Requisicao:**
```json
{
  "medication_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "scheduled_at": "2026-10-08T08:00:00Z"
}
```

### `GET /doses/timeline`
Retorna a linha do tempo agrupada pelos status:
- `PENDING`
- `TAKEN`
- `SNOOZED`
- `SKIPPED`

---

## Webhook Telegram (`/webhooks/telegram`)

### `POST /webhooks/telegram`
Endpoint receptor de updates do Telegram (mensagens de texto e callbacks de botoes).

**Seguranca:**
Requer cabecalho opcional `X-Telegram-Bot-Api-Secret-Token` caso a variavel `TELEGRAM_WEBHOOK_SECRET` esteja configurada.
