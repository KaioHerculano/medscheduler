# Instalacao e Execucao

Guia passo a passo para configurar o ambiente de desenvolvimento e executar os servicos.

---

## Pre-requisitos

- Docker e Docker Compose instalados.
- Python 3.9+ (caso execute localmente sem Docker).
- Bot do Telegram criado via `@BotFather`.

---

## Execucao com Docker Compose

1. Clone o repositorio:
   ```bash
   git clone https://github.com/KaioHerculano/medscheduler.git
   cd medscheduler
   ```

2. Crie e configure o arquivo `.env`:
   ```bash
   cp .env.example .env
   ```

3. Inicie os containers:
   ```bash
   docker compose up -d --build
   ```

4. Execute as migrations do banco de dados:
   ```bash
   docker compose exec app alembic upgrade head
   ```

5. Carregue o catalogo inicial de medicamentos:
   ```bash
   docker compose exec app python scripts/seed.py
   ```

O servico estara disponivel em `http://localhost:8000` e a documentacao interativa em `http://localhost:8000/docs`.
