# Changelog - Fase 8 FIX

## [Fase 8.1] - Correções Cirúrgicas de Fechamento

### Adicionado
- Suporte a filtragem por `domain` no bloco de Impacto do LLM (Backend & Frontend).
- Documentação explícita sobre limitações da heurística de sessão B3 em `DOMAIN_GUIDE.md`.
- Seção de gerenciamento de seeds por domínio em `DOMAIN_GUIDE.md`.

### Corrigido
- Endpoint `/analytics/llm-impact` agora respeita o parâmetro `domain`.
- Componente `PerformanceDashboard` agora passa o domínio ativo para todas as requisições de analytics.
- Script de auditoria ajustado para garantir exclusão de `.env` ativos e pastas de cache/lixo.

### Segurança & Higiene
- Remoção definitiva de arquivos `.env` ativos e `bsi_demo.db` do pacote de auditoria.
- Saneamento de `__pycache__` e `node_modules` no processo de empacotamento.
