# BSI Phase 9: Initial Capital Allocation Layer

## Visão Geral
A Fase 9 introduz a primeira camada de decisão estratégica de capital do BSI. Diferente das fases anteriores que focavam em captura e interpretação de sinais individuais, esta fase olha para o **portfólio como um todo**, filtrando e priorizando oportunidades com base em restrições explícitas do usuário.

## Componentes Principais

### 1. Perfil do Usuário (`PortfolioProfile`)
O sistema agora exige um perfil explícito para sugerir alocações.
- **Capital Inicial**: O montante total sob gestão.
- **Perfil de Risco**: Influencia quais teses são aceitáveis (ex: sinais agressivos são rejeitados em perfis conservadores).
- **Limites de Exposição**: Travas de segurança para evitar concentração excessiva em um único ativo ou domínio.
- **Reserva de Caixa**: Capital intocável para segurança operacional.

### 2. Motor de Alocação Heurístico
O motor utiliza uma heurística explicável para ranquear oportunidades:
- **Priority Score**: Calculado como uma média ponderada de Confiança (40%), Alinhamento de Contexto (30%), Tese (20%) e Qualidade de Dados (10%).
- **Lógica Greedy**: Aloca capital seguindo o ranking até que os limites de exposição ou o capital disponível se esgotem.

### 3. Ranking e Justificativa
Cada oportunidade recebe um status claro:
- `RECOMMENDED`: Passou em todos os filtros e tem prioridade.
- `SECONDARY`: Elegível, mas recebeu menos capital por prioridade inferior.
- `OUT_OF_PROFILE`: Rejeitado por incompatibilidade de risco.
- `CAPITAL_CONSTRAINED`: Elegível, mas barrado por limites de capital/exposição.
- `LOW_PRIORITY`: Abaixo do threshold mínimo de qualidade/score.

## IMPORTANTE: Natureza desta Camada
- **NÃO é um Otimizador Quantitativo**: Não utiliza correlação histórica ou teoria moderna de portfólio (Markowitz/Black-Litterman) ainda. É um motor de regras heurísticas.
- **NÃO Executa Ordens**: Esta camada gera **recomendações**. A execução permanece sob julgamento do usuário.
- **Seeded Demo**: Os dados iniciais de demonstração servem para ilustrar a estrutura de decisão e não representam conselhos de investimento ou performance real garantida.

## Como Operar
1. Acesse a aba **Portfolio**.
2. Configure seu capital e restrições no formulário à esquerda.
3. Clique em **Recalcular Alocação** para processar os sinais mais recentes (últimas 24h) contra seu perfil.
4. Analise o ranking e as justificativas para decidir suas próximas ações manuais.
