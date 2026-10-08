# Algoritmo de Rotacao Analgesica

O motor de agendamento e rotacao e centralizado na classe `SchedulerEngine`, desenvolvida como modulo estatico e deterministico.

---

## Formula de Horario de Alarme

Para calcular o proximo horario de disparo de um medicamento $M$ pertencente ao grupo rotativo $G$:

$$T_{next} = \max(T_{M} + I_{M}, T_{G} + S_{G})$$

Onde:
- $T_{M}$: Horario da ultima tomada do mesmo principio ativo.
- $I_{M}$: Intervalo minimo do principio ativo (`min_interval_hours`).
- $T_{G}$: Horario da tomada mais recente de qualquer medicamento do mesmo grupo.
- $S_{G}$: Espacamento minimo de seguranca do grupo (`spacing_hours`, padrao: 2 horas).

---

## Deteccao de Atraso e Recalculo em Cascata

Quando o usuario confirma a ingestao atraves do botao `Tomei Agora`:

1. O sistema verifica se houve atraso:
   $$\Delta t = T_{taken} - T_{scheduled} > 30\text{ minutos}$$

2. Se $\Delta t > 30$ minutos:
   - A dose atual e persistida com `status = TAKEN` e `taken_at = T_{taken}`.
   - A proxima dose agendada do mesmo medicamento e recalculada para:
     $$T_{proxima} = \max(T_{agendado\_original}, T_{taken} + I_{M})$$
   - Todas as doses subsequentes do mesmo grupo rotativo sao ajustadas iterativamente:
     $$T_{dose_{i}} = \max(T_{dose_{i}}, T_{ref} + S_{G})$$
     garantindo que nenhuma dose do mesmo grupo ocorra antes de 2 horas da dose imediatamente anterior.

---

## Normalizacao Temporal (UTC)

Todas as funcoes de calculo utilizam normalizacao automatica para UTC via `SchedulerEngine._to_utc()`. Isso garante que datetimes sem fuso horario (como os retornados por SQLite em ambiente de teste) possam ser subtraidos e comparados com datetimes com fuso horario (como os gerados pelo `datetime.now(timezone.utc)` e pelo driver `asyncpg`).
