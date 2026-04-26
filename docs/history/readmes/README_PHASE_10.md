# Phase 10: Gestão da Carteira Viva

Esta fase marca a transição do BSI de um motor de recomendações estáticas para uma camada de gestão de portfólio dinâmico. O sistema agora é capaz de monitorar posições ativas, detectar desvios de perfil (*drift*) e sugerir substituições inteligentes baseadas em edge superior.

## Novos Conceitos

### 1. Posições Ativas (`PortfolioPosition`)
Representam o capital atualmente comprometido em ativos. Diferente das recomendações, as posições são persistentes e rastreáveis. No MVP, o sistema assume que o usuário seguiu a recomendação e mantém o estado "simulado" da carteira.

### 2. Diagnóstico de Saúde (Drift & Concentração)
O motor de Review agora analisa:
- **Concentração por Ativo**: Se uma valorização ou aporte ultrapassou o limite de `% por posição` definido no perfil.
- **Exposição por Domínio**: Se a soma das posições em Crypto ou B3 ultrapassou o teto permitido.
- **Drift de Caixa**: Se a reserva de liquidez está abaixo do mínimo exigido.

### 3. Heurística de Substituição (`REPLACE`)
O sistema compara continuamente as posições atuais com novos sinais interpretados. 
- **Regra**: Se um novo sinal tem um `Priority Score` pelo menos 20 pontos superior à posição mais fraca da carteira e o capital disponível é insuficiente, o sistema sugere a **Substituição**.
- **Justificativa**: "Trocar Ativo A (Score 60) por Ativo B (Score 85) para priorizar alocação em oportunidade superior."
- **Nota**: Este threshold é uma heurística provisória de MVP para demonstrar a lógica de priorização assistida, não representando uma solução de otimização matemática final.

## Operação

### Aba "Gestão da Carteira"
No frontend, a nova aba de Gestão permite:
1. **Visualizar Diagnóstico**: Gráficos de barra mostrando o uso de limites por domínio.
2. **Rodar Análise de Saúde**: Executa o motor heurístico manualmente.
3. **Sugestões de Ação**: Lista de cards (`HOLD`, `REDUCE`, `REPLACE`) com justificativas auditáveis.
4. **Ciente**: Registro de que a sugestão foi analisada pelo usuário.

## Princípios de Design
- **Não-Automação**: O sistema nunca altera a carteira sozinho.
- **Sobriedade**: A linguagem foca em métricas e diagnósticos técnicos, evitando termos de marketing.
- **Transparência**: O "Porquê" da ação é tão importante quanto a ação sugerida.
