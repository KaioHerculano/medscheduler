# MedScheduler - Plano de Implementacao Tecnica

Sistema backend para gerenciamento automatizado de rotina pos-operatoria de medicamentos, focado em analgesia escalonada rotativa (rotacao de farmacos sem colisao) e integracao bidirecional com Telegram (Mobile UI com Inline Buttons).

---

## 1. Visao Geral da Arquitetura

O sistema opera orientado a eventos e tarefas temporizadas:
- FastAPI: API REST e receptor de Webhooks do Telegram.
- PostgreSQL + SQLAlchemy 2.0 (Async) + Alembic: Persistencia relacional de medicamentos, cronogramas e historico de doses.
- Redis + APScheduler: Fila de agendamento de disparos de lembretes e timers de rescalonamento.
- Telegram Bot API: Interface do usuario movel com botoes clicaveis (InlineKeyboardMarkup / CallbackQuery).

---

## 2. Modelagem do Banco de Dados

### 2.1. Entidades Principais

1. medications
   - id: UUID (PK)
   - name: String (ex: "Toragesic", "Paco", "Dipirona", "Cefadroxila")
   - category: Enum (ANALGESIC, ANTIBIOTIC, GASTRIC_PROTECTION, MUSCLE_RELAXANT, ANTIEMETIC)
   - min_interval_hours: Integer (ex: 6 para Toragesic, 12 para antibiotico)
   - is_as_needed: Boolean (ex: True para Vonau / nauseas)
   - notes: Text (ex: "Tomar com agua", "Em jejum")

2. rotation_groups
   - id: UUID (PK)
   - name: String (ex: "Analgesia Rotativa Pos-Op")
   - spacing_hours: Integer (ex: 2 - espacamento fixo entre qualquer medicamento do grupo)

3. doses (Agenda e Historico)
   - id: UUID (PK)
   - medication_id: UUID (FK)
   - scheduled_at: DateTime (com timezone UTC/America/Sao_Paulo)
   - taken_at: DateTime (nullable)
   - status: Enum (PENDING, TAKEN, SNOOZED, SKIPPED)
   - telegram_message_id: Integer (nullable, para edicao do botao apos o clique)
   - created_at: DateTime

---

## 3. Logica de Dominio: Motor de Analgesia Rotativa

A regra de negocio central:
Proximo Alarme = max(Ultima dose do remedio X + min_interval, Ultima dose de QUALQUER analgesico + spacing)

Se houver atraso na confirmacao de uma dose alem de 30 minutos:
1. A dose e marcada com o horario real em que foi tomada (taken_at).
2. O proximo agendamento do mesmo principio ativo e recalculado para taken_at + min_interval_hours.
3. A fila geral rotativa empurra os analgesicos subsequentes para manter a distancia de seguranca de 2 horas.

---

## 4. Fases de Execucao

### Fase 1: Fundacao do Backend
- [x] Configuracao do repositorio, Docker Compose (FastAPI + PostgreSQL + Redis), Dockerfile e dependencias.
- [x] Modelos do SQLAlchemy 2.0 (Async) e migrations com Alembic.
- [x] Arquitetura em camadas: Repositories e Services desacoplados com SOLID.
- [x] Seed inicial com os remedios da rotina pos-operatoria (Toragesic, Paco, Dipirona, Cefadroxila, Ciclobenzaprina, Omeprazol, Vonau).
- [x] Configuracao inicial de TDD (Pytest) e pipeline de CI/CD via GitHub Actions.

### Fase 2: Integracao com Telegram e Botoes
- [x] Criacao do servico assincrono do Telegram Bot API (TelegramService).
- [x] Implementacao do envio de mensagens com teclado inline (InlineKeyboardMarkup):
  - [ Tomei Agora ]
  - [ Adiar 15 min ]
  - [ Pular Dose ]
- [x] Endpoint de webhook (/webhooks/telegram) para processar o callback e dar feedback imediato.
- [x] Edicao da mensagem do bot removendo os botoes apos clique para evitar duplicidade.
- [x] Testes unitarios e de integracao para o servico e webhook do Telegram.

### Fase 3: Motor de Rotação e Agendamento Automatico
- [x] Implementacao do motor de rotacao analgesica (SchedulerEngine).
- [x] Integracao do APScheduler ao ciclo de vida do FastAPI.
- [x] Job a cada minuto conferindo doses com scheduled_at <= now() e status == PENDING.
- [x] Testes unitarios para regras de recalculamento de doses atrasadas e agendamentos.

### Fase 4: Refinamento de UX, Resiliencia e Documentacao
- [ ] Logica de insistencia (Nagging): novo aviso caso passe tempo limite sem confirmacao.
- [ ] Comando /status no Telegram para consultar a linha do tempo do dia.
- [ ] Documentacao completa com MkDocs (padrao Material) inspirada no car_api.
