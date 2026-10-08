# MedScheduler

Bem-vindo a documentacao oficial do **MedScheduler**.

O MedScheduler e um sistema backend desenvolvido em FastAPI para gerenciamento automatizado de rotina pos-operatoria de medicamentos, com foco central em **analgesia escalonada rotativa** e integracao bidirecional com o **Telegram**.

---

## Proposta de Valor

A gestao de farmacos no periodo pos-operatorio exige precisao rigorosa:
- Medicamentos de classes semelhantes (analgesicos/anti-inflamatorios) nao podem colidir em horarios proximos para evitar sobrecarga renal e hepatica.
- Intervalos minimos entre doses do mesmo principio ativo precisam ser estritamente respeitados.
- Confirmacoes manuais ou atrasos na ingestao demandam recalculamento dinamico de toda a grade de horarios.

O MedScheduler automatiza todo esse ciclo com alertas no celular via Telegram e botoes de confirmacao em tempo real.

---

## Principais Funcionalidades

- **Motor de Analgesia Rotativa**: Algoritmo que calcula distanciamento de seguranca entre principios ativos e propaga recalculamentos em cascata quando ocorrem atrasos.
- **Integracao Telegram Bot**: Notificacoes com botoes interativos inline (`Tomei Agora`, `Adiar 15 min`, `Pular Dose`) e comando `/status`.
- **Trabalhadores Assincronos (APScheduler)**: Verificacao continua de doses pendentes e mecanismo de insistencia (Nagging) para doses nao confirmadas.
- **Arquitetura Limpa e Desacoplada**: Repositorios e servicos organizados com base nos principios SOLID, SQLAlchemy 2.0 Async e PostgreSQL.

---

## Navegacao Rapida

- [Visao Geral](overview.md)
- [Arquitetura do Sistema](architecture.md)
- [Algoritmo de Rotacao](rotation-algorithm.md)
- [Endpoints da API](api-endpoints.md)
- [Integracao com Telegram](telegram-integration.md)
- [Agendador e Insistencia](scheduler-workers.md)
