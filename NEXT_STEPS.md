# BSI - Next Steps (Pós-Fase 11)

## Fase 12: Módulos de Opções (B3 & BTC)
- Ingestão de sinais de opções (Greeks, Strike, Expiry).
- Prompt especializado para estratégias de proteção (Hedge) e renda.
- Visualização de "Payoff" no frontend para decisões assistidas.

## Fase 13: Integração Read-Only com Broker
- Conexão via API (Binance, B3/Corretoras) para leitura de saldo real.
- Sincronização da Carteira Simulada (Intenção) vs. Carteira Real (Execução).
- Alertas de divergência e drift entre o plano registrado e a realidade da conta.

## Fase 14: Analytics de Aderência Operacional
- Score de fidelidade do usuário ao sistema.
- Relatórios de performance comparativa: Sistema vs. Usuário.
- Análise de "Faltas" (performance de sinais rejeitados).

## Infraestrutura
- Implementação de workers de expiração automática para a Camada de Governança.
- Migração de banco de dados para PostgreSQL.
