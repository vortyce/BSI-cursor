# Changelog - Fase 11 (Final)

## [1.11.2] - 2026-04-24

### Adicionado
- **Taxonomia Completa**: Estados `ACCEPTED`, `REJECTED`, `DEFERRED`, `IGNORED` e `EXPIRED` suportados nativamente.
- **Botão "Adiar"**: Suporte no frontend para decisões conscientes de postergação.
- **Filtro de Expirados**: Recomendações que perderam a validade agora são tratadas explicitamente.
- **Snapshot de Impacto**: Registro detalhado do estado da carteira antes e depois de decisões aceitas.

### Alterado
- **Documentação Principal**: Migração total de contexto para Fase 11 nos arquivos `README_REVIEW.md`, `OPEN_ISSUES.md` e `NEXT_STEPS.md`.
- **Heurísticas de MVP**: Formalização das regras de simulação (50% reduce, +20 replace) como provisórias e auditáveis.
- **Trilha Auditável**: Melhoria visual para distinguir decisões aceitas com impacto aplicado de escolhas sem mutação.

### Corrigido
- Inconsistência de tipagem entre TypeScript e Enums Python na camada de decisão.
- Sincronização do estado `IGNORED` como o padrão para recomendações pendentes.
