# BSI - Review Package (Fase 11.5 FIX)

Esta entrega encerra a **Fase 11: Histórico de Decisões e Aprendizado Operacional**. O sistema agora implementa uma camada de governança assistida honesta, registrando o processo decisório do usuário sobre as recomendações sistêmicas.

## Escopo da Entrega (Fase 11)

1. **Taxonomia de Decisão Consolidada**: Estados `ACCEPTED`, `REJECTED`, `DEFERRED` e `EXPIRED` sincronizados entre Backend e Frontend. A ausência de decisão é o estado pendente natural.
2. **Histórico de Intenção**: Registro auditável das escolhas do usuário com justificativas, distinguindo claramente decisões com e sem efeito na carteira.
3. **Simulação Assistida (MVP Heuristics)**: Mutações na carteira ocorrem apenas em decisões aceitas, tratando-se de **simulação de intenção** baseada em heurísticas provisórias isoladas.
4. **Trilha Auditável (Audit Trail)**: Histórico cronológico comparando Sugestão vs Decisão vs Impacto Aplicado.

## Simulação e Heurísticas de MVP

> [!IMPORTANT]
> **Heurísticas Provisórias**: As regras de aplicação (ex: corte de 50% em REDUCE, threshold de +20 em REPLACE) estão isoladas no código como **[MVP SIMULATION POLICY]**. Elas servem para validar o fluxo de governança e não representam políticas financeiras ótimas ou execução real.
> **Sem Execução Real**: O BSI não possui integração com brokers, OMS ou envio de ordens reais nesta fase. Todas as mutações são registros de intenção aplicados ao motor de dados.

## Correções de Estabilidade da Fase 11.5

- Build frontend validado com `npm run build`.
- `DEFERRED` permanece rastreável e não é tratado como decisão final.
- `HOLD`/`NO_ACTION` não são expostos como pendências operacionais acionáveis.
- `domain` é persistido na ingestão de webhook, com default apenas quando ausente.
- Logger estruturado usa assinatura correta nos fluxos de interpretação.
- Pacote final limpo, sem `.env` ativo, bancos locais, ZIPs internos, `node_modules`, `dist`, `__pycache__` ou `*.pyc`.

## Integridade do Pacote

- **PROJECT_TREE.txt**: Reflete 1:1 o conteúdo do ZIP.
- **Higiene**: Removidos todos os artefatos de ambiente local (`.env`, `node_modules`, `__pycache__`).
- **Auditabilidade**: Cada mutação na carteira simulada agora possui um snapshot de impacto vinculado a uma decisão humana.

---
**Status**: Fase 11.5 FIX concluída e pronta para nova auditoria.
