# BSI Architecture - Modular Expansion Strategy

O BSI foi desenhado para ser agnóstico ao mercado, permitindo expansão modular.

## Estrutura de Domínios (Futuro)
Embora a Fase 7 foque em consolidação, a estrutura de serviços deve seguir o padrão:
- `services/crypto_spot/`: Lógica específica para Bitcoin e Altcoins em Spot.
- `services/b3_equities/`: Lógica para mercado de ações brasileiro.
- `services/options/`: Lógica para gregas e cálculo de prêmios.

## Padrão de Integração
- **Ingestão**: Webhooks devem carregar metadados de domínio para roteamento.
- **Interpretação**: Prompts são isolados por domínio para garantir contexto técnico.
- **Performance**: Desfechos seguem a mesma taxonomia de qualidade, permitindo comparar IA vs Real em qualquer módulo.
