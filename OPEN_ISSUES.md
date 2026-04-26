# BSI - Open Issues (Pós-Fase 11)

## Governança e Decisões
- **Heurísticas de Simulação**: O corte de 50% em `REDUCE` e a abertura de posições via `REPLACE` são heurísticas provisórias de MVP. Precisam ser substituídas por políticas de alocação dinâmica.
- **Expiração de Recomendações**: Falta um worker de background para expirar recomendações automaticamente após 48h sem resposta do usuário.
- **Shadow Trading**: O sistema registra decisões rejeitadas, mas ainda não calcula a performance hipotética desses sinais para análise de custo de oportunidade.

## Carteira Viva
- **Snapshot de Impacto**: O registro de impacto é baseado em snapshots JSON. Falta um histórico estruturado de saldo para gráficos de evolução patrimonial simulada.
- **Proxy de Preço**: A simulação usa o `trigger_price` como proxy, ignorando slippage e variações intradiárias.

## Dados e Infraestrutura
- **PostgreSQL**: Necessário para garantir a integridade das trilhas auditáveis em ambiente de produção.
- **Logging de Falhas**: Falhas na política de simulação são registradas silenciosamente no banco; falta um sistema de alertas para o administrador.
