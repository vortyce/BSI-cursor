# BSI Domain & Market Guide (Fase 8)

O BSI Terminal suporta arquitetura multi-domínio, permitindo isolamento analítico entre mercados distintos.

## Domínios Suportados

1. **CRYPTO_SPOT**
   - Ativos: Criptoativos (BTC, ETH, etc).
   - Funcionamento: 24/7.
   - Seed: `--mode crypto_demo`

2. **B3_EQUITIES**
   - Ativos: Ações brasileiras (PETR4, VALE3, etc).
   - Funcionamento: Horário comercial BRT.
   - Seed: `--mode b3_demo`

## Heurística de Sessão (B3)

> [!IMPORTANT]
> A derivação de sessões da B3 no BSI é uma **heurística operacional de MVP**.
> - Não substitui o calendário oficial ou feeds de dados em tempo real da B3.
> - Serve exclusivamente para enriquecer o contexto do módulo B3 Equities para a interpretação do LLM.
> - Não pretende refletir todas as fases reais do pregão (como leilões de interrupção ou variações de horário de verão) com precisão regulatória.

Atualmente, o sistema utiliza janelas fixas (UTC-3) para classificar o sinal:
- **PRE_MARKET:** 09:00 - 10:00 (Leilão de Abertura sugerido)
- **REGULAR_SESSION:** 10:00 - 17:00
- **CLOSING_PHASE:** 17:00 - 18:00
- **AFTER_MARKET:** 18:00 - 19:00
- **OUT_OF_SESSION:** Período noturno/madrugada.

## Gerenciamento de Dados (Seeds)

O script `seed_db.py` no diretório do backend permite popular o sistema para demonstração:

- `python seed_db.py --mode crypto_demo`: Popula apenas sinais e desfechos de Cripto.
- `python seed_db.py --mode b3_demo`: Popula apenas sinais e desfechos de B3 Equities.
- `python seed_db.py --mode all_demo`: Popula ambos os domínios (padrão).
- `python seed_db.py --clean`: Limpa o banco antes de popular.

## Convenções de Ambiente

O pacote de auditoria inclui apenas templates de configuração:
- `.env.example`: Configuração geral.
- `.env.demo.example`: Configuração otimizada para modo demonstração local.
- `.env.real.example`: Configuração para ambiente de produção (Postgres/OpenAI Real).
- `.env.minimal.example`: Configuração mínima para teste de conectividade.
