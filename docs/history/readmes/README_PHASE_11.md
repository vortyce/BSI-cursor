# Phase 11: Histórico de Decisões e Aprendizado Operacional

Esta fase introduz a **Camada de Governança** do BSI. O sistema deixa de ser apenas consultivo para se tornar um diário operacional assistido, onde cada recomendação sistêmica aguarda uma decisão humana para ser refletida na carteira simulada.

## Conceitos de Governança

### 1. O Ato da Deciso (`PortfolioDecision`)
Cada recomendação gerada pelo motor de review (Fase 10) agora requer uma ação do usuário:
- **ACCEPTED**: O usuário concorda com a sugestão. O sistema aplica o efeito na carteira simulada.
- **REJECTED**: O usuário discorda. A recomendação é arquivada com a justificativa.
- **DEFERRED**: O usuário adia a decisão para um momento futuro (pendência mantida).
- **EXPIRED**: A recomendação perdeu a validade (timeout de 48h ou mudança drástica de mercado).

### 2. Aplicação Simulada (Simulated Impact)
Decisões `ACCEPTED` geram mutações no estado das posições:
- **REPLACE**: Encerra a posição antiga e abre a nova.
- **EXIT**: Marca a posição como `CLOSED`.
- **REDUCE**: Diminui o capital alocado na posição.

**Decisão vs. Efeito**:
- Uma **Decisão** é o ato de registro da escolha do usuário (ex: Rejeitar). Todas as interações geram uma `PortfolioDecision`.
- O **Efeito** é a mutação técnica da carteira. Este ocorre **apenas** quando o status é `ACCEPTED`. Decisões `REJECTED` ou `DEFERRED` são registradas para auditoria, mas não alteram o estado da carteira simulada.

> [!IMPORTANT]
> **Aviso de Simulação**: Estas ações ocorrem apenas no modelo de dados do BSI para fins de rastreabilidade e aprendizado. **Não há envio de ordens para corretoras ou execução real de capital.**

### 3. Trilha Auditável (Audit Trail)
O sistema mantém o registro:
`[Timestamp] -> [Recomendação Original] -> [Escolha do Usuário] -> [Nota do Usuário] -> [Efeito na Carteira]`

## Operação

### Central de Governança
No frontend, a aba de Gestão agora possui duas sub-visões:
1. **Status da Carteira**: Visão consolidada de posições e diagnósticos.
2. **Central de Governança**: Onde decisões pendentes são tomadas e o histórico auditável é consultado.

## Valor para o Aprendizado
Esta camada permite futuras análises de aderência:
- "Qual a minha taxa de aceitação para sinais de Crypto?"
- "Eu costumo ignorar sugestões de saída em ativos que depois caem?"
- "O sistema é mais conservador que o meu comportamento real?"
