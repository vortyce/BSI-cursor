# Changelog - Fase 11 (Microfix Final)

## [1.11.4] - 2026-04-24

### Alterado
- **Taxonomia Honesta**: Redução dos estados de decisão para `ACCEPTED`, `REJECTED`, `DEFERRED` e `EXPIRED`, alinhando backend e frontend.
- **Isolamento de Policy**: Formalização do bloco `[MVP SIMULATION POLICY]` no `DecisionService` para isolar heurísticas de alocação e mutação.
- **Audit Trail**: Melhoria visual no frontend para destacar decisões sem impacto na carteira (Intenção vs Efeito).
- **Encoding**: `PROJECT_TREE.txt` agora gerado em UTF-8 para melhor compatibilidade de auditoria.

### Removido
- Estado `IGNORED` da taxonomia oficial (tratado como ausência de decisão).
- Logs de `print()` no backend, substituídos por tratamento silencioso de erros de simulação com registro no banco.

### Documentação
- `README_REVIEW.md` reescrito para focar exclusivamente na Camada de Governança da Fase 11.
- `OPEN_ISSUES` e `NEXT_STEPS` atualizados para refletir as limitações honestas das heurísticas de MVP.
