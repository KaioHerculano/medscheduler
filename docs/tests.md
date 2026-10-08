# Testes e Qualidade

O projeto MedScheduler mantem cobertura total com testes automatizados assincronos e verificacao estatica de codigo.

---

## Execucao dos Testes

Os testes sao executados utilizando **Pytest** integrado ao **pytest-asyncio**:

```bash
python3 -m pytest
```

Para execucao com relatorio detalhado:

```bash
python3 -m pytest -v
```

---

## Verificacao Estatica com Ruff

O projeto utiliza o **Ruff** com limite de 79 caracteres por linha, aspas simples e regras de ordenacao de imports (isort):

```bash
python3 -m ruff check .
```

Para formatacao automatica:

```bash
python3 -m ruff format .
```

---

## Estrutura da Suite de Testes

- `tests/test_health.py`: Verificacao basica do endpoint `/health`.
- `tests/test_medications.py`: Cadastro e listagem de farmacos e grupos.
- `tests/test_scheduler_engine.py`: Testes unitarios do algoritmo de rotacao e regras matematicas.
- `tests/test_delayed_rescheduling.py`: Testes de integracao do recalculo em cascata com atraso.
- `tests/test_scheduler_worker.py`: Testes dos jobs periodicos de despacho e insistencia (Nagging).
- `tests/test_telegram.py`: Testes do servico HTTP, envio de lembretes, comando `/status` e processamento de callbacks.
