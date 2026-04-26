# Changelog - Fase 7: Consolidação Operacional

## [v7.0.0] - 2026-04-23

### Backend (Governance & Health)
- **Status API**: Implementação de `/api/v1/system/status` com integridade de banco, contagem de registros e indicadores de presença de dados (Seeded vs Real).
- **Configuração**: Adição de `ENVIRONMENT_MODE` ao core config para distinguir contextos de execução.
- **Seeds**: Refatoração de `seed_db.py` com suporte a CLI (`--mode minimal`, `--mode demo`) e flag `--clean`.

### Frontend (Observability)
- **Status Dashboard**: Adição de widgets de saúde do sistema no `PerformanceDashboard` (DB Status, Env Mode, Signal Counts).
- **Indicadores Visuais**: Badge dinâmico para presença de dados reais vs. sementes.

### Governança & Arquitetura
- **Templates de Ambiente**: Criação de `.env.demo.example`, `.env.real.example`, `.env.minimal.example` e padronização do `.env.example`.
- **Modulariedade**: Criação de `docs/ARCHITECTURE.md` estabelecendo a estratégia de expansão para B3/Opções sem alteração de schema imediata.
- **Saneamento**: Movimentação de changelogs antigos para `docs/history/` e limpeza do diretório raiz.
- **Manual**: Criação do `README_OPERATIONAL.md` com instruções de setup e manutenção.
