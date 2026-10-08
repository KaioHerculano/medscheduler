# Arquitetura do Sistema

O MedScheduler segue principios de arquitetura em camadas e desacoplamento conforme padroes de Clean Architecture e SOLID.

---

## Diagrama de Blocos

```mermaid
flowchart TD
    subgraph Client["Camada de Interface"]
        TelegramUser["Usuario no Telegram"]
        APIClient["Cliente HTTP (Frontend / Postman)"]
    end

    subgraph API["FastAPI Application"]
        Routers["app/routers/ (health, medications, doses, webhooks)"]
        Lifespan["FastAPI Lifespan (Startup / Shutdown)"]
    end

    subgraph ServiceLayer["Camada de Servicos (Business Logic)"]
        DoseService["DoseService"]
        MedicationService["MedicationService"]
        TelegramWebhookService["TelegramWebhookService"]
        TelegramService["TelegramService (HTTP Client)"]
        SchedulerEngine["SchedulerEngine (Dominio Puro)"]
    end

    subgraph WorkerLayer["Trabalhadores Assincronos"]
        APScheduler["APScheduler"]
        PendingJob["check_and_dispatch_pending_doses"]
        NaggingJob["check_and_dispatch_nagging_reminders"]
    end

    subgraph DataLayer["Camada de Persistencia"]
        DoseRepository["DoseRepository"]
        MedicationRepository["MedicationRepository"]
        RotationGroupRepository["RotationGroupRepository"]
        PostgreSQL[("PostgreSQL 16")]
    end

    APIClient --> Routers
    TelegramUser -->|Webhook| Routers
    Routers --> DoseService
    Routers --> MedicationService
    Routers --> TelegramWebhookService
    TelegramWebhookService --> DoseService
    TelegramWebhookService --> TelegramService
    DoseService --> SchedulerEngine
    DoseService --> DoseRepository
    DoseService --> MedicationRepository
    Lifespan --> APScheduler
    APScheduler --> PendingJob
    APScheduler --> NaggingJob
    PendingJob --> TelegramService
    NaggingJob --> TelegramService
    PendingJob --> DoseRepository
    NaggingJob --> DoseRepository
    DoseRepository --> PostgreSQL
    MedicationRepository --> PostgreSQL
    RotationGroupRepository --> PostgreSQL
```

---

## Divisao de Responsabilidades

- **Routers (`app/routers/`)**: Recebem requisicoes HTTP, validam schemas Pydantic e injetam dependencias.
- **Services (`app/services/`)**: Centralizam regras de negocio, orquestracao de fluxos e chamadas a servicos externos.
- **Repositories (`app/repositories/`)**: Encapsulam exclusivamente operacoes de persistencia com SQLAlchemy 2.0 Async.
- **Engine (`SchedulerEngine`)**: Regras matematicas e de dominio puras sem dependencia de banco ou framework.
- **Workers (`app/workers/`)**: Rotinas de agendamento em background gerenciadas pelo APScheduler.
