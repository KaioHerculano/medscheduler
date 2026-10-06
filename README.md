# 📋 MedScheduler

Sistema backend para gerenciamento automatizado de rotina pós-operatória de medicamentos, focado em **analgesia escalonada rotativa** (rotação de fármacos sem colisão) e integração bidirecional com Telegram (Mobile UI com Inline Buttons) e Discord (Log / Monitoramento).

---

## 🛠️ Tecnologias
- **FastAPI** (Python 3.11+)
- **PostgreSQL** + **SQLAlchemy 2.0 (Async)** + **Alembic**
- **Redis** + **APScheduler**
- **Telegram Bot API**
- **Discord Webhooks**
- **Docker & Docker Compose**

---

## 📌 Roadmap de Implementação

- [ ] **Fase 1: Fundação do Backend** (Docker Compose, Banco de Dados, Modelos SQLAlchemy, Migrations e Seeds)
- [ ] **Fase 2: Integração com Telegram** (Bot, Teclados Inline e Webhooks de Ação)
- [ ] **Fase 3: Motor de Rotação e Agendamento** (Cálculo analgésico e APScheduler)
- [ ] **Fase 4: Auditoria Discord e Refinamentos UX** (Logs em tempo real e notificações)
