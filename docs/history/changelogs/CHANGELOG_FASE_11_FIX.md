# Changelog - Fase 11 (Fix Final)

## [1.11.1] - 2026-04-24

### Corrigido
- **Taxonomia Unificada**: Sincronização dos estados `ACCEPTED`, `REJECTED`, `DEFERRED`, `IGNORED` e `EXPIRED` em todas as camadas do sistema.
- **Enquadramento Documental**: `README_REVIEW.md` agora reflete corretamente o escopo de Histórico de Decisões (Fase 11).
- **Consistência do Frontend**: O `DecisionCenter` agora suporta explicitamente a ação "Adiar" e exibe o estado correto das recomendações.
- **Separação Decisão/Efeito**: Documentação técnica expandida para explicar que o efeito na carteira simulada é exclusivo do estado `ACCEPTED`.

### Alterado
- **Linguagem de Simulação**: Reforço da terminologia "Simulated Application" para evitar ambiguidade com execução real de mercado.
- **Auditoria**: O `impact_snapshot_json` agora é registrado mesmo em decisões sem efeito (como `REJECTED`), marcando como impacto vazio/nulo para fins de histórico.
