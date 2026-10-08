# Configuracao

Todas as configuracoes sao gerenciadas atraves do Pydantic Settings em `app/core/config.py`, carregadas a partir de variaveis de ambiente ou do arquivo `.env`.

---

## Variaveis de Ambiente

| Variavel | Tipo | Padrao | Descricao |
| :--- | :--- | :--- | :--- |
| `PROJECT_NAME` | `str` | `MedScheduler` | Nome do projeto na documentacao FastAPI |
| `ENVIRONMENT` | `str` | `development` | Ambiente de execucao (`development`, `test`, `production`) |
| `DEBUG` | `bool` | `true` | Exibicao de logs SQL e detalhamento de erros |
| `DATABASE_URL` | `str` | `postgresql+asyncpg://...` | String de conexao assincrona com o PostgreSQL |
| `REDIS_URL` | `str` | `redis://localhost:6379/0` | URL do Redis |
| `TELEGRAM_BOT_TOKEN` | `str` | `None` | Token de autenticacao gerado pelo BotFather |
| `TELEGRAM_CHAT_ID` | `str` | `None` | Chat ID do paciente para recebimento dos alertas |
| `TELEGRAM_WEBHOOK_SECRET` | `str` | `None` | Segredo para validacao do cabecalho do webhook |
| `TIMEZONE` | `str` | `America/Sao_Paulo` | Fuso horario de referencia |

---

## Configuracao do Webhook no Telegram

Para apontar o webhook do Telegram para a sua instancia local em desenvolvimento:

```bash
curl -F "url=https://seu-dominio.ngrok.io/webhooks/telegram" \
     -F "secret_token=seu_segredo_configurado" \
     https://api.telegram.org/bot<SEU_TOKEN>/setWebhook
```
