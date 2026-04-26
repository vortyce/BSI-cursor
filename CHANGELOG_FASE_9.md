# Changelog - Fase 9: Alocação Inicial e Priorização

## [Backend]
- **Novos Modelos**: `PortfolioProfile`, `AllocationRecommendation`, `AllocationItem`.
- **Enums**: Adicionados `RiskProfile`, `PrimaryGoal`, `AllocationStatus`, etc.
- **Motor de Alocação**: Implementado `PortfolioService` com lógica de ranking heurístico explicável.
- **API**: Novos endpoints em `/api/v1/portfolio` para gestão de perfil e execução do motor.
- **Demo**: Atualizado `seed_db.py` para incluir cenários de alocação multi-domínio.

## [Frontend]
- **Nova Aba**: Adicionada aba "Portfolio" ao dashboard principal.
- **Gestão de Perfil**: Formulário para configuração de capital, risco e limites.
- **Visualização de Alocação**: Dashboard de breakdown de capital (Total, Reserva, Alocado, Disponível).
- **Ranking de Oportunidades**: Tabela detalhada com scores heurísticos, status coloridos e justificativas.

## [Arquitetura]
- Introdução da camada de decisão estratégica acima da camada de inteligência LLM.
- Separação clara entre "Sinal Aceitável" e "Sinal Alocável".
- Suporte explícito para a decisão de "Não Operar" (RecommendationStatus.NO_ACTION).
