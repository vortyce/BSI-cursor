# Changelog - BSI Terminal Fase 11.5 FIX

## [1.11.5-allocation-fix] - 2026-04-26

### Problemas Corrigidos

- Corrigida incoerência da engine de alocação que permitia Crypto como bloco principal em perfil conservador.
- Corrigido fluxo da interface para recalcular a recomendação imediatamente após salvar o perfil, evitando exibição de recomendação antiga via `/recommendation/latest`.
- Adicionados limites explícitos por perfil de risco sem alterar arquitetura, schema do banco ou contrato do frontend:
  - Conservador: Crypto limitado a 10% do capital total, B3 priorizado com mínimo preferencial de 80% e caixa limitado a 20%.
  - Moderado: Crypto limitado a 20% do capital total, B3 com mínimo de 60% e caixa limitado a 20%.
  - Agressivo: Crypto limitado a 35% do capital total e B3 com mínimo de 40%.
- Preservadas as heurísticas existentes de score, ranking de sinais, filtros por domínio, compatibilidade de perfil e status `NO_ACTION`.
- Incluída explicação textual quando o cap de Crypto reduz ou bloqueia uma recomendação.

### Arquivos Alterados

- `bsi-backend/app/services/portfolio_service.py`
- `bsi-frontend/src/components/PortfolioTab.tsx`
- `CHANGELOG.md`
- `PROJECT_TREE.txt`

### Validação

- Validação direta da engine com `capital_total = 100000` confirmou perfil conservador com `CRYPTO_SPOT = 10000` e `B3_EQUITIES = 80000`.
- Validação do cenário visual reportado, com `capital_total = 100000`, perfil conservador e reserva configurada em 25%, confirmou reserva limitada a `20000`, `CRYPTO_SPOT = 0` e `B3_EQUITIES = 80000`.
- Validação via API local `/api/v1/portfolio/recommendation/run` confirmou `cash = 20000`, `crypto = 0` e `b3 = 80000`.
- Validação direta confirmou que moderado permite mais Crypto que conservador e agressivo permite mais Crypto que moderado.
- Validação direta confirmou que `NO_ACTION` continua funcionando quando não há oportunidades elegíveis.
- Backend: `python -m compileall -q bsi-backend` passou.
- Backend: import da aplicação FastAPI passou.
- Backend: `seed_db.py --mode all_demo --clean` passou em SQLite temporário.
- Frontend: `npm run build` passou, confirmando compatibilidade sem alteração de contrato.
- Não houve mudança estrutural, alteração destrutiva de schema ou avanço para Fase 12.

## [1.11.5-fix-v2] - 2026-04-26

### Problemas Corrigidos

- Controllers em `app/api/v1/` não acessam mais ORM diretamente: removidos `db.query`, `db.add`, `db.commit`, `db.rollback`, `db.delete` e `db.refresh` da camada API.
- Controllers não importam mais models: removidos imports `from app.models...` dos endpoints.
- Controllers não levantam mais `HTTPException`; erros de domínio agora passam por `ServiceError`, `NotFoundError`, `ValidationError` e `BusinessRuleError`.
- Adicionado handler global para converter erros de service no envelope padronizado `{ success, data, error, meta }`.
- Movida a montagem de payloads complexos de controllers para services.
- Criado `SystemService` para concentrar checks e contagens de status operacional.
- Expandido `WebhookIngestionService` para listar sinais e montar detalhe completo sem vazamento de ORM para API.
- Expandido `PortfolioService`, `PortfolioReviewService` e `DecisionService` com métodos de aplicação/DTO legacy-compatible.
- Validação de dimensão de breakdown foi movida de controller para `OutcomeService`.
- Transações críticas foram revisadas para que controllers não controlem transação e operações lógicas fiquem nos services.

### Arquivos Alterados

- `bsi-backend/main.py`
- `bsi-backend/app/core/errors.py`
- `bsi-backend/app/api/v1/portfolio.py`
- `bsi-backend/app/api/v1/webhooks.py`
- `bsi-backend/app/api/v1/interpretations.py`
- `bsi-backend/app/api/v1/system.py`
- `bsi-backend/app/api/v1/outcomes.py`
- `bsi-backend/app/services/system_service.py`
- `bsi-backend/app/services/webhook_ingestion_service.py`
- `bsi-backend/app/services/portfolio_service.py`
- `bsi-backend/app/services/portfolio_review_service.py`
- `bsi-backend/app/services/decision_service.py`
- `bsi-backend/app/services/interpretation_service.py`
- `bsi-backend/app/services/outcome_service.py`
- `CHANGELOG.md`
- `PROJECT_TREE.txt`

### Validação

- Busca obrigatória em `app/api/v1/` não encontrou `db.query`, `db.add`, `db.commit`, `db.rollback`, `db.delete`, `db.refresh`, `from app.models` ou `raise HTTPException`.
- Backend: `python -m compileall -q bsi-backend` passou.
- Backend: import da aplicação FastAPI passou.
- Backend: `seed_db.py --mode all_demo --clean` passou em SQLite limpo de validação.
- Backend: smoke test do fluxo `webhook -> signal -> interpretation -> outcome -> portfolio -> decision` passou.
- Frontend: `npm install` passou.
- Frontend: `npm run build` passou.

### Riscos Remanescentes

- `npm install` ainda reporta 2 vulnerabilidades moderadas; requer análise com `npm audit` antes de ambiente real.
- O handler padronizado cobre erros de service; erros inesperados genéricos ainda seguem comportamento padrão do FastAPI.
- As heurísticas de simulação de carteira continuam sendo política provisória de MVP.
- Ainda não há worker automático para expiração de recomendações.

## [1.11.5-fix] - 2026-04-26

### Problemas Corrigidos

- Corrigida a compilação do frontend em `bsi-frontend/src/App.tsx`, preservando as abas `signals`, `performance` e `portfolio`.
- Adicionados `bsi-frontend/tsconfig.json` e `bsi-frontend/tsconfig.node.json` compatíveis com Vite/React.
- Corrigido o uso de `title` em ícone `lucide-react` no `PerformanceDashboard`.
- Corrigido o fluxo de pendências para que decisões `DEFERRED` permaneçam rastreáveis e não sejam tratadas como decisão final.
- Ajustado o tratamento de `HOLD`/`NO_ACTION` para não aparecerem como pendências operacionais acionáveis e não aplicarem mutação simulada indevida.
- Corrigida a persistência de `domain` no fluxo de webhook, mantendo `CRYPTO_SPOT` como default apenas quando o campo estiver ausente.
- Corrigidas chamadas ao logger estruturado em `InterpretationService`.
- Corrigido registro de outcome novo para preencher `entry_reference_price` a partir do sinal.
- Removidos artefatos proibidos do pacote final: `.env` ativo, bancos locais, ZIPs internos, `node_modules`, `dist`, `__pycache__` e `*.pyc`.

### Arquivos Alterados

- `bsi-backend/app/schemas/webhook.py`
- `bsi-backend/app/services/webhook_ingestion_service.py`
- `bsi-backend/app/services/decision_service.py`
- `bsi-backend/app/services/interpretation_service.py`
- `bsi-backend/app/services/outcome_service.py`
- `bsi-frontend/src/App.tsx`
- `bsi-frontend/src/components/DecisionCenter.tsx`
- `bsi-frontend/src/components/PerformanceDashboard.tsx`
- `bsi-frontend/tsconfig.json`
- `bsi-frontend/tsconfig.node.json`
- `PROJECT_TREE.txt`
- `README_REVIEW.md`

### Validação

- Backend: `python -m compileall -q bsi-backend` passou.
- Backend: import da aplicação FastAPI passou.
- Backend: `seed_db.py --mode all_demo --clean` passou em SQLite limpo de validação.
- Backend: smoke test do fluxo `webhook -> signal -> interpretation -> outcome -> portfolio -> decision` passou.
- Frontend: `npm install` passou.
- Frontend: `npm run build` passou.

### Riscos Remanescentes

- `npm install` ainda reporta 2 vulnerabilidades moderadas; requer análise com `npm audit` antes de ambiente real.
- As heurísticas de simulação de carteira continuam sendo política provisória de MVP.
- Ainda não há worker automático para expiração de recomendações.
- O pacote segue voltado a demo/auditoria; produção deve restringir CORS e migrar para PostgreSQL conforme documentação.
