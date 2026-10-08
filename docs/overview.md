# Visao Geral

O MedScheduler foi concebido para eliminar erros comuns durante o periodo critico de recuperacao pos-cirurgica domiciliar.

---

## O Desafio da Analgesia Pos-Operatoria

Em recuperacoes pos-operatorias convencionais, prescrevem-se multiplos medicamentos com caracteristicas distintas:
- Antibacterianos (ex: Cefadroxila a cada 12 horas fixas).
- Protetores gastricos (ex: Omeprazol em jejum matinal).
- Analgesicos principais e de resgate (ex: Toragesic, Paco, Dipirona).
- Relaxantes musculares e antiemeticos de suporte.

O maior risco e a superposicao indevida de farmacos que atuam sobre as mesmas vias metabolicas ou a ingestao muito antecipada da proxima dose por esquecimento.

---

## Principios Clinicos Aplicados

1. **Intervalo Minimo por Principio Ativo**:
   Cada medicamento possui um atributo `min_interval_hours` (ex: 6 horas para Dipirona e Toragesic). Uma nova dose daquele remedio nunca pode ser agendada antes desse periodo.

2. **Espacamento de Seguranca de Grupo (Anti-Colisao)**:
   Medicamentos alocados em um mesmo `RotationGroup` compartilham um `spacing_hours` minimo (padrao: 2 horas). Se o Remedio A for tomado as 08:00, o Remedio B do mesmo grupo nao pode ocorrer antes das 10:00.

3. **Recalculo Reativo**:
   Se uma dose for confirmada com atraso superior a 30 minutos em relacao ao horario planejado, o sistema empurra as doses futuras em cascata para manter a conformidade clinica.
