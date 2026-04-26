# Changelog - Fase 6 FIX (Surgical Refinement)

## [v6.1.0] - 2026-04-23

### Backend (Analytical Core)
- **Summary Enriquecido**: Adição de `interpreted_success_rate`, `interpreted_failed_rate` e `no_interpretation_rate` ao serviço de performance.
- **Breakdown Honesto**: Inclusão sistemática de `n` (sample size), `avg_return_pct` e `median_return_pct` em todos os breakdowns.
- **Filtro de Qualidade**: Implementação de suporte a filtro por `data_quality` em todos os endpoints analíticos principais.
- **Mediana em Memória**: Implementação de cálculo de mediana em memória (via Python statistics) para contornar limitações do SQLite e garantir precisão analítica em amostras pequenas.

### Frontend (UI/UX Analítica)
- **Seletor de Qualidade**: Adicionado dropdown global no dashboard de performance para filtragem explícita de `data_quality`.
- **Badge Dinâmico**: O indicador de qualidade agora reflete o filtro ativo e destaca visualmente dados `SEEDED_DEMO`.
- **Avisos de Amostra**: Implementação de ícones de alerta (`ShieldAlert`) para grupos com $n < 5$ na tabela de breakdown.
- **Alinhamento de Contratos**: Sincronização total das interfaces TypeScript com o novo shape da API.

### Documentação
- **Reenquadramento Estratégico**: README_REVIEW reescrito para focar em "Refinamento Analítico" e "Robustez", abandonando a linguagem de demonstração da Fase 5.
