# MedScheduler

Sistema backend para gerenciamento automatizado de rotina pos-operatoria de medicamentos, focado em analgesia escalonada rotativa (rotacao de farmacos sem colisao) e integracao bidirecional com Telegram (Mobile UI com Inline Buttons).

---

## Tecnologias
- FastAPI (Python 3.11+)
- PostgreSQL + SQLAlchemy 2.0 (Async) + Alembic
- Redis + APScheduler
- Telegram Bot API
- Docker e Docker Compose

---

## Arquitetura e Principios
- Clean Architecture / Arquitetura em Camadas
- Principios SOLID
- Repositories para abstracao de acesso a dados
- Services para encapsulamento das regras de negocio
- Controllers / Routers desacoplados com Dependency Injection

---

## Roadmap de Implementacao

- [x] Fase 1: Fundacao do Backend (Docker Compose, Banco de Dados, Modelos SQLAlchemy, Migrations e Seeds)
- [x] Fase 2: Integracao com Telegram (Bot, Teclados Inline e Webhooks de Acao)
- [ ] Fase 3: Motor de Rotacao e Agendamento (Calculo analgesico e APScheduler)
- [ ] Fase 4: Refinamentos UX e Documentacao (MkDocs padrao Material)
