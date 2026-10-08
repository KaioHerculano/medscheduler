# MedScheduler - Plano de Implementação Técnica

Sistema backend para gerenciamento automatizado de rotina pós-operatória de medicamentos, focado em analgesia escalonada rotativa (rotação de fármacos sem colisão) e integração bidirecional com o Telegram (Mobile UI com botões inline interativos).

---

## 1. Visão Geral da Arquitetura

O sistema opera de forma orientada a eventos e tarefas temporizadas:
- **FastAPI**: API REST assíncrona com versionamento estrito e receptor de webhooks do Telegram.
- **PostgreSQL + SQLAlchemy 2.0 (Async) + Alembic**: Persistência relacional de medicamentos, cronogramas, doses e usuários.
- **Redis + APScheduler**: Fila de agendamento de disparos de lembretes, insistência e recálculo em cascata.
- **Telegram Bot API**: Interface de usuário móvel com botões clicáveis interativos (`InlineKeyboardMarkup` / `CallbackQuery`).
- **MkDocs (Material Theme)**: Documentação técnica completa conteinerizada na porta 8001.

---

## 2. Modelagem do Banco de Dados

### 2.1. Entidades Principais

1. **medications**
   - `id`: UUID (Chave Primária)
   - `name`: String (ex: "Toragesic", "Paco", "Dipirona", "Cefadroxila")
   - `category`: Enum (`ANALGESIC`, `ANTIBIOTIC`, `GASTRIC_PROTECTION`, `MUSCLE_RELAXANT`, `ANTIEMETIC`)
   - `min_interval_hours`: Integer (ex: 6 para Toragesic, 12 para antibiótico)
   - `is_as_needed`: Boolean (ex: True para Vonau / náuseas)
   - `notes`: Text (ex: "Sublingual (dissolver sob a língua)", "Tomar em jejum")
   - `rotation_group_id`: UUID (Chave Estrangeira, opcional)

2. **rotation_groups**
   - `id`: UUID (Chave Primária)
   - `name`: String (ex: "Analgesia Rotativa Pós-Op")
   - `spacing_hours`: Integer (ex: 2 - espaçamento fixo mínimo entre qualquer medicamento do grupo)

3. **doses** (Agenda e Histórico)
   - `id`: UUID (Chave Primária)
   - `medication_id`: UUID (Chave Estrangeira)
   - `scheduled_at`: DateTime (com fuso horário UTC / America/Cuiaba)
   - `taken_at`: DateTime (opcional / nulo até confirmação)
   - `status`: Enum (`PENDING`, `TAKEN`, `SNOOZED`, `SKIPPED`)
   - `telegram_message_id`: Integer (opcional, para edição do botão após o clique)
   - `last_notified_at`: DateTime (opcional, registro temporal da última notificação enviada)
   - `reminder_count`: Integer (contador de notificações e avisos de insistência)
   - `created_at`: DateTime

4. **users** (Planejado para Fase 6)
   - `id`: UUID (Chave Primária)
   - `email`: String (único, indexado)
   - `hashed_password`: String (hash criptográfico seguro)
   - `full_name`: String
   - `is_active`: Boolean
   - `is_superuser`: Boolean
   - `created_at`: DateTime
   - `updated_at`: DateTime

---

## 3. Lógica de Domínio: Motor de Analgesia Rotativa

A regra central de segurança farmacológica:
$$T_{next} = \max(T_{M} + I_{M}, T_{G} + S_{G})$$

Onde:
- $T_{M}$: Horário da última tomada do mesmo princípio ativo.
- $I_{M}$: Intervalo mínimo do medicamento (`min_interval_hours`).
- $T_{G}$: Horário da tomada mais recente de qualquer fármaco do grupo rotativo.
- $S_{G}$: Espaçamento de segurança entre analgésicos (`spacing_hours`, padrão: 2 horas).

Em caso de atraso na confirmação ($\Delta t > 30$ minutos em relação ao horário previsto):
1. A dose é persistida com `status = TAKEN` e `taken_at = now`.
2. A próxima dose do mesmo medicamento é recalculada para $\max(T_{agendado}, T_{taken} + I_{M})$.
3. Todas as doses futuras do mesmo grupo rotativo sofrem ajuste progressivo em cascata mantendo no mínimo 2 horas de espaçamento.

---

## 4. Fases de Execução do Projeto

### Fase 1: Fundação do Backend (Concluída - PR #1)
- [x] Configuração do repositório, Docker Compose, Dockerfile e dependências.
- [x] Modelos do SQLAlchemy 2.0 (Async) e migrações com Alembic.
- [x] Arquitetura em camadas: Repositories e Services desacoplados com princípios SOLID.
- [x] Seed inicial com os 7 medicamentos da rotina pós-operatória.
- [x] Configuração inicial de testes com Pytest e pipeline de CI via GitHub Actions.

### Fase 2: Integração com Telegram e Botões (Concluída - PR #2)
- [x] Criação do serviço assíncrono `TelegramService` com httpx.
- [x] Envio de notificações de lembrete com teclado inline (`Tomei Agora`, `Adiar 15 min`, `Pular Dose`).
- [x] Endpoint de webhook para processar respostas e dar feedback imediato.
- [x] Edição da mensagem para remoção de botões após confirmação.
- [x] Validação de token secreto do webhook (`X-Telegram-Bot-Api-Secret-Token`).

### Fase 3: Motor de Rotação e Agendamento Automático (Concluída - PR #3)
- [x] Implementação pura do motor `SchedulerEngine` (cálculo determinístico e UTC).
- [x] Integração do APScheduler ao ciclo de vida (`lifespan`) do FastAPI.
- [x] Job periódico a cada minuto para disparo de doses pendentes vencidas.
- [x] Algoritmo reativo de recálculo em cascata para confirmações com atraso.

### Fase 4: Refinamento de UX, Resiliência e Documentação (Concluída - PR #4)
- [x] Mecanismo de insistência periódica (*nagging*): novo aviso a cada 10 minutos para doses pendentes (máximo 3 tentativas).
- [x] Colunas de rastreamento `last_notified_at` e `reminder_count` com migração Alembic.
- [x] Comando interativo `/status` no Telegram com resumo completo de doses do dia.
- [x] Parametrização completa de portas e variáveis de ambiente no Docker Compose e `.env`.
- [x] Suíte de documentação estática conteinerizada com MkDocs Material na porta 8001.

---

### Fase 5: Padronização de API, Fuso Horário e Revisão Gramatical (Próxima Fase)
- [ ] **Versionamento Estrito de Endpoints**:
  - Aplicação do prefixo `/api/v1/` para todas as rotas de domínio:
    - `/api/v1/medications` (gestão de medicamentos e grupos rotativos)
    - `/api/v1/doses` (agendamento, confirmação, adiamento e linha do tempo)
    - `/api/v1/webhooks` (recebimento de callbacks do Telegram)
  - Endpoint de verificação de integridade `/health_check` e `/health` na raiz da aplicação, em conformidade com os projetos de referência `car_api` e `fastapi-gym-backend`.
- [ ] **Adequação do Fuso Horário Local**:
  - Definição padrão de `TIMEZONE=America/Cuiaba` (UTC-4) no `.env.example` e em `app/core/config.py`.
  - Conversão determinística de exibições para o fuso de Cuiabá nas mensagens de texto do Telegram e no comando `/status` (ex: "às 08:30").
- [ ] **Atualização da Suíte de Testes**:
  - Adequação de todos os clientes de teste HTTP em `tests/` para consumir as rotas sob `/api/v1/`.
  - Inclusão de testes de contrato para `/health_check`.
- [ ] **Revisão Ortográfica e Gramatical Completa**:
  - Correção sistemática de acentuação e concordância em português no `README.md` e em todos os documentos de `docs/` (`index.md`, `overview.md`, `architecture.md`, `rotation-algorithm.md`, `api-endpoints.md`, `telegram-integration.md`, `scheduler-workers.md`, `installation.md`, `configuration.md`, `tests.md`).

---

### Fase 6: Autenticação, Usuários e Segurança de Acesso (JWT)
- [ ] **Modelagem e Persistência de Usuários**:
  - Criação do modelo `User` em `app/models/user.py` com campos `id`, `email`, `hashed_password`, `full_name`, `is_active`, `is_superuser`.
  - Criação da migração Alembic para tabela `users`.
  - Criação de `UserRepository` e `UserService` assíncronos.
- [ ] **Infraestrutura Criptográfica e Segurança**:
  - Configuração do `pwdlib` (Argon2 / Bcrypt) para hashing seguro e verificação de senhas.
  - Implementação de geração e validação de tokens JWT (HS256) em `app/core/security.py`.
  - Variáveis de ambiente `SECRET_KEY`, `ALGORITHM` e `ACCESS_TOKEN_EXPIRE_MINUTES`.
- [ ] **Endpoints de Autenticação e Usuários**:
  - Schemas Pydantic para `Token`, `TokenData`, `UserCreate`, `UserRead`, `UserUpdate`.
  - Router `/api/v1/auth`:
    - `POST /api/v1/auth/login` (emissão de token via OAuth2PasswordRequestForm / JSON).
  - Router `/api/v1/users`:
    - `POST /api/v1/users/` (cadastro de novos operadores).
    - `GET /api/v1/users/me` (consulta dos dados do usuário autenticado).
- [ ] **Proteção de Rotas com Dependency Injection**:
  - Implementação da dependência `get_current_user` para proteger os endpoints `/api/v1/medications` e `/api/v1/doses`.
  - Manutenção do isolamento do webhook `/api/v1/webhooks/telegram` protegido exclusivamente pela chave secreta do Telegram.
- [ ] **Suíte de Testes de Segurança**:
  - Testes unitários e de integração cobrindo login bem-sucedido, credenciais inválidas, expiração de tokens e bloqueio de rotas protegidas sem autenticação.

---

### Fase 7: Observabilidade, Auditoria e Prontidão de Produção (Futura)
- [ ] **Tratamento Global de Erros e Logs Estruturados**:
  - Middleware de correlação de requisições (`X-Correlation-ID`) e logs em formato JSON.
  - Exception handlers globais para padronização de respostas de erro (RFC 7807).
- [ ] **Segurança Adicional de Rede**:
  - Configuração de políticas de CORS (`CORSMiddleware`) e rate limiting nas rotas sensíveis.
- [ ] **Métricas e Monitoramento**:
  - Exposição de métricas para Prometheus e monitoramento da integridade dos jobs em segundo plano do APScheduler.
- [ ] **Auditoria de Histórico de Doses**:
  - Tabela de log de auditoria para registrar todas as alterações de status, adiamentos e justificativas de doses.
