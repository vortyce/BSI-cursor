# Changelog - Fase 6: Refinamento Analítico e Robustez Operacional

## [v6.0.0] - 2026-04-23

### Análise e Métricas
- **LLM Impact Analysis**: Implementação de endpoint dedicado e visão no dashboard para medir o valor incremental da IA (Alpha da IA).
- **Amostragem ($n$)**: Inclusão sistemática do tamanho da amostra em todas as métricas para evitar conclusões precipitadas em grupos pequenos.
- **Métricas Granulares**: Adição de taxas de resolução, abertura e sucesso interpretado.
- **Avisos de Amostra**: Implementação de alertas visuais no frontend para grupos com menos de 5 sinais.

### Classificação de Qualidade dos Dados
- **DataSourceQuality**: Implementação de taxonomia para distinguir a origem dos dados:
    - `SEEDED_DEMO`: Dados artificiais de demonstração.
    - `REAL_CAPTURED`: Fluxo real de sinais.
    - `PARTIAL`: Dados reais incompletos.
    - `INSUFFICIENT`: Base insuficiente para análise.
    - `MANUAL_OVERRIDE`: Ajuste manual por operador.

### Explicabilidade Operacional
- **Primary Thesis**: Nova taxonomia de teses dominante (ex: `TREND_ALIGNED`, `VOLATILITY_WARNING`, `UNCLEAR_CONTEXT`) para categorizar a lógica da interpretação do LLM.

### Engenharia
- **Contratos Unificados**: Alinhamento de tipos entre backend (FastAPI) e frontend (TypeScript).
- **Robustez de API**: Novos filtros por qualidade de dados nos endpoints de performance.
