# Changelog - Fase 10 (Gestão da Carteira Viva)

## [1.10.0] - 2026-04-24

### Adicionado
- **Modelos de Dados**: `PortfolioPosition`, `PortfolioReview`, `PortfolioActionItem`.
- **Enums**: `PositionStatus`, `PortfolioActionType`, `ConcentrationStatus`.
- **Serviço de Review**: `PortfolioReviewService` com lógica de cálculo de pesos dinâmicos e detecção de drift.
- **Heurística de Substituição**: Comparação de scores entre posições ativas e novos sinais (threshold +20).
- **Frontend**: Nova interface de Gestão de Carteira com diagnóstico visual e lista de ações.
- **Seeded Demo**: Novos cenários para demonstrar excesso de domínio e oportunidade superior.

### Alterado
- **Portfolio API**: Novos endpoints para gestão de posições e execução de reviews.
- **PortfolioTab**: Integração de sub-navegação entre Alocação e Gestão.
- **Seed Script**: Atualizado para popular o estado inicial da carteira viva.

### Corrigido
- Normalização de imports no backend.
- Limpeza de BOM (Byte Order Mark) no arquivo de configuração `.env`.
