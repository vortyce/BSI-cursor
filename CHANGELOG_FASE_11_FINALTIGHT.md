# Changelog - Fase 11 (FinalTight)

## [1.11.5] - 2026-04-24

### Alterado
- **Taxonomia Final**: Sincronização dos estados `ACCEPTED`, `REJECTED`, `DEFERRED` e `EXPIRED`. Removido estado `IGNORED` para evitar enum decorativo.
- **Simulation Policy**: Isolamento total do bloco `[MVP SIMULATION POLICY]` no `DecisionService`, marcando formalmente as heurísticas de alocação e preços como provisórias.
- **Audit Trail**: Melhoria na distinção visual entre decisões com impacto aplicado e apenas registros de intenção.
- **Encoding de Auditoria**: `PROJECT_TREE.txt` agora gerado via PowerShell em UTF-8 para garantir legibilidade.

### Documentação
- `README_REVIEW.md` reescrito para o contexto exclusivo da Fase 11.
- `OPEN_ISSUES` e `NEXT_STEPS` reancorados na Camada de Governança e Histórico.
- Glossário de heurísticas de MVP adicionado ao manual técnico.

### Removido
- Logs de `print()` residuais no backend.
- Referências a estados de decisão não suportados no frontend.
