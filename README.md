# MedScheduler

Sistema backend para gerenciamento automatizado da rotina pós-operatória de medicamentos, focado em analgesia escalonada rotativa (rotação de fármacos sem colisão) e integração bidirecional com o Telegram (Mobile UI com botões inline interativos).

---

## Tecnologias
- FastAPI (Python 3.11+)
- PostgreSQL + SQLAlchemy 2.0 (Async) + Alembic
- Redis + APScheduler
- Telegram Bot API
- Docker e Docker Compose
- MkDocs (Material Theme)

---

## Arquitetura e Princípios
- Clean Architecture / Arquitetura em Camadas
- Princípios SOLID
- Repositórios para abstração de acesso a dados
- Serviços para encapsulamento das regras de negócio
- Controladores / Rotas desacopladas com Injeção de Dependências
- Versionamento estrito de endpoints (`/api/v1/`)

---

## Roadmap de Implementação

- [x] **Fase 1: Fundação do Backend** (Docker Compose, Banco de Dados, Modelos SQLAlchemy, Migrações e Seeds)
- [x] **Fase 2: Integração com Telegram** (Bot, Teclados Inline e Webhooks de Ação)
- [x] **Fase 3: Motor de Rotação e Agendamento** (Cálculo analgésico e APScheduler)
- [x] **Fase 4: Refinamentos de UX, Resiliência e Documentação** (Mecanismo de insistência, comando `/status` e MkDocs na porta 8001)
- [ ] **Fase 5: Padronização de API, Fuso Horário e Revisão Gramatical** (Prefixo `/api/v1/`, fuso `America/Cuiaba` e acentuação completa)
- [ ] **Fase 6: Autenticação, Usuários e Segurança** (JWT, hash seguro com `pwdlib`, rota `/api/v1/auth/login` e proteção de endpoints)
- [ ] **Fase 7: Observabilidade, Auditoria e Prontidão de Produção** (Logs estruturados, rate limit, CORS e rastreamento de auditoria)
